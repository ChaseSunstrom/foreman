"""Foreman's own friction since the last self-improvement pass (T-0125): the digest one read-only subagent turns into
fixes for the self-inbox, and the trigger fm next uses. A pass is recursive: the next digest reports what became of
the self items, so a fix that didn't remove its friction shows up again. Reads the global events and every project's
ledger; writes only this project's meta (rsi_at, rsi_every), under its lock."""
import collections
import os
import statistics
import time

import fmcore as c

WINDOW_DAYS = 7  # the first pass looks back this far
MAX_LINES = 6  # per section
MIN_GAP_H = 2  # T-0154: a pass needs time to gather friction (pass 2 came due 13 min after pass 1 with one line)


def _start(meta):
    return meta.get("rsi_at") or c.iso(time.time() - WINDOW_DAYS * 86400)


def _ledgers(start):
    for p, _ in c.all_projects():
        for e in c.tail_jsonl(os.path.join(p.dir, "ledger.jsonl"), 6000):
            if (e.get("ts") or "") > start:
                yield p, e


def digest(p):
    """{section: [lines]} of what went wrong or slow since the last pass, newest kinds first, each line bounded."""
    meta = c.read_meta(p)
    start = _start(meta)
    events = [e for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 30000) if (e.get("ts") or "") > start]
    ledger = list(_ledgers(start))
    out = {}

    guard = [e for e in events if e.get("kind") == "guard_block"]
    key = lambda e: (e.get("category"), c.fit(c.plain(str(e.get("target") or "")), 110))
    blocks = collections.Counter(key(e) for e in guard)
    example = {key(e): c.fit(c.plain(str(e["cmd"])), 160) for e in guard if e.get("cmd")}  # T-0172: the newest
    out["guard blocks (each a stop Claude had to work around; a false one costs a rewrite)"] = [
        f"{n}× {cat}: {target}" + (f" — e.g. `{example[(cat, target)]}`" if (cat, target) in example else "")
        for (cat, target), n in blocks.most_common(MAX_LINES)]

    fails = collections.Counter((e.get("tool"), c.fit(str(e.get("target") or ""), 90))
                                for e in events if e.get("kind") == "tool_fail")
    out["failed tool calls"] = [f"{n}× {tool}: {target}" for (tool, target), n in fails.most_common(MAX_LINES)]

    kinds = collections.Counter(e.get("event") for _, e in ledger)
    waits = collections.Counter(e.get("kind") for e in events if e.get("kind") in ("drive_wait", "drive_reload"))
    out["nudges and drive stops"] = [x for x in (
        f"{kinds['stop_gate']}× the Stop hook held a turn for missing evidence" if kinds["stop_gate"] else "",
        f"{waits['drive_wait']}× the drive ended a turn to wait on background work" if waits["drive_wait"] else "",
        f"{waits['drive_reload']}× the drive ended a turn for a mod reload" if waits["drive_reload"] else "",
        f"{kinds['task_block']}× a task was blocked" if kinds["task_block"] else "") if x]

    runs = collections.defaultdict(list)
    for _, e in ledger:
        if e.get("event") == "check_run":
            for r in (e.get("data") or {}).get("results") or []:
                if isinstance(r, dict) and isinstance(r.get("s"), (int, float)):
                    runs[r.get("cmd")].append(r["s"])
    out["slow gates (latest vs usual)"] = [
        f"{cmd}: {xs[-1]:.0f}s vs usual {statistics.median(xs):.0f}s" for cmd, xs in runs.items()
        if len(xs) >= 3 and xs[-1] > 1.5 * statistics.median(xs) and xs[-1] > 5][:MAX_LINES]

    ms = sorted(e["ms"] for e in events if e.get("kind") == "hook_ms" and isinstance(e.get("ms"), (int, float)))
    if ms:
        out["hook latency"] = [f"p95 {ms[int(len(ms) * 0.95) - 1 if len(ms) > 1 else 0]:.0f} ms over {len(ms)} hook runs"]

    said = [c.fit(c.plain(str((e.get("data") or {}).get("text") or "")), 200) for _, e in ledger
            if e.get("event") == "correction" or (e.get("event") == "note" and
                                                  str((e.get("data") or {}).get("text") or "").startswith("steer:"))]
    out["what the user corrected or steered (their words)"] = said[-MAX_LINES:]

    out["lessons recorded"] = [f"{e.get('task')}: {c.fit(c.plain(str(e['data']['lesson'])), 160)}" for _, e in ledger
                               if e.get("event") == "task_done" and (e.get("data") or {}).get("lesson")][-MAX_LINES:]

    mine = [b for b in c.load_briefs(p) if b.meta.get("source") == "self"]
    open_ = [b for b in mine if b.status not in c.CLOSED]
    closed = [b for b in mine if b.status == "done" and (b.meta.get("updated") or "") > start]  # dropped ones fixed nothing
    out["self-inbox: what became of earlier passes"] = (
        [f"done since: {b.id} {c.fit(b.title, 90)}" for b in closed][:MAX_LINES] +
        [f"open: {b.id} {c.fit(b.title, 90)}" for b in open_][:MAX_LINES])
    return {"since": start, "sections": {k: v for k, v in out.items() if v}}


