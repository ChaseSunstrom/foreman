"""fm flow FILE (T-1639): a user journey run in the headless Chromium fm shot finds (fmshot.Browser; nothing is
installed), as a verify command. One step a line, words split like a shell's (quote a selector or text with spaces);
blank lines and lines starting with # are skipped:

    goto URL|FILE          a file in the flow's folder (a path relative to it, or a file:// URL), or http(s) on
                           localhost, 127.0.0.1 or [::1] (--any-url: any http(s) page)
    click SELECTOR         the first match, once it is there and shown
    type SELECTOR TEXT     focus it, then insert TEXT as typed input after what is there
    expect SELECTOR [TEXT] it is there (and its text or value contains TEXT)
    wait MS                0 to 10000

Each element step waits up to --timeout seconds (default 10, at most 60) for its element; the whole journey at most
TOTAL_S. The flow is untrusted data (a cloned repo's): only these verbs, at most MAX_STEPS steps and MAX_ARG characters
a word; a selector or text reaches the page only as a JSON argument to one fixed function (ACT), never as code; and
every request the page makes (redirects, refreshes, clicked links, subresources) is held to the goto rule through
DevTools' Fetch domain: one outside it is failed, and a page that tries to go there fails its step. Exit 0: every step
held; 1: the step that failed is named (or the flow is malformed); 2: no browser, or it did not start: a journey never
passes without one."""
import json
import os
import pathlib
import re
import shlex
import sys
import time
import urllib.parse
import urllib.request

import fmshot

MAX_BYTES, MAX_STEPS, MAX_ARG, MAX_WAIT_MS = 256 << 10, 200, 2000, 10000
MAX_STEP_S, TOTAL_S, POLL_S, CLICK_S = 60, 600, 0.1, 0.25  # --timeout's cap, the journey's, the poll, after a click
MAX_NOTES = 10  # blocked subresources named per step
VERBS = {"goto": (1, 1), "click": (1, 1), "type": (2, 2), "expect": (1, 2), "wait": (1, 1)}
LOCAL = {"localhost", "127.0.0.1", "::1"}
NEVER = "fm-flow.nothing"  # an event that never comes: Browser.wait on it reads (and answers) events for a while
# The one function a step runs in the page: op, selector and text arrive as JSON values (see _act).
ACT = """(op, sel, text) => {
  let el;
  try { el = document.querySelector(sel); } catch (e) { return {bad: String(e && e.message).slice(0, 200)}; }
  if (!el) return {missing: true};
  if (op === "expect") {
    const shown = String(el.innerText || el.textContent || ""), value = typeof el.value === "string" ? el.value : "";
    return {ok: text === null || shown.includes(text) || value.includes(text), text: (shown || value).slice(0, 200)};
  }
  if (!el.getClientRects().length) return {hidden: true};
  el.scrollIntoView({block: "center", inline: "center"});
  if (op === "click") el.click();
  if (op === "type") {
    el.focus();
    if (el !== document.activeElement) return {unfocusable: true};
    try { const n = el.value.length; el.setSelectionRange(n, n); } catch (e) {}  // type after what is there
  }
  return {ok: true};
}"""


def _inside(path, root):
    """The real path of a file under root (links resolved); ValueError otherwise."""
    real, top = os.path.realpath(path), os.path.realpath(root)
    if not real.startswith(top + os.sep):
        raise ValueError(f"{path} is outside the flow's folder {root}")
    if not os.path.isfile(real):
        raise ValueError(f"no such file: {path}")
    return real


def target(word, root, any_url):
    """The URL a goto opens, rebuilt from its parts: a file under root, or http(s) on a local host (any host with
    any_url); ValueError for anything else."""
    if re.search(r"[\s\x00-\x1f\x7f\\]", word):  # Chrome reads a backslash as a slash; urlsplit doesn't
        raise ValueError(f"no spaces, control characters or backslashes in a URL: {word!r}")
    if not re.match(r"(?i)[a-z][a-z0-9+.-]*:", word):  # a path: relative to the flow's folder
        return pathlib.Path(_inside(os.path.join(root, word), root)).as_uri()
    try:
        u = urllib.parse.urlsplit(word)
        host, port = u.hostname, u.port
    except ValueError as e:
        raise ValueError(f"not a URL: {e}") from None
    scheme, tail = u.scheme.lower(), (f"?{u.query}" if u.query else "") + (f"#{u.fragment}" if u.fragment else "")
    if "@" in u.netloc:
        raise ValueError(f"no user@ in a URL: {word}")
    if scheme == "file" and host in (None, "localhost"):
        return pathlib.Path(_inside(urllib.request.url2pathname(u.path), root)).as_uri() + tail
    if scheme in ("http", "https") and host and (host in LOCAL or any_url):
        netloc = (f"[{host}]" if ":" in host else host) + (f":{port}" if port is not None else "")
        return urllib.parse.urlunsplit((scheme, netloc, u.path, u.query, u.fragment))
    raise ValueError("goto opens a file in the flow's folder or http(s) on localhost, 127.0.0.1 or [::1]"
                     + ("" if any_url else " (--any-url: any http(s) page)") + f", not {word}")


