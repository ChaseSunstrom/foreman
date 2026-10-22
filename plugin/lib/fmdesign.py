"""T-1506: fm design lint: the tells of generated design and craft slips in UI source, by text rules (stdlib only).

Precision first: a rule fires only where its text pattern is unambiguous, and a rule that can't be precise is left out.
ponytail: regex and small tokenizers over source text, not computed style; a headless browser would see cascade and
inheritance this can't. Rules that need the whole design (fonts, radius, shadows, tokens, keyframes, a reduced-motion
path) look across every file of one run, so lint the UI's root rather than one component.
An inline `design-lint: allow RULE why` comment silences RULE on its own line and the next; it needs the why."""
import bisect
import colorsys
import os
import re

RULES = [
    {"id": "generic-font", "why": "every type stack leads with Inter or the system face: the default look of generated UI",
     "fix": "pick a typeface with a voice for headings or body (a system stack can stay as the fallback)"},
    {"id": "purple-blue-gradient", "why": "the purple-to-blue gradient is the stock hero of generated design",
     "fix": "derive the gradient from the brand's own palette, or use a flat colour"},
    {"id": "one-radius", "why": "one border-radius on every element flattens the hierarchy (5+ uses, all equal)",
     "fix": "scale radius with size: small controls tighter, cards and sheets looser, pills and avatars round"},
    {"id": "same-shadow", "why": "the same soft grey shadow on every card (3+ uses, all equal): no elevation system",
     "fix": "define 2-3 elevation levels, tinted with the ink colour, and use them by meaning"},
    {"id": "img-alt", "why": "an img without alt: screen readers read the file name",
     "fix": "add alt describing what the image says, or alt=\"\" when it is decoration"},
    {"id": "reduced-motion", "why": "motion (transform, position or size) with no prefers-reduced-motion path in the run",
     "fix": "add @media (prefers-reduced-motion: reduce) that stills it (or useReducedMotion in the component)"},
    {"id": "layout-animation", "why": "animating width, height, top, left or margin re-lays the page every frame",
     "fix": "animate transform (translate/scale) and opacity instead"},
    {"id": "flash", "why": "a flash faster than 3 per second can trigger seizures (WCAG 2.3.1)",
     "fix": "slow it to at most 3 flashes a second, or stop it after 3 runs"},
    {"id": "unseeded-random", "why": "Math.random in rendering code: each render (and the server's) differs",
     "fix": "use a seeded generator (mulberry32(seed)) or compute the values once outside render"},
    {"id": "untokened-duration", "why": "a literal duration where the design defines duration tokens",
     "fix": "use the token (var(--dur-...)) so motion keeps one rhythm"},
]
BY_ID = {r["id"]: r for r in RULES}

