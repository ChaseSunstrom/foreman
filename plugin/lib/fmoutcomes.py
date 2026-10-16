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
SURVIVE_DAYS = 30  # T-1060: a close survives when nothing undid it this long after
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
    closed = {b.id: done_at(b) for b in briefs if b.status == "done" and not b.meta.get("done_in")}  # T-0852: a
    # task folded into another has no close of its own: its host's record is the one that counts
    reverted, when = collections.defaultdict(list), collections.defaultdict(list)  # when: T-1060, each bad event's time
    for at, subj, _, tasks in reverts(p):
        for t in tasks:
            reverted[t].append(subj)
            when[t].append((_ts(at), "reverted"))
    later = collections.defaultdict(list)
    for f in briefs:
        # ponytail: a FIX naming exactly one finished task is a follow-up fix; releases and batches name several
        # (or a version) and are skipped. Upgrade path: overlap of the two tasks' touched files.
        if f.type != "FIX" or f.status == "dropped" or _VERSION.search(f.title):
            continue
        named = (set(_TID.findall(" ".join([f.title, f.section("Raw request")]))) - {f.id}) & closed.keys()
        if len(named) == 1 and str(f.meta.get("created") or "") >= closed[next(iter(named))]:
            later[next(iter(named))].append(f.id)
            when[next(iter(named))].append((_ts(f.meta.get("created")), f"fixed by {f.id}"))
    corrected = collections.defaultdict(list)  # T-0602: the user corrected it after it closed
    events = c.ledger_events(p, ("correction", "smoke"))  # T-1060 review: the archived months too
    for e in events:
        t = e.get("task")
        if e.get("event") == "correction" and t in closed and str(e.get("ts") or "") > closed[t]:
            corrected[t].append(c.fit(str((e.get("data") or {}).get("text") or ""), 100))
            when[t].append((_ts(e.get("ts")), "corrected"))
    smoked = collections.defaultdict(list)  # T-0743: a smoke run that found defects within a week of the close
    for e in events:
        if e.get("event") == "smoke" and (e.get("data") or {}).get("defects"):
            at = c.parse_ts(e.get("ts"))
            for t, ts in closed.items():
                done = c.parse_ts(ts)
                if at and done and 0 <= (at - done).total_seconds() <= SMOKE_DAYS * 86400:
                    smoked[t].append(f"smoke {str(e.get('ts'))[:10]}: {e['data']['defects']} defect(s)")
                    # no survival loss: smoke covers the whole UI, too weak a link to grade a task lost for good
    fate = lambda i: ("reverted" if i in reverted else "fixed later" if i in later else
                      "corrected" if i in corrected else "smoke failed after" if i in smoked else "held")
    return {b.id: {"fate": fate(b.id), "by": reverted.get(b.id) or sorted(later.get(b.id, [])) or corrected.get(b.id, [])
                   or smoked.get(b.id, []),
                   "type": b.type, "tier": b.tier, **_survival(closed[b.id], when.get(b.id, []))}
            for b in briefs if b.id in closed}


def _ts(s):
    """A time from a ledger/brief stamp (UTC Z) or git's %cI (with an offset); None when unreadable."""
    t = c.parse_ts(s) if s else None
    if t is None and s:
        import datetime
        try:
            t = datetime.datetime.fromisoformat(str(s)).astimezone(datetime.timezone.utc)
        except ValueError:
            t = None
    return t


def _survival(closed_at, bad):
    """T-1060 (wild C1, 'grade closed work by whether it survived'): survived (nothing undid it within SURVIVE_DAYS of
    the close), lost (the first thing that did, and when), or settling (days left in the window)."""
    import datetime
    t0 = _ts(closed_at)
    if not t0:
        return {"survival": "unknown"}
    end = t0 + datetime.timedelta(days=SURVIVE_DAYS)
    now = datetime.datetime.now(datetime.timezone.utc)
    hits = sorted((at, why) for at, why in bad if at and t0 <= at <= min(end, now))  # a future-dated commit waits
    if hits:
        return {"survival": "lost", "lost_at": c.iso(hits[0][0].timestamp()), "lost_by": hits[0][1]}
    left = (end - now).total_seconds() / 86400
    return {"survival": "survived"} if left <= 0 else {"survival": "settling", "days_left": int(left) + 1}


def survival_lines(p, outs=None):
    """One line: how the closes graded, and the days since the last lost one (an accident-free counter)."""
    import datetime
    outs = outcomes(p) if outs is None else outs
    n = collections.Counter(o.get("survival") for o in outs.values())
    if not outs:
        return []
    lost = [_ts(o["lost_at"]) for o in outs.values() if o.get("lost_at")]
    since = (f"days since a lost task: {max(0, (datetime.datetime.now(datetime.timezone.utc) - max(lost)).days)}" if lost
             else "no lost task yet")
    return [f"Survival ({SURVIVE_DAYS} days): {n['survived']} survived, {n['lost']} lost, {n['settling']} settling; {since}"]


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
    if getattr(args, "readme", False):  # T-0960: the one sentence a README publishes
        held = sum(o["fate"] == "held" for o in outs.values())
        ungraded = sum(1 for b in c.load_briefs(p, include_archive=True) if b.id in outs and not b.meta.get("verified"))
        return fmcli.out(args, {"held": held, "closed": len(outs), "ungraded": ungraded},
                         f"{held} of {len(outs)} closed tasks held; {ungraded} ungraded.")
    bad = {t: o for t, o in outs.items() if o["fate"] != "held"}
    fates = collections.Counter(o["fate"] for o in bad.values())
    lines = [f"{len(outs)} finished task(s): {len(outs) - len(bad)} held"
             + "".join(f", {n} {k}" for k, n in fates.most_common())]
    lines += [f"- {t} {o['fate']}: {c.fit(', '.join(o['by'][:3]), 140)}" for t, o in sorted(bad.items())[-20:]]
    if getattr(args, "atlas", False):  # T-0620
        return fmcli.out(args, atlas(p, outs), "\n".join(atlas_lines(p, outs)))
    for flag in ("settle", "claims", "regret", "graveyard", "seen"):  # T-1060: reports that read the 30-day grades
        if getattr(args, flag, False):
            res = globals()["_" + flag](p, outs)
            return fmcli.out(args, res, "\n".join(res["lines"]))
    lines += survival_lines(p, outs) + track_lines(p) + calibration_lines(p, outs)
    rows = track(p, outs)
    return fmcli.out(args, {"tasks": outs, "track": {f"{a} {b}": dict(r) for (a, b), r in rows.items()}},
                     "\n".join(lines))


