"""Standing orders (T-0452): requests that capture themselves on a schedule or when a file changes — "every week,
check the dependencies", "when api.json changes, review it". fm night runs them; fm orders run does too."""
import hashlib
import json
import os
import re
import time

import fmcore as c

_PERIOD = re.compile(r"(\d+)([mhdw])")
_SECONDS = {"m": 60, "h": 3600, "d": 86400, "w": 7 * 86400}


def _path(p):
    return os.path.join(p.dir, "orders.json")


def load(p):
    try:
        with open(_path(p), encoding="utf-8") as f:
            orders = json.load(f)
        return orders if isinstance(orders, list) else []
    except (OSError, ValueError):
        return []


def _save(p, orders):
    c.write_atomic(_path(p), json.dumps(orders, indent=1) + "\n")


def _sig(p, rel):
    try:
        with open(os.path.join(p.root, rel), "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    except OSError:
        return "missing"


def run(p, now=None):
    """Capture each due order once: --every after its period, --on-change when its file's content changed since the
    last look (the first look only notes it). An open task of the same title isn't captured twice. [fired orders]"""
    import fmcli
    now, fired = now or time.time(), []
    with c.lock(p.dir):
        orders = load(p)
        titles = {b.title for b in c.load_briefs(p) if b.status not in c.CLOSED}
        for o in orders:
            due = False
            if o.get("every"):
                m = _PERIOD.fullmatch(o["every"])
                due = bool(m) and now - float(o.get("last_ts") or 0) >= int(m.group(1)) * _SECONDS[m.group(2)]
            elif o.get("on_change"):
                sig = _sig(p, o["on_change"])
                due, o["sig"] = o.get("sig") is not None and sig != o["sig"], sig
            if not due:
                continue
            o["last_ts"], o["last"] = now, c.now()
            title = fmcli._title(o["text"])
            if title not in titles:
                b = fmcli._create(p, title, o.get("type") or "FEATURE", c.guess_tier(o.get("type") or "FEATURE", o["text"]),
                                  "captured", raw=o["text"], source="order")
                c.log_event(p, "capture", task=b.id, data={"source": "order", "order": o["n"]})
                titles.add(title)
            fired.append(o)
        _save(p, orders)
        if fired:
            c.regen_views(p)
    return fired


def cmd_orders(args):
    import fmcli
    p = fmcli.resolve(args)
    orders = load(p)
    if args.action == "add":
        if bool(args.every) == bool(args.on_change):
            raise fmcli.UsageError("fm orders add needs one of --every PERIOD (30m, 6h, 1d, 1w) or --on-change PATH")
        if args.every and not _PERIOD.fullmatch(args.every):
            raise fmcli.UsageError("--every takes a number and m, h, d or w: 30m, 6h, 1d, 1w")
        text = " ".join(args.text).strip()
        if not text:
            raise fmcli.UsageError("fm orders add … \"<what to capture>\"")
        n = max((o.get("n", 0) for o in orders), default=0) + 1
        order = {"n": n, "text": c.redact(text), "every": args.every, "on_change": args.on_change,
                 "type": (args.type or "FEATURE").upper()}
        with c.lock(p.dir):
            _save(p, load(p) + [order])
        return fmcli.out(args, order, f"Order {n} added: {order['text']} "
                         + (f"(every {args.every})" if args.every else f"(when {args.on_change} changes)"))
    if args.action == "rm":
        n = int(args.text[0]) if args.text and args.text[0].isdigit() else None
        if n is None or not any(o.get("n") == n for o in orders):
            raise fmcli.UsageError("fm orders rm N (fm orders list shows the numbers)")
        with c.lock(p.dir):
            _save(p, [o for o in load(p) if o.get("n") != n])
        return fmcli.out(args, {"removed": n}, f"Order {n} removed.")
    if args.action == "run":
        fired = run(p)
        return fmcli.out(args, {"fired": fired}, f"{len(fired)} order(s) fired" + "".join(
            f"\n  {o['n']}. {o['text']}" for o in fired))
    rows = [f"  {o['n']}. {o['text']} — " + (f"every {o['every']}" if o.get("every") else f"when {o['on_change']} changes")
            + (f" (last {o['last']})" if o.get("last") else "") for o in orders]
    return fmcli.out(args, {"orders": orders}, "\n".join(["Standing orders:"] + rows) if rows else
                     "No standing orders (fm orders add --every 1w \"…\" or --on-change PATH \"…\").")