EXTS = {".css", ".scss", ".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}
MARKUP = {".html", ".htm", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", "vendor", "dist"}
MAX_BYTES = 1_000_000  # bigger is generated or minified: skipped, and listed as skipped

GENERIC_FONTS = {"inter", "system-ui", "-apple-system", "blinkmacsystemfont", "segoe ui", "roboto", "helvetica neue",
                 "helvetica", "arial", "sans-serif", "ui-sans-serif"}
GENERIC_KEYWORDS = {"sans-serif", "serif", "monospace", "system-ui", "cursive", "fantasy", "ui-sans-serif", "ui-serif",
                    "ui-monospace", "ui-rounded"}
LAYOUT_PROPS = {"width", "height", "top", "left", "right", "bottom", "inset", "max-width", "max-height", "min-width",
                "min-height", "margin", "margin-top", "margin-bottom", "margin-left", "margin-right", "padding",
                "padding-top", "padding-bottom", "padding-left", "padding-right"}
MOTION_PROPS = LAYOUT_PROPS | {"transform", "translate", "rotate", "scale", "offset-distance", "background-position"}
FLASH_PROPS = {"opacity", "visibility", "background", "background-color", "color", "filter", "fill"}
NAMED = {"blue": "#0000ff", "royalblue": "#4169e1", "dodgerblue": "#1e90ff", "slateblue": "#6a5acd",
         "mediumslateblue": "#7b68ee", "cornflowerblue": "#6495ed", "purple": "#800080", "rebeccapurple": "#663399",
         "mediumpurple": "#9370db", "blueviolet": "#8a2be2", "darkviolet": "#9400d3", "violet": "#ee82ee",
         "indigo": "#4b0082", "black": "#000000", "gray": "#808080", "grey": "#808080"}
TW_PURPLE, TW_BLUE = {"purple", "violet", "fuchsia"}, {"blue", "indigo", "sky"}

NUM = r"(?:\d++\.?\d*+|\.\d++)"  # possessive: a long digit run never backtracks
TIME = re.compile(r"(?<![\w.-])(" + NUM + r")(ms|s)(?![\w-])")
DECL = re.compile(r"(?<![\w$.-])(--[\w-]+|[a-zA-Z][a-zA-Z-]*)\s*:\s*([^;{}]*)")
KEYFRAMES = re.compile(r"@(?:-webkit-)?keyframes\s+([\w-]+)\s*\{")
ALLOW = re.compile(r"design-lint:\s*allow\s+([\w-]+)([^\n]*)")
TAILWIND = re.compile(r"(?<![\w-])(?:from|via|to)-([a-z]+)-\d{2,3}(?![\w-])")
REDUCED = re.compile(r"prefers-reduced-motion|useReducedMotion|reducedMotion")


def _blank(text, pattern, flags=re.S):
    """Spaces over every match, newlines kept, so offsets and line numbers still point at the source."""
    return re.sub(pattern, lambda m: re.sub(r"[^\n]", " ", m.group()), text, flags=flags)


class Source:
    def __init__(self, path, text):
        self.path, self.raw = path, text
        ext = os.path.splitext(path)[1].lower()
        self.css_file, self.js = ext in (".css", ".scss"), ext in (".jsx", ".tsx")
        code = _blank(text, r"/\*.*?(?:\*/|\Z)")  # an unclosed comment runs to the end (and stays linear)
        if ext in MARKUP:
            code = _blank(code, r"<!--.*?(?:-->|\Z)")
        self.code = code  # comments blanked: markup and script rules read this
        if ext in MARKUP:  # CSS rules read only <style> blocks and style="" attributes
            keep, low, b = [" " if ch != "\n" else ch for ch in code], code.lower(), 0
            for m in re.finditer(r"<style\b[^>]*>|\sstyle\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", code, re.I):
                if m.start() < b:  # inside the block just kept: each character is copied once
                    continue
                if m.group().startswith("<"):  # a block runs to its </style>, or to the end when it never closes
                    a, b = m.end(), low.find("</style", m.end())
                    b = len(code) if b < 0 else b
                else:
                    g = 1 if m.group(1) is not None else 2
                    a, b = m.start(g), m.end(g)
                keep[a:b] = code[a:b]
            self.css = "".join(keep)
        else:
            self.css = code
        ends = _closers(self.css)
        self.nl = [i for i, ch in enumerate(text) if ch == "\n"]
        self.allowed = {}
        for i, line in enumerate(text.split("\n"), 1):
            for m in ALLOW.finditer(line):  # the why must hold a word once comment closers are gone
                if re.search(r"[A-Za-z]", re.sub(r"\*/|-->|[{}]", "", m.group(2))):
                    for n in (i, i + 1):
                        self.allowed.setdefault(n, set()).add(m.group(1))
        self.frames = [(m.group(1), m.end(), ends.get(m.end() - 1, len(self.css))) for m in KEYFRAMES.finditer(self.css)]
        self.frame_starts = [a for _, a, _ in self.frames]

    def line(self, offset):
        return bisect.bisect_left(self.nl, offset) + 1

    def frame_at(self, offset):
        """The @keyframes whose body holds offset (the innermost by start), or None."""
        i = bisect.bisect_right(self.frame_starts, offset) - 1
        return self.frames[i][0] if i >= 0 and offset < self.frames[i][2] else None


def _closers(text):
    """Each '{' offset → its '}' offset, in one pass; an unclosed brace is left out (it runs to the end)."""
    stack, out = [], {}
    for m in re.finditer(r"[{}]", text):
        if m.group() == "{":
            stack.append(m.start())
        elif stack:
            out[stack.pop()] = m.start()
    return out


def _split(value, seps):
    """Split at seps outside parentheses: commas between transition items, spaces between shorthand tokens."""
    out, depth, cur = [], 0, ""
    for ch in value:
        depth += (ch == "(") - (ch == ")")
        if depth == 0 and ch in seps:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return [x for x in out if x]


class Decl:
    def __init__(self, src, m):
        self.src, self.offset = src, m.start()
        prop = m.group(1)
        self.prop = prop if prop.startswith("--") else re.sub(r"[A-Z]", lambda x: "-" + x.group().lower(), prop)
        v = m.group(2).strip()[:2000]  # a real declaration is short; this bounds the per-value regexes
        if v and v[0] in "'\"`":  # a CSS-in-JS string value ends at its quote
            v = v[1:].split(v[0], 1)[0]
        elif src.js:  # ponytail: an unquoted JS object value ends at its line
            v = v.split("\n", 1)[0].rstrip(",")
        self.value = re.sub(r"\s+", " ", re.sub(r"!important", "", v)).strip()
        self.in_frames = src.frame_at(self.offset)
        self.line = src.line(self.offset)


def _seconds(token):
    m = TIME.fullmatch(token)
    return m and float(m.group(1)) / (1000 if m.group(2) == "ms" else 1)


def _rgb(text):
    """(r, g, b) in 0..1 for a hex, rgb(), hsl() or named colour; None when it isn't one."""
    t = text.strip().lower()
    t = NAMED.get(t, t)
    if t.startswith("#"):
        h = t[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) if len(h) in (6, 8) else None
    nums = re.findall(r"-?\d*\.?\d+%?", t[t.find("(") + 1:])
    if t.startswith("rgb") and len(nums) >= 3:
        return tuple(min(1.0, float(n[:-1]) / 100 if n.endswith("%") else float(n) / 255) for n in nums[:3])
    if t.startswith("hsl") and len(nums) >= 3:
        hue, s, li = (float(n.rstrip("%")) for n in nums[:3])
        return colorsys.hls_to_rgb((hue % 360) / 360, li / 100, s / 100)
    return None


COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}(?![\w-])|(?:rgba?|hsla?)\([^)]*\)|(?<![\w-])(?:" + "|".join(NAMED) + r")(?![\w-])")


