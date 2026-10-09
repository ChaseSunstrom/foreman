"""Foreman's own friction since the last self-improvement pass (T-0125): the digest one read-only subagent turns into
fixes for the self-inbox, and the trigger fm next uses. A pass is recursive: the next digest reports what became of
the self items, so a fix that didn't remove its friction shows up again. Reads the global events and every project's
ledger; writes only this project's meta (rsi_at, rsi_every), under its lock."""
import collections
import glob
import json
import os
import re
import statistics
import time

import fmcore as c

WINDOW_DAYS = 7  # the first pass looks back this far
MAX_LINES = 6  # per section
MIN_GAP_H = 2  # T-0154: a pass needs time to gather friction (pass 2 came due 13 min after pass 1 with one line)


def _start(meta):
    return meta.get("rsi_at") or c.iso(time.time() - WINDOW_DAYS * 86400)


def _ledgers(start, here=None):
    for p, _ in c.all_projects():
        if here and p.slug != here.slug and c.read_meta(p).get("sensitive"):
            continue  # T-0435: a sensitive project's ledger stays out of another project's digest
        for e in c.tail_jsonl(os.path.join(p.dir, "ledger.jsonl"), 6000):
            if (e.get("ts") or "") > start:
                yield p, e


def _transcript_commands(sids):
    """{(session id, command as the guard event shows it): (command, cwd)} from those sessions' transcripts."""
    base = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
    out = {}
    for sid in sids:
        for path in glob.glob(os.path.join(base, "*", f"{sid}.jsonl")) if re.fullmatch(r"[\w-]+", sid) else []:
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    for line in f:
                        if '"Bash"' not in line:
                            continue
                        try:
                            entry = json.loads(line)
                        except ValueError:
                            continue
                        content = (entry.get("message") or {}).get("content") if isinstance(entry, dict) else None
                        for b in content if isinstance(content, list) else []:
                            cmd = (b.get("input") or {}).get("command") if isinstance(b, dict) and \
                                b.get("type") == "tool_use" and b.get("name") == "Bash" else None
                            if isinstance(cmd, str):
                                shown = c.fit(c.redact(cmd.replace("\n", " ")), 160)  # as the hook logs it
                                out.setdefault((sid, shown), (cmd, entry.get("cwd") or ""))
            except OSError:
                continue
    return out


def _recheck(events):
    """{event index: what today's guard says of the command it blocked then} (T-0187): a fix that removed the friction
    shows as 'allows it'; a command no transcript holds any more gets no word."""
    import fmreplay
    bash = [(i, e) for i, e in enumerate(events) if e.get("tool") == "Bash" and e.get("cmd") and e.get("session_id")]
    found = _transcript_commands({e["session_id"] for _, e in bash})
    runs = {i: found[(e["session_id"], e["cmd"])] for i, e in bash if (e["session_id"], e["cmd"]) in found}
    now = fmreplay.verdicts(runs.values())
    return {i: "today's guard allows it" if now.get(fmreplay._key(*run)) == "allow" else "still blocks"
            for i, run in runs.items()}


def _rate(n, calls):
    return f"{n * 100 / calls:.1f}".rstrip("0").rstrip(".")


STAGES = {"task_plan": "plan", "focus": "focus", "step_done": "step", "evidence": "evidence", "check_run": "check",
          "audit": "audit", "finish": "finish", "task_done": "done", "task_block": "block"}
SMOOTH = 3  # stage events or fewer for a finished task: too smooth to have been checked much


def _failed(e):
    d = e.get("data") or {}
    if e.get("event") == "evidence":
        return bool(c.result_exit(d.get("result")))  # "✗ exit 1 · …": a failed run (T-0750)
    return e.get("event") == "check_run" and any((r or {}).get("exit") for r in d.get("results") or [])


