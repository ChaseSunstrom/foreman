"""fm stories CHART (T-1640): a component's state matrix, one page with a cell per state a state chart lists, each
state shot in the headless Chromium fm shot finds (fmshot.Browser; nothing is installed). The chart is JSON:

    {"component": "Sign-up form",               optional: the page's title (default: the chart's file name)
     "page": "form.html",                        optional: where every state starts (a file beside the chart, or
                                                 http(s) on localhost, 127.0.0.1 or [::1]: fm flow's goto rule)
     "states": [{"name": "default"},             1 to MAX_STATES, names unique (any case)
                {"name": "hover", "steps": ["goto form.html?state=hover"]},
                {"name": "error", "steps": ["type \\"#email\\" bad", "click \\"#go\\""]}]}

Each state's steps are fm flow steps (goto, click, type, expect, wait), at most MAX_STEPS; one that doesn't start with a
goto starts with `goto PAGE`. The chart is untrusted data: no other keys, capped sizes, and every step held to fm
flow's rules (its parser, its URL rule and its request blocking). The page (default <project state>/stories/
<chart>.html, or --out: a .html file that isn't a link, replaced only when fm stories wrote it) is one file with each
shot inline as a data: PNG (MAX_TOTAL_PNG in all) and a CSP that loads nothing else. States run in one browser in
turn, each from about:blank; cookies and storage carry over (ponytail: a fresh profile per state if a chart ever needs
it). Exit 0: the page is written and every state's steps held; 1: a malformed chart, or a state that failed (its cell
names the step); 2: no browser, or it did not start: the page lists the states and how to reach each, says why there
are no shots, and the run is never a pass (as fm flow's)."""
import base64
import html
import json
import os
import re
import shlex
import sys
import time

import fmcore as c
import fmflow
import fmshot

MAX_BYTES, MAX_STATES, MAX_STEPS, MAX_NAME, MAX_TITLE = 64 << 10, 20, 20, 60, 120
MAX_PNG, MAX_TOTAL_PNG = 2 << 20, 12 << 20  # one shot inline (a viewport is well under it); all, about 16 MB as base64
STEP_S, TOTAL_S = 5, 300  # each element step's wait; the whole run's, held inside each state's steps too
KEYS, STATE_KEYS = {"component", "page", "states"}, {"name", "steps"}
MARK = "<!-- fm stories (T-1640)"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _text(v, what, cap):
    if (not isinstance(v, str) or not v.strip() or len(v) > cap or re.search(r"[\x00-\x1f\x7f-\x9f]", v)
            or len(v.splitlines()) != 1):  # U+2028 and U+2029 end a line too: no smuggled steps
        raise ValueError(f"{what} is a line of text, 1 to {cap} characters with no control characters")
    return v


def parse(text, root, default_title):
    """{title, states: [{name, lines, steps}]}; ValueError naming what is wrong."""
    if len(text) > MAX_BYTES:
        raise ValueError(f"over {MAX_BYTES >> 10} KB")
    try:
        chart = json.loads(text)
    except ValueError as e:
        raise ValueError(f"not JSON: {e}") from None
    if not isinstance(chart, dict) or set(chart) - KEYS:
        raise ValueError(f"a chart is a JSON object with only {', '.join(sorted(KEYS))}")
    title = _text(chart.get("component", default_title), "component", MAX_TITLE)
    page = _text(chart["page"], "page", fmflow.MAX_ARG) if "page" in chart else None
    states = chart.get("states")
    if not isinstance(states, list) or not 1 <= len(states) <= MAX_STATES:
        raise ValueError(f"states is a list of 1 to {MAX_STATES} states")
    out, seen = [], set()
    for i, s in enumerate(states, 1):
        try:
            if not isinstance(s, dict) or set(s) - STATE_KEYS:
                raise ValueError(f"a state is an object with only {', '.join(sorted(STATE_KEYS))}")
            name = _text(s.get("name"), "name", MAX_NAME)
            if name.casefold() in seen:
                raise ValueError(f"{name!r} is named twice")
            seen.add(name.casefold())
            lines = s.get("steps", [])
            if not isinstance(lines, list) or len(lines) > MAX_STEPS:
                raise ValueError(f"steps is a list of at most {MAX_STEPS} fm flow steps")
            lines = [_text(x, "a step", fmflow.MAX_ARG * 2) for x in lines]  # one line each: no smuggled steps
            if not (lines and lines[0].split(None, 1)[0] == "goto"):
                if page is None:
                    raise ValueError("its steps don't start with a goto and the chart names no page")
                lines = [f"goto {shlex.quote(page)}"] + lines
            steps = fmflow.parse("\n".join(lines), root)
        except ValueError as e:
            raise ValueError(f"state {i}: {e}") from None
        out.append({"name": name, "lines": lines, "steps": steps})
    return {"title": title, "states": out}


