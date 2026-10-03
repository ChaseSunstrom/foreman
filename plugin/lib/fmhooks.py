"""Foreman hook handlers. Entry point: run(event, raw_stdin) -> exit code (JSON, if any, goes to stdout).

Non-guard handlers fail open: any exception is logged to state/logs/hooks.log and the hook exits 0.
The PreToolUse guard fails closed: any exception blocks the tool call (exit 2).
Injected text is factual state, never instructions.
"""
import hashlib
import json
import os
import re
import sys
import time

import fmcore as c

CTX_BUDGET = 2000       # SessionStart additionalContext
PROMPT_BUDGET = 400     # UserPromptSubmit additionalContext
NOTE_BUDGET = 200       # PreToolUse scope note
DRIVE_MAX = 50          # consecutive drive continuations without a user prompt
CONTEXT_NOTE_PCT = 60     # context use at a task boundary worth mentioning (context rot)
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
GUARDED = FILE_TOOLS | {"Bash"}
# async events (latency irrelevant) and per-batch MessageDisplay are not timed
UNTIMED = {"MessageDisplay", "PostToolUse", "PostToolUseFailure", "SubagentStart", "SubagentStop"}


def _tb():
    """The current exception's traceback; imported only when something failed (traceback costs ~15 ms per hook)."""
    import traceback
    return traceback.format_exc()


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
            log_error(event, _tb())
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
    if sid and re.fullmatch(r"[\w-]{1,100}", sid):  # a new or compacted context: the next prompt restates the state,
        folder = os.path.join(c.state_dir(), "sessions")  # and one-shot notes (outline, thrash, tripwires) re-arm
        try:
            names = [n for n in os.listdir(folder) if n.startswith(sid + ".")]
        except OSError:
            names = []
        for name in names:
            try:
                os.remove(os.path.join(folder, name))
            except OSError:  # another SessionStart got it first
                pass
    p = c.find_project(_cwd(pl), create=True)
    if not p:
        return None
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    if env_file and sid:
        with open(env_file, "a") as f:
            f.write(f"export FOREMAN_SESSION_ID={sid}\nexport FOREMAN_PROJECT={p.slug}\n")
    with c.lock(p.dir, timeout=LOCK_QUICK):
        meta = c.read_meta(p)
        other, other_note = meta.get("session") or {}, None
        age = c.age_days(other.get("seen"))
        if other.get("id") and other["id"] != sid and age is not None and age < 15 / 1440:
            other_note = f"Another Claude Code session ({other['id'][:8]}) was active in this project {int(age * 1440)}m ago."
        offered = c.age_days(meta.get("digest_offered"))
        if offered is None or offered >= 7:  # once a week: what got done (R1 weekly digest)
            meta["digest_offered"] = c.now()  # checked once a week even when there was nothing to show
            try:
                import fmcost
                week = fmcost.weekly_line(p)
            except Exception:
                log_error("SessionStart", _tb())
                week = None
            if week:
                other_note = " ".join(x for x in (other_note, week) if x)
        meta.update(session={"id": sid, "seen": c.now()}, last_active=c.now(), sensitive=c.detect_sensitive(p.root))
        c.write_meta(p, meta)
        synced = _sync_import(p)
        sd = c.regen_views(p)
    if synced:
        other_note = " ".join(x for x in (other_note, synced) if x)
    c.log_event(p, "session_start", data={"source": pl.get("source")}, session=sid)
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": session_context(p, sd, other_note)},
            "terminalSequence": _title_seq(sd)}


def _sync_import(p):
    """A repo with a .foreman/ mirror (fm sync) brings its work along: take in what's new at session start, and on a
    fresh clone (no local briefs, sync never switched off here) turn syncing on. Caller holds the lock; returns a note
    for the session context, or None."""
    import fmsync
    meta = c.read_meta(p)
    if not os.path.isdir(fmsync.mirror(p)) or not (meta.get("sync") or ("sync" not in meta and not
                                                                          c.load_briefs(p, include_archive=True))):
        return None
    try:
        res = fmsync.import_(p)
    except (OSError, ValueError):
        log_error("SessionStart", _tb())
        return None
    meta = c.read_meta(p)
    meta["sync"] = True
    c.write_meta(p, meta)
    n = res["added"] + res["updated"]
    return (f"fm sync: {res['added']} added, {res['updated']} updated from .foreman/"
            + (f"; {len(res['conflicts'])} conflict(s) (fm sync status)" if res["conflicts"] else "") + ".") if n or \
        res["conflicts"] else None


def session_context(p, sd, other_note=None):
    a = sd["active"]
    head = [f"Foreman project {p.slug} ({p.root}). Drive: {'on' if sd['drive'] else 'off'}"
            + (", paused" if sd["paused"] else "") + "."
            + (" Autonomy: full." if sd.get("autonomy") == "full" else "")
            + (f" State: fallback {c.state_dir()} (fm doctor)." if c.fallback_marker() else "")]
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
    try:
        focus.append("Next: " + c.next_for(p)[2])
    except Exception:  # a malformed brief costs the Next line, not the whole session context
        log_error("SessionStart", _tb())
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

# Lock waits (seconds). Hooks run on every event, so most wait briefly; the ones carrying the user's words or an fm ask
# wait longer, because dropping those costs more than a slow turn.
LOCK_QUICK = 1  # SessionStart heartbeat, Stop drive counters: losing one is harmless
LOCK_WORDS = 3  # UserPromptSubmit: on timeout it says the message wasn't recorded
LOCK_SLOW = 5  # recording an fm ask (dropping it makes fm ask refuse), PreCompact checkpoint

_PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)


_YES = re.compile(r"^\W*(yes|y|yep|yeah|yup|sure|ok|okay|approved?|confirm(ed)?|lgtm|go(\s+ahead)?|do it)\b(?!\s*\?)"
                  r"(?!\W*(?:but\s+)?(?:no\b(?!\s+(?:problem|worries))|not\b|don'?t\b|do\s+not\b|never\b|wait\b|"
                  r"hold\b|cancel\b|stop\b|actually\b))", re.I)  # a negation right after the yes cancels it