def _settle(p, outs):
    """One `outcome` ledger event per task whose window has closed (survived or lost), once per task."""
    done = {e.get("task") for e in c.ledger_events(p, ("outcome",))}
    new = [(t, o) for t, o in sorted(outs.items()) if o.get("survival") in ("survived", "lost") and t not in done]
    for t, o in new:
        c.log_event(p, "outcome", task=t, data={k: o[k] for k in ("survival", "lost_at", "lost_by", "fate") if k in o})
    return {"graded": [t for t, _ in new], "lines": [f"{len(new)} graded"]
            + [f"- {t} {o['survival']}" + (f": {o['lost_by']}" if o.get("lost_by") else "") for t, o in new[-20:]]}


def _graded(p, outs):
    return {b.id: b for b in c.load_briefs(p, include_archive=True) if b.id in outs
            and outs[b.id].get("survival") in ("survived", "lost")}


def _claims(p, outs):
    """Did a strong close survive more often than a weak one? Survival by the grade the finish recorded."""
    rows = collections.defaultdict(lambda: [0, 0])
    for t, b in _graded(p, outs).items():
        r = rows[str(b.meta.get("verified") or "ungraded")]
        r[0] += 1
        r[1] += outs[t]["survival"] == "survived"
    return {"by_grade": {k: {"graded": n, "survived": ok} for k, (n, ok) in rows.items()},
            "lines": ["Survival by close grade:"] + ([f"- {k}: {ok} of {n} survived" for k, (n, ok) in sorted(rows.items())]
                                                     or [f"- nothing graded yet: a close is graded {SURVIVE_DAYS} days on"])}


def _regret(p, outs):
    """Lost tasks with the approach they took, and the decisions a later one reversed."""
    import fmcost
    lost = [(t, b) for t, b in _graded(p, outs).items() if outs[t]["survival"] == "lost"]
    lines = [f"Lost within {SURVIVE_DAYS} days ({len(lost)}):"] + [
        f"- {t} {c.fit(c.plain(b.title), 60)}: {outs[t].get('lost_by')}; approach: "
        f"{c.fit(c.plain(' '.join(b.section('Approach').split())) or '(none written)', 120)}" for t, b in lost[-15:]]
    rev = fmcost.reversals(p)
    lines += ["Decisions reversed, by kind: " + " · ".join(f"{k}: {r} of {n}" for k, (n, r) in rev.items())] \
        if any(r for _, r in rev.values()) else []
    return {"lost": [t for t, _ in lost], "lines": lines}


def _graveyard(p, outs):
    """What didn't make it: lost closes and dropped tasks."""
    lost = [t for t, o in outs.items() if o.get("survival") == "lost"]
    briefs = c.load_briefs(p, include_archive=True)
    dropped = [b for b in briefs if b.status == "dropped"]
    by = {b.id: b for b in briefs if b.id in lost}
    lines = [f"Lost ({len(lost)}):"] + [f"- {t} {c.fit(c.plain(by[t].title), 60)}: {outs[t].get('lost_by')}"
                                        for t in sorted(lost)[-15:] if t in by]
    lines += [f"Dropped ({len(dropped)}):"] + [f"- {b.id} {c.fit(c.plain(b.title), 60)}" for b in dropped[-15:]]
    return {"lost": sorted(lost), "dropped": [b.id for b in dropped], "lines": lines}


def _seen(p, outs):
    """Did a correction during the task (the user steering it) make it more or less likely to survive?"""
    graded = _graded(p, outs)
    during = {e.get("task") for e in c.ledger_events(p, ("correction",)) if e.get("task") in graded
              and str(e.get("ts") or "") <= str(done_at(graded[e["task"]]) or "")}
    rows = {k: [t for t in graded if (t in during) == k] for k in (True, False)}
    lines = [f"- {'corrected during the task' if k else 'not corrected'}: "
             f"{sum(outs[t]['survival'] == 'survived' for t in ts)} of {len(ts)} survived" for k, ts in rows.items()]
    return {"corrected": sorted(rows[True]), "lines": ["Survival by whether the user corrected the task:"] + lines}


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
    out = ("Caution: " + "; ".join(hits[:3]) + " — test its edges first.") if hits else ""
    try:  # wild C18: files git history keeps fixing; the map is a hint, it never stops a focus
        import fmmap
        hot = [f for f in fmmap.load(p).get("fixy", []) if any(f == s or f.startswith(s.rstrip("/") + "/") for s in scope)]
    except Exception:
        hot = []
    return "\n".join(filter(None, [out, ("Hotspot: " + ", ".join(hot[:5]) + " — fixed again and again in git history.") if hot else ""]))
