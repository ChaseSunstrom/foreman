"""Foreman hook handlers. Entry point: run(event, raw_stdin) -> exit code (JSON, if any, goes to stdout).

Non-guard handlers fail open: any exception is logged to state/logs/hooks.log and the hook exits 0.
The PreToolUse guard fails closed: any exception blocks the tool call (exit 2).
Injected text is factual state, never instructions.
"""
import json
import os
import re
import sys
import time
import traceback

import fmcore as c

CTX_BUDGET = 2000       # SessionStart additionalContext
PROMPT_BUDGET = 400     # UserPromptSubmit additionalContext
NOTE_BUDGET = 200       # PreToolUse scope note
DRIVE_MAX = 50          # consecutive drive continuations without a user prompt
APPROVAL_TTL = 24 * 3600  # seconds a pending `fm ask` stays answerable
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
GUARDED = FILE_TOOLS | {"Bash"}
# async events (latency irrelevant) and per-batch MessageDisplay are not timed
UNTIMED = {"MessageDisplay", "PostToolUse", "PostToolUseFailure", "SubagentStart", "SubagentStop"}


class HookBlock(Exception):
    """Raised by a handler to block with exit code 2 and the message on stderr."""


# ---------------------------------------------------------------- plumbing

def run(event, raw):
    t0 = time.monotonic()
    if event == "PreToolUse":
        code = _pre_tool_use(raw)
    else:
        code = 0
        try:
            payload = json.loads(raw) if raw.strip() else {}
            handler = HANDLERS.get(event)
            out = handler(payload) if handler else None
            if out is not None:
                print(json.dumps(out, ensure_ascii=False))
        except HookBlock as e:
            print(str(e), file=sys.stderr)
            code = 2
        except Exception:
            log_error(event, traceback.format_exc())
    if event not in UNTIMED:
        _event({"kind": "hook_ms", "event": event, "ms": round((time.monotonic() - t0) * 1000, 1)})
    return code


def log_error(event, text):
    try:
        path = os.path.join(c.state_dir(), "logs", "hooks.log")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{c.now()} {event} {c.redact(text).rstrip()}\n")
    except OSError:
        pass


def _event(rec):
    try:
        rec = dict({"ts": c.now()}, **rec)
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(c.redact_obj(rec), ensure_ascii=False) + "\n")
    except OSError:
        pass


def _cwd(pl):
    return pl.get("cwd") or os.getcwd()


def _clean(s, limit=120):
    return re.sub(r"[\x00-\x1f\x7f;]", " ", str(s))[:limit]


def _title_seq(sd):
    label = c.state_line(sd) if sd else "idle"
    return f"\x1b]0;foreman · {_clean(label, 80)}\x07"


def _progress_seq(sd):
    a = sd.get("active") if sd else None
    if a and a["steps_total"]:
        return f"\x1b]9;4;1;{int(100 * a['steps_done'] / a['steps_total'])}\x07"
    return "\x1b]9;4;0;0\x07"


def _notify_seq(body):
    return f"\x1b]777;notify;Foreman;{_clean(body, 200)}\x07"


def _gate_path(p):
    return os.path.join(p.dir, "gate.json")


def _read_gate(p):
    try:
        with open(_gate_path(p)) as f:
            g = json.load(f)
    except (OSError, ValueError):
        g = {}
    g.setdefault("evidence", [])
    g.setdefault("drive", {})
    return g


def _write_gate(p, g):
    g["evidence"] = g["evidence"][-200:]
    c.write_atomic(_gate_path(p), json.dumps(g, indent=1) + "\n")


# ---------------------------------------------------------------- SessionStart

def session_start(pl):
    sid = pl.get("session_id")
    p = c.find_project(_cwd(pl), create=True)
    if not p:
        return None
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    if env_file and sid:
        with open(env_file, "a") as f:
            f.write(f"export FOREMAN_SESSION_ID={sid}\nexport FOREMAN_PROJECT={p.slug}\n")
    with c.lock(p.dir, timeout=1):
        meta = c.read_meta(p)
        other, other_note = meta.get("session") or {}, None
        age = c.age_days(other.get("seen"))
        if other.get("id") and other["id"] != sid and age is not None and age < 15 / 1440:
            other_note = f"Another Claude Code session ({other['id'][:8]}) was active in this project {int(age * 1440)}m ago."
        meta.update(session={"id": sid, "seen": c.now()}, last_active=c.now(), sensitive=c.detect_sensitive(p.root))
        c.write_meta(p, meta)
        sd = c.regen_views(p)
    c.log_event(p, "session_start", data={"source": pl.get("source")}, session=sid)
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": session_context(p, sd, other_note)},
            "terminalSequence": _title_seq(sd)}


