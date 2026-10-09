"""T-0708 (Frontier 08, first slice): the control plane between Claude sessions on one machine, at zero tokens until
something happens. The bus: typed messages to a session or all, delivered by the hooks that already run (a note on
the next tool call; a session about to stop is held for its mail), and --wake types one short line into a session's
tmux pane. Leases: an edit leases the function it lands in; another session's edit inside it is refused, naming the
holder. The conductor: live sessions, their mail and leases, and one steer for all. Files under Foreman's state."""
import json
import os
import re
import subprocess
import time

import fmcore as c

LIVE_S = 15 * 60       # a session whose statusline wrote within this is live
LEASE_S = 20 * 60      # an edit holds its function this long, renewed by each edit
FRESH_ALL_S = 15 * 60  # a session reading mail for the first time gets broadcasts this recent
KEEP = 500             # messages kept
TYPES = ("note", "steer", "stop")
_DEF = re.compile(r"^(\s*)(?:(?:export|pub|async|static|public|private)\s+)*(?:def|class|function|fn|func)\s+(\w+)")


def _dir():
    d = os.path.join(c.state_dir(), "bus")
    os.makedirs(d, exist_ok=True)
    return d


def _sid(s):
    return re.sub(r"[^\w-]", "", str(s or ""))[:80]


# ---------------------------------------------------------------- bus

def send(to, text, kind="note", sender=None):
    if kind not in TYPES:
        raise ValueError(f"type is one of {', '.join(TYPES)}")
    msg = {"ts": c.now(), "t": time.time(), "from": _sid(sender) or "user", "to": "all" if to == "all" else _sid(to),
           "type": kind, "text": c.redact(str(text))[:2000]}
    path = os.path.join(_dir(), "mail.jsonl")
    with c.lock(_dir()):
        try:
            with open(path) as f:
                lines = f.read().splitlines()[-(KEEP - 1):]
        except OSError:
            lines = []
        c.write_atomic(path, "\n".join(lines + [json.dumps(msg)]) + "\n")
    return msg


def _for(msg, sid):
    to = msg.get("to") or ""
    return msg.get("from") != sid and (to == "all" or (len(to) >= 6 and sid.startswith(to)))


def unread(sid, mark=True):
    """Messages for this session it hasn't been shown, oldest first; shown now when mark."""
    sid = _sid(sid)
    if not sid:
        return []
    cur = os.path.join(_dir(), f"seen-{sid}")
    try:
        with open(os.path.join(_dir(), "mail.jsonl")) as f:
            msgs = [json.loads(x) for x in f if x.strip()]
    except (OSError, ValueError):
        return []
    try:
        with open(cur) as f:
            seen = float(f.read().strip() or 0)
        first = False
    except (OSError, ValueError):
        seen, first = 0.0, True
    out = [m for m in msgs if m.get("t", 0) > seen and _for(m, sid)
           and not (first and m.get("to") == "all" and m.get("t", 0) < time.time() - FRESH_ALL_S)]
    if mark and msgs:
        c.write_atomic(cur, str(max(m.get("t", 0) for m in msgs)))
    return out


def render(msgs):
    return " ".join(("Steer" if m["type"] == "steer" else "Stop request" if m["type"] == "stop" else "Message")
                    + f" from {m['from'][:8]} ({m['ts'][11:16]}): {m['text']}"
                    + (" — apply it to your active task and log it (fm task log ID \"steer: …\")."
                       if m["type"] == "steer" else "") for m in msgs)


def note(sid):
    """The PreToolUse note: this session's unread mail, once."""
    msgs = unread(sid)
    return ("Foreman mail: " + render(msgs)) if msgs else None


def wake(sid):
    """One short line typed into the session's tmux pane (the statusline recorded it), so an idle session reads its
    mail; False when no pane is known."""
    snap = _snapshot(sid)
    pane = (snap or {}).get("tmux_pane")
    if not pane or not re.fullmatch(r"%\d+", str(pane)):
        return False
    try:
        subprocess.run(["tmux", "send-keys", "-t", pane, "-l", "Foreman mail waiting: read it (fm bus read) and act on it"],
                       capture_output=True, timeout=10, check=True)
        subprocess.run(["tmux", "send-keys", "-t", pane, "Enter"], capture_output=True, timeout=10, check=True)
        return True
    except (OSError, subprocess.SubprocessError):
        return False