def render(d):
    lines = [f"Foreman friction since {d['since']}:"]
    for title, items in d["sections"].items():
        lines.append(f"\n{title}:")
        lines += [f"  - {x}" for x in items]
    if len(lines) == 1:
        lines.append("  (nothing recorded)")
    return "\n".join(lines)


BRIEF = """# Foreman self-improvement pass

You review Foreman (a Claude Code plugin: `~/.claude/foreman`, CLI `fm`, library `plugin/lib/fm*.py`, hooks
`plugin/hooks/`, UI mod `mods/foreman-ui/`) from its own friction, read-only. The digest below is what went wrong or
slow since the last pass, from Foreman's ledgers and events.

{digest}

Return at most 5 improvements, most valuable first. For each:
- the friction it removes, citing the digest line(s) it comes from;
- the cause, grounded in the code (file:line you read), not guessed;
- the change, as small as works, and its type (FIX/PERFORMANCE/CLEAN/FEATURE/SECURITY) and size (S/M/L);
- done when: one observable check.
Also say whether an earlier pass's item (the self-inbox section) failed to remove its friction, and whether this
loop itself should change (how often it runs, what it reads). For the guard, propose shell forms to add to FORMS in
plugin/tests/test_guard_diff.py (it runs them in real bash and fails on any the guard misses). Skip anything you
can't ground; say so instead.
"""


def due(p):
    """True at a task boundary once rsi_every tasks of this project closed since the last pass, and at least MIN_GAP_H
    hours after it (0 or unset: off)."""
    meta = c.read_meta(p)
    every = int(meta.get("rsi_every") or 0)
    if every <= 0 or (meta.get("rsi_at") and (c.age_days(meta["rsi_at"]) or 0) * 24 < MIN_GAP_H):
        return False
    start = meta.get("rsi_at") or meta.get("created") or ""
    done = sum(1 for e in c.tail_jsonl(os.path.join(p.dir, "ledger.jsonl"), 6000)
               if e.get("event") == "task_done" and (e.get("ts") or "") >= start)  # second-resolution stamps
    return done >= every


ACTION = ("self-improvement pass due: fm friction --brief, then one foreman:fm-recon subagent on that brief; capture "
          "its grounded findings with fm capture --source self, then fm friction --mark")


def cmd_friction(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.every is not None:
        if args.every < 0:
            raise fmcli.UsageError("--every takes 0 (off) or a number of closed tasks")
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["rsi_every"] = args.every
            c.write_meta(p, meta)
        return print(f"Self-improvement pass: every {args.every} closed tasks." if args.every else
                     "Self-improvement pass: off.")
    if args.mark:
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["rsi_at"] = c.now()
            c.write_meta(p, meta)
        c.log_event(p, "rsi_pass")
        return print("Pass recorded; the next digest starts here and reports what became of its items.")
    d = digest(p)
    if args.json:
        return fmcli.out(args, d, "")
    text = render(d)
    if args.brief:
        path = os.path.join(p.dir, "audits", f"rsi-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        c.write_atomic(path, BRIEF.format(digest=text))
        return print(f"Self-improvement brief ({len(text)} chars of digest): {path}")
    print(text)
