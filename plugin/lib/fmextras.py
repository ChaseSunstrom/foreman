"""fm extras (T-1556): playful things made from an fm code run, offline and stdlib only.

    fm extras zine [--events FILE] [--out FILE]     the run folded into a one-sheet, eight-page printable zine (SVG)
    fm extras vase [--events FILE] [--out FILE]     the run turned on a lathe: a closed vase, an ASCII STL to print
    fm extras cursor X,Y X,Y … [--out FILE]         a cursor gliding between points with a click at each, for demos

A run is the event stream fm code records (fm code … --json > FILE); without --events, the sample run every theme
draws. Breakout, the game that opens while a run's checks run, lives in the fm code app (B) and is defined here."""
import html
import json
import math
import os
import textwrap

# ---------------------------------------------------------------- reading a run


def load(path):
    """The events in a recorded run, one JSON object a line (bad lines skipped, as the app's replay does)."""
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if isinstance(e, dict):
                out.append(e)
    return out


def digest(events):
    """What a zine says about a run: {title, kind, task, request, criteria, steps, before, work, files, after,
    tokens}, each from the run's own events."""
    d = {"title": "", "kind": "", "task": "", "request": "", "criteria": [], "steps": [], "before": None, "work": [],
         "files": [], "after": None, "tokens": 0}
    for e in events:
        k = e.get("event")
        if k == "start":
            d["request"] = str(e.get("request") or "")
        elif k == "plan" and isinstance(e.get("plan"), dict):
            p = e["plan"]
            d["title"] = str(p.get("title") or "")
            d["kind"] = " ".join(str(p.get(x) or "") for x in ("type", "tier")).strip()
            d["criteria"] = [str(c.get("text", "")) for c in p.get("criteria") or [] if isinstance(c, dict)]
            d["steps"] = [str(s) for s in p.get("steps") or []]
        elif k == "task":
            d["task"] = str(e.get("task") or "")
        elif k == "verify":
            v = (str(e.get("cmd") or ""), e.get("exit"), str(e.get("output") or ""))
            if e.get("label") == "before":
                d["before"] = d["before"] or v
            else:
                d["after"] = v
        elif k == "action":
            d["work"].append(f"{e.get('action', '')} {e.get('target', '')}: {e.get('result', '')}")
        elif k == "changed":
            d["files"] += [str(f) for f in e.get("files") or [] if str(f) not in d["files"]]
        elif k == "tokens":
            d["tokens"] = int(e.get("total_in") or 0) + int(e.get("total_out") or 0)
    d["title"] = d["title"] or d["request"] or "An fm code run"
    return d


# ---------------------------------------------------------------- the zine