def _pin_hashes(pins):
    """{plugin id: content hash} for the pins an approval may record, computed before the project lock is taken."""
    pins = [x for x in pins if x]
    if not pins:
        return {}
    import fmplugins
    return {x: fmplugins.content_hash(x) for x in pins}


def _resolve_approvals(p, meta, sid, text, hashes=None):
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
        fresh = bool(at) and time.time() - at.timestamp() < c.APPROVAL_TTL
        b = c.find_brief(p, a["task"]) if yes and fresh else None
        if b:
            _grant(p, b, a["allow"], sid, "chat", pin=a.get("pin"), h=(hashes or {}).get(a.get("pin")),
                   reply=c.redact(text[:80]))
            notes.append(f"User approved {cats} for {b.id}")
        else:
            c.log_event(p, "approval_declined", task=a["task"], data={"allow": a["allow"], "expired": not fresh},
                        session=sid)
            notes.append(f"Pending {cats} for {a['task']} not granted ({'expired' if not fresh else 'reply was not a yes'})")
    return notes


STATUS_WORDS = {"status", "where are we", "fm status", "what's the status", "whats the status"}
_CORRECTION = re.compile(r"(?i)^\W*(no\b[,.!\s]|nope\b|don'?t\b|do not\b|stop\b|that'?s (wrong|not)|not what i|wrong\b|"
                         r"i said\b|i meant\b|why did you\b|you (should|shouldn'?t)\b|never\b|please don'?t\b)")


def user_prompt_submit(pl):
    sid = pl.get("session_id")
    p = c.find_project(_cwd(pl), create=True)
    if not p:
        return None
    text = _PASTED.sub("", pl.get("prompt") or "").strip()
    if text.startswith("<task-notification>"):  # a background agent's result, not the user: no approvals, words, holds
        for tid in re.findall(r"<task-id>([\w-]+)</task-id>", text):
            _event({"kind": "bg_done", "session_id": sid, "id": tid})  # drive stops waiting on it
        return None
    if text.lower().strip(" ?.!") in STATUS_WORDS:  # R2: a state question costs no model tokens
        try:
            state = c.render_state(c.state_dict(p))
            return {"decision": "block", "reason": c.fit(state.split("\n", 2)[-1].strip(), 1800)
                    + "\n(Answered by Foreman from its state, without the model; ask in more words for more.)"}
        except Exception:
            log_error("UserPromptSubmit", _tb())
    r = c.parse_intake(text)
    if _CORRECTION.match(text):  # R2: the user's corrections, for /foreman:reflect to turn into durable preferences
        try:
            act = c.active_brief(c.load_briefs(p))
            c.log_event(p, "correction", task=act.id if act else None, data={"text": c.fit(c.plain(text), 300)},
                        session=sid)
        except Exception:
            log_error("UserPromptSubmit", _tb())
    try:
        hashes = _pin_hashes(a.get("pin") for a in c.read_meta(p).get("pending_approvals") or [] if isinstance(a, dict))
        with c.lock(p.dir, timeout=LOCK_WORDS):
            meta = c.read_meta(p)
            approvals = _resolve_approvals(p, meta, sid, text, hashes)
            prompts = _load_list(_prompts_path(p))  # a dialog still open when the user speaks was refused or ignored
            if any(a.get("session") == sid for a in prompts):
                c.write_atomic(_prompts_path(p), json.dumps([a for a in prompts if a.get("session") != sid]))
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
            hold = c.is_plan_only(text)
            if sid in g["drive"] or hold:
                g["drive"].setdefault(sid, {}).update(count=0, hold=hold)  # a plan-only prompt holds drive this turn
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
                     + (" plus block lines" if r.context or r.constraints or r.done_when or r.skip else "")
                     + "; canonical order CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE (fm intake prints it)")
    if c.is_plan_only(text):
        parts.append("Plan-only request: drive won't start implementation until the next message")
    if r.overrides:
        parts.append("Override word: " + ", ".join(r.overrides))
    elif c.is_exhaustive(text):
        parts.append("Exhaustive request (everything / fully featured): the Foreman procedure is /foreman:brainstorm in "
                     "super mode (fm ideas --rounds 4: rounds build on each other until dry), then every grounded idea")
    elif not r.items and c.is_open_ended(text):
        parts.append("Open-ended request with no concrete target; the Foreman procedure for it is /foreman:brainstorm")
    elif not r.items and c.is_work_request(text):
        parts.append("Untagged work request; Foreman intake classifies it first (type and tier on the reply's first "
                     "line), then briefs it (fm task new … --focus)")
    a, state = sd["active"], []
    if a:
        state.append(f"Active: {a['id']} {a['type']} " + (f"step {a['step']['n']}/{a['step']['of']}" if a["step"]
                                                        else f"{a['steps_done']}/{a['steps_total']} steps done"))
    else:
        state.append("No active task" + (f"; {len(sd['queue'])} queued" if sd["queue"] else ""))
    try:
        state.append("Next: " + c.next_for(p)[2])
    except Exception:
        log_error("UserPromptSubmit", _tb())
    if sd["inbox"]:
        state.append(f"Inbox: {len(sd['inbox'])}")
    if sd["paused"]:
        state.append("Drive paused")
    if sd.get("autonomy") == "full":
        state.append("Autonomy: full")
    if not _same_note(pl.get("session_id"), " | ".join(state)):  # unchanged state isn't repeated every turn
        parts += state
        nxt = next((x[6:] for x in state if x.startswith("Next: ")), None)
        if nxt:  # T-0051: fm usage compares it with what ran next
            _event({"kind": "next", "session_id": pl.get("session_id"), "project": p.slug, "action": nxt[:200]})
    out = {"terminalSequence": _title_seq(sd)}
    if parts:
        out["hookSpecificOutput"] = {"hookEventName": "UserPromptSubmit",
                                     "additionalContext": ("Foreman: " + ". ".join(parts) + ".")[:PROMPT_BUDGET]}
    return out