def _mine(ledger, label):
    """T-0658: process mining over the window's ledgers — the paths tasks really take (stage sequences, repeats
    collapsed), finished tasks that went smoothly but closed with a weak grade, and how many failed runs came before
    each block (where work gives up)."""
    runs = collections.defaultdict(list)
    for lp, e in ledger:
        if e.get("task") and e.get("event") in STAGES:
            runs[(lp.slug, e["task"])].append((lp, e))
    paths, smooth, gave_up = collections.Counter(), [], collections.defaultdict(list)
    for (_, tid), pairs in runs.items():
        lp, evs = pairs[0][0], [e for _, e in pairs]
        seq = [STAGES[e["event"]] for e in evs]
        seq = [s for i, s in enumerate(seq) if not i or s != seq[i - 1]]
        if seq[-1] in ("done", "block"):
            paths[" → ".join(seq)] += 1
        end = evs[-1]
        if end["event"] == "task_done" and len(evs) <= SMOOTH \
                and (end.get("data") or {}).get("verified") not in ("strong", "ok"):
            smooth.append(f"{label(lp)}{tid} ({len(evs)} stage events, graded "
                          f"{(end.get('data') or {}).get('verified') or 'ungraded'})")
        if end["event"] == "task_block":
            gave_up[sum(_failed(e) for e in evs)].append(f"{label(lp)}{tid}")
    return {
        "common paths (stage sequences of tasks that finished or blocked)": [
            f"{s} ×{n}" for s, n in paths.most_common(3)],
        "smooth but unverified (few stage events, weak grade: check these held)": smooth[:MAX_LINES],
        "give-up points (failed runs before each block)": [
            f"after {n} failed run(s): {', '.join(t[:5])}" for n, t in sorted(gave_up.items())][:MAX_LINES]}


