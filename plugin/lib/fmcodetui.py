"""T-1283: Foreman Code's terminal UI (`fm code tui`). It runs fm code as a child with --json and draws only from that
event stream (fmcode.EVENTS), so the harness stays the source of truth: the TUI never edits, verifies or closes.

Layers, each testable without a terminal: State (events → what happened); Canvas and the panels (a grid of styled
cells); render (state + config + time → a canvas); App (keys → commands, views, the child process). main() runs the
screen through fmcodetui's own ANSI renderer (fmcodeterm; no curses)
driver, --plain its line-by-line twin and --snapshot an SVG of the screen. Pictures over prose: a station track, check
chips, change bars and a token chart; the model's own words are one key away. Themes, layout and keys are config;
panels and commands are registries extensions add to. Stdlib only."""
import functools
import html
import json
import math
import os
import queue
import shutil
import signal
import subprocess
import sys
import threading
import time
import unicodedata

from fmcodeterm import PASTE_CAP, Term, colour_depth, parse_keys, session, split_tail  # noqa: E402 (T-1300)

SCHEMA = 1  # the fm code event stream this reader knows (fmcode.SCHEMA)
FM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "fm")

# Themes come from a palette of a few colours. A colour is "#rrggbb" or a 0-255 index; the driver maps hex to the
# terminal's 256 colours (8 on a small terminal), NO_COLOR drops them, and the SVG snapshot uses them as they are.
PALETTES = {
    "night": {"bg": "#0D1420", "bar": "#1B2638", "head": "#131C2B", "ink": "#E7ECF4", "dim": "#8A98AE",
              "said": "#9AA8BC", "accent": "#86A8FF", "ok": "#47C98B", "bad": "#FF6B6B", "warn": "#FFC83D",
              "edge": "#33445F", "track": "#2E3D58", "shade": "#2A3650", "barink": "#C9D3E3",
              "accent2": "#C792FF", "ok2": "#B8F26B", "bad2": "#FFA26B", "glow": "#FFFFFF", "panel": "#111B2B"},
    "paper": {"bg": "#F6F7F9", "bar": "#E1E6EE", "head": "#E9EDF3", "ink": "#1B2330", "dim": "#5E6B7E",
              "said": "#4F5B6C", "accent": "#2F54C9", "ok": "#12805C", "bad": "#C42B2B", "warn": "#9A6200",
              "edge": "#C3CCD9", "track": "#CDD5E1", "shade": "#C9D1DD", "barink": "#2B3442", "paint": True,
              "accent2": "#8B3FD1", "ok2": "#4E9F1D", "bad2": "#C2571A", "glow": "#FFFFFF", "panel": "#FFFFFF"},
}
# signal: night with pass blue and fail orange, told apart with red-green colour blindness (T-1300)
PALETTES["signal"] = dict(PALETTES["night"], ok="#4DA3FF", ok2="#9AD4FF", bad="#FF8A1F", bad2="#FFC46B",
                          warn="#F2D544", accent="#C4A8FF", accent2="#FF8FD8")
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
            "chip_todo": {"fg": p["dim"], "bg": p["bar"]}, "accent2": {"fg": p["accent2"]}, "ok2": {"fg": p["ok2"]},
            "bad2": {"fg": p["bad2"]}, "glow": {"fg": p["glow"]}, "panel": {"bg": p["panel"]}}


def _mono():
    """No colours: what had a background is reversed, the rest keeps its weight."""
    return {n: dict({k: v for k, v in spec.items() if k in ("bold", "italic")}, **({"reverse": True} if "bg" in spec
                                                                                   and n != "screen" else {}))
            for n, spec in _theme(PALETTES["night"]).items()}


PRESETS = {"night": lambda: _theme(PALETTES["night"]), "paper": lambda: _theme(PALETTES["paper"]),
           "signal": lambda: _theme(PALETTES["signal"]), "mono": _mono}
THEME = PRESETS["night"]()
BORDERS = {"rounded": "╭╮╰╯─│", "square": "┌┐└┘─│", "heavy": "┏┓┗┛━┃", "double": "╔╗╚╝═║", "ascii": "++++-|"}
DEFAULTS = {
    "preset": "night",
    "motion": "full",
    "theme": THEME,
    "border": "rounded",
    "layout": {"top": ["track"], "columns": [["log"], ["checks", "files", "time", "tokens"]], "widths": [58, 42],
               "heights": [[1], ["auto", "auto", "auto", 1]], "narrow": ["checks", "log"],
               "narrow_heights": ["auto", 1], "narrow_below": 80},
    "keys": {"q": "quit", "n": "new", "s": "stop", "r": "resume", "?": "help", "d": "diff", "h": "history",
             "m": "model", "t": "thoughts", "\t": "focus", "KEY_UP": "up", "KEY_DOWN": "down", "k": "up", "j": "down",
             "\n": "expand", "KEY_ENTER": "expand", "KEY_PPAGE": "page_up", "KEY_NPAGE": "page_down", "G": "follow",
             "p": "projects"},
}
HINTS = [("n", "new"), ("p", "projects"), ("d", "diff"), ("h", "history"), ("t", "thoughts"), ("?", "keys"),
         ("q", "quit")]
CHIP = {"done": (" ✓ ", "chip_ok"), "now": (" ● ", "chip_accent"), "todo": ("   ", "chip_todo"),
        "fail": (" ✖ ", "chip_bad")}
NODE = {"done": ("●", "ok"), "now": ("◉", "accent"), "todo": ("○", "track"), "fail": ("✖", "bad")}
LINK = {"done": ("━", "ok"), "now": ("━", "accent"), "fail": ("━", "bad"), "todo": ("─", "track")}
BLOCKS = "▁▂▃▄▅▆▇█"
SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
MOTIONS = ("full", "reduced", "off")
LOG_HIDES = ("plan", "task", "before")  # the track and Checks show these; --plain prints them
SINGLE_BELOW = 60  # columns: a terminal narrower than this shows the activity log alone


# ---------------------------------------------------------------- state: what the events say happened

class NewerStream(ValueError):
    """A stream from a newer fm code: said on the screen, not skipped like a malformed event."""