def _colours(value):
    return [c for c in (_rgb(m.group()) for m in COLOUR.finditer(value)) if c]


def _family(rgb):
    hue, li, s = colorsys.rgb_to_hls(*rgb)
    if s < .3 or not .15 <= li <= .9:
        return None
    hue *= 360
    return "blue" if 195 <= hue < 250 else "purple" if 250 <= hue <= 300 else None


def _resolve(value, props):
    return re.sub(r"var\(\s*(--[\w-]+)[^)]*\)", lambda m: props.get(m.group(1), m.group()), value)


def _transitioned(d):
    """The properties a transition or transition-property declaration names ('all' and var() ones left out)."""
    items = _split(d.value, ",")
    return [] if d.value in ("none", "") else [i.split()[0] for i in items if i and not i.startswith("var(")]


class Run:
    def __init__(self, sources):
        self.sources = sources
        self.decls = [Decl(s, m) for s in sources for m in DECL.finditer(s.css)]
        self.props = {}
        for d in self.decls:
            if d.prop.startswith("--"):
                self.props.setdefault(d.prop, d.value)
        self.frames = {}
        for d in self.decls:
            if d.in_frames:
                self.frames.setdefault(d.in_frames, set()).add(d.prop)
        self.reduced = any(REDUCED.search(s.code) for s in sources)
        self.dur_tokens = [d for d in self.decls if d.prop.startswith("--") and TIME.fullmatch(d.value)]
        self.found = []

    def flag(self, rule, src, line, detail):
        self.found.append({"rule": rule, "file": src.path, "line": line, "detail": detail,
                           "why": BY_ID[rule]["why"], "fix": BY_ID[rule]["fix"]})

    def where(self, prop):
        return [d for d in self.decls if d.prop == prop and not d.in_frames]

    def anim_names(self, d):
        return [t for item in _split(d.value, ",") for t in _split(item, " ") if t in self.frames]

    # ---- generic tells: they look across the whole run
    def generic_font(self):
        stacks = []
        for d in self.decls:
            v = d.value
            if d.prop == "font":
                m = re.search(r"(?<![\w.])" + NUM + r"(?:px|rem|em|%|pt|vw|vh|ch|ex)(?:\s*/\s*[\w.%-]+)?\s+(.+)$", v)
                v = m.group(1) if m else ""
            elif d.prop.startswith("--"):
                if v.split(",")[-1].strip().strip("'\"").lower() not in GENERIC_KEYWORDS:
                    continue
            elif d.prop != "font-family":
                continue
            fams = [f.strip().strip("'\"").lower() for f in v.split(",")]
            if not fams[0] or "var(" in v or fams[0] in ("inherit", "initial", "unset") or \
                    {"monospace", "ui-monospace"} & set(fams):
                continue
            stacks.append((d, fams[0]))
        if stacks and all(f in GENERIC_FONTS for _, f in stacks):
            d = stacks[0][0]
            self.flag("generic-font", d.src, d.line, f"every type stack leads with a default face ({d.value})")

    def gradient(self):
        for d in self.decls:
            if "gradient(" in d.value:
                fams = {_family(c) for c in _colours(_resolve(d.value, self.props))}
                if {"blue", "purple"} <= fams:
                    self.flag("purple-blue-gradient", d.src, d.line, d.value[:80])
        for s in self.sources:
            if s.css_file:
                continue
            for i, line in enumerate(s.code.split("\n"), 1):
                fams = set(TAILWIND.findall(line))
                if fams & TW_PURPLE and fams & TW_BLUE:
                    self.flag("purple-blue-gradient", s, i, "Tailwind gradient " + " ".join(sorted(fams)))

    def one_radius(self):
        ds = [d for d in self.where("border-radius") if d.value.lower() not in ("0", "0px", "none", "inherit",
                                                                                 "initial", "unset")]
        if len(ds) >= 5 and len({d.value.lower() for d in ds}) == 1:
            self.flag("one-radius", ds[0].src, ds[0].line, f"border-radius: {ds[0].value} on all {len(ds)} uses")

    def same_shadow(self):
        ds = [d for d in self.where("box-shadow") if d.value.lower() not in ("none", "inherit", "initial", "unset")]
        if len(ds) >= 3 and len({d.value for d in ds}) == 1:
            cs = _colours(_resolve(ds[0].value, self.props))
            if cs and all(max(c) - min(c) < .02 for c in cs):
                self.flag("same-shadow", ds[0].src, ds[0].line, f"box-shadow: {ds[0].value} on all {len(ds)} uses")

    # ---- craft slips
    def img_alt(self):
        for s in self.sources:
            if s.css_file:
                continue
            upto = 0
            for m in re.finditer(r"<img(?![\w-])", s.code, re.I):
                if m.start() < upto:  # inside the last tag scanned: each character is scanned once
                    continue
                attrs, depth, quote, upto = None, 0, None, min(len(s.code), m.end() + 4000)
                for i in range(m.end(), upto):
                    ch = s.code[i]
                    if quote:
                        quote = None if ch == quote else quote
                    elif ch in "\"'" and not depth or ch == "`" and depth:
                        quote = ch
                    elif ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                    elif ch == ">" and depth <= 0:
                        attrs, upto = s.code[m.end():i], i
                        break
                if attrs is None or re.search(r"\{\s*\.\.\.", attrs):  # unterminated, or a spread may carry alt
                    continue
                if not re.search(r"(?:^|\s)(?:v-bind)?:?alt(?=\s*=|[\s/]|$)|\{\s*alt\s*\}", attrs):
                    self.flag("img-alt", s, s.line(m.start()), "<img " + " ".join(attrs.split())[:60] + ">")

    def motion(self):
        layout = []
        for d in self.decls:
            if d.prop in ("transition", "transition-property") and not d.in_frames:
                props = _transitioned(d)
                moving = [p for p in props if p in MOTION_PROPS]
                if moving and not self.reduced:
                    self.flag("reduced-motion", d.src, d.line, f"{d.prop}: {d.value}")
                layout += [(d, p) for p in props if p in LAYOUT_PROPS]
            elif d.prop in ("animation", "animation-name") and not d.in_frames and not self.reduced:
                moving = [n for n in self.anim_names(d) if self.frames[n] & MOTION_PROPS]
                if moving:
                    self.flag("reduced-motion", d.src, d.line, f"{d.prop}: {d.value} (@keyframes {moving[0]} moves)")
            elif d.in_frames and d.prop in LAYOUT_PROPS:
                layout.append((d, d.prop))
        seen = set()
        for d, p in layout:
            if id(d) not in seen:
                seen.add(id(d))
                self.flag("layout-animation", d.src, d.line, f"animates {p}" +
                          (f" in @keyframes {d.in_frames}" if d.in_frames else ""))

    def flash(self):
        for d in self.where("animation"):
            for item in _split(d.value, ","):
                toks = _split(item, " ")
                times = [x for x in (_seconds(t) for t in toks) if x is not None]
                names = [t for t in toks if t in self.frames and self.frames[t] & FLASH_PROPS]
                counts = [float(t) for t in toks if re.fullmatch(r"\d*\.?\d+", t)]
                runs = float("inf") if "infinite" in toks else (counts[0] if counts else 1)
                if not times or not names or not times[0] or runs <= 3:
                    continue
                rate = 1 / (times[0] * (2 if {"alternate", "alternate-reverse"} & set(toks) else 1))
                if rate > 3:
                    self.flag("flash", d.src, d.line, f"{names[0]} flashes {rate:.1f} times a second")

    def unseeded_random(self):
        for s in self.sources:
            if not s.css_file:
                for m in re.finditer(r"Math\.random\s*\(", s.code):
                    self.flag("unseeded-random", s, s.line(m.start()), "Math.random()")

    def untokened_duration(self):
        if not self.dur_tokens:
            return
        for d in self.decls:
            if d.prop in ("transition", "animation", "transition-duration", "animation-duration", "transition-delay",
                          "animation-delay") and not d.in_frames:
                bare = re.sub(r"var\([^)]*\)", "", d.value)  # a token's fallback is fine
                lit = [m.group() for m in TIME.finditer(bare) if _seconds(m.group()) >= .02]  # .01ms resets pass
                if lit:
                    self.flag("untokened-duration", d.src, d.line, f"{lit[0]} where tokens exist (e.g. "
                                                                   f"{self.dur_tokens[0].prop})")

    def check(self):
        for rule in (self.generic_font, self.gradient, self.one_radius, self.same_shadow, self.img_alt, self.motion,
                     self.flash, self.unseeded_random, self.untokened_duration):
            rule()
        by_path = {s.path: s for s in self.sources}
        kept = [f for f in self.found if f["rule"] not in by_path[f["file"]].allowed.get(f["line"], ())]
        return sorted(kept, key=lambda f: (f["file"], f["line"], f["rule"]))


