"""fm flow FILE (T-1639): a user journey run in the headless Chromium fm shot finds (fmshot.Browser; nothing is
installed), as a verify command. One step a line, words split like a shell's (quote a selector or text with spaces);
blank lines and lines starting with # are skipped:

    goto URL|FILE          file://, or http(s) on localhost, 127.0.0.1 or [::1] (--any-url: any http(s)); a bare
                           path is a file beside the flow
    click SELECTOR         the first match, once it is there and shown
    type SELECTOR TEXT     focus it, then insert TEXT as typed input after what is there
    expect SELECTOR [TEXT] it is there (and its text or value contains TEXT)
    wait MS                0 to 10000

Each element step waits up to --timeout seconds (default 10, at most 60) for its element; the whole journey at most
TOTAL_S. The flow is untrusted data: only these verbs, at most MAX_STEPS steps and MAX_ARG characters a word, and a
selector or text reaches the page only as a JSON argument to one fixed function (ACT), never as code. Exit 0: every
step held; 1: the step that failed is named (or the flow is malformed); 2: no browser, or it did not start — a
journey never passes without one."""
import json
import os
import pathlib
import re
import shlex
import signal
import sys
import time
import urllib.parse

import fmshot

MAX_BYTES, MAX_STEPS, MAX_ARG, MAX_WAIT_MS = 256 << 10, 200, 2000, 10000
MAX_STEP_S, TOTAL_S, POLL_S = 60, 600, 0.1  # --timeout's cap, the whole journey's, the element poll
VERBS = {"goto": (1, 1), "click": (1, 1), "type": (2, 2), "expect": (1, 2), "wait": (1, 1)}
LOCAL = {"localhost", "127.0.0.1", "::1"}
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


def target(word, base, any_url):
    """The URL a goto opens; ValueError for anything but a local page (or, with any_url, any http(s) page)."""
    if not re.match(r"(?i)[a-z][a-z0-9+.-]*:", word):  # a path: a file beside the flow
        path = os.path.join(base, word)
        if not os.path.isfile(path):
            raise ValueError(f"no such file: {word}")
        return pathlib.Path(os.path.abspath(path)).as_uri()
    try:
        u = urllib.parse.urlsplit(word)
        host = u.hostname
    except ValueError as e:
        raise ValueError(f"not a URL: {e}") from None
    scheme = u.scheme.lower()
    if scheme == "file" and host in (None, "localhost"):
        return word
    if scheme in ("http", "https") and host and (host in LOCAL or any_url):
        return word
    raise ValueError("goto opens file:// or http(s) on localhost, 127.0.0.1 or [::1]"
                     + ("" if any_url else " (--any-url: any http(s) page)") + f", not {word}")


def parse(text, base, any_url=False):
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
                args = [target(args[0], base, any_url)]
            if verb == "wait" and not (args[0].isdigit() and int(args[0]) <= MAX_WAIT_MS):
                raise ValueError(f"wait takes 0 to {MAX_WAIT_MS} ms, not {args[0]!r}")
        except ValueError as e:
            raise ValueError(f"line {no}: {e}") from None
        if len(steps) == MAX_STEPS:
            raise ValueError(f"over {MAX_STEPS} steps")
        steps.append({"n": len(steps) + 1, "line": no, "verb": verb, "args": args})
    if not steps:
        raise ValueError("no steps")
    return steps


def _act(b, op, sel, text, end):
    """Run ACT until it holds or `end`: None, or why not. A navigation under way (no context yet) is retried."""
    expr = f"({ACT})(...{json.dumps([op, sel, text])})"  # JSON is a JS literal: data, never code
    last = None
    while True:
        try:
            res = b.call("Runtime.evaluate", b.sid, expression=expr, returnByValue=True)
            if "exceptionDetails" in res:
                raise RuntimeError(res["exceptionDetails"].get("text", "the page threw"))
            got = (res.get("result") or {}).get("value") or {}
        except RuntimeError as e:
            got = {"error": str(e)}
        if got.get("bad"):
            return f"{sel} is not a valid selector: {got['bad']}"
        if got.get("ok"):
            return None
        last = got
        if time.monotonic() + POLL_S >= end:
            break
        time.sleep(POLL_S)
    if last.get("missing"):
        return f"no element matches {sel}"
    if last.get("hidden"):
        return f"{sel} is there but not shown"
    if last.get("unfocusable"):
        return f"{sel} can't take focus"
    if "text" in last:
        return f"{sel} shows {json.dumps(last['text'], ensure_ascii=False)}, not {json.dumps(text, ensure_ascii=False)}"
    return f"{sel}: {last.get('error', 'no answer')}"


