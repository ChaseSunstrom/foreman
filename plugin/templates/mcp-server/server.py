#!/usr/bin/env python3
"""An MCP server over stdio (JSON-RPC 2.0, one message a line), made by Foreman's `fm mcp new`. Stdlib only.

One tool runs the wrapped command. Safety: argv only, never a shell; every argument is a string that matches ARG
(no leading '-', so never an option; no NUL; at most MAX_ARG characters) or, for the subcommand, one of SUBS; at most
MAX_ARGS arguments; a TIMEOUT and an output cap (MAX_OUT). Tune the constants, keep the checks.
Register: claude mcp add NAME -- python3 /path/to/server.py   (or: fm mcp register claude DIR)"""
import json
import re
import subprocess
import sys
import threading

NAME = "__NAME__"
WRAP = ["__WRAP__"]  # the command, as argv
SUBS = ["__SUBS__"]  # the subcommands the caller may pick (an enum); empty: none
DESCRIPTION = "__DESCRIPTION__"
ARG = re.compile(r"[^\x00-][^\x00]*")  # first character not '-' (never a flag), no NUL anywhere
MAX_ARG, MAX_ARGS, TIMEOUT, MAX_OUT, MAX_LINE = 200, 20, 30, 100_000, 1_000_000
VERSION = "2025-06-18"


def schema():
    props = {"args": {"type": "array", "maxItems": MAX_ARGS, "description": "arguments, each a plain value (no options)",
                      "items": {"type": "string", "pattern": "^[^\\u0000-][^\\u0000]*$", "maxLength": MAX_ARG}}}
    if SUBS:
        props["sub"] = {"type": "string", "enum": SUBS, "description": "the subcommand"}
    return {"type": "object", "properties": props, "required": ["sub"] if SUBS else [], "additionalProperties": False}


class Refused(Exception):
    pass


def argv_for(args):
    """The argv for one call, or Refused."""
    if not isinstance(args, dict) or set(args) - set(schema()["properties"]):
        raise Refused(f"arguments: an object with only {', '.join(schema()['properties'])}")
    argv = list(WRAP)
    if SUBS:
        if args.get("sub") not in SUBS:
            raise Refused(f"sub: one of {', '.join(SUBS)}")
        argv.append(args["sub"])
    words = args.get("args", [])
    if not isinstance(words, list) or len(words) > MAX_ARGS:
        raise Refused(f"args: a list of at most {MAX_ARGS} strings")
    for w in words:
        if not isinstance(w, str) or len(w) > MAX_ARG or not ARG.fullmatch(w):
            raise Refused(f"refused argument {str(w)[:40]!r}: a string of 1 to {MAX_ARG} characters, not starting "
                          "with '-', no NUL")
    return argv + words


def call(args):
    """(text, is_error) for one tool call."""
    try:
        argv = argv_for(args)
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    except Refused as e:
        return str(e), True
    except OSError as e:
        return f"can't run {WRAP[0]}: {e.strerror}", True
    fired = threading.Event()
    timer = threading.Timer(TIMEOUT, lambda: (fired.set(), proc.kill()))
    timer.start()
    try:
        data = proc.stdout.read(MAX_OUT + 1)  # read as it streams: never more than the cap is held
    finally:
        if len(data or b"") > MAX_OUT:
            proc.kill()
        code = proc.wait()
        timer.cancel()
    if fired.is_set() and len(data) <= MAX_OUT:
        return f"timed out after {TIMEOUT} s", True
    text = data[:MAX_OUT].decode("utf-8", "replace")
    if len(data) > MAX_OUT:
        return text + f"\n… cut at {MAX_OUT} bytes", False
    return text + ("" if code == 0 else f"\n(exit {code})"), code != 0


def answer(msg):
    """The response to one message, or None for a notification."""
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return {"jsonrpc": "2.0", "id": msg.get("id") if isinstance(msg, dict) else None,
                "error": {"code": -32600, "message": "Invalid Request"}}
    method, mid, params = msg["method"], msg.get("id"), msg.get("params") or {}
    if "id" not in msg:
        return None
    if method == "initialize":
        result = {"protocolVersion": params.get("protocolVersion") or VERSION,
                  "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": NAME, "version": "1"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [{"name": NAME, "description": DESCRIPTION, "inputSchema": schema()}]}
    elif method == "tools/call":
        if params.get("name") != NAME:
            text, err = f"no such tool: {str(params.get('name'))[:60]}", True
        else:
            text, err = call(params.get("arguments") or {})
        result = {"content": [{"type": "text", "text": text}], "isError": err}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    while True:
        line = sys.stdin.readline(MAX_LINE)
        if not line:
            break
        if len(line) >= MAX_LINE and not line.endswith("\n"):  # a line too long is refused, never held
            while (rest := sys.stdin.readline(MAX_LINE)) and not rest.endswith("\n"):
                pass
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request: too long"}}
        elif not line.strip():
            continue
        else:
            try:
                msg = json.loads(line)
            except ValueError:
                out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
            else:
                try:
                    out = answer(msg)
                except Exception as e:  # one bad request never ends the server
                    out = {"jsonrpc": "2.0", "id": msg.get("id") if isinstance(msg, dict) else None,
                           "error": {"code": -32603, "message": f"Internal error: {type(e).__name__}"}}
        if out is not None:
            sys.stdout.write(json.dumps(out) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
