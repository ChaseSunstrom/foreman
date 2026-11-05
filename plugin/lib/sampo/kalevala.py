"""Kalevala (T-3050, T-3081): one Rune tower per aspect, run together. Each tower is rune's --tower home
(research/genesis/towers/NAME: its own gen-0, docs and steers); Kalevala's own state, its manifest and its generations,
sits in research/genesis/kalevala. Moons, exam scenarios and the user's steers stay shared at the root."""
import concurrent.futures
import contextlib
import fcntl
import json
import os
import re
import subprocess
import sys

from sampo import budget
from sampo import core as c
from sampo import moonscale
from sampo import rune

FIXED = ("problem solving", "memory", "efficiency")  # the aspects every project gets, open coverage or not


def home(p):
    return os.path.join(rune.root(p), "kalevala")


def _manifest(p):
    return os.path.join(home(p), "manifest.json")


def load(p):
    """The manifest. A damaged one raises (json's ValueError): start never overwrites it from scratch."""
    if not os.path.exists(_manifest(p)):
        return {"towers": {}}
    with open(_manifest(p), encoding="utf-8") as f:
        return json.load(f)


def _save(p, m):
    os.makedirs(home(p), exist_ok=True)
    c.write_atomic(_manifest(p), json.dumps(m, indent=2, sort_keys=True) + "\n")


def tower_name(aspect):
    """A tower name from an aspect: lowercase words joined by '-', at most 24 characters (rune.TOWER_NAME), a letter
    first, never 'root'."""
    s = re.sub(r"[^a-z0-9]+", "-", aspect.lower()).strip("-")[:24].rstrip("-")
    if not rune._valid(s):
        s = ("aspect-" + s).strip("-")[:24].rstrip("-")
    return s


def aspects(p):
    """[(aspect, name)]: each coverage.md area with open coverage (an empty cell or an idea), then the fixed three.
    The first aspect to a name keeps it; a later one with the same name is left out."""
    cov = rune.coverage(p, rune._doc(rune.root(p), "coverage.md"))
    names = [r["area"] for r in cov["rows"] if r["empty"] or r["ideas"]]
    out, taken = [], set()
    for aspect in names + list(FIXED):
        name = tower_name(aspect)
        if name not in taken:
            taken.add(name)
            out.append((aspect, name))
    return out


def tower_rows(p):
    """Each opened tower: its aspect, whether its gen-0 still matches its seal, and its generation and verdicts."""
    info = {r["name"]: r for r in rune.towers(p)}
    out = []
    for name, t in sorted(load(p)["towers"].items()):
        rune.set_tower(name)
        try:
            sealed = rune.sealed(p) == ""
        finally:
            rune.set_tower(None)
        r = info.get(name, {})
        out.append({"name": name, "aspect": t["aspect"], "sealed": sealed, "generation": r.get("generation"),
                    "select": r.get("select"), "drift": r.get("drift")})
    return out


def start(p):
    """Open a tower for each aspect that has none yet: its gen-0 is the root's sealed gen-0 plus the aspect."""
    bad = rune.sealed(p)
    if bad:  # the root's gen-0 comes first; every tower's gen-0 extends it
        raise ValueError(f"the root gen-0 isn't sealed ({bad}): fm genesis init --file GEN0 first")
    with open(os.path.join(rune.root(p), "gen-0.md"), "rb") as f:
        root = f.read()
    opened, skipped = [], []
    for aspect, name in aspects(p):
        if name in load(p)["towers"]:
            skipped.append(name)
            continue
        gen0 = root + f"\n## Aspect\n{aspect}: this tower's focus; its generations work this aspect's gaps first.\n".encode()
        rune.set_tower(name)  # rune.init takes its own lock, so it runs outside ours
        try:
            rune.init(p, gen0)
        finally:
            rune.set_tower(None)
        with c.lock(p.dir):
            m = load(p)
            m["towers"][name] = {"aspect": aspect}
            _save(p, m)
        opened.append(name)
    return {"towers": tower_rows(p), "opened": opened, "skipped": skipped}