SHEET = (1100, 850)  # US letter, landscape, at 100 units an inch
PANEL = (SHEET[0] // 4, SHEET[1] // 2)
WRAP = 30  # characters a body line holds in a panel
# page -> (column, row) on the sheet, the common one-sheet fold: the top row upside down, the covers bottom right
IMPOSE = {5: (0, 0), 4: (1, 0), 3: (2, 0), 2: (3, 0), 6: (0, 1), 7: (1, 1), 8: (2, 1), 1: (3, 1)}
FOLD = ["Fold in half the long way, then open.", "Fold in half the short way, then in half again; open.",
        "Fold the short way and cut the middle slit along the dashed line.", "Open, fold the long way, push the ends "
        "in so the slit opens into a cross, and fold the pages round to the cover."]


def pages(d):
    """The eight pages: [(heading, [lines])], page 1 the cover and page 8 the back."""
    def verify(v, none):
        if not v:
            return [none]
        cmd, code, out = v
        return [f"$ {cmd}", "passed" if code == 0 else f"failed (exit {code})"] + ([out] if out else [])
    return [
        (d["title"], [d["kind"], d["task"], "", "a run of fm code, folded"]),
        ("What was asked", [d["request"] or "(no request recorded)"] + [f"• {c}" for c in d["criteria"]]),
        ("The plan", [f"{i}. {s}" for i, s in enumerate(d["steps"], 1)] or ["(no steps recorded)"]),
        ("Before", verify(d["before"], "no check ran before the change")),
        ("The work", d["work"][-10:] or ["(no actions recorded)"]),
        ("What changed", d["files"][:12] or ["(no files changed)"]),
        ("Proof", verify(d["after"], "no check ran after the change") + ([f"{d['tokens']:,} tokens"]
                                                                          if d["tokens"] else [])),
        ("How to fold", FOLD + ["", "Made with fm extras zine"]),
    ]


def _page_svg(n, heading, lines):
    w, h = PANEL
    big = 30 if n == 1 else 22
    head = textwrap.wrap(str(heading), 16 if n == 1 else 20)[:3] or [""]
    title = "".join(f'<text x="24" y="{56 + i * (big + 6)}" font-size="{big}" font-weight="700">{html.escape(t)}</text>'
                    for i, t in enumerate(head))
    body, y = [], 56 + (len(head) - 1) * (big + 6) + 40
    for line in lines:
        for part in textwrap.wrap(str(line), WRAP) or [""]:
            if y > h - 50:
                break
            if part:
                body.append(f'<text x="24" y="{y}" font-size="14">{html.escape(part)}</text>')
            y += 20
    return (f'<rect width="{w}" height="{h}" fill="none"/>{title}{"".join(body)}'
            f'<text x="{w - 24}" y="{h - 22}" font-size="12" text-anchor="end" opacity=".6">{n}</text>')


def zine(events):
    """The run as one printable sheet: eight panels imposed so a single fold-and-cut makes the booklet."""
    w, h = PANEL
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="11in" height="8.5in" viewBox="0 0 {SHEET[0]} {SHEET[1]}" '
           f'font-family="system-ui, sans-serif" fill="#1d1d1f"><rect width="{SHEET[0]}" height="{SHEET[1]}" '
           f'fill="#ffffff"/>']
    for n, (heading, lines) in enumerate(pages(digest(events)), 1):
        col, row = IMPOSE[n]
        x, y = col * w, row * h
        turn = f" rotate(180 {w / 2:g} {h / 2:g})" if row == 0 else ""
        out.append(f'<g class="page" data-page="{n}" transform="translate({x} {y}){turn}">'
                   f'{_page_svg(n, heading, lines)}</g>')
    guides = [f'<line x1="{c * w}" y1="0" x2="{c * w}" y2="{SHEET[1]}"/>' for c in (1, 2, 3)]
    guides.append(f'<line x1="0" y1="{h}" x2="{SHEET[0]}" y2="{h}"/>')
    out.append(f'<g class="folds" stroke="#bbb" stroke-dasharray="4 6">{"".join(guides)}</g>'
               f'<line class="cut" x1="{w}" y1="{h}" x2="{3 * w}" y2="{h}" stroke="#c0392b" stroke-width="2" '
               f'stroke-dasharray="10 6"/></svg>\n')
    return "".join(out)


# ---------------------------------------------------------------- the vase

RADIUS = {"verify-fail": 14.0, "verify-pass": 44.0, "refused": 20.0, "changed": 38.0, "step": 32.0}


def profile(events, height=120.0):
    """[(radius, z)] from the foot up: each event of the run a ring (a failed check pinches the wall, a passing one
    swells it, a refusal nips it), smoothed so the lathe turns a curve."""
    rs = [28.0]
    for e in events:
        k = e.get("event")
        key = ("verify-pass" if not e.get("exit") else "verify-fail") if k == "verify" else (
            "refused" if k == "action" and e.get("result") == "refused" else k)
        rs.append(RADIUS.get(key, 28.0))
    rs.append(26.0)  # the lip
    for _ in range(2):
        rs = [rs[0]] + [(a + 2 * b + c) / 4 for a, b, c in zip(rs, rs[1:], rs[2:])] + [rs[-1]]
    return [(r, height * i / (len(rs) - 1)) for i, r in enumerate(rs)]


def _facet(a, b, c):
    u = [b[i] - a[i] for i in range(3)]
    v = [c[i] - a[i] for i in range(3)]
    n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    size = math.sqrt(sum(x * x for x in n)) or 1.0
    f = lambda p: " ".join(f"{x:.4f}" for x in p)  # noqa: E731
    return (f"  facet normal {f(x / size for x in n)}\n    outer loop\n      vertex {f(a)}\n      vertex {f(b)}\n"
            f"      vertex {f(c)}\n    endloop\n  endfacet\n")


