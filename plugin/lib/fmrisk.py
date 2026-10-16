"""T-1080: one daily risk budget for autonomy. Destructive guard blocks, failed closes and reverts spend weighted points
on the ledger's (UTC) day; past the cap, autonomy steps down a notch (full → standard, standard → slow) and optional
work waits, until the day rolls. Only the user moves the cap (the guard's USER_ONLY_FM): a brake the braked can lift
isn't one."""
import math
import os
import time

import fmcore as c

WEIGHTS = {"destructive block": 1, "failed close": 2, "revert": 3}
DESTRUCTIVE = {"rm-outside", "git-destructive", "system", "credentials", "self-authorize", "pipe-shell", "confine"}
CAP = 6
_MEMO = {}  # (slug, day, ledger size and mtime) -> status: one read per process while nothing new is logged


def _day():
    return time.strftime("%Y-%m-%d", time.gmtime())


def cap(p, meta=None):
    v = (c.read_meta(p) if meta is None else meta).get("risk_cap")
    return float(v) if isinstance(v, (int, float)) and math.isfinite(v) and v >= 0 else CAP


def status(p, meta=None):
    """{"spent", "cap", "slowed", "counts"} for today."""
    day = _day()
    try:
        st = os.stat(os.path.join(p.dir, "ledger.jsonl"))
        key = (p.slug, day, st.st_size, st.st_mtime_ns)
    except OSError:
        key = (p.slug, day, 0, 0)
    counts = _MEMO.get(key)
    if counts is None:
        counts = dict.fromkeys(WEIGHTS, 0)
        for e in c.ledger_events(p, kinds=["guard_block", "close_affected"], since=day):
            d = e.get("data") or {}
            if e.get("event") == "guard_block" and d.get("category") in DESTRUCTIVE:
                counts["destructive block"] += 1
            elif e.get("event") == "close_affected" and d.get("exit"):
                counts["failed close"] += 1
        # ponytail: one git log per process per ledger change; a hand revert shows once the ledger moves again
        subjects = c._git(p.root, "log", f"--since={day} 00:00:00 +0000", "--format=%s", fail="") if c.git_root(p.root) else ""
        counts["revert"] = sum(1 for s in subjects.splitlines() if s.startswith("Revert "))
        _MEMO[key] = counts
    spent = sum(WEIGHTS[k] * n for k, n in counts.items())
    limit = cap(p, meta)
    return {"spent": spent, "cap": limit, "slowed": spent >= limit, "counts": counts}


def slowed(p, meta=None):
    """Why today's risk budget slows autonomy, or None."""
    try:
        s = status(p, meta)
    except Exception:  # an unreadable ledger never changes autonomy
        return None
    if not s["slowed"]:
        return None
    what = ", ".join(f"{n} {k}{'s' if n != 1 else ''}" for k, n in s["counts"].items() if n)
    return f"today's risk budget is spent ({s['spent']:g} of {s['cap']:g}: {what}); autonomy steps down a notch until tomorrow"


def cmd_risk(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "set":
        if args.day is None or not (math.isfinite(args.day) and args.day >= 0):
            raise fmcli.UsageError("fm risk set --day N --because \"<why>\" (N ≥ 0 points a day)")
        if not args.because:
            raise fmcli.UsageError("fm risk set needs --because \"<why>\" (it is logged)")
        old = cap(p)
        c.update_meta(p, risk_cap=args.day)
        c.log_event(p, "risk_cap", data={"from": old, "to": args.day, "because": c.fit(c.plain(args.because), 200)})
        return fmcli.out(args, {"cap": args.day}, f"risk cap {old:g} → {args.day:g} points a day")
    s = status(p)
    lines = [f"Risk today: {s['spent']:g} of {s['cap']:g} points" + (" — slowed" if s["slowed"] else "")]
    lines += [f"  {n} {k} × {WEIGHTS[k]}" for k, n in s["counts"].items() if n]
    if s["slowed"]:
        lines.append("  " + slowed(p))
    return fmcli.out(args, s, "\n".join(lines))