def _first_time(sid, key):
    """True the first time this session asks for key (a one-shot note); False after, or without a usable id."""
    if not sid or not re.fullmatch(r"[\w-]{1,100}", sid):
        return False
    path = os.path.join(c.state_dir(), "sessions", f"{sid}.{key}")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        os.close(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except OSError:
        return False


def _generated_note(pl, path):
    """R4: an edit of a generated or vendored file, said once per session per file."""
    import fmmap
    if not fmmap.is_generated(path):
        return None
    if not _first_time(pl.get("session_id"), "gen-" + hashlib.sha1(path.encode()).hexdigest()[:10]):
        return None
    return (f"Foreman: {os.path.basename(path)} looks generated or vendored; a hand edit is overwritten or drifts — "
            f"change its source or generator instead, unless that is the point.")


_JSONC = re.compile(r"(^|/)(tsconfig[^/]*|jsconfig[^/]*|devcontainer|\.eslintrc)\.json$|/\.vscode/")  # JSON with
# comments: valid for its tools, not for json.loads (Claude Code's own settings.json is strict JSON: still checked)


def _syntax_note(path):
    """R3: an edit that left a Python or JSON file unparsable, said right away (before a test run finds it)."""
    try:
        if not path.endswith((".py", ".json")) or not os.path.isfile(path) or os.path.getsize(path) > 2_000_000 \
                or _JSONC.search(path):
            return None
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if path.endswith(".py"):
            compile(text, path, "exec", dont_inherit=True)
        else:
            json.loads(text)
    except SyntaxError as e:
        return f"Foreman: {os.path.basename(path)}:{e.lineno}: SyntaxError: {e.msg} — the edit left it unparsable."
    except ValueError as e:  # JSONDecodeError, or undecodable bytes
        return f"Foreman: {os.path.basename(path)}: not valid JSON/UTF-8 after the edit: {c.fit(str(e), 120)}"
    except OSError:
        return None
    return None


THRASH = 6  # edits of one file with no check recorded in between


def _thrash_note(pl, p, act, path):
    """R1: the same file edited again and again with no check recorded in between is guessing, not converging."""
    n = 0
    for e in reversed(c.ledger_tail(p, 300)):
        if e.get("task") != act.id:
            continue
        if e.get("event") in ("evidence", "step_done", "check_run", "focus"):
            break
        if e.get("event") == "touched" and (e.get("data") or {}).get("file") == path:
            n += 1
    if n < THRASH or not _first_time(pl.get("session_id"), "thrash-" + hashlib.sha1(path.encode()).hexdigest()[:10]):
        return None
    return (f"Foreman: {os.path.basename(path)} has been edited {n} times without a check in between. State one "
            f"hypothesis (fm task log {act.id} \"hypothesis: …\"), test it, and log what it rules out before editing "
            f"again (skills/intake/references/debugging.md).")


BIG_READ = 600  # lines


def _big_read_note(pl, ti):
    """A whole-file Read of a big source file: say once per session that fm outline gives its map (T-0067)."""
    path = os.path.join(_cwd(pl), str(ti.get("file_path") or ""))
    if ti.get("offset") or ti.get("limit") or not path.endswith((".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java",
                                                                   ".rb", ".c", ".cc", ".cpp", ".kt", ".swift", ".php")):
        return None
    try:
        with open(path, "rb") as f:
            n = sum(chunk.count(b"\n") for chunk in iter(lambda: f.read(1 << 16), b""))
    except OSError:
        return None
    if n < BIG_READ or not _first_time(pl.get("session_id"), "outline"):
        return None
    return (f"Foreman: {os.path.basename(path)} is {n} lines. For big files, `fm outline PATH` lists definitions with "
            f"line ranges; then Read only the range you need (offset/limit).")


def _same_note(sid, text):
    """Whether this session was last told exactly this state; records it when not (SessionStart clears it)."""
    if not sid or not re.fullmatch(r"[\w-]{1,100}", sid):
        return False
    path = os.path.join(c.state_dir(), "sessions", f"{sid}.note")
    try:
        with open(path, encoding="utf-8") as f:
            if f.read() == text:
                return True
    except OSError:
        pass
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        c.write_atomic(path, text)
    except OSError:
        pass
    return False


# ---------------------------------------------------------------- PreToolUse (guard: fail closed)

def _pin_problem(b, target, current):
    """Why the plugin yes can't be spent on this change (T-0036), or None. target is what the guard read from the call
    (fmguard.plugin_target: a plugin id, "?" or None); current is that plugin's content hash now. An install or
    enable needs a yes pinned to that plugin, under 24 h old, whose content still hashes as when the user said yes; a
    change the guard can't tie to one plugin ("?") is never covered; while a pin is in place, nothing else is either."""
    pin = b.meta.get("plugin_pin")
    if target == "?":
        return ("run the fm plugins or claude plugin command itself, naming exactly one plugin, so it can be checked "
                "against the user's yes")
    if pin is not None and not (isinstance(pin, list) and len(pin) == 3):
        return f"{b.id}'s plugin_pin is malformed; ask again: fm ask {b.id} plugin --pin <plugin id> --why \"…\""
    if target is None:
        return (f"the user's plugin yes is pinned to installing or enabling {pin[0]}; ask separately for this change"
                if pin else None)
    ask = f"ask again: fm ask {b.id} plugin --pin {target} --why \"<what it adds>\""
    if not pin or pin[0] != target:
        return f"the user's plugin yes names {pin[0] if pin else 'no plugin'}, not {target}; {ask}"
    if not str(pin[2]).isdigit() or time.time() - int(pin[2]) >= c.APPROVAL_TTL:
        return f"the user's yes for {target} is over 24 h old; {ask}"
    if current != pin[1]:
        return f"{target} changed since the user's yes (its content no longer matches what they approved); {ask}"
    return None


def _use_plugin_grant(p, tid, detail, sid, guard=None):
    """A plugin yes covers one change (new code in every session): the call it lets through uses it up. None when
    spent, else why not. The content is hashed before the lock (it can take a while on a big plugin); the pin is
    checked on the brief re-read under the lock, so a newer yes another session just recorded is never burned by a
    call checked against the old one. Inside the guard's fail-closed try."""
    if guard is None:
        import fmguard as guard
    target = guard.plugin_target(detail)
    current = None
    if target and target != "?":
        import fmplugins
        current = fmplugins.content_hash(target)
    with c.lock(p.dir, timeout=LOCK_QUICK):
        b = c.find_brief(p, tid)
        if "plugin" not in (b.meta.get("allow") or []):
            return "the plugin yes was already used by another call (one yes covers one change)"
        problem = _pin_problem(b, target, current)
        if problem:
            return problem
        b.meta["allow"] = [x for x in b.meta.get("allow") or [] if x != "plugin"]
        b.meta.pop("plugin_pin", None)
        b.append_log(f"plugin grant used for: {str(detail)[:120]}")
        c.save_brief(p, b)
        c.log_event(p, "approval_used", task=tid, data={"allow": ["plugin"], "detail": str(detail)[:200]}, session=sid)
    return None


def _committed(name):
    """A library module as last committed in Foreman's repo (git HEAD), for when the working copy fails to import or
    run: a half-applied edit can't lock the session out, and protection stays on. None without a committed copy."""
    import subprocess
    import types
    lib = os.path.join(c.PLUGIN_ROOT, "lib")
    root = c.git_root(lib)
    # only Foreman's own repo (plugin/ at its top), never some other repository the plugin copy happens to sit in
    if not root or os.path.normpath(os.path.join(root, "plugin")) != os.path.normpath(c.PLUGIN_ROOT):
        return None
    rel = os.path.relpath(os.path.join(lib, f"{name}.py"), root).replace(os.sep, "/")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}  # GIT_DIR etc. would pick another repo
    try:
        r = subprocess.run(["git", "-C", root, "show", f"HEAD:{rel}"], capture_output=True, text=True, timeout=5,
                           env=env)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode or not r.stdout:
        return None
    mod = types.ModuleType(f"{name}_committed")  # registered under its own name, beside the working copy
    mod.__file__ = os.path.join(lib, f"{name}.py")  # fmcore finds its plugin folder from it
    sys.modules[mod.__name__] = mod
    exec(compile(r.stdout, f"HEAD:{rel}", "exec"), mod.__dict__)
    return mod