def session_context(p, sd, other_note=None):
    a = sd["active"]
    head = [f"Foreman project {p.slug} ({p.root}). Drive: {'on' if sd['drive'] else 'off'}"
            + (", paused" if sd["paused"] else "") + "."
            + (" Autonomy: full." if sd.get("autonomy") == "full" else "")]
    focus, resume = [], []
    if a:
        step = f"step {a['step']['n']}/{a['step']['of']}: {a['step']['text']}" if a["step"] else \
            f"{a['steps_done']}/{a['steps_total']} steps done"
        focus.append(f"Active: {a['id']} [{a['type']} {a['tier']}] {a['title']} — {step}.")
        r = c.resume_info(p).get("resume", "")
        r = " / ".join(l.strip("- ").strip() for l in r.replace("<!-- auto -->", "").splitlines() if l.strip())
        if r:
            resume.append(f"Resume here: {r[:400]}")
        focus.append(f"Brief: {a['path']}")
    else:
        focus.append("Active: none.")
    q = sd["queue"]
    queue = [("Queue: " + "; ".join(f"{x['id']} {x['type']} {x['tier']} {x['title'][:50]}" for x in q[:5])
              + (f" (+{len(q) - 5} more)" if len(q) > 5 else "") + ".") if q else "Queue: empty."]
    inbox = sd["inbox"]
    tail = [f"Inbox: {len(inbox)}" + (" — " + "; ".join(f"{x['id']} {x['title'][:40]}" for x in inbox[:3]) if inbox else "") + "."]
    if sd["blocked"]:
        tail.append(f"Blocked: {len(sd['blocked'])} ({', '.join(x['id'] for x in sd['blocked'][:5])}).")
    if sd["tidy_overdue_days"]:
        tail.append(f"Tidy overdue: last tidy {sd['last_tidy'] or 'never'} ({sd['tidy_overdue_days']} days).")
    if sd["cycles"]:
        tail.append("Dependency cycles: " + "; ".join("↔".join(x) for x in sd["cycles"])[:150] + ".")
    if sd["sensitive"]:
        tail.append("Sensitive repo: new sessions here start in manual permission mode.")
    if other_note:
        tail.append(other_note)
    text = ""
    for parts in ([head, focus, resume, queue, tail], [head, focus, queue, tail], [head, focus, tail]):
        text = "\n".join(line for part in parts for line in part)
        if len(text) <= CTX_BUDGET:
            return text
    return text[:CTX_BUDGET]


# ---------------------------------------------------------------- UserPromptSubmit

_PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)


_YES = re.compile(r"^\W*(yes|y|yep|yeah|yup|sure|ok|okay|approved?|confirm(ed)?|lgtm|go|do it)\b(?!\s*\?)", re.I)


def _resolve_approvals(p, meta, sid, text):
    """The only path from a pending `fm ask` to an authorization: the user's own next prompt in that session.

    A reply starting with yes grants every pending request of the session; anything else cancels them."""
    pend = meta.get("pending_approvals") or []
    valid = [a for a in pend if isinstance(a, dict) and a.get("task") and isinstance(a.get("allow"), list)
             and a.get("session")]  # a request no session owns is never answerable
    mine = [a for a in valid if sid and a["session"] == sid]
    if len(valid) != len(pend):
        meta["pending_approvals"] = valid
    if not mine:
        return []
    meta["pending_approvals"] = [a for a in valid if a not in mine]
    yes, notes = bool(_YES.match(text)), []
    for a in mine:
        cats, at = ", ".join(a["allow"]), c.parse_ts(a.get("at"))
        fresh = bool(at) and time.time() - at.timestamp() < APPROVAL_TTL
        b = c.find_brief(p, a["task"]) if yes and fresh else None
        if b:
            b.meta["allow"] = list(dict.fromkeys(list(b.meta.get("allow") or []) + a["allow"]))
            b.append_log(f"user approved {cats} in chat")
            c.save_brief(p, b)
            c.log_event(p, "approval_granted", task=b.id, data={"allow": a["allow"], "reply": c.redact(text[:80])},
                        session=sid)
            notes.append(f"User approved {cats} for {b.id}")
        else:
            c.log_event(p, "approval_declined", task=a["task"], data={"allow": a["allow"], "expired": not fresh},
                        session=sid)
            notes.append(f"Pending {cats} for {a['task']} not granted ({'expired' if not fresh else 'reply was not a yes'})")
    return notes