def allowed(url, root, any_url):
    try:
        target(url, root, any_url)
        return True
    except ValueError:
        return False


def parse(text, root, any_url=False):
    """The steps: [{n, line, verb, args}]; ValueError naming the line for anything else."""
    if len(text) > MAX_BYTES:
        raise ValueError(f"over {MAX_BYTES >> 10} KB")
    steps = []
    for no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            words = shlex.split(line)
            verb, args = words[0], words[1:]
            if verb not in VERBS:
                raise ValueError(f"{verb!r} isn't a step (the steps: {', '.join(VERBS)})")
            lo, hi = VERBS[verb]
            if not lo <= len(args) <= hi:
                raise ValueError(f"{verb} takes {lo}" + (f" or {hi}" if hi != lo else "") + f" words, not {len(args)}")
            if any(len(a) > MAX_ARG for a in args):
                raise ValueError(f"a word over {MAX_ARG} characters")
            if verb == "goto":
                args = [target(args[0], root, any_url)]
            if verb == "wait" and not (re.fullmatch(r"[0-9]{1,5}", args[0]) and int(args[0]) <= MAX_WAIT_MS):
                raise ValueError(f"wait takes 0 to {MAX_WAIT_MS} ms, not {args[0]!r}")
        except ValueError as e:
            raise ValueError(f"line {no}: {e}") from None
        if len(steps) == MAX_STEPS:
            raise ValueError(f"over {MAX_STEPS} steps")
        steps.append({"n": len(steps) + 1, "line": no, "verb": verb, "args": args})
    if not steps:
        raise ValueError("no steps")
    return steps


def _pause(b, seconds):
    """Sleep, answering the page's held requests meanwhile."""
    if seconds > 0:
        b.wait(NEVER, seconds)


def _act(b, op, sel, text, end):
    """Run ACT until it holds or `end`: None, or why not. A navigation under way (no context yet) is retried."""
    expr = f"({ACT})(...{json.dumps([op, sel, text])})"  # JSON is a JS literal: data, never code
    while True:
        try:
            res = b.call("Runtime.evaluate", b.sid, expression=expr, returnByValue=True)
            if "exceptionDetails" in res:
                raise RuntimeError(str(res["exceptionDetails"].get("text", "the page threw")))
            got = res["result"].get("value") or {}
        except RuntimeError as e:
            got = {"error": str(e)}
        if got.get("bad"):
            return f"{sel} is not a valid selector: {got['bad']}"
        if got.get("ok"):
            return None
        if time.monotonic() + POLL_S >= end:
            break
        _pause(b, POLL_S)
    if got.get("missing"):
        return f"no element matches {sel}"
    if got.get("hidden"):
        return f"{sel} is there but not shown"
    if got.get("unfocusable"):
        return f"{sel} can't take focus"
    if "text" in got:
        return f"{sel} shows {json.dumps(got['text'], ensure_ascii=False)}, not {json.dumps(text, ensure_ascii=False)}"
    return f"{sel}: {got.get('error', 'no answer')}"


def step(b, s, timeout, end):
    """One step: None, or why it failed."""
    verb, args = s["verb"], s["args"]
    if verb == "wait":  # its own cap (MAX_WAIT_MS), not --timeout's
        _pause(b, min(int(args[0]) / 1000, end - time.monotonic()))
        return None
    end = min(end, time.monotonic() + timeout)
    if verb == "goto":
        b.events.clear()
        nav = b.call("Page.navigate", b.sid, url=args[0])
        if nav.get("errorText"):
            return f"did not load: {nav['errorText']}"
        b.wait("Page.loadEventFired", max(0.0, min(fmshot.LOAD_S, end - time.monotonic())))
        return None  # still loading: the next element step waits for what it needs
    why = _act(b, verb, args[0], args[1] if len(args) > 1 else None, end)
    if verb == "type" and why is None:
        b.call("Input.insertText", b.sid, text=args[1])
    if verb == "click" and why is None:  # a navigation it starts is asked for just after: held to the rule here
        _pause(b, CLICK_S)
    return why