FEATURE = "kalevala"  # Kalevala's own budget line: each tower step is charged here, its share of the day cap
EST_JOB = 0.25  # USD per tower step until the feature has its own recent runs (budget.estimate)
MAX_STEPS = 200  # the manifest's step log keeps the newest this many
JOB_TIMEOUT = 3 * 3600  # one genesis step, as night.py's jobs
JOB_VERBS = {"spec": False, "seed": True, "select": True}  # the stages run as jobs; True: the CLI takes a generation


class Busy(RuntimeError):
    """A tower's step is already running: its lock is held."""


@contextlib.contextmanager
def tower_lock(p, name):
    """One step per tower at a time: a non-blocking flock on the tower's lock file under Kalevala's home."""
    os.makedirs(home(p), exist_ok=True)
    with open(os.path.join(home(p), f"{name}.lock"), "a") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise Busy(name) from None
        yield


def order(rows):
    """Thinnest first: the lowest generation, then the name."""
    return [r["name"] for r in sorted(rows, key=lambda r: (r.get("generation") or 0, r["name"]))]


def job_argv(name, st):
    """The genesis job for a tower's next step, or None when its command isn't one a job runs (gen-1's seed is a put
    the main thread makes). The command names the generation: seed N writes gen-N/seed.md, select N judges gen N."""
    tok = st["command"].split()
    if len(tok) < 3 or tok[1] != "genesis" or tok[2] not in JOB_VERBS:  # rune's commands: the CLI name, then genesis
        return None
    argv = [sys.executable, os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "genesis", tok[2]]
    if JOB_VERBS[tok[2]]:
        if len(tok) < 4 or not tok[3].isdigit():
            return None
        argv.append(tok[3])
    return argv + ["--tower", name]


def plan(names, slots, fit):
    """(run now, queued, K): the first `fit` towers run, the rest wait; at most `slots` run at once."""
    if names and fit < 1:
        raise budget.BudgetError("kalevala: today's share of the budget is spent, no tower step fits; "
                                 "or raise it: fm budget set --day N --because \"<why>\"")
    run = names[:max(fit, 0)]
    return run, names[len(run):], min(max(slots, 1), len(run))


def share():
    """Kalevala's share of the day cap: half of it (of the cap as the economy leaves it), for all its towers' steps."""
    return budget.effective()[0]["day"] * 0.5


def spent_today():
    return round(sum(float(e.get("usd") or 0) for e in budget.ledger() if e.get("feature") == FEATURE), 4)


def _slots(p):
    prof = moonscale._local(bool(c.read_meta(p).get("sensitive")))
    return max(int(prof.get("slots") or 1), 1) if prof else 1


def _stage(p, name):
    """The tower's next action (rune.step, read-only), read with the tower's home in place."""
    rune.set_tower(name)
    try:
        return rune.step(p)
    finally:
        rune.set_tower(None)


def _run(argv, cwd, env):
    return subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=JOB_TIMEOUT).returncode


def _held(p, name):
    try:
        with tower_lock(p, name):
            return False
    except Busy:
        return True