def user_prompt_submit(pl):
    sid = pl.get("session_id")
    p = c.find_project(_cwd(pl), create=True)
    if not p:
        return None
    text = _PASTED.sub("", pl.get("prompt") or "").strip()
    r = c.parse_intake(text)
    try:
        with c.lock(p.dir, timeout=3):
            meta = c.read_meta(p)
            approvals = _resolve_approvals(p, meta, sid, text)
            meta["session"] = {"id": sid, "seen": c.now()}
            if "PAUSE" in r.overrides:
                meta["paused"] = True
            elif "RESUME" in r.overrides:
                meta["paused"] = False
            elif "FULL AUTO" in r.overrides:
                meta["autonomy"] = "full"
            elif "STANDARD" in r.overrides:
                meta["autonomy"] = "standard"
            c.write_meta(p, meta)
            g = _read_gate(p)
            if sid in g["drive"]:
                g["drive"][sid]["count"] = 0
                _write_gate(p, g)
            sd = c.regen_views(p) if r.overrides or approvals else c.state_dict(p)
    except c.LockTimeout:  # never drop a yes / PAUSE silently
        return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext":
                "Foreman: state was busy (another session or fm held the lock), so this message was not recorded: "
                "no approval, override word or heartbeat was applied. Pending approvals are unchanged."}}
    parts = list(approvals)
    if r.items:
        tags = ", ".join(i.type + ("!" if i.urgent else "") + ("?" if i.explore else "") for i in r.items)
        n = len(r.items)
        parts.append(f"Message has {n} intake item{'s' if n > 1 else ''} ({tags})"
                     + (" plus block lines" if r.context or r.constraints or r.done_when or r.skip else ""))
    if r.overrides:
        parts.append("Override word: " + ", ".join(r.overrides))
    elif not r.items and c.is_open_ended(text):
        parts.append("Open-ended request with no concrete target; the Foreman procedure for it is /foreman:brainstorm")
    a = sd["active"]
    if a:
        parts.append(f"Active: {a['id']} {a['type']} " + (f"step {a['step']['n']}/{a['step']['of']}" if a["step"]
                                                        else f"{a['steps_done']}/{a['steps_total']} steps done"))
    else:
        parts.append("No active task" + (f"; {len(sd['queue'])} queued" if sd["queue"] else ""))
    if sd["inbox"]:
        parts.append(f"Inbox: {len(sd['inbox'])}")
    if sd["paused"]:
        parts.append("Drive paused")
    if sd.get("autonomy") == "full":
        parts.append("Autonomy: full")
    note = ("Foreman: " + ". ".join(parts) + ".")[:PROMPT_BUDGET]
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": note},
            "terminalSequence": _title_seq(sd)}


# ---------------------------------------------------------------- PreToolUse (guard: fail closed)

def _pre_tool_use(raw):
    try:
        import fmguard
        pl = json.loads(raw)
        tool = pl.get("tool_name", "")
        if tool not in GUARDED:
            return 0
        ctx, p, act = _guard_ctx(pl, fmguard)
        block = fmguard.check(tool, pl.get("tool_input"), ctx)
    except Exception as e:
        log_error("PreToolUse", traceback.format_exc())
        print(f"Foreman guard internal error ({type(e).__name__}); the tool call was blocked (fail-closed). "
              f"Details: {os.path.join(c.state_dir(), 'logs', 'hooks.log')}. "
              f"If this persists: claude plugin disable foreman@foreman", file=sys.stderr)
        return 2
    if block:
        reason = fmguard.message(block, ctx)
        _event({"kind": "guard_block", "session_id": pl.get("session_id"), "category": block.category,
                "tool": tool, "target": str(block.detail)[:120], "project": p.slug if p else None})
        try:
            if p:
                c.log_event(p, "guard_block", task=act.id if act else None,
                            data={"category": block.category, "detail": str(block.detail)[:200]},
                            session=pl.get("session_id"))
        except Exception:
            log_error("PreToolUse", traceback.format_exc())
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))
        print(reason, file=sys.stderr)
        return 2
    try:
        note = _scope_note(pl, p, act)
        if note:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": note}}))
    except Exception:
        log_error("PreToolUse", traceback.format_exc())
    return 0


