"""fm mcp (T-0245): Foreman's memory and state as read-only MCP tools over stdio — JSON-RPC 2.0, one message a line,
stdlib only — so other agents and clients can read the project's state, next action, recall, research notes and
briefs. Each tool runs the matching read-only fm command (the CLI stays the one implementation); everything sent is
redacted; a sensitive project serves nothing. Registering it (`claude mcp add foreman -- fm mcp`) is the user's
step: the guard asks for the plugin category."""
import json
import os
import re
import subprocess
import sys

import fmcore as c

VERSION = "2025-06-18"
_TEXT = {"type": "object", "properties": {}, "additionalProperties": False}
TOOLS = [
    ("state", "The project's Foreman state: active task, queue, inbox, blocked work.", _TEXT, lambda a: ["state"]),
    ("next", "The one next required action and its procedure.", _TEXT, lambda a: ["next"]),
    ("recall", "Past work, decisions, lessons and research related to a question.",
     {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
     lambda a: ["recall", _need(a, "query", r"[^\x00-][^\x00]{0,499}")]),  # review: no leading -, so never a flag
    ("research_list", "The names of the project's saved research notes, newest first.", _TEXT, None),
    ("research_read", "One saved research note by name (from research_list).",
     {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}, None),
    ("task_show", "A task's brief: request, interpretation, criteria, steps, evidence and log.",
     {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]},
     lambda a: ["task", "show", _need(a, "id", r"T-[0-9]{4,}")]),
    ("checks", "The project's last gate run (fm check): each command, its exit and time.", _TEXT, None),
]
MAX_LINE = 1_000_000


class _Bad(Exception):
    pass


def _need(args, key, pattern):
    v = args.get(key) if isinstance(args, dict) else None
    if not isinstance(v, str) or not re.fullmatch(pattern, v):
        raise _Bad(f"{key}: expected {pattern}")
    return v


def _fm(p, argv):
    r = subprocess.run([sys.executable, os.path.join(c.PLUGIN_ROOT, "bin", "fm"), *argv], cwd=p.root,
                       capture_output=True, text=True, timeout=120, env=dict(os.environ, FOREMAN_NO_BACKGROUND="1"))
    return (r.stdout if r.returncode == 0 else (r.stderr or r.stdout)), r.returncode != 0


def _call(p, name, args):
    """(text, is_error) for one tool call."""
    if c.read_meta(p).get("sensitive"):
        return "sensitive project: fm mcp serves nothing from it", True
    tool = next((t for t in TOOLS if t[0] == name), None)
    if not tool:
        return f"no such tool: {c.fit(c.plain(str(name)), 60)}", True
    try:
        folder = os.path.join(p.dir, "research")
        if name == "research_list":
            names = sorted((n for n in os.listdir(folder) if n.endswith(".md")) if os.path.isdir(folder) else [],
                           key=lambda n: os.path.getmtime(os.path.join(folder, n)), reverse=True)
            return "\n".join(n[:-3] for n in names[:200]) or "(no research notes)", False
        if name == "research_read":
            note = _need(args, "name", r"[A-Za-z0-9][A-Za-z0-9._-]{0,120}")
            path = os.path.join(folder, note + ".md")
            if not os.path.isfile(path) or os.path.dirname(os.path.realpath(path)) != os.path.realpath(folder):
                return f"no research note named {note}", True
            with open(path, encoding="utf-8", errors="replace") as f:
                return f.read(200_000), False
        if name == "checks":  # review: the request's "check results", read from the ledger in-process
            run = next((e for e in reversed(c.ledger_tail(p, 5000)) if e.get("event") == "check_run"), None)
            if not run:
                return "(fm check hasn't run in this project)", False
            rows = (run.get("data") or {}).get("results") or []
            return "\n".join([f"fm check at {run.get('ts')}:"] + [
                f"{'✓' if r.get('exit') == 0 else '✗'} {r.get('cmd')} (exit {r.get('exit')}, {r.get('s')} s)"
                for r in rows if isinstance(r, dict)]), False
        return _fm(p, tool[3](args))
    except _Bad as e:
        return str(e), True
    except (OSError, subprocess.SubprocessError) as e:
        return f"{type(e).__name__}: {c.fit(str(e), 200)}", True


def _answer(p, msg):
    """The response to one message, or None for a notification."""
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return {"jsonrpc": "2.0", "id": msg.get("id") if isinstance(msg, dict) else None,
                "error": {"code": -32600, "message": "Invalid Request"}}
    method, mid, params = msg["method"], msg.get("id"), msg.get("params") or {}
    if "id" not in msg:  # notifications (initialized, cancelled): nothing to say
        return None
    if method == "initialize":
        result = {"protocolVersion": params.get("protocolVersion") or VERSION,
                  "capabilities": {"tools": {"listChanged": False}},
                  "serverInfo": {"name": "foreman", "version": "1"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        sensitive = c.read_meta(p).get("sensitive")
        result = {"tools": [] if sensitive else [{"name": n, "description": d, "inputSchema": s} for n, d, s, _ in TOOLS]}
    elif method == "tools/call":
        text, err = _call(p, params.get("name"), params.get("arguments") or {})
        result = {"content": [{"type": "text", "text": c.redact(text)}], "isError": err}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def cmd_mcp(args):
    import fmcli
    p = fmcli.resolve(args)
    while True:
        line = sys.stdin.readline(MAX_LINE)
        if not line:
            break
        if len(line) >= MAX_LINE and not line.endswith("\n"):  # review: a line too long is refused, never held
            while (rest := sys.stdin.readline(MAX_LINE)) and not rest.endswith("\n"):
                pass
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {
                "code": -32600, "message": f"Invalid Request: a message over {MAX_LINE} bytes"}}) + "\n")
            sys.stdout.flush()
            continue
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            try:
                out = _answer(p, msg)
            except Exception as e:  # one bad request never ends the server
                out = {"jsonrpc": "2.0", "id": msg.get("id") if isinstance(msg, dict) else None,
                       "error": {"code": -32603, "message": f"Internal error: {type(e).__name__}"}}
        if out is not None:
            sys.stdout.write(json.dumps(out) + "\n")
            sys.stdout.flush()
