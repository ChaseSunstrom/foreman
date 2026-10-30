#!/usr/bin/env python3
"""Build the Pages site (T-1220): python3 site/build.py [OUT]  (default: _site beside site/)

Copies site/ (the landing page, style.css, assets) and the demo files, then renders one page per capability from
site/pages.py with charts drawn from site/data/stats.json (made by site/stats.py on a machine with Foreman's state).
Charts are inline SVG that follow the page's light and dark tokens; every mark has a hover title and every chart a
data table. Stdlib only, so the Pages workflow runs it with the runner's Python. T-1411: the pages load nothing from
another host (fonts are the reader's own, named first in style.css with system fallbacks); the build fails on any
page, stylesheet, script or picture that would."""
import html
import html.parser
import json
import os
import re
import shlex
import hashlib
import shutil
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
with open(os.path.join(HERE, "assets", "foreman.svg"), "rb") as _f:  # T-2060: browsers keep a favicon by its URL
    ICON = "assets/foreman.svg?v=" + hashlib.sha256(_f.read()).hexdigest()[:8]
SOURCE_ONLY = {"build.py", "stats.py", "pages.py", "bench_safety.py", "share.html", "__pycache__"}
TYPES = ["FEATURE", "FIX", "CLEAN", "PERFORMANCE", "SECURITY", "RESEARCH"]
esc = html.escape


def fmt(n):
    return f"{n:,.0f}" if (isinstance(n, (int, float)) and abs(n) >= 100) or isinstance(n, int) else f"{n:g}"


def safe_out(out):
    """Site review: the output folder is wiped first, so never the repo, its site/ source, a folder holding either,
    the home folder or the root."""
    out = os.path.realpath(out)
    keep = [os.path.realpath(x) for x in (ROOT, HERE, os.path.expanduser("~"))]
    return out != os.path.sep and not any(out == k or k.startswith(out.rstrip(os.sep) + os.sep) for k in keep)


OWN_HOSTS = {"chasesunstrom.github.io"}  # the site itself
# T-1785: XML namespace URIs in script or CSS text are names, never fetched; in a src or href they still count
NAMESPACES = {"http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink", "http://www.w3.org/1999/xhtml"}
ABSOLUTE = re.compile(r"""(?i)\bhttps?:[/\\]{2}[^\s'"`)<>]+""")  # any http(s) URL in a stylesheet or script
CSS_SHORT = re.compile(r"""(?i)(?:url\(\s*|@import\s+)['"]?([/\\]{2}[^\s'")]+)""")  # url(//host/x), @import "//host"


def _outside(url):
    """The URL if it names a host other than the site's own (as a browser reads it: tabs and newlines dropped, \\ as /)."""
    try:
        u = urllib.parse.urlsplit(re.sub(r"[\t\n\r]", "", url).strip().replace("\\", "/"))
        return url if u.netloc and (u.hostname or "") not in OWN_HOSTS else None
    except ValueError:
        return url


def _text_urls(text):
    text = re.sub(r"(?s)/\*.*?\*/", "", text)
    return [u for u in ABSOLUTE.findall(text) if u not in NAMESPACES] + CSS_SHORT.findall(text)


class _Loads(html.parser.HTMLParser):
    """Every URL a page or SVG makes the browser fetch: src, srcset, poster, data, href off anything but a link to
    follow (<a>, <area>), CSS in <style> and style="", and any http(s) URL in a <script>."""

    def __init__(self):
        super().__init__()
        self.urls, self.inside = [], None

    def handle_starttag(self, tag, attrs):
        self.handle_startendtag(tag, attrs)
        self.inside = tag if tag in ("style", "script") else None

    def handle_startendtag(self, tag, attrs):
        for k, v in attrs:
            if v is None:
                continue
            if k == "srcset":
                self.urls += [c.split()[0] for c in v.split(",") if c.split()]
            elif k == "ping":  # <a ping> posts to each URL on a click
                self.urls += v.split()
            elif k in ("src", "poster", "data", "background") or k in ("href", "xlink:href") and tag not in ("a", "area"):
                self.urls.append(v)
            elif k == "style":
                self.urls += _text_urls(v)

    def handle_endtag(self, tag):
        self.inside = None

    def handle_data(self, data):
        if self.inside:
            self.urls += _text_urls(data)