def _guard_ctx(pl, fmguard):
    cwd, home = _cwd(pl), os.path.expanduser("~")
    p = act = None
    try:
        p = c.find_project(cwd)
        act = c.active_brief(c.load_briefs(p)) if p else None
    except Exception:
        log_error("PreToolUse", traceback.format_exc())  # unreadable state: no authorizations, guard still runs
    scratch = [s for s in (pl.get("scratchpad_dir"), "/tmp", "/var/tmp", os.environ.get("TMPDIR")) if s]
    ctx = fmguard.Ctx(cwd=cwd, project_root=fmguard.project_root_for(cwd, home), home=home,
                      foreman_home=c.foreman_home(), state_dir=c.state_dir(), scratch=scratch,
                      allow=set(act.meta.get("allow") or []) if act else set(), task_id=act.id if act else None)
    return ctx, p, act


def _scope_note(pl, p, act):
    if not (p and act and pl.get("tool_name") in FILE_TOOLS):
        return None
    scope = act.meta.get("scope") or []
    ti = pl.get("tool_input") or {}
    path = os.path.normpath(os.path.join(_cwd(pl), ti.get("file_path") or ti.get("notebook_path") or ""))
    rel = os.path.relpath(path, p.root) if path.startswith(p.root.rstrip("/") + "/") else path
    if not scope or any(c.glob_match(rel, s) for s in scope):
        return None
    for e in c.ledger_tail(p, 300):
        if e.get("event") == "scope_note" and e.get("task") == act.id and (e.get("data") or {}).get("file") == path:
            return None
    c.log_event(p, "scope_note", task=act.id, data={"file": path}, session=pl.get("session_id"))
    return f"Foreman: {rel} is outside {act.id} scope [{', '.join(scope)}]."[:NOTE_BUDGET]


# ---------------------------------------------------------------- PostToolUse / Failure (async)

def _target(ti):
    if not isinstance(ti, dict):
        return ""
    for k in ("file_path", "notebook_path", "command", "pattern", "url", "query", "description", "skill", "prompt"):
        if ti.get(k):
            return str(ti[k]).replace("\n", " ")
    return ""


def post_tool_use(pl, ok=True):
    tool, ti = pl.get("tool_name", ""), pl.get("tool_input") or {}
    p = c.find_project(_cwd(pl))
    rec = {"session_id": pl.get("session_id"), "kind": "tool" if ok else "tool_fail", "tool": tool,
           "target": _target(ti)[:120], "ms": pl.get("duration_ms"), "ok": ok, "project": p.slug if p else None}
    if pl.get("agent_type"):
        rec["agent_type"] = pl["agent_type"]
    if not ok:
        rec["error"] = str(pl.get("error") or "").split("\n")[0][:120]
    _event(rec)
    if ok and p and tool in FILE_TOOLS:
        act = c.active_brief(c.load_briefs(p))
        path = os.path.normpath(os.path.join(_cwd(pl), ti.get("file_path") or ti.get("notebook_path") or ""))
        c.log_event(p, "touched", task=act.id if act else None, data={"file": path, "tool": tool},
                    session=pl.get("session_id"))
    return None


def post_tool_use_failure(pl):
    return post_tool_use(pl, ok=False)


# ---------------------------------------------------------------- PreCompact

def pre_compact(pl):
    p = c.find_project(_cwd(pl))
    if p:
        with c.lock(p.dir, timeout=5):
            c.checkpoint(p, auto=True, session=pl.get("session_id"))
    return None


# ---------------------------------------------------------------- Stop: evidence gate + drive