# ---------------------------------------------------------------- sessions

def _snapshot(sid):
    try:
        with open(os.path.join(c.state_dir(), "sessions", f"{_sid(sid)}.json")) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def live():
    """Snapshots of the sessions seen within LIVE_S, newest first."""
    import datetime
    d = os.path.join(c.state_dir(), "sessions")
    cut = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=LIVE_S)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    out = []
    for n in os.listdir(d) if os.path.isdir(d) else []:
        if n.endswith(".json"):
            s = _snapshot(n[:-5])
            if s and str(s.get("ts", "")) >= cut:
                out.append(s)
    return sorted(out, key=lambda s: str(s.get("ts")), reverse=True)


# ---------------------------------------------------------------- leases

def _leases():
    try:
        with open(os.path.join(_dir(), "leases.json")) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    now = time.time()
    return {k: v for k, v in data.items() if v.get("until", 0) > now}


def _write_leases(data):
    c.write_atomic(os.path.join(_dir(), "leases.json"), json.dumps(data, indent=1))


def _lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(2_000_000)
    except OSError:
        return None


def _region(text, snippet):
    """(first, last) 0-based lines of snippet in text, or None."""
    i = text.find(snippet) if snippet else -1
    if i < 0:
        return None
    a = text.count("\n", 0, i)
    return a, a + snippet.count("\n")


def _indent(s):
    return len(s) - len(s.lstrip())


def enclosing(text, region):
    """The innermost definition around a region, by indentation: its name, or None at top level.
    ponytail: indentation, not a parser; a language whose bodies aren't indented gets file-free edits."""
    lines = text.split("\n")
    a = region[0]
    want = next((_indent(lines[i]) for i in range(a, min(region[1] + 1, len(lines))) if lines[i].strip()), 0)
    for i in range(min(a, len(lines) - 1), -1, -1):
        m = _DEF.match(lines[i])
        if m and (len(m.group(1)) < want or i == a):
            return m.group(2)
    return None


def span(text, name):
    """(first, last) lines of the definition named name, or None."""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        m = _DEF.match(ln)
        if m and m.group(2) == name:
            ind, end = len(m.group(1)), len(lines) - 1
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and _indent(lines[j]) <= ind:
                    end = j - 1
                    break
            return i, end
    return None


def _edits(tool, ti):
    if tool == "MultiEdit":
        return [(e.get("old_string"), e.get("new_string")) for e in ti.get("edits") or [] if isinstance(e, dict)]
    return [(ti.get("old_string"), ti.get("new_string"))] if tool == "Edit" else []


def after_edit(pl, p, path):
    """PostToolUse: lease what this session's edit landed in (a Write leases the file)."""
    sid, tool = _sid(pl.get("session_id")), pl.get("tool_name")
    if not sid or not path.startswith(p.root.rstrip("/") + "/"):
        return
    rel = os.path.relpath(path, p.root)
    if tool == "Write":
        names = ["*"]
    else:
        text = _lines(path) or ""
        names = {n for _, new in _edits(tool, pl.get("tool_input") or {})
                 if (r := _region(text, new)) and (n := enclosing(text, r))}
    if not names:
        return
    act = c.active_brief(c.load_briefs(p), p.lane)
    with c.lock(_dir()):
        data = _leases()
        for n in names:
            data[f"{p.slug}:{rel}::{n}"] = {"session": sid, "task": act.id if act else None, "project": p.slug,
                                           "file": rel, "symbol": n, "until": time.time() + LEASE_S}
        _write_leases(data)