def files(paths, skipped=None):
    """The UI source files under paths, sorted; vendored, hidden and over-size files left out (named in skipped)."""
    out = []
    for p in paths:
        if os.path.isfile(p):
            out += [p] if os.path.splitext(p)[1].lower() in EXTS else []
            continue
        for root, dirs, names in os.walk(p):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS)
            out += [os.path.join(root, n) for n in sorted(names)
                    if os.path.splitext(n)[1].lower() in EXTS and ".min." not in n]
    kept = []
    for f in out:
        try:
            size = os.path.getsize(f)
        except OSError:  # a dangling link
            continue
        if size > MAX_BYTES:
            if skipped is not None:
                skipped.append(f)
        else:
            kept.append(f)
    return kept


def lint(paths, skipped=None):
    sources = []
    for f in files(paths, skipped):
        with open(f, encoding="utf-8", errors="replace") as fh:
            sources.append(Source(f, fh.read()))
    return Run(sources).check()


def render(found):
    return [f"{f['file']}:{f['line']}: {f['rule']}: {f['detail']} — fix: {f['fix']}" for f in found]


def rules_help():
    return "rules (silence one with an inline comment: design-lint: allow RULE why):\n" + "\n".join(
        f"  {r['id']:<20} {r['why']}" for r in RULES)


def cmd_design(args):
    import sys
    import fmcli
    missing = [p for p in args.paths if not os.path.exists(p)]
    if missing:
        print(f"fm: design lint: no such file or directory: {', '.join(missing)}", file=sys.stderr)
        return 2
    skipped = []
    paths = files(args.paths, skipped)
    found, n = lint(paths), len(paths)
    text = "\n".join(render(found) + [f"{len(found)} finding(s) in {n} file(s)"]) if found else \
        f"design lint: clean ({n} file(s))"
    if skipped:
        text += f"\nskipped (over {MAX_BYTES // 1000} KB): " + ", ".join(skipped)
    fmcli.out(args, {"findings": found, "files": n, "skipped": skipped}, text)
    return 1 if found else 0
