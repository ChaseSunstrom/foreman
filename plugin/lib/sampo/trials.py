"""T-1059: a self-change (fm rule add, fm evolve) is a pre-registered trial: the metric it should move and by when.
The digest grades a due trial on ledger event rates in equal windows before and after; one that didn't move the
metric is proposed for revert (never reverted unattended). T-2351: a task a trigger filed is a trial on that trigger's own
key (register_fix at fm task done), graded held, didn't hold (one FIX) or unmeasured on the key's sightings."""
import datetime
import hashlib
import json
import math
import os

from sampo import core as c


def _path(p):
    return os.path.join(p.dir, "trials.json")


def load(p):
    try:
        with open(_path(p), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def add(p, what, moves, by):
    """Record the trial; the metric is a ledger event kind in the plural (corrections -> correction)."""
    if int(by) < 1:
        from sampo import cli
        raise cli.UsageError("--by must be at least 1 day")
    rec = {"what": c.fit(what, 80), "moves": moves, "by": int(by), "at": c.now()}
    with c.lock(p.dir, timeout=2):
        c.write_atomic(_path(p), json.dumps(load(p) + [rec]))
    return rec


# T-2351: triggers no failure signal fired for: a person or this session wrote them (user, discovered, self), Foreman's
# own trial verdict (trial: else a FIX would trial itself), or a listing that repeats each poll whether or not anything
# recurred (github issues still open, specs, sibling projects' sweeps)
NO_TRIAL = {"user", "discovered", "self", "trial", "cross-project", "github", "spec"}
FIX_DUE = 14  # days after the fix lands that its key must stay gone
LIVE = 30  # days before the fix's first focus whose sightings show the key was live


def key_hash(key):
    """A trigger key's stable id: its sightings and its trial share it; the key's text (a URL, a signature) isn't kept."""
    return hashlib.sha1(key.encode("utf-8", "surrogateescape")).hexdigest()[:16]


def register_fix(p, b):
    """T-2351: the trial of a task a trigger filed (its brief carries trigger and trigger_key), once per task, due
    FIX_DUE days from now (its close: the work is on the main tree); None for a user-filed or already registered one."""
    k, trig = b.meta.get("trigger_key"), b.meta.get("trigger")
    if not k or not trig or trig in NO_TRIAL:
        return None
    focus = next((e.get("ts") for e in c.ledger_events(p, ("focus",), since=str(b.meta.get("created") or ""))
                  if e.get("task") == b.id), None)
    rec = {"what": f"Self-fix {b.id} ({c.fit(str(trig), 30)})", "kind": "self-fix", "task": b.id, "trigger": trig,
           "key": k, "at": c.now(), "by": FIX_DUE, "focus": focus or b.meta.get("created") or c.now()}
    with c.lock(p.dir, timeout=2):
        rows = load(p)
        if any(t.get("task") == b.id for t in rows if isinstance(t, dict)):
            return None
        c.write_atomic(_path(p), json.dumps(rows + [rec]))
    return rec


def _seen(p, key, since, until):
    return sum((e.get("data") or {}).get("key") == key and str(e.get("ts") or "") < until
               for e in c.ledger_events(p, ("trigger_seen",), since=since))


def _grade_fix(p, t, now, act=False):
    """held (the key was live before and gone since), didn't hold (seen again: one FIX, filed once), or unmeasured
    (seen only when it was filed: its absence proves nothing, so never held)."""
    fmt = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")  # noqa: E731
    at, focus = _t(t["at"]), _t(t["focus"])
    due = at + datetime.timedelta(days=int(t["by"]))
    if now < due:
        return "pending", f"pending, {math.ceil((due - now).total_seconds() / 86400)} days left"
    before = _seen(p, t["key"], fmt(focus - datetime.timedelta(days=LIVE)), fmt(focus))
    after = _seen(p, t["key"], fmt(at), fmt(due))
    if after and act:  # the digest files it; fm trial and fm triggers only read
        from sampo import eco
        tid = t["task"]
        eco.capture_once(p, f"Self-fix {tid} didn't hold: its trigger {t['trigger']} fired again\n"
                              f"(the key was seen {before} times in the {LIVE} days before the fix and {after} times in "
                              f"the {t['by']} days after it landed; to revert locally: git log --grep {tid} names its "
                              f"commit, git revert it; or fix the cause again)", "FIX", "trial",
                           key=f"Self-fix {tid} didn't hold")
    if after:
        return "didn't hold", f"didn't hold: its key was seen {before} times before the fix, {after} since"
    if before <= 1:
        return "unmeasured", "unmeasured: its key was seen only when it was filed, so its absence proves nothing"
    return "held", f"held: its key was seen {before} times before the fix, none in the {t['by']} days since"


def held_fixes(p):
    """{trigger: held self-fixes}, from the verdicts the digest stored (no regrading here), counted only once fm outcomes
    also shows the task survived (no revert, re-fix or user correction within its window): a signal Sampo didn't author."""
    held = [t for t in load(p) if isinstance(t, dict) and t.get("kind") == "self-fix" and t.get("verdict") == "held"]
    if not held:
        return {}
    from sampo import outcomes
    outs, n = outcomes.outcomes(p), {}
    for t in held:
        o = outs.get(t.get("task")) or {}
        if o.get("survival") == "survived" and o.get("fate") == "held":
            n[t["trigger"]] = n.get(t["trigger"], 0) + 1
    return n


def _t(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def grade(p, t, now=None, act=False):
    """(verdict, detail): pending, moved, or no movement. Lower is better; moved means at most half the before rate."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if t.get("kind") == "self-fix":
        return _grade_fix(p, t, now, act)
    at, n = _t(t["at"]), t["by"]
    due = at + datetime.timedelta(days=n)
    if now < due:
        return "pending", f"pending, {math.ceil((due - now).total_seconds() / 86400)} days left"
    fmt = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
    if t["moves"] == "brier":  # T-2337: a calibration bar moved; the metric is the Brier of bets stated before vs after
        from sampo import outcomes
        rows = outcomes.bar_rows(outcomes.scored(p))  # the survival-scored rows, the only ones that moved the bar
        b = outcomes.brier([r for r in rows if str(r["ts"]) < fmt(at)])
        a = outcomes.brier([r for r in rows if fmt(at) <= str(r["ts"]) < fmt(due)])
        if a is None and now < due + datetime.timedelta(days=outcomes.SURVIVE_DAYS):  # T-2610: reads wait for windows
            return "pending", (f"pending: the bets placed since the move score as their {outcomes.SURVIVE_DAYS}-day "
                               "windows end")
        if b is not None and a is not None and a < b:
            return "moved", f"moved (Brier {b:.2f} -> {a:.2f})"
        return "revert", "no movement: propose revert (Brier " + (f"{b:.2f} -> {a:.2f})" if None not in (a, b)
                                                                   else "no scored bets after the move)")
    kind = t["moves"][:-1] if t["moves"].endswith("s") else t["moves"]
    ts = [str(e.get("ts") or "") for e in c.ledger_events(p, (kind,), since=fmt(at - datetime.timedelta(days=n)))]
    before = sum(x < fmt(at) for x in ts) / n
    after = sum(fmt(at) <= x < fmt(due) for x in ts) / n
    rates = f"{t['moves']}/day {before:.1f} -> {after:.1f}"
    if before and after <= before / 2:
        return "moved", f"moved ({rates})"
    return "revert", f"no movement: propose revert ({rates})"


def cmd_trial(args):
    from sampo import cli
    p = cli.resolve(args)
    cli.out(args, load(p), "\n".join(lines(p)) or "No trials: fm rule add X --moves corrections --by 30")


def lines(p, act=False):
    """The digest's trial rows: the last 8, plus every self-fix not yet settled. act (the digest): file a didn't-hold FIX
    and store a self-fix's final verdict, so it is graded once and fm triggers reads it without regrading."""
    trials = load(p)
    shown = [t for i, t in enumerate(trials) if i >= len(trials) - 8 or (isinstance(t, dict) and t.get("kind") ==
                                                                          "self-fix" and not t.get("verdict"))]
    rows, settled = [], {}
    for t in shown:
        try:
            if t.get("verdict"):
                rows.append(f"- {t['what']}: {t.get('detail') or t['verdict']}")
                continue
            v, detail = grade(p, t, act=act)
            rows.append(f"- {t['what']}: {detail}")
            if act and t.get("kind") == "self-fix" and v in ("held", "didn't hold", "unmeasured"):
                settled[t["task"]] = (v, detail)
        except Exception:  # a malformed record, a lock or a ledger error must never crash the digest
            pass
    if settled:
        try:
            with c.lock(p.dir, timeout=2):
                cur = load(p)
                for t in cur:
                    if isinstance(t, dict) and t.get("task") in settled:
                        t["verdict"], t["detail"] = settled[t["task"]]
                c.write_atomic(_path(p), json.dumps(cur))
        except Exception:
            pass  # graded again next digest
    return ["Trials (self-changes):"] + rows if rows else []
