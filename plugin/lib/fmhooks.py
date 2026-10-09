"""Foreman hook handlers. Entry point: run(event, raw_stdin) -> exit code (JSON, if any, goes to stdout).

Non-guard handlers fail open: any exception is logged to state/logs/hooks.log and the hook exits 0.
The PreToolUse guard fails closed: any exception blocks the tool call (exit 2).
Injected text is factual state, never instructions.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

import fmcore as c

CTX_BUDGET = 2000       # SessionStart additionalContext
PROMPT_BUDGET = 400     # UserPromptSubmit additionalContext
NOTE_BUDGET = 200       # PreToolUse scope note
DRIVE_MAX = 50          # consecutive drive continuations without a user prompt
OFFERS_MAX = 3          # T-0401: queued tasks offered, one per Stop, while one set of background jobs runs
LONG_JOB_S = 20 * 60    # T-0415: a background job running longer no longer holds the drive
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

def _quiet():
    """T-0077: FOREMAN_QUIET=1 marks a session an orchestrator drives: only the guard runs."""
    return os.environ.get("FOREMAN_QUIET", "") not in ("", "0")


BREAKER_FAILS, BREAKER_PAUSE_S = 3, 600  # T-0087: failures in a row that pause an event, and for how long
UNBREAKABLE = {"PreToolUse", "TaskCompleted"}  # gates: the guard fails closed, TaskCompleted refuses unevidenced work


def breaker():
    """{event: {"fails": failures in a row, "until": epoch it is paused until}}, shared by every project (the
    handlers are); an entry of any other shape is dropped, so a damaged file can't stop the hooks."""
    try:
        with open(os.path.join(c.state_dir(), "logs", "breaker.json"), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    return {k: v for k, v in data.items() if isinstance(v, dict) and num(v.get("fails", 0)) and num(v.get("until", 0))} \
        if isinstance(data, dict) else {}


def paused_hooks():
    now = time.time()
    return sorted(e for e, v in breaker().items() if v.get("until", 0) > now)


def _breaker_set(event, entry):
    """Record or clear an event's entry; False when the file couldn't be written."""
    br = breaker()
    br.pop(event, None) if entry is None else br.update({event: entry})
    try:  # ponytail: concurrent async hooks can lose an update; the next failure counts again
        c.write_atomic(os.path.join(c.state_dir(), "logs", "breaker.json"), json.dumps(br))
        return True
    except OSError:
        return False


def run(event, raw):
    t0 = time.monotonic()
    if event != "PreToolUse" and _quiet():
        return 0
    if event == "PreToolUse":
        code = _pre_tool_use(raw)
    else:
        code, state = 0, ({} if event in UNBREAKABLE else breaker().get(event) or {})
        if state.get("until", 0) > time.time():
            return 0  # T-0087: paused after failing in a row; fm doctor and the band say so
        try:
            payload = json.loads(raw) if raw.strip() else {}
            handler = HANDLERS.get(event)
            out = handler(payload) if handler else None
            if out is not None:
                print(json.dumps(out, ensure_ascii=False))
            if state:
                _breaker_set(event, None)
        except HookBlock as e:
            if state:
                _breaker_set(event, None)  # it ran: a block isn't a failure
            print(str(e), file=sys.stderr)
            code = 2
        except Exception:
            log_error(event, _tb())
            fails = state.get("fails", 0) + 1  # after a pause one more failure pauses it again
            until = time.time() + BREAKER_PAUSE_S if fails >= BREAKER_FAILS and event not in UNBREAKABLE else 0
            if _breaker_set(event, {"fails": fails, "until": until}) and until:
                log_error(event, f"paused for {BREAKER_PAUSE_S // 60} min after {fails} failures in a row "
                                 f"(it runs again at {time.strftime('%H:%M', time.localtime(until))})")
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
        busy = other_note is not None
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
        import fmeco  # T-0463, T-0574: the Foreman this project runs, on which machine (fm projects, fm doctor)
        meta.update(session={"id": sid, "seen": c.now()}, last_active=c.now(), sensitive=c.detect_sensitive(p.root),
                    foreman=fmeco.stamp())
        c.write_meta(p, meta)
        synced = _sync_import(p)
        sd = c.regen_views(p)
    if synced:
        other_note = " ".join(x for x in (other_note, synced) if x)
    c.log_event(p, "session_start", data={"source": pl.get("source"), "root": c.PLUGIN_ROOT},  # T-0391: the code
                session=sid)  # this session runs (fm doctor compares it with the installed one)
    if second_due(pl, meta, busy) and not os.environ.get("FOREMAN_NO_BACKGROUND"):  # T-0276: never in the hook's time
        try:
            subprocess.Popen([os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "second", "session", "--if-due",
                              "--exclude", sid or ""], cwd=p.root, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        except Exception:  # a review that can't start must never cost the session its start
            log_error("SessionStart", _tb())
    if pl.get("source") in (None, "startup", "resume") and not os.environ.get("FOREMAN_NO_BACKGROUND") \
            and not c.panicked():  # T-0482: Claude Code's version; a new one runs the checks
        try:  # review: canary_due too, inside — a surprise there must never blank the session start
            if fmeco.canary_due():
                subprocess.Popen([os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "canary", "--if-changed"], cwd=p.root,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 start_new_session=True)
        except Exception:
            log_error("SessionStart", _tb())
    try:  # T-0383: infer what builds on what (detached, once a day, when 3+ open tasks are new)
        import fmrelate
        if fmrelate.due(meta, [x["id"] for x in ([sd["active"]] if sd["active"] else []) + sd["queue"] + sd["inbox"]]):
            fmrelate.spawn(p)
    except Exception:
        log_error("SessionStart", _tb())
    out = {"hookEventName": "SessionStart", "additionalContext": session_context(p, sd, other_note)}
    first = not busy and _resume_turn(pl, sd)  # another session minutes ago: don't start a second driver
    if first:
        out["initialUserMessage"] = first
    return {"hookSpecificOutput": out, "terminalSequence": _title_seq(sd)}


def second_due(pl, meta, busy=False):
    """T-0276: a new session (not a compaction or /clear) in a project not reviewed today, not sensitive, and no other
    session active minutes ago (its transcript would be read as the "previous" one while it is still answering)."""
    return (not busy and pl.get("source") in (None, "startup", "resume") and meta.get("second_session") != c.now()[:10]
            and not meta.get("sensitive") and not c.panicked())


def _resume_turn(pl, sd):
    """T-0138: `claude --continue` with drive on and full autonomy starts its own first turn instead of waiting for a
    prompt. A fresh start may be for something else, and standard autonomy waits for the person."""
    if (pl.get("source") != "resume" or not sd["drive"] or sd["paused"] or sd.get("autonomy") != "full"
            or os.environ.get("FOREMAN_DRIVE_TASK")):
        return None
    waiting = [t for t in sd.get("pending") or [] if t]
    work = next((w for w in ([sd["active"]] if sd["active"] else []) + sd["queue"] + sd["inbox"]
                 if w["id"] not in waiting), None)
    return work and f"Continue the Foreman drive: {work['id']} — {work['title'][:100]}"


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


def _grants_note(meta):
    return ((" Standing yes: core (Foreman's code; fm standing off revokes)." if "core" in (meta.get("standing") or {})
             else "") + (" Trust: on (Claude may edit the guard and Claude Code settings; /fm-trust off ends it)."
                         if c.trusted() else ""))


def session_context(p, sd, other_note=None):
    a = sd["active"]
    head = [f"Foreman project {p.slug} ({p.root}). Drive: {'on' if sd['drive'] else 'off'}"
            + (", paused" if sd["paused"] else "") + "."
            + (" Autonomy: full." if sd.get("autonomy") == "full" else "")
            + (" PAUSED everywhere (fm pause): nothing unattended starts; the user lifts it." if sd.get("panic") else "")
            + _grants_note(c.read_meta(p))
            + (f" State: fallback {c.state_dir()} (fm doctor)." if c.fallback_marker() else "")]
    focus, resume = [], []
    if a:
        step = f"step {a['step']['n']}/{a['step']['of']}: {a['step']['text']}" if a["step"] else \
            f"{a['steps_done']}/{a['steps_total']} steps done"
        focus.append(f"Active: {a['id']} [{a['type']} {a['tier']}] {a['title']} — {step}.")
        info = c.resume_info(p)
        r = " / ".join(l.strip("- ").strip() for l in info.get("resume", "").replace("<!-- auto -->", "").splitlines()
                       if l.strip())
        if r:
            resume.append(f"Resume here: {r[:400]}")
        if info.get("stale"):  # T-0113
            resume.append(f"Stale since it started (gone from the repo now): {', '.join(info['stale'])[:300]} — "
                          f"re-check the brief before relying on it.")
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
    try:
        import fmmap
        mapped = [x for x in [fmmap.compact(p)] if x]
    except Exception:  # the map is a convenience: never the session context
        log_error("SessionStart", _tb())
        mapped = []
    text = ""
    for parts in ([head, focus, resume, mapped, queue, tail], [head, focus, resume, queue, tail],
                  [head, focus, queue, tail], [head, focus, tail]):
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
_CORRECTION = re.compile(r"(?i)^\W*(no\b[,.!\s]|nope\b|don['’]?t\b|do not\b|stop\b|that['’]?s (wrong|not)|not what i|"
                         r"wrong\b|i said\b|i meant\b|why did you\b|you (should|shouldn['’]?t)\b|never\b|please don['’]?t\b)")


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
            act = c.active_brief(c.load_briefs(p), p.lane)
            c.log_event(p, "correction", task=act.id if act else None, data={"text": c.fit(c.plain(text), 300)},
                        session=sid)
            c.add_veto(p, text)  # T-0251: "never X" is checked before the next X
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
            if (meta.get("resume_after_reload") or {}).get("session") == sid:
                meta.pop("resume_after_reload")  # T-0145: the reloaded mod's prompt (or the user's) resumed it
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
            # a plan-only prompt holds drive this turn; turn_at: when this turn began (T-0145)
            g["drive"].setdefault(sid, {}).update(count=0, hold=hold, turn_at=time.time())
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
                     + (" plus block lines" if r.context or r.constraints or r.done_when or r.skip
                        or any(i.own for i in r.items) else "")
                     + "; canonical order CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE (fm intake prints it)")
        a = sd["active"] if sd else None
        if a and any(i.urgent for i in r.items):  # T-0385: JARVIS finished three tasks before an urgent one
            parts.append(f"Urgent: fm checkpoint {a['id']} now and switch to it (don't finish {a['id']} first)")
    if c.is_plan_only(text):
        parts.append("Plan-only request: drive won't start implementation until the next message")
    if r.overrides:
        parts.append("Override word: " + ", ".join(r.overrides))
    elif c.is_exhaustive(text):
        parts.append("Exhaustive request (everything / fully featured): run fm mission --request \"<their words>\" (it "
                     "composes the mission, lenses and fm ideas line), then /foreman:brainstorm super mode (--rounds 4) until dry")
    elif not r.items and c.is_open_ended(text):
        parts.append("Open-ended request with no concrete target; the Foreman procedure for it is /foreman:brainstorm, "
                     "seeded by fm mission --request \"<their words>\"")
    elif c.is_broad(text):
        parts.append("Broad request: sweep the whole space before planning (fm ideas --lens 'capability map' "
                     "--lens approaches, or a capability list in the brief)")
    if c.is_sweep(text):
        parts.append("Repo-wide cleanup: tier L, playbook clean/repo-sweep.md (every area checked by a stated method; "
                     "a tool finding nothing isn't done)")
    if not r.items and not r.overrides and c.is_work_request(text):  # T-0364: a one-liner brief skipped the thinking
        parts.append("Work request: classify it (type and tier) on your first line; S → fm task new … --focus; "
                     "M/L → plan before any edit (/foreman:intake §2: every capability and approach, then choose)")
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
            try:
                c.hints_shown(p, nxt)  # T-0250: what was shown and not used gets quieter
            except Exception:
                log_error("UserPromptSubmit", _tb())
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
        if tool in ("Agent", "Task"):  # T-0320: subagents wait only while usage runs ahead of pace
            try:
                import fmbudget
                fmbudget.check_subagent()
            except ValueError as e:  # BudgetError: over the cap
                print(f"Foreman {e}", file=sys.stderr)
                return 2
            except Exception:  # a spend cap, not a safety check: a broken budget never blocks work
                log_error("PreToolUse", _tb())
            return 0
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
        if block.category == "brief" and p:  # T-0409: the work in progress is usually right there in the queue
            try:
                nxt = next(iter(c.order_queue(c.load_briefs(p))[0]), None)
            except Exception:
                nxt = None
            if nxt:
                reason += f" To continue the queued work instead: fm focus {nxt.id} ({c.fit(nxt.title, 60)})."
        if _repeat_streak(pl.get("session_id"), block.category, str(block.detail)[:120]) >= 2:  # T-0440: 3rd in a row
            tid = act.id if act else "ID"
            how = (f"ask the user (fm ask {tid} {block.category} --why \"<what and why>\"), or "
                   if block.category not in guard.NOT_AUTHORIZABLE else "")
            reason += (f" Stop retrying: this exact refusal came 3 times in a row. Instead, {how}record why the task "
                       f"can't go on (fm task block {tid} \"<why>\") and take the next task.")
        _event({"kind": "guard_block", "session_id": pl.get("session_id"), "category": block.category,
                "rule": getattr(block, "rule", None), "tool": tool, "target": str(block.detail)[:120], "project": p.slug if p else None,
                "cmd": _window(c.redact(_target(pl.get("tool_input") or {})), block.detail)})  # T-0172, T-0423
        try:
            if p:
                c.log_event(p, "guard_block", task=act.id if act else None,
                            data={"category": block.category, "detail": str(block.detail)[:200],
                                  "rule": getattr(block, "rule", None)},  # T-0672 (committed fallback may lack it)
                            session=pl.get("session_id"))
        except Exception:
            log_error("PreToolUse", _tb())
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": reason}}))
        print(reason, file=sys.stderr)
        return 2
    try:
        _record_asks(pl, p, guard)
        decision = _ask_prompt(pl, p, guard) or _wait_loop(pl)
    except Exception:
        log_error("PreToolUse", _tb())
        decision = None
    if decision:  # fm ask: Claude Code's own permission prompt carries the request to the user
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision[0],
                                                 "permissionDecisionReason": decision[1]}}))
        return 2 if decision[0] == "deny" else 0
    if _quiet():
        return 0  # T-0077: the guard has spoken; no brief requirement or notes in a session another tool drives
    try:
        note = " ".join(filter(None, [_veto_note(pl, p), _scope_note(pl, p, act), _tripwire_note(pl, p, act)]))
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
        act = c.active_brief(c.load_briefs(p), p.lane) if p else None
    except Exception:
        log_error("PreToolUse", "the working copy of fmcore failed to read the task; trying the committed fmcore "
                                "(fix plugin/lib/fmcore.py):\n" + _tb())
        try:  # a bug in the library mustn't hide the active task's grants (the fix itself would be refused)
            cc = _committed("fmcore")
            p = cc.find_project(cwd) if cc else None
            lane = getattr(p, "lane", None)  # a committed copy from before lanes only finds main checkouts
            act = (cc.active_brief(cc.load_briefs(p), lane) if lane else cc.active_brief(cc.load_briefs(p))) if p else None
        except Exception:
            log_error("PreToolUse", _tb())  # unreadable state: no authorizations, guard still runs
    scratch = [s for s in (pl.get("scratchpad_dir"), "/tmp", "/var/tmp", os.environ.get("TMPDIR")) if s]
    try:
        meta = c.read_meta(p) if p else {}
    except Exception:
        meta = {}  # unreadable: no standing yes or trust, the guard asks as before
    ctx = fmguard.Ctx(cwd=cwd, project_root=fmguard.project_root_for(cwd, home), home=home,
                      foreman_home=c.foreman_home(), state_dir=c.state_dir(),
                      state_fallbacks=c.state_fallbacks(), scratch=scratch,
                      allow=set(act.meta.get("allow") or []) if act else set(), task_id=act.id if act else None,
                      standing=set(meta.get("standing") or {}), trusted=bool(c.trusted()),
                      confine=(p.lane, c.main_worktree(p.lane)) if p and getattr(p, "lane", None) and act
                      and act.meta.get("builder") else None,
                      unbriefed=p.root if p and not act and not _quiet() else None)  # T-0308: Bash writes too
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
            task, cats, *_ = _ask_target(args)
            asks.append({"task": task, "allow": cats, "session": pl["session_id"], "at": time.time(), "dialog": dialog})
    if not asks:
        return
    path = os.path.join(p.dir, "asks.json")
    with c.lock(p.dir, timeout=LOCK_SLOW):
        seen = _load_list(path)
        seen = [a for a in seen if time.time() - a.get("at", 0) < c.ASK_TTL] + asks
        c.write_atomic(path, json.dumps(seen[-20:]))


