"""What became of finished work (T-0616): reverted in git, fixed later by a FIX task that names it, or held; and the
track record that follows (T-0641): per type and tier, how many closed on their first fm task finish and how many held.
Everything is derived on demand from git, the briefs and the ledger, so there is nothing extra to keep in sync."""
import collections
import re
import subprocess

import fmcore as c

_TID = re.compile(r"\bT-\d{4,}\b")
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
    FIX task created after it closed names it), else "held"."""
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
    return {b.id: {"fate": "reverted" if b.id in reverted else "fixed later" if b.id in later else "held",
                   "by": reverted.get(b.id) or sorted(later.get(b.id, [])), "type": b.type, "tier": b.tier}
            for b in briefs if b.id in closed}


def track(p, outs=None):
    """{(type, tier): Counter(n, first, held)}: first = its first fm task finish ran no failing check."""
    outs = outcomes(p) if outs is None else outs
    first = {}
    for e in c.ledger_tail(p, 50000):
        if e.get("event") == "finish" and e.get("task") and e["task"] not in first:
            first[e["task"]] = not (e.get("data") or {}).get("failed")
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


def track_lines(p):
    rows = sorted(track(p).items(), key=lambda kv: -kv[1]["n"])
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
    lines += track_lines(p)
    rows = track(p, outs)
    return fmcli.out(args, {"tasks": outs, "track": {f"{a} {b}": dict(r) for (a, b), r in rows.items()}},
                     "\n".join(lines))