def conflict(pl, p, path):
    """PreToolUse: why another session's lease forbids this edit, or None."""
    sid, tool = _sid(pl.get("session_id")), pl.get("tool_name")
    if not path.startswith(p.root.rstrip("/") + "/"):
        return None
    rel = os.path.relpath(path, p.root)
    held = [v for v in _leases().values() if v["project"] == p.slug and v["file"] == rel and v["session"] != sid]
    if not held:
        return None
    text = _lines(path) or ""
    regions = [r for old, _ in _edits(tool, pl.get("tool_input") or {}) if (r := _region(text, old))]
    for v in held:
        s = None if v["symbol"] == "*" else span(text, v["symbol"])
        hit = tool in ("Write", "NotebookEdit") or v["symbol"] == "*" or (
            s and any(r[0] <= s[1] and s[0] <= r[1] for r in regions))
        if hit:
            left = int((v["until"] - time.time()) // 60) + 1
            what = rel if v["symbol"] == "*" else f"{rel}::{v['symbol']}"
            return (f"Foreman lease: {what} is leased by session {v['session'][:8]}"
                    + (f" ({v['task']})" if v.get("task") else "") + f" for {left} more min, which is editing it now. "
                    f"Work elsewhere meanwhile, or ask it: fm bus send {v['session'][:8]} \"<what you need>\".")
    return None


# ---------------------------------------------------------------- commands

def cmd_bus(args):
    import fmcli
    me = fmcli.session()
    if args.action == "send":
        if len(args.words) < 2:
            raise fmcli.UsageError("fm bus send <session|all> "<text>" [--type note|steer|stop] [--wake]")
        msg = send(args.words[0], " ".join(args.words[1:]), args.type, me)
        woke = [s for s in ([x["session_id"] for x in live()] if msg["to"] == "all" else [msg["to"]])
                if args.wake and wake(s)]
        return fmcli.out(args, dict(msg, woke=woke), f"Sent to {msg['to']}" + (f"; woke {len(woke)}" if woke else "")
                         + ".")
    msgs = unread(me or (args.words[0] if args.words else ""), mark=True)
    return fmcli.out(args, {"messages": msgs}, render(msgs) if msgs else "No unread mail.")


def cmd_lease(args):
    import fmcli
    p = fmcli.resolve(args)
    me = _sid(fmcli.session()) or "user"
    with c.lock(_dir()):
        data = _leases()
        if args.action in ("take", "drop"):
            if not args.target:
                raise fmcli.UsageError(f"fm lease {args.action} FILE[::SYMBOL]")
            rel, _, sym = args.target.partition("::")
            rel = os.path.relpath(os.path.abspath(rel), p.root) if os.path.exists(rel) else rel
            key = f"{p.slug}:{rel}::{sym or '*'}"
            if args.action == "drop":
                data.pop(key, None) if data.get(key, {}).get("session") in (me, None) else None
            elif data.get(key) and data[key]["session"] != me:
                raise fmcli.UsageError(f"{rel}::{sym or '*'} is leased by session {data[key]['session'][:8]}")
            else:
                data[key] = {"session": me, "task": None, "project": p.slug, "file": rel, "symbol": sym or "*",
                             "until": time.time() + args.minutes * 60}
            _write_leases(data)
    rows = [v for v in data.values() if v["project"] == p.slug]
    return fmcli.out(args, {"leases": rows}, "\n".join(
        f"{v['file']}::{v['symbol']}  session {v['session'][:8]}" + (f" ({v['task']})" if v.get("task") else "")
        + f", {int((v['until'] - time.time()) // 60) + 1} min left" for v in rows) or "No leases held.")


REMOTE_S = 60  # a remote's tiles are refreshed (detached, over the user's own ssh) when older than this
REMOTE_FM = "$HOME/.claude/foreman/plugin/bin/fm"


def rows(sessions=None):
    """The conductor's view of each live session here."""
    leases = _leases().values()
    out = []
    for s in live() if sessions is None else sessions:
        sid = s["session_id"]
        p = c.find_project(s["cwd"]) if s.get("cwd") and os.path.isdir(s["cwd"]) else None
        act = c.active_brief(c.load_briefs(p), p.lane) if p else None
        out.append({"session": sid, "project": s.get("project"), "task": act.id if act else None,
                    "title": c.fit(act.title, 80) if act else None, "context_pct": s.get("context_pct"),
                    "seen": s.get("ts"), "tmux": bool(s.get("tmux_pane")), "mail": len(unread(sid, mark=False)),
                    "leases": sum(v["session"] == sid for v in leases)})
    return out


def remotes():
    """{name: {"target": ssh target, "fm": its fm path}}: only machines the user added (fm conductor remote add)."""
    try:
        with open(os.path.join(_dir(), "remotes.json")) as f:
            data = json.load(f)
        return {k: v for k, v in data.items() if isinstance(v, dict) and v.get("target")}
    except (OSError, ValueError):
        return {}


def _ssh(r, command, timeout=20):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", r["target"], command],
                          capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)


