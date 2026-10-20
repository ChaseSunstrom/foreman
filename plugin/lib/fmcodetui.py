"""T-1283: Foreman Code's terminal UI (`fm code tui`). It runs fm code as a child with --json and draws only from that
event stream (fmcode.EVENTS), so the harness stays the source of truth: the TUI never edits, verifies or closes.

Layers, each testable without a terminal: State (events → what happened); Canvas and the panels (a grid of styled
cells); render (state + config → a canvas); App (keys → commands, views, the child process). main() is the thin curses
driver, --plain its line-by-line twin and --snapshot an SVG of the screen. Pictures over prose: a station track, check
chips, change bars and a token chart; the model's own words are one key away. Themes, layout and keys are config;
panels and commands are registries extensions add to. Stdlib only."""
import html
import json
import os
import queue
import shutil
import signal
import subprocess
import sys
import threading
import time

SCHEMA = 1  # the fm code event stream this reader knows (fmcode.SCHEMA)
FM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "fm")

# Themes come from a palette of a few colours. A colour is "#rrggbb" or a 0-255 index; the driver maps hex to the
# terminal's 256 colours (8 on a small terminal), NO_COLOR drops them, and the SVG snapshot uses them as they are.
PALETTES = {
    "night": {"bg": "#0D1420", "bar": "#1B2638", "head": "#131C2B", "ink": "#E7ECF4", "dim": "#8A98AE",
              "said": "#9AA8BC", "accent": "#86A8FF", "ok": "#47C98B", "bad": "#FF6B6B", "warn": "#FFC83D",
              "edge": "#33445F", "track": "#2E3D58", "shade": "#2A3650", "barink": "#C9D3E3"},
    "paper": {"bg": "#F6F7F9", "bar": "#E1E6EE", "head": "#E9EDF3", "ink": "#1B2330", "dim": "#5E6B7E",
              "said": "#4F5B6C", "accent": "#2F54C9", "ok": "#12805C", "bad": "#C42B2B", "warn": "#9A6200",
              "edge": "#C3CCD9", "track": "#CDD5E1", "shade": "#C9D1DD", "barink": "#2B3442", "paint": True},
}
_BG, _INK = PALETTES["night"]["bg"], PALETTES["night"]["ink"]


def _theme(p):
    """Every style from a palette; a light palette paints the screen (a dark terminal would show through)."""
    chip = lambda c: {"fg": p["bg"], "bg": c, "bold": True}
    return {"screen": dict({"fg": p["ink"], "bg": p["bg"]}, **({"paint": True} if p.get("paint") else {})),
            "text": {}, "strong": {"fg": p["ink"], "bold": True}, "dim": {"fg": p["dim"]},
            "said": {"fg": p["said"], "italic": True}, "accent": {"fg": p["accent"], "bold": True},
            "ok": {"fg": p["ok"]}, "bad": {"fg": p["bad"], "bold": True}, "warn": {"fg": p["warn"]},
            "border": {"fg": p["edge"]}, "title": {"fg": p["accent"], "bold": True}, "track": {"fg": p["track"]},
            "chart": {"fg": p["accent"]}, "shade": {"fg": p["shade"]}, "select": {"fg": p["bg"], "bg": p["accent"]},
            "brand": chip(p["accent"]), "header": {"fg": p["ink"], "bg": p["head"]},
            "header_dim": {"fg": p["dim"], "bg": p["head"]}, "bar": {"fg": p["barink"], "bg": p["bar"]},
            "bar_dim": {"fg": p["dim"], "bg": p["bar"]}, "key": {"fg": p["warn"], "bg": p["bar"], "bold": True},
            "input": {"fg": p["ink"], "bg": p["bar"], "bold": True}, "chip_ok": chip(p["ok"]),
            "chip_bad": chip(p["bad"]), "chip_warn": chip(p["warn"]), "chip_accent": chip(p["accent"]),
            "chip_todo": {"fg": p["dim"], "bg": p["bar"]}}


def _mono():
    """No colours: what had a background is reversed, the rest keeps its weight."""
    return {n: dict({k: v for k, v in spec.items() if k in ("bold", "italic")}, **({"reverse": True} if "bg" in spec
                                                                                   and n != "screen" else {}))
            for n, spec in _theme(PALETTES["night"]).items()}


PRESETS = {"night": lambda: _theme(PALETTES["night"]), "paper": lambda: _theme(PALETTES["paper"]), "mono": _mono}
THEME = PRESETS["night"]()
BORDERS = {"rounded": "╭╮╰╯─│", "square": "┌┐└┘─│", "heavy": "┏┓┗┛━┃", "double": "╔╗╚╝═║", "ascii": "++++-|"}
DEFAULTS = {
    "preset": "night",
    "theme": THEME,
    "border": "rounded",
    "layout": {"top": ["track"], "columns": [["log"], ["checks", "files", "time", "tokens"]], "widths": [58, 42],
               "heights": [[1], ["auto", "auto", "auto", 1]], "narrow": ["checks", "log"],
               "narrow_heights": ["auto", 1], "narrow_below": 80},
    "keys": {"q": "quit", "n": "new", "s": "stop", "r": "resume", "?": "help", "d": "diff", "h": "history",
             "m": "model", "t": "thoughts", "\t": "focus", "KEY_UP": "up", "KEY_DOWN": "down", "k": "up", "j": "down",
             "\n": "expand", "KEY_ENTER": "expand", "KEY_PPAGE": "page_up", "KEY_NPAGE": "page_down", "G": "follow"},
}
HINTS = [("n", "new"), ("d", "diff"), ("h", "history"), ("t", "thoughts"), ("?", "keys"), ("q", "quit")]
CHIP = {"done": (" ✓ ", "chip_ok"), "now": (" ● ", "chip_accent"), "todo": ("   ", "chip_todo"),
        "fail": (" ✖ ", "chip_bad")}
NODE = {"done": ("●", "ok"), "now": ("◉", "accent"), "todo": ("○", "track"), "fail": ("✖", "bad")}
LINK = {"done": ("━", "ok"), "now": ("━", "accent"), "fail": ("━", "bad"), "todo": ("─", "track")}
BLOCKS = "▁▂▃▄▅▆▇█"
LOG_HIDES = ("plan", "task", "before")  # the track and Checks show these; --plain prints them
SINGLE_BELOW = 60  # columns: a terminal narrower than this shows the activity log alone


# ---------------------------------------------------------------- state: what the events say happened