def guard(b, root, any_url):
    """Hold every request the page makes to the goto rule: the state the steps read ({doc, other})."""
    seen = {"doc": None, "other": []}

    def paused(p):
        url = p["request"]["url"]
        if allowed(url, root, any_url):
            return b.send("Fetch.continueRequest", b.sid, requestId=p["requestId"])
        b.send("Fetch.failRequest", b.sid, requestId=p["requestId"], errorReason="BlockedByClient")
        if p.get("resourceType") == "Document":
            seen["doc"] = seen["doc"] or url
        elif len(seen["other"]) < MAX_NOTES:
            seen["other"].append(url)
        return None
    b.on["Fetch.requestPaused"] = paused
    b.call("Fetch.enable", b.sid, patterns=[{"urlPattern": "*", "requestStage": "Request"}])
    return seen


def run(b, steps, timeout, seen):
    """(done, failed): each step run in turn until one fails or TOTAL_S has passed."""
    done, end = [], time.monotonic() + TOTAL_S
    for s in steps:
        seen["doc"], seen["other"] = None, []
        try:
            why = step(b, s, timeout, end) if time.monotonic() < end else f"the journey ran past {TOTAL_S} s"
        except (OSError, RuntimeError, EOFError, ValueError) as e:  # TimeoutError is an OSError: the browser hung
            why = f"the browser failed: {e}"
        except (KeyError, TypeError, AttributeError) as e:  # an answer without the fields DevTools always sends
            why = f"the browser answered oddly: {type(e).__name__} {e}"
        if seen["doc"]:
            why = f"the page went outside the allowed pages, to {seen['doc']} (blocked)"
        done.append(dict(s, ok=why is None, error=why, blocked=list(seen["other"])))
        if why:
            return done, s["n"]
    return done, None


def _show(s):
    return fmshot.safe(" ".join([s["verb"]] + [a if len(a) <= 80 else a[:77] + "..." for a in s["args"]]))


def cmd_flow(args):
    import fmcli
    name = fmshot.safe(args.file)
    if not 0 < args.timeout <= MAX_STEP_S:
        raise fmcli.UsageError(f"fm flow: --timeout is above 0 and at most {MAX_STEP_S} s")
    if not os.path.isfile(args.file):  # a folder, a FIFO (it would block) or nothing
        raise fmcli.UsageError(f"fm flow: {name} isn't a file")
    root = os.path.dirname(os.path.abspath(args.file))
    try:
        with open(args.file, encoding="utf-8") as f:
            steps = parse(f.read(MAX_BYTES + 1), root, args.any_url)
    except (OSError, ValueError) as e:  # UnicodeDecodeError is a ValueError
        raise fmcli.UsageError(f"fm flow: {name}: {fmshot.safe(e)}") from None
    path, note = fmshot.find_browser("fm flow")
    if not path:
        fmcli.out(args, {"ok": False, "skipped": note}, f"fm flow: not run, not a pass: {note}.")
        sys.exit(2)
    with fmshot.killable():
        try:
            b = fmshot.Browser(path, fmshot.SIZE)
        except (OSError, RuntimeError, EOFError, ValueError) as e:
            why = f"the browser ({fmshot.safe(path)}) did not start: {fmshot.safe(e)}"
            fmcli.out(args, {"ok": False, "browser": path, "skipped": why}, f"fm flow: not run, not a pass: {why}")
            sys.exit(2)
        try:
            try:
                seen = guard(b, root, args.any_url)
            except (OSError, RuntimeError, EOFError, ValueError) as e:
                why = f"the browser ({fmshot.safe(path)}) would not hold requests to the goto rule: {fmshot.safe(e)}"
                fmcli.out(args, {"ok": False, "browser": path, "skipped": why}, f"fm flow: not run, not a pass: {why}")
                sys.exit(2)
            done, failed = run(b, steps, args.timeout, seen)
        finally:
            b.close()
    lines = ([f"note: {note}"] if note else []) + [f"fm flow: {name} ({len(steps)} steps) in {fmshot.safe(path)}"]
    for s in done:
        lines.append(f"  ✓ {s['n']} {_show(s)}" if s["ok"] else
                     f"✗ step {s['n']} (line {s['line']}) {_show(s)}: {fmshot.safe(s['error'])}")
        lines += [f"    blocked {fmshot.safe(u)}: outside the goto rule" for u in s["blocked"]]
    left = len(steps) - failed if failed else 0
    lines += [f"  {left} step{'s' if left != 1 else ''} not run"] if left else []
    fmcli.out(args, {"file": args.file, "browser": path, "ok": not failed, "failed": failed, "steps": done},
              "\n".join(lines))
    if failed:
        sys.exit(1)
    return None