def shoot(b, states, root):
    """Each state reached and shot, in place: {ok, error, png, why}."""
    seen, end = fmflow.guard(b, root, False), time.monotonic() + TOTAL_S
    b.call("Page.addScriptToEvaluateOnNewDocument", b.sid, source=fmshot.FREEZE)  # shots that don't move
    gone = None
    for s in states:
        s.update(ok=False, error=None, png=None)
        if gone or time.monotonic() >= end:
            s["error"] = gone or f"not shot: the run passed {TOTAL_S} s"
            continue
        try:
            b.call("Page.navigate", b.sid, url="about:blank")  # a fresh page: a goto to a #fragment doesn't reload
            done, failed = fmflow.run(b, s["steps"], STEP_S, seen, end)
            s["ok"] = failed is None
            if failed:
                s["error"] = f"step {failed} ({fmflow._show(done[-1])}): {done[-1]['error']}"
            fmflow._pause(b, fmshot.SETTLE_S)
            png = b.png()
            if not png.startswith(PNG_MAGIC) or len(png) > MAX_PNG:
                s["why"] = f"the shot is not a PNG under {MAX_PNG >> 20} MB"
                s["ok"] = False
            else:
                s["png"] = png
        except (OSError, RuntimeError, EOFError, ValueError, KeyError) as e:  # KeyError: an answer without data
            s.update(ok=False, why=f"not shot: {e}")
            if isinstance(e, (EOFError, TimeoutError)):  # gone or hung: the rest would wait too
                gone = "not shot: the browser stopped answering"


CSS = """body { font: 15px/1.4 system-ui, sans-serif; margin: 24px; color: #1a1a1a; background: #f6f6f4 }
h1 { font-size: 20px; margin: 0 0 4px } .note { color: #555; margin: 0 0 20px }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px }
.cell { margin: 0; background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 12px }
.cell img { width: 100%; height: auto; border: 1px solid #eee; display: block }
figcaption { font-weight: 600; margin-bottom: 8px } .bad { color: #a00 } .why { color: #555 }
ol { margin: 8px 0 0; padding-left: 20px; font: 12px/1.5 ui-monospace, monospace; color: #444 }"""


def page_html(chart, note):
    """The page; a shot past MAX_TOTAL_PNG in all is dropped from its state, with why."""
    e, cells, total = html.escape, [], 0
    for s in chart["states"]:
        if s.get("png") and total + len(s["png"]) > MAX_TOTAL_PNG:
            s.update(png=None, why=f"not inlined: the shots in all passed {MAX_TOTAL_PNG >> 20} MB")
        total += len(s.get("png") or b"")
        shot = (f'<img src="data:image/png;base64,{base64.b64encode(s["png"]).decode()}" alt="{e(s["name"])} state">'
                if s.get("png") else "")
        msgs = [f'<p class="bad">{e(s["error"])}</p>' if s.get("error") else "",
                f'<p class="why">{e(s["why"])}</p>' if s.get("why") else ""]
        steps = "".join(f"<li>{e(x)}</li>" for x in s["lines"])
        cells.append(f'<figure class="cell" data-state="{e(s["name"])}"><figcaption>{e(s["name"])}</figcaption>'
                     f'{shot}{"".join(msgs)}<ol>{steps}</ol></figure>')
    return (f'<!doctype html>\n{MARK}: one cell per state; loads nothing from another host -->\n<html lang="en"><head>'
            '<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
            'img-src data:; style-src \'unsafe-inline\'">'
            f'<meta name="viewport" content="width=device-width"><title>{e(chart["title"])}: states</title>'
            f'<style>{CSS}</style></head><body><h1>{e(chart["title"])}</h1><p class="note">{e(note)}</p>'
            f'<div class="grid">{"".join(cells)}</div></body></html>\n')