_CLAIM = re.compile(r"\b(done|completed?|finished|fixed|implemented|all set|ready for review|works now|resolved|shipped)\b", re.I)
_NEG = re.compile(r"\b(not|isn't|isnt|aren't|haven't|hasn't|won't|wasn't|yet to|still)\b[\w\s,']{0,20}$", re.I)
_ASK = re.compile(r"(\?\s*$)|\b(should i|shall i|do you want|would you like|want me to"
                  r"|please (confirm|approve|choose|decide|advise|review)|let me know|awaiting your"
                  r"|need your (input|approval|decision|answer)|which (option|approach) do you)\b", re.I)


def claims_done(msg):
    for m in _CLAIM.finditer(msg or ""):
        if not _NEG.search(msg[max(0, m.start() - 30):m.start()]):
            return True
    return False


def needs_user(msg):
    return bool(_ASK.search((msg or "").strip()[-400:]))


def _marks(p):
    def size(path):
        try:
            return os.path.getsize(path)
        except OSError:
            return 0
    return {"ledger": size(os.path.join(p.dir, "ledger.jsonl")), "events": size(os.path.join(c.state_dir(), "events.jsonl"))}


def _progressed(p, marks, sid):
    if _marks(p)["ledger"] != marks.get("ledger"):
        return True
    try:
        with open(os.path.join(c.state_dir(), "events.jsonl"), encoding="utf-8") as f:
            f.seek(marks.get("events", 0))
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("session_id") == sid and e.get("kind") in ("tool", "tool_fail"):
                    return True
    except OSError:
        pass
    return False


def stop(pl):
    sid, msg = pl.get("session_id"), pl.get("last_assistant_message") or ""
    p = c.find_project(_cwd(pl))
    if not p:
        return None
    briefs = c.load_briefs(p)
    sd = c.state_dict(p, briefs)
    act = c.active_brief(briefs)
    seq = _title_seq(sd) + _progress_seq(sd)
    with c.lock(p.dir, timeout=1):
        g = _read_gate(p)
        reason = _evidence_gate(p, act, pl, g) or _drive(p, sd, briefs, pl, g)
        d = g["drive"].setdefault(sid, {"count": 0})
        had_work, d["had_work"] = d.get("had_work"), bool(sd["active"] or sd["queue"])
        _write_gate(p, g)
    if not reason and ((act and needs_user(msg)) or (had_work and not d["had_work"])):
        seq += _notify_seq("waiting for your answer" if act else "queue empty")
    out = {"terminalSequence": seq}
    if reason:
        out.update(decision="block", reason=reason)
    return out


def _evidence_gate(p, act, pl, g):
    if not act or pl.get("stop_hook_active") or not claims_done(pl.get("last_assistant_message")):
        return None
    steps, cur = act.steps(), act.current_step()
    if cur:
        missing, label, flag = not act.has_evidence(step=cur.n), f"step {cur.n}/{len(steps)}", f"--step {cur.n} "
    else:
        missing, label, flag = not act.has_evidence(), "task", ""
    key = f"{pl.get('session_id')}:{act.id}:{cur.n if cur else 'task'}"
    if not missing or key in g["evidence"]:
        return None
    g["evidence"].append(key)
    c.log_event(p, "stop_gate", task=act.id, data={"step": cur.n if cur else None}, session=pl.get("session_id"))
    return (f"Foreman: {act.id} {label} has no recorded verification evidence. Record it: "
            f"fm task evidence {act.id} {flag}\"<cmd>\" \"<result>\", or state why it can't be verified.")