class State:
    def __init__(self):
        self.request = self.task = self.model = self.worker = self.error = None
        self.plan, self.criteria, self.steps, self.step = {}, [], [], 0
        self.actions, self.log, self.verify, self.files, self.stat = [], [], [], {}, {}
        self.tokens, self.calls, self.status, self.closed = [0, 0], [], "idle", ""
        self.first_ts = self.last_ts = None
        self.heard = None  # T-1336: seconds a quiet CLI turn has printed nothing, from its last working or stalled event
        self.marks = {}  # when each step (1, 2, …) and the final checks ("checks") began
        self.ext = {}  # extensions' own data for this run

    def apply(self, e):
        """Take one event; an unknown or malformed one changes nothing (a newer fm code may send more)."""
        kind = e.get("event") if isinstance(e, dict) else None
        fn = getattr(self, f"_on_{kind}", None) if isinstance(kind, str) and kind.isidentifier() else None
        if fn:
            ts = e.get("ts")
            if "ts" in e and not (isinstance(ts, (int, float)) and not isinstance(ts, bool) and math.isfinite(ts)):
                e = {k: v for k, v in e.items() if k != "ts"}  # T-1306: a time that isn't a finite number isn't one
            # T-1306: a handler that trips on a bad field leaves the state as it was. One level of copies covers the
            # handlers here: each validates before it changes anything nested. ponytail: the copy grows with the log
            # (quadratic over a run); fine at hundreds of events, validate per handler if runs reach tens of thousands.
            before = {k: v.copy() if isinstance(v, (list, dict)) else v for k, v in vars(self).items()}
            try:
                fn(e)
            except Exception as x:
                vars(self).clear()
                vars(self).update(before)
                if isinstance(x, NewerStream):
                    raise
                return self
            if "ts" in e:
                self.first_ts = self.first_ts or e["ts"]
                self.last_ts = e["ts"]
        for h in (HANDLERS.get(kind, []) + HANDLERS.get("*", [])) if isinstance(kind, str) else []:
            t0, why = time.monotonic(), None
            try:
                h(self, e)
            except Exception as x:  # an extension's handler that throws is said once and dropped
                why = f"{type(x).__name__}: {x}; switched off"
            took = time.monotonic() - t0
            if why is None and took > HANDLER_BUDGET:  # T-1315: one over its budget too
                why = f"handler {getattr(h, '__qualname__', '?')} took {took * 1000:.0f} ms; switched off"
            if why:
                for hs in HANDLERS.values():
                    if h in hs:
                        hs.remove(h)
                self.note("error", text=f"extension {getattr(h, '__module__', '?')}: {why}")
        return self

    def note(self, kind, **fields):
        if self.log and self.log[-1].get("kind") == "working":  # T-1329: the ticking line goes at the next one
            self.log.pop()
        self.log.append(dict(fields, kind=kind))
        self.heard = None  # anything else said: the CLI was heard, or the turn is over

    def _on_start(self, e):
        if int(e.get("schema") or 1) > SCHEMA:
            raise NewerStream(f"fm code's event stream is schema {e.get('schema')}; this TUI reads {SCHEMA}: update Foreman")
        if e.get("resume") and self.plan:  # fm code --resume sends no plan again: the screen keeps the run's
            self.task, self.status = e.get("task") or self.task, "running"
            return
        self.__init__()
        self.request, self.model, self.worker = (None if e.get(k) is None else str(e[k])  # the header joins them
                                                 for k in ("request", "model", "worker"))
        self.task = e.get("task")
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
            self.stat = {str(k): v for k, v in e["stat"].items() if isinstance(v, list) and len(v) == 2
                         and all(type(n) is int for n in v)}  # the Changed title sums them

    def _on_closed(self, e):
        if isinstance(e.get("tokens"), list) and len(e["tokens"]) == 2:  # first: a bad count changes nothing
            self.tokens = [int(e["tokens"][0] or 0), int(e["tokens"][1] or 0)]
        self.status, self.closed = "closed", e.get("text", "")
        for s in self.steps:
            s["state"] = "done"
        self.note("closed", text=e.get("text", ""))

    def _on_note(self, e):  # T-1328: which runner the run uses and why, or a caution about it
        self.note("note", text=str(e.get("text", "")))

    def _on_tool(self, e):  # T-1329: a worker or planner CLI's tool use, as it happens
        self.note("tool", action=str(e.get("action") or ""), text=str(e.get("target") or ""))

    def _on_working(self, e):  # T-1329: a quiet CLI turn's heartbeat, one line that ticks
        self.note("working", text=str(e.get("text") or "working"))
        self.heard = _secs(e.get("silent"))

    def _on_stalled(self, e):  # T-1336: a CLI turn silent past FM_STALL, with its likely cause: a warning that stays
        self.note("stalled", text=str(e.get("text") or "stalled"))
        self.heard = _secs(e.get("secs"))

    def _on_answer(self, e):  # T-1320: a question answered: no task, nothing changed
        self.status = "answered"
        for line in str(e.get("text", "")).splitlines() or [""]:
            self.note("answer", text=line)

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


def _secs(v):
    """A count of seconds from an event, or None for anything else (a bool, a string, NaN, a negative)."""
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v >= 0 else None


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
        self.bg = [[None] * self.w for _ in range(self.h)]  # the colour under a cell with no background of its own

    def tint(self, y, x, h, w, colour):
        for r in range(max(0, y), min(self.h, y + h)):
            for c in range(max(0, x), min(self.w, x + w)):
                self.bg[r][c] = colour

    def put(self, y, x, s, style="text", right=None):
        """s at (y, x), clipped at `right` (exclusive) or the edge; the column after it."""
        if not 0 <= y < self.h:
            return x
        end, last = min(self.w, right if right is not None else self.w), None
        for ch in str(s):
            if unicodedata.combining(ch):  # an accent joins the letter before it, in the same cell
                if last is not None:
                    self.cells[y][last] = (self.cells[y][last][0] + ch, style)
                continue
            wide = unicodedata.east_asian_width(ch) in "WF"
            if x + wide >= end:
                if x < end and x >= 0:
                    self.cells[y][x] = (" ", style)  # half a wide character doesn't fit: a space
                break
            if x >= 0:
                self.cells[y][x], last = (ch if ch.isprintable() else " ", style), x
                if wide:  # it fills two columns: the second is an empty cell, so the row stays w columns
                    self.cells[y][x + 1] = ("", style)
            x += 1 + wide
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


def _cells(ch):
    """The columns ch fills, by the rule put draws by: an accent none, a wide (CJK, emoji) character two.
    ponytail: an emoji ZWJ sequence counts by its parts; wcwidth-style tables if that ever matters."""
    return 0 if unicodedata.combining(ch) else 2 if unicodedata.east_asian_width(ch) in "WF" else 1


def width(s):
    """The columns s fills on a terminal."""
    return sum(map(_cells, str(s)))


def _take(chars, n):
    """The longest run from the front of chars that fills at most n columns."""
    out, used = [], 0
    for ch in chars:
        used += _cells(ch)
        if used > n:
            break
        out.append(ch)
    return out


def pad(s, n):
    """s padded with spaces to n columns (an f-string's :<n counts characters, not columns)."""
    s = str(s)
    return s + " " * max(0, n - width(s))


def fit(s, n, strip=True):
    s = " ".join(str(s).split()) if strip else str(s).replace("\n", " ")
    if len(_take(s, n)) == len(s):  # _take stops at n columns, so a huge log line costs no more than a short one
        return s
    return "".join(_take(s, n - 1)) + "…" if n > 0 else ""


def tail(s, n):
    """A path in n columns, keeping its end (the file name)."""
    if len(_take(reversed(s), n)) == len(s):
        return s
    end = "".join(reversed(_take(reversed(s), n - 1 if n > 1 else max(n, 0))))
    end = end.lstrip("".join(c for c in end if unicodedata.combining(c)))  # an accent whose letter was cut
    return "…" + end if n > 1 else end


def wrap(s, n, lines=2):
    """s in at most `lines` lines of n columns, broken at spaces; the last one ends in … when it's cut."""
    out, cur = [], ""
    for word in " ".join(str(s).split()).split(" "):
        if cur and width(cur) + 1 + width(word) > n:
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
    fx = current()
    edge = "border" if not focused else rgb(fg=mix(col(cfg, "border"), col(cfg, "accent"), 0.55 + 0.45 * fx.wave(2.4)),
                                            bold=True) if fx.moving else "accent"
    if h < 2 or w < 4:
        return y, x, 0, 0
    cv.tint(y, x, h, w, col(cfg, "panel", "bg"))
    cv.put(y, x, tl + hz * (w - 2) + tr, edge)
    for r in range(y + 1, y + h - 1):
        cv.put(r, x, vt, edge)
        cv.put(r, x + w - 1, vt, edge)
    cv.put(y + h - 1, x, bl + hz * (w - 2) + br, edge)
    if title and w > 8:
        end = cv.put(y, x + 2, f" {fit(title, min(w - 8, max(4, w - 8 - (width(note) + 2 if note else 0))))} ", "title")
        if note and end + width(note) + 3 < x + w:  # the title keeps 4 columns at least; the note goes if it doesn't fit
            cv.put(y, x + w - width(note) - 4, f" {note} ", "dim")
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


# ---------------------------------------------------------------- colour and motion (T-1300)

def rgb(fg=None, bg=None, bold=False, italic=False):
    """A computed style: colours worked out for this cell at this instant (a gradient, a pulse, a fade)."""
    return ("rgb", fg, bg, bold, italic)


def resolve(style, cfg, cell_bg=None):
    """{fg, bg, bold, italic, reverse} for a cell: a theme style by name, or a computed one; a cell with no
    background of its own sits on its panel's tint (cell_bg)."""
    if isinstance(style, tuple) and style[:1] == ("rgb",):
        _, fg, bg, bold, italic = style
        spec = {k: v for k, v in (("fg", fg), ("bg", bg), ("bold", bold), ("italic", italic)) if v not in (None, False)}
    else:
        spec = dict(((cfg or {}).get("theme") or THEME).get(style) or {})
    if "bg" not in spec and cell_bg is not None and not spec.get("reverse"):
        spec["bg"] = cell_bg
    return spec


def col(cfg, name, key="fg"):
    return (((cfg or {}).get("theme") or THEME).get(name) or {}).get(key)


def mix(a, b, k):
    """Colour a → b by k (0..1); with one of them missing (mono, NO_COLOR) the other, or None."""
    if a is None or b is None:
        return a if b is None else b
    ka, kb, k = _rgb(a), _rgb(b), max(0.0, min(1.0, k))
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * k) for x, y in zip(ka, kb))