def refresh(name):
    """Fetch a remote's live sessions into its cache (run detached by fleet())."""
    r = remotes().get(name)
    if not r:
        return
    try:
        out = _ssh(r, f"{r.get('fm') or REMOTE_FM} conductor --json")
        data = {"ts": c.now(), "sessions": json.loads(out.stdout).get("sessions") or []} if not out.returncode else \
            {"ts": c.now(), "sessions": [], "error": c.fit(out.stderr.strip() or f"exit {out.returncode}", 160)}
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        data = {"ts": c.now(), "sessions": [], "error": c.fit(str(e), 160)}
    c.write_atomic(os.path.join(_dir(), f"remote-{name}.json"), json.dumps(data))


def fleet():
    """Live sessions here and the cached tiles of each added remote; a stale cache starts a detached refresh."""
    import datetime
    out = rows()
    for name in remotes():
        path = os.path.join(_dir(), f"remote-{name}.json")
        try:
            with open(path) as f:
                cache = json.load(f)
        except (OSError, ValueError):
            cache = {}
        try:
            age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(
                str(cache.get("ts")).replace("Z", "+00:00"))).total_seconds()
        except ValueError:
            age = None
        if (age is None or age > REMOTE_S) and not os.environ.get("FOREMAN_NO_BACKGROUND"):
            subprocess.Popen([os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "conductor", "refresh", name],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        out += [dict(x, remote=name, age_s=round(age) if age is not None else None) for x in cache.get("sessions") or []
                if isinstance(x, dict)]
        if cache.get("error"):
            out.append({"session": "-", "remote": name, "error": cache["error"]})
    return out


def cmd_conductor(args):
    import fmcli
    import shlex
    if args.action == "remote":
        data = remotes()
        if args.words[:1] == ["add"] and len(args.words) in (3, 4):
            name, target = args.words[1], args.words[2]
            if not re.fullmatch(r"[\w.-]{1,40}", name) or not re.fullmatch(r"[\w.@:-]{1,200}", target):
                raise fmcli.UsageError("fm conductor remote add NAME [user@]host [FM_PATH]")
            data[name] = {"target": target, "fm": args.words[3] if len(args.words) == 4 else REMOTE_FM}
        elif args.words[:1] == ["rm"] and len(args.words) == 2:
            data.pop(args.words[1], None)
            try:
                os.unlink(os.path.join(_dir(), f"remote-{args.words[1]}.json"))
            except OSError:
                pass
        elif args.words:
            raise fmcli.UsageError("fm conductor remote [add NAME [user@]host [FM_PATH] | rm NAME]")
        if args.words:
            c.write_atomic(os.path.join(_dir(), "remotes.json"), json.dumps(data, indent=1))
        return fmcli.out(args, {"remotes": data}, "\n".join(f"{k}: {v['target']}" for k, v in data.items())
                         or "No remotes (fm conductor remote add NAME user@host). Nothing is fetched from elsewhere.")
    if args.action == "refresh":
        for name in args.words or list(remotes()):
            refresh(name)
        return 0
    sessions = live()
    if args.action == "steer":
        if not args.words:
            raise fmcli.UsageError("fm conductor steer \"<text>\" [--wake]")
        text = " ".join(args.words)
        send("all", text, "steer", fmcli.session())
        woke = [s["session_id"] for s in sessions if args.wake and wake(s["session_id"])]
        reached = []
        for name, r in remotes().items():  # the user's own machines, added by them
            try:
                ok = not _ssh(r, f"{r.get('fm') or REMOTE_FM} bus send all {shlex.quote(text)} --type steer").returncode
            except (OSError, subprocess.SubprocessError):
                ok = False
            reached.append(name) if ok else None
        return fmcli.out(args, {"sessions": len(sessions), "woke": woke, "remotes": reached},
                         f"Steer sent to {len(sessions)} live session(s)" + (f" and {', '.join(reached)}" if reached
                                                                             else "")
                         + (f"; woke {len(woke)}" if woke else "") + ".")
    found = rows(sessions)
    return fmcli.out(args, {"sessions": found}, ("Live sessions:\n" + "\n".join(
        f"  {r['session'][:8]}  {r['project'] or '-'}  {r['task'] or 'no task'}  ctx {r['context_pct']}%  "
        f"seen {str(r['seen'])[11:16]}  mail {r['mail']}  leases {r['leases']}" + ("  tmux" if r["tmux"] else "")
        for r in found)) if found else "No live sessions (none wrote a statusline in the last 15 min).")