def _guard_decision(pl, guard):
    ctx, p, act = _guard_ctx(pl, guard)
    found = guard.findings(pl.get("tool_name", ""), pl.get("tool_input"), ctx)
    return ctx, p, act, found, guard.check(pl.get("tool_name", ""), pl.get("tool_input"), ctx, found)


def _pre_tool_use(raw):
    try:
        pl = json.loads(raw)
        tool = pl.get("tool_name", "")
        if tool not in GUARDED:
            return 0
        try:
            import fmguard as guard
            ctx, p, act, found, block = _guard_decision(pl, guard)
        except Exception:
            log_error("PreToolUse", "the working copy of fmguard failed; using the committed guard (fix "
                                    "plugin/lib/fmguard.py):\n" + _tb())
            guard = _committed("fmguard")
            if guard is None:
                raise
            ctx, p, act, found, block = _guard_decision(pl, guard)
        used = next((d for cat, d in found if cat == "plugin"), None) if not block and act else None
        if used is not None and "plugin" in ctx.allow:
            problem = _use_plugin_grant(p, act.id, used, pl.get("session_id"), guard)
            if problem:
                block = guard.Block("plugin", problem)
    except Exception as e:
        log_error("PreToolUse", _tb())
        print(f"Foreman guard internal error ({type(e).__name__}); the tool call was blocked (fail-closed). "
              f"Details: {os.path.join(c.state_dir(), 'logs', 'hooks.log')}. "
              f"If this persists: claude plugin disable foreman@foreman", file=sys.stderr)
        return 2
    if block:
        reason = guard.message(block, ctx)
        _event({"kind": "guard_block", "session_id": pl.get("session_id"), "category": block.category,
                "tool": tool, "target": str(block.detail)[:120], "project": p.slug if p else None})
        try:
            if p:
                c.log_event(p, "guard_block", task=act.id if act else None,
                            data={"category": block.category, "detail": str(block.detail)[:200]},
                            session=pl.get("session_id"))
        except Exception:
            log_error("PreToolUse", _tb())
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))
        print(reason, file=sys.stderr)
        return 2
    try:
        _record_asks(pl, p, guard)
        decision = _ask_prompt(pl, p, guard)
    except Exception:
        log_error("PreToolUse", _tb())
        decision = None
    if decision:  # fm ask: Claude Code's own permission prompt carries the request to the user
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision[0],
                                                 "permissionDecisionReason": decision[1]}}))
        return 2 if decision[0] == "deny" else 0
    gate = _no_task_gate(pl, p, act, ctx)
    if gate:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": gate}}))
        print(gate, file=sys.stderr)
        return 2
    try:
        note = " ".join(filter(None, [_scope_note(pl, p, act), _tripwire_note(pl, p, act)]))
        if note:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": note}}))
    except Exception:
        log_error("PreToolUse", _tb())
    return 0


def _guard_ctx(pl, fmguard):
    cwd, home = _cwd(pl), os.path.expanduser("~")
    p = act = None
    try:
        p = c.find_project(cwd)
        act = c.active_brief(c.load_briefs(p)) if p else None
    except Exception:
        log_error("PreToolUse", "the working copy of fmcore failed to read the task; trying the committed fmcore "
                                "(fix plugin/lib/fmcore.py):\n" + _tb())
        try:  # a bug in the library mustn't hide the active task's grants (the fix itself would be refused)
            cc = _committed("fmcore")
            p = cc.find_project(cwd) if cc else None
            act = cc.active_brief(cc.load_briefs(p)) if p else None
        except Exception:
            log_error("PreToolUse", _tb())  # unreadable state: no authorizations, guard still runs
    scratch = [s for s in (pl.get("scratchpad_dir"), "/tmp", "/var/tmp", os.environ.get("TMPDIR")) if s]
    ctx = fmguard.Ctx(cwd=cwd, project_root=fmguard.project_root_for(cwd, home), home=home,
                      foreman_home=c.foreman_home(), state_dir=c.state_dir(),
                      state_fallbacks=c.state_fallbacks(), scratch=scratch,
                      allow=set(act.meta.get("allow") or []) if act else set(), task_id=act.id if act else None)
    return ctx, p, act