def _ask_target(args):
    """(task, sorted categories, why, problems, plugin pin, standing) from `fm ask` arguments, read by fm's own parser so
    the dialog and the grant can't drift from what the command means."""
    import contextlib
    import io
    import fmcli
    try:
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):  # -h prints
            ns = fmcli.build_parser().parse_args(args)
    except SystemExit:
        return "", [], "", ["arguments fm ask doesn't accept"], None, False
    return ns.id, sorted(set(ns.categories)), ns.why or "", [], ns.pin, bool(ns.standing)


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
    if set(cats) & set(_UNDO) and c.git_root(p.root):  # T-0672 (T-0478): where to come back to, as of this yes
        point = undo_point(p.root, b.id)
        if point.get("head"):
            b.append_log(f"undo point at this yes for {', '.join(sorted(set(cats) & set(_UNDO)))}: HEAD "
                         f"{point['head'][:12]}" + (f", tracked uncommitted work in {point['ref']} (git stash apply "
                                                    f"{point['ref']})" if point.get("ref") else
                                                    ", uncommitted work NOT recorded" if point.get("dirty") else ""))
    c.save_brief(p, b)
    if cats:
        c.log_event(p, "approval_granted", task=b.id, data=dict({"allow": cats, "via": via}, **data), session=sid)