def outside_loads(text, ext):
    """T-1411: the URLs on another host that this .html, .svg, .css or .js file makes the browser fetch."""
    if ext in (".html", ".svg"):
        p = _Loads()
        p.feed(text)
        p.close()
        urls = p.urls
    else:
        urls = _text_urls(text)
    return [u for u in urls if _outside(u)]


def outside_hosts(out):
    """Each built file's outside loads, as "path: url" lines."""
    found = []
    for d, dirs, files in os.walk(out):
        dirs.sort()
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext in (".html", ".svg", ".css", ".js"):
                with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
                    rel = os.path.relpath(os.path.join(d, f), out)
                    found += [f"{rel}: {u}" for u in outside_loads(fh.read(), ext)]
    return found


def table(head, rows):
    th = "".join(f"<th>{esc(str(h))}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{esc(fmt(c) if isinstance(c, (int, float)) else str(c))}</td>" for c in r)
                 + "</tr>" for r in rows)
    return f'<details class="data"><summary>Show the numbers</summary><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></details>'


def legend(keys):
    return '<ul class="legend">' + "".join(f'<li><i class="sw s{i + 1}"></i>{esc(k.title() if k.isupper() else k)}</li>'
                                           for i, k in enumerate(keys)) + "</ul>"


def figure(title, note, svg, data):
    return (f'<figure class="chart"><figcaption><b>{esc(title)}</b>{f"<span>{esc(note)}</span>" if note else ""}'
            f'</figcaption>{svg}{data}</figure>')


def hbars(title, note, items, unit="", series=1, budget=None):
    """Horizontal bars, sorted by the caller; value at each tip. budget: {label: value} draws a tick per row."""
    items = list(items)
    top = max([v for _, v in items] + list((budget or {}).values()) + [1])
    row, label_w, w = 30, 170, 640
    plot = w - label_w - 70
    h = row * len(items) + 8
    out = [f'<svg class="viz grow-x" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">']  # T-1615
    for i, (k, v) in enumerate(items):
        y = 4 + i * row
        bw = max(2, plot * v / top)
        out.append(f'<text class="lab" x="{label_w - 10}" y="{y + 17}" text-anchor="end">{esc(str(k))}</text>')
        out.append(f'<rect class="m s{series}" x="{label_w}" y="{y + 5}" width="{bw:.1f}" height="18" rx="4">'
                   f'<title>{esc(str(k))}: {fmt(v)}{unit}</title></rect>')
        bx = label_w + plot * budget[k] / top if budget and k in budget else 0
        tip = max(bw, bx - label_w + 4) if bx and bx - label_w - bw < 60 else bw  # past a budget tick it would cross
        out.append(f'<text class="val" x="{label_w + tip + 8:.1f}" y="{y + 18}">{fmt(v)}{esc(unit)}</text>')
        if bx:
            out.append(f'<line class="budget" x1="{bx:.1f}" x2="{bx:.1f}" y1="{y + 1}" y2="{y + 27}">'
                       f'<title>budget {fmt(budget[k])}{unit}</title></line>')
    out.append("</svg>")
    head = ["", "value"] + (["budget"] if budget else [])
    rows = [[k, v] + ([budget.get(k, "")] if budget else []) for k, v in items]
    return figure(title, note, "".join(out), table(head, rows))