def _record_asks(pl, p, fmguard):
    """Note each `fm ask` about to run, with the session id from the hook payload (the agent can't set that), so
    fm ask binds the request to the session that really asked instead of trusting its own environment."""
    if not p or pl.get("tool_name") != "Bash" or not pl.get("session_id"):
        return
    cmd, asks = (pl.get("tool_input") or {}).get("command") or "", []
    dialog = bool(fmguard.lone_fm_ask(cmd)) and not os.environ.get("FOREMAN_DRIVE_TASK")  # PreToolUse asks for one
    for args in fmguard.fm_calls(cmd):
        if len(args) > 2 and args[0] == "ask":
            task, cats, _, _, _ = _ask_target(args)
            asks.append({"task": task, "allow": cats, "session": pl["session_id"], "at": time.time(), "dialog": dialog})
    if not asks:
        return
    path = os.path.join(p.dir, "asks.json")
    with c.lock(p.dir, timeout=LOCK_SLOW):
        seen = _load_list(path)
        seen = [a for a in seen if time.time() - a.get("at", 0) < c.ASK_TTL] + asks
        c.write_atomic(path, json.dumps(seen[-20:]))


def _ask_target(args):
    """(task, sorted categories, why, problems, plugin pin) from `fm ask` arguments, read by fm's own parser so the dialog and
    the grant can't drift from what the command means."""
    import contextlib
    import io
    import fmcli
    try:
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):  # -h prints
            ns = fmcli.build_parser().parse_args(args)
    except SystemExit:
        return "", [], "", ["arguments fm ask doesn't accept"], None
    return ns.id, sorted(set(ns.categories)), ns.why or "", [], ns.pin


_plain = c.plain  # dialog text (fm ask): see fmcore.plain


def _grant(p, b, cats, sid, via, pin=None, h=None, **data):
    """The one place a user's approval becomes an authorization (chat reply or permission dialog). A plugin yes with
    a pin records the plugin and h, its content hash taken just before (outside the lock): plugin_pin: [id, h, epoch]
    (T-0036). The newest plugin yes defines what's allowed, so it replaces an earlier pin."""
    cats = list(cats)
    if "plugin" in cats:
        b.meta.pop("plugin_pin", None)
        if h:
            b.meta["plugin_pin"] = [pin, h, str(int(time.time()))]
            data["pin"] = pin
        elif pin:  # the plugin the yes named is gone: nothing to pin it to, so it grants nothing
            cats.remove("plugin")
            b.append_log(f"plugin yes for {pin} not granted: it is no longer installed or in a known marketplace")
    b.meta["allow"] = list(dict.fromkeys(list(b.meta.get("allow") or []) + cats))
    if cats:
        b.append_log(f"user approved {', '.join(cats)} " + ("in chat" if via == "chat" else "in Claude Code's permission prompt"))
    c.save_brief(p, b)
    if cats:
        c.log_event(p, "approval_granted", task=b.id, data=dict({"allow": cats, "via": via}, **data), session=sid)


def _ask_prompt(pl, p, fmguard):
    if not p or pl.get("tool_name") != "Bash":
        return None
    cmd = (pl.get("tool_input") or {}).get("command") or ""
    if not any(fmguard._fm_subcommand(a)[0] == "ask" for a in fmguard.fm_calls(cmd)):
        return None
    if not any(a[:1] == ["ask"] and not any(x in ("-p", "--project") or x.startswith("--project=") for x in a)
               for a in fmguard.fm_calls(cmd)):
        return ("deny", "Foreman: run fm ask from the project's directory, without -p, so the dialog and the grant "
                        "refer to the same task")
    args = fmguard.lone_fm_ask(cmd)
    if not args:
        return ("deny", "Foreman: run fm ask as its own Bash command (nothing chained, piped or substituted), so the "
                        "permission prompt approves exactly that request")
    task, cats, why, bad, pin = _ask_target(args)
    unknown = [x for x in cats if x not in fmguard.CATEGORIES or x in fmguard.NOT_AUTHORIZABLE]
    if pin:
        import fmplugins
        if "plugin" not in cats or not fmguard.PLUGIN_ID.fullmatch(pin) or fmplugins.content_hash(pin) is None:
            bad = bad + [f"--pin {_plain(pin)[:60]} (a known plugin, with the plugin category)"]
    if bad or unknown or not cats or not re.fullmatch(r"T-\d{4,}", task):
        return ("deny", f"Foreman: fm ask takes an id, categories ({', '.join(x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE)}) "
                        f"and --why; not {', '.join(bad + unknown) or 'this'}")
    if os.environ.get("FOREMAN_DRIVE_TASK"):  # fm run's claude -p: no one can answer a dialog here
        return ("deny", f"Foreman: nobody can answer a permission prompt in this headless session. Record it with "
                        f"fm task block {task} \"needs {', '.join(cats)} from the user\" and stop.")
    b = c.find_brief(p, task)
    return ("ask", f"Foreman asks you to grant {', '.join(cats)} for {task}"
                   + (f" ({_plain(b.title)[:70]})" if b else "") + (f": {c.redact(_plain(why))[:200]}" if why else "")
                   + (f". The plugin yes holds only for installing or enabling {pin} as its content is now"
                      + ("" if fmplugins.pin_covers_code(pin) else
                         " (a remote source: the pin covers its marketplace entry, not the code it fetches)")
                      if pin else "")
                   + ". Yes grants it to that task; No refuses. Only your answer here can grant it.")


def _prompts_path(p):
    return os.path.join(p.dir, "prompts.json")


def permission_request(pl):
    """Claude Code is about to show a permission dialog: note it for an `fm ask`, so only that approved call grants."""
    import fmguard
    args = fmguard.lone_fm_ask((pl.get("tool_input") or {}).get("command") or "") if pl.get("tool_name") == "Bash" else None
    p = c.find_project(_cwd(pl)) if args else None
    if not p or not pl.get("session_id"):
        return None
    task, cats, _, _, _ = _ask_target(args)
    with c.lock(p.dir, timeout=LOCK_SLOW):
        seen = [a for a in _load_list(_prompts_path(p)) if time.time() - a.get("at", 0) < c.APPROVAL_TTL]
        seen.append({"task": task, "allow": cats, "session": pl["session_id"], "tool_use_id": pl.get("tool_use_id"),
                     "at": time.time()})
        c.write_atomic(_prompts_path(p), json.dumps(seen[-20:]))
    return None