_UNDO = {  # T-0672 (T-0478): what a destructive grant can and can't be brought back from (review: exactly)
    "git-destructive": "partly restorable: Foreman records HEAD and tracked uncommitted changes as of this yes; "
                       "untracked files (git clean) and remote history (a force push) are not covered",
    "rm-outside": "irreversible: files deleted outside the repo can't be brought back from git",
    "publish": "irreversible: a release, push to a registry or deploy can't be fully taken back",
    "system": "may be irreversible: system changes outside the repo aren't recorded",
}


def restorable(category):
    return _UNDO.get(category, "")


def undo_point(root, tid=None):
    """T-0672: {"head", "stash", "ref", "dirty"}: the commit the repo is on, and `git stash create`'s commit of tracked
    uncommitted work (never the stash list or the working tree), kept under refs/foreman/undo/<task> so gc can't take
    it; "dirty" when there was work but no stash commit came back (a timeout), so the log says it wasn't recorded."""
    head = c._git(root, "rev-parse", "HEAD").strip()
    stash = c._git(root, "stash", "create", timeout=10).strip()
    ref = f"refs/foreman/undo/{tid or 'grant'}"
    pinned = bool(stash) and c._git(root, "update-ref", ref, stash, fail=None) is not None
    dirty = not stash and bool(c._git(root, "status", "--porcelain", "--untracked-files=no").strip())
    return {"head": head, "stash": stash, "ref": ref if pinned else "", "dirty": dirty}