def _drive(p, sd, briefs, pl, g):
    sid = pl.get("session_id")
    full = sd.get("autonomy") == "full"
    if not sd["drive"] or sd["paused"] or (needs_user(pl.get("last_assistant_message")) and not full):
        return None
    waiting = [t for t in sd.get("pending") or [] if t]
    if waiting and not full:
        return None  # an `fm ask` is open: the user's reply decides it
    work = next((w for w in ([sd["active"]] if sd["active"] else []) + sd["queue"] if w["id"] not in waiting), None)
    if not work:
        return None  # nothing left that doesn't need the user
    wb = next(b for b in briefs if b.id == work["id"])
    if (wb.meta.get("explore") or wb.tier == "L") and not wb.meta.get("approved") and not full:
        return None  # waiting on the user's approval (AUTONOMY standard)
    d = g["drive"].setdefault(sid, {"count": 0})
    if pl.get("stop_hook_active") and d.get("marks") and not _progressed(p, d["marks"], sid):
        return None  # no progress since the last continuation: let the turn end
    if d.get("count", 0) >= DRIVE_MAX:
        return None
    more = [x["id"] for x in sd["queue"] if x["id"] != work["id"]]
    what = (f"step {work['step']['n']}/{work['step']['of']} ({work['step']['text'][:80]}) is open" if work.get("step")
            else "is open" if sd["active"] and work["id"] == sd["active"]["id"] else "is next in the queue (not focused)")
    reason = (f"Foreman drive: {work['id']} {work['type']} {what}"
              + (f"; {len(more)} more queued ({', '.join(more[:4])})" if more else "")
              + (". Autonomy full: the user is not asked mid-run; decide with your default and record it (fm decide), "
                 "self-approve L/? plans after the self-critique, keep what needs the user (fm ask) for the final report"
                 + (f"; waiting on the user: {', '.join(waiting)}" if waiting else "") + "."
                 if full else
                 ". No question to the user or approval is pending. Drive ends when the queue is empty, "
                 "when a question or approval is needed, or with `fm drive off`."))
    _event({"kind": "drive", "session_id": sid, "task": work["id"]})
    d.update(count=d.get("count", 0) + 1, marks=_marks(p))
    return reason


# ---------------------------------------------------------------- TaskCompleted, subagents

def task_completed(pl):
    m = re.search(r"\b(T-\d{4,})\s+step\s+(\d+)", pl.get("task_subject") or "")
    if not m:
        return None
    p = c.find_project(_cwd(pl))
    b = c.find_brief(p, m.group(1)) if p else None
    n = int(m.group(2))
    if b and not b.has_evidence(step=n):
        raise HookBlock(f"Foreman: {b.id} step {n} has no recorded evidence; record it with "
                        f"fm task evidence {b.id} --step {n} \"<cmd>\" \"<result>\" before completing this task.")
    return None


def subagent_start(pl):
    _event({"kind": "subagent_start", "session_id": pl.get("session_id"), "agent_id": pl.get("agent_id"),
            "agent_type": pl.get("agent_type")})
    return None


def subagent_stop(pl):
    _event({"kind": "subagent_stop", "session_id": pl.get("session_id"), "agent_id": pl.get("agent_id"),
            "agent_type": pl.get("agent_type")})
    p = c.find_project(_cwd(pl))
    if p and pl.get("agent_type"):
        act = c.active_brief(c.load_briefs(p))
        c.log_event(p, "subagent", task=act.id if act else None,
                    data={"agent_type": pl.get("agent_type"), "agent_id": pl.get("agent_id"),
                          "transcript": pl.get("agent_transcript_path"),
                          "summary_chars": len(pl.get("last_assistant_message") or "")},
                    session=pl.get("session_id"))
    return None


# ---------------------------------------------------------------- display, notifications, end

def message_display(pl):
    delta = pl.get("delta") or ""
    shown, badge = c.redact(delta), ""
    if pl.get("index") == 0:
        p = c.find_project(_cwd(pl))
        if p:
            try:
                with open(os.path.join(p.dir, "badge.txt")) as f:
                    label = f.read().strip()
            except OSError:
                label = ""
            if label:
                badge = f"[{label} · {time.strftime('%H:%M')}] "
    if badge or shown != delta:
        return {"hookSpecificOutput": {"hookEventName": "MessageDisplay", "displayContent": badge + shown}}
    return None


def notification(pl):
    p = c.find_project(_cwd(pl))
    sd = c.state_dict(p) if p else None
    return {"terminalSequence": _notify_seq(pl.get("message") or "Claude Code needs your attention") + _title_seq(sd)}


def session_end(pl):
    p = c.find_project(_cwd(pl))
    if p:
        c.update_meta(p, last_active=c.now())
        c.regen_registry()
    return None


HANDLERS = {
    "SessionStart": session_start, "UserPromptSubmit": user_prompt_submit, "PostToolUse": post_tool_use,
    "PostToolUseFailure": post_tool_use_failure, "PreCompact": pre_compact, "Stop": stop,
    "TaskCompleted": task_completed, "SubagentStart": subagent_start, "SubagentStop": subagent_stop,
    "MessageDisplay": message_display, "Notification": notification, "SessionEnd": session_end,
}
