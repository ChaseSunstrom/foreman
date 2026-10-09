"""What became of finished work (T-0616): reverted in git, fixed later by a FIX task that names it, or held; and the
track record that follows (T-0641): per type and tier, how many closed on their first fm task finish and how many held.
Everything is derived on demand from git, the briefs and the ledger, so there is nothing extra to keep in sync."""
import collections
import os
import re
import subprocess

import fmcore as c

_TID = re.compile(r"\bT-\d{4,}\b")
SMOKE_DAYS = 7  # a failing smoke run this soon after a close points at that task (weakly: smoke covers the whole UI)
_VERSION = re.compile(r"\b\d+\.\d+\.\d+\b")  # a release task names what it ships


def reverts(p, n=200):
    """[(date, revert subject, the reverted commit's subject, {task ids named})] from git's Revert commits, newest
    first; [] outside git."""
    try:
        out = subprocess.run(["git", "-C", p.root, "log", f"-n{n}", "--grep=^Revert ", "--format=%cI%x1f%s%x1f%b%x1e"],
                             capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    rows = []
    for rec in out.split("\x1e"):
        parts = rec.strip().split("\x1f")
        if len(parts) == 3:
            orig = (re.match(r'Revert "(.*)"$', parts[1]) or [None, parts[1]])[1]
            rows.append((parts[0], parts[1], orig, set(_TID.findall(parts[1] + " " + parts[2]))))
    return rows


def done_at(b):
    """When the brief was last closed done (its log), else its updated stamp."""
    hits = re.findall(r"(?m)^- (\S+) done\b", b.section("Log"))
    return hits[-1] if hits else str(b.meta.get("updated") or "")


def outcomes(p):
    """{task id: {fate, by, type, tier}} for every done task: "reverted" (a Revert commit names it), "fixed later" (a
    FIX task created after it closed names it), "corrected" (a user correction logged against it after it closed),
    else "held"."""
    briefs = c.load_briefs(p, include_archive=True)
    closed = {b.id: done_at(b) for b in briefs if b.status == "done"}
    reverted = collections.defaultdict(list)
    for _, subj, _, tasks in reverts(p):
        for t in tasks:
            reverted[t].append(subj)
    later = collections.defaultdict(list)
    for f in briefs:
        # ponytail: a FIX naming exactly one finished task is a follow-up fix; releases and batches name several
        # (or a version) and are skipped. Upgrade path: overlap of the two tasks' touched files.
        if f.type != "FIX" or f.status == "dropped" or _VERSION.search(f.title):
            continue
        named = (set(_TID.findall(" ".join([f.title, f.section("Raw request")]))) - {f.id}) & closed.keys()
        if len(named) == 1 and str(f.meta.get("created") or "") >= closed[next(iter(named))]:
            later[next(iter(named))].append(f.id)
    corrected = collections.defaultdict(list)  # T-0602: the user corrected it after it closed
    for e in c.ledger_tail(p, 50000):
        t = e.get("task")
        if e.get("event") == "correction" and t in closed and str(e.get("ts") or "") > closed[t]:
            corrected[t].append(c.fit(str((e.get("data") or {}).get("text") or ""), 100))
    smoked = collections.defaultdict(list)  # T-0743: a smoke run that found defects within a week of the close
    for e in c.ledger_tail(p, 50000):
        if e.get("event") == "smoke" and (e.get("data") or {}).get("defects"):
            at = c.parse_ts(e.get("ts"))
            for t, ts in closed.items():
                done = c.parse_ts(ts)
                if at and done and 0 <= (at - done).total_seconds() <= SMOKE_DAYS * 86400:
                    smoked[t].append(f"smoke {str(e.get('ts'))[:10]}: {e['data']['defects']} defect(s)")
    fate = lambda i: ("reverted" if i in reverted else "fixed later" if i in later else
                      "corrected" if i in corrected else "smoke failed after" if i in smoked else "held")
    return {b.id: {"fate": fate(b.id), "by": reverted.get(b.id) or sorted(later.get(b.id, [])) or corrected.get(b.id, [])
                   or smoked.get(b.id, []),
                   "type": b.type, "tier": b.tier}
            for b in briefs if b.id in closed}


def track(p, outs=None):
    """{(type, tier): Counter(n, first, held)}: first = its first fm task finish ran no failing check."""
    outs = outcomes(p) if outs is None else outs
    first = _first_finish(p)
    rows = collections.defaultdict(collections.Counter)
    for tid, o in outs.items():
        r = rows[(o["type"], o["tier"])]
        r["n"] += 1
        r["first"] += first.get(tid, True)
        r["held"] += o["fate"] == "held"
    return rows


def _row(r):
    return f"{r['first']} of {r['n']} closed on the first finish, {r['held']} of {r['n']} held"


def track_line(p, typ, tier):
    """One line for fm focus: this project's record for the type and tier, once it has two finished tasks."""
    r = track(p).get((typ, tier))
    return f"Track record for {typ} {tier} here: {_row(r)} (no later fix or revert)." if r and r["n"] >= 2 else ""


def track_lines(p, outs=None):
    rows = sorted(track(p, outs).items(), key=lambda kv: -kv[1]["n"])
    return ["Track record (all time; held = no later fix or revert): " + " · ".join(
        f"{t} {tier}: {_row(r)}" for (t, tier), r in rows[:6])] if rows else []


def cmd_outcomes(args):
    import fmcli
    p = fmcli.resolve(args)
    outs = outcomes(p)
    bad = {t: o for t, o in outs.items() if o["fate"] != "held"}
    fates = collections.Counter(o["fate"] for o in bad.values())
    lines = [f"{len(outs)} finished task(s): {len(outs) - len(bad)} held"
             + "".join(f", {n} {k}" for k, n in fates.most_common())]
    lines += [f"- {t} {o['fate']}: {c.fit(', '.join(o['by'][:3]), 140)}" for t, o in sorted(bad.items())[-20:]]
    if getattr(args, "atlas", False):  # T-0620
        return fmcli.out(args, atlas(p, outs), "\n".join(atlas_lines(p, outs)))
    lines += track_lines(p) + calibration_lines(p, outs)
    rows = track(p, outs)
    return fmcli.out(args, {"tasks": outs, "track": {f"{a} {b}": dict(r) for (a, b), r in rows.items()}},
                     "\n".join(lines))


BUCKETS = ((0, 59), (60, 79), (80, 94), (95, 100))


def calibration(p, outs=None):
    """T-0619, one axis: a task's stated confidence (fm task set ID confidence=N, 0-100) that it holds on its first
    finish, against what happened: [(lo, hi, n, ok)] per bucket, and the Brier score (0 is perfect; None without
    data). ok = closed on the first finish and held."""
    outs = outcomes(p) if outs is None else outs
    first = _first_finish(p)
    stated = {b.id: b.meta.get("confidence") for b in c.load_briefs(p, include_archive=True) if b.id in outs}
    pairs = []
    for tid, conf in stated.items():
        try:
            pairs.append((int(conf), first.get(tid, True) and outs[tid]["fate"] == "held"))
        except (TypeError, ValueError):
            continue
    rows = [(lo, hi, sum(lo <= x <= hi for x, _ in pairs), sum(ok for x, ok in pairs if lo <= x <= hi))
            for lo, hi in BUCKETS]
    brier = sum((x / 100 - ok) ** 2 for x, ok in pairs) / len(pairs) if pairs else None
    return [r for r in rows if r[2]], brier


def calibration_lines(p, outs=None):
    rows, brier = calibration(p, outs)
    return ["Calibration (stated confidence → held on the first finish): " + " · ".join(
        f"{lo}–{hi}%: {n} task(s), {ok} held on the first finish ({round(100 * ok / n)}%)" for lo, hi, n, ok in rows)
        + f"; Brier {brier:.2f} (0 is perfect)"] if rows else []


def _first_finish(p):
    first = {}
    for e in c.ledger_tail(p, 50000):
        if e.get("event") == "finish" and e.get("task") and e["task"] not in first:
            first[e["task"]] = not (e.get("data") or {}).get("failed")
    return first


ATLAS_MIN = 3  # tasks before a file or language counts


def atlas(p, outs=None):
    """T-0620: where work tends not to hold. {"files": [...], "languages": [...]}, each row (name, n, bad, weak):
    done tasks that touched it, how many were later fixed or reverted, how many closed with a weak grade; worst first."""
    outs = outcomes(p) if outs is None else outs
    files, langs = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for b in c.load_briefs(p, include_archive=True):
        if b.id not in outs:
            continue
        touched = [x.lstrip("- ").strip() for x in b.section("Files touched").splitlines() if x.strip()]
        bad, weak = outs[b.id]["fate"] != "held", b.meta.get("verified") == "weak"
        for key, group in [(f, files) for f in touched] + [(e, langs) for e in
                                                             {os.path.splitext(f)[1] or "(none)" for f in touched}]:
            r = group[key]
            r["n"], r["bad"], r["weak"] = r["n"] + 1, r["bad"] + bad, r["weak"] + weak

    def rank(group):
        rows = [(k, r["n"], r["bad"], r["weak"]) for k, r in group.items() if r["n"] >= ATLAS_MIN]
        return sorted(rows, key=lambda x: (-(x[2] + x[3]) / x[1], -x[1], x[0]))
    return {"files": rank(files), "languages": rank(langs)}


def atlas_lines(p, outs=None, n=8):
    a = atlas(p, outs)
    out = []
    for title, rows in (("Files", a["files"]), ("Languages", a["languages"])):
        rows = [r for r in rows if r[2] or r[3]][:n]
        out += [f"{title} where work didn't hold (of {ATLAS_MIN}+ tasks):"] + [
            f"- {k}: {bad} of {total} needed a later fix or revert" + (f", {weak} closed weak" if weak else "")
            for k, total, bad, weak in rows] if rows else []
    return out or [f"No file or language with {ATLAS_MIN}+ finished tasks has needed a later fix yet."]


def caution(p, scope):
    """One line for fm focus when the task's scope covers a file where 20%+ of past work (2+ tasks) needed a fix."""
    hits = []
    for k, total, bad, _ in atlas(p)["files"]:
        if bad >= 2 and bad / total >= 0.2 and any(k == s or k.startswith(s.rstrip("/") + "/") for s in scope):
            hits.append(f"{k}: {bad} of {total} tasks that touched it needed a later fix or revert")
    return ("Caution: " + "; ".join(hits[:3]) + " — test its edges first.") if hits else ""