def _grant_prompted(pl, p):
    """PostToolUse of an `fm ask` the user approved in its permission dialog: grant it."""
    import fmguard
    args = fmguard.lone_fm_ask((pl.get("tool_input") or {}).get("command") or "")
    sid, tuid = pl.get("session_id"), pl.get("tool_use_id")
    if not args or not sid:
        return
    task, cats, _, _, pin = _ask_target(args)
    ok = [x for x in cats if x in fmguard.CATEGORIES and x not in fmguard.NOT_AUTHORIZABLE]
    h = _pin_hashes([pin]).get(pin)
    with c.lock(p.dir, timeout=LOCK_SLOW):
        seen = _load_list(_prompts_path(p))
        hit = next((a for a in seen if a.get("session") == sid and a.get("task") == task and a.get("allow") == cats
                    and time.time() - a.get("at", 0) < c.APPROVAL_TTL
                    and (not tuid or not a.get("tool_use_id") or a["tool_use_id"] == tuid)), None)
        b = c.find_brief(p, task)
        if not hit or not b or ok != cats:
            log_error("PostToolUse", f"fm ask for {task} ({', '.join(cats)}) ran but no permission dialog was recorded "
                                     f"for it: nothing granted (PermissionRequest hook not loaded? /reload-plugins)")
            return
        seen.remove(hit)
        c.write_atomic(_prompts_path(p), json.dumps(seen))
        _grant(p, b, cats, sid, "prompt", pin=pin, h=h, bound=bool(tuid and hit.get("tool_use_id")))
        meta = c.read_meta(p)
        meta["pending_approvals"] = [a for a in meta.get("pending_approvals") or []
                                     if not (isinstance(a, dict) and a.get("task") == task)]
        c.write_meta(p, meta)
        c.regen_views(p)


def _load_list(path):
    try:
        with open(path) as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def _edit_path(pl):
    ti = pl.get("tool_input") or {}
    target = ti.get("file_path") or ti.get("notebook_path") if isinstance(ti, dict) else None
    return os.path.normpath(os.path.join(_cwd(pl), target)) if target else None


def _in_project(path, p):
    return bool(path) and path.startswith(p.root.rstrip("/") + "/")


def _no_task_gate(pl, p, act, ctx):
    """File edits inside a Foreman project need an active task (rules: never edit without a brief)."""
    if not p or act or pl.get("tool_name") not in FILE_TOOLS:
        return None
    path = _edit_path(pl)
    exempt = [pl.get("scratchpad_dir"), os.path.join(ctx.home, ".claude", "projects")]  # session scratch, auto memory
    if not _in_project(path, p) or any(e and path.startswith(e.rstrip("/") + "/") for e in exempt):
        return None
    return (f"Foreman: no active task in {p.slug}, so {os.path.relpath(path, p.root)} can't be edited yet. One "
            f"command starts a small task: fm task new \"<title>\" --type FIX --tier S --ac \"<done when>\" "
            f"--step \"<step>\" --focus (bigger work: /foreman:intake; fm next says what's next).")


def _tripwire_note(pl, p, act):
    """An edit of a file a finished task touched and left a lesson about: that lesson, once per session per task."""
    if not p or pl.get("tool_name") not in FILE_TOOLS:
        return None
    path = _edit_path(pl)
    if not _in_project(path, p):
        return None
    import fmrecall
    hit = fmrecall.tripwire(p, os.path.relpath(path, p.root), act.id if act else None)
    if not hit or not _first_time(pl.get("session_id"), f"trip-{hit[0]}"):
        return None
    return c.fit(f"Foreman: {hit[0]} (done) also changed this file; its lesson: {hit[1]}", 320)


def _scope_note(pl, p, act):
    if not (p and act and pl.get("tool_name") in FILE_TOOLS):
        return None
    scope = act.meta.get("scope") or []
    path = _edit_path(pl)
    if not _in_project(path, p):
        return None  # not a project edit (auto memory, scratch, other repos)
    rel = os.path.relpath(path, p.root)
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
    if p and tool == "Bash":
        try:
            _auto_evidence(pl, p, ok)
        except Exception:
            log_error("PostToolUse", _tb())
    if ok and tool in ("TaskStop", "KillShell", "KillBash"):  # a stopped task sends no completion notice
        tid = ti.get("task_id") or ti.get("shell_id") or ti.get("bash_id")
        if tid:
            _event({"kind": "bg_done", "session_id": pl.get("session_id"), "id": str(tid)})
    if ok and tool == "Bash" and ti.get("run_in_background"):
        m = re.search(r"\bID:?\s*([\w-]+)|backgroundTaskId\W+([\w-]+)", json.dumps(pl.get("tool_response")))
        if m:
            _event({"kind": "bg_start", "session_id": pl.get("session_id"), "id": m.group(1) or m.group(2)})
    if ok and p and tool == "Bash":
        _grant_prompted(pl, p)
    if ok and p and tool in FILE_TOOLS:
        act = c.active_brief(c.load_briefs(p))
        path = os.path.normpath(os.path.join(_cwd(pl), ti.get("file_path") or ti.get("notebook_path") or ""))
        c.log_event(p, "touched", task=act.id if act else None, data={"file": path, "tool": tool},
                    session=pl.get("session_id"))
        note = _syntax_note(path) or _generated_note(pl, path) or (_thrash_note(pl, p, act, path) if act else None)
        if note:
            return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}}
    note = _big_read_note(pl, ti) if ok and tool == "Read" else None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}} if note else None


