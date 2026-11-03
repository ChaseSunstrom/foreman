"""M-12 kill test: does a track-record-weighted pool of forecasters beat the best single one on whether a close survives?

Sample (run 2 on): closes 14+ days old, labelled failed when a fix or revert came within 14 days of the close; each
failure with a findable commit is paired with the held close nearest it in id (run 1 drew held closes from an older era
only, so era leaked into the label; its output is m12-run1-confounded.json). Forecasters, each blind to the outcome:
  planner: Haiku reads the brief's title, request and criteria and the diff, posts P(survives 14 days unfixed).
  rival:   Sonnet reads the same, first names the likeliest way it breaks, then posts the probability.
  base:    no model: the held rate of settled closes of the same type and tier (Laplace).
  history: no model: the held rate of settled earlier closes whose commits touched any of the same files (run 3).
Pool: a logarithmic opinion pool, weights 1 / mean log loss on every other row (leave-one-out; a walk-forward pool is
reported beside it), scored by Brier against the hindsight-best single forecaster, with a bootstrap of the margin.
Pass (viable) if the pool's Brier beats the best single forecaster's by 0.02 or more.
Usage: kill_m12.py OUT_JSON [N]. Prints one JSON object; model answers are cached in m12-answers.json beside it."""
import concurrent.futures as cf
import datetime
import json
import math
import os
import random
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "plugin", "lib"))
from sampo import core as c  # noqa: E402
from sampo import ideas  # noqa: E402
from sampo import outcomes  # noqa: E402

OUT = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "m12-answers.json")  # every answer, so a rerun is free
SYSTEM = ("You forecast whether a finished software change will hold. 'Holds' means no later task had to fix or revert "
          "this work within 14 days of its close. End your reply with one line exactly: P = <a probability from 0.01 "
          "to 0.99>")
RIVAL = "First name, in two sentences, the likeliest way this change breaks or needs a follow-up fix. Then forecast."


def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, errors="replace").stdout


def diff(tid):
    shas = git("log", "--all", "--format=%H %P", "-E",  # the task's own commit: its id leads, or ends, a line
               f"--grep=^(Merge )?{tid}([^0-9]|$)|\\({tid}\\)$").splitlines()
    out = []
    for ln in shas[:4]:
        sha, *parents = ln.split()
        out.append(git("diff", "--stat", "--patch", f"{parents[0]}", sha) if parents else "")
    return "\n".join(out)[:7000]


def brief_text(b):
    return (f"Task {b.id} [{b.meta.get('type')} {b.meta.get('tier')}]: {b.title}\n"
            f"Request: {c.fit(c.plain(b.section('Raw request')), 800)}\n"
            f"Acceptance criteria:\n{c.fit(b.section('Acceptance criteria'), 1200)}")


def ask(model, prompt):
    text = ideas.run_child("moonshot-kill", SYSTEM, prompt, model, 300, project="foreman-4a056f",
                             detail="M-12 forecaster") or ""
    m = re.findall(r"P\s*=\s*(0?\.\d+|1(?:\.0+)?|0)", text)
    return min(0.99, max(0.01, float(m[-1]))) if m else None


def logit(x):
    return math.log(x / (1 - x))