def _headroom(p, runnable, k):
    """(USD per step, run now, queued, K): the least that Kalevala's share, the day's cap and this command's cap leave."""
    est = budget.estimate(FEATURE, 1, EST_JOB)
    cur, _ = budget.effective(p)
    left = min(share() - spent_today(), cur["day"] - budget.spent()[0], cur["run"] - budget.RUN["usd"])
    return (est,) + plan(runnable, k or _slots(p), int(left // est) if left > 0 else 0)


def _job(p, name, st, argv, env, runner):
    at = c.now()
    try:
        rc = runner(argv, p.root, env)
    except Exception:  # a timeout or a missing interpreter fails this tower's step; the others go on
        rc = -1
    return {"tower": name, "stage": st["stage"], "status": "ran" if rc == 0 else "failed", "rc": rc, "at": at}


def step(p, k=None, runner=None, dry_run=False):
    """Each opened tower's next genesis step as a job: at most K at once, one step per tower at a time, inside
    Kalevala's share of the day's budget. Towers past the share wait, thinnest first. The round goes in the manifest."""
    runner = runner or _run
    budget.check(FEATURE, EST_JOB)  # the day and per-command caps still hold for Kalevala
    env = dict(os.environ, FOREMAN_NO_BACKGROUND="1", FOREMAN_TOWER_READONLY_EXAM="1", FOREMAN_SPEND_AS=FEATURE)
    with contextlib.ExitStack() as held:  # a round holds the locks of the towers it charges until their jobs end
        with c.lock(p.dir):  # stages, plan and charges under one lock: no stale stage, no two steps on one headroom
            names = order(tower_rows(p))
            stages = {n: _stage(p, n) for n in names}
            argvs = {n: job_argv(n, stages[n]) for n in names}
            runnable = [n for n in names if argvs[n] and stages[n]["kind"] == "ok"]
            at = c.now()
            skipped = [{"tower": n, "stage": stages[n]["stage"], "status": "skipped", "rc": None, "at": at}
                       for n in names if n not in runnable]
            est, run, queued, width = _headroom(p, runnable, k)
            if dry_run:
                results = [{"tower": n, "stage": stages[n]["stage"], "status": "planned"} for n in run]
                return {"dry_run": True, "k": width, "est": est, "share": round(share(), 4), "spent": spent_today(),
                        "results": results + skipped, "queued": queued, "rounds": load(p).get("rounds", 0)}
            busy, charged = [], []
            for n in run:  # a tower another step holds is busy and uncharged; the rest are charged before their jobs start
                try:
                    held.enter_context(tower_lock(p, n))
                except Busy:
                    busy.append(n)
                    continue
                budget.record(FEATURE, usd=est, runs=1, project=p.slug, detail=f"{n} {stages[n]['stage']}")
                charged.append(n)
        done = [{"tower": n, "stage": stages[n]["stage"], "status": "busy", "rc": None, "at": at} for n in busy]
        try:
            if charged:
                with concurrent.futures.ThreadPoolExecutor(max_workers=width) as ex:
                    futs = [ex.submit(_job, p, n, stages[n], argvs[n], env, runner) for n in charged]
                    done += [f.result() for f in futs]
        finally:  # each job's own spend is charged under FEATURE by its child; the estimate given back leaves the real cost
            for n in charged:
                budget.record(FEATURE, usd=-est, runs=0, project=p.slug, detail=f"settle {n}")
    done += skipped
    with c.lock(p.dir):
        m = load(p)
        m["rounds"] = m.get("rounds", 0) + 1
        m["steps"] = (m.get("steps", []) + done)[-MAX_STEPS:]
        _save(p, m)
    return {"dry_run": False, "k": width, "est": est, "share": round(share(), 4), "spent": spent_today(),
            "results": done, "queued": queued, "rounds": m["rounds"]}


AGENT = "foreman"  # the exam lines Kalevala reads are the ones fm exam grade stamps for this agent


def _tower_scores(p, names):
    """{tower: closed train scenarios on its newest graded run, or None when it has none}: rune's own reading of
    each tower's exam lines (the train split; a scenario counts only if every graded line of the run closed it)."""
    out = {}
    for name in names:
        rune.set_tower(name)
        try:
            lines = [x for x in rune.exam_lines(p, AGENT) if x.get("split") != "holdout"]
        finally:
            rune.set_tower(None)
        if not lines:
            out[name] = None
            continue
        run = lines[-1].get("run")
        out[name] = len(rune.train_scenarios([x for x in lines if x.get("run") == run]))
    return out


CAPS_FILE = "capabilities.md"  # written into each set tower's home; rune._seed carries it as a seed section
CAPS_MAX = 30  # the newest this many go into a tower's seed; the registry keeps every one
BEHAVIOUR = ("ideas", "think", "review", "plan", "memory", "recall", "prompt", "skills")  # what a close can change
NOT_BEHAVIOUR = ("plugin/tests/", "docs/")


def behaviour(files):
    """The Sampo behaviour areas a closed task's files touch (T-3081 step 4), sorted; [] when none. A word of the path
    (split on non-alphanumerics) names an area, or its plural: plan.py counts, planet.py doesn't. ponytail: word match,
    not a path map; upgrade: an explicit path map once a word misleads."""
    out = set()
    for f in files:
        if not f.startswith(NOT_BEHAVIOUR):
            words = set(re.split(r"[^a-z0-9]+", f.lower()))
            out.update(a for a in BEHAVIOUR if a in words or a + "s" in words)
    return sorted(out)


def registry(p):
    """Every closed task whose close changed Sampo's behaviour (its task_done row carries areas), oldest first, once."""
    seen, out = set(), []
    for e in c.ledger_events(p, ["task_done"]):
        d, task = e.get("data") or {}, e.get("task")
        if d.get("areas") and task and task not in seen:
            seen.add(task)
            out.append({"task": task, "title": d.get("title") or task, "areas": list(d["areas"]), "at": e.get("ts")})
    return out


def _caps_text(caps):
    """A tower's capabilities.md: the newest CAPS_MAX registry rows, one line each (titles folded to one line)."""
    return ("Sampo's closed work that changed how it behaves since gen-0, newest last. Use each one; never rebuild it.\n\n"
            + "".join(f"- {x['task']} ({' '.join(c.plain(x['title']).split())[:120]}): {', '.join(x['areas'])}\n"
                      for x in caps[-CAPS_MAX:]))


def _caps_path(p, name):
    return os.path.join(rune.root(p), "towers", name, CAPS_FILE)


def _gen_result(n, g):
    return {"gen": n, **{k: g[k] for k in ("verdict", "base", "reason", "scores")}, "helped": g.get("helped", {})}


def gen(p):
    """Kalevala's next generation: the tower set (every opened tower with a sealed gen-0) and each tower's setup, in
    gen-N/setup.md. The parent gen must be selected first, so each one builds on a judged one."""
    with c.lock(p.dir):
        m = load(p)
        done = m.get("gens", {})
        n = max((int(k) for k in done), default=0) + 1
        if n > 1 and "verdict" not in done[str(n - 1)]:
            raise ValueError(f"kalevala gen {n - 1} isn't selected yet: fm kalevala select {n - 1} first")
        rows = [t for t in tower_rows(p) if t["sealed"]]
        if not rows:
            raise ValueError("no sealed tower to set: fm kalevala start first")
        based = done[str(n - 1)]["base"] if n > 1 else "root gen-0"
        text = (f"# Setup\n\nGen: {n}\nBased on: {based}\n\nTowers this gen runs; select compares them with gen {n - 1} "
                f"on the towers both scored:\n" + "".join(f"- {t['name']}: {t['aspect']} (tower gen {t['generation']})\n"
                                                         for t in rows))
        caps = registry(p)  # step 4: every set tower's next seed carries the registry (rune._seed's section)
        ids = [x["task"] for x in caps]
        had = done[str(n - 1)].get("capabilities", []) if n > 1 else []
        if caps:
            for t in rows:
                c.write_atomic(_caps_path(p, t["name"]), _caps_text(caps))
        os.makedirs(os.path.join(home(p), f"gen-{n}"), exist_ok=True)
        c.write_atomic(os.path.join(home(p), f"gen-{n}", "setup.md"), text)
        done[str(n)] = {"set": [t["name"] for t in rows], "based_on": based, "at": c.now(), "capabilities": ids,
                        "new_capabilities": [i for i in ids if i not in had]}
        m["gens"] = done
        _save(p, m)
    return {"gen": n, "set": done[str(n)]["set"], "based_on": based,
            "new_capabilities": done[str(n)]["new_capabilities"]}


def select(p, n):
    """Judge Kalevala's gen n by the towers' combined exam results: the closed train scenarios summed over the towers
    both gens scored. Kept when that sum beats gen n-1's on them, reverted otherwise (the seed base then the parent's).
    Gen 1, or a gen sharing no scored tower with its parent, is the baseline. Writes gen-n/select.md and Kalevala's own
    lineage.md. A judged gen is returned as it stands."""
    with c.lock(p.dir):
        m = load(p)
        done = m.get("gens", {})
        g = done.get(str(n))
        if g is None:
            raise ValueError(f"no kalevala gen {n}: fm kalevala gen first")
        if "verdict" in g:
            return _gen_result(n, g)
        scores = _tower_scores(p, g["set"])
        if all(v is None for v in scores.values()):
            raise ValueError(f"no tower in gen {n} has a graded exam line: fm exam run RUN --agent {AGENT} in each "
                             f"tower, then fm kalevala select {n}")
        prev = done.get(str(n - 1)) if n > 1 else None
        common = [t for t in g["set"] if scores[t] is not None and prev and prev["scores"].get(t) is not None]
        if not common:
            verdict, base = "baseline", f"gen-{n}"
            why = f"no tower graded in gen {n - 1} as well: gen {n} is the baseline"
        else:
            now, before = sum(scores[t] for t in common), sum(prev["scores"][t] for t in common)
            verdict, base = ("kept", f"gen-{n}") if now > before else ("reverted", prev["base"])
            why = f"closed {now} train scenario(s) across {', '.join(common)}; gen {n - 1} closed {before} on them"
        # step 4: gen n-1's new capabilities went into the towers' seeds; did each tower that scored both gens rise?
        helped = {}
        if prev and prev.get("new_capabilities"):
            helped = {t: {"new": list(prev["new_capabilities"]), "rose": scores[t] > prev["scores"][t]} for t in common}
        g.update(scores=scores, verdict=verdict, base=base, reason=why, judged=c.now(), helped=helped)
        os.makedirs(os.path.join(home(p), f"gen-{n}"), exist_ok=True)
        c.write_atomic(os.path.join(home(p), f"gen-{n}", "select.md"),
                       f"# Select\n\nGen: {n}\nVerdict: {verdict}\nSeed base: {base}\nReason: {why}\n"
                       f"Scores: {json.dumps(scores, sort_keys=True)}\nHelped: {json.dumps(helped, sort_keys=True)}\n")
        lin = os.path.join(home(p), "lineage.md")
        old = "# Lineage\n"
        if os.path.exists(lin):
            with open(lin, encoding="utf-8") as f:
                old = f.read()
        if f"## gen-{n}\n" not in old:  # a judged gen's section is written once, even if a later save failed
            c.write_atomic(lin, old.rstrip("\n") + f"\n\n## gen-{n}\n- {verdict}: {why}\n- seed base: {base}\n")
        m["gens"] = done
        _save(p, m)
    return _gen_result(n, g)


def cmd_kalevala(args):
    from sampo import cli as scli
    p = scli.resolve(args)
    action = args.action or "status"
    if action == "start":
        r = start(p)
        return scli.out(args, r, f"opened {len(r['opened'])} tower(s), {len(r['skipped'])} already open"
                                 + "".join(f"\n  {t['name']}: {t['aspect']}" for t in r["towers"]))
    if action == "status":
        r = {"towers": tower_rows(p)}
        return scli.out(args, r, "\n".join(f"{t['name']}: {t['aspect']} (sealed: {t['sealed']})" for t in r["towers"])
                        or "no towers yet: sampo kalevala start")
    if action == "step":
        r = step(p, k=args.k, dry_run=args.dry_run)
        head = (f"dry run: " if r["dry_run"] else "") + (f"{len(r['results'])} tower(s), at most {r['k']} at once; "
                f"Kalevala's share ${r['share']:.2f} today, ${r['spent']:.2f} spent")
        return scli.out(args, r, head + "".join(f"\n  {x['tower']}: {x['status']} ({x['stage']})" for x in r["results"])
                        + (f"\n  queued past the share, thinnest first: {', '.join(r['queued'])}" if r["queued"] else ""))
    if action == "gen":
        r = gen(p)
        return scli.out(args, r, f"kalevala gen {r['gen']}: {len(r['set'])} tower(s), based on {r['based_on']}; "
                                 f"select it after its steps: fm kalevala select {r['gen']}")
    if action == "select":
        if args.n is None:
            raise scli.UsageError("kalevala select needs the generation: fm kalevala select N")
        r = select(p, args.n)
        return scli.out(args, r, f"kalevala gen {r['gen']}: {r['verdict']}, seed base {r['base']}; {r['reason']}")
    raise scli.UsageError(f"unknown kalevala action {action!r}")