class State:
    def __init__(self):
        self.request = self.task = self.model = self.worker = self.error = None
        self.plan, self.criteria, self.steps, self.step = {}, [], [], 0
        self.actions, self.log, self.verify, self.files, self.stat = [], [], [], {}, {}
        self.tokens, self.calls, self.status, self.closed = [0, 0], [], "idle", ""
        self.first_ts = self.last_ts = None
        self.marks = {}  # when each step (1, 2, …) and the final checks ("checks") began
        self.ext = {}  # extensions' own data for this run

    def apply(self, e):
        """Take one event; an unknown or malformed one changes nothing (a newer fm code may send more)."""
        kind = e.get("event") if isinstance(e, dict) else None
        fn = getattr(self, f"_on_{kind}", None) if isinstance(kind, str) and kind.isidentifier() else None
        if fn:
            fn(e)
            if isinstance(e.get("ts"), (int, float)):
                self.first_ts = self.first_ts or e["ts"]
                self.last_ts = e["ts"]
        for h in (HANDLERS.get(kind, []) + HANDLERS.get("*", [])) if isinstance(kind, str) else []:
            try:
                h(self, e)
            except Exception as x:  # an extension's handler that throws is said once and dropped
                for hs in HANDLERS.values():
                    if h in hs:
                        hs.remove(h)
                self.note("error", text=f"extension {getattr(h, '__module__', '?')}: {type(x).__name__}: {x}")
        return self

    def note(self, kind, **fields):
        self.log.append(dict(fields, kind=kind))

    def _on_start(self, e):
        if int(e.get("schema") or 1) > SCHEMA:
            raise ValueError(f"fm code's event stream is schema {e.get('schema')}; this TUI reads {SCHEMA}: update Foreman")
        if e.get("resume") and self.plan:  # fm code --resume sends no plan again: the screen keeps the run's
            self.task, self.status = e.get("task") or self.task, "running"
            return
        self.__init__()
        self.request, self.model, self.worker, self.task = (e.get(k) for k in ("request", "model", "worker", "task"))
        self.status = "planning"

    def _on_plan(self, e):
        p = e.get("plan") if isinstance(e.get("plan"), dict) else {}
        self.plan = p
        self.criteria = [{"text": str(c.get("text", "")), "verify": str(c.get("verify", "")), "state": "todo"}
                         for c in p.get("criteria") or [] if isinstance(c, dict)]
        self.steps = [{"text": str(s), "state": "todo"} for s in p.get("steps") or []]
        self.note("plan", text=str(p.get("title", "")), sub=f"{p.get('type', '')} {p.get('tier', '')}".strip(),
                  checks=len(self.criteria), steps=len(self.steps))

    def _on_task(self, e):
        self.task, self.status = e.get("task"), "running"
        self.note("task", text=str(e.get("text") or e.get("task") or ""))

    _on_resume = _on_task

    def _on_step(self, e):
        n = int(e.get("step") or 0)
        for i, s in enumerate(self.steps, 1):
            s["state"] = "done" if i < n else "now" if i == n else s["state"]
        self.step, self.status, self.marks[n] = n, "running", e.get("ts")
        self.note("step", n=n, text=self.steps[n - 1]["text"] if 0 < n <= len(self.steps) else "")

    def _on_say(self, e):
        self.note("say", text=e.get("text", ""))

    def _on_tokens(self, e):
        self.tokens = [int(e.get("total_in") or 0), int(e.get("total_out") or 0)]
        self.calls.append(int(e.get("call_in") or 0))

    def _on_action(self, e):
        a = {k: e.get(k) for k in ("action", "target", "result", "detail")}
        a["step"] = self.step
        self.actions.append(a)
        self.note("action", **a)

    def _on_worker(self, e):
        self.note("worker", text=e.get("text", ""))

    def _on_revert(self, e):
        self.note("revert", file=e.get("file"), reason=e.get("reason"))

    def _on_fix(self, e):
        self.status = "fixing"
        self.note("fix", text=e.get("text", ""))

    def _on_verify(self, e):
        self.verify.append(e)
        n, bad, label = int(e.get("criterion") or 0), bool(e.get("exit")), e.get("label") or "verify"
        if 0 < n <= len(self.criteria):
            c = self.criteria[n - 1]
            c["state"], c["first"] = ("fail" if bad else "pass"), label == "before"
        if label == "before":  # the red run before the work: the Checks panel's; --plain prints it
            self.note("before", n=n, bad=bad, cmd=e.get("cmd") or "", detail=e.get("output"))
        else:
            for s in self.steps:
                s["state"] = "done"
            self.marks.setdefault("checks", e.get("ts"))
            self.note("verify", n=n, bad=bad, cmd=e.get("cmd") or "", detail=e.get("output"))

    def _on_changed(self, e):
        self.files[int(e.get("step") or self.step)] = [str(f) for f in e.get("files") or []]
        if isinstance(e.get("stat"), dict):
            self.stat = {str(k): v for k, v in e["stat"].items() if isinstance(v, list) and len(v) == 2}

    def _on_closed(self, e):
        self.status, self.closed = "closed", e.get("text", "")
        for s in self.steps:
            s["state"] = "done"
        if isinstance(e.get("tokens"), list) and len(e["tokens"]) == 2:
            self.tokens = [int(e["tokens"][0] or 0), int(e["tokens"][1] or 0)]
        self.note("closed", text=e.get("text", ""))

    def _on_blocked(self, e):
        self.status, self.error = "blocked", e.get("reason") or e.get("text")
        self.note("blocked", text=e.get("text", ""))

    def _on_error(self, e):
        self.status, self.error = "error", e.get("text")
        self.note("error", text=e.get("text", ""))

    def _on_exit(self, e):  # the TUI's own: the child ended
        if self.status in ("planning", "running", "fixing", "idle") and e.get("code"):
            self.status = "stopped"
            if e.get("stderr"):
                self.note("error", text=e["stderr"].strip().splitlines()[-1])


def duration(s):
    s = max(0, int(s))
    return f"{s}s" if s < 60 else f"{s // 60}m{s % 60:02d}s" if s < 3600 else f"{s // 3600}h{s // 60 % 60:02d}m"


def stations(st):
    """[(label, sub, state)] along the track: the plan, each step, the checks, the close."""
    planned = st.marks.get(1)
    nodes = [("plan", duration(planned - st.first_ts) if isinstance(planned, (int, float)) and st.first_ts else "",
              "done" if st.plan else "now" if st.status == "planning" else "todo")]
    for i, s in enumerate(st.steps, 1):
        n = sum(a["step"] == i for a in st.actions)
        start, end = st.marks.get(i), st.marks.get(i + 1) or st.marks.get("checks") or st.last_ts
        took = duration(end - start) if isinstance(start, (int, float)) and isinstance(end, (int, float)) else ""
        sub = "  ".join(x for x in (f"{n} action{'s' * (n != 1)}" if n else "", took if s["state"] != "todo" else "") if x)
        nodes.append((s["text"], sub, s["state"]))
    after = [v for v in st.verify if v.get("label") != "before"]
    passed = sum(c["state"] == "pass" for c in st.criteria)
    check = ("done" if st.criteria and passed == len(st.criteria) and after else
             "fail" if after and after[-1].get("exit") and st.status != "fixing" else
             "now" if after or st.status == "fixing" else "todo")
    nodes.append(("checks", f"{passed}/{len(st.criteria)} pass" if after else "", check))
    sha = next((w for w in st.closed.split() if len(w) >= 7 and all(c in "0123456789abcdef" for c in w)), "")
    nodes.append(("close", sha or (st.status if st.status in ("blocked", "error", "stopped") else ""),
                  "done" if st.status == "closed" else "fail" if st.status in ("blocked", "error", "stopped") else "todo"))
    return nodes


# ---------------------------------------------------------------- canvas and widgets

class Canvas:
    """A grid of (character, style) cells; .text() is what a test reads, to_svg what a reader sees."""
    def __init__(self, w, h):
        self.w, self.h = max(w, 1), max(h, 1)
        self.cells = [[(" ", "text")] * self.w for _ in range(self.h)]

    def put(self, y, x, s, style="text", right=None):
        """s at (y, x), clipped at `right` (exclusive) or the edge; the column after it."""
        if not 0 <= y < self.h:
            return x
        end = min(self.w, right if right is not None else self.w)
        for ch in str(s):
            if x >= end:
                break
            if x >= 0:
                self.cells[y][x] = (ch if ch.isprintable() else " ", style)
            x += 1
        return x

    def line(self, y, x, segments, right):
        """A line of (text, style) segments from x, clipped at right; the last one gets the ellipsis."""
        for text, style in segments:
            if x >= right:
                break
            x = self.put(y, x, fit(text, right - x, strip=False), style, right=right)
        return x

    def fill(self, y, style, x=0, right=None):
        self.put(y, x, " " * ((right if right is not None else self.w) - x), style)

    def text(self):
        return "\n".join("".join(c for c, _ in row).rstrip() for row in self.cells)

    def style_of(self, needle):
        """The style of the first cell of needle's first appearance (tests ask what a line looks like)."""
        for row in self.cells:
            i = "".join(c for c, _ in row).find(needle)
            if i >= 0:
                return row[i][1]
        return None


def fit(s, n, strip=True):
    s = " ".join(str(s).split()) if strip else str(s).replace("\n", " ")
    return s if len(s) <= n else s[:max(n - 1, 0)] + "…" if n > 0 else ""


def tail(s, n):
    """A path in n columns, keeping its end (the file name)."""
    return s if len(s) <= n else "…" + s[-(n - 1):] if n > 1 else s[-n:]


def wrap(s, n, lines=2):
    """s in at most `lines` lines of n columns, broken at spaces; the last one ends in … when it's cut."""
    out, cur = [], ""
    for word in " ".join(str(s).split()).split(" "):
        if cur and len(cur) + 1 + len(word) > n:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    out.append(cur)
    if len(out) > lines:
        out = out[:lines - 1] + [fit(" ".join(out[lines - 1:]), n)]
    return [fit(x, n) for x in out]


def box(cv, y, x, h, w, title, cfg, focused=False, note=""):
    """A bordered panel, its title and a dim note in the top edge; its inner (y, x, h, w)."""
    tl, tr, bl, br, hz, vt = BORDERS.get(cfg.get("border"), BORDERS["rounded"])
    edge = "accent" if focused else "border"
    if h < 2 or w < 4:
        return y, x, 0, 0
    cv.put(y, x, tl + hz * (w - 2) + tr, edge)
    for r in range(y + 1, y + h - 1):
        cv.put(r, x, vt, edge)
        cv.put(r, x + w - 1, vt, edge)
    cv.put(y + h - 1, x, bl + hz * (w - 2) + br, edge)
    if title and w > 8:
        end = cv.put(y, x + 2, f" {fit(title, w - 8 - (len(note) + 2 if note else 0))} ", "title")
        if note and end + len(note) + 3 < x + w:
            cv.put(y, x + w - len(note) - 4, f" {note} ", "dim")
    return y + 1, x + 2, h - 2, w - 4


def _segments(cells):
    out = []
    for ch, style in cells:
        if out and out[-1][1] == style:
            out[-1] = (out[-1][0] + ch, style)
        else:
            out.append((ch, style))
    return out