def main():
    p = c.find_project(ROOT)
    outs = outcomes.outcomes(p)
    briefs = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    closed_at = {i: str(b.meta.get("updated") or "") for i, b in briefs.items()}
    # Run 2: run 1's held closes were only those whose window had ended, all of them ancient (T-0014..T-0198), so era
    # leaked into the label. Now: the label is the forecast's own question (a fix or revert within 14 days of the
    # close), both classes closed 14+ days ago, and each failure is paired with the held close nearest it in id.
    def when(s):
        try:
            return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        except ValueError:
            return None
    now = datetime.datetime.now(datetime.timezone.utc)
    label = {}
    for i, o in outs.items():
        closed = when(outcomes.done_at(briefs[i])) if i in briefs else None
        if not closed or (now - closed).days < 14:
            continue
        fixes = [when(briefs[f].meta.get("created")) for f in o.get("by") or [] if f in briefs]
        fixes = [f for f in fixes if f]
        label[i] = 0 if any((f - closed).days <= 14 for f in fixes) or (o["fate"] == "reverted" and not fixes) else 1
    rnd = random.Random(12)
    bad = [i for i, y in label.items() if y == 0]
    rnd.shuffle(bad)
    good = sorted((i for i, y in label.items() if y == 1), key=lambda i: int(i[2:]))
    pick, used = [], set()
    for i in bad:
        if len(pick) >= 2 * N:
            break
        if not diff(i).strip():
            continue
        mate = next((g for g in sorted(good, key=lambda g: abs(int(g[2:]) - int(i[2:])))
                     if g not in used and diff(g).strip()), None)
        if mate:
            used.add(mate)
            pick += [(i, 0), (mate, 1)]
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

    closed = {i: when(outcomes.done_at(b)) for i, b in briefs.items() if b.status == "done"}

    def settled(j, i):  # j's 14-day label was known when i closed: no peeking at later fixes
        return j in label and closed.get(j) and closed.get(i) and (closed[i] - closed[j]).days >= 14

    def laplace(js):
        return min(0.99, max(0.01, (sum(label[j] for j in js) + 1) / (len(js) + 2)))

    def base(i):  # the held rate of settled closes of the same type and tier
        b = briefs[i]
        return laplace([j for j in label if settled(j, i) and briefs[j].meta.get("type") == b.meta.get("type")
                        and briefs[j].meta.get("tier") == b.meta.get("tier")])

    files = {}  # task id -> files its own commits touched, from one pass over the history
    tid = re.compile(r"^(?:Merge )?(T-\d{4,})(?:[^0-9]|$)|\((T-\d{4,})\)$")
    cur = None
    for ln in git("log", "--all", "--format=%x00%s", "--name-only", "-m", "--first-parent").splitlines():
        if ln.startswith("\0"):
            m = tid.search(ln[1:])
            cur = (m.group(1) or m.group(2)) if m else None
        elif ln.strip() and cur:
            files.setdefault(cur, set()).add(ln.strip())

    def history(i):  # run 3: the held rate of settled earlier closes that touched any of the same files
        mine = files.get(i) or set()
        return laplace([j for j in label if settled(j, i) and files.get(j, set()) & mine])

    jobs = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for i, _ in pick:
            text = brief_text(briefs[i]) + "\n\nThe change:\n" + diff(i)
            for name, model, prompt in (("planner", "haiku", text), ("rival", "sonnet", RIVAL + "\n\n" + text)):
                key = f"{i}:{name}"
                if key not in cache:
                    jobs[ex.submit(ask, model, prompt)] = key
        for f in cf.as_completed(jobs):
            cache[jobs[f]] = f.result()
            json.dump(cache, open(CACHE, "w"))
    rows = [{"id": i, "y": y, "planner": cache.get(f"{i}:planner"), "rival": cache.get(f"{i}:rival"), "base": base(i),
             "history": history(i)}
            for i, y in pick]
    rows = [r for r in rows if r["planner"] is not None and r["rival"] is not None]
    names = ("planner", "rival", "base", "history")
    ll = lambda name, rs: sum(-math.log(r[name] if r["y"] else 1 - r[name]) for r in rs) / len(rs)  # noqa: E731
    brier = lambda ps, rs: sum((q - r["y"]) ** 2 for q, r in zip(ps, rs)) / len(rs)  # noqa: E731

    def pooled(r, rest):  # leave-one-out: the weights never see the row they forecast
        w = {n: 1 / ll(n, rest) for n in names}
        return 1 / (1 + math.exp(-sum(w[n] * logit(r[n]) for n in names) / sum(w.values())))
    pool = [pooled(r, rows[:k] + rows[k + 1:]) for k, r in enumerate(rows)]
    by_id = sorted(range(len(rows)), key=lambda k: int(rows[k]["id"][2:]))  # walk-forward: earlier closes only
    walk = {}
    for n_, k in enumerate(by_id):
        before = [rows[j] for j in by_id[:n_]]
        walk[k] = pooled(rows[k], before) if len(before) >= 10 else \
            1 / (1 + math.exp(-sum(logit(rows[k][n]) for n in names) / len(names)))
    walk = [walk[k] for k in range(len(rows))]
    single = {n: round(brier([r[n] for r in rows], rows), 4) for n in names}
    top = min(single, key=single.get)
    margin = single[top] - brier(pool, rows)
    boot = []  # how often a resample of the rows keeps the margin at 0.02 or more
    for _ in range(2000):
        ix = [rnd.randrange(len(rows)) for _ in rows]
        rs = [rows[k] for k in ix]
        boot.append(brier([r[top] for r in rs], rs) - brier([pool[k] for k in ix], rs))
    boot.sort()
    res = {"sample": {"failed": sum(1 for r in rows if not r["y"]), "held": sum(1 for r in rows if r["y"])},
           "weights_all": {n: round(1 / ll(n, rows), 3) for n in names}, "brier_single": single, "best_single": top,
           "brier_pool": round(brier(pool, rows), 4), "margin": round(margin, 4),
           "margin_90": [round(boot[100], 4), round(boot[1899], 4)],
           "share_resamples_margin_ge_0.02": round(sum(b >= 0.02 for b in boot) / len(boot), 3),
           "brier_pool_walk_forward": round(brier(walk, rows), 4),
           "auc": {n: round(sum((a[n] > b[n]) + 0.5 * (a[n] == b[n]) for a in rows if a["y"] for b in rows if not b["y"])
                         / max(1, sum(r["y"] for r in rows) * sum(not r["y"] for r in rows)), 3) for n in names},
           "verdict": "viable" if margin >= 0.02 else "not-yet"}
    json.dump({"result": res, "rows": rows}, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1))


main()