def digest(p, recheck=True):
    """{section: [lines]} of what went wrong or slow since the last pass, newest kinds first, each line bounded, and the
    window's counts (kept at --mark for the next digest's trend)."""
    meta = c.read_meta(p)
    start = _start(meta)
    events = [e for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 30000) if (e.get("ts") or "") > start]
    ledger = list(_ledgers(start, p))
    label = lambda lp: "" if lp.slug == p.slug else f"[{lp.slug}] "  # T-0435: which project a line came from
    out = {}

    guard = [e for e in events if e.get("kind") == "guard_block"]
    key = lambda e: (e.get("category"), c.fit(c.plain(str(e.get("target") or "")), 110))
    blocks = collections.Counter(key(e) for e in guard)
    example = {key(e): c.fit(c.plain(str(e["cmd"])), 160) for e in guard if e.get("cmd")}  # T-0172: the newest
    shown = blocks.most_common(MAX_LINES)
    newest = {key(e): e for e in guard}
    now = _recheck([newest[k] for k, _ in shown]) if recheck else {}
    out["guard blocks (each a stop Claude had to work around; a false one costs a rewrite)"] = [
        f"{n}× {cat}: {target}" + (f" — e.g. `{example[(cat, target)]}`" if (cat, target) in example else "")
        + (f" — {now[i]}" if i in now else "") for i, ((cat, target), n) in enumerate(shown)]
    rules = collections.Counter(e["rule"] for e in guard if e.get("rule"))  # T-0672: which checks fire most
    if rules:
        out["guard rules by fire count (a rule that fires often on harmless work is the one to look at)"] = [
            f"{n}× {r}" for r, n in rules.most_common(MAX_LINES)]

    failed = [e for e in events if e.get("kind") == "tool_fail"]  # T-0301: grouped by why, not by which file
    why = lambda e: (e.get("tool"), c.fit(c.plain(str(e.get("error") or "no error recorded")), 90))
    fails = collections.Counter(why(e) for e in failed)
    target = {why(e): c.fit(c.plain(str(e.get("target") or "")), 90) for e in failed}  # the newest example
    out["failed tool calls"] = [f"{n}× {k[0]}: {k[1]}" + (f" — e.g. {target[k]}" if target[k] else "")
                                for k, n in fails.most_common(MAX_LINES)]

    kinds = collections.Counter(e.get("event") for _, e in ledger)
    waits = collections.Counter(e.get("kind") for e in events if e.get("kind") == "drive_reload")  # T-0301: a wait on
    # background work is the drive working as meant (the notification resumes it), not a stop
    out["nudges and drive stops"] = [x for x in (
        f"{kinds['stop_gate']}× the Stop hook held a turn for missing evidence" if kinds["stop_gate"] else "",
        f"{waits['drive_reload']}× the drive ended a turn for a mod reload" if waits["drive_reload"] else "",
        f"{kinds['task_block']}× a task was blocked" if kinds["task_block"] else "") if x]

    runs = collections.defaultdict(list)
    for _, e in ledger:
        if e.get("event") == "check_run":
            for r in (e.get("data") or {}).get("results") or []:
                if isinstance(r, dict) and isinstance(r.get("s"), (int, float)) and r["s"] > 0:  # T-0424: a reused pass is 0.0 s
                    runs[r.get("cmd")].append(r["s"])
    out["slow gates (latest vs usual)"] = [
        f"{cmd}: {xs[-1]:.0f}s vs usual {statistics.median(xs):.0f}s" for cmd, xs in runs.items()
        if len(xs) >= 3 and xs[-1] > 1.5 * statistics.median(xs) and xs[-1] > 5][:MAX_LINES]

    ms = sorted(e["ms"] for e in events if e.get("kind") == "hook_ms" and isinstance(e.get("ms"), (int, float)))
    if ms:
        out["hook latency"] = [f"p95 {ms[int(len(ms) * 0.95) - 1 if len(ms) > 1 else 0]:.0f} ms over {len(ms)} hook runs"]

    try:  # T-0437: hooks never fail a call, so the errors they swallow are friction only hooks.log saw
        import fmdoctor
        errs = [e for e in fmdoctor.recent_hook_errors() if " paused for " not in e[0]]  # the breaker's note
    except Exception:
        errs = []
    if errs:
        top = collections.Counter((e[0].split(" ") + ["?"])[1] for e in errs).most_common(1)[0]
        out["errors the hooks swallowed"] = [f"{len(errs)} in the last 24 h, most in {top[0]} ({top[1]}); latest: "
                                             f"{c.fit(c.plain(errs[-1][-1].strip()), 160)} (state/logs/hooks.log)"]

    steer = lambda e: e.get("event") == "note" and str((e.get("data") or {}).get("text") or "").startswith("steer:")
    said = [label(lp) + c.fit(c.plain(str((e.get("data") or {}).get("text") or "")), 200) for lp, e in ledger
            if e.get("event") == "correction" or steer(e)]
    out["what the user corrected or steered (their words)"] = said[-MAX_LINES:]

    out["escapes: defects found after a task closed (the lenses that passed it)"] = [  # T-0285: review recall over time
        f"{label(lp)}{e.get('task')} ({', '.join((e.get('data') or {}).get('lenses') or []) or 'no lens'}) → "
        f"{(e.get('data') or {}).get('by')} {c.fit(c.plain(str((e.get('data') or {}).get('title') or '')), 140)}"
        for lp, e in ledger if e.get("event") == "escape"][-MAX_LINES:]

    out["surprises: where the model of the code was wrong (fm surprise)"] = [
        f"{label(lp)}{e.get('task') or '-'}: {c.fit(c.plain(str((e.get('data') or {}).get('text') or '')), 200)}"
        for lp, e in ledger if e.get("event") == "surprise"][-MAX_LINES:]

    others = collections.defaultdict(collections.Counter)  # T-0435: how much friction each other project had
    for lp, e in ledger:
        kind = "steer" if steer(e) else e.get("event")
        if lp.slug != p.slug and kind in ("guard_block", "correction", "steer", "task_block", "escape", "surprise",
                                          "stop_gate", "task_done"):
            others[lp.slug][kind.replace("_", " ")] += 1
    out["other projects (since the last pass)"] = [
        f"{slug}: " + ", ".join(f"{n} {k}" for k, n in cnt.most_common()) for slug, cnt in sorted(others.items())][:MAX_LINES]

    out["lessons recorded"] = [f"{e.get('task')}: {c.fit(c.plain(str(e['data']['lesson'])), 160)}" for _, e in ledger
                               if e.get("event") == "task_done" and (e.get("data") or {}).get("lesson")][-MAX_LINES:]

    briefs = c.load_briefs(p)
    out["requests from other projects (fm sweep, fm -p SLUG capture --source cross-project), open here"] = [
        f"{b.id} {c.fit(b.title, 140)}" for b in briefs
        if b.meta.get("source") == "cross-project" and b.status not in c.CLOSED][:MAX_LINES]  # T-0443

    mine = [b for b in briefs if b.meta.get("source") == "self"]
    open_ = [b for b in mine if b.status not in c.CLOSED]
    closed = [b for b in mine if b.status == "done" and (b.meta.get("updated") or "") > start]  # dropped ones fixed nothing
    out["self-inbox: what became of earlier passes"] = (
        [f"done since: {b.id} {c.fit(b.title, 90)}" for b in closed][:MAX_LINES] +
        [f"open: {b.id} {c.fit(b.title, 90)}" for b in open_][:MAX_LINES])
    budget = collections.defaultdict(lambda: [0, 0])  # T-0499: what the hooks put into the model's context
    for e in events:
        if e.get("kind") == "inject":
            b = budget[(e.get("event"), e.get("key"))]
            b[0], b[1] = b[0] + 1, b[1] + int(e.get("chars") or 0)
    out["injected notes (event: kind — times, characters)"] = [
        f"{ev}: {k} — {n}×, {ch:,} chars" for (ev, k), (n, ch) in sorted(budget.items(), key=lambda x: -x[1][1])
    ][:MAX_LINES]
    out["notes repeated 3+ times (a candidate for a hard check instead of prose: T-0470)"] = [
        f"{k} ({n}× from {ev})" for (ev, k), (n, _) in budget.items()
        if n >= 3 and ev not in ("SessionStart", "UserPromptSubmit")][:MAX_LINES]  # those two speak every turn
    out.update(_mine(ledger, label))  # T-0658
    try:  # T-0620: where this project's work hasn't held, for the pass to look at first
        import fmoutcomes
        out["weak areas (fm outcomes --atlas)"] = [x[2:] for x in fmoutcomes.atlas_lines(p) if x.startswith("- ")][:MAX_LINES]
    except Exception:  # a report line; never the digest
        pass
    lessons = collections.Counter(e.get("task") for e in events if e.get("kind") == "lesson_shown")  # T-0454
    out["lessons shown (one shown often while the same blocks recur may need rewording)"] = [
        f"{t}: {n}×" for t, n in lessons.most_common(MAX_LINES)]
    dead = [d for d in meta.get("deadends") or [] if isinstance(d, dict) and d.get("text")]  # T-0471
    skipped = 0
    for k in list(out) if dead else []:
        keep = [x for x in out[k] if not any(d["text"].lower() in str(x).lower() for d in dead)]
        skipped, out[k] = skipped + len(out[k]) - len(keep), keep
    if skipped:
        out["dead ends (fm friction --reject)"] = [f"{skipped} line(s) skipped: " + "; ".join(
            f"\"{d['text']}\" ({d.get('why') or 'no reason given'})" for d in dead[:5])]
    kinds_ev = collections.Counter(e.get("kind") for e in events)
    counts = {"tool calls": kinds_ev["tool"], "guard blocks": kinds_ev["guard_block"],
              "failed tool calls": kinds_ev["tool_fail"],
              "drive stops": kinds_ev["drive_reload"] + kinds["stop_gate"], "steers": len(said)}
    last = meta.get("rsi_counts") or {}
    if last.get("tool calls") and counts["tool calls"]:  # T-0187: did the last pass's fixes make it better
        out["trend: the last pass's window → this one, per 100 tool calls"] = [" · ".join(
            f"{k} {_rate(last.get(k) or 0, last['tool calls'])} → {_rate(counts[k], counts['tool calls'])}"
            for k in counts if k != "tool calls" and (last.get(k) or counts[k]))]
    return {"since": start, "sections": {k: v for k, v in out.items() if v}, "counts": counts}


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
A guard block marked "today's guard allows it" was fixed since: leave it. The trend line compares the last pass's
window with this one. Also say whether an earlier pass's item (the self-inbox section) failed to remove its friction,
and whether this loop itself should change (how often it runs, what it reads). For the guard, propose shell forms to add to FORMS in
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
    if getattr(args, "reject", None):  # T-0471: a dead end later passes skip (and cite) instead of proposing again
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["deadends"] = (meta.get("deadends") or []) + [{"text": c.redact(args.reject), "why": c.redact(
                args.why or ""), "at": c.now()}]
            c.write_meta(p, meta)
        return print(f"Dead end recorded: lines with \"{args.reject}\" are skipped from now on.")
    if args.mark:
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["rsi_counts"] = digest(p, recheck=False)["counts"]
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