def columns(values, w, height=3):
    """values as a column chart `height` rows tall, newest on the right; [row text, …] top first."""
    cw = max(1, min(6, (w + 1) // max(len(values), 1) - 1))
    vals = values[-max(1, (w + 1) // (cw + 1)):]
    top = max(vals, default=0) or 1
    out = []
    for r in range(height):
        base = (height - 1 - r) * 8
        cells = [BLOCKS[min(8, e - base) - 1] if e > base else " " for e in
                 (max(1, round(v * height * 8 / top)) if v else 0 for v in vals)]
        out.append(" ".join(c * cw for c in cells))
    return out


# ---------------------------------------------------------------- panels: (state, width, height, app) → lines
# Each panel returns lines of (text, style) segments. height is None when the layout measures it (an "auto"
# panel), or the inner rows a stretching panel has to fill.

def _track(st, w, h, app):
    """The run as a line of stations (✓ done, ● now, an empty slot to come, ✖ failed), each labelled under it; a
    long plan on a narrow screen gets one-cell nodes."""
    nodes = stations(st)
    n = len(nodes)
    big = (w - 3) / (n - 1) >= 7
    marks = CHIP if big else NODE
    cw = 3 if big else 1
    xs = [round(i * (w - cw) / (n - 1)) for i in range(n)]
    rows = [[(" ", "text")] * w for _ in range(3)]
    for i, (_, _, state) in enumerate(nodes):
        glyph, style = marks[state]
        for k, ch in enumerate(glyph):
            rows[0][xs[i] + k] = (ch, style)
        if i < n - 1:
            for x in range(xs[i] + cw + (1 if big else 0), xs[i + 1] - (1 if big else 0)):
                rows[0][x] = LINK[nodes[i + 1][2]]
    gap = (w - cw) // (n - 1)
    for r in (1, 2):
        last = fit(nodes[-1][r - 1], max(1, gap - 1))
        starts = xs[:-1] + [w - len(last)]
        for i, node in enumerate(nodes):
            room = len(last) if i == n - 1 else starts[i + 1] - starts[i] - 1
            if room < 4 and node[2] not in ("now", "fail"):
                continue
            style = {"now": "accent", "done": "text", "fail": "bad"}.get(node[2], "dim") if r == 1 else "dim"
            text = node[r - 1] if r == 1 or len(node[r - 1]) <= room else node[r - 1].split("  ")[-1]  # time first
            for k, ch in enumerate(fit(text, max(room, 4))):
                if starts[i] + k < w:
                    rows[r][starts[i] + k] = (ch, style)
    return [_segments(r) for r in rows]


def _checks(st, w, h, app):
    if not st.criteria:
        return [[("checks come with the plan", "dim")]]
    out = []
    for c in st.criteria:
        chip = (" PASS ", "chip_ok") if c["state"] == "pass" else (" RED  ", "chip_warn") if c.get("first") else \
            (" FAIL ", "chip_bad") if c["state"] == "fail" else (" ···· ", "chip_todo")
        first, *more = wrap(c["text"], max(8, w - 8))
        out.append([chip, ("  ", "text"), (first, "text")])
        out += [[("        ", "text"), (line, "text")] for line in more]
    return out


def _files(st, w, h, app):
    stat = st.stat or {f: [0, 0] for fs in st.files.values() for f in fs}
    if not stat:
        return [[("nothing changed yet", "dim")]]
    rows = sorted(stat.items(), key=lambda kv: (-(kv[1][0] + kv[1][1]), kv[0]))
    top = max(1, max(a + d for _, (a, d) in rows))
    nums = max(len(f" +{a} −{d}") for _, (a, d) in rows)
    nw = max(6, min(max(len(p) for p, _ in rows), w - nums - 8))
    bw = max(2, w - nw - nums - 1)
    out = []
    for path, (a, d) in rows:
        plus = max(1 if a else 0, round(a * bw / top))
        minus = max(1 if d else 0, min(bw - plus, round(d * bw / top)))
        out.append([(tail(path, nw).ljust(nw), "text"), (" ", "text"), ("▆" * plus, "ok"), ("▆" * minus, "bad"),
                    (" " * (bw - plus - minus), "text"), (f" +{a}", "ok"), (f" −{d}" if d else "", "bad")])
    return out


def _tokens(st, w, h, app):
    """Each model call's prompt size as a column, newest on the right, sat on the panel's floor; the totals under it."""
    if not st.calls:
        return [[("no model calls yet", "dim")]]
    tall = min(10, max(3, (h or 5) - 1))
    lines = [[(row, "chart")] for row in columns(st.calls, w, tall)]
    lines.append([(human(st.tokens[0]), "strong"), (" in   ", "dim"), (human(st.tokens[1]), "strong"), (" out", "dim")])
    return [[]] * max(0, (h or 0) - len(lines)) + lines


def spans(st):
    """[(label, start, end)] of the run's phases (plan, each step, the checks) in seconds from its start."""
    if not st.first_ts:
        return []
    at = lambda v: isinstance(v, (int, float))
    marks = [("plan", st.first_ts)] + [(f"step {k}", st.marks[k]) for k in sorted(k for k in st.marks if k != "checks")
                                       if at(st.marks[k])]
    marks += [("checks", st.marks["checks"])] if at(st.marks.get("checks")) else []
    ends = [m[1] for m in marks[1:]] + [st.last_ts]
    return [(label, start - st.first_ts, end - st.first_ts) for (label, start), end in zip(marks, ends)]


def _time(st, w, h, app):
    """Where the time went: each phase as a bar on the run's own clock."""
    sp = spans(st)
    if not sp:
        return [[("starts with the run", "dim")]]
    total = max(1, sp[-1][2])
    dw = max(len(duration(e - s)) for _, s, e in sp) + 2
    bw = max(4, w - 8 - dw)
    out = []
    for i, (label, s, e) in enumerate(sp):
        a = min(bw - 1, int(s * bw / total))
        b = max(a + 1, min(bw, round(e * bw / total)))
        live = i == len(sp) - 1 and st.status != "closed"
        style = ("bad" if st.status in ("blocked", "error", "stopped") else "accent") if live else "ok"
        out.append([(f"{label:<8}", "dim"), (" " * a, "text"), ("▆" * (b - a), style), (" " * (bw - b), "text"),
                    (duration(e - s).rjust(dw), "accent" if live else "dim")])
    return out


def entry_segments(e, w, thoughts=True):
    """An Activity line; None for one the panel leaves out (the model's own words unless thoughts are on)."""
    k = e.get("kind")
    if k == "step":
        head = f" {e['n']} "
        return [("──", "border"), (head, "chip_accent"), (" " + e["text"] + " ", "strong"),
                ("─" * max(0, w - len(head) - len(e["text"]) - 4), "border")]
    if k == "say":
        return [("  ┊ ", "border"), (e["text"], "said")] if thoughts else None
    if k == "action":
        if e.get("result") == "refused":
            return [("  ⊘ ", "bad"), (f"{e.get('action') or '':<7}", "dim"), (str(e.get("target") or ""), "bad"),
                    ("  ", "text"), (" GUARD ", "chip_bad")]
        bad = e.get("result") == "error"
        return [(f"  {'!' if bad else '✓'} ", "warn" if bad else "ok"), (f"{e.get('action') or '':<7}", "dim"),
                (str(e.get("target") or ""), "warn" if bad else "text")]
    if k == "revert":
        return [("  ↺ ", "warn"), (f"{'revert':<7}", "dim"), (str(e.get("file")), "warn"), ("  ", "text"),
                (" PUT BACK ", "chip_warn")]
    if k == "verify":
        return [("  ", "text"), (" FAIL " if e["bad"] else " PASS ", "chip_bad" if e["bad"] else "chip_ok"),
                (f"  check {e['n']}", "dim")]
    if k == "before":
        return [("  ", "text"), (" RED " if e["bad"] else " GREEN ", "chip_warn" if e["bad"] else "chip_ok"),
                (f"  check {e['n']} before the work", "dim")]
    if k == "plan":
        return [(" PLAN ", "chip_accent"), (f"  {e['text']}", "strong"),
                (f"  {e['sub']}, {e['checks']} checks, {e['steps']} steps", "dim")]
    if k == "task":
        return [("  ", "text"), (e["text"], "dim")]
    if k == "fix":
        return [("  ↻ ", "warn"), (e["text"], "warn")]
    if k == "worker":
        return [("  ⚙ ", "accent"), (e["text"].strip(), "text")]
    if k == "closed":
        return [(" DONE ", "chip_ok"), ("  " + e["text"], "ok")]
    if k in ("blocked", "error"):
        return [(" STOP ", "chip_bad"), ("  " + e["text"], "bad")]
    return [("  ", "text"), (e.get("text", ""), "dim")]


def entry_text(e):
    """An Activity line as plain text (--plain): a refusal says why, and no control character reaches the terminal."""
    text = "".join(t for t, _ in entry_segments(e, 0) or []).strip(" ─")
    if e.get("kind") == "action" and e.get("result") == "refused" and e.get("detail"):
        text += f" — {e['detail']}"
    return "".join(c if c.isprintable() else " " for c in text)


def _log(st, w, h, app):
    out, thoughts = [], app is None or app.thoughts
    for i, e in enumerate(st.log):
        segs = None if e.get("kind") in LOG_HIDES else entry_segments(e, w, thoughts)
        if segs is None:
            continue
        if app is not None and app.selected == i:
            segs = [("".join(t for t, _ in segs).ljust(w), "select")]
        out.append(segs)
        if app is not None and i in app.expanded and e.get("detail"):
            out += [[("      ", "text"), (part, "dim")] for line in str(e["detail"]).splitlines()[:30]
                    for part in wrap(line, max(10, w - 6), lines=4)]
    return out or [[("press ", "dim"), ("n", "accent"), (" and type a request", "dim")]]


def _plan(st, w, h, app):  # the plan in words: not in the default layout, one config line away
    if not st.plan:
        return [[("no plan yet", "dim")]]
    out = [[(line, "strong")] for line in wrap(st.plan.get("title", ""), w)]
    for c in st.criteria:
        out += [[("· ", "dim"), (c["text"], "text")], [("  $ ", "dim"), (c["verify"], "dim")]]
    return out


def _verify(st, w, h, app):  # each check's command and its output: also one config line away
    out = []
    for e in st.verify[-8:]:
        bad = bool(e.get("exit"))
        out.append([(" FAIL " if bad else " PASS ", "chip_bad" if bad else "chip_ok"), ("  " + (e.get("cmd") or ""), "text")])
        out += [[("   ", "text"), (x, "dim")] for x in str(e.get("output") or "").strip().splitlines()[-4:]]
    return out or [[("not run yet", "dim")]]


def _title(st, name):
    if name == "track":
        return (st.plan.get("title") or st.request or "No run yet"), (
            f"{st.plan.get('type', '')} {st.plan.get('tier', '')}".strip() if st.plan else "")
    if name == "log":
        return "Activity", (f"{len(st.actions)} actions" if st.actions else "")
    if name == "checks" and st.criteria:
        return "Checks", f"{sum(c['state'] == 'pass' for c in st.criteria)}/{len(st.criteria)}"
    if name == "files" and st.stat:
        return "Changed", f"+{sum(a for a, _ in st.stat.values())} −{sum(d for _, d in st.stat.values())}"
    if name == "tokens" and st.calls:
        return "Tokens per call", f"{len(st.calls)} calls"
    if name == "time" and st.first_ts:
        return "Time", duration((st.last_ts or st.first_ts) - st.first_ts)
    return PANELS[name][0], ""


PANELS = {"track": ("Run", _track), "log": ("Activity", _log), "checks": ("Checks", _checks),
          "files": ("Changed", _files), "time": ("Time", _time), "tokens": ("Tokens", _tokens),
          "plan": ("Plan", _plan), "verify": ("Check output", _verify)}


# ---------------------------------------------------------------- render

def human(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.1f}k" if n >= 1e3 else str(n)


STATUS_CHIP = {"running": "chip_accent", "planning": "chip_warn", "fixing": "chip_warn", "closed": "chip_ok",
               "blocked": "chip_bad", "error": "chip_bad", "stopped": "chip_bad"}


def elapsed(st, app):
    if not st.first_ts:
        return ""
    s = int((time.time() if app is not None and app.running() else st.last_ts or st.first_ts) - st.first_ts)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def _header(cv, st, app):
    cv.fill(0, "header")
    x = cv.put(0, 0, " ◆ FOREMAN CODE ", "brand")
    clock = elapsed(st, app)
    right = "   ".join(v for v in (st.worker and f"worker {st.worker}" or st.model or "", clock and f"⏱ {clock}") if v)
    right = f"{right}  " if right else ""
    if st.request:
        cv.line(0, x + 2, [(st.request, "header")], cv.w - len(right) - 2)
    cv.put(0, cv.w - len(right), right, "header_dim")


def _status(cv, st, app):
    y = cv.h - 1
    cv.fill(y, "bar")
    segs = [(f" {st.status.upper()} ", STATUS_CHIP.get(st.status, "chip_todo"))]
    if st.task:
        segs += [("  ", "bar"), (st.task, "bar")]
    if st.steps:
        segs += [("   ", "bar"), (f"step {st.step}/{len(st.steps)}", "bar_dim")]
    if app is not None and app.message:
        segs += [("   ", "bar"), (app.message, "key")]
    hints = [seg for k, word in HINTS for seg in ((f" {k} ", "key"), (f"{word} ", "bar_dim"))]
    hint_w = sum(len(t) for t, _ in hints) + 1
    room = cv.w - hint_w if cv.w - hint_w > 36 else cv.w
    cv.line(y, 0, segs, room)
    if room < cv.w:
        cv.line(y, room, hints, cv.w)


def _draw(name, st, w, h, app):
    try:
        return [[(str(t), str(s)) for t, s in line] for line in PANELS[name][1](st, w, h, app)]
    except Exception as e:  # an extension's panel that fails, or returns something else than lines, says why
        return [[(f"panel {name} failed: {type(e).__name__}: {e}", "bad")]]


def _panel(cv, st, app, cfg, name, y, x, h, w, lines):
    title, note = _title(st, name)
    iy, ix, ih, iw = box(cv, y, x, h, w, title, cfg, app is not None and app.focused() == name, note)
    follow = name == "log" and (app is None or app.follow)
    top = max(0, len(lines) - ih) if follow else min(app.scroll if app else 0, max(0, len(lines) - ih))
    for r, segs in enumerate(lines[top:top + ih]):
        cv.line(iy + r, ix, segs, ix + iw)


def render(st, w, h, cfg, app=None):
    """The whole screen for this state: header, panels per the layout, the status bar, and any open view."""
    cv = Canvas(w, h)
    prompt = app is not None and app.mode == "prompt"
    y0, body_h = 1, h - 2 - (1 if prompt else 0)
    lay = cfg.get("layout") or DEFAULTS["layout"]
    narrow, single = w < int(lay.get("narrow_below", 80)), w < SINGLE_BELOW
    order = []
    for name in [n for n in lay.get("top") or [] if n in PANELS and not single]:  # full-width rows, as tall as they need
        lines = _draw(name, st, w - 4, None, app)
        ph = min(len(lines) + 2, max(3, body_h // 3))
        _panel(cv, st, app, cfg, name, y0, 0, ph, w, lines)
        y0, body_h = y0 + ph, body_h - ph
    columns_ = [["log"]] if single else [lay.get("narrow") or ["log"]] if narrow else lay.get("columns") or [["log"]]
    widths = [100] if len(columns_) == 1 else list(lay.get("widths") or [])
    widths = (widths + [100 // len(columns_)] * len(columns_))[:len(columns_)]
    heights = [lay.get("narrow_heights") or []] if narrow else list(lay.get("heights") or [])
    x = 0
    for ci, col in enumerate(columns_):
        cw = w - x if ci == len(columns_) - 1 else max(12, w * widths[ci] // max(sum(widths), 1))
        names = [n for n in col if n in PANELS] or ["log"]
        weights = ((list(heights[ci]) if ci < len(heights) else []) + [1] * len(names))[:len(names)]
        measured = {n: _draw(n, st, max(1, cw - 4), None, app) for n, wt in zip(names, weights) if wt == "auto"}
        fixed = {n: min(len(lines) + 2, body_h * 45 // 100) for n, lines in measured.items()}
        rest = body_h - sum(fixed.values())
        flex = sum(wt for wt in weights if wt != "auto") or 1
        y = y0
        for pi, name in enumerate(names):
            share = fixed[name] if name in fixed else max(3, rest * weights[pi] // flex)
            ph = y0 + body_h - y if pi == len(names) - 1 else share
            lines = measured.get(name) or _draw(name, st, max(1, cw - 4), max(1, ph - 2), app)
            _panel(cv, st, app, cfg, name, y, x, ph, cw, lines)
            order.append(name)
            y += ph
        x += cw
    if app is not None:
        app.order = order
    _header(cv, st, app)
    _status(cv, st, app)
    if prompt:
        cv.fill(h - 2, "input")
        cv.line(h - 2, 0, [(" request › ", "key"), (app.input, "input"), ("▏", "key")], w)
    if app is not None and app.mode in VIEWS:
        VIEWS[app.mode](cv, st, app, cfg)
    return cv


# ---------------------------------------------------------------- views over the main screen

KEY_NAMES = {"\t": "Tab", "\n": "Enter", "KEY_ENTER": "Enter", "KEY_UP": "↑", "KEY_DOWN": "↓", "KEY_PPAGE": "PgUp",
             "KEY_NPAGE": "PgDn"}
COMMAND_LABELS = [("new", "type a request"), ("stop", "stop the run"), ("resume", "resume it"),
                  ("diff", "the run's changes"), ("history", "past runs"), ("model", "model or worker"),
                  ("thoughts", "the model's own words"), ("focus", "next panel"), ("up", "up"), ("down", "down"),
                  ("expand", "open a line"), ("follow", "follow the latest"), ("help", "keys"), ("quit", "quit")]


def _overlay(cv, cfg, title, note, w=None, h=None):
    """A view's box over the screen; the screen behind it fades so the view stands out."""
    cv.cells = [[(c, "shade") for c, _ in row] for row in cv.cells]
    w, h = min(w or cv.w - 8, cv.w - 2), min(h or cv.h - 4, cv.h - 2)
    y, x = max(1, (cv.h - h) // 2), max(0, (cv.w - w) // 2)
    for r in range(y, y + h):
        cv.put(r, x, " " * w)
    return box(cv, y, x, h, w, title, cfg, focused=True, note=note)


def _help_view(cv, st, app, cfg):
    keys = {}
    for k, cmd in (cfg.get("keys") or {}).items():
        name = KEY_NAMES.get(k) or key_name(k)
        if name not in keys.setdefault(cmd, []):
            keys[cmd].append(name)
    rows = [(" ".join(keys[cmd]), label) for cmd, label in [*COMMAND_LABELS, *app.extra_labels] if keys.get(cmd)]
    iy, ix, ih, iw = _overlay(cv, cfg, "Keys", "any key closes", 46, len(rows) + 4)
    for i, (k, label) in enumerate(rows[:ih - 1]):
        cv.line(iy + 1 + i, ix, [(f"{k:>11}", "warn"), ("   ", "text"), (label, "text")], ix + iw)


def _diff_style(line):
    return ("strong" if line.startswith(("diff --git", "+++", "---")) else "accent" if line.startswith("@@")
            else "ok" if line.startswith("+") else "bad" if line.startswith("-") else "text")


def _diff_view(cv, st, app, cfg):
    iy, ix, ih, iw = _overlay(cv, cfg, "Changes", "q closes")
    lines = app.view_lines or ["no changes"]
    app.view_scroll = max(0, min(app.view_scroll, len(lines) - ih))
    for r, line in enumerate(lines[app.view_scroll:app.view_scroll + ih]):
        cv.line(iy + r, ix, [(line.expandtabs(4), _diff_style(line))], ix + iw)


def _list_view(title, note, row):
    def view(cv, st, app, cfg):
        iy, ix, ih, iw = _overlay(cv, cfg, title, note, 96, min(len(app.items) + 4, cv.h - 4))
        if not app.items:
            cv.line(iy + 1, ix, [("nothing here yet", "dim")], ix + iw)
        first = max(0, app.item_index - ih + 2)
        for r, item in enumerate(app.items[first:first + ih - 1]):
            segs = row(item)
            if first + r == app.item_index:
                segs = [("".join(t for t, _ in segs).ljust(iw), "select")]
            cv.line(iy + 1 + r, ix, segs, ix + iw)
    return view


def _history_row(item):
    chip = {"closed": (" DONE ", "chip_ok"), "blocked": (" STOP ", "chip_bad"), "error": (" STOP ", "chip_bad")}.get(
        item["status"], (" ···· ", "chip_todo"))
    when = time.strftime("%b %d %H:%M", time.localtime(item["ts"])) if item.get("ts") else ""
    return [chip, (f"  {item['task'] or '—':<8}", "strong"), (f"  {when:<12}", "dim"), ("  " + item["request"], "text")]


def _picker_row(item):
    kind, name = item
    return [(" MODEL  " if kind == "model" else " WORKER ", "chip_accent" if kind == "model" else "chip_warn"),
            ("  " + name, "text")]


VIEWS = {"help": _help_view, "diff": _diff_view, "history": _list_view("Past runs", "Enter opens one", _history_row),
         "picker": _list_view("Run the next request with", "Enter picks", _picker_row)}


# ---------------------------------------------------------------- colours and the SVG snapshot

def _rgb(c):
    """A theme colour as (r, g, b): "#rrggbb", or a 256-colour index."""
    if isinstance(c, str) and len(c) == 7 and c.startswith("#"):
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    i = int(c)
    if i < 16:
        base = [(0, 0, 0), (205, 49, 49), (13, 188, 121), (229, 229, 16), (36, 114, 200), (188, 63, 188),
                (17, 168, 205), (229, 229, 229)]
        r, g, b = base[i % 8]
        return (min(255, r + 50), min(255, g + 50), min(255, b + 50)) if i >= 8 else (r, g, b)
    if i < 232:
        lv = [0, 95, 135, 175, 215, 255]
        return lv[(i - 16) // 36], lv[(i - 16) % 36 // 6], lv[(i - 16) % 6]
    return (8 + (i - 232) * 10,) * 3


def to_256(c):
    """The nearest 256-colour index (the 6x6x6 cube or the grey ramp) for a theme colour."""
    if isinstance(c, int):
        return c
    r, g, b = _rgb(c)
    lv = [0, 95, 135, 175, 215, 255]
    near = lambda v: min(range(6), key=lambda i: abs(lv[i] - v))
    cube = 16 + 36 * near(r) + 6 * near(g) + near(b)
    grey = 232 + min(23, max(0, round((sum((r, g, b)) / 3 - 8) / 10)))
    dist = lambda idx: sum((a - b_) ** 2 for a, b_ in zip(_rgb(idx), (r, g, b)))
    return min((cube, grey), key=dist)


def _hex(c):
    return "#%02x%02x%02x" % _rgb(c)


def to_svg(cv, cfg, title="fm code tui"):
    """The canvas as an SVG terminal window: each run of one style is one text element, fitted to its cells."""
    theme = cfg.get("theme") or THEME
    screen = theme.get("screen", {})
    bg, fg = _hex(screen.get("bg", _BG)), _hex(screen.get("fg", _INK))
    cw, ch, pad, chrome = 8.4, 18, 16, 34
    W, H = round(cv.w * cw + 2 * pad), round(cv.h * ch + 2 * pad + chrome)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           '<style>text{font-family:"JetBrains Mono","Cascadia Code","Noto Sans Mono","DejaVu Sans Mono",monospace;'
           'font-size:14px;white-space:pre}</style>',
           f'<rect width="{W}" height="{H}" rx="12" fill="{bg}"/>',
           f'<rect width="{W}" height="{chrome}" rx="12" fill="#0A101A"/><rect y="{chrome - 12}" width="{W}" height="12" fill="#0A101A"/>']
    for i, dot in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        out.append(f'<circle cx="{22 + i * 20}" cy="{chrome / 2}" r="6" fill="{dot}"/>')
    out.append(f'<text x="{W / 2}" y="{chrome / 2 + 5}" text-anchor="middle" fill="#8A98AE">{html.escape(title)}</text>')
    for y, row in enumerate(cv.cells):
        x = 0
        while x < len(row):
            style, end = row[x][1], x
            while end < len(row) and row[end][1] == style:
                end += 1
            spec = theme.get(style) or {}
            s_fg, s_bg = spec.get("fg"), spec.get("bg")
            if spec.get("reverse"):
                s_fg, s_bg = s_bg or screen.get("bg", _BG), s_fg or screen.get("fg", _INK)
            px, py = pad + x * cw, chrome + pad + y * ch
            if s_bg is not None:
                out.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{(end - x) * cw:.1f}" height="{ch}" fill="{_hex(s_bg)}"/>')
            text = "".join(c for c, _ in row[x:end])
            k = 0
            while k < len(text):  # block glyphs as exact rects (one per run), as a terminal fills its cells
                c, j = text[k], k
                while j < len(text) and text[j] == c:
                    j += 1
                if c in BLOCKS:
                    part = (BLOCKS.index(c) + 1) / 8
                    out.append(f'<rect x="{px + k * cw:.1f}" y="{py + ch * (1 - part):.1f}" width="{(j - k) * cw:.1f}" '
                               f'height="{ch * part:.1f}" fill="{_hex(s_fg) if s_fg is not None else fg}"/>')
                k = j
            text = "".join(" " if c in BLOCKS else c for c in text)
            if text.strip():
                attrs = (' font-weight="bold"' if spec.get("bold") else "") + (
                    ' font-style="italic"' if spec.get("italic") else "")
                out.append(f'<text x="{px:.1f}" y="{py + ch * 0.74:.1f}" fill="{_hex(s_fg) if s_fg is not None else fg}"'
                           f' textLength="{(end - x) * cw:.1f}" lengthAdjust="spacingAndGlyphs"{attrs}>'
                           f'{html.escape(text)}</text>')
            x = end
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- the app: keys, commands, views, the child

class App:
    def __init__(self, cfg, spawn=None, root=None, opts=None, diff=None, history=None, choices=None):
        self.cfg, self.state = cfg, State()
        self.mode, self.input, self.message, self.done = "main", "", "", False
        self.spawn = spawn or self._spawn
        self.root, self.opts = root or os.getcwd(), dict(opts or {})
        self.diff_source, self.history_dir = diff or self._git_diff, history
        self.choices_source = choices or self._choices
        self.child, self.events = None, queue.Queue()
        self.order, self.focus, self.scroll, self.follow, self.thoughts = [], 0, 0, True, False
        self.selected, self.expanded = None, set()
        self.view_lines, self.view_scroll, self.items, self.item_index = [], 0, [], 0
        self.extra_labels, self.ext = list(EXT_LABELS), {}
        self.commands = {"quit": self.quit, "new": self.new, "stop": self.stop, "resume": self.resume,
                         "help": self.help, "focus": self.next_focus, "up": lambda: self.move(-1),
                         "down": lambda: self.move(1), "page_up": lambda: self.move(-10),
                         "page_down": lambda: self.move(10), "expand": self.expand, "follow": self.follow_tail,
                         "diff": self.show_diff, "history": self.show_history, "model": self.show_picker,
                         "thoughts": self.toggle_thoughts}
        self.commands.update({name: self._ext_command(name, fn) for name, fn in EXT_COMMANDS.items()})

    def _ext_command(self, name, fn):
        def run():
            try:
                fn(self)
            except Exception as e:  # an extension's bug shows in the status bar; the screen stays up
                self.message = f"{name} failed: {type(e).__name__}: {e}"
        return run

    # -- keys
    def key(self, k):
        if self.mode == "prompt":
            return self._prompt_key(k)
        if self.mode == "help":
            self.mode = "main"
            return None
        if self.mode in ("diff", "history", "picker"):
            return self._view_key(k)
        fn = self.commands.get(self.cfg["keys"].get(k))
        return fn() if fn else None

    def _view_key(self, k):
        cmd = self.cfg["keys"].get(k)
        step = {"up": -1, "down": 1, "page_up": -10, "page_down": 10}.get(cmd)
        if k in ("\x1b", "q") or cmd == {"diff": "diff", "history": "history", "picker": "model"}[self.mode]:
            self.mode = "main"
        elif step and self.mode == "diff":
            self.view_scroll = max(0, self.view_scroll + step)
        elif step:
            self.item_index = max(0, min(len(self.items) - 1, self.item_index + step))
        elif cmd == "expand" and self.items:
            item, self.mode = self.items[self.item_index], "main"
            if isinstance(item, dict):
                self.replay(item["path"])
            else:
                kind, name = item
                self.opts.update(model=name if kind == "model" else None, worker=name if kind == "worker" else None)
                self.message = f"next run: {kind} {name}"

    def _prompt_key(self, k):
        if k in ("\n", "\r", "KEY_ENTER"):
            text, self.mode, self.input = self.input.strip(), "main", ""
            if text:
                self.start([text])
        elif k == "\x1b":
            self.mode, self.input = "main", ""
        elif k in ("KEY_BACKSPACE", "\x7f", "\b"):
            self.input = self.input[:-1]
        elif len(k) == 1 and k.isprintable():
            self.input += k

    def focused(self):
        return self.order[self.focus % len(self.order)] if self.order else None

    # -- commands
    def quit(self):
        self.stop()
        self.done = True

    def new(self):
        if self.running():
            self.message = "a run is going: s stops it"
        else:
            self.mode = "prompt"

    def help(self):
        self.mode = "help"

    def toggle_thoughts(self):
        self.thoughts = not self.thoughts
        self.message = "showing the model's own words" if self.thoughts else ""

    def next_focus(self):
        self.focus, self.scroll = self.focus + 1, 0

    def move(self, n):
        if self.focused() == "log":
            last = len(self.state.log) - 1
            self.selected = max(0, min(last, (last if self.selected is None else self.selected) + n))
            self.follow = self.selected == last
        else:
            self.scroll = max(0, self.scroll + n)

    def expand(self):
        if self.selected is not None:
            self.expanded ^= {self.selected}

    def follow_tail(self):
        self.follow, self.selected = True, None

    def stop(self):
        if self.running():
            try:
                os.killpg(self.child.pid, signal.SIGTERM)
            except (OSError, AttributeError):
                pass
            self.message = "stopped: r resumes"

    def resume(self):
        if self.running() or not self.state.task:
            self.message = "a run is going" if self.state.task else "nothing to resume"
            return
        self.child = self.spawn([], dict(self.opts, resume=self.state.task))

    def show_diff(self):
        try:
            self.view_lines = (self.diff_source() or "").splitlines()
        except (OSError, subprocess.SubprocessError) as e:
            self.view_lines = [f"no diff: {e}"]
        self.view_scroll, self.mode = 0, "diff"

    def show_history(self):
        self.items, self.item_index, self.mode = history(self.history_dir), 0, "history"

    def show_picker(self):
        try:
            self.items = list(self.choices_source())
        except Exception as e:  # a model server that doesn't answer: say so, keep the screen
            self.items, self.message = [], f"no models: {e}"
        self.item_index, self.mode = 0, "picker"

    def replay(self, path):
        st = State()
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        st.apply(json.loads(line))
                    except ValueError:
                        continue
        except OSError as e:
            self.message = f"can't read {path}: {e}"
            return
        self.state, self.selected, self.expanded, self.follow = st, None, set(), True
        self.message = f"viewing {st.task or 'a past run'}"

    def _git_diff(self):
        """The run's changes step by step: each file under the step that first changed it, a new file in full; after
        the close, the commit's. fm code's judge's git, with no external diff or textconv: nothing a worker planted in
        the repo's config runs when d is pressed."""
        import fmcode
        git = lambda *a: os.fsdecode(fmcode._git(self.root, *a).stdout)
        closed = self.state.status == "closed"
        base = ["show", "--format=", "--no-ext-diff", "--no-textconv", "HEAD"] if closed else [
            "diff", "--no-ext-diff", "--no-textconv", "HEAD"]
        groups, seen = [], set()
        for n in sorted(self.state.files):
            new = [f for f in self.state.files[n] if f not in seen]
            seen.update(new)
            groups += [(n, new)] if new else []
        if not groups:
            return git(*base)
        out = []
        for n, files in groups:
            out.append(f"── step {n}: {self.state.steps[n - 1]['text'] if 0 < n <= len(self.state.steps) else ''} ")
            for f in files:
                d = git(*base, "--", f)
                if not d and not closed and os.path.isfile(os.path.join(self.root, f)):  # new, so untracked
                    d = git("diff", "--no-ext-diff", "--no-textconv", "--no-index", "--", os.devnull, f)
                out += d.rstrip("\n").splitlines()
        return "\n".join(out)

    def _choices(self):
        import fmcode
        import fmmodels
        out = [("model", p.get("name")) for p in fmmodels.profiles() if p.get("name")]
        return out + [("worker", w) for w, tpl in fmcode.WORKERS.items() if shutil.which(tpl.split()[0])]

    # -- the child
    def running(self):
        return self.child is not None and getattr(self.child, "poll", lambda: 0)() is None

    def start(self, words, **extra):
        self.state, self.selected, self.expanded, self.follow, self.message = State(), None, set(), True, ""
        self.child = self.spawn(words, dict(self.opts, **extra))

    def _spawn(self, words, opts):
        argv = [sys.executable, FM, "code", *words, "--json"]
        for k, v in opts.items():
            if v not in (None, False, ""):
                argv += [f"--{k.replace('_', '-')}"] + ([] if v is True else [str(v)])
        p = subprocess.Popen(argv, cwd=self.root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True, start_new_session=True)
        threading.Thread(target=self._read, args=(p,), daemon=True).start()
        return p

    def _read(self, p):
        for line in p.stdout:
            try:
                self.events.put(json.loads(line))
            except ValueError:
                continue
        err = p.stderr.read()
        p.wait()
        self.events.put({"event": "exit", "code": p.returncode, "stderr": err[-2000:]})

    def feed(self, e):
        try:
            self.state.apply(e)
        except ValueError as x:
            self.state.status, self.state.error = "error", str(x)
            self.state.note("error", text=str(x))

    def poll(self):
        """Take the events that arrived; whether any did (so the driver redraws)."""
        got = False
        while True:
            try:
                self.feed(self.events.get_nowait())
            except queue.Empty:
                return got
            got = True


def _json_line(raw):
    try:
        e = json.loads(raw)
    except ValueError:
        return None
    return e if isinstance(e, dict) else None


def history(folder):
    """Past runs, newest first: [{path, task, request, status, ts}] from code/<task>.events.jsonl, each read at its
    first line and its last 16 KB, not whole."""
    out = []
    try:
        names = [n for n in os.listdir(folder or "") if n.endswith(".events.jsonl")]
    except OSError:
        return out
    for n in names:
        path = os.path.join(folder, n)
        try:
            with open(path, "rb") as f:
                first = _json_line(f.readline())
                f.seek(max(0, os.fstat(f.fileno()).st_size - 16384))
                tail = f.read().decode("utf-8", "replace").splitlines()
        except OSError:
            continue
        last = next((e for e in map(_json_line, reversed(tail)) if e and e.get("event") in ("closed", "blocked", "error")),
                    None)
        if first:
            out.append({"path": path, "task": n.split(".")[0], "request": str(first.get("request") or ""),
                        "status": (last or {}).get("event", "stopped"), "ts": first.get("ts") or os.path.getmtime(path)})
    return sorted(out, key=lambda x: -(x["ts"] or 0))


# ---------------------------------------------------------------- extensions: Python files in Foreman's home folder

HANDLERS = {}      # an fm code event kind, or "*" → [fn(state, event)]
EXT_COMMANDS = {}  # a command's name → fn(app)
EXT_LABELS = []    # (command, what it does) for the keys view


class API:
    """What an extension's setup(api) gets: three calls, each adding to a registry the TUI reads."""
    version = 1

    def panel(self, name, title, fn):
        """A panel a layout can name: fn(state, width, height, app) → lines, each a list of (text, style)."""
        PANELS[name] = (title, fn)

    def command(self, name, fn, key=None, label=None):
        """A command a key can run: fn(app). key binds it unless that key is taken; label shows in the keys view."""
        EXT_COMMANDS[name] = fn
        if name not in COMMANDS:
            COMMANDS.append(name)
        if label:
            EXT_LABELS.append((name, label))
        for k in (parse_key(key) or []) if key else []:
            DEFAULTS["keys"].setdefault(k, name)

    def on(self, event, fn):
        """fn(state, event) after the state takes each event of this kind ("*": every event)."""
        HANDLERS.setdefault(event, []).append(fn)


def extensions_dir():
    import fmcore
    return os.path.join(fmcore.foreman_home(), "tui")


def load_extensions(folder=None):
    """Run setup(API()) of each *.py in Foreman's home folder's tui/ (a project's files never: they'd run as you).
    [one line per file that failed or was skipped]; the others still load."""
    import importlib.util
    folder = folder or extensions_dir()
    try:
        names = sorted(n for n in os.listdir(folder) if n.endswith(".py"))
    except OSError:
        return []
    errors, uid = [], getattr(os, "getuid", lambda: None)()
    for n in names:
        path = os.path.join(folder, n)
        try:
            st = os.stat(path)
            if (uid is not None and st.st_uid != uid) or st.st_mode & 0o022:
                errors.append(f"{path}: skipped: another user can change it")
                continue
            spec = importlib.util.spec_from_file_location(f"fm_tui_ext_{n[:-3]}", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.setup(API())
        except Exception as e:  # its own bug: one line, and the next extension still loads
            errors.append(f"{path}: {type(e).__name__}: {e}")
    return errors


# ---------------------------------------------------------------- config: tui.toml in Foreman's home folder

COMMANDS = [c for c, _ in COMMAND_LABELS] + ["page_up", "page_down"]  # what a key can run (extensions add theirs)
KEY_ALIASES = {"tab": ["\t"], "enter": ["\n", "KEY_ENTER"], "esc": ["\x1b"], "space": [" "], "up": ["KEY_UP"],
               "down": ["KEY_DOWN"], "left": ["KEY_LEFT"], "right": ["KEY_RIGHT"], "pgup": ["KEY_PPAGE"],
               "pgdn": ["KEY_NPAGE"], "home": ["KEY_HOME"], "end": ["KEY_END"], "backspace": ["KEY_BACKSPACE"]}
STYLE_FIELDS = ("fg", "bg", "bold", "italic", "reverse", "paint")


def config_path():
    import fmcore
    return os.path.join(fmcore.foreman_home(), "tui.toml")


def parse_key(name):
    """A key's name in tui.toml as the keys curses reports: [key, …], or None for a name that isn't a key."""
    low = str(name).lower()
    if low in KEY_ALIASES:
        return KEY_ALIASES[low]
    if len(low) == 6 and low.startswith("ctrl+") and low[5].isalpha():
        return ["^" + low[5].upper()]
    if low[:1] == "f" and low[1:].isdigit() and 1 <= int(low[1:]) <= 12:
        return [f"KEY_F({int(low[1:])})"]
    return [name] if len(name) == 1 and name.isprintable() and name != " " else None


def key_name(k):
    """The reverse: how tui.toml names a key curses reports."""
    alias = next((n for n, ks in KEY_ALIASES.items() if k in ks), None)
    if alias:
        return alias
    if len(k) == 2 and k[0] == "^" and k[1].isalpha():
        return "ctrl+" + k[1].lower()
    return f"f{k[6:-1]}" if k.startswith("KEY_F(") else k


def _colour(v):
    if isinstance(v, str):
        return len(v) == 7 and v[0] == "#" and all(c in "0123456789abcdefABCDEF" for c in v[1:])
    return isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 255


def _style_error(name, spec, theme):
    if name not in theme:
        return f"no such style ({', '.join(theme)})"
    if not isinstance(spec, dict):
        return None if _colour(spec) else f"{spec!r} isn't a colour (#rrggbb or 0-255)"
    for k, v in spec.items():
        if k not in STYLE_FIELDS:
            return f"{k}: not a style field ({', '.join(STYLE_FIELDS[:5])})"
        if k in ("fg", "bg") and not _colour(v):
            return f"{k} = {v!r} isn't a colour (#rrggbb or 0-255)"
        if k not in ("fg", "bg") and not isinstance(v, bool):
            return f"{k} is true or false"
    return None


def _layout_error(k, v, table, cfg):
    names = lambda xs: isinstance(xs, list) and all(isinstance(n, str) for n in xs)
    size = lambda x: x == "auto" or isinstance(x, int) and not isinstance(x, bool) and x > 0
    if k in ("top", "narrow", "columns"):
        cols = v if k == "columns" else [v]
        if not (isinstance(cols, list) and cols and all(names(c) and (c or k != "columns") for c in cols)):
            return "a list of columns, each a list of panel names" if k == "columns" else "a list of panel names"
        unknown = [n for c in cols for n in c if n not in PANELS]
        return f"no panel {unknown[0]!r} (panels: {', '.join(PANELS)})" if unknown else None
    if k == "widths":
        cols = table.get("columns", cfg["layout"]["columns"])
        ok = isinstance(v, list) and len(v) == len(cols) and all(size(x) and x != "auto" for x in v)
        return None if ok else "one whole number above 0 per column"
    if k == "heights":
        ok = isinstance(v, list) and all(isinstance(c, list) and all(size(x) for x in c) for c in v)
        return None if ok else 'a list per column of "auto" or a whole number above 0 per panel'
    if k == "narrow_heights":
        return None if isinstance(v, list) and all(size(x) for x in v) else '"auto" or a whole number above 0 per panel'
    if k == "narrow_below":
        return None if isinstance(v, int) and not isinstance(v, bool) and v >= 0 else "a number of columns"
    return f"not a layout setting ({', '.join(DEFAULTS['layout'])})"


def load_config(path=None):
    """DEFAULTS with the user's tui.toml over them: (config, [one line per bad setting]). A bad setting is skipped, the
    rest apply."""
    import copy
    import tomllib
    cfg = copy.deepcopy(DEFAULTS)
    path = path or config_path()
    try:
        with open(path, "rb") as f:
            user = tomllib.load(f)
    except FileNotFoundError:
        return cfg, []
    except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        return cfg, [f"{path}: {(str(e).splitlines() or [type(e).__name__])[0]}"]
    errors = []
    bad = lambda msg: errors.append(f"{path}: {msg}")
    if "theme" in user:
        if user["theme"] in PRESETS:
            cfg["preset"], cfg["theme"] = user["theme"], PRESETS[user["theme"]]()
        else:
            bad(f"theme = {user['theme']!r}: no such theme ({', '.join(PRESETS)})")
    for key, val in user.items():
        if key == "theme":
            continue
        if key == "border":
            if val in BORDERS:
                cfg["border"] = val
            else:
                bad(f"border = {val!r}: one of {', '.join(BORDERS)}")
        elif key in ("colors", "layout", "keys") and not isinstance(val, dict):
            bad(f"{key}: a [{key}] table")
        elif key == "colors":
            for name, spec in val.items():
                msg = _style_error(name, spec, cfg["theme"])
                if msg:
                    bad(f"colors.{name}: {msg}")
                else:
                    cfg["theme"][name] = spec if isinstance(spec, dict) else {"fg": spec}
        elif key == "layout":
            for k, v in val.items():
                msg = _layout_error(k, v, val, cfg)
                if msg:
                    bad(f"layout.{k}: {msg}")
                else:
                    cfg["layout"][k] = v
        elif key == "keys":
            for name, cmd in val.items():
                keys = parse_key(name)
                if not keys:
                    bad(f"keys.{name}: not a key (a letter, ctrl+x, f1-f12, {', '.join(KEY_ALIASES)})")
                elif cmd != "none" and cmd not in COMMANDS:
                    bad(f"keys.{name} = {cmd!r}: no such command ({', '.join(COMMANDS)}, or none)")
                else:
                    for k in keys:
                        cfg["keys"].pop(k, None) if cmd == "none" else cfg["keys"].__setitem__(k, cmd)
        else:
            bad(f"{key}: not a setting (theme, border, colors, layout, keys)")
    return cfg, errors


def _toml(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(map(_toml, v)) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{_toml_key(k)} = {_toml(x)}" for k, x in v.items()) + " }" if v else "{}"
    return json.dumps(str(v), ensure_ascii=False)  # a JSON string is a TOML basic string


def _toml_key(k):
    return k if k and all(c.isascii() and (c.isalnum() or c in "_-") for c in k) else json.dumps(k, ensure_ascii=False)


def print_config(cfg, path=None):
    """The config as tui.toml text that loads back the same: a starting point to edit."""
    out = [f"# fm code tui's settings{f': {path}' if path else ''}. Delete what you don't change.",
           f"theme = {_toml(cfg.get('preset', 'night'))}  # {', '.join(PRESETS)}; [colors] changes single styles",
           f"border = {_toml(cfg['border'])}  # {', '.join(BORDERS)}", "",
           "[colors]  # a style: a colour (#rrggbb or 0-255), or { fg, bg, bold, italic, reverse }"]
    out += [f"{_toml_key(n)} = {_toml(spec)}" for n, spec in cfg["theme"].items()]
    out += ["", f"[layout]  # panels: {', '.join(PANELS)}"] + [f"{_toml_key(k)} = {_toml(v)}" for k, v in cfg["layout"].items()]
    out += ["", f"[keys]  # a letter, ctrl+x, f1-f12, {', '.join(KEY_ALIASES)}; \"none\" unbinds one"]
    seen = set()
    for k, cmd in cfg["keys"].items():
        if key_name(k) not in seen:
            seen.add(key_name(k))
            out.append(f"{_toml_key(key_name(k))} = {_toml(cmd)}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- drivers

def run_plain(app, out=sys.stdout):
    """--plain: each new Activity line as text, the model's own words included; the run's exit status."""
    while True:
        e = app.events.get()
        seen = len(app.state.log)
        app.feed(e)
        for entry in app.state.log[seen:] if len(app.state.log) >= seen else app.state.log:
            print(entry_text(entry), file=out, flush=True)
        if e.get("event") == "exit":
            return 0 if app.state.status == "closed" else 1


def _attrs(curses, cfg):
    """{style: curses attr}: theme colours as 256-colour indexes (the 8 basic ones on a smaller terminal), none on
    NO_COLOR; the screen style's background stays the terminal's own."""
    out, pairs = {}, {}
    color = curses.has_colors() and not os.environ.get("NO_COLOR")
    if color:
        curses.use_default_colors()
    small = color and curses.COLORS < 256
    pick = (lambda c: -1 if c is None else min(range(8), key=lambda i: sum((a - b) ** 2 for a, b in zip(_rgb(i), _rgb(c)))))\
        if small else (lambda c: -1 if c is None else to_256(c))
    theme = cfg.get("theme") or THEME
    screen = theme.get("screen") or {}
    base = (screen.get("fg"), screen.get("bg")) if screen.get("paint") else (None, None)
    for name, spec in theme.items():
        a = (curses.A_BOLD if spec.get("bold") else 0) | (curses.A_REVERSE if spec.get("reverse") else 0)
        a |= getattr(curses, "A_ITALIC", 0) if spec.get("italic") else 0
        if color and name != "screen" and ("fg" in spec or "bg" in spec or base[1] is not None):
            key = (pick(spec.get("fg", base[0])), pick(spec.get("bg", base[1])))
            if key not in pairs and len(pairs) < curses.COLOR_PAIRS - 1:
                curses.init_pair(len(pairs) + 1, *key)
                pairs[key] = len(pairs) + 1
            a |= curses.color_pair(pairs.get(key, 0))
        elif not color and (name.startswith(("bar", "chip")) or name in ("select", "brand", "key", "input")):
            a |= curses.A_REVERSE
        out[name] = a
    return out


def _paint(scr, cv, attrs):
    for y, row in enumerate(cv.cells):
        x = 0
        while x < len(row):
            style, end = row[x][1], x
            while end < len(row) and row[end][1] == style:
                end += 1
            try:
                scr.addstr(y, x, "".join(c for c, _ in row[x:end]), attrs.get(style, 0))
            except Exception:  # curses refuses the bottom-right cell; the rest is drawn
                pass
            x = end
    scr.refresh()


def key_of(k):
    """A key as tui.toml names it: get_wch gives a control key as its character (Ctrl-R is \\x12), so ^R; Enter's
    \\r is \\n."""
    if k == "\r":
        return "\n"
    if len(k) == 1 and ord(k) < 32 and k not in "\t\n\x1b\b":
        return "^" + chr(ord(k) + 64)
    return k


def run_screen(app, wrapper=None):
    """The curses screen until q. Whatever ends it (q, Ctrl-C, a crash, a closed terminal) stops the run first: fm
    code runs in its own session and would carry on into a closed pipe."""
    def hangup(*_):
        raise SystemExit(129)
    try:
        old = signal.signal(signal.SIGHUP, hangup)
    except (ValueError, AttributeError):  # not the main thread, or no SIGHUP here
        old = None
    try:
        if wrapper is None:
            import curses
            wrapper = curses.wrapper
        wrapper(lambda scr: _loop(scr, app))
    finally:
        app.stop()
        if old is not None:
            signal.signal(signal.SIGHUP, old)


def _loop(scr, app):
    import curses
    curses.curs_set(0)
    scr.timeout(250)
    attrs = _attrs(curses, app.cfg)
    while not app.done:
        app.poll()
        h, w = scr.getmaxyx()
        scr.erase()
        _paint(scr, render(app.state, w, h, app.cfg, app), attrs)  # every tick, so the clock moves during a run
        try:
            k = scr.get_wch()
        except curses.error:
            continue
        if k != curses.KEY_RESIZE:
            app.key(curses.keyname(k).decode() if isinstance(k, int) else key_of(k))


def snapshot(events, path, size=(120, 34), cfg=None, mode="main"):
    """The screen after these events, as an SVG at path (README pictures, the site, a bug report)."""
    cfg = cfg or DEFAULTS
    app = App(cfg, spawn=lambda *a, **k: None)
    for e in events:
        app.feed(e)
    app.mode = mode
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_svg(render(app.state, size[0], size[1], cfg, app), cfg))
    return path


def main(args, words):
    """fm code tui [REQUEST…] [--plain] [--model M | --worker CLI] [--verify CMD] [--resume [ID]] [--print-config]
    [--snapshot FILE --events FILE]. A bad setting or extension is said once and skipped; --print-config exits 2."""
    ext_errors = load_extensions()
    cfg, errors = load_config()
    problems = [f"extension {e}" for e in ext_errors] + errors
    if getattr(args, "print_config", False):
        print(print_config(cfg, config_path()), end="")
    for e in problems:
        print(f"fm code tui: {e}", file=sys.stderr)
    if getattr(args, "print_config", False):
        return 2 if errors else 0
    if getattr(args, "snapshot", None):
        src = getattr(args, "events", None)
        if not src:
            print("fm code tui --snapshot needs --events FILE (fm code … --json > FILE records one)", file=sys.stderr)
            return 2
        with open(src, encoding="utf-8") as f:
            events = [json.loads(line) for line in f if line.strip()]
        w, _, h = (getattr(args, "size", None) or "120x34").partition("x")
        print(snapshot(events, args.snapshot, (int(w), int(h)), cfg))
        return 0
    import fmcli
    p = fmcli.resolve(args)  # -p, like fm code itself; the child runs in the project's root
    opts = {k: getattr(args, k, None) for k in ("model", "worker", "verify", "escalate", "max_steps", "no_commit",
                                                 "worker_timeout", "dry_plan")}
    app = App(cfg, root=os.path.realpath(p.root), opts=opts, history=os.path.join(p.dir, "code"))
    resume = getattr(args, "resume", None)
    first = (lambda: app.start([], resume=resume or True)) if resume is not None else (
        lambda: app.start([" ".join(words)])) if words else None
    if getattr(args, "plain", False) or not sys.stdout.isatty():
        if not first:
            print('fm code tui --plain needs a request: fm code tui --plain "fix the login bug"', file=sys.stderr)
            return 2
        first()
        return run_plain(app)
    if problems:
        app.message = f"{len(problems)} setting(s) skipped: {problems[0]}"
    if first:
        first()
    run_screen(app)
    return 0
