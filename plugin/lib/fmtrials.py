"""T-1059: a self-change (fm rule add, fm evolve) is a pre-registered trial: the metric it should move and by when.
The digest grades a due trial on ledger event rates in equal windows before and after; one that didn't move the
metric is proposed for revert (never reverted unattended)."""
import datetime
import json
import math
import os

import fmcore as c


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
        import fmcli
        raise fmcli.UsageError("--by must be at least 1 day")
    rec = {"what": c.fit(what, 80), "moves": moves, "by": int(by), "at": c.now()}
    with c.lock(p.dir, timeout=2):
        c.write_atomic(_path(p), json.dumps(load(p) + [rec]))
    return rec


def _t(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def grade(p, t, now=None):
    """(verdict, detail): pending, moved, or no movement. Lower is better; moved means at most half the before rate."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    at, n = _t(t["at"]), t["by"]
    due = at + datetime.timedelta(days=n)
    if now < due:
        return "pending", f"pending, {math.ceil((due - now).total_seconds() / 86400)} days left"
    fmt = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
    if t["moves"] == "brier":  # T-2337: a calibration bar moved; the metric is the Brier of bets stated before vs after
        import fmoutcomes
        rows = [r for r in fmoutcomes.scored(p) if r["outcome"]]
        b = fmoutcomes.brier([r for r in rows if str(r["ts"]) < fmt(at)])
        a = fmoutcomes.brier([r for r in rows if fmt(at) <= str(r["ts"]) < fmt(due)])
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
    import fmcli
    p = fmcli.resolve(args)
    fmcli.out(args, load(p), "\n".join(lines(p)) or "No trials: fm rule add X --moves corrections --by 30")


def lines(p):
    rows = []
    for t in load(p)[-8:]:
        try:
            rows.append(f"- {t['what']}: {grade(p, t)[1]}")
        except (KeyError, TypeError, ValueError, AttributeError, ZeroDivisionError):
            pass  # a malformed record must never crash the digest
    return ["Trials (self-changes):"] + rows if rows else []
