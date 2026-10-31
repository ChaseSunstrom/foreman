"""fm triggers (T-2276): which triggers earn their keep. Each capture event names its trigger (capture_once's trigger=,
else the event's source); a captured brief's final status says whether it was worth filing. A trigger whose recent
closed captures were mostly dropped files at low priority (demote, never silence). Stdlib only; reads the ledger and
the briefs, writes nothing."""
import datetime
import json
import os

import fmcore as c

MIN_CLOSED = 5        # closed captures before a precision counts
WINDOW = 20           # the last this-many closed captures decide
LOW_PRECISION = 0.3
LOOKBACK_DAYS = 180   # ponytail: capture_once reads this much ledger; widen if rare triggers need older history
URGENT = {"baseline", "ci", "ci-red", "security"}  # a red build is never "noise": never demoted


def _since(days):
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _captures(p, days, only=None):
    """[(trigger, task id)] oldest first. The user's own captures aren't triggers."""
    out = []
    for e in c.ledger_events(p, kinds=["capture"], since=_since(days)):
        d = e.get("data") or {}
        t = str(d.get("trigger") or d.get("source") or "")
        if t and t != "user" and e.get("task") and (only is None or t == only):
            out.append((t, e["task"]))
    return out


def _status(p):
    return {b.id: b.status for b in c.load_briefs(p, include_archive=True)}


def stats(p, days=LOOKBACK_DAYS, status=None):
    """{trigger: {fired, done, dropped, open, precision}}: precision is done/(done+dropped), None with none closed."""
    status = _status(p) if status is None else status
    rows = {}
    for t, tid in _captures(p, days):
        r = rows.setdefault(t, {"trigger": t, "fired": 0, "done": 0, "dropped": 0, "open": 0})
        r["fired"] += 1
        r[status.get(tid) if status.get(tid) in c.CLOSED else "open"] += 1
    for r in rows.values():
        closed = r["done"] + r["dropped"]
        r["precision"] = round(r["done"] / closed, 3) if closed else None
    return rows


def noisy(p, trigger, caps=None, status=None):
    """(precision, closed) over the trigger's last WINDOW closed captures when that's a demotion, else None. caps
    (all of _captures) and status (_status) may be passed in when a caller asks about many triggers."""
    if trigger in URGENT:
        return None
    caps = _captures(p, LOOKBACK_DAYS, only=trigger) if caps is None else [x for x in caps if x[0] == trigger]
    if len(caps) < MIN_CLOSED:  # too few firings to have enough closes: skip loading every brief
        return None
    status = _status(p) if status is None else status
    closed = [status[tid] for _, tid in caps if status.get(tid) in c.CLOSED][-WINDOW:]
    if len(closed) < MIN_CLOSED:
        return None
    prec = closed.count("done") / len(closed)
    return (prec, len(closed)) if prec < LOW_PRECISION else None


def noisiest(p):
    """The trigger with the most dropped captures and precision under LOW_PRECISION, or None: for fm state. Cached in
    triggers.json keyed on the ledger's size, so a polled fm state doesn't load every brief (T-2276: +90 ms CPU
    here). ponytail: any new ledger line invalidates it; key on the capture/close counts if that bites."""
    path = os.path.join(p.dir, "triggers.json")
    try:
        size = os.path.getsize(os.path.join(p.dir, "ledger.jsonl"))
    except OSError:
        size = -1
    try:
        with open(path) as f:
            hit = json.load(f)
        if hit.get("size") == size:
            return hit.get("noisiest")
    except (OSError, ValueError, AttributeError):
        pass
    status, caps = _status(p), _captures(p, LOOKBACK_DAYS)
    bad = [r for r in stats(p, LOOKBACK_DAYS, status).values() if noisy(p, r["trigger"], caps, status)]
    n = max(bad, key=lambda r: r["dropped"], default=None)
    try:
        c.write_atomic(path, json.dumps({"size": size, "noisiest": n}))
    except OSError:
        pass
    return n


def cmd_triggers(args):
    import fmcli
    p = fmcli.resolve(args)
    args.days = min(max(args.days, 1), 3650)
    status, caps = _status(p), _captures(p, LOOKBACK_DAYS)
    rows = sorted(stats(p, args.days, status).values(), key=lambda r: (-r["fired"], r["trigger"]))
    lines = [f"{'trigger':<22}{'fired':>6}{'done':>6}{'dropped':>8}{'open':>6}{'precision':>10}"]
    for r in rows:
        prec = "-" if r["precision"] is None else f"{r['precision']:.2f}"
        flag = "  (files at low priority)" if noisy(p, r["trigger"], caps, status) else ""
        lines.append(f"{r['trigger']:<22}{r['fired']:>6}{r['done']:>6}{r['dropped']:>8}{r['open']:>6}{prec:>10}{flag}")
    fmcli.out(args, {"days": args.days, "triggers": rows},
              "\n".join(lines) if rows else f"No trigger has filed a task in the last {args.days} days.")