def step(b, s, timeout, end):
    """One step: None, or why it failed."""
    verb, args = s["verb"], s["args"]
    end = min(end, time.monotonic() + timeout)
    if verb == "goto":
        b.events.clear()
        nav = b.call("Page.navigate", b.sid, url=args[0])
        if nav.get("errorText"):
            return f"did not load: {nav['errorText']}"
        b.wait("Page.loadEventFired", max(0.0, min(fmshot.LOAD_S, end - time.monotonic())))
        return None  # still loading: the next element step waits for what it needs
    if verb == "wait":
        time.sleep(max(0.0, min(int(args[0]) / 1000, end - time.monotonic())))
        return None
    why = _act(b, verb, args[0], args[1] if len(args) > 1 else None, end)
    if verb == "type" and why is None:
        b.call("Input.insertText", b.sid, text=args[1])
    return why


def run(b, steps, timeout):
    """(done, failed): each step run in turn until one fails or TOTAL_S has passed."""
    done, end = [], time.monotonic() + TOTAL_S
    for s in steps:
        try:
            why = step(b, s, timeout, end) if time.monotonic() < end else f"the journey ran past {TOTAL_S} s"
        except (OSError, RuntimeError, EOFError, ValueError) as e:  # TimeoutError is an OSError: the browser hung
            why = f"the browser failed: {e}"
        done.append(dict(s, ok=why is None, error=why))
        if why:
            return done, s["n"]
    return done, None


def _show(s):
    return fmshot._safe(" ".join([s["verb"]] + [a if len(a) <= 80 else a[:77] + "..." for a in s["args"]]))


def cmd_flow(args):
    import fmcli
    name = fmshot._safe(args.file)
    if not 0 < args.timeout <= MAX_STEP_S:
        raise fmcli.UsageError(f"fm flow: --timeout is above 0 and at most {MAX_STEP_S} s")
    if not os.path.isfile(args.file):  # a folder, a FIFO (it would block) or nothing
        raise fmcli.UsageError(f"fm flow: {name} isn't a file")
    try:
        with open(args.file, encoding="utf-8") as f:
            steps = parse(f.read(MAX_BYTES + 1), os.path.dirname(os.path.abspath(args.file)), args.any_url)
    except (OSError, ValueError) as e:  # UnicodeDecodeError is a ValueError
        raise fmcli.UsageError(f"fm flow: {name}: {fmshot._safe(e)}") from None
    env = os.environ.get("FOREMAN_CHROME")
    bad = f"FOREMAN_CHROME={fmshot._safe(env)!r} isn't an executable file" if env and not fmshot._usable(env) else None
    path = fmshot.chrome()
    if not path:
        why = (bad + "; " if bad else "") + fmshot.NONE.replace("fm shot", "fm flow")
        fmcli.out(args, {"ok": False, "skipped": why}, f"fm flow: not run, not a pass: {why}.")
        sys.exit(2)

    def stop(signum, frame):  # killed: unwind, so the browser's group dies and its profile goes
        raise SystemExit(128 + signum)
    old = signal.signal(signal.SIGTERM, stop)
    try:
        try:
            b = fmshot.Browser(path, fmshot.SIZE)
        except (OSError, RuntimeError, EOFError, ValueError) as e:
            why = f"the browser ({fmshot._safe(path)}) did not start: {fmshot._safe(e)}"
            fmcli.out(args, {"ok": False, "browser": path, "skipped": why}, f"fm flow: not run, not a pass: {why}")
            sys.exit(2)
        try:
            done, failed = run(b, steps, args.timeout)
        finally:
            b.close()
    finally:
        signal.signal(signal.SIGTERM, old)
    lines = [f"fm flow: {name} ({len(steps)} steps) in {fmshot._safe(path)}"]
    for s in done:
        lines.append(f"  ✓ {s['n']} {_show(s)}" if s["ok"] else
                     f"✗ step {s['n']} (line {s['line']}) {_show(s)}: {fmshot._safe(s['error'])}")
    if failed:
        left = len(steps) - failed
        lines += [f"  {left} step{'s' if left != 1 else ''} not run"] if left else []
    fmcli.out(args, {"file": args.file, "browser": path, "ok": not failed, "failed": failed, "steps": done},
              "\n".join(lines))
    if failed:
        sys.exit(1)
    return None