def pairs(title, note, rows, names=("With Foreman", "Claude Code"), unit=""):
    """Two horizontal bars per row (series 1 and 2), each with its value at the tip: rows are (label, a, b)."""
    rows = list(rows)
    top = max([max(a, b) for _, a, b in rows] + [1e-9])
    band, label_w, w = 72, 0, 640  # T-1239: each label above its bars, full width, so a long task name stays inside
    plot = w - label_w - 80
    h = band * len(rows) + 6
    out = [f'<svg class="viz pairs grow-x" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">']
    for i, (k, a, b) in enumerate(rows):
        y = 4 + i * band
        out.append(f'<text class="lab" x="0" y="{y + 14}">{esc(str(k))}</text>')
        for j, (v, name) in enumerate(((a, names[0]), (b, names[1]))):
            yy = y + 20 + j * 22
            bw = max(2, plot * v / top)
            out.append(f'<rect class="m s{j + 1}" x="{label_w}" y="{yy}" width="{bw:.1f}" height="18" rx="4">'
                       f'<title>{esc(str(k))} · {esc(name)}: {fmt(v)}{unit}</title></rect>'
                       f'<text class="val" x="{label_w + bw + 8:.1f}" y="{yy + 13}">{fmt(v)}{esc(unit)}</text>')
    out.append("</svg>")
    return figure(title, note, legend(list(names)) + "".join(out),
                  table(["", names[0], names[1]], [[k, a, b] for k, a, b in rows]))


def verdicts(rows, names=("Claude Code alone", "With Foreman")):
    """A table of commands and what each setup does with them; the stamp carries the outcome, never colour alone."""
    stamp = {"deny": '<span class="stamp stop">Stopped</span>', "saved": '<span class="stamp sig">Saved first</span>',
             "allow": '<span class="stamp warn">Runs</span>', "run": '<span class="stamp warn">Runs</span>'}
    body = "".join(f"<tr><td><code>{esc(r['cmd'])}</code><br><small>{esc(r.get('what', ''))}</small></td>"
                   f"<td>{stamp['run']}</td><td>{stamp.get(r['decision'], esc(r['decision']))}</td></tr>" for r in rows)
    return (f'<div class="verdicts"><table><thead><tr><th>Command</th><th>{esc(names[0])}</th><th>{esc(names[1])}</th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>')


