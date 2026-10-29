"""T-1080: one daily risk budget for autonomy. Destructive guard blocks, failed closes and reverts spend weighted points
on the ledger's (UTC) day; past the cap, autonomy steps down a notch (full → standard, standard → slow) and optional
work waits, until the day rolls. Only the user moves the cap (the guard's USER_ONLY_FM): a brake the braked can lift
isn't one."""
import json
import math
import os
import re
import time

import fmcore as c

WEIGHTS = {"destructive block": 1, "failed close": 2, "revert": 3}
DESTRUCTIVE = {"rm-outside", "git-destructive", "system", "credentials", "self-authorize", "pipe-shell", "confine"}
CAP = 6
_MEMO = {}  # (slug, day, ledger size and mtime) -> status: one read per process while nothing new is logged
CACHE = "risk.json"  # T-2028: today's counts, the ledger offset they cover and the revert count, for the next process
_MARKS = c.lazy(rb'"guard_block"|"close_affected"')


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
        counts = _MEMO[key] = _counts(p, day)
    spent = sum(WEIGHTS[k] * n for k, n in counts.items())
    limit = cap(p, meta)
    return {"spent": spent, "cap": limit, "slowed": spent >= limit, "counts": counts}


def _counts(p, day):
    """Today's counts. T-2028: every hook process read the day's ledger and ran git log; the cache file lets one read
    only the lines past its offset (checked by the start of the last line read, which holds its unique chain hash, so
    fm tidy's in-place roll fails it and the day is read afresh) and run git log only when HEAD's reflog moved."""
    cpath = os.path.join(p.dir, CACHE)
    try:
        with open(cpath, encoding="utf-8") as f:
            old = json.load(f)
    except (OSError, ValueError):
        old = None
    old = old if isinstance(old, dict) and old.get("day") == day else {}
    n, saved = {"destructive block": 0, "failed close": 0}, old.get("n")
    off, line, mark, ok = 0, 0, "", False
    try:
        with open(os.path.join(p.dir, "ledger.jsonl"), "rb") as f:
            at, at_line, m = old.get("off"), old.get("line"), old.get("mark")
            if isinstance(saved, dict) and all(isinstance(saved.get(k), int) for k in n) and isinstance(m, str) and m \
                    and isinstance(at, int) and isinstance(at_line, int) and 0 <= at_line < at:
                f.seek(at_line)
                ok = f.read(len(m.encode("latin-1"))) == m.encode("latin-1")
            if ok:
                n, off, line, mark = {k: saved[k] for k in n}, at, at_line, m
                f.seek(at)
            else:
                c._seek_since(f, day.encode())
                off = f.tell()
            for raw in f:
                if not raw.endswith(b"\n"):
                    break  # still being written: the next read takes it
                if _MARKS.search(raw):
                    try:
                        e = json.loads(raw)
                    except (ValueError, RecursionError):
                        e = None
                    d = e.get("data") if isinstance(e, dict) else None
                    d = d if isinstance(d, dict) else {}
                    if isinstance(e, dict) and str(e.get("ts") or "") >= day:
                        if e.get("event") == "guard_block" and d.get("category") in DESTRUCTIVE:
                            n["destructive block"] += 1
                        elif e.get("event") == "close_affected" and d.get("exit"):
                            n["failed close"] += 1
                line, mark, off = off, raw[:64].decode("latin-1"), off + len(raw)
    except OSError:
        pass
    root, gkey = c.git_root(p.root), None
    try:  # a worktree's .git is a file: no key, so git log each time
        s = os.stat(os.path.join(root, ".git", "logs", "HEAD")) if root else None
        gkey = [s.st_size, s.st_mtime_ns] if s else None
    except OSError:
        pass
    if gkey and old.get("git") == gkey and isinstance(old.get("rev"), int):
        rev = old["rev"]
    else:
        subjects = c._git(p.root, "log", f"--since={day} 00:00:00 +0000", "--format=%s", fail="") if root else ""
        rev = sum(1 for s in subjects.splitlines() if s.startswith("Revert "))
    if not ok or n != saved or gkey != old.get("git") or rev != old.get("rev") or off - old.get("off", 0) > 65536:
        try:  # most calls write nothing: the next process rereads the few lines since
            c.write_atomic(cpath, json.dumps({"day": day, "off": off, "line": line, "mark": mark, "n": n,
                                              "git": gkey, "rev": rev}))
        except OSError:
            pass
    return {**n, "revert": rev}


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


def collisions(p, days=7):
    """T-1875: the last days' guard blocks by rule, most first: [{rule, category, n, spends, detail, rewrite}], spends
    when its category counts against the budget, detail the newest, rewrite the guard's hint for it ("" when none)."""
    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - days * 86400))
    n, last = {}, {}
    for e in c.ledger_events(p, kinds=["guard_block"], since=since):
        d = e.get("data") or {}
        r = str(d.get("rule") or d.get("category") or "?")
        n[r], last[r] = n.get(r, 0) + 1, d
    if not n:
        return []
    import fmguard  # about 12 ms, at SessionStart only, and only when the week had a block
    rows = []
    for r in sorted(n, key=lambda r: -n[r]):
        cat, detail = str(last[r].get("category") or ""), str(last[r].get("detail") or "")
        rows.append({"rule": c.plain(r), "category": cat, "n": n[r], "spends": cat in DESTRUCTIVE,
                     "detail": c.defang(c.fit(c.redact(c.plain(detail)), 120)),
                     "rewrite": fmguard._hint(detail, cat).strip() or (  # T-1897: the live brief block's own route
                         "Start one: fm task new \"<title>\" --type FIX --tier S --ac \"<done when>\" --step \"<step>\" "
                         "--focus, or fm focus ID as its own command." if cat == "brief" else "")})
    return rows


def collision_line(p, least=3):
    """T-1875: one SessionStart line for the week's most-hit guard rule when it fired least times or more, else None."""
    top = next(iter(collisions(p)), None)
    if not top or top["n"] < least:
        return None
    say = re.split(r"(?<=[.!?])\s", top["rewrite"], maxsplit=1)[0] or f"Last: {top['detail']}."  # review: keep it short
    return c.fit(f"Guard collisions: {top['rule']} blocked {top['n']}× in 7 days. {say} fm risk lists them.", 240)


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
    s["collisions"] = collisions(p)  # T-1875: a habit costs rewrites even where it spends no risk
    if s["collisions"]:
        lines.append("Guard collisions, 7 days (the rewrite that passes):")
        lines += [f"  {h['n']}× {h['rule']}" + (" (spends risk)" if h["spends"] else "")
                  + f" — {c.fit(h['rewrite'], 160) or 'last: ' + h['detail']}"
                  for h in sorted(s["collisions"], key=lambda h: not h["spends"])[:8]]  # T-1972: what spent it first
    return fmcli.out(args, s, "\n".join(lines))