def _auto_evidence(pl, p, ok):
    """R6 (T-0063): a Bash command that is exactly a criterion's verify command is recorded as that criterion's
    evidence with its real result, as if fm had run it ([ran]); no second run through fm task evidence --run."""
    cmd = " ".join(str((pl.get("tool_input") or {}).get("command") or "").split())
    cmd = re.sub(r"^fm quiet (?:--(?:tail|timeout) \S+ )*(?:-- )?", "", cmd)  # the same check, run quietly
    act = c.active_brief(c.load_briefs(p)) if cmd else None
    hits = [n for n, v in (act.verify_cmds() if act else []) if v and " ".join(v.split()) == cmd]
    if not hits:
        return
    if ok:
        r = pl.get("tool_response")
        code, output = 0, f"{r.get('stdout') or ''}\n{r.get('stderr') or ''}" if isinstance(r, dict) else str(r or "")
    else:
        err = str(pl.get("error") or "")
        m = re.match(r"Exit code (\d+)", err)
        code, output = (int(m.group(1)) if m else 1), err.split("\n", 1)[-1]
    result, tree = c.run_result(code, c.redact(output)), c.worktree_id(p.root)
    with c.lock(p.dir, timeout=LOCK_QUICK):
        b = c.find_brief(p, act.id)
        for n in hits:
            b.add_evidence(cmd, result, ac=n, tree=tree, ran=True)
        c.save_brief(p, b)
        c.log_event(p, "evidence", task=b.id, data={"ac": hits, "cmd": cmd[:200], "auto": True},
                    session=pl.get("session_id"))


def post_tool_use_failure(pl):
    """Also failure memory (T-0046): a failed command whose failure a finished task already met gets a pointer to it."""
    post_tool_use(pl, ok=False)
    if pl.get("tool_name") != "Bash":
        return None
    try:
        p = c.find_project(_cwd(pl))
        if not p:
            return None
        import fmrecall
        act = c.active_brief(c.load_briefs(p))
        note = fmrecall.note_failure(p, act.id if act else None, str(pl.get("error") or ""))
    except Exception:
        log_error("PostToolUseFailure", _tb())
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUseFailure", "additionalContext": note}} if note else None


# ---------------------------------------------------------------- PreCompact

def pre_compact(pl):
    p = c.find_project(_cwd(pl))
    if p:
        with c.lock(p.dir, timeout=LOCK_SLOW):
            c.checkpoint(p, auto=True, session=pl.get("session_id"))
    return None


# ---------------------------------------------------------------- Stop: evidence gate + drive

_CLAIM = re.compile(r"\b(done|completed?|finished|fixed|implemented|all set|ready for review|works now|resolved|shipped)\b", re.I)
_NEG = re.compile(r"\b(not|isn't|isnt|aren't|haven't|hasn't|won't|wasn't|yet to|still)\b[\w\s,']{0,20}$", re.I)
_ASK = re.compile(r"(\?\s*$)|\b(should i|shall i|do you want|would you like|want me to"
                  r"|please (confirm|approve|choose|decide|advise|review)|let me know|awaiting your"
                  r"|need your (input|approval|decision|answer)|which (option|approach) do you)\b", re.I)


# what a claim is about, just before it in the same sentence: "steps 1–3 are done", "T-0012 done"
_STEP_HEADER = re.compile(r"▸\s*Step\s+(\d+)/\d+")  # the Foreman reply format's per-step header
_ABOUT = re.compile(r"\b(?:steps?\s+(\d+)(?:\s*(?:[–-]|to|and|,)\s*(\d+))?|(T-\d{4,}))\b[^.;\n]{0,40}$", re.I)


def claims_done(msg, step=None, finished=(), closed=()):
    """A completion claim, unless negated or about work that is already over: steps other than `step` that are all
    in `finished` (named just before it, or heading its section), or a task in `closed`. Naming a step or task that isn't over still counts as a claim."""
    for m in _CLAIM.finditer(msg or ""):
        before = msg[max(0, m.start() - 60):m.start()]
        if _NEG.search(before[-30:]):
            continue
        about = _ABOUT.search(before)
        if about and about.group(3) and about.group(3).upper() in closed:
            continue
        header = None
        for header in _STEP_HEADER.finditer(msg, 0, m.start()):
            pass
        if header and step is not None and int(header.group(1)) != step and int(header.group(1)) in finished:
            continue  # under a finished step's "▸ Step N/M" header: about that step, however far below it
        if about and about.group(1) and step is not None:
            span = range(int(about.group(1)), int(about.group(2) or about.group(1)) + 1)
            if step not in span and all(n in finished for n in span):
                continue
        return True
    return False


_FENCE = re.compile(r"```.*?(?:```|$)", re.S)
_QUESTION_LINE = re.compile(r"\?\**\s*$", re.M)


def needs_user(msg):
    """The reply ends with, or lists, questions for the user (numbered questions often sit above a summary)."""
    tail = _FENCE.sub("", (msg or "").strip())  # a "?" inside a code block isn't put to the user
    return bool(_ASK.search(tail[-400:]) or _QUESTION_LINE.search(tail[-2500:]))


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
    with c.lock(p.dir, timeout=LOCK_QUICK):
        g = _read_gate(p)
        _scan_notices(pl, g)
        reason = _evidence_gate(p, act, pl, g, {b.id for b in briefs if b.status in c.CLOSED}) or _question_nudge(pl) or _drive(p, sd, briefs, pl, g)
        d = g["drive"].setdefault(sid, {"count": 0})
        had_work, d["had_work"] = d.get("had_work"), bool(sd["active"] or sd["queue"])
        _write_gate(p, g)
    if not reason and ((act and needs_user(msg)) or (had_work and not d["had_work"])):
        seq += _notify_seq("waiting for your answer" if act else "queue empty")
    out = {"terminalSequence": seq}
    if reason:
        out.update(decision="block", reason=reason)
    return out


def _question_nudge(pl):
    """A question for the user left in the reply text gets lost when they type something else; the user asked for
    such blockers as Claude Code prompts. Sent back once per stop chain."""
    if pl.get("stop_hook_active") or os.environ.get("FOREMAN_DRIVE_TASK") or \
            not needs_user(pl.get("last_assistant_message")):
        return None  # (fm run's headless sessions have nobody to ask)
    return ("Foreman: the reply asks the user something in text. If it's yours to decide, decide it and record it "
            "(fm decide); otherwise ask it with the AskUserQuestion tool (one prompt, your default first), or "
            "fm ask for a guard category, so the answer can't be lost in chat. Where that tool isn't available "
            "(claude -p), decide with your default and record it. Either way, repeat what the user needs from the "
            "earlier reply (plan, order, results) in your final message: print mode shows only that one.")