def cmd_stories(args):
    import fmcli
    import fmpage
    name = fmshot.safe(args.chart)
    if not os.path.isfile(args.chart):  # a folder, a FIFO (it would block) or nothing
        raise fmcli.UsageError(f"fm stories: {name} isn't a file")
    root = os.path.dirname(os.path.abspath(args.chart))
    stem = re.sub(r"[^a-z0-9_-]+", "-", os.path.basename(args.chart).lower().rsplit(".", 1)[0]).strip("-") or "chart"
    try:
        with open(args.chart, encoding="utf-8") as f:
            chart = parse(f.read(MAX_BYTES + 1), root, stem[:MAX_TITLE])
    except (OSError, ValueError) as e:  # UnicodeDecodeError is a ValueError
        raise fmcli.UsageError(f"fm stories: {name}: {fmshot.safe(e)}") from None
    default = None if args.out else os.path.join(fmcli.resolve(args).dir, "stories", f"{stem[:60]}.html")
    path = fmpage._out(args, default, MARK)
    states = chart["states"]
    browser, note = fmshot.find_browser("fm stories")
    size, scale = fmshot.view(args)
    if browser:
        with fmshot.killable():
            try:
                b = fmshot.Browser(browser, size, scale, getattr(args, "reduced_motion", False))
            except (OSError, RuntimeError, EOFError, ValueError) as e:
                browser, note = None, f"the browser ({fmshot.safe(browser)}) did not start: {fmshot.safe(e)}"
            else:
                try:
                    shoot(b, states, root)
                except (OSError, RuntimeError, EOFError, ValueError) as e:  # before any state: not run at all
                    browser, note = None, f"the browser ({fmshot.safe(browser)}) failed: {fmshot.safe(e)}"
                finally:
                    b.close()
    if not browser:  # the listing still helps; a run with no step checked is never a pass (fm flow's exit 2)
        for s in states:
            s.update(ok=False, error=None, png=None, why="Not shot (see above).")
        head = f"No shots: {note}. Each state lists the fm flow steps that reach it."
    else:
        head = f"States shot in {fmshot.safe(browser)}, {size[0]}x{size[1]}" + (
            f"; note: {note}" if note else "")
    c.write_atomic(path, page_html(chart, head))
    shot, failed = sum(1 for s in states if s.get("png")), [s for s in states if not s.get("ok")]
    data = {"path": path, "browser": browser, "note": note, "ok": bool(browser) and not failed,
            "states": [{"name": s["name"], "shot": bool(s.get("png")), "ok": bool(s.get("ok")),
                        "error": s.get("error"), "why": s.get("why")} for s in states]}
    lines = [f"fm stories: wrote {path}: {len(states)} states of {fmshot.safe(chart['title'])}, {shot} shot"]
    if not browser:
        fmcli.out(args, dict(data, skipped=note), "\n".join(lines + [f"fm stories: not run, not a pass: {note}."]))
        sys.exit(2)
    for s in states:
        why = s.get("error") or s.get("why")
        lines.append(f"  ✓ {fmshot.safe(s['name'])}" + (f" ({fmshot.safe(why)})" if why else "") if s["ok"] else
                     f"  ✗ {fmshot.safe(s['name'])}: {fmshot.safe(why)}")
    fmcli.out(args, data, "\n".join(lines))
    if failed:
        sys.exit(1)
    return None