def columns(title, note, rows, keys, label_key="day", short=lambda s: s[5:]):
    """Columns over time, stacked when there is more than one key; a 2px surface gap between segments."""
    w, h, left, bottom, top_pad = 640, 240, 44, 26, 12
    totals = [sum(r.get(k, 0) for k in keys) for r in rows]
    top = max(totals + [1])
    step = 10 ** max(0, len(str(int(top))) - 1)
    top_tick = -(-top // step) * step
    plot_w, plot_h = w - left - 8, h - bottom - top_pad
    slot = plot_w / max(1, len(rows))
    bw = min(46, slot * 0.62)
    out = [f'<svg class="viz grow-y" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">']  # T-1615
    for t in range(0, int(top_tick) + 1, int(max(1, top_tick // 4))):
        y = top_pad + plot_h - plot_h * t / top_tick
        out.append(f'<line class="grid" x1="{left}" x2="{w - 8}" y1="{y:.1f}" y2="{y:.1f}"/>'
                   f'<text class="tick" x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{fmt(t)}</text>')
    for i, r in enumerate(rows):
        x = left + i * slot + (slot - bw) / 2
        y = top_pad + plot_h
        for j, k in enumerate(keys):
            v = r.get(k, 0)
            if not v:
                continue
            hh = plot_h * v / top_tick
            y -= hh
            gap = 2 if j else 0
            out.append(f'<rect class="m s{j + 1}" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(1, hh - gap):.1f}"'
                       f' rx="{3 if j == len(keys) - 1 or len(keys) == 1 else 1}">'
                       f'<title>{esc(r[label_key])} · {esc(k.title() if k.isupper() else k)}: {fmt(v)}</title></rect>')
        if len(rows) <= 16 or i % 2 == 0:
            out.append(f'<text class="tick" x="{x + bw / 2:.1f}" y="{h - 8}" text-anchor="middle">{esc(short(r[label_key]))}</text>')
    out.append(f'<line class="axis" x1="{left}" x2="{w - 8}" y1="{top_pad + plot_h}" y2="{top_pad + plot_h}"/></svg>')
    data = table([label_key] + keys + (["total"] if len(keys) > 1 else []),
                 [[r[label_key]] + [r.get(k, 0) for k in keys] + ([t] if len(keys) > 1 else []) for r, t in zip(rows, totals)])
    return figure(title, note, (legend(keys) if len(keys) > 1 else "") + "".join(out), data)


def line(title, note, rows, key, label_key):
    """One series over time, 2px line, the last value labelled at its end."""
    if not rows:  # site review: no release commits yet raised IndexError
        return figure(title, note, "<p>No data yet.</p>", "")
    w, h, left, bottom, top_pad = 640, 220, 50, 26, 16
    vals = [r[key] for r in rows]
    lo, hi = 0, max(vals + [1])
    step = 10 ** max(0, len(str(int(hi))) - 1)
    hi = -(-hi // step) * step
    plot_w, plot_h = w - left - 70, h - bottom - top_pad
    xs = [left + (plot_w * i / max(1, len(rows) - 1)) for i in range(len(rows))]
    ys = [top_pad + plot_h - plot_h * (v - lo) / (hi - lo) for v in vals]
    out = [f'<svg class="viz draw" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">']  # T-1615
    for t in range(0, int(hi) + 1, int(max(1, hi // 4))):
        y = top_pad + plot_h - plot_h * t / hi
        out.append(f'<line class="grid" x1="{left}" x2="{left + plot_w}" y1="{y:.1f}" y2="{y:.1f}"/>'
                   f'<text class="tick" x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{fmt(t)}</text>')
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<polyline class="ln s1" points="{pts}" fill="none" pathLength="1"/>')  # T-1615: drawn as a fraction
    for x, y, r in zip(xs, ys, rows):
        out.append(f'<circle class="dot s1" cx="{x:.1f}" cy="{y:.1f}" r="4"><title>{esc(r[label_key])}: {fmt(r[key])}</title></circle>')
    out.append(f'<text class="val" x="{xs[-1] + 10:.1f}" y="{ys[-1] + 4:.1f}">{fmt(vals[-1])}</text>')
    for i in sorted({0, len(rows) // 2, len(rows) - 1}):  # two rows: each label once
        out.append(f'<text class="tick" x="{xs[i]:.1f}" y="{h - 8}" text-anchor="middle">{esc(rows[i][label_key])}</text>')
    out.append(f'<line class="axis" x1="{left}" x2="{left + plot_w}" y1="{top_pad + plot_h}" y2="{top_pad + plot_h}"/></svg>')
    return figure(title, note, "".join(out), table([label_key, key], [[r[label_key], r[key]] for r in rows]))


def tiles(pairs, cls=""):
    return f'<div class="tiles{" " + cls if cls else ""}">' + "".join(f'<div class="tile"><span>{esc(label)}</span>'
                                           f'<strong>{fmt(v) if isinstance(v, (int, float)) else esc(v)}</strong></div>'
                                           for label, v in pairs) + "</div>"


PROOF_MARK = "<!-- proof: build.py fills it from data/stats.json (T-1609) -->"
SHADER_MARK = "<!-- shaders: build.py fills it with four shader cards running live (T-2062) -->"
LANDING_SHADERS = ("shader-aurora-bands", "shader-soft-caustics", "shader-grain-gradient", "shader-halftone")
STATIONS = [("tasks_done", "tasks done"), ("evidence", "evidence runs"), ("proofs", "proofs"), ("commits", "commits")]


def proof(totals, asof=""):
    """T-1609, T-2040: the hero's proof ledger, the four totals from Foreman's own record as plain figures on hairlines
    (the diamond poster and its WebGL scene read as decoration, not data). Inline, so it is first paint."""
    items = "".join(f"<div><dt>{esc(label)}</dt><dd>{esc(fmt(totals.get(k) or 0))}</dd></div>" for k, label in STATIONS)
    return f'<div class="proof"><p>From Foreman\'s own record{", to " + esc(asof) if asof else ""}</p><dl>{items}</dl></div>'


def layout(title, desc, body, pages, here, depth=1):
    up = "../" * depth
    current = ' aria-current="page"'
    nav = "".join(f'<a href="{up}features/{p["slug"]}.html"{current if p["slug"] == here else ""}>{esc(p["nav"])}</a>'
                  for p in pages)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>try {{ var t = localStorage.getItem("fm-theme"); if (t) document.documentElement.setAttribute("data-theme", t); }} catch (e) {{}}</script>
<title>{esc(title)} · Foreman</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)} · Foreman">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://chasesunstrom.github.io/foreman/assets/share.png">
<link rel="icon" href="{up}{ICON}" type="image/svg+xml">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{up}index.html"><img src="{up}assets/foreman.svg" alt="" width="28" height="28">Foreman</a>
    <nav class="nav" aria-label="Main">
      <a class="hide-sm" href="{up}features/index.html">Features</a>
      <a href="{up}index.html#install">Install</a>
      <a href="https://github.com/ChaseSunstrom/foreman">GitHub</a>
      <button class="theme" type="button" aria-label="Switch between light and dark" title="Light or dark">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg>
      </button>
    </nav>
  </div>
</header>
<div class="wrap feature-shell">
  <nav class="side" aria-label="Features">{nav}</nav>
  <main class="feature">{body}</main>
</div>
<footer>
  <div class="wrap">
    <a class="brand" href="{up}index.html"><img src="{up}assets/foreman.svg" alt="" width="22" height="22">Foreman</a>
    <nav aria-label="Links">
      <a href="https://github.com/ChaseSunstrom/foreman">Source</a>
      <a href="https://github.com/ChaseSunstrom/foreman/blob/main/README.md">Read me</a>
      <a href="https://github.com/ChaseSunstrom/foreman/blob/main/CHANGELOG.md">Changelog</a>
    </nav>
    <p class="fine">A community plugin for Claude Code. Not made by or affiliated with Anthropic. Charts are drawn from Foreman's own record of building itself.</p>
  </div>
</footer>
<script src="{up}site.js"></script>
</body>
</html>
"""


# T-1320: real fm code runs, one per kind of request, kept as their event streams (fm code --json) in demo/examples/
EXAMPLES = [("fix", "Fix a bug"), ("feature", "Add a feature"), ("rename", "Rename across files"),
            ("docs", "Write docs"), ("question", "Ask about the code"), ("new-project", "Start from an empty folder"),
            ("javascript", "Another language")]


def load_example(path):
    """One run's events → what its card shows: the request, the plan, each check before and after, the files, the
    worker turns, tokens, time and how it ended."""
    with open(path, encoding="utf-8") as f:
        ev = [json.loads(line) for line in f if line.startswith("{")]
    first = lambda kind: next((e for e in ev if e.get("event") == kind), {})
    checks = {}
    for e in ev:
        if e.get("event") == "verify":
            checks.setdefault(e.get("criterion"), {})["before" if e.get("label") == "before" else "after"] = e.get("exit")
    stat = {}
    for e in ev:
        if e.get("event") == "changed":
            stat.update(e.get("stat") or {f: stat.get(f, [0, 0]) for f in e.get("files") or []})
    tokens = next((e.get("total_in", 0) + e.get("total_out", 0) for e in reversed(ev) if e.get("event") == "tokens"), 0)
    ts = [e["ts"] for e in ev if isinstance(e.get("ts"), (int, float))]
    end = next((e for e in reversed(ev) if e.get("event") in ("closed", "blocked", "error", "answer")), {})
    return {"request": first("start").get("request", ""), "worker": first("start").get("worker"),
            "plan": first("plan").get("plan") or {}, "checks": checks, "stat": stat, "tokens": tokens,
            "turns": sum(e.get("event") == "worker" for e in ev), "seconds": round(ts[-1] - ts[0]) if ts else None,
            "end": end.get("event"), "end_text": end.get("text", ""), "events": ev}


def _took(sec):
    return "" if sec is None else f"{sec // 60}m{sec % 60:02d}s" if sec >= 60 else f"{sec}s"


def example_html(name, label, ex):
    pl, worker = ex["plan"], ex["worker"]
    cmd = f"fm code {shlex.quote(ex['request'])}" + (f" --worker {shlex.quote(worker)}" if worker else "")
    rows = []
    for i, c in enumerate(pl.get("criteria") or [], 1):
        got = ex["checks"].get(i, {})
        after = got.get("after")
        chip = ("pass", "PASS") if after == 0 else ("fail", "FAIL") if after is not None else ("todo", "····")
        first = " (failed before the work)" if got.get("before") not in (0, None) else ""
        rows.append(f'<li><span class="chip {chip[0]}">{chip[1]}</span> {esc(c.get("text", ""))}'
                    f'<code>{esc(c.get("verify", ""))}</code><small>{first}</small></li>')
    files = "".join(f"<li><code>{esc(f)}</code> <span class=\"plus\">+{a}</span>"
                    + (f' <span class="minus">−{d}</span>' if d else "") + "</li>" for f, (a, d) in ex["stat"].items())
    facts = [f"{ex['turns']} worker turn{'s' if ex['turns'] != 1 else ''}" if ex["turns"] else "",
             f"{ex['tokens'] / 1000:.0f}k tokens" if ex["tokens"] else "", _took(ex["seconds"])]
    end = {"closed": "Closed", "blocked": "Blocked", "error": "Stopped", "answer": "Answer"}.get(ex["end"], "Ended")
    return (f'<article class="ex" id="ex-{name}"><header><span class="ex-kind">{esc(label)}</span>'
            f'<p class="ex-cmd"><code>{esc(cmd)}</code></p></header><div class="ex-body">'
            f'<img class="ex-shot" src="../assets/examples/{name}.svg" loading="lazy" alt="fm code tui at the end of this '
            f'run: {esc(pl.get("title", ""))}"><div class="ex-facts">'
            + (f'<p><b>Plan</b> {esc(pl.get("type", ""))} {esc(pl.get("tier", ""))} · {esc(pl.get("title", ""))}</p>'
               if pl.get("type") else '<p><b>Plan</b> a question: answered from the files, no task, nothing changed</p>')
            + (f'<p><b>Steps</b></p><ol class="ex-steps">{"".join(f"<li>{esc(s)}</li>" for s in pl.get("steps") or [])}</ol>'
               if pl.get("steps") else "")
            + (f'<p><b>Checks</b></p><ul class="ex-checks">{"".join(rows)}</ul>' if rows else "")
            + (f'<p><b>Changed</b></p><ul class="ex-files">{files}</ul>' if files else "")
            + (f'<div class="ex-answer"><p><b>{end}</b></p>{"".join(f"<p>{esc(x)}</p>" for x in ex["end_text"].split(chr(10)) if x.strip())}</div>'
               if ex["end"] == "answer" else f'<p class="ex-end"><b>{end}</b> {esc(ex["end_text"])}</p>')
            + f'<p class="ex-meta">{esc(" · ".join(x for x in facts if x))} · replay it: '
              f'<code>fm code tui --events demo/examples/{name}.jsonl</code> · '
              f'<a href="../stories/{name}.html">the case study</a></p></div></div></article>')


STEP_KINDS = {"before": "before", "verify": "check"}


def case_study_html(name, label, ex):
    """T-1541: one recorded run as a case study: its card, then every event in order at the time it came: the checks
    failing before the work, each step and what it changed, the checks after, and how it ended."""
    ev = ex["events"]
    t0 = next((e["ts"] for e in ev if isinstance(e.get("ts"), (int, float))), 0)
    rows = []
    for e in ev:
        kind, at = e.get("event"), e.get("ts")
        when = (_took(round(at - t0)) or "0s") if isinstance(at, (int, float)) else ""
        if kind == "verify":
            ok = e.get("exit") == 0
            rows.append((when, "before" if e.get("label") == "before" else "check",
                         f"{'passes' if ok else 'fails'}: <code>{esc(str(e.get('cmd') or ''))}</code>",
                         "pass" if ok else "fail"))
        elif kind == "step":
            rows.append((when, "step", esc(str(e.get("text") or f"step {e.get('step')}")), ""))
        elif kind == "changed":
            rows.append((when, "changed", ", ".join(f"<code>{esc(str(f))}</code>" for f in e.get("files") or []), ""))
        elif kind in ("closed", "blocked", "error", "answer"):
            rows.append((when, kind, esc(str(e.get("text") or "")), "pass" if kind == "closed" else ""))
    timeline = "".join(f'<li class="{cls}"><span class="at">{w}</span> <b>{esc(k)}</b> {txt}</li>'
                       for w, k, txt, cls in rows)
    title = ex["plan"].get("title") or ex["request"]
    return (f'<p class="kicker">Case study · {esc(label)}</p><h1>{esc(title)}</h1><p class="lede">{esc(ex["request"])}'
            f'</p>{example_html(name, label, ex)}<section><h2>The run, event by event</h2>'
            f'<ol class="timeline">{timeline}</ol></section>'
            '<p class="next"><a href="../features/code.html">Back to fm code</a></p>')


def examples_html(folder=None):
    folder = folder or os.path.join(ROOT, "demo", "examples")
    cards = [example_html(n, label, load_example(os.path.join(folder, n + ".jsonl")))
             for n, label in EXAMPLES if os.path.isfile(os.path.join(folder, n + ".jsonl"))]
    return f'<div class="examples">{"".join(cards)}</div>' if cards else ""


def render_page(p, stats, pages):
    parts = [f'<p class="kicker">{esc(p["nav"])}</p><h1>{esc(p["title"])}</h1><p class="lede">{p["lede"]}</p>']
    for block in p["blocks"]:
        kind = block[0]
        if kind == "text":  # T-1246: its body may be computed from the stats
            body = block[2](stats) if callable(block[2]) else block[2]
            parts.append(f"<section><h2>{esc(block[1])}</h2>{body}</section>")
        elif kind == "term":
            parts.append(f'<div class="term"><pre>{block[1]}</pre></div>')
        elif kind == "chart":
            parts.append(block[1](stats))
        elif kind == "raw":
            parts.append(block[1])
        elif kind == "examples":  # T-1320
            parts.append(f"<section><h2>{esc(block[1])}</h2>{block[2]}{examples_html()}</section>")
    i = [q["slug"] for q in pages].index(p["slug"])
    nxt = pages[(i + 1) % len(pages)]
    parts.append(f'<p class="next"><a href="{nxt["slug"]}.html">Next: {esc(nxt["nav"])}</a></p>')
    return layout(p["title"], p["desc"], "".join(parts), pages, p["slug"])


def render_index(pages):
    cards = "".join(f'<a class="fcard" href="{p["slug"]}.html"><b>{esc(p["nav"])}</b><span>{esc(p["desc"])}</span></a>'
                    for p in pages)
    body = ('<p class="kicker">Features</p><h1>Everything Foreman does</h1><p class="lede">Each page shows what one part '
            'of Foreman does, how it works, the commands, and charts from Foreman\'s own record of building itself.</p>'
            f'<div class="fgrid">{cards}</div>')
    return layout("Features", "Every part of Foreman, with charts from its own history.", body, pages, "index")


def build(out):
    sys.path.insert(0, HERE)
    import pages as P
    with open(os.path.join(HERE, "data", "stats.json"), encoding="utf-8") as f:
        stats = json.load(f)
    bench_path = os.path.join(HERE, "data", "bench.json")
    if os.path.isfile(bench_path):  # T-1222: the safety benchmark (site/bench_safety.py)
        with open(bench_path, encoding="utf-8") as f:
            stats.update(json.load(f))
    if os.path.isdir(out):
        shutil.rmtree(out)
    shutil.copytree(HERE, out, ignore=lambda d, names: [n for n in names if n in SOURCE_ONLY])
    with open(os.path.join(out, "index.html"), encoding="utf-8") as f:  # T-1609: the hero's poster
        page = f.read()
    for what, mark in (("proof", PROOF_MARK), ("shaders", SHADER_MARK)):  # review: a lost mark shipped a hero with no proof
        if mark not in page:
            raise SystemExit(f"build.py: site/index.html lost the {what} mark: {mark}")
    totals, asof = stats.get("totals") or {}, str(stats.get("generated") or "")
    sys.path.insert(0, os.path.join(ROOT, "plugin", "lib"))  # T-1283: fm code tui draws its own picture
    import fmcodetui
    import fmreplay
    import fmscene
    looks = [c for c in fmscene.sketch_cards() if c["name"] in LANDING_SHADERS]
    if len(looks) != len(LANDING_SHADERS):  # a renamed card would ship a short strip
        raise SystemExit("build.py: a landing shader card is missing: " + ", ".join(LANDING_SHADERS))
    page = page.replace(SHADER_MARK, fmscene.sketchbook_html(looks, page=False), 1)
    cards = stats.get("cards") or {}
    counts = {"tasks": totals.get("tasks_done", 0), "tests": (stats.get("code") or {}).get("tests", 0),  # T-2040
              "cards": sum(cards.values()), "areas": len(cards), "pages": len(P.PAGES), "replay": fmreplay.MAX}
    if not (counts["tests"] and counts["cards"]):  # review: a stats.json without them shipped "0 tests"
        raise SystemExit("build.py: site/data/stats.json has no code.tests or cards; run site/stats.py")
    page = page.replace(PROOF_MARK, proof(totals, asof), 1).replace('rel="icon" href="assets/foreman.svg"',
                                                                    f'rel="icon" href="{ICON}"', 1)
    for k, v in counts.items():
        page = page.replace("{{" + k + "}}", fmt(v))
    if "{{" in page:  # a count the build doesn't know would ship as braces
        raise SystemExit("build.py: site/index.html has an unknown {{count}}: " + page[page.index("{{"):][:40])
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    os.makedirs(os.path.join(out, "demo"), exist_ok=True)
    for f in ("live.mp4", "demo.svg"):
        shutil.copy2(os.path.join(ROOT, "demo", f), os.path.join(out, "demo", f))
    with open(os.path.join(ROOT, "demo", "code-tui.jsonl"), encoding="utf-8") as f:
        fmcodetui.snapshot([json.loads(line) for line in f if line.strip()], os.path.join(out, "assets", "code-tui.svg"),
                           (120, 34))
    fmcodetui.tour_svg(os.path.join(out, "assets", "code-tui-tour.svg"), (120, 34))  # T-2061: today's TUI, every build
    os.makedirs(os.path.join(out, "assets", "examples"), exist_ok=True)  # T-1320: each example's last screen
    for name, _ in EXAMPLES:
        src = os.path.join(ROOT, "demo", "examples", name + ".jsonl")
        if os.path.isfile(src):
            fmcodetui.snapshot(load_example(src)["events"], os.path.join(out, "assets", "examples", name + ".svg"),
                               (120, 34))
    os.makedirs(os.path.join(out, "stories"), exist_ok=True)  # T-1541: each recorded run as a case study
    for name, label in EXAMPLES:
        src = os.path.join(ROOT, "demo", "examples", name + ".jsonl")
        if os.path.isfile(src):
            ex = load_example(src)
            with open(os.path.join(out, "stories", name + ".html"), "w", encoding="utf-8") as f:
                f.write(layout(f"Case study: {ex['plan'].get('title') or label}", ex["request"][:150],
                               case_study_html(name, label, ex), P.PAGES, None))
    os.makedirs(os.path.join(out, "gallery"), exist_ok=True)  # T-1785: each UI playbook's worked example
    for name, _, _, src in P.gallery():
        if not os.path.isfile(src):
            raise SystemExit(f"build.py: ui/{name}.md's Example: line names a file that doesn't exist: {src}")
        shutil.copy2(src, os.path.join(out, "gallery", name + ".html"))
    os.makedirs(os.path.join(out, "features"), exist_ok=True)
    for p in P.PAGES:
        with open(os.path.join(out, "features", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(render_page(p, stats, P.PAGES))
    with open(os.path.join(out, "features", "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index(P.PAGES))
    return len(P.PAGES)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_site")
    if target.startswith("-"):  # it takes no options: `--check` once became a folder that got committed
        print("usage: python3 site/build.py [OUTPUT_FOLDER] (default _site; it takes no options)", file=sys.stderr)
        sys.exit(2)
    if not safe_out(target):
        sys.exit(f"build.py: refusing to wipe {target}: give a new or build-only folder, such as _site")
    n = build(os.path.abspath(target))
    outside = outside_hosts(target)
    if outside:
        sys.exit("build.py: the site loads nothing from another host (T-1411), but these would:\n  " + "\n  ".join(outside))
    print(f"built {target}: landing page + {n} feature pages")