def vase(events, segments=48, height=120.0, name="fm-vase"):
    """The run's profile turned about the z axis into a closed solid (a slicer's vase mode prints its wall), as an
    ASCII STL in millimetres, every facet wound outward."""
    prof = profile(events, height)
    ring = lambda r, z: [(r * math.cos(2 * math.pi * j / segments), r * math.sin(2 * math.pi * j / segments), z)
                         for j in range(segments)]  # noqa: E731
    rings = [ring(r, z) for r, z in prof]
    out = [f"solid {name}\n"]
    for lo, hi in zip(rings, rings[1:]):
        for j in range(segments):
            a, b, c, d = lo[j], lo[(j + 1) % segments], hi[(j + 1) % segments], hi[j]
            out += [_facet(a, b, c), _facet(a, c, d)]
    foot, top = (0.0, 0.0, 0.0), (0.0, 0.0, prof[-1][1])
    for j in range(segments):
        out += [_facet(foot, rings[0][(j + 1) % segments], rings[0][j]),
                _facet(top, rings[-1][j], rings[-1][(j + 1) % segments])]
    return "".join(out) + f"endsolid {name}\n"


# ---------------------------------------------------------------- cursor choreography


def cursor(points, size=(800, 450), move=0.9, rest=0.4):
    """An arrow cursor gliding between points on arcs, easing in and out, with a ripple where each move lands: an
    animated SVG to lay over a demo's frames."""
    pts = [(float(x), float(y)) for x, y in points]
    if len(pts) < 2:
        raise ValueError("a choreography needs two points or more")
    path, lengths = [f"M{pts[0][0]:g},{pts[0][1]:g}"], [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        bend = 0.2  # a hand moves on an arc, not a ruler
        c1 = (x0 + dx / 3 - dy * bend, y0 + dy / 3 + dx * bend)
        c2 = (x0 + 2 * dx / 3 - dy * bend, y0 + 2 * dy / 3 + dx * bend)
        path.append(f"C{c1[0]:g},{c1[1]:g} {c2[0]:g},{c2[1]:g} {x1:g},{y1:g}")
        bez = lambda t: tuple((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3
                              for p0, p1, p2, p3 in zip((x0, y0), c1, c2, (x1, y1)))  # noqa: E731
        samples = [bez(i / 16) for i in range(17)]
        lengths.append(lengths[-1] + sum(math.dist(a, b) for a, b in zip(samples, samples[1:])))
    if not lengths[-1]:
        raise ValueError("a choreography needs points that differ")
    total = (move + rest) * (len(pts) - 1)
    times, keys, splines = [0.0], [0.0], []
    for i in range(1, len(pts)):  # each move eases in and out, then the cursor rests on its target
        start = (i - 1) * (move + rest)
        times += [(start + move) / total, (start + move + rest) / total]
        keys += [lengths[i] / lengths[-1]] * 2
        splines += ["0.45 0 0.2 1", "0 0 1 1"]
    fmt = lambda xs: ";".join(f"{x:.4f}" for x in xs)  # noqa: E731
    ripples = "".join(
        f'<circle cx="{x:g}" cy="{y:g}" r="4" fill="none" stroke="#2f6fed" stroke-width="2" opacity="0">'
        f'<animate attributeName="r" from="4" to="22" dur="{rest:g}s" begin="{(i - 1) * (move + rest) + move:g}s"/>'
        f'<animate attributeName="opacity" values="0.8;0" dur="{rest:g}s" begin="{(i - 1) * (move + rest) + move:g}s"'
        f'/></circle>' for i, (x, y) in enumerate(pts[1:], 1))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" '
            f'viewBox="0 0 {size[0]} {size[1]}">{ripples}<path d="M0,0 L0,18 L5,13.5 L8.5,21 L11.5,19.5 L8,12.5 '
            f'L14,12.5 Z" fill="#ffffff" stroke="#111111" stroke-width="1.2" stroke-linejoin="round">'
            f'<animateMotion dur="{total:g}s" fill="freeze" path="{" ".join(path)}" calcMode="spline" '
            f'keyPoints="{fmt(keys)}" keyTimes="{fmt(times)}" keySplines="{";".join(splines)}"/></path></svg>\n')


# ---------------------------------------------------------------- Breakout, while the checks run


class Breakout:
    """A paddle, a ball and three rows of bricks on a w x h field of cells. step(dt) moves the ball in sub-steps of
    at most one cell, so it never tunnels through a brick; lines() draws the field."""
    BRICK, PADDLE = 3, 7

    def __init__(self, w=36, h=14):
        self.w, self.h = w, h
        n = (w - 1) // (self.BRICK + 1)
        left = (w - n * (self.BRICK + 1) + 1) // 2  # the wall centred
        self.bricks = {(left + i * (self.BRICK + 1), y) for y in (1, 2, 3) for i in range(n)}
        self.paddle, self.score, self.lives = (w - self.PADDLE) // 2, 0, 3
        self._serve()

    def _serve(self):
        self.ball, self.vel = [self.w / 2, self.h - 3.0], [7.0, -9.0]

    def move(self, cells):
        self.paddle = max(0, min(self.w - self.PADDLE, self.paddle + cells))

    @property
    def over(self):
        return self.lives <= 0 or not self.bricks

    def _brick_at(self, x, y):
        return next((b for b in self.bricks if b[1] == y and b[0] <= x < b[0] + self.BRICK), None)

    def step(self, dt):
        if self.over or dt <= 0:
            return
        n = max(1, math.ceil(max(abs(self.vel[0]), abs(self.vel[1])) * min(dt, 0.5)))
        for _ in range(n):
            d = min(dt, 0.5) / n
            x, y = self.ball[0] + self.vel[0] * d, self.ball[1] + self.vel[1] * d
            if not 0 <= x < self.w:
                self.vel[0], x = -self.vel[0], min(max(x, 0.0), self.w - 0.001)
            if y < 0:
                self.vel[1], y = -self.vel[1], 0.0
            hit = self._brick_at(int(x), int(y))
            if hit:
                self.bricks.discard(hit)
                self.score += 1
                self.vel[1], y = -self.vel[1], self.ball[1]
            if self.vel[1] > 0 and y >= self.h - 1:
                if self.paddle <= x < self.paddle + self.PADDLE:
                    off = (x - self.paddle) / self.PADDLE - 0.5  # where it lands on the paddle steers it
                    self.vel = [self.vel[0] + off * 8, -abs(self.vel[1])]
                    y = self.h - 1.001
                elif y >= self.h:
                    self.lives -= 1
                    self._serve()
                    return
            self.ball = [x, y]

    def lines(self):
        rows = [[" "] * self.w for _ in range(self.h)]
        for x, y in self.bricks:
            rows[y][x:x + self.BRICK] = ["▆"] * self.BRICK
        for i in range(self.PADDLE):
            rows[self.h - 1][self.paddle + i] = "▀"
        bx, by = int(self.ball[0]), int(self.ball[1])
        if 0 <= bx < self.w and 0 <= by < self.h:
            rows[by][bx] = "●"
        return ["".join(r) for r in rows]


# ---------------------------------------------------------------- the verb


def cmd_extras(args):
    import fmcli
    words = list(args.words or [])
    what = words[0] if words else ""
    if what in ("zine", "vase"):
        if args.events:
            try:
                events = load(args.events)
            except OSError as e:
                raise fmcli.UsageError(f"can't read {args.events}: {e} (fm code … --json > FILE records a run)")
        else:
            import fmcodetui
            events = fmcodetui.SAMPLE_RUN
        text = zine(events) if what == "zine" else vase(events)
        path = args.out or ("zine.svg" if what == "zine" else "vase.stl")
    elif what == "cursor":
        try:
            pts = [tuple(float(v) for v in p.split(",")) for p in words[1:]]
            text = cursor(pts) if all(len(p) == 2 for p in pts) else None
        except ValueError:
            text = None
        if not text:
            raise fmcli.UsageError("fm extras cursor X,Y X,Y … (two points or more, in the demo's pixels)")
        path = args.out or "cursor.svg"
    else:
        raise fmcli.UsageError("fm extras zine|vase [--events FILE] | cursor X,Y X,Y … [--out FILE]")
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    note = {"zine": "print it on one letter sheet, landscape, and fold it as page 8 says",
            "vase": "a closed solid: print it in your slicer's vase mode", "cursor": "lay it over the demo"}[what]
    return fmcli.out(args, {"out": path, "kind": what}, f"wrote {path}: {note}")