def _evidence_gate(p, act, pl, g, closed=()):
    if not act or pl.get("stop_hook_active"):
        return None
    steps, cur = act.steps(), act.current_step()
    if not claims_done(pl.get("last_assistant_message"), step=cur.n if cur else None,
                       finished={s.n for s in steps if s.done}, closed=closed):
        return None
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


def _context_pct(sid):
    """Context-window use for a session, from the statusline's snapshot (state/sessions/<id>.json)."""
    try:
        with open(os.path.join(c.state_dir(), "sessions", f"{sid}.json")) as f:
            pct = json.load(f).get("context_pct")
        return int(pct) if pct is not None else None
    except (OSError, ValueError, TypeError):
        return None


BG_WAIT_S = 2 * 3600  # backstop: a start older than this is assumed finished (T-0096: 6 h stalled a 5-day session)


def _running(sid):
    """Background agents and commands of this session still running: their completion notification wakes the
    session, so drive waits instead of pushing busywork."""
    state = {}
    for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 1500):
        if e.get("session_id") != sid or (c.age_days(e.get("ts")) or 0) * 86400 > BG_WAIT_S:
            continue
        kind, key = e.get("kind"), e.get("agent_id") or e.get("id")
        if kind in ("subagent_start", "bg_start"):
            state[key] = True
        elif kind in ("subagent_stop", "bg_done"):
            state[key] = False
    return [k for k, on in state.items() if on]


def _scan_notices(pl, g):
    """Completion notices folded into a running turn never reach UserPromptSubmit (T-0096): read the transcript's new
    bytes for their task ids, from where the last Stop left off, so drive doesn't wait on work that already finished."""
    path, sid = pl.get("transcript_path"), pl.get("session_id")
    if not path or not sid:
        return
    offsets = g.setdefault("scan", {})
    try:
        start = offsets.get(sid, 0)
        if start > os.path.getsize(path):
            start = 0  # a new or rewritten transcript
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(8 * 1024 * 1024)  # ponytail: 8 MB per Stop; a huge first scan finishes over a few stops
    except OSError:
        return
    offsets[sid] = start + len(data)
    for tid in set(re.findall(rb"<task-id>([\w-]+)</task-id>", data)):
        _event({"kind": "bg_done", "session_id": sid, "id": tid.decode()})


def _drive(p, sd, briefs, pl, g):
    sid = pl.get("session_id")
    full = sd.get("autonomy") == "full"
    if not sd["drive"] or sd["paused"] or (needs_user(pl.get("last_assistant_message")) and not full):
        return None
    waiting = [t for t in sd.get("pending") or [] if t]
    if waiting and not full:
        return None  # an `fm ask` is open: the user's reply decides it
    scope = os.environ.get("FOREMAN_DRIVE_TASK")  # fm run: one task per fresh session; the next gets its own
    work = next((w for w in ([sd["active"]] if sd["active"] else []) + sd["queue"]
                 if w["id"] not in waiting and (not scope or w["id"] == scope)), None)
    if not work and full and not scope:  # T-0097: in full autonomy the user's captured requests are work too
        work = next((w for w in sd["inbox"] if w["id"] not in waiting), None)
    if not work:
        return None  # nothing left that doesn't need the user
    wb = next(b for b in briefs if b.id == work["id"])
    if c.waits_on_user(wb, waiting, "full" if full else "standard"):
        return None  # waiting on the user's approval (AUTONOMY standard)
    d = g["drive"].setdefault(sid, {"count": 0})
    if d.get("hold"):
        return None  # the user asked for planning only this turn
    bg = pl.get("background_tasks")  # T-0115: the engine's own in-flight list, when this build sends it
    running = [str(t.get("id")) for t in bg if isinstance(t, dict)] if isinstance(bg, list) else _running(sid)
    if running:  # background work is out; its completion notification wakes the session
        _event({"kind": "drive_wait", "session_id": sid, "task": work["id"], "running": running[:5]})
        return None
    if pl.get("stop_hook_active") and d.get("marks") and not _progressed(p, d["marks"], sid):
        return None  # no progress since the last continuation: let the turn end
    if d.get("count", 0) >= DRIVE_MAX:
        return None
    more = [x["id"] for x in sd["queue"] if x["id"] != work["id"]]
    what = (f"step {work['step']['n']}/{work['step']['of']} ({work['step']['text'][:80]}) is open" if work.get("step")
            else "is open" if sd["active"] and work["id"] == sd["active"]["id"]
            else "is captured in the inbox (plan it, then work it)" if work.get("status") == "captured"
            else "is next in the queue (not focused)")
    reason = (f"Foreman drive: {work['id']} {work['type']} {what}"
              + (f"; {len(more)} more queued ({', '.join(more[:4])})" if more else "")
              + (". Autonomy full: the user is not asked mid-run; decide with your default and record it (fm decide), "
                 "self-approve L/? plans after the self-critique, keep what needs the user (fm ask) for the final report"
                 + (f"; waiting on the user: {', '.join(waiting)}" if waiting else "") + "."
                 if full else
                 ". No question to the user or approval is pending. Drive ends when the queue is empty, "
                 "when a question or approval is needed, or with `fm drive off`."))
    try:
        reason += " Next: " + c.next_for(p, briefs)[2]
        pct = _context_pct(sid)
        if not sd["active"] and pct is not None and pct >= CONTEXT_NOTE_PCT:
            reason += (f" Context {pct}% used at a task boundary; Foreman state is saved, so this is a good point for "
                       f"the user to /compact or start a fresh session (auto-compaction will also handle it).")
    except Exception:
        log_error("Stop", _tb())
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
    """Secrets masked on screen. No task badge (T-0095): the statusline and the band show the task, without going stale."""
    delta = pl.get("delta") or ""
    shown = c.redact(delta)
    if shown != delta:
        return {"hookSpecificOutput": {"hookEventName": "MessageDisplay", "displayContent": shown}}
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
    "PermissionRequest": permission_request,
}