_WAIT_LOOP = re.compile(r"(?<![\w-])(?:until|while)\s.*?(?<![\w-])sleep\s+(?:(\d+(?:\.\d+)?)([smhd]?)|\$)", re.S)


def _wait_loop(pl):
    """T-0426 (JARVIS: `until grep -q … log; do sleep 20; done` held the session 10 minutes): a foreground loop that
    sleeps 5 s or more between checks leaves the session idle until it ends."""
    ti = pl.get("tool_input") or {}
    m = _WAIT_LOOP.search(ti.get("command") or "") if pl.get("tool_name") == "Bash" else None
    if not m or ti.get("run_in_background") or (
            m.group(1) and float(m.group(1)) * {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400}[m.group(2)] < 5):
        return None
    return ("deny", "Foreman: a foreground wait loop holds this session idle until it ends. Run it with "
                    "run_in_background (its completion notification wakes you) or as a Monitor, and do other work "
                    "meanwhile: the next step, another task, a builder lane.")


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
    task, cats, why, bad, pin, standing = _ask_target(args)
    unknown = [x for x in cats if x not in fmguard.CATEGORIES or x in fmguard.NOT_AUTHORIZABLE]
    if pin:
        import fmplugins
        if "plugin" not in cats or not fmguard.PLUGIN_ID.fullmatch(pin) or fmplugins.content_hash(pin) is None:
            bad = bad + [f"--pin {_plain(pin)[:60]} (a known plugin, with the plugin category)"]
    if standing and cats != ["core"]:
        bad = bad + ["--standing with anything but core alone"]
    if bad or unknown or not cats or not re.fullmatch(r"T-\d{4,}", task):
        return ("deny", f"Foreman: fm ask takes an id, categories ({', '.join(x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE)}) "
                        f"and --why; not {', '.join(bad + unknown) or 'this'}")
    if os.environ.get("FOREMAN_DRIVE_TASK"):  # fm run's claude -p: no one can answer a dialog here
        return ("deny", f"Foreman: nobody can answer a permission prompt in this headless session. Record it with "
                        f"fm task block {task} \"needs {', '.join(cats)} from the user\" and stop.")
    b = c.find_brief(p, task)
    if b and b.status in c.CLOSED and not standing:  # T-0302: the guard reads grants off the active task only
        return ("deny", f"Foreman: {task} is closed ({b.status}), and a grant works only while its task is active: "
                        f"ask on an open task (fm task new …, then fm ask NEW-ID …)")
    if standing:
        return ("ask", f"Foreman asks for a standing yes: core for {task} and every later task in this project, "
                       f"until you say stop (fm standing off). It covers Foreman's own code, rules and evals; Claude "
                       f"Code settings, Foreman state and the guard file still ask each time"
                       + (f": {c.redact(_plain(why))[:200]}" if why else "")
                       + ". Yes grants it; No refuses. Only your answer here can grant it.")
    return ("ask", f"Foreman asks you to grant {', '.join(cats)} for {task}"
                   + (f" ({_plain(b.title)[:70]})" if b else "") + (f": {c.redact(_plain(why))[:200]}" if why else "")
                   + (f". The plugin yes holds only for installing or enabling {pin} as its content is now"
                      + ("" if fmplugins.pin_covers_code(pin) else
                         " (a remote source: the pin covers its marketplace entry, not the code it fetches)")
                      if pin else "")
                   + "".join(f". {x}: {restorable(x)}" for x in cats if restorable(x))  # T-0672
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
    task, cats, *_ = _ask_target(args)
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
    task, cats, why, _, pin, standing = _ask_target(args)
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
        if standing and cats == ["core"]:  # T-0119: the dialog said "every later task"; fm standing off revokes
            meta["standing"] = dict(meta.get("standing") or {}, core={"at": c.now(), "task": task, "why": why[:200]})
            c.log_event(p, "standing_granted", task=task, data={"allow": ["core"], "why": why[:200]}, session=sid)
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


_EDIT_VERBS = "edit write change modify touch update overwrite create"


def _veto_note(pl, p):
    """T-0251: a command or edit that carries every key word of something the user said not to do: their words."""
    if not p:
        return None
    tool, ti = pl.get("tool_name"), pl.get("tool_input") or {}
    target = ti.get("command") if tool == "Bash" else f"{_EDIT_VERBS} {_edit_path(pl)}" if tool in FILE_TOOLS else None
    hits = c.veto_hits(p, target) if target else []
    if not hits:
        return None
    return " ".join(f"Foreman: the user said \"{v.get('said', '')}\" ({str(v.get('at', ''))[:10]}); this call matches "
                    f"it — ask first, or do it another way." for v in hits[:2])


def _tripwire_note(pl, p, act):
    """An edit of a file a finished task touched and left a lesson about: that lesson, once per session per task."""
    if not p or pl.get("tool_name") not in FILE_TOOLS:
        return None
    path = _edit_path(pl)
    if not _in_project(path, p):
        return None
    import fmrecall
    rel, sid = os.path.relpath(path, p.root), pl.get("session_id")
    hit = fmrecall.tripwire(p, rel, act.id if act else None)
    if not hit or not _first_time(sid, f"trip-{hit[0]}") or not _first_time(sid, f"tripfile-{rel}"):
        return None
    # T-0127: a task closed in this same session left its lesson in this context already
    if sid and any(e.get("event") == "task_done" and e.get("task") == hit[0] and e.get("session_id") == sid
                   for e in c.ledger_tail(p, 400)):
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


def _bash_touches(pl, p):
    """T-0086: files a Bash command changed (git status entries whose mtime falls inside the call) are the active
    task's touches, as an Edit's are, and one outside its scope gets the scope note (once per file)."""
    import subprocess
    act, top = c.active_brief(c.load_briefs(p), p.lane), c.git_root(p.root)
    if not act or not top:
        return None
    since = time.time() - (pl.get("duration_ms") or 0) / 1000 - 2  # mtime granularity and hook latency
    try:
        out = subprocess.run(["git", "-C", top, "status", "--porcelain", "-z", "--untracked-files=all"],
                             capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    entries, scope, outside, skip = out.split("\0"), act.meta.get("scope") or [], [], False
    for ent in entries:
        if skip or len(ent) < 4:  # a rename's original path follows it
            skip = False
            continue
        skip = ent[0] in "RC"
        full = os.path.join(top, ent[3:])  # porcelain paths are relative to the repository's top
        rel = os.path.relpath(full, p.root)
        try:
            mtime = os.path.getmtime(full)
            fresh = mtime >= since and os.path.isfile(full)
        except OSError:
            continue  # deleted: the task's diff at finish still sees it
        if not fresh or rel.startswith(("..", ".foreman/")):
            continue
        # timed by the file, not by this async hook: a scope reason the same command logged comes after it (T-0164)
        c.log_event(p, "touched", task=act.id, data={"file": full, "tool": "Bash", "at": c.iso(mtime)},
                    session=pl.get("session_id"))
        if scope and not any(c.glob_match(rel, s) for s in scope):
            outside.append(full)
    noted = {(e.get("data") or {}).get("file") for e in c.ledger_tail(p, 300)
             if e.get("event") == "scope_note" and e.get("task") == act.id} if outside else set()
    new = [f for f in outside if f not in noted]
    for f in new:
        c.log_event(p, "scope_note", task=act.id, data={"file": f}, session=pl.get("session_id"))
    rels = [os.path.relpath(f, p.root) for f in new]
    return (f"Foreman: that command changed {', '.join(rels[:5])}{' …' if len(rels) > 5 else ''}, outside {act.id} "
            f"scope [{', '.join(scope)}]."[:NOTE_BUDGET]) if new else None


# ---------------------------------------------------------------- PostToolUse / Failure (async)

def _target(ti):
    if not isinstance(ti, dict):
        return ""
    for k in ("file_path", "notebook_path", "command", "pattern", "url", "query", "description", "skill", "prompt"):
        if ti.get(k):
            return str(ti[k]).replace("\n", " ")
    return ""


def _repeat_streak(sid, category, target):
    """T-0440: how many of this session's latest tool events, back to back, were this same refusal."""
    n = 0
    for e in reversed(c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 400)):
        if e.get("session_id") != sid or e.get("kind") not in ("guard_block", "tool", "tool_fail"):
            continue
        if e.get("kind") != "guard_block" or e.get("category") != category or e.get("target") != target:
            break
        n += 1
    return n


def _window(cmd, detail, width=160):
    """T-0423: ~width chars of the command around where the block's target (the detail up to its first " (") or its
    variable first appears, so the event shows what tripped the guard; the head when nothing matches."""
    target = str(detail).split(" (", 1)[0].strip()
    var = re.match(r"\$\{?(\w+)", target)
    hit = target and (re.search(re.escape(target), cmd) or var and re.search(r"\$\{?" + var.group(1) + r"\b", cmd))
    if len(cmd) <= width or not hit:
        return c.fit(cmd, width)
    start = max(0, min(hit.start() - width // 3, len(cmd) - width + 2))
    end = start + width - 2
    return ("…" if start else "") + cmd[start:end] + ("…" if end < len(cmd) else "")


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
    if ok and p and tool == "Skill":
        try:
            c.hint_used(p, "skills")  # T-0250: the skills hint was worth showing
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
        note = _bash_touches(pl, p)
        if note:
            return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}}
    if ok and p and tool in FILE_TOOLS:
        act = c.active_brief(c.load_briefs(p), p.lane)
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
    act = c.active_brief(c.load_briefs(p), p.lane) if cmd else None
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
        cur = b.current_step()
        step = cur.n if code == 0 and cur and not b.has_evidence(step=cur.n) else None
        if step:  # T-0149: a passing criterion check verifies the step it ran in (the Stop gate asks per step)
            b.add_evidence(cmd, result, step=step, tree=tree, ran=True)
        c.save_brief(p, b)
        c.log_event(p, "evidence", task=b.id, data={"ac": hits, "step": step, "cmd": cmd[:200], "auto": True},
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
        act = c.active_brief(c.load_briefs(p), p.lane)
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
    act = c.active_brief(briefs, p.lane)
    seq = _title_seq(sd) + _progress_seq(sd)
    with c.lock(p.dir, timeout=LOCK_QUICK):
        g = _read_gate(p)
        _scan_notices(pl, g)
        d0 = g["drive"].get(sid) or {}
        # T-0147: a turn ending on purpose for a mod reload isn't held by the nudges; the resumed turn records evidence
        reload_due = sd["drive"] and _ui_changed(sid, _turn_began(p, sid, d0), d0.get("ui_mtime"))
        nudge = None if reload_due else (_evidence_gate(p, act, pl, g, {b.id for b in briefs if b.status in c.CLOSED})
                                         or _question_nudge(pl) or _headless_wait(pl))
        reason = nudge or _drive(p, sd, briefs, pl, g)
        d = g["drive"].setdefault(sid, {"count": 0})
        had_work, d["had_work"] = d.get("had_work"), bool(sd["active"] or sd["queue"])
        reloading, waiting_on = d.pop("reloading", None), d.pop("waiting_on", None)
        _write_gate(p, g)
    if not reason and ((act and needs_user(msg)) or (had_work and not d["had_work"])):
        seq += _notify_seq("waiting for your answer" if act else "queue empty")
    out = {"terminalSequence": seq}
    if reason:
        out.update(decision="block", reason=reason)
    elif reloading:
        out["systemMessage"] = ("Foreman: this turn ended so Claude Code reloads the Foreman UI you changed; the drive "
                                "picks up by itself (type continue if it doesn't)")
    elif waiting_on:
        out["systemMessage"] = (f"Foreman: the drive waits for background work ({', '.join(waiting_on)}) and continues "
                                f"when it finishes (type continue to go on now)")
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


def _headless():
    return os.environ.get("FOREMAN_DRIVE_TASK") or os.environ.get("CLAUDE_CODE_ENTRYPOINT") == "sdk-cli"


def _cc_version():
    """Claude Code's version as a tuple, read from `claude --version` at most once a day (state/claude-version); ()
    when unknown. T-0372: only headless stops ask, and they're rare."""
    path = os.path.join(c.state_dir(), "claude-version")
    try:
        if time.time() - os.path.getmtime(path) < 86400:
            with open(path, encoding="utf-8") as f:
                return tuple(int(x) for x in f.read().strip().split("."))
    except (OSError, ValueError):
        pass
    try:
        out = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=5).stdout
        m = re.match(r"\s*(\d+)\.(\d+)\.(\d+)", out)
        if not m:
            return ()
        c.write_atomic(path, ".".join(m.groups()) + "\n")
        return tuple(int(x) for x in m.groups())
    except (OSError, subprocess.SubprocessError):
        return ()


def _headless_wait(pl):
    """T-0310: claude -p (and fm run) ends with the turn, so a background task's notification never arrives: wait for
    it in this turn. Once per stop chain."""
    if pl.get("stop_hook_active") or not _headless() or _cc_version() >= (2, 1, 292):
        return None  # T-0372: from 2.1.292 claude -p waits for background work and wakes on it
    bg = pl.get("background_tasks")
    running = [str(t.get("id")) for t in bg if isinstance(t, dict)] if isinstance(bg, list) else \
        _running(pl.get("session_id"))
    if not running:
        return None
    return (f"Foreman: this is a headless run (claude -p): it ends with this turn, so the background work still running "
            f"({', '.join(running[:3])}) never reports back. Wait for it now (read its output until it finishes, or "
            f"rerun it in the foreground), then finish with its result.")


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
    if sd.get("panic") or not sd["drive"] or sd["paused"] or (needs_user(pl.get("last_assistant_message")) and not full):
        return None
    waiting = [t for t in sd.get("pending") or [] if t]
    if waiting and not full:
        return None  # an `fm ask` is open: the user's reply decides it
    scope = os.environ.get("FOREMAN_DRIVE_TASK")  # fm run: one task per fresh session; the next gets its own
    work = next((w for w in ([sd["active"]] if sd["active"] else []) + sd["queue"]
                 if w["id"] not in waiting and (not scope or w["id"] == scope)), None)
    if not work and full and not scope:  # T-0097: in full autonomy the user's captured requests are work too
        work = next((w for w in sd["inbox"] if w["id"] not in waiting), None)
    d = g["drive"].setdefault(sid, {"count": 0})
    if d.get("hold"):
        return None  # the user asked for planning only this turn
    if not work:  # nothing left that doesn't need the user
        # waiting: what's left is the user's; drained: checked already, and no task has been made since; review: only
        # after this turn worked a task (answering a question isn't a drain) and within DRIVE_MAX
        began = _turn_began(p, sid, d) or time.time()
        worked = any(time.time() - (c.age_days(b.meta.get("updated")) or 1e9) * 86400 >= began - 1 for b in briefs)
        if (not full or scope or waiting or d.get("drained") == len(briefs) or not worked or _headless()
                or d.get("count", 0) >= DRIVE_MAX):
            return None
        # T-0417: in full autonomy a drained queue is when to look at the product as its user does, once per drain
        d.update(drained=len(briefs), count=d.get("count", 0) + 1, marks=_marks(p))
        _event({"kind": "drive_drained", "session_id": sid, "project": p.slug})  # project: fm explain (T-0464)
        return ("Foreman drive: the queue is empty. Before stopping, check the product the way its user uses it: "
                + ("fm smoke, then " if (c.read_meta(p).get("smoke") or {}).get("web") else "")
                + "every screen at desktop and phone width (or every command), the main flows, the service logs. "
                  "fm capture --source self each defect or gap, then plan and work the first. If everything holds, "
                  "say so in one line and stop.")
    wb = next(b for b in briefs if b.id == work["id"])
    if c.waits_on_user(wb, waiting, "full" if full else "standard"):
        return None  # waiting on the user's approval (AUTONOMY standard)
    bg = pl.get("background_tasks")  # T-0115: the engine's own in-flight list, when this build sends it
    running = sorted(str(t.get("id")) for t in bg if isinstance(t, dict)) if isinstance(bg, list) else sorted(_running(sid))
    # T-0415: a job running for LONG_JOB_S is a service (a workflow, a watch, a server), not something to wait for
    now, since = time.time(), d.setdefault("since", {})
    d["since"] = since = {k: since.get(k, now) for k in running}
    agents = {str(t.get("id")) for t in bg if isinstance(t, dict) and t.get("type") == "agent"} if isinstance(bg, list) \
        else set()  # T-0575: a subagent (a builder can take 30 min) is work that ends, never a service
    running = [k for k in running if k in agents or now - since[k] < LONG_JOB_S]
    if running and sd["active"]:  # background work is out; its notification wakes the session (no active task:
        # the jobs don't hold back starting the next one)
        first = d.get("waited") != running[:5]  # sorted: the same jobs in another order aren't a new set
        if first:  # one wait, one event (T-0152: every Stop counted again in fm friction)
            _event({"kind": "drive_wait", "session_id": sid, "project": p.slug, "task": work["id"],
                    "running": running[:5]})
            d["offered"] = []
        d.update(waited=running[:5], waiting_on=running[:3])  # waiting_on: said on screen, a silent end reads as a stall
        if _headless() or d.get("count", 0) >= DRIVE_MAX:
            return None
        offered = d.get("offered") or []
        offer = _side_work(sd, briefs, work, full, offered) if len(offered) < OFFERS_MAX else None
        if offer:  # T-0401: a concrete next task, a new one each Stop, instead of one generic push and then idling
            d.update(offered=offered + [offer["id"]], count=d.get("count", 0) + 1, marks=_marks(p))
            how = _start_how(offer, lanes_free(briefs))
            _event({"kind": "drive_offer", "session_id": sid, "project": p.slug, "task": work["id"],
                    "offer": offer["id"], "how": how})
            return (f"Foreman drive: background work is still running ({', '.join(running[:3])}); don't idle on it. "
                    f"Start {offer['id']} ({offer['tier']} {offer['type']}: {c.fit(offer['title'], 80)}) now: {how}. "
                    f"A queued task that can't move now (it needs a device, a person, another task): fm task block ID "
                    f"\"why\", and take the next. The drive offers another when you stop; its notification still "
                    f"wakes you for {work['id']}.")
        if not first:
            return None
        # T-0364: once per running set, work on what doesn't need it instead of idling (357 waits vs 11 pushes)
        d.update(count=d.get("count", 0) + 1, marks=_marks(p))
        more = [x["id"] for x in sd["queue"] + (sd["inbox"] if full else []) if x["id"] != work["id"]][:3]
        if not more and full and d.get("drained") != len(briefs):  # T-0415: nothing else queued: find the next
            d["drained"] = len(briefs)  # work rather than wait; once per drain, as below, not once per set of jobs
            return (f"Foreman drive: background work is still running ({', '.join(running[:3])}) and nothing else is "
                    f"queued; don't wait on it. Check the product end to end as its user uses it (every screen at "
                    f"desktop and phone width, or every command; the main flows; the service logs), fm capture each "
                    f"defect or gap you find, then plan and work the first. Its notification still wakes you for "
                    f"{work['id']}.")
        return (f"Foreman drive: background work is still running ({', '.join(running[:3])}); its notification wakes "
                f"you, so don't sleep or poll. Meanwhile do what doesn't need its result: the next step's test, the "
                f"audit lenses on the current diff (fm audit prep), docs, "
                + (f"grounding and planning {', '.join(more)}, or an independent S/M task in a builder lane "
                   f"(fm lane brief ID). " if more else "planning what comes after this task. ")
                + "If nothing is independent of it, end the turn with one line naming what you wait on.")
    d.pop("waited", None)
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
    changed = _ui_changed(sid, _turn_began(p, sid, d), d.get("ui_mtime"))
    if changed:  # T-0145: Claude Code hot-reloads only at a real turn end; the reloaded mod resumes (fm ui --json)
        meta = c.read_meta(p)  # the caller holds the lock
        meta["resume_after_reload"] = {"session": sid, "at": c.now(), "task": work["id"]}
        c.write_meta(p, meta)
        d.update(ui_mtime=changed, reloading=True)
        _event({"kind": "drive_reload", "session_id": sid, "project": p.slug, "task": work["id"]})
        return None
    _event({"kind": "drive", "session_id": sid, "project": p.slug, "task": work["id"]})
    d.update(count=d.get("count", 0) + 1, marks=_marks(p))
    return reason


def _side_work(sd, briefs, work, full, offered):
    """T-0401: the next queued task (then, in full autonomy, captured one) that can move while the active one's
    background jobs run: not the active one, not offered already for this set, not waiting on the active task
    (depends_on or what fm relate inferred), not already briefed for a builder lane."""
    by_id = {b.id: b for b in briefs}
    lanes = lanes_free(briefs)
    for x in sd["queue"] + (sd["inbox"] if full else []):
        b = by_id.get(x["id"])
        if (b is None or x["id"] == work["id"] or x["id"] in offered or work["id"] in c._deps(b)
                or b.meta.get("builder") or any(s.done for s in b.steps())  # T-0429: under way here already
                or b.section("Verification evidence").strip()):
            continue
        if (x.get("status") != "captured" and b.section("Plan review").strip()
                and not (lanes and x.get("tier") in ("S", "M"))):  # T-0700: planned and reviewed, no lane free:
            continue                                                 # nothing left to do on it from here
        return x
    return None


def lanes_free(briefs):
    """T-0700: whether fm lane brief would take another builder (it refuses past fmlanes.BUILDERS)."""
    import fmlanes
    return sum(1 for b in briefs if b.meta.get("builder") and b.status not in c.CLOSED) < fmlanes.BUILDERS


def _start_how(x, lanes=True):
    """How to start a side task: a builder lane for planned S/M work while a slot is free, planning for the rest."""
    if x.get("status") == "captured":
        return (f"plan it (fm task new \"<title>\" --from {x['id']} with its criteria and steps; /foreman:intake §2 "
                f"for M/L), so it's ready to run")
    if x.get("tier") in ("S", "M") and lanes:
        return f"fm lane brief {x['id']}, then launch the builder it prints (Agent, isolation worktree)"
    return f"ground it and sharpen its plan (fm second plan {x['id']}), so it's ready when the current task lands"


def _turn_began(p, sid, d):
    """When this session's turn began: the prompt hook's turn_at, else (a turn the old hook started) when it was seen."""
    seen = c.read_meta(p).get("session") or {}
    age = c.age_days(seen.get("seen")) if seen.get("id") == sid else None
    return d.get("turn_at") or (time.time() - age * 86400 if age is not None else None)


def _ui_changed(sid, since, handed):
    """The newest change to this session's hot-reloaded mods (~/.claude/dev-mods/<session>/, the types Claude Code
    writes on each load left out) made since this turn began and not yet handed to a reload, else None."""
    if not sid or not re.fullmatch(r"[\w-]{1,100}", sid) or not since:
        return None
    root = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "dev-mods", sid)
    newest = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # T-0203: tests and docs aren't loaded, so changing them needs no reload
        dirnames[:] = [n for n in dirnames if not (n == "types" and dirpath.endswith(".claude-plugin") or n == "tests")]
        for name in (n for n in filenames if not n.endswith(".md")):
            try:
                newest = max(newest, os.stat(os.path.join(dirpath, name)).st_mtime)
            except OSError:
                pass
    return newest if newest > max(since, handed or 0) else None


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
    if pl.get("agent_transcript_path"):  # T-0227: what the subagent used, against the day's cap
        try:
            import fmbudget
            tokens = fmbudget.transcript_tokens(pl["agent_transcript_path"])
            if tokens:
                fmbudget.record(f"subagent:{pl.get('agent_type') or '?'}", tokens=tokens,
                                detail=pl.get("agent_id") or "")
        except Exception:  # the ledger is bookkeeping: never the subagent's log event
            log_error("SubagentStop", _tb())
    p = c.find_project(_cwd(pl))
    if p and pl.get("agent_type"):
        act = c.active_brief(c.load_briefs(p), p.lane)
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