def ease_out(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


class Motion:
    """What render needs to animate, kept across frames: when each watched value changed, and from what. A value
    already there in the first frame is no change (opening a finished run shows it as it is); one first seen later
    is new (a fresh activity line fades in, a new number rolls up from 0)."""

    def __init__(self):
        self.seen, self.frames, self.last_change = {}, 0, -1e9

    def since(self, key, value, t):
        """Seconds since key's value became `value` (inf when it already was in the first frame)."""
        rec = self.seen.get(("s", key))
        if rec is None or rec[0] != value:
            rec = (value, None if rec is None and self.frames <= 1 else t)
            self.seen[("s", key)] = rec
            if rec[1] is not None:
                self.last_change = max(self.last_change, t)
        return float("inf") if rec[1] is None else max(0.0, t - rec[1])

    def eased(self, key, value, t, dur=0.7):
        """value as shown at t: it rolls from what was shown before to the new value over dur seconds."""
        rec = self.seen.get(("e", key))
        if rec is None:
            rec = (value, value, None) if self.frames <= 1 else (value, 0, t)
        elif rec[0] != value:
            rec = (value, self._at(rec, t, dur), t)
        self.seen[("e", key)] = rec
        if rec[2] is not None and t - rec[2] < dur:
            self.last_change = max(self.last_change, t)
        return self._at(rec, t, dur)

    @staticmethod
    def _at(rec, t, dur):
        target, frm, t0 = rec
        return target if t0 is None else frm + (target - frm) * ease_out((t - t0) / dur)

    def busy(self, t, window=1.6):
        return t - self.last_change < window


class FX:
    """One frame's motion: its time, the setting (full: everything moves; reduced: colours change, nothing moves;
    off: still) and the theme's colours. A frame drawn without an App (a snapshot, a test) is still."""

    def __init__(self, cfg=None, app=None, t=0.0):
        self.cfg, self.t = cfg or DEFAULTS, t
        mode = self.cfg.get("motion", "full") if app is not None else "off"
        self.motion = app.motion if app is not None else None
        # a theme with no colours (mono) can't flash or fade: its chips keep their reverse; things still turn
        self.moving, self.colour = mode == "full", mode in ("full", "reduced") and col(self.cfg, "accent") is not None

    def since(self, key, value):
        return self.motion.since(key, value, self.t) if self.colour else float("inf")

    def ease(self, key, value, dur=0.7):
        return self.motion.eased(key, value, self.t, dur) if self.moving else value

    def wave(self, period):
        """0..1, a slow sine: what breathes and pulses."""
        return (math.sin(self.t * 2 * math.pi / period) + 1) / 2 if self.moving else 0.5

    def c(self, name, key="fg"):
        return col(self.cfg, name, key)

    def spin(self):
        return SPIN[int(self.t * 10) % len(SPIN)]


_FX = FX()


def current():
    """The frame being drawn (render sets it): panels and extensions ask it for time and colour."""
    return _FX


def faded(style, k, cfg, under):
    """style's colours brought in from the panel's tint (k 0) to themselves (k 1): a line arriving."""
    spec = resolve(style, cfg)
    fg = spec.get("fg") or col(cfg, "screen")
    return rgb(fg=mix(under, fg, k), bg=spec.get("bg") and mix(under, spec["bg"], k), bold=spec.get("bold", False),
               italic=spec.get("italic", False))


LIVE = ("planning", "running", "fixing")


def _waiting(st, text):
    """An empty panel's words: still when idle; during a run a light passes over them, as a skeleton shimmers."""
    fx = current()
    if st.status not in LIVE or not fx.moving:
        return [[(text, "dim")]]
    dim, ink, d0 = fx.c("dim"), fx.c("screen"), (fx.t * 18) % (len(text) + 12)
    return [_segments([(ch, rgb(fg=mix(dim, ink, 0.8 * (1 - (d0 - i) / 6) if 0 <= d0 - i < 6 else 0)))
                       for i, ch in enumerate(text)])]


def _focus_line(segs, w, band, cfg):
    """segs on the band that marks the line being worked now; chips keep their own colours."""
    out = []
    for t, style in segs:
        spec = resolve(style, cfg)
        out.append((t, style if spec.get("bg") or spec.get("reverse") else rgb(
            fg=spec.get("fg") or col(cfg, "screen"), bg=band, bold=spec.get("bold", False),
            italic=spec.get("italic", False))))
    return out + [(" " * max(0, w - sum(len(t) for t, _ in segs)), rgb(bg=band))]


# ---------------------------------------------------------------- panels: (state, width, height, app) → lines
# Each panel returns lines of (text, style) segments. height is None when the layout measures it (an "auto"
# panel), or the inner rows a stretching panel has to fill.

def _track(st, w, h, app):
    """The run as a line of stations (✓ done, the one being worked, an empty slot to come, ✖ failed), each labelled
    under it; a long plan on a narrow screen gets one-cell nodes. In motion: the station being worked pulses and its
    spinner turns, a light runs along the link into it, done links are a gradient, and a close sends a wave along."""
    fx = current()
    nodes = stations(st)
    n = len(nodes)
    big = (w - 3) / (n - 1) >= 7
    marks = CHIP if big else NODE
    cw = 3 if big else 1
    xs = [round(i * (w - cw) / (n - 1)) for i in range(n)]
    rows = [[(" ", "text")] * w for _ in range(3)]
    ok, ok2, accent, glow, track = fx.c("ok"), fx.c("ok2"), fx.c("accent"), fx.c("glow"), fx.c("track")
    for i, (_, _, state) in enumerate(nodes):
        glyph, style = marks[state]
        if state == "now" and fx.moving:
            glyph = f" {fx.spin()} " if big else fx.spin()
            if fx.colour:
                style = rgb(fg=col(fx.cfg, "chip_accent"), bg=mix(accent, glow, 0.1 + 0.4 * fx.wave(1.7)), bold=True) \
                    if big else rgb(fg=mix(accent, glow, 0.5 * fx.wave(1.7)), bold=True)
        for k, ch in enumerate(glyph):
            rows[0][xs[i] + k] = (ch, style)
        if i < n - 1:
            span = list(range(xs[i] + cw + (1 if big else 0), xs[i + 1] - (1 if big else 0)))
            into = nodes[i + 1][2]
            for j, x in enumerate(span):
                ch, style = LINK[into]
                if into == "done":
                    style = rgb(fg=mix(ok, ok2, (x / max(1, w - 1))))
                elif into == "now" and fx.moving:  # a light running toward the station being worked
                    d = (fx.t * 22) % (len(span) + 10) - j
                    style = rgb(fg=mix(mix(track, accent, 0.6), glow, (1 - d / 8) if 0 <= d < 8 else 0), bold=True)
                rows[0][x] = (ch, style)
    wave = fx.since("track:status", st.status)
    if st.status == "closed" and fx.moving and wave < 1.8:  # done: a bright wave runs the length of the track
        p = wave / 1.3 * (w + 16) - 8
        for x, (ch, style) in enumerate(rows[0]):
            k = max(0.0, 1 - abs(x - p) / 7)
            if k and ch != " ":
                spec = resolve(style, fx.cfg)
                rows[0][x] = (ch, rgb(fg=mix(spec.get("fg"), glow, 0.9 * k), bg=spec.get("bg") and mix(
                    spec["bg"], glow, 0.5 * k), bold=True))
    gap = (w - cw) // (n - 1)
    for r in (1, 2):
        last = fit(nodes[-1][r - 1], max(1, gap - 1))
        starts = xs[:-1] + [w - width(last)]
        for i, node in enumerate(nodes):
            room = width(last) if i == n - 1 else starts[i + 1] - starts[i] - 1
            if room < 4 and node[2] not in ("now", "fail"):
                continue
            style = {"now": "accent", "done": "text", "fail": "bad"}.get(node[2], "dim") if r == 1 else "dim"
            text = node[r - 1] if r == 1 or width(node[r - 1]) <= room else node[r - 1].split("  ")[-1]  # time first
            x = starts[i]
            for ch in fit(text, max(room, 4)):  # a wide glyph fills two cells: the second is empty, as Canvas.put does
                cw_ = width(ch)
                if x + cw_ > w:
                    break
                if cw_:
                    rows[r][x] = (ch, style)
                    if cw_ == 2:
                        rows[r][x + 1] = ("", style)
                elif x:
                    rows[r][x - 1] = (rows[r][x - 1][0] + ch, style)
                x += cw_
    return [_segments(r) for r in rows]


def _checks(st, w, h, app):
    """Each criterion as a chip and its words; a chip that just changed flashes bright and settles."""
    if not st.criteria:
        return _waiting(st, "checks come with the plan")
    fx, out = current(), []
    for i, c in enumerate(st.criteria):
        text, name = (" PASS ", "chip_ok") if c["state"] == "pass" else (" RED  ", "chip_warn") if c.get("first") \
            else (" FAIL ", "chip_bad") if c["state"] == "fail" else (" ···· ", "chip_todo")
        since = fx.since(f"check:{i}", (c["state"], bool(c.get("first"))))
        style = name if since >= 1.1 else rgb(fg=col(fx.cfg, name), bg=mix(fx.c("glow"), col(fx.cfg, name, "bg"),
                                                                        ease_out(since / 1.1)), bold=True)
        first, *more = wrap(c["text"], max(8, w - 8))
        out.append([(text, style), ("  ", "text"), (first, "text")])
        out += [[("        ", "text"), (line, "text")] for line in more]
    return out


def _files(st, w, h, app):
    """Each changed file's added and removed lines as a bar (a gradient), longest first; bars and numbers grow."""
    stat = st.stat or {f: [0, 0] for fs in st.files.values() for f in fs}
    if not stat:
        return _waiting(st, "nothing changed yet")
    fx = current()
    rows = sorted(stat.items(), key=lambda kv: (-(kv[1][0] + kv[1][1]), kv[0]))
    top = max(1, max(a + d for _, (a, d) in rows))
    nums = max(len(f" +{a} −{d}") for _, (a, d) in rows)
    nw = max(6, min(max(width(p) for p, _ in rows), w - nums - 8))
    bw = max(2, w - nw - nums - 1)
    ok, ok2, bad, bad2 = fx.c("ok"), fx.c("ok2"), fx.c("bad"), fx.c("bad2")
    out = []
    for path, (a, d) in rows:
        plus = round(fx.ease(f"bar+:{path}", max(1 if a else 0, round(a * bw / top))))
        minus = round(fx.ease(f"bar-:{path}", max(1 if d else 0, min(bw - plus, round(d * bw / top)))))
        bar = [("▆", rgb(fg=mix(ok, ok2, j / max(1, bw - 1)))) for j in range(plus)] + \
              [("▆", rgb(fg=mix(bad, bad2, j / max(1, bw - 1)))) for j in range(minus)]
        shown_a, shown_d = round(fx.ease(f"n+:{path}", a)), round(fx.ease(f"n-:{path}", d))
        heat = fx.since(f"heat:{path}", (a, d))  # a file that just changed glows, then cools to plain text
        name = "text" if heat >= 3 or not fx.colour else rgb(fg=mix(fx.c("glow"), fx.c("screen"), ease_out(heat / 3)),
                                                             bold=True)
        out.append([(pad(tail(path, nw), nw), name), (" ", "text")] + _segments(bar) + [
            (" " * max(0, bw - plus - minus), "text"), (f" +{shown_a}".ljust(len(f" +{a}")), "ok"),
            (f" −{shown_d}".ljust(len(f" −{d}")) if d else "", "bad")])
    return out


def _tokens(st, w, h, app):
    """Each model call's prompt size as a column (shaded floor to top, rising when it arrives), newest on the right,
    sat on the panel's floor; the totals under it, rolling."""
    if not st.calls:
        return _waiting(st, "no model calls yet")
    fx = current()
    tall = min(10, max(3, (h or 5) - 1))
    vals = [fx.ease(f"col:{i}", v, 0.9) for i, v in enumerate(st.calls)]
    accent, accent2 = fx.c("chart") or fx.c("accent"), fx.c("accent2")
    lines = [[(row, rgb(fg=mix(accent, accent2, (tall - 1 - r) / max(1, tall - 1))))]
             for r, row in enumerate(columns(vals, w, tall))]
    roll = lambda key, v: human(round(fx.ease(key, v))).rjust(len(human(v)))  # rolls in place: labels stay put
    lines.append([(roll("tok:in", st.tokens[0]), "strong"), (" in   ", "dim"), (roll("tok:out", st.tokens[1]), "strong"),
                  (" out", "dim")])
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
    """Where the time went: each phase as a bar on the run's own clock, done ones a gradient, the live one
    shimmering."""
    sp = spans(st)
    if not sp:
        return _waiting(st, "starts with the run")
    fx = current()
    total = max(1, sp[-1][2])
    dw = max(len(duration(e - s)) for _, s, e in sp) + 2
    bw = max(4, w - 8 - dw)
    ok, ok2, accent, glow, bad = fx.c("ok"), fx.c("ok2"), fx.c("accent"), fx.c("glow"), fx.c("bad")
    out = []
    for i, (label, s, e) in enumerate(sp):
        a = min(bw - 1, int(s * bw / total))
        b = max(a + 1, min(bw, round(e * bw / total)))
        live = i == len(sp) - 1 and st.status not in ("closed", "answered")
        cells = []
        for x in range(a, b):
            if not live:
                c = mix(ok, ok2, x / max(1, bw - 1))
            elif st.status in ("blocked", "error", "stopped"):
                c = bad
            else:
                d = (fx.t * 14) % (b - a + 8) - (x - a)
                c = mix(accent, glow, 0.7 * (1 - d / 5) if fx.moving and 0 <= d < 5 else 0)
            cells.append(("▆", rgb(fg=c)))
        out.append([(f"{label:<8}", "dim"), (" " * a, "text")] + _segments(cells) + [
            (" " * (bw - b), "text"), (duration(e - s).rjust(dw), "accent" if live else "dim")])
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
    if k == "note":
        return [("  i ", "accent"), (e["text"], "text")]
    if k == "tool":
        return [("  · ", "dim"), (f"{e.get('action', '')[:7]:<7}", "dim"), (e["text"], "text")]
    if k == "working":
        return [("  … ", "accent"), (e["text"].strip(), "dim")]
    if k == "stalled":
        return [("  ⚠ ", "warn"), (e["text"].strip(), "warn")]
    if k == "closed":
        return [(" DONE ", "chip_ok"), ("  " + e["text"], "ok")]
    if k == "answer":
        return [("  ", "text"), (e.get("text", ""), "text")]
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
    """The run as it happens; a line that just arrived fades in from the panel."""
    out, thoughts, fx = [], app is None or app.thoughts, current()
    under, now = fx.c("panel", "bg"), None
    for i, e in enumerate(st.log):
        if e.get("kind") == "answer":  # T-1320: an answer is read whole, wrapped to the panel
            out += [[("  ", "text"), (part, "text")] for part in wrap(e.get("text", ""), max(10, w - 2), lines=200)]
            continue
        segs = None if e.get("kind") in LOG_HIDES else entry_segments(e, w, thoughts)
        if segs is None:
            continue
        arrived = fx.since(f"log:{i}", e.get("kind"))
        if arrived < 0.6:
            segs = [(t, faded(style, ease_out(arrived / 0.6), fx.cfg, under)) for t, style in segs]
        if arrived < 1.6 and e.get("result") == "refused":  # the guard's no lands with a flash
            hot = rgb(fg=col(fx.cfg, "chip_bad"), bg=mix(fx.c("glow"), col(fx.cfg, "chip_bad", "bg"),
                                                         ease_out(arrived / 1.6)), bold=True)
            segs = [(t, hot if t == " GUARD " else style) for t, style in segs]
        if app is not None and app.selected == i:
            segs = [("".join(t for t, _ in segs).ljust(w), "select")]
        else:
            now = len(out)
        out.append(segs)
        if app is not None and i in app.expanded and e.get("detail"):
            out += [[("      ", "text"), (part, "dim")] for line in str(e["detail"]).splitlines()[:30]
                    for part in wrap(line, max(10, w - 6), lines=4)]
    band = mix(under, fx.c("accent"), 0.16) if under and fx.c("accent") else None
    if st.status in LIVE and now == len(out) - 1 and band:  # the line being worked now sits on a band
        out[now] = _focus_line(out[now], w, band, fx.cfg)
    if not out and st.status in LIVE:  # started, nothing done yet: say what it's doing, mid-panel
        words = {"planning": "planning the work", "fixing": "fixing the checks"}.get(st.status, "working")
        line = [(" " * max(0, (w - len(words) - 2) // 2), "text"), ((fx.spin() if fx.moving else "◆") + " ", "accent")] + _waiting(st, words)[0]
        return [[]] * max(0, ((h or 1) - 1) // 2) + [line]
    return out or _welcome(w, h, fx)


def _welcome(w, h, fx):
    """The screen before any run: Foreman's mark, breathing, and the keys that start something."""
    a, b = fx.c("accent"), fx.c("accent2")
    keys = [("n", "new request"), ("h", "past runs"), ("m", "model"), ("?", "keys")]
    chips = [seg for k, word in keys for seg in ((f" {k} ", "chip_accent"), (f" {word}   ", "dim"))]
    width = sum(len(t) for t, _ in chips)
    pad = lambda n: [(" " * max(0, (w - n) // 2), "text")]
    lines = [pad(1) + [("◆", rgb(fg=mix(a, b, fx.wave(3.2)), bold=True) if a else "accent")], [],
             pad(12) + [("Foreman Code", "strong")],
             pad(42) + [("plan, edit, check and close, each guarded", "dim")], [], pad(width) + chips]
    top = max(0, ((h or len(lines)) - len(lines)) // 2)
    return [[]] * top + lines


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
BUILTIN_PANELS = {name: fn for name, (_, fn) in PANELS.items()}  # T-1315: never switched off (an extension's are)


# ---------------------------------------------------------------- render

def human(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.1f}k" if n >= 1e3 else str(n)


STATUS_CHIP = {"running": "chip_accent", "planning": "chip_warn", "fixing": "chip_warn", "closed": "chip_ok",
               "answered": "chip_ok",
               "blocked": "chip_bad", "error": "chip_bad", "stopped": "chip_bad"}


def elapsed(st, app):
    if not st.first_ts:
        return ""
    s = int((time.time() if app is not None and app.running() else st.last_ts or st.first_ts) - st.first_ts)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def _header(cv, st, app):
    cv.fill(0, "header")
    fx, brand = current(), " ◆ FOREMAN CODE "
    a, b, glow, ink = fx.c("accent"), fx.c("accent2"), fx.c("glow"), col(fx.cfg, "brand")
    sweep = (fx.t % 7) / 1.4 * (len(brand) + 8) - 4 if fx.moving else -99  # a glint crosses the name now and then
    for i, ch in enumerate(brand):
        bg = mix(mix(a, b, i / (len(brand) - 1)), glow, 0.55 * max(0.0, 1 - abs(i - sweep) / 3))
        cv.put(0, i, ch, rgb(fg=ink, bg=bg, bold=True) if bg else "brand")
    x = len(brand)
    clock = elapsed(st, app)
    right = "   ".join(v for v in (st.worker and f"worker {st.worker}" or st.model or "", clock and f"⏱ {clock}") if v)
    right = f"{right}  " if right else ""
    if st.request:
        cv.line(0, x + 2, [(st.request, "header")], cv.w - len(right) - 2)
    cv.put(0, cv.w - len(right), right, "header_dim")


def _status(cv, st, app):
    y = cv.h - 1
    cv.fill(y, "bar")
    fx, name = current(), STATUS_CHIP.get(st.status, "chip_todo")
    live = st.status in LIVE
    since = fx.since("status:chip", st.status)
    chip = rgb(fg=col(fx.cfg, name), bg=mix(fx.c("glow"), col(fx.cfg, name, "bg"), ease_out(since / 1.2)), bold=True) \
        if since < 1.2 else name
    segs = [(f" {fx.spin()} {st.status.upper()} " if live and fx.moving else f" {st.status.upper()} ", chip)]
    if st.task:
        segs += [("  ", "bar"), (st.task, "bar")]
    if st.steps:
        segs += [("   ", "bar"), (f"step {st.step}/{len(st.steps)}", "bar_dim")]
    if live and st.heard is not None:  # T-1336
        segs += [("   ", "bar"), (f"last heard {duration(st.heard)} ago", "bar_dim")]
    if app is not None and app.message:
        segs += [("   ", "bar"), (app.message, "key")]
    hints = [seg for k, word in HINTS for seg in ((f" {k} ", "key"), (f"{word} ", "bar_dim"))]
    hint_w = sum(len(t) for t, _ in hints) + 1
    room = cv.w - hint_w if cv.w - hint_w > 36 else cv.w
    cv.line(y, 0, segs, room)
    if room < cv.w:
        cv.line(y, room, hints, cv.w)


def _draw(name, st, w, h, app):
    fn = PANELS[name][1]
    ext = app is not None and BUILTIN_PANELS.get(name) is not fn
    if ext and name in app.panels_off:
        return [[(app.panels_off[name], "bad")]]
    t0 = time.monotonic()
    try:
        return [[(str(t), s if isinstance(s, tuple) else str(s)) for t, s in line] for line in fn(st, w, h, app)]
    except Exception as e:  # an extension's panel that fails, or returns something else than lines, says why
        return [[(f"panel {name} failed: {type(e).__name__}: {e}", "bad")]]
    finally:  # T-1315: an extension's panel over its budget PANEL_STRIKES frames running is switched off
        took = time.monotonic() - t0
        if ext:  # counted once a frame: a panel can be drawn twice in one (measured, then drawn)
            frame, strikes = app.panel_strikes.get(name, (None, 0))
            if frame != app.motion.frames:
                strikes = strikes + 1 if took > PANEL_BUDGET else 0
            app.panel_strikes[name] = (app.motion.frames, strikes)
            if strikes >= PANEL_STRIKES:
                app.panels_off[name] = f"panel {name} took {took * 1000:.0f} ms; switched off"
                app.state.note("error", text=app.panels_off[name])


def _panel(cv, st, app, cfg, name, y, x, h, w, lines):
    title, note = _title(st, name)
    iy, ix, ih, iw = box(cv, y, x, h, w, title, cfg, app is not None and app.focused() == name, note)
    follow = name == "log" and (app is None or app.follow)
    top = max(0, len(lines) - ih) if follow else min(app.scroll if app else 0, max(0, len(lines) - ih))
    for r, segs in enumerate(lines[top:top + ih]):
        cv.line(iy + r, ix, segs, ix + iw)


def render(st, w, h, cfg, app=None, t=None):
    """The whole screen for this state at time t (the App's clock): header, panels per the layout, the status bar,
    any open view. Motion is a function of state and time, so any instant can be drawn (tests, snapshots, video)."""
    global _FX
    if app is not None:
        app.motion.frames += 1
        t = app.clock() if t is None else t
    _FX = FX(cfg, app, t or 0.0)
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
    for ci, names_ in enumerate(columns_):
        cw = w - x if ci == len(columns_) - 1 else max(12, w * widths[ci] // max(sum(widths), 1))
        names = [n for n in names_ if n in PANELS] or ["log"]
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
        cv.line(h - 2, 0, [(" request › ", "key"), (app.input.replace("\n", " ↵ "), "input"), ("▏", "key")], w)
    if app is not None and app.mode in VIEWS:
        VIEWS[app.mode](cv, st, app, cfg)
    return cv


# ---------------------------------------------------------------- views over the main screen

KEY_NAMES = {"\t": "Tab", "\n": "Enter", "KEY_ENTER": "Enter", "KEY_UP": "↑", "KEY_DOWN": "↓", "KEY_PPAGE": "PgUp",
             "KEY_NPAGE": "PgDn"}
COMMAND_LABELS = [("new", "type a request"), ("stop", "stop the run"), ("resume", "resume it"),
                  ("diff", "the run's changes"), ("history", "past runs"), ("projects", "every Foreman project"),
                  ("model", "model or worker"),
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
        iy, ix, ih, iw = _overlay(cv, cfg, title(app) if callable(title) else title, note, 110,
                                  min(len(app.items) + 4, cv.h - 4))
        if not app.items:
            cv.line(iy + 1, ix, [("nothing here yet", "dim")], ix + iw)
        first = max(0, app.item_index - ih + 2)
        for r, item in enumerate(app.items[first:first + ih - 1]):
            segs = row(item)
            if first + r == app.item_index:
                segs = [(pad("".join(t for t, _ in segs), iw), "select")]
            cv.line(iy + 1 + r, ix, segs, ix + iw)
    return view


def _history_row(item):
    chip = {"closed": (" DONE ", "chip_ok"), "blocked": (" STOP ", "chip_bad"), "error": (" STOP ", "chip_bad")}.get(
        item["status"], (" ···· ", "chip_todo"))
    when = time.strftime("%b %d %H:%M", time.localtime(item["ts"])) if item.get("ts") else ""
    return [chip, ("  " + pad(item["task"] or "—", 8), "strong"), ("  " + pad(when, 12), "dim"),
            ("  " + item["request"], "text")]


def _picker_row(item):
    kind, name = item
    return [(" MODEL  " if kind == "model" else " WORKER ", "chip_accent" if kind == "model" else "chip_warn"),
            ("  " + name, "text")]


def _num(v):
    return v if isinstance(v, (int, float)) and v == v else 0


def _project_row(p):
    """T-1330: one Foreman project on the home: what's active, its counts, or why it can't be shown."""
    name = str(p.get("project") or "?")
    if p.get("error"):
        return [(" ERROR ", "chip_bad"), ("  " + pad(name, 24), "strong"), ("  " + str(p["error"]), "bad")]
    if p.get("exists") is False:
        return [(" GONE  ", "chip_bad"), ("  " + pad(name, 24), "strong"), (f"  folder missing: {p.get('root')}", "dim")]
    a = p.get("active") if isinstance(p.get("active"), dict) else None
    counts = f"queue {_num(p.get('queue'))}  inbox {_num(p.get('inbox'))}  blocked {_num(p.get('blocked'))}"
    return [(" ACTIVE " if a else " IDLE   ", "chip_accent" if a else "chip_todo"), ("  " + pad(name, 24), "strong"),
            (f"  {counts:<34}", "dim"), ("  " + (f"{a.get('id')} {a.get('title') or ''}" if a else "nothing active"),
                                         "text")]


_SECTION = {"active": (" ACTIVE  ", "chip_accent"), "queue": (" QUEUED  ", "chip_todo"),
            "inbox": (" INBOX   ", "chip_todo"), "blocked": (" BLOCKED ", "chip_bad")}


def _work_row(it):
    """T-1330: one line of a project's view: a task by section, a past run, or why its state can't be read."""
    if it.get("kind") == "error":
        return [(" ERROR ", "chip_bad"), ("  " + str(it.get("text")), "bad")]
    if it.get("kind") == "run":
        return _history_row(it)
    t = it.get("task") or {}
    why = f"  ({t['reason']})" if t.get("reason") else ""
    return [_SECTION.get(it.get("section"), (" TASK    ", "chip_todo")), ("  " + pad(t.get("id") or "?", 7), "strong"),
            (f"  {str(t.get('type') or '')[:4]:<4} {str(t.get('tier') or '')}", "dim"),
            ("  " + str(t.get("title") or "") + why, "text")]


def fm_projects():
    """Every Foreman project on this machine, as fm projects --json lists them."""
    return (_fm_json("projects").get("projects") or [])


def fm_project_state(p):
    """A project's work, as fm state --json gives it, and its fm code runs' folder."""
    st = _fm_json("state", "-p", str(p.get("project")))
    import fmcore
    q = fmcore.project_by_slug(str(p.get("project")))
    st["code_dir"] = os.path.join(q.dir, "code") if q else None
    return st


def _fm_json(*args):
    r = subprocess.run([sys.executable, FM, *args, "--json"], capture_output=True, text=True, timeout=60,
                       stdin=subprocess.DEVNULL)
    if r.returncode:
        raise RuntimeError(" ".join((r.stderr or r.stdout).split())[-300:] or f"fm {args[0]} exit {r.returncode}")
    return json.loads(r.stdout)


VIEWS = {"help": _help_view, "diff": _diff_view, "history": _list_view("Past runs", "Enter opens one", _history_row),
         "picker": _list_view("Run the next request with", "Enter picks", _picker_row),
         "home": _list_view("Foreman projects", "Enter opens · n new request there · Esc run screen · q quits",
                            _project_row),
         "project": _list_view(lambda app: str((app.project or {}).get("project") or "project"),
                               "Enter/r runs a task · Enter replays a run · n new · m runner · Esc projects",
                               _work_row)}


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


@functools.lru_cache(maxsize=4096)  # the terminal asks for every cell of every frame
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
    back, head = [], len(out)  # every background goes under every glyph, so a later run's background can't cut a hairline into a bar
    for y, row in enumerate(cv.cells):
        x, under = 0, cv.bg[y]
        while x < len(row):
            style, end = row[x][1], x
            while end < len(row) and row[end][1] == style and under[end] == under[x]:
                end += 1
            spec = resolve(style, cfg, under[x])
            s_fg, s_bg = spec.get("fg"), spec.get("bg")
            if spec.get("reverse"):
                s_fg, s_bg = s_bg or screen.get("bg", _BG), s_fg or screen.get("fg", _INK)
            px, py = pad + x * cw, chrome + pad + y * ch
            if s_bg is not None:
                back.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{(end - x) * cw + 0.6:.1f}" height="{ch + 0.6:.1f}" '
                            f'fill="{_hex(s_bg)}"/>')  # +0.6: neighbouring runs overlap, no seam between them
            text = "".join(c for c, _ in row[x:end])
            k = 0
            while k < len(text):  # block glyphs as exact rects (one per run), as a terminal fills its cells
                c, j = text[k], k
                while j < len(text) and text[j] == c:
                    j += 1
                if c in BLOCKS:
                    part = (BLOCKS.index(c) + 1) / 8
                    out.append(f'<rect x="{px + k * cw:.1f}" y="{py + ch * (1 - part):.1f}" width="{(j - k) * cw + 0.6:.1f}" '
                               f'height="{ch * part + 0.6:.1f}" fill="{_hex(s_fg) if s_fg is not None else fg}"/>')
                k = j
            text = "".join(" " if c in BLOCKS else c for c in text)
            if text.strip():
                attrs = (' font-weight="bold"' if spec.get("bold") else "") + (
                    ' font-style="italic"' if spec.get("italic") else "")
                out.append(f'<text x="{px:.1f}" y="{py + ch * 0.74:.1f}" fill="{_hex(s_fg) if s_fg is not None else fg}"'
                           f' textLength="{(end - x) * cw:.1f}" lengthAdjust="spacingAndGlyphs"{attrs}>'
                           f'{html.escape(text)}</text>')
            x = end
    out[head:head] = back
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- the app: keys, commands, views, the child

class App:
    def __init__(self, cfg, spawn=None, root=None, opts=None, diff=None, history=None, choices=None, projects=None,
                 project_state=None):
        self.cfg, self.state = cfg, State()
        self.mode, self.input, self.message, self.done = "main", "", "", False
        self.spawn = spawn or self._spawn
        self.root, self.opts = root or os.getcwd(), dict(opts or {})
        self.diff_source, self.history_dir = diff or self._git_diff, history
        self.choices_source = choices or self._choices
        # T-1330: the app's home (every Foreman project) and a project's view, read through fm
        self.projects_source, self.state_source = projects or fm_projects, project_state or fm_project_state
        self.project, self.view_back, self.next_root, self.prompt_back = None, "main", None, "main"
        self.child, self.events = None, queue.Queue()
        self.order, self.focus, self.scroll, self.follow, self.thoughts = [], 0, 0, True, False
        self.selected, self.expanded = None, set()
        self.view_lines, self.view_scroll, self.items, self.item_index = [], 0, [], 0
        self.extra_labels, self.ext = list(EXT_LABELS), {}
        self.panel_strikes, self.panels_off = {}, {}  # T-1315: an extension panel's (frame, slow frames running); off
        self.motion, self.clock = Motion(), time.monotonic  # T-1300: what moves, and the time it moves by
        self.commands = {"quit": self.quit, "new": self.new, "stop": self.stop, "resume": self.resume,
                         "help": self.help, "focus": self.next_focus, "up": lambda: self.move(-1),
                         "down": lambda: self.move(1), "page_up": lambda: self.move(-10),
                         "page_down": lambda: self.move(10), "expand": self.expand, "follow": self.follow_tail,
                         "diff": self.show_diff, "history": self.show_history, "model": self.show_picker,
                         "thoughts": self.toggle_thoughts, "projects": self.show_home}
        self.commands.update({name: self._ext_command(name, fn) for name, fn in EXT_COMMANDS.items()})

    def fps(self, t):
        """How often to draw: 30 while something eases or flashes, 12 while live work spins and pulses, 1 when the
        screen is still (4 with motion off and a run going, for its clock)."""
        mode = self.cfg.get("motion", "full")
        live = self.running() or self.state.status in ("planning", "running", "fixing")
        if mode == "off":
            return 4 if live else 1
        if self.motion.busy(t):
            return 30
        return 12 if live and mode == "full" else 1

    def _ext_command(self, name, fn):
        def run():  # T-1315: one that raises or runs over COMMAND_BUDGET is said in Activity and switched off
            t0, why = time.monotonic(), None
            try:
                fn(self)
            except Exception as e:  # an extension's bug shows in the status bar; the screen stays up
                why = f"failed: {type(e).__name__}: {e}"
            took = time.monotonic() - t0
            if why is None and took > COMMAND_BUDGET:
                why = f"took {took * 1000:.0f} ms"
            if why:
                self.commands.pop(name, None)
                self.message = f"command {name} {why}; switched off"
                self.state.note("error", text=self.message)
        return run

    # -- keys
    def key(self, k):
        if isinstance(k, tuple):  # T-1316: a paste: the prompt takes it whole, newlines kept; anywhere else nothing
            if self.mode == "prompt" and k[0] == "paste":
                text = "".join(c for c in k[1].replace("\t", " ") if c == "\n" or c.isprintable())
                self.input = (self.input + text)[:PASTE_CAP]
            return None
        if self.mode == "prompt":
            return self._prompt_key(k)
        if self.mode == "help":
            self.mode = "main"
            return None
        if self.mode in ("home", "project"):
            return self._home_key(k)
        if self.mode in ("diff", "history", "picker"):
            return self._view_key(k)
        fn = self.commands.get(self.cfg["keys"].get(k))
        return fn() if fn else None

    def _view_key(self, k):
        cmd = self.cfg["keys"].get(k)
        step = {"up": -1, "down": 1, "page_up": -10, "page_down": 10}.get(cmd)
        if k in ("\x1b", "q") or cmd == {"diff": "diff", "history": "history", "picker": "model"}[self.mode]:
            self._back()
        elif step and self.mode == "diff":
            self.view_scroll = max(0, self.view_scroll + step)
        elif step:
            self.item_index = max(0, min(len(self.items) - 1, self.item_index + step))
        elif cmd == "expand" and self.items:
            item, self.mode = self.items[self.item_index], "main"
            if not isinstance(item, dict):  # a runner picked: back to the project it's for, if any
                self._back()
            self.view_back = "main"
            if isinstance(item, dict):
                self.replay(item["path"])
            else:
                kind, name = item
                self.opts.update(model=name if kind == "model" else None, worker=name if kind == "worker" else None)
                self.message = f"next run: {kind} {name}"

    def _prompt_key(self, k):
        if k in ("\n", "\r", "KEY_ENTER"):
            text, self.mode, self.input, self.prompt_back = self.input.strip(), "main", "", "main"
            if text:
                self.start([text])
        elif k == "\x1b":
            self.input, self.next_root = "", None
            back, self.prompt_back = self.prompt_back, "main"
            if back == "project" and self.project is not None:
                self.mode, self.items, self.item_index = "project", self.project_items, self.project_index
            else:
                self.mode = "main"
        elif k in ("KEY_BACKSPACE", "\x7f", "\b"):
            self.input = self.input[:-1]
        elif len(k) == 1 and k.isprintable():
            self.input += k

    def focused(self):
        return self.order[self.focus % len(self.order)] if self.order else "log"  # the first frame too

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

    # -- the app (T-1330): home over every Foreman project, a project's work and past runs
    def _back(self):
        """Close a view: to the project or home it was opened from, else the run's screen."""
        back, self.view_back = self.view_back, "main"
        if back == "project" and self.project is not None:
            self.mode, self.items, self.item_index = "project", self.project_items, self.project_index
        elif back == "home":
            self.show_home()
        else:
            self.mode = "main"

    def show_home(self):
        try:
            found = list(self.projects_source())
        except Exception as e:  # fm isn't answering: say so, keep the screen
            found, self.message = [], f"can't list projects: {e}"
        self.items = sorted((x for x in found if isinstance(x, dict)),  # a missing folder last, then newest first
                            key=lambda x: (x.get("exists") is False, -_num(x.get("updated"))))
        self.item_index, self.mode = 0, "home"

    def open_project(self, proj):
        """A project's view: its active task, queue, inbox and blocked tasks, then its past runs; runs start there."""
        rows, self.project = [], proj
        if proj.get("exists") is False:
            rows.append({"kind": "error", "text": f"folder missing: {proj.get('root')} (nothing can run here)"})
        try:
            st = self.state_source(proj) or {}
        except Exception as e:  # its state can't be read: say why here, home still draws
            st, rows = {}, [{"kind": "error", "text": f"can't read {proj.get('project')}'s state: {e}"}]
        if isinstance(st.get("active"), dict):
            rows.append({"kind": "task", "section": "active", "task": st["active"]})
        for sec in ("queue", "inbox", "blocked"):
            rows += [{"kind": "task", "section": sec, "task": t} for t in st.get(sec) or [] if isinstance(t, dict)]
        rows += [dict(r, kind="run") for r in history(st.get("code_dir"))]
        self.project_code = st.get("code_dir")  # the run's own folder and history move only when a run starts here
        self.project_items, self.project_index = rows, 0
        self.items, self.item_index, self.mode = rows, 0, "project"

    def _home_key(self, k):
        cmd = self.cfg["keys"].get(k)
        step = {"up": -1, "down": 1, "page_up": -10, "page_down": 10}.get(cmd)
        item = self.items[self.item_index] if self.items else None
        if step:
            self.item_index = max(0, min(len(self.items) - 1, self.item_index + step))
            if self.mode == "project":
                self.project_index = self.item_index
        elif k == "\x1b" or cmd == "projects":
            if self.mode == "project":
                self.show_home()
            else:
                self.mode = "main"
        elif cmd == "quit":
            return self.quit()
        elif self.mode == "home" and item and cmd in ("expand", "new"):
            self.open_project(item)
            if cmd == "new":
                self.new_here()
        elif self.mode == "project" and cmd == "new":
            self.new_here()
        elif self.mode == "project" and cmd == "model":
            self.view_back = "project"
            self.show_picker()
        elif self.mode == "project" and item and item.get("kind") == "task" and cmd in ("expand", "resume"):
            self.run_task(item["task"])
        elif self.mode == "project" and item and item.get("kind") == "run" and cmd == "expand":
            self.mode = "main"
            self.replay(item["path"])
        return None

    def _here(self):
        """Whether a run can start in the open project; the next run's folder and history are set to it."""
        if self.running():
            self.message = "a run is going: s stops it"
            return False
        if (self.project or {}).get("exists") is False:
            self.message = f"{self.project.get('project')}'s folder is missing: nothing can run there"
            return False
        self.next_root = (str(self.project.get("root") or self.root), self.project_code)
        return True

    def run_task(self, t):
        """fm code --task ID in the open project's folder, with the runner picked by m."""
        if self._here():
            self.mode = "main"
            self.start(["--task", str(t.get("id"))])

    def new_here(self):
        """A new request typed for the open project; Esc goes back to its view."""
        if self._here():
            self.prompt_back = "project"
            self.new()

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
        self.motion = Motion()
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
        try:
            runners = fmcode.all_runners()
        except fmcode.CodeError as e:  # T-1395: the models still list, with what's wrong in code.toml
            self.message = str(e)
            return out
        return out + [("worker", w) for w, r in runners.items()  # T-1330: code.toml's runners too
                      if r.get("work") and fmcode._installed(w, r)]

    # -- the child
    def running(self):
        return self.child is not None and getattr(self.child, "poll", lambda: 0)() is None

    def start(self, words, **extra):
        self.state, self.selected, self.expanded, self.follow, self.message = State(), None, set(), True, ""
        self.motion = Motion()
        if self.next_root:  # T-1330: a run started from a project's view runs in that project
            (self.root, code), self.next_root = self.next_root, None
            self.history_dir = code or self.history_dir
        try:
            self.child = self.spawn(words, dict(self.opts, **extra))
        except OSError as e:  # a folder gone since, fm missing: say so, keep the screen
            self.child = None
            self.state.status, self.state.error = "error", f"couldn't start: {e}"
            self.state.note("error", text=f"couldn't start: {e}")

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
# T-1315: an extension's time budgets, in seconds; past one it's switched off for the session with a note in Activity.
PANEL_BUDGET, PANEL_STRIKES = 0.05, 3  # a panel over 50 ms on 3 frames running
HANDLER_BUDGET = 0.05                  # an event handler over 50 ms once
COMMAND_BUDGET = 2.0                   # a command over 2 s once


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


def contrast(a, b):
    """WCAG contrast ratio of two colours (1 to 21)."""
    def lum(c):
        ch = [v / 255 for v in _rgb(c)]
        ch = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _faint(spec, theme):
    """Why a style's text can't be read on what it sits on (its own background or the screen's), or None."""
    fg, bg = spec.get("fg"), spec.get("bg") or theme.get("screen", {}).get("bg")
    if fg is None or bg is None:
        return None
    ratio = contrast(fg, bg)
    return f"{fg} on {bg} is too faint to read ({ratio:.1f}:1; text needs 3:1)" if ratio < 3 else None


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
        if key == "motion":
            if val in MOTIONS:
                cfg["motion"] = val
            else:
                bad(f"motion = {val!r}: one of {', '.join(MOTIONS)}")
        elif key == "border":
            if val in BORDERS:
                cfg["border"] = val
            else:
                bad(f"border = {val!r}: one of {', '.join(BORDERS)}")
        elif key in ("colors", "layout", "keys") and not isinstance(val, dict):
            bad(f"{key}: a [{key}] table")
        elif key == "colors":
            for name, spec in val.items():
                msg = _style_error(name, spec, cfg["theme"])
                if not msg and name not in ("screen", "panel", "border", "track", "shade"):  # text has to be read
                    msg = _faint(spec if isinstance(spec, dict) else {"fg": spec}, cfg["theme"])
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
            bad(f"{key}: not a setting (theme, motion, border, colors, layout, keys)")
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
           f"motion = {_toml(cfg.get('motion', 'full'))}  # full; reduced: colours change, nothing moves; off",
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

def replay_file(path, cfg, plain, out=sys.stdout):
    """fm code tui --events FILE: the run on the screen, or (plain) its Activity lines; 0 for a closed run, 1 for
    another, 2 when FILE can't be read."""
    if not os.path.isfile(path):
        print(f"fm code tui: can't read {path}: no such file (fm code … --json > FILE records a run)", file=sys.stderr)
        return 2
    app = App(cfg, spawn=lambda *a, **k: None)
    app.replay(path)
    if app.message.startswith("can't read"):
        print(f"fm code tui: {app.message}", file=sys.stderr)
        return 2
    if not plain:
        run_screen(app)
        return 0
    for entry in app.state.log:
        print(__import__("fmcore").redact(entry_text(entry)), file=out, flush=True)  # T-1302: piped lines get shared
    return 0 if app.state.status == "closed" else 1


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


def key_of(k):
    """A key as tui.toml names it: a control key as ^R, Enter's \\r as \\n (parse_keys does this for raw input)."""
    if k == "\r":
        return "\n"
    if len(k) == 1 and ord(k) < 32 and k not in "\t\n\x1b\b":
        return "^" + chr(ord(k) + 64)
    return k


def _loop(io, app):
    """Draw, wait for a key or the next frame, repeat: as often as what's on screen moves (App.fps)."""
    term, w, h = Term(colour_depth()), 80, 24
    if term.depth == 0:  # NO_COLOR: the mono theme, whose chips are reversed and panels untinted
        app.cfg = dict(app.cfg, theme=_mono(), preset="mono")
    while not app.done:
        app.poll()
        if io.resized():
            w, h = io.size()
            term.prev = None
            io.write("\x1b[2J")
        t = app.clock()
        io.write(term.frame(render(app.state, w, h, app.cfg, app, t=t), app.cfg))
        for k in io.keys(1 / app.fps(t)):
            app.key(k)


def run_screen(app, wrapper=None):
    """The screen until q. Whatever ends it (q, Ctrl-C, a crash, a closed terminal) stops the run first: fm code
    runs in its own session and would carry on into a closed pipe. wrapper owns the terminal (fmcodeterm.session)."""
    def hangup(*_):
        raise SystemExit(129)
    old = {}
    for name in ("SIGHUP", "SIGTERM"):  # a closed terminal or a kill: the run stops and the terminal comes back
        try:
            old[name] = signal.signal(getattr(signal, name), hangup)
        except (ValueError, AttributeError):  # not the main thread, or no such signal here
            pass
    try:
        (wrapper or session)(lambda io: _loop(io, app))
    finally:
        app.stop()
        for name, handler in old.items():
            signal.signal(getattr(signal, name), handler)


def record(events, path, size=(120, 34), fps=20, seconds=None, cfg=None, hold=2.5):
    """A run's events played back as a video (mp4, or gif by its name): frames drawn at their instant, put to PNG by
    rsvg-convert and joined by ffmpeg. For the README, the site and a bug report."""
    if not (shutil.which("ffmpeg") and shutil.which("rsvg-convert")):
        raise RuntimeError("fm code tui --record needs ffmpeg and rsvg-convert on PATH")
    import fmcore
    import tempfile
    cfg = cfg or DEFAULTS
    events = fmcore.redact_obj([e for e in events if isinstance(e, dict)])  # T-1302: frames never hold a token
    seconds = seconds or max(4.0, min(16.0, len(events) * 0.45))
    gap, app = seconds / max(len(events), 1), App(cfg, spawn=lambda *a, **k: None)
    with tempfile.TemporaryDirectory(prefix="fm-tui-") as tmp:
        fed, svg = 0, os.path.join(tmp, "frame.svg")
        for f in range(int((seconds + hold) * fps)):
            t = f / fps
            while fed < len(events) and fed * gap <= t:
                app.feed(events[fed])
                fed += 1
            with open(svg, "w", encoding="utf-8") as fh:
                fh.write(to_svg(render(app.state, size[0], size[1], cfg, app, t=1000.0 + t), cfg))
            subprocess.run(["rsvg-convert", "-o", os.path.join(tmp, f"f{f:05d}.png"), svg], check=True)
        args = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%05d.png")]
        args += ["-vf", "split[a][b];[a]palettegen[p];[b][p]paletteuse"] if path.endswith(".gif") else [
            "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2"]
        subprocess.run(args[:1] + ["-nostdin"] + args[1:] + [os.path.abspath(path)], check=True, stdin=subprocess.DEVNULL)
    return path


def snapshot(events, path, size=(120, 34), cfg=None, mode="main"):
    """The screen after these events, as an SVG at path (README pictures, the site, a bug report)."""
    cfg = cfg or DEFAULTS
    import fmcore
    app = App(cfg, spawn=lambda *a, **k: None)
    for e in fmcore.redact_obj(list(events)):  # T-1302: a shared file never holds a token a worker printed
        app.feed(e)
    app.mode = mode
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_svg(render(app.state, size[0], size[1], cfg, app), cfg))
    return path


def main(args, words, home=False):
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
    out = getattr(args, "snapshot", None) or getattr(args, "record", None)
    if out:
        src = getattr(args, "events", None)
        if not src:
            print("fm code tui --snapshot/--record needs --events FILE (fm code … --json > FILE records one)",
                  file=sys.stderr)
            return 2
        with open(src, encoding="utf-8") as f:
            events = [json.loads(line) for line in f if line.strip()]
        w, _, h = (getattr(args, "size", None) or "120x34").partition("x")
        if getattr(args, "snapshot", None):
            print(snapshot(events, out, (int(w), int(h)), cfg))
            return 0
        try:
            print(record(events, out, (int(w), int(h)), cfg=cfg))
        except (RuntimeError, subprocess.CalledProcessError) as e:
            print(f"fm code tui: {e}", file=sys.stderr)
            return 2
        return 0
    if getattr(args, "events", None):  # T-1363: a recorded run alone replays: on the screen, else as Activity lines
        return replay_file(args.events, cfg, plain=getattr(args, "plain", False) or not sys.stdout.isatty()
                           or not sys.stdin.isatty())
    import fmcli
    try:
        p = fmcli.resolve(args, create=not home)  # the app never registers a folder by opening in it
    except fmcli.UsageError:
        if not home:
            raise
        p = None  # T-1330: outside any project the app opens on its home
    opts = {k: getattr(args, k, None) for k in ("model", "worker", "verify", "escalate", "max_steps", "no_commit",
                                                 "worker_timeout", "dry_plan")}
    root = os.path.realpath(p.root) if p else os.getcwd()
    app = App(cfg, root=root, opts=opts, history=p and os.path.join(p.dir, "code"))
    if home:  # T-1330: inside a project, its view; elsewhere every project
        app.show_home()
        here = next((x for x in app.items if p and x.get("project") == p.slug), None)  # a worktree too
        if here:
            app.open_project(here)
        if problems:
            app.message = f"{len(problems)} setting(s) skipped: {problems[0]}"
        run_screen(app)
        return 0
    resume = getattr(args, "resume", None)
    first = (lambda: app.start([], resume=resume or True)) if resume is not None else (
        lambda: app.start([" ".join(words)])) if words else None
    if getattr(args, "plain", False) or not sys.stdout.isatty() or not sys.stdin.isatty():
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
