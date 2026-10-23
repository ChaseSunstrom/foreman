"""T-1506: fm design lint: the tells of generated design and craft slips in UI source, by text rules (stdlib only).

Precision first: a rule fires only where its text pattern is unambiguous, and a rule that can't be precise is left out.
ponytail: regex and small tokenizers over source text, not computed style; a headless browser would see cascade and
inheritance this can't. Rules that need the whole design (fonts, radius, shadows, tokens, keyframes, a reduced-motion
path) look across every file of one run, so lint the UI's root rather than one component.
An inline `design-lint: allow RULE why` comment silences RULE on its own line (and the next, when the comment stands on
a line of its own); it needs the why.

T-1507: design tokens beside it: fm design palette (a light/dark role palette from one seed colour, OKLCH maths by
hand), fm design contrast (a token file's pairs, WCAG 2.x on the sRGB hex a browser paints) and fm design extract (a
repo's :root custom properties into DESIGN.md's Tokens section). `python3 fmdesign.py contrast …` runs without fm."""
import bisect
import colorsys
import json
import math
import os
import re
import stat

RULES = [
    {"id": "generic-font", "why": "every type stack leads with Inter or the system face: the default look of generated UI",
     "fix": "pick a typeface with a voice for headings or body (a system stack can stay as the fallback)"},
    {"id": "purple-blue-gradient", "why": "the purple-to-blue gradient is the stock hero of generated design",
     "fix": "derive the gradient from the brand's own palette, or use a flat colour"},
    {"id": "one-radius", "why": "one 6-16 px border-radius on every element flattens the hierarchy (5+ uses, all "
                                "equal; 0-4 px, circles and pills aside)",
     "fix": "scale radius with size: small controls tighter, cards and sheets looser, pills and avatars round"},
    {"id": "same-shadow", "why": "the same soft grey shadow on every card (3+ uses, all equal): no elevation system",
     "fix": "define 2-3 elevation levels, tinted with the ink colour, and use them by meaning"},
    {"id": "img-alt", "why": "an img without alt: screen readers read the file name",
     "fix": "add alt describing what the image says, or alt=\"\" when it is decoration"},
    {"id": "reduced-motion", "why": "motion (transform, position or size) with no prefers-reduced-motion path in the run",
     "fix": "add @media (prefers-reduced-motion: reduce) that stills it (or useReducedMotion in the component)"},
    {"id": "layout-animation", "why": "animating width, height, top, left, margin, padding, font-size or box-shadow, or "
                                      "transition: all, costs layout or paint every frame",
     "fix": "animate transform (translate/scale) and opacity; list the properties a transition covers"},
    {"id": "flash", "why": "a flash faster than 3 per second can trigger seizures (WCAG 2.3.1)",
     "fix": "slow it to at most 3 flashes a second, or stop it after 3 runs"},
    {"id": "unseeded-random", "why": "Math.random in rendering code: each render (and the server's) differs",
     "fix": "use a seeded generator (mulberry32(seed)) or compute the values once outside render"},
    {"id": "untokened-duration", "why": "a literal duration where the design defines duration tokens",
     "fix": "use the token (var(--dur-...)) so motion keeps one rhythm"},
    {"id": "afterglow", "why": "a state change (:hover, :focus, :active, [aria-*], .is-*) of colour, background, "
                               "transform or opacity with no transition: an instant jump reads as a glitch",
     "fix": "add a transition (or animation) on the element for the property, with a duration token"},
]
BY_ID = {r["id"]: r for r in RULES}
NOT_COVERED = ("not read: computed style and the cascade; .js/.ts files; tailwind.config theme values (but a fontFamily "
               "there keeps font-sans from counting as the system face); class names built in code other than "
               "class/className attributes, cn/clsx/twMerge/cva calls and @apply; side-specific rounded-t-* classes; an "
               "unquoted JSX style value past its line; animation longhands other than name, duration, iteration "
               "count and direction; afterglow matches a state block to a transition by selector text, so a transition set by a "
               "parent rule, a nested &:hover or the cascade is missed; animations run from JS (the Web Animations API, framer-motion props); Math.random in Vue and Svelte scripts")

EXTS = {".css", ".scss", ".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}
MARKUP = {".html", ".htm", ".vue", ".svelte"}
LINE_COMMENTS = {".scss", ".jsx", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", "bower_components", "vendor", "dist", "build", "out", "target", "venv",
             "htmlcov", "lcov-report"}  # built, vendored or generated (coverage reports): also fmcore.ui_paths
MAX_BYTES = 1_000_000  # bigger is generated or minified: skipped, and listed as skipped
MAX_FILES = 5000

GENERIC_FONTS = {"inter", "system-ui", "-apple-system", "blinkmacsystemfont", "segoe ui", "roboto", "helvetica neue",
                 "helvetica", "arial", "sans-serif", "ui-sans-serif"}
GENERIC_KEYWORDS = {"sans-serif", "serif", "monospace", "system-ui", "cursive", "fantasy", "ui-sans-serif", "ui-serif",
                    "ui-monospace", "ui-rounded"}
LAYOUT_PROPS = {"width", "height", "top", "left", "right", "bottom", "inset", "max-width", "max-height", "min-width",
                "min-height", "margin", "margin-top", "margin-bottom", "margin-left", "margin-right", "padding",
                "padding-top", "padding-bottom", "padding-left", "padding-right"}
COSTLY_PROPS = LAYOUT_PROPS | {"font-size", "box-shadow"}  # layout or paint every frame (motion.md)
MOTION_PROPS = LAYOUT_PROPS | {"transform", "translate", "rotate", "scale", "offset-distance", "background-position"}
COLOUR_PROPS = {"color", "background", "background-color", "fill", "filter", "border-color"}
EASINGS = {"ease", "linear", "ease-in", "ease-out", "ease-in-out", "step-start", "step-end"}
NAMED = {"blue": "#0000ff", "royalblue": "#4169e1", "dodgerblue": "#1e90ff", "slateblue": "#6a5acd",
         "mediumslateblue": "#7b68ee", "cornflowerblue": "#6495ed", "purple": "#800080", "rebeccapurple": "#663399",
         "mediumpurple": "#9370db", "blueviolet": "#8a2be2", "darkviolet": "#9400d3", "violet": "#ee82ee",
         "indigo": "#4b0082", "black": "#000000", "gray": "#808080", "grey": "#808080"}
TW_PURPLE, TW_BLUE = {"purple", "violet", "fuchsia"}, {"blue", "indigo", "sky"}
TW_RADIUS = {"": 4, "none": 0, "xs": 2, "sm": 4, "md": 6, "lg": 8, "xl": 12, "2xl": 16, "3xl": 24, "4xl": 32,
             "full": 9999}  # sm is 2 px in Tailwind 3, 4 in 4: either way under the band
TW_SHADOWS = {"shadow", "shadow-2xs", "shadow-xs", "shadow-sm", "shadow-md", "shadow-lg", "shadow-xl", "shadow-2xl",
              "shadow-inner"}

NUM = r"(?:\d++\.?\d*+|\.\d++)"  # possessive: a long digit run never backtracks
TIME = re.compile(r"(?<![\w.-])(" + NUM + r")(ms|s)(?![\w-])")
DECL = re.compile(r"(?<![\w$.-])(--[\w-]+|\$[\w-]+|[a-zA-Z][a-zA-Z-]*)\s*:\s*([^;{}]*)")
KEYFRAMES = re.compile(r"@(?:-webkit-)?keyframes\s+([\w-]+)\s*\{")
ALLOW = re.compile(r"design-lint:\s*allow\s+([\w-]+)([^\n]*)")
TAILWIND = re.compile(r"(?<![\w-])(?:from|via|to)-([a-z]+)-\d{2,3}(?![\w-])")
STATE = re.compile(r":(?:hover|focus-visible|focus-within|focus|active)\b|\[aria-[^\]]*\]|\.is-[\w-]+")
AFTERGLOW_PROPS = {"color", "background", "background-color", "transform", "opacity"}
REDUCED = re.compile(r"prefers-reduced-motion|useReducedMotion|reducedMotion")
# the {0,4000} bounds keep an unclosed quote or brace from rescanning the file at every match attempt
CLASS_ATTR = re.compile(r"(?<![\w:-])(?:class|className)\s*=\s*(?:\"([^\"]{0,4000})\"|'([^']{0,4000})'|"
                        r"\{\s*`([^`]{0,4000})`\s*\}|\{\s*\"([^\"]{0,4000})\"\s*\}|\{\s*'([^']{0,4000})'\s*\})")
CLASS_CALL = re.compile(r"\b(?:cn|clsx|classnames|classNames|twMerge|cva)\(([^()]{0,4000})\)")
QUOTED = re.compile(r"\"([^\"\n]*)\"|'([^'\n]*)'|`([^`]*)`")
NEXT_FONT = re.compile(r"import\s*\{([^}]{0,2000})\}\s*from\s*['\"]next/font/(google|local)['\"]")
GOOGLE_FONTS = re.compile(r"fonts\.googleapis\.com/css2?\?[^\"'\s)>]*")


def _blank(text, pattern, flags=re.S):
    """Spaces over every match, newlines kept, so offsets and line numbers still point at the source."""
    return re.sub(pattern, lambda m: re.sub(r"[^\n]", " ", m.group()), text, flags=flags)


def _keep(code, spans):
    """code with everything outside spans blanked (newlines kept)."""
    keep = [" " if ch != "\n" else ch for ch in code]
    for a, b in spans:
        keep[a:b] = code[a:b]
    return "".join(keep)


def _blocks(code, tag):
    """(start, end) of each <tag>…</tag> body, an unclosed one running to the end; each character is visited once."""
    low, spans, b = code.lower(), [], 0
    for m in re.finditer(r"<" + tag + r"\b[^>]*>", code, re.I):
        if m.start() < b:
            continue
        a, b = m.end(), low.find("</" + tag, m.end())
        b = len(code) if b < 0 else b
        spans.append((a, b))
    return spans


class Source:
    def __init__(self, path, text):
        self.path, self.raw = path, text
        self.ext = ext = os.path.splitext(path)[1].lower()
        self.css_file, self.js = ext in (".css", ".scss"), ext in (".jsx", ".tsx")
        comments = [r"/\*.*?(?:\*/|\Z)"]  # an unclosed comment runs to the end (and stays linear)
        if ext in LINE_COMMENTS:
            comments.append(r"(?<!\S)//[^\n]*")  # after a space or at a line's start: not https:// or url(//…)
        if ext in MARKUP:
            comments.append(r"<!--.*?(?:-->|\Z)")
        self.code = code = _blank(text, "|".join(comments))  # one pass: a // inside /* */ and the reverse both hold
        if ext in MARKUP:  # CSS rules read only <style> blocks and style="" attributes
            spans = _blocks(code, "style") + [m.span(1) if m.group(1) is not None else m.span(2) for m in
                                              re.finditer(r"\sstyle\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", code, re.I)]
            self.css = _keep(code, spans)
        else:
            self.css = code
        # T-1507: braces and semicolons inside a CSS string (content: "}") are text, not structure; JSX keeps its
        # own (an apostrophe in JSX text is no quote)
        self.braces = self.css if self.js else re.sub(r"\"[^\"\n]*\"|'[^'\n]*'",
                                                      lambda m: re.sub(r"[{};]", " ", m.group()), self.css)
        ends = _closers(self.braces)
        self.opens = sorted(ends)
        self.nl = [i for i, ch in enumerate(text) if ch == "\n"]
        self.allowed = {}
        for i, line in enumerate(text.split("\n"), 1):
            for m in ALLOW.finditer(line):  # the why must hold a word once comment closers are gone
                if re.search(r"[A-Za-z]", re.sub(r"\*/|-->|[{}]", "", m.group(2))):
                    rest = re.sub(r"<!--.*?(?:-->|$)|/\*.*?(?:\*/|$)|//.*$|\{\s*\}", "", line).strip()
                    for n in (i, i + 1) if not rest else (i,):  # a comment alone on its line covers the next
                        self.allowed.setdefault(n, set()).add(m.group(1))
        self.frames = [(m.group(1), m.end(), ends.get(m.end() - 1, len(self.css))) for m in KEYFRAMES.finditer(self.css)]
        self.frame_starts = [a for _, a, _ in self.frames]
        self.class_strings = [] if self.css_file else \
            [(m.start(g), m.group(g)) for m in CLASS_ATTR.finditer(code) for g in range(1, 6) if m.group(g) is not None]
        if not self.css_file:
            for m in CLASS_CALL.finditer(code):
                self.class_strings += [(m.start(1) + q.start(), q.group()) for q in QUOTED.finditer(m.group(1))]
        self.class_strings += [(m.start(1), m.group(1)) for m in re.finditer(r"@apply\s+([^;{}]*)", self.css)]

    def line(self, offset):
        return bisect.bisect_left(self.nl, offset) + 1

    def frame_at(self, offset):
        """The @keyframes whose body holds offset (the innermost by start), or None."""
        i = bisect.bisect_right(self.frame_starts, offset) - 1
        return self.frames[i][0] if i >= 0 and offset < self.frames[i][2] else None

    def block_of(self, offset):
        """The offset of the nearest '{' before offset: declarations of one rule share it."""
        i = bisect.bisect_right(self.opens, offset) - 1
        return self.opens[i] if i >= 0 else -1

    def tokens(self):
        """(offset, class) for each class in the class strings, variant prefixes (md:, hover:) dropped."""
        for base, text in self.class_strings:
            for m in re.finditer(r"[^\s\"'`]+", text):
                tok = m.group()
                if "$" not in tok and "{" not in tok and "}" not in tok:
                    yield base + m.start(), tok.rsplit(":", 1)[-1]


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
        self.prop = prop if prop[0] in "-$" else re.sub(r"[A-Z]", lambda x: "-" + x.group().lower(), prop)
        # a value cut at '{' is built at runtime: ${…} in a template, SCSS #{$r}, Svelte {r}px
        self.dynamic = m.end() < len(src.css) and src.css[m.end()] == "{"
        v = m.group(2).strip()[:2000]  # a real declaration is short; this bounds the per-value regexes
        if v and v[0] in "'\"`":  # a CSS-in-JS string value ends at its quote
            v = v[1:].split(v[0], 1)[0]
        elif src.js:  # ponytail: an unquoted JS object value ends at its line
            v = v.split("\n", 1)[0].rstrip(",")
        self.value = re.sub(r"\s+", " ", re.sub(r"!important", "", v)).strip()
        self.in_frames = src.frame_at(self.offset)
        self.block = src.block_of(self.offset)
        self.line = src.line(self.offset)


def _seconds(token):
    m = TIME.fullmatch(token)
    return m and float(m.group(1)) / (1000 if m.group(2) == "ms" else 1)


def _px(value, js=False):
    """A length in px (rem and em at 16 px; a bare number in a JSX style object is px), else None."""
    m = re.fullmatch("(" + NUM + r")(px|rem|em)?", value)
    if not m or not m.group(2) and not (js or float(m.group(1)) == 0):
        return None
    return float(m.group(1)) * (16 if m.group(2) in ("rem", "em") else 1)


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
    hue = round(hue * 360, 1)  # hsl(300 …) comes back as 299.99…: magenta must stay magenta
    return "blue" if 195 <= hue < 250 else "purple" if 250 <= hue < 300 else None


def _resolve(value, props):
    """var(--x) and SCSS $x replaced by their definitions in the run (two levels)."""
    for _ in range(2):
        value = re.sub(r"var\(\s*(--[\w-]+)[^)]*\)", lambda m: props.get(m.group(1), m.group()), value)
        value = re.sub(r"\$[\w-]+", lambda m: props.get(m.group(), m.group()), value)
    return value


def _transitioned(d):
    """The properties a transition or transition-property names: 'all' for all and for an item that starts with its
    duration or easing; var() items left out."""
    if d.value in ("none", ""):
        return []
    out = []
    for item in _split(d.value, ","):
        first = item.split()[0]
        if first.startswith("var("):
            continue
        timed = TIME.fullmatch(first) or first in EASINGS or first.startswith(("cubic-bezier(", "steps("))
        out.append("all" if d.prop == "transition" and timed else first)
    return out


HANDLER_CALL = re.compile(r"(?:\buse(?:Layout|Insertion)?Effect|\buseCallback|\bsetTimeout|\bsetInterval|"
                          r"\brequestAnimationFrame|\baddEventListener|\.then|\.catch|\bon[A-Z]\w*)\s*$")
ASSIGNED_ARROW = re.compile(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^()]*\)|[\w$]+)\s*$")
NAMED_FN = re.compile(r"function\s*\*?\s*([A-Za-z_$][\w$]*)\s*\([^()]*\)$")
METHOD = re.compile(r"(?:^|[\s;{}])([A-Za-z_$][\w$]*)\s*\([^()]*\)$")
JS_ASSIGN = re.compile(r"(?:const|let|var)\s+[^=;]*=$|\breturn$")


def _in_render(code, pos):
    """True when pos sits in a render path: a JSX attribute or child expression, a component's body (a capitalised
    function or arrow, or render()), and not inside an event handler, an effect, a timer or a named helper.
    ponytail: brackets inside strings and comments are counted too; a window of 3000 characters back."""
    depth, i, lo = 0, pos - 1, max(0, pos - 3000)
    while i >= lo:
        ch = code[i]
        if ch in ")]}":
            depth += 1
        elif ch in "([{":
            if depth:
                depth -= 1
            else:
                before = code[max(0, i - 200):i]
                b = before.rstrip()
                if ch == "(" and HANDLER_CALL.search(before):
                    return False
                if ch == "{":
                    if re.search(r"\bon[A-Z]\w*\s*=\s*$", before):
                        return False
                    if b.endswith(")"):
                        m = NAMED_FN.search(b)
                        if m:
                            return m.group(1)[0].isupper()
                        m = METHOD.search(b)
                        if m and m.group(1) not in ("if", "for", "while", "switch", "catch", "with"):
                            return m.group(1) == "render"
                    elif not b.endswith(("=>", "$", "{")) and not JS_ASSIGN.search(b):
                        if re.search(r"[\w-]\s*=$", b) or b.endswith(">"):
                            return True  # a JSX attribute's or child's expression
        elif ch == ">" and not depth and i and code[i - 1] == "=":
            m = ASSIGNED_ARROW.search(code[max(0, i - 201):i - 1])
            if m:
                return m.group(1)[0].isupper()
            i -= 1
        i -= 1
    return False


class Run:
    def __init__(self, sources, tw_fonts=False):
        self.sources, self.tw_fonts = sources, tw_fonts
        self.order = {s.path: n for n, s in enumerate(sources)}
        self.decls = [Decl(s, m) for s in sources for m in DECL.finditer(s.css)]
        self.props = {}
        for d in self.decls:
            if d.prop[0] in "-$" and not d.in_frames:
                self.props.setdefault(d.prop, d.value)
        self.frames = {}
        for d in self.decls:
            if d.in_frames:
                self.frames.setdefault(d.in_frames, []).append((d.prop, d.value))
        self.reduced = any(REDUCED.search(s.code) for s in sources)
        self.dur_tokens = [d for d in self.decls if d.prop[0] in "-$" and TIME.fullmatch(d.value)]
        self.tokens = [(s, off, tok) for s in sources for off, tok in s.tokens()]
        self.found = []

    def flag(self, rule, src, line, detail):
        self.found.append({"rule": rule, "file": src.path, "line": line, "detail": detail,
                           "why": BY_ID[rule]["why"], "fix": BY_ID[rule]["fix"]})

    def first(self, uses):
        return min(uses, key=lambda u: (self.order[u[0].path], u[1]))

    def where(self, prop):
        return [d for d in self.decls if d.prop == prop and not d.in_frames]

    def frame_props(self, name):
        return {p for p, _ in self.frames.get(name, ())}

    def flashes(self, name):
        """The keyframes reach opacity 0, hide, or change a colour."""
        for p, v in self.frames.get(name, ()):
            if p == "opacity" and _px(v.rstrip("%")) == 0 or p == "visibility" and v == "hidden" or p in COLOUR_PROPS:
                return True
        return False

    # ---- generic tells: they look across the whole run
    def generic_font(self):
        stacks = []  # (source, line, primary family)
        for d in self.decls:
            v = d.value
            if d.prop == "font":
                m = re.search(r"(?<![\w.])" + NUM + r"(?:px|rem|em|%|pt|vw|vh|ch|ex)(?:\s*/\s*[\w.%-]+)?\s+(.+)$", v)
                v = m.group(1) if m else ""
            elif d.prop[0] in "-$":
                if v.split(",")[-1].strip().strip("'\"").lower() not in GENERIC_KEYWORDS:
                    continue
            elif d.prop != "font-family":
                continue
            fams = [f.strip().strip("'\"").lower() for f in v.split(",")]
            if not fams[0] or "var(" in v or "$" in v or fams[0] in ("inherit", "initial", "unset") or \
                    {"monospace", "ui-monospace"} & set(fams):
                continue
            stacks.append((d.src, d.line, fams[0]))
        for s in self.sources:
            if s.js:
                for m in NEXT_FONT.finditer(s.code):
                    names = [n.split(" as ")[0].strip().replace("_", " ").lower() for n in m.group(1).split(",")]
                    stacks += [(s, s.line(m.start()), "local" if m.group(2) == "local" else n) for n in names
                               if n and not re.search(r"mono|code", n)]
            for m in GOOGLE_FONTS.finditer(s.code):
                for f in re.findall(r"family=([^&:;]+)", m.group()):
                    f = f.replace("+", " ").replace("%20", " ").strip().lower()
                    if f and not re.search(r"mono|code", f):
                        stacks.append((s, s.line(m.start()), f))
        if "--font-sans" not in self.props and not self.tw_fonts:  # Tailwind's default font-sans is the system face
            stacks += [(s, s.line(off), "ui-sans-serif") for s, off, tok in self.tokens if tok == "font-sans"]
        stacks += [(s, s.line(off), "ui-serif") for s, off, tok in self.tokens if tok == "font-serif"]
        if stacks and all(f in GENERIC_FONTS for _, _, f in stacks):
            s, line, f = self.first(stacks)
            self.flag("generic-font", s, line, f"every type stack leads with a default face ({f})")

    def gradient(self):
        for d in self.decls:
            if "gradient(" in d.value:
                fams = {_family(c) for c in _colours(_resolve(d.value, self.props))}
                if {"blue", "purple"} <= fams:
                    self.flag("purple-blue-gradient", d.src, d.line, d.value[:80])
        for s in self.sources:
            for base, text in s.class_strings:
                hits = list(TAILWIND.finditer(text))
                fams = {m.group(1) for m in hits}
                if fams & TW_PURPLE and fams & TW_BLUE:
                    self.flag("purple-blue-gradient", s, s.line(base + hits[0].start()),
                              "Tailwind gradient " + " ".join(m.group() for m in hits))

    def one_radius(self):
        uses = []  # (source, line, key, px)
        for d in self.where("border-radius"):
            v = _resolve(d.value, self.props).lower()
            if d.dynamic:
                uses.append((d.src, d.line, ("dynamic", d.offset), None))
                continue
            if v in ("none", "inherit", "initial", "unset", "50%"):
                continue
            px = _px(v, d.src.js)
            if px is None or 4 < px < 999:
                uses.append((d.src, d.line, f"{px:g}px" if px is not None else v, px))
        for s, off, tok in self.tokens:
            m = re.fullmatch(r"rounded(?:-(none|xs|sm|md|lg|xl|[234]xl|full)|-\[([^\]]+)\])?", tok)
            if m:
                px = TW_RADIUS[m.group(1) or ""] if m.group(2) is None else _px(m.group(2))
                if px is None or 4 < px < 999:
                    uses.append((s, s.line(off), f"{px:g}px" if px is not None else tok, px))
        if len(uses) >= 5 and len({u[2] for u in uses}) == 1 and uses[0][3] is not None and 6 <= uses[0][3] <= 16:
            s, line, key, _ = self.first(uses)
            self.flag("one-radius", s, line, f"border-radius {key} on all {len(uses)} uses")

    def same_shadow(self):
        uses = []  # (source, line, key)
        for d in self.where("box-shadow"):
            v = _resolve(d.value, self.props)
            if d.dynamic:
                uses.append((d.src, d.line, ("dynamic", d.offset)))
            elif v.lower() not in ("none", "inherit", "initial", "unset"):
                uses.append((d.src, d.line, v))
        tinted = False
        for s, off, tok in self.tokens:
            if tok in TW_SHADOWS:
                uses.append((s, s.line(off), "tw:" + tok))
            elif re.fullmatch(r"shadow-(?!none$)[a-z]+(?:-\d{2,3})?(?:/\d+)?", tok):
                tinted = True  # shadow-indigo-500/20: a coloured shadow somewhere
        if len(uses) < 3 or len({u[2] for u in uses}) != 1 or isinstance(uses[0][2], tuple):
            return
        key = uses[0][2]
        if key.startswith("tw:"):
            grey = not tinted
        else:
            cs = _colours(key)
            grey = cs and all(max(c) - min(c) < .02 for c in cs)
        if grey:
            s, line, _ = self.first(uses)
            self.flag("same-shadow", s, line, f"box-shadow {key.removeprefix('tw:')} on all {len(uses)} uses")

    # ---- craft slips
    def img_alt(self):
        named = re.compile(r"(?:^|\s)(?:v-bind:|:)?alt(?=\s*=|[\s/]|$)|(?:^|\s)\[(?:attr\.)?alt\]\s*=|\{\s*alt\s*\}|"
                           r"aria-hidden\s*=\s*[\"'{]*\s*true|role\s*=\s*[\"'](?:presentation|none)[\"']|"
                           r"aria-label(?:ledby)?\s*=")
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
                if not named.search(attrs):
                    self.flag("img-alt", s, s.line(m.start()), "<img " + " ".join(attrs.split())[:60] + ">")

    def motion(self):
        costly = []
        for d in self.decls:
            if d.prop in ("transition", "transition-property") and not d.in_frames:
                props = _transitioned(d)
                if [p for p in props if p in MOTION_PROPS] and not self.reduced:
                    self.flag("reduced-motion", d.src, d.line, f"{d.prop}: {d.value}")
                bad = [p for p in props if p in COSTLY_PROPS or p == "all"]
                if bad:
                    costly.append((d, "transition: all" if bad[0] == "all" else f"animates {bad[0]}"))
            elif d.prop in ("animation", "animation-name") and not d.in_frames and not self.reduced:
                names = [t for item in _split(d.value, ",") for t in _split(item, " ") if t in self.frames]
                moving = [n for n in names if self.frame_props(n) & MOTION_PROPS]
                if moving:
                    self.flag("reduced-motion", d.src, d.line, f"{d.prop}: {d.value} (@keyframes {moving[0]} moves)")
            elif d.in_frames and d.prop in COSTLY_PROPS:
                costly.append((d, f"animates {d.prop} in @keyframes {d.in_frames}"))
        for d, detail in costly:
            self.flag("layout-animation", d.src, d.line, detail)

    def flash(self):
        specs = []  # (decl to report, tokens)
        blocks, shorthand = {}, {}  # one rule's animation longhands, and its shorthand
        for d in self.decls:
            if d.prop.startswith("animation-") and not d.in_frames:
                blocks.setdefault((d.src.path, d.block), {})[d.prop] = d
        for d in self.where("animation"):
            shorthand.setdefault((d.src.path, d.block), d)
            longs = blocks.get((d.src.path, d.block), {})
            if not ("animation-name" in longs or "animation-duration" in longs):
                specs += [(d, _split(item, " ")) for item in _split(d.value, ",")]
        for key, longs in blocks.items():
            if "animation-name" not in longs and "animation-duration" not in longs:
                continue
            anchor = longs.get("animation-duration") or longs["animation-name"]
            toks = _split(_split(shorthand[key].value, ",")[0], " ") if key in shorthand else []
            for prop in ("animation-name", "animation-duration", "animation-iteration-count", "animation-direction"):
                if prop in longs:
                    toks.append(_split(longs[prop].value, ",")[0])
            specs.append((anchor, toks))
        for d, toks in specs:
            times = [x for x in (_seconds(t) for t in toks) if x is not None]
            names = [t for t in toks if t in self.frames and self.flashes(t)]
            counts = [float(t) for t in toks if re.fullmatch(NUM, t)]
            runs = float("inf") if "infinite" in toks else (counts[-1] if counts else 1)
            if not times or not names or not times[-1] or runs <= 3:
                continue
            dur = times[-1] if d.prop == "animation-duration" else times[0]
            rate = 1 / (dur * (2 if {"alternate", "alternate-reverse"} & set(toks) else 1))
            if rate > 3:
                self.flag("flash", d.src, d.line, f"{names[0]} flashes {rate:.1f} times a second")

    def unseeded_random(self):
        for s in self.sources:
            if s.js:
                code, judge = s.code, _in_render
            elif s.ext in (".vue", ".svelte"):  # the template is the render path; scripts aren't read
                spans, last = [], 0
                for a, b in sorted(_blocks(s.code, "script") + _blocks(s.code, "style")):
                    spans.append((last, a))
                    last = max(last, b)
                code, judge = _keep(s.code, spans + [(last, len(s.code))]), _in_template
            else:
                continue
            for n, m in enumerate(re.finditer(r"Math\.random\s*\(", code)):
                if n >= 200:  # ponytail: a file with more is generated
                    break
                if judge(code, m.start()):
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

    def afterglow(self):
        # ponytail: the element is its selector minus state parts, matched as text across all files; no cascade
        base = lambda sel: re.sub(r"\s+", " ", STATE.sub("", sel)).strip()
        sel_of = lambda d: [x for x in re.split(r",", re.split(r"[;{}]", d.src.css[:d.block])[-1]) if x.strip()] \
            if d.block >= 0 else []
        moves = set()  # elements that transition or animate something (a nonzero time, or a named property/animation)
        for d in self.decls:
            if d.prop in ("transition", "transition-property", "transition-duration", "animation", "animation-name") \
                    and not d.in_frames and d.value and d.value.lower() != "none":
                named = d.prop in ("transition-property", "animation-name")
                # a var() duration is a token this run can't resolve; the lint asks for tokens, so it counts (T-1707)
                if named or "var(" in d.value or any(_seconds(m.group()) > 0 for m in TIME.finditer(d.value)):
                    moves.update(base(x) for x in sel_of(d))
        if "*" in moves:  # a transition on * covers every element
            return

        def covered(x):  # T-1707: .kiln .mark covers .kiln .tile:hover .mark; .tabs button covers .tabs [aria-pressed]
            x = x.strip()
            b, bare = base(x).split(), STATE.sub("", x) != STATE.sub("", x).rstrip()  # bare: a state on a descendant
            for m in moves:
                mp = m.split()
                if bare and b and m.startswith(" ".join(b) + " "):
                    return True
                if b and mp and mp[-1] == b[-1]:
                    rest = iter(b)
                    if all(p in rest for p in mp):  # moving's compounds in order within the state's
                        return True
            return False
        quiet, seen = {}, set()  # source → spans of prefers-reduced-motion: reduce blocks; blocks already flagged
        for d in self.decls:
            if d.prop not in AFTERGLOW_PROPS or d.in_frames or d.src.js or d.dynamic or (d.src.path, d.block) in seen:
                continue
            sels = [x for x in sel_of(d) if STATE.search(x)]
            # a nested &:hover is skipped: ponytail: resolving & against the parent block is not done
            if not sels or any("&" in x or covered(x) for x in sels):
                continue
            if d.src.path not in quiet:
                ends = _closers(d.src.css)
                quiet[d.src.path] = [(m.end(), ends.get(m.end() - 1, len(d.src.css)))
                                     for m in re.finditer(r"@media[^{]*prefers-reduced-motion\s*:\s*reduce[^{]*\{",
                                                          d.src.css)]
            if not any(a <= d.offset < b for a, b in quiet[d.src.path]):
                seen.add((d.src.path, d.block))
                sel = sels[0].strip()
                self.flag("afterglow", d.src, d.line, f"{d.prop} changes on {sel} with no transition on "
                          f"'{base(sel)}' in this run (matched by selector text); add one, or silence with "
                          f"design-lint: allow afterglow <why>")

    def check(self):
        for rule in (self.generic_font, self.gradient, self.one_radius, self.same_shadow, self.img_alt, self.motion,
                     self.flash, self.unseeded_random, self.untokened_duration, self.afterglow):
            rule()
        by_path = {s.path: s for s in self.sources}
        kept = [f for f in self.found if f["rule"] not in by_path[f["file"]].allowed.get(f["line"], ())]
        return sorted(kept, key=lambda f: (self.order[f["file"]], f["line"], f["rule"]))


def _in_template(code, pos):
    """A Vue or Svelte template expression, unless it is an event handler's (on:click, @click, v-on:)."""
    return not re.search(r"(?:\bon:\w+|@\w+|v-on:\w+)\s*=\s*[\"{][^\"}]*$", code[max(0, pos - 300):pos])


def _read(path, strict=False):
    """(text, None) for a regular file up to MAX_BYTES, else (None, why). Never blocks on a FIFO or device. strict:
    text that isn't UTF-8 is refused rather than decoded with replacement characters (a file fm will write back)."""
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    except OSError as e:
        return None, e.strerror.lower() if e.strerror else str(e)
    with os.fdopen(fd, "rb") as fh:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, "not a regular file"
        if st.st_size > MAX_BYTES:
            return None, f"over {MAX_BYTES // 1000} KB"
        try:
            data = fh.read(MAX_BYTES + 1)
        except OSError as e:
            return None, e.strerror.lower() if e.strerror else str(e)
    if len(data) > MAX_BYTES:
        return None, f"over {MAX_BYTES // 1000} KB"
    try:
        return data.decode("utf-8", errors="strict" if strict else "replace"), None
    except UnicodeDecodeError as e:
        return None, f"not UTF-8 text (byte {e.start}); convert it to UTF-8 first"


def collect(paths):
    """(files, skipped, configs, empty): the UI source files under paths in order, each real file once; what was left
    out and why; tailwind.config files met; the paths that hold no UI file at all."""
    files, skipped, configs, empty, seen = [], [], [], [], set()
    for p in paths:
        found = []
        if os.path.isfile(p):
            found = [p] if os.path.splitext(p)[1].lower() in EXTS else []
        elif os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS)
                for n in sorted(names):
                    if n.startswith("tailwind.config."):
                        configs.append(os.path.join(root, n))
                    elif os.path.splitext(n)[1].lower() in EXTS and ".min." not in n:
                        found.append(os.path.join(root, n))
                if len(found) > MAX_FILES:
                    break
        if not found:
            empty.append(p)
        for f in found:
            real = os.path.realpath(f)
            if real in seen:
                continue
            seen.add(real)
            if len(files) >= MAX_FILES:
                skipped.append({"file": p, "why": f"over {MAX_FILES} files: the rest not linted"})
                break
            files.append(f)
    return files, skipped, configs, empty


def run(paths):
    """(findings, files linted, skipped, empty paths)."""
    files, skipped, configs, empty = collect(paths)
    sources = []
    for f in files:
        text, why = _read(f)
        if why:
            skipped.append({"file": f, "why": why})
        else:
            sources.append(Source(f, text))
    tw_fonts = any("fontFamily" in (_read(c)[0] or "") for c in configs)
    return Run(sources, tw_fonts).check(), [s.path for s in sources], skipped, empty


def lint(paths, skipped=None):
    found, _, sk, _ = run(paths)
    if skipped is not None:
        skipped.extend(sk)
    return found


def render(found):
    return [f"{f['file']}:{f['line']}: {f['rule']}: {f['detail']} — fix: {f['fix']}" for f in found]


def rules_help():
    return ("rules (silence one with an inline comment: design-lint: allow RULE why):\n" + "\n".join(
        f"  {r['id']:<20} {r['why']}" for r in RULES) + "\n\n" + NOT_COVERED + ".")


# ---------------------------------------------------------------- T-1507: tokens (palette, contrast, extract)

ROLES = ["surface", "surface-raised", "surface-sunken", "text", "text-muted", "border", "accent", "on-accent",
         "accent-subtle", "on-subtle"]  # type-and-colour.md's roles, less status, hover and focus (focus: the accent)
SURFACES = ("surface", "surface-raised", "surface-sunken")
# (fg, bg, light floor, dark floor): text on every surface it lands on, edges 3:1, body text 7:1 in dark (Foreman's)
PAIRS = [(fg, s, need, 7 if fg == "text" else need) for fg, need in
         (("text", 4.5), ("text-muted", 4.5), ("border", 3), ("accent", 4.5)) for s in SURFACES] + \
        [("on-accent", "accent", 4.5, 4.5), ("on-subtle", "accent-subtle", 4.5, 4.5)]
MARGIN = 0.03  # palette aims this far past each floor: one 8-bit channel step can't land a pair under it
F = r"[-+]?(?:\d++\.?\d*+|\.\d++)(?:e[-+]?\d++)?"  # possessive, as NUM: a long digit run never backtracks
OKLCH = re.compile(r"oklch\(\s*(" + F + r")(%?)\s+(" + F + r")(%?)\s+(" + F + r"|none)(?:deg)?\s*(?:/\s*(" + F +
                   r")(%?)\s*)?\)", re.I)


def _cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)


def _linear(L, C, h):
    """Linear sRGB of an OKLCH colour, unclipped (Björn Ottosson's OKLab matrices)."""
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l, m, s = ((L + x * a + y * b) ** 3 for x, y in
               ((0.3963377774, 0.2158037573), (-0.1055613458, -0.0638541728), (-0.0894841775, -1.2914855480)))
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def in_gamut(L, C, h):
    return all(-1e-4 <= v <= 1 + 1e-4 for v in _linear(L, C, h))


def _encode(v):
    """Linear light to the sRGB curve, clipped as the browser clips an out-of-gamut value."""
    v = min(max(v, 0.0), 1.0)
    return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def oklch_of(rgb):
    """(L, C, h) of an sRGB colour in 0..1."""
    r, g, b = (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb)
    l, m, s = (_cbrt(x) for x in (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
                                  0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
                                  0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b))
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def _oklch_parts(m):
    """(L, C, h) of an OKLCH match, or None when its alpha is below 1 (a translucent colour has no contrast alone) or a
    number isn't finite (1e999)."""
    if m.group(6) is not None and not float(m.group(6)) / (100 if m.group(7) else 1) >= 1:
        return None
    L = float(m.group(1)) / (100 if m.group(2) else 1)
    C = float(m.group(3)) * (0.004 if m.group(4) else 1)  # CSS: 100% chroma is 0.4
    h = 0.0 if m.group(5).lower() == "none" else float(m.group(5))
    if not all(map(math.isfinite, (L, C, h))):
        return None
    return min(max(L, 0.0), 1.0), max(C, 0.0), h % 360


def parse_colour(text):
    """(r, g, b) in 0..1 as a browser paints it (out-of-gamut clipped) for oklch(), a hex, rgb(), hsl() or a named
    colour; None when it isn't one we read or it is translucent."""
    t = (text or "").strip().lower()
    m = OKLCH.fullmatch(t)
    if m:
        lch = _oklch_parts(m)
        return lch and tuple(_encode(v) for v in _linear(*lch))
    t = {"white": "#ffffff", "red": "#ff0000", "green": "#008000", "yellow": "#ffff00", "orange": "#ffa500"}.get(t, t)
    if t.startswith("#"):
        if not re.fullmatch(r"#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})", t) or len(t) in (5, 9) and t[-1] != "f" \
                or len(t) == 9 and t[-2] != "f":
            return None
    elif t.startswith(("rgb", "hsl")):
        nums = re.findall(r"-?\d*\.?\d+%?", t[t.find("(") + 1:])
        if len(nums) > 3 and float(nums[3].rstrip("%")) / (100 if nums[3].endswith("%") else 1) < 1:
            return None
    rgb = _rgb(t)
    return rgb and tuple(min(max(v, 0.0), 1.0) for v in rgb)


def hex_of(rgb):
    return "#" + "".join("%02X" % round(v * 255) for v in rgb)


def _luminance(rgb):
    """WCAG 2.x relative luminance of the 8-bit colour the browser paints."""
    ch = [round(min(max(v, 0.0), 1.0) * 255) / 255 for v in rgb]
    ch = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(a, b):
    """WCAG 2.x contrast ratio (1 to 21) of two sRGB colours."""
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _tok(L, C, h):
    """A role's colour as written: L and h kept, chroma lowered until it fits sRGB, then rounded (C down, so it
    still fits); its hex and contrast come from the rounded value."""
    L, h = round(min(max(L, 0.0), 1.0), 3), round(h % 360, 1) % 360
    if not in_gamut(L, C, h):
        lo, hi = 0.0, C
        for _ in range(30):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if in_gamut(L, mid, h) else (lo, mid)
        C = lo
    lch = (L, math.floor(C * 1000) / 1000, h)
    rgb = tuple(_encode(v) for v in _linear(*lch))
    return {"oklch": lch, "hex": hex_of(rgb), "rgb": rgb}


def _floors(role, dark):
    """(other role, floor) for each pair the role is in."""
    return [(b if f == role else f, dn if dark else ln) for f, b, ln, dn in PAIRS if role in (f, b)]


def palette(seed):
    """Light and dark values for ROLES from one seed colour, and the proof of every pair. Neutrals take the seed's hue
    at a whisper of its chroma; each text role starts at type-and-colour.md's lightness and moves away from its
    surfaces in 0.01 steps until every pair it is in clears its floor by MARGIN; the accent keeps the seed's hue and
    chroma."""
    rgb = parse_colour(seed)
    if rgb is None:
        raise ValueError(f"can't read the seed {seed!r}: write a hex, rgb(), hsl() or oklch() colour, opaque")
    m = OKLCH.fullmatch(seed.strip().lower())
    L0, C0, h0 = _oklch_parts(m) if m else oklch_of(rgb)
    nc = min(0.012, C0 / 10)
    pal = {"seed": hex_of(rgb), "proofs": []}
    for dark, name in ((False, "light"), (True, "dark")):
        t = {r: _tok(L, nc, h0) for r, L in zip(SURFACES, (.18, .22, .27) if dark else (.97, .99, .93))}
        t["on-accent"] = t["surface"] if dark else _tok(.99, nc, h0)
        t["accent-subtle"] = _tok(.30, min(C0 * .5, .06), h0) if dark else _tok(.95, min(C0 * .25, .03), h0)
        starts = {"text": (.93 if dark else .22, nc), "text-muted": (.66 if dark else .45, nc), "border": (.55, nc),
                  "accent": (min(max(L0, .70), .80), C0 * .8) if dark else (L0, C0)}
        for role in ("text", "text-muted", "border", "accent", "on-subtle"):
            if role == "on-subtle":  # the accent, a little further from its subtle fill
                starts[role] = (max(t["accent"]["oklch"][0], .80), C0 * .6) if dark else (t["accent"]["oklch"][0], C0)
            L, C = starts[role]
            for _ in range(102):  # 0.01 a step: at most from one end of L to the other
                t[role] = _tok(L, C, h0)
                if all(contrast(t[role]["rgb"], t[o]["rgb"]) >= need + MARGIN for o, need in _floors(role, dark)) \
                        or L >= 1 and dark or L <= 0 and not dark:
                    break
                L = min(max(L + (.01 if dark else -.01), 0.0), 1.0)
        pal[name] = {r: t[r] for r in ROLES}
        pal["proofs"] += _proofs(lambda r: t[r]["rgb"], name, [(f, b, dn if dark else ln) for f, b, ln, dn in PAIRS])
    return pal


def _proofs(colour, theme, pairs):
    out = []
    for fg, bg, need in pairs:
        r = contrast(colour(fg), colour(bg))
        out.append({"fg": fg, "bg": bg, "theme": theme, "ratio": r, "need": need, "pass": r >= need})
    return out


def _css(tok):
    return "oklch({:g} {:g} {:g})".format(*tok["oklch"])


def export(pal, fmt="css"):
    """The palette as DTCG JSON (2025.10 colour values: oklch components and a hex fallback), CSS custom properties
    (light-dark() roles, which fm design contrast reads back) or a Tailwind v4 theme (those, plus @theme inline)."""
    if fmt == "dtcg":
        return json.dumps({theme: {r: {"$type": "color", "$value": {"colorSpace": "oklch", "components":
                                                                     list(tok["oklch"]), "hex": tok["hex"].lower()}}
                                   for r, tok in pal[theme].items()} for theme in ("light", "dark")}, indent=2) + "\n"
    lines = [f"/* fm design palette {pal['seed']}: light and dark roles; prove them with fm design contrast FILE */",
             ":root {", "  color-scheme: light dark;"]
    lines += [f"  --{r}: light-dark({_css(pal['light'][r])}, {_css(pal['dark'][r])});  "
              f"/* {pal['light'][r]['hex']} {pal['dark'][r]['hex']} */" for r in ROLES]
    lines += ["}", ':root[data-theme="light"] { color-scheme: light; }',
              ':root[data-theme="dark"] { color-scheme: dark; }']
    if fmt == "tailwind":
        lines += ["@theme inline {"] + [f"  --color-{r}: var(--{r});" for r in ROLES] + ["}"]
    return "\n".join(lines) + "\n"


def render_proofs(proofs, warnings=()):
    return "\n".join([f"  {w}" for w in warnings] + [
        f"{'pass' if p['pass'] else 'FAIL'}  {p['theme']:5}  {p['fg'] + '/' + p['bg']:28} {p['ratio']:5.2f}:1  "
        f"(needs {p['need']:g})" for p in proofs])


QUALS = r"(?:\.[\w-]+|\[[^\]]{0,200}\]|:[\w-]+(?:\([^()]{0,200}\))?)*"
# one whole compound selector that sets tokens: :root, html or :host with any qualifiers (html.dark,
# :root[data-theme="dark"], :host(.dark)), or only theme classes and attributes (.dark, [data-theme="dark"])
ROOT_PART = re.compile(r"(?::root|html|:host(?:\([^()]{0,200}\))?)" + QUALS +
                       r"|(?:\.(?:theme-)?(?:dark|light)|\[data-[\w-]*(?:theme|mode|scheme)\b[^\]]{0,200}\])+", re.I)
DARK = re.compile(r"\bdark\b", re.I)


def _block(sel, parent):
    """(sets tokens, dark, an override to leave out) for a block, from its selector and its parent block's flags. A
    nested at-rule or &-selector inside a token block is one too (:root { @media (…dark) {…} &.dark {…} })."""
    in_root, dark, skip = parent
    parts = [p.strip() for p in sel.split(",")]
    root = bool(re.match(r"@theme\b", sel)) or any(ROOT_PART.fullmatch(p) for p in parts) or \
        in_root and (sel.startswith("@") or all(re.fullmatch("&" + QUALS, p) for p in parts))
    cond = re.match(r"@(?:media|supports|container)\b", sel) and "prefers-color-scheme" not in sel
    return root, dark or bool(DARK.search(sel)), skip or bool(cond)


def _props(src):
    """(name, value, dark, offset) for each custom property set in a token block (:root, html or :host with any
    qualifiers, @theme, a .dark or [data-theme] block, or an at-rule or &-selector nested in one); dark when the block
    or one around it says dark. Other @media, @supports and @container blocks are overrides, not the token, and are
    left out. Each block's flags come from its parent's, so deep nesting stays linear. ponytail: a dark-first file
    (dark in :root, light in a prefers-color-scheme: light block) reads as light only."""
    text = re.sub(r"#\{([^{}\n]{0,200})\}", lambda m: "  " + m.group(1) + " ", src.braces)  # SCSS #{$x}: not a block
    css, stack, last, out = src.css, [], 0, []
    for m in re.finditer(r"[{};]", text):
        if m.group() == "{":
            sel = re.sub(r":not\([^()]{0,200}\)", "", css[max(last, m.start() - 2000):m.start()]).strip()
            stack.append(_block(sel, stack[-1] if stack else (False, False, False)))
        else:
            d = re.match(r"\s*(--[\w-]+)\s*:(.*)", css[last:m.start()], re.S)
            value = d and re.sub(r" ?! ?important$", "", " ".join(d.group(2).split()), flags=re.I)
            if value and stack and stack[-1][0] and not stack[-1][2]:
                out.append((d.group(1), value, stack[-1][1], last + d.start(1)))
            if m.group() == "}" and stack:
                stack.pop()
        last = m.end()
    return out


def _branch(value, dark):
    """light-dark(A, B)'s A or B; any other value as it is."""
    m = re.fullmatch(r"light-dark\((.*)\)", value or "", re.S)
    parts = _split(m.group(1), ",") if m else []
    return parts[dark] if len(parts) == 2 else value


def _colour_of(tokens, name, dark, seen=()):
    """The sRGB colour a token paints in one theme, through var() and light-dark(); ValueError naming the token when
    it can't be read."""
    base, over = tokens
    if name in seen:
        raise ValueError(f"{name}: var() loop through {' → '.join(seen)}")
    if len(seen) > 50:
        raise ValueError(f"{name}: var() chain over 50 deep")
    v = over.get(name, base.get(name)) if dark else base.get(name)
    if v is None:
        raise ValueError(f"{name}: not defined")
    for _ in range(50):
        v = _branch(v, dark)
        m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,(.*))?\)", v, re.S)
        if not m:
            break
        if m.group(2) is None or m.group(1) in base or dark and m.group(1) in over:
            return _colour_of(tokens, m.group(1), dark, seen + (name,))
        v = m.group(2).strip()  # the fallback, when the reference is undefined
    rgb = parse_colour(v)
    if rgb is None:
        raise ValueError(f"{name}: can't read {v[:80]!r} (write oklch(), a hex, rgb(), hsl(), var() or light-dark(); "
                         "opaque)")
    return rgb


def _themes(tokens):
    base, over = tokens
    return (False, True) if over or any("light-dark(" in v for v in base.values()) else (False,)


def check_pairs(tokens, specs=(), strict=True):
    """(proofs, warnings) for each pair spec fg/bg[:need[,dark need]] (default: the known role pairs present) in each
    theme the tokens have. strict: a token that can't be read raises ValueError; else its pairs are left out."""
    base, over = tokens
    pairs = []
    for spec in specs:
        pair, _, need = spec.partition(":")
        names = pair.split("/")
        needs = need.split(",") if need else ["4.5"]
        if len(names) != 2 or not all(re.fullmatch(r"(?:--)?[\w-]+", n) for n in names) or len(needs) > 2 or \
                not all(re.fullmatch(r"\d+(?:\.\d+)?", n) for n in needs):
            raise ValueError(f"can't read the pair {spec!r}: write fg/bg, fg/bg:4.5 or fg/bg:4.5,7 (light, dark)")
        fg, bg = (n if n.startswith("--") else "--" + n for n in names)
        pairs.append((fg, bg, float(needs[0]), float(needs[-1])))
    if not specs:
        pairs = [("--" + f, "--" + b, ln, dn) for f, b, ln, dn in PAIRS if "--" + f in base and "--" + b in base]
        if not pairs:
            raise ValueError("no pairs given and none of the known roles (--text on --surface, …) defined")
    proofs = []
    for dark in _themes(tokens):
        for fg, bg, ln, dn in pairs:
            try:
                p = _proofs(lambda n: _colour_of(tokens, n, dark), "dark" if dark else "light",
                            [(fg, bg, dn if dark else ln)])
            except ValueError:
                if strict:
                    raise
                continue
            proofs += [dict(x, fg=fg[2:], bg=bg[2:]) for x in p]
    warnings = sorted({f"{n}: {m.group()} is outside sRGB, the browser will clip it; lower the chroma"
                       for n, v in [*base.items(), *over.items()] for m in OKLCH.finditer(v)
                       if (lch := _oklch_parts(m)) and not in_gamut(*lch)})
    return proofs, warnings


def read_tokens(path):
    """(base, dark) custom properties of one token file."""
    text, why = _read(path)
    if text is None:
        raise ValueError(f"{path}: {why}")
    base, over = {}, {}
    for name, value, dark, _ in _props(Source(path, text)):
        (over if dark else base)[name] = value
    if not base and not over:
        raise ValueError(f"{path}: no :root custom properties")
    return base, over


TW_TOKEN = re.compile(r"""(['"]?)(?<![\w-])([\w-]++)\1\s*:\s*(?:(\{)|(['"])([^'"\n]{0,200})\4)|([{}])|"""
                      r"""(['"`])(?:\\.|(?!\7)[^\\\n]){0,2000}\7""")


def _tw_colours(text):
    """(--color-NAME, value, line) for each literal colour under a colors key of a tailwind.config file, DEFAULT being
    the bare name. ponytail: string literals only; spreads, require() and function values aren't read."""
    code = _blank(text, r"/\*.*?(?:\*/|\Z)|(?<!\S)//[^\n]*")
    nl = [i for i, ch in enumerate(code) if ch == "\n"]
    stack, out = [], []
    for m in TW_TOKEN.finditer(code):
        if m.group(6) == "{":
            stack.append("")
        elif m.group(6) == "}":
            stack = stack[:-1]
        elif m.group(3):
            stack.append(m.group(2))
        elif m.group(5) is not None and "colors" in stack and parse_colour(m.group(5)):
            path = [k for k in stack[stack.index("colors") + 1:] + [m.group(2)] if k and k != "DEFAULT"]
            if path:
                out.append(("--color-" + "-".join(path), m.group(5).strip(), bisect.bisect_left(nl, m.start()) + 1))
    return out


KINDS = ("colour", "font", "length", "duration", "shadow", "number", "other")
MAX_ROWS = 500


def _kind(name, value, colour):
    v = value or ""
    if colour:
        return "colour"
    if re.search(r"font|family", name):
        return "font"
    if re.fullmatch(NUM + r"(?:px|rem|em|ch|ex|lh|rlh|%|vw|vh|vmin|vmax|svh|dvh|lvh)", v) or \
            re.match(r"(?:clamp|calc|min|max)\(", v):
        return "length"
    if TIME.fullmatch(v):
        return "duration"
    if "shadow" in name:
        return "shadow"
    return "number" if re.fullmatch("-?" + NUM, v) else "other"


def extract(paths):
    """(rows, proofs, files read, skipped): one row per custom property set in the run's token blocks (and literal
    tailwind.config colours), colours first; the known role pairs' contrast; what wasn't read and why."""
    files, skipped, configs, _ = collect(paths)
    props, read = [], 0
    for f in files + configs:
        text, why = _read(f)
        if text is None:
            skipped.append({"file": f, "why": why})
            continue
        read += 1
        if f in configs:
            props += [(n, v, False, f, ln) for n, v, ln in _tw_colours(text)]
        else:
            src = Source(f, text)
            props += [(n, v, d, f, src.line(o)) for n, v, d, o in _props(src)]
    base, over, where = {}, {}, {}
    for n, v, d, f, ln in props:
        (over if d else base)[n] = v
        if not d or n not in where:
            where[n] = (f, ln)
    tokens, rows = (base, over), []
    for n in where:
        hexes = []
        for dark in (False, True):
            try:
                hexes.append(hex_of(_colour_of(tokens, n, dark)))
            except ValueError:
                hexes.append(None)
        light, dark = _branch(base.get(n), 0), _branch(over.get(n, base.get(n)), 1)
        same = (light, hexes[0]) == (dark, hexes[1])
        rows.append({"name": n, "kind": _kind(n, light or dark, hexes[0] or hexes[1]), "light": light,
                     "light_hex": hexes[0], "dark": None if same else dark, "dark_hex": None if same else hexes[1],
                     "file": where[n][0], "line": where[n][1]})
    rows.sort(key=lambda r: KINDS.index(r["kind"]))  # stable: each kind keeps the source's order
    try:
        proofs = check_pairs(tokens, strict=False)[0]
    except ValueError:  # none of the known role pairs is defined
        proofs = []
    return rows, proofs, read, skipped


def _cell(text, limit=60):
    text = " ".join(str(text).split()).replace("`", "'")
    return (text[:limit - 1] + "…" if len(text) > limit else text).replace("|", "\\|")


def _rel(path, base_dir):
    """path from base_dir when it lies under it, else …/<folder>/<name>: the same text whichever folder fm ran from,
    and no home folder or machine layout in a file meant for the repo."""
    full = os.path.abspath(path)
    rel = os.path.relpath(full, base_dir)
    if rel == ".." or rel.startswith(".." + os.sep):
        return "…/" + "/".join(full.rstrip(os.sep).split(os.sep)[-2:])
    return rel


def section(rows, proofs, srcs, base_dir):
    """DESIGN.md's Tokens section (markdown lines): the table, then each known text/surface pair's contrast."""
    def val(v, h):
        return " ".join(x for x in (f"`{_cell(v, 200)}`" if v else "", h or "") if x)  # T-1624: fm motion reads them
    out = ["## Tokens", "",
           f"Written by `fm design extract {_cell(' '.join(_rel(p, base_dir) for p in srcs), 4096)}` from the CSS "
           "custom properties set in :root, "
           "html, :host and @theme (dark: a .dark, [data-theme] or prefers-color-scheme: dark block, or light-dark()) "
           "and tailwind.config colours. Rerun it after a token change; it rewrites this section only.", "",
           "| Token | Kind | Light | Dark | Source |", "|---|---|---|---|---|"]
    for r in rows[:MAX_ROWS]:
        out.append(f"| `{r['name']}` | {r['kind']} | {val(r['light'], r['light_hex'])} | "
                   f"{val(r['dark'], r['dark_hex'])} | {_cell(_rel(r['file'], base_dir), 4096)}:{r['line']} |")
    if len(rows) > MAX_ROWS:
        out += ["", f"{len(rows) - MAX_ROWS} more token(s) left out of the table."]
    if proofs:
        out += ["", "Contrast (WCAG 2.x, on the sRGB hex the browser paints):", ""]
        by = {}
        for p in proofs:
            by.setdefault((p["fg"], p["bg"]), []).append(p)
        for (fg, bg), ps in by.items():
            got = ", ".join(f"{p['ratio']:.2f}:1 {p['theme']}" if len(ps) > 1 else f"{p['ratio']:.2f}:1" for p in ps)
            needs = ", ".join(f"{p['need']:g}" + (" dark" if p["theme"] == "dark" else "") for p in ps) \
                if len({p["need"] for p in ps}) > 1 else f"{ps[0]['need']:g}"
            bad = [p["theme"] for p in ps if not p["pass"]]
            out.append(f"- `{fg}` on `{bg}`: {got} (needs {needs})" + (f": FAIL in {' and '.join(bad)}" if bad else ""))
    return out


def headings(doc):
    """((line index, heading) for each # and ## heading outside fenced code, the fence left open at the end or None)
    of a markdown file's lines."""
    heads, fence = [], None
    for i, ln in enumerate(doc):
        f = re.match(r" {0,3}(`{3,}|~{3,})", ln)
        if f:  # a fence closes on its own character, at least as long
            mark = f.group(1)
            fence = None if fence and mark[0] == fence[0] and len(mark) >= len(fence) else fence or mark
        elif not fence and re.match(r"#{1,2}\s", ln):
            heads.append((i, ln.strip()))
    return heads, fence


def has_direction(text):
    """DESIGN.md records a design direction: it has a ## Direction section (the Tokens-only file fm design extract
    starts is a palette, not a direction)."""
    return any(h == "## Direction" for _, h in headings(text.split("\n"))[0])


def write_section(path, lines, title):
    """Put the section into the markdown file at path (through a symlink, under a lock): replace its own (## Tokens up
    to the next heading, fenced code aside), else insert it after ## Knobs, else append it; a missing file starts with
    a DESIGN.md title. Every other section is kept byte for byte, CRLF line ends included; a file that isn't UTF-8 is
    refused, never rewritten."""
    import fmcore
    path = os.path.realpath(path)
    with fmcore.lock(os.path.join(fmcore.state_dir(), "locks", "design-md")):  # ponytail: one lock for every DESIGN.md
        text = ""
        if os.path.lexists(path):
            text, why = _read(path, strict=True)
            if text is None:
                raise ValueError(f"{path}: {why}")
        crlf = "\r\n" in text
        text = text.replace("\r\n", "\n")
        if not text.strip():
            text = (f"# DESIGN.md: {_cell(title, 80)}\n\nNo direction recorded yet: /foreman:directions or the "
                    "playbook ui/design-direction.md fills the other sections.\n")
        doc = text.split("\n")
        heads, fence = headings(doc)
        if fence:  # the section would land inside it, and every run would add another
            raise ValueError(f"{path}: a {fence} code fence is never closed; close it and run again")
        _splice(doc, heads, lines)
        out = "\n".join(doc)
        fmcore.write_atomic(path, out.replace("\n", "\r\n") if crlf else out)


def _splice(doc, heads, lines):
    """doc (a list of lines) with lines as its ## Tokens section, in place."""
    def end_of(i):
        return next((j for j, _ in heads if j > i), None)
    own = next((i for i, h in heads if h == "## Tokens"), None)
    knobs = next((i for i, h in heads if h == "## Knobs"), None)
    if own is not None:
        a, b = own, end_of(own)
    elif knobs is not None and end_of(knobs) is not None:
        a = b = end_of(knobs)
    else:
        a = b = None
    if b is None:  # to the end of the file
        keep = doc[:len(doc) if a is None else a]
        while keep and not keep[-1].strip():
            keep.pop()
        doc[:] = keep + [""] + lines + [""]
    else:
        doc[a:b] = lines + [""]


# T-1651: fm design tokens compiles the ## Tokens table above to each surface. A token's role comes from its name's
# words (the first role here that one names; within a role the earlier word, then the shorter name, wins).
# ponytail: name words only; a DESIGN.md knob naming roles explicitly when a project's names don't say them.
TOKEN_ROLES = (("border", ("border", "rule")), ("ok", ("success", "ok")), ("bad", ("danger", "error", "destructive")),
               ("warn", ("warning", "warn")), ("muted", ("muted", "subtle")), ("raised", ("raised", "panel", "card")),
               ("accent", ("primary", "accent", "brand")), ("bg", ("bg", "background", "surface", "paper")),
               ("text", ("text", "ink", "fg", "foreground")))
APP_STYLES = {  # role -> (fm code style, field): as fmcodetui._theme paints its palette
    "bg": (("screen", "bg"), ("select", "fg"), ("brand", "fg"), ("chip_ok", "fg"), ("chip_bad", "fg"),
           ("chip_warn", "fg"), ("chip_accent", "fg")),
    "text": (("screen", "fg"), ("strong", "fg"), ("header", "fg"), ("input", "fg")),
    "muted": (("dim", "fg"), ("said", "fg"), ("header_dim", "fg"), ("bar_dim", "fg"), ("chip_todo", "fg")),
    "accent": (("accent", "fg"), ("title", "fg"), ("chart", "fg"), ("select", "bg"), ("brand", "bg"),
               ("chip_accent", "bg")),
    "ok": (("ok", "fg"), ("chip_ok", "bg")), "bad": (("bad", "fg"), ("chip_bad", "bg")),
    "warn": (("warn", "fg"), ("key", "fg"), ("chip_warn", "bg")), "border": (("border", "fg"),),
    "raised": (("header", "bg"), ("header_dim", "bg"), ("bar", "bg"), ("bar_dim", "bg"), ("key", "bg"),
               ("input", "bg"), ("chip_todo", "bg"), ("panel", "bg"))}
PANE_KEYS = {"accent": "accent", "ok": "ok", "warn": "warn", "err": "bad", "dim": "muted", "muted": "muted",
             "track": "border", "white": "text"}  # the C object in mods/foreman-ui/hooks/kit.ts, by role
PANE_ALL = ("accent", "accent2", "ok", "warn", "err", "edit", "agent", "web", "skill", "dim", "muted", "add", "del",
            "track", "white")


def read_design(path):
    """{name: {kind, light, dark, light_hex, dark_hex}} from the markdown file's ## Tokens table, in table order: the
    cells as fm design extract's section() writes them (a backquoted value, then a hex). ValueError when it has none."""
    text, why = _read(path, strict=True)
    if text is None:
        raise ValueError(f"{path}: {why}")
    doc = text.replace("\r\n", "\n").split("\n")
    heads, _ = headings(doc)
    at = next((i for i, h in heads if h == "## Tokens"), None)
    if at is None:
        raise ValueError(f"{path} has no ## Tokens section: fm design extract PATHS writes it")
    end = next((j for j, _ in heads if j > at), len(doc))
    out, col = {}, None
    for ln in doc[at + 1:end]:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip())[1:-1]]
        if col is None:  # the columns by the header's names, wherever they stand
            low = [c.lower() for c in cells]
            if {"token", "light", "dark"} <= set(low):
                col = {k: low.index(k) for k in ("token", "kind", "light", "dark") if k in low}
            continue
        name = re.fullmatch(r"`(--[A-Za-z0-9_-]+)`", cells[col["token"]]) if len(cells) > max(col.values()) else None
        if not name or name.group(1) in out:
            continue
        row = {"kind": cells[col["kind"]] if "kind" in col else ""}
        for theme in ("light", "dark"):
            cell = cells[col[theme]]
            m = re.fullmatch(r"(?:`(.*)`)?\s*(#[0-9A-Fa-f]{6})?", cell)
            row[theme] = m and m.group(1) is not None and m.group(1).replace("\\|", "|") or None
            row[f"{theme}_hex"] = m and m.group(2) or None
        if row["light"] or row["light_hex"] or row["dark"] or row["dark_hex"]:
            out[name.group(1)] = row
    if not out:
        raise ValueError(f"{path}: its ## Tokens section has no token rows under a | Token | Kind | Light | Dark | "
                         "Source | header")
    return out


def _safe_css(v):
    """The value can't end its declaration, its block or the sheet: no ; { } < \\ @ url( or comment, every bracket
    and quote closed."""
    if re.search(r"[;{}<\\@]|/\*|\*/|url\(", v, re.I):
        return False
    stack, q = [], None
    for ch in v:
        if q:
            q = None if ch == q else q
        elif ch in "\"'":
            q = ch
        elif ch in "([":
            stack.append(")" if ch == "(" else "]")
        elif ch in ")]" and (not stack or stack.pop() != ch):
            return False
    return not stack and not q


def _css_value(row, theme):
    """The token's CSS value in that theme, or None: as written when that is safe (_safe_css) and whole, else its hex."""
    v, h = row[theme], row[f"{theme}_hex"]
    if not v or v.endswith("…") or not _safe_css(v):
        v = h.lower() if h else None
    return v


def to_css(tokens):
    lines = ["/* fm design tokens --to css: DESIGN.md's ## Tokens; dark values under prefers-color-scheme, .dark and "
             "[data-theme=\"dark\"] */", ":root {"]
    dark, left = [], []
    for name, row in tokens.items():
        got = {}
        for theme in ("light", "dark"):
            if row[theme] or row[f"{theme}_hex"]:
                got[theme] = _css_value(row, theme)
                if got[theme] is None:
                    left.append(f"{name} ({theme})")
        if got.get("light") is not None:
            lines.append(f"  {name}: {got['light']};")
        if got.get("dark") is not None and got["dark"] != got.get("light"):
            dark.append(f"{name}: {got['dark']};")
    lines.append("}")
    if dark:
        lines += ["@media (prefers-color-scheme: dark) {", "  :root {"] + [f"    {d}" for d in dark] + ["  }", "}"]
        lines += ['.dark, [data-theme="dark"] {'] + [f"  {d}" for d in dark] + ["}"]
    if left:
        lines.append(f"/* left out (a value CSS can't hold as one declaration, and no hex): {', '.join(left)} */")
    return "\n".join(lines) + "\n"


def token_roles(tokens, dark=True):
    """{role: (token name, #hex)}: the colour each role takes, in the theme asked (a token with one value: that)."""
    best = {}
    want, other = ("dark_hex", "light_hex") if dark else ("light_hex", "dark_hex")
    texty = {"text", "ink", "fg", "foreground"}
    for i, (name, row) in enumerate(tokens.items()):
        h = row[want] or row[other]
        words = re.split(r"[-_]+", name.lower().strip("-"))
        if not h or "on" in words:  # --on-accent: text on a role's colour, not the role
            continue
        for role, names in TOKEN_ROLES:
            if role not in ("text", "muted") and {"fg", "foreground"} & set(words):
                continue  # shadcn's --primary-foreground: text on the role's colour; it may still be text
            hit = [names.index(w) for w in words if w in names]
            if hit:  # muted: --text-muted, --muted-foreground are text; --surface-muted, shadcn's --muted surfaces
                rank = (role == "muted" and not texty & set(words), min(hit), len(words), i)
                if role not in best or rank < best[role][0]:
                    best[role] = (rank, name, h)
                break
    return {r: (n, h) for r, (_, n, h) in best.items()}


def to_app(tokens, theme=None):
    """A tui.toml fragment: theme = the preset under it (theme light: paper, dark: night, None: the dark values on the
    preset that fits their screen's lightness), then [colors] (each style the preset's, with the roles' colours),
    checked as fm settings checks the file: a style the app would skip (too faint) is left out, and said; a preset
    style never written that is too faint on the new screen is named too."""
    import fmcodetui as T
    import fmsettings
    light = theme == "light"
    roles = token_roles(tokens, not light)
    if not roles:
        raise ValueError("no token's name says its role (" + ", ".join(w for _, ws in TOKEN_ROLES for w in ws) + ")")
    bg = roles.get("bg", (None, None))[1]
    pale = bool(bg) and T.contrast(bg, "#000000") > T.contrast(bg, "#FFFFFF")
    preset = "paper" if light or (theme is None and pale) else "night"
    base = T.PRESETS[preset]()
    styles = {}
    for role, (_, h) in roles.items():
        for style, field in APP_STYLES[role]:
            styles.setdefault(style, dict(base[style]))[field] = h
    styles = {n: styles[n] for n in base if n in styles}  # screen first: the faint check reads its background
    left = []
    for _ in range(len(styles) + 1):  # each pass drops at least one style the app refuses
        now = dict(base, **styles)  # what the app draws: the faint check of the styles left as the preset's own
        faint = [f"{n} ({why})" for n in base if n not in styles and n not in ("screen", "panel", "border", "track",
                 "shade", "glow") for why in [T._faint(base[n], now)] if why]  # glow: a flash's mix colour, not text
        text = "\n".join([
            f"# fm code app theme: DESIGN.md's ## Tokens ({'light' if light else 'dark'} values), for tui.toml",
            "# roles: " + ", ".join(f"{r} {n}" for r, (n, _) in roles.items()),
            f"theme = {T._toml(preset)}", "", "[colors]"] +
            [f"{T._toml_key(n)} = {T._toml(s)}" for n, s in styles.items()] +
            [f"# not mapped, the {preset} theme's own: {', '.join(n for n in base if n not in styles)}"] +
            [f"# left out: {x}" for x in left] +
            ([f"# too faint on this screen, the {preset} theme's own (set them under [colors]): {', '.join(faint)}"]
             if faint else [])) + "\n"
        errors = fmsettings._load(text, "tui.toml")[1]
        named = [(m.group(1), e) for e in errors for m in [re.match(r"tui\.toml: colors\.(\w+): ", e)] if m]
        if len(named) < len(errors):
            raise ValueError("the app can't read the theme: " + "; ".join(errors))
        if not named:
            return text
        for n, e in named:
            styles.pop(n, None)
            left.append(e[len("tui.toml: "):])
    raise ValueError("the app refuses every style: " + "; ".join(left))


def to_pane(tokens, theme=None):
    """(JSON text, unmapped keys): the Claude Code pane's palette keys with the roles' colours (dark unless light)."""
    roles = token_roles(tokens, theme != "light")
    pal = {k: roles[r][1] for k, r in PANE_KEYS.items() if r in roles}
    if not pal:
        raise ValueError("no token's name says a role the pane paints (" + ", ".join(sorted(set(PANE_KEYS.values())))
                         + ")")
    return json.dumps(pal, indent=2) + "\n", [k for k in PANE_ALL if k not in pal]


def _default_out():
    import fmcore
    root = fmcore.git_root(os.getcwd()) or os.getcwd()
    out, docs = os.path.join(root, "DESIGN.md"), os.path.join(root, "docs", "DESIGN.md")
    return docs if not os.path.lexists(out) and os.path.isfile(docs) else out


def contrast_file(path, specs):
    return check_pairs(read_tokens(path), specs)


def _design_tokens(args, fmcli):
    import sys
    act, err = args.action, sys.stderr
    try:
        if act == "palette":
            if len(args.paths) != 1:
                raise ValueError("palette takes one seed colour, e.g. fm design palette '#3366cc'")
            pal = palette(args.paths[0])
            text = export(pal, args.format)
            failed = sum(not p["pass"] for p in pal["proofs"])
            if getattr(args, "json", False):
                fmcli.out(args, {"seed": pal["seed"], "proofs": pal["proofs"], "export": text,
                                 **{t: {r: {"oklch": list(x["oklch"]), "hex": x["hex"]} for r, x in pal[t].items()}
                                    for t in ("light", "dark")}}, None)
            else:
                sys.stdout.write(text)
                print(render_proofs(pal["proofs"]) + f"\npalette: {len(pal['proofs']) - failed} of "
                      f"{len(pal['proofs'])} pairs pass (body text 7:1 in dark)", file=err)
            return 1 if failed else 0
        if act == "contrast":
            proofs, warnings = contrast_file(args.paths[0], args.paths[1:])
            failed = sum(not p["pass"] for p in proofs)
            fmcli.out(args, {"proofs": proofs, "warnings": warnings, "failed": failed},
                      render_proofs(proofs, warnings) + f"\ncontrast: {failed} of {len(proofs)} failed")
            return 1 if failed else 0
        if act == "tokens":  # T-1651: prints only; the user puts it where the surface reads it
            if len(args.paths) != 1:
                raise ValueError("tokens takes one DESIGN.md, e.g. fm design tokens DESIGN.md --to css")
            to = getattr(args, "to", None) or "css"
            light, dark = getattr(args, "light", False), getattr(args, "dark", False)
            if light and dark:
                raise ValueError("--light or --dark, not both")
            theme = "light" if light else "dark" if dark else None
            tokens, unmapped = read_design(args.paths[0]), []
            if to == "css":
                if theme:
                    print(f"design tokens: --{theme} ignored: --to css carries both themes", file=err)
                text = to_css(tokens)
            elif to == "app":
                text = to_app(tokens, theme)
            else:
                text, unmapped = to_pane(tokens, theme)
            if getattr(args, "json", False):
                fmcli.out(args, {"to": to, "text": text, "unmapped": unmapped}, None)
            else:
                sys.stdout.write(text)
                if unmapped:  # JSON has no comments: the keys the pane keeps its own colour for go to stderr
                    print(f"pane: not mapped, the pane's own: {', '.join(unmapped)}", file=err)
            return 0
        missing = [p for p in args.paths if not os.path.exists(p)]
        if missing:
            raise ValueError(f"no such file or directory: {', '.join(missing)}")
        rows, proofs, read, skipped = extract(args.paths)
        gone = "; ".join(f"{x['file']} ({x['why']})" for x in skipped)
        if not rows:
            raise ValueError(f"no :root custom properties under {', '.join(args.paths)} (it reads :root, html, :host, "
                             "@theme and .dark or [data-theme] blocks, and tailwind.config colours)"
                             + (f"; skipped: {gone}" if gone else ""))
        out = args.out or _default_out()
        base_dir = os.getcwd() if out == "-" else os.path.dirname(os.path.realpath(out))
        lines = section(rows, proofs, args.paths, base_dir)
        if out != "-":
            write_section(out, lines, os.path.basename(base_dir))
        text = "\n".join(lines) if out == "-" else \
            f"design extract: {len(rows)} token(s) from {read} file(s) → {out} (## Tokens)"
        fmcli.out(args, {"out": out, "tokens": rows, "proofs": proofs, "files": read, "skipped": skipped},
                  text + (f"\nskipped: {gone}" if gone else ""))
        return 0
    except (ValueError, OSError, fmcli.c.LockTimeout) as e:  # OSError: the write (read-only, --out a directory)
        print(f"fm: design {act}: {e}", file=err)
        return 2


def cmd_design(args):
    import sys
    import fmcli
    if args.action == "check":  # T-1645: the gates DESIGN.md opts into
        if len(args.paths) > 1:
            print("fm: design check takes one project root", file=sys.stderr)
            return 2
        got = check_gates(args.paths[0] if args.paths else ".")
        fmcli.out(args, got, render_gates(got))
        return 1 if any(g["mode"] == "blocking" and not all(m["pass"] for m in g["musts"])
                        for g in got["gates"]) else 0
    if not args.paths:  # only check defaults its argument (the project root)
        print(f"fm: design {args.action}: needs an argument (fm design -h)", file=sys.stderr)
        return 2
    if args.action != "lint":
        return _design_tokens(args, fmcli)
    missing = [p for p in args.paths if not os.path.exists(p)]
    if missing:
        print(f"fm: design lint: no such file or directory: {', '.join(missing)}", file=sys.stderr)
        return 2
    found, linted, skipped, empty = run(args.paths)
    if empty:
        print(f"fm: design lint: no UI files under {', '.join(empty)} (it reads {' '.join(sorted(EXTS))})",
              file=sys.stderr)
        return 2
    n = len(linted)
    text = "\n".join(render(found) + [f"{len(found)} finding(s) in {n} file(s)"]) if found else \
        f"design lint: clean ({n} file(s))"
    if skipped:
        text += "\nskipped: " + "; ".join(f"{x['file']} ({x['why']})" for x in skipped)
    fmcli.out(args, {"findings": found, "files": n, "skipped": skipped}, text)
    return 1 if found else 0


# T-1645: design gates a project opts into in DESIGN.md's ## Gates section ("- brief: advisory" or "blocking")
GATES = ("brief",)
MODES = ("advisory", "blocking")


def _section_lines(doc, name):
    """The lines of DESIGN.md's ## name section (outside code fences), [] when it has none."""
    heads, _ = headings(doc)
    for k, (i, h) in enumerate(heads):
        if h == f"## {name}":
            return doc[i + 1:heads[k + 1][0] if k + 1 < len(heads) else len(doc)]
    return []


def brief_musts(doc):
    """What the brief promises the code holds, as (label, kind, value): each hex in the Colour knob, each quoted or
    backticked family in the Type knob, each duration in the Motion knob, and each "- must: TEXT" in Direction."""
    musts = []
    for ln in _section_lines(doc, "Knobs"):
        m = re.match(r"\s*[-*]\s*(Type|Colou?r|Motion)\s*:(.*)", ln)
        if not m:
            continue
        kind, rest = m.group(1).lower(), m.group(2)
        if kind == "type":
            musts += [(f"font {f.strip()}", "font", f.strip()) for f in re.findall(r'["`“]([^"`”\n]{1,60})["`”]', rest)]
        elif kind.startswith("colo"):
            musts += [(f"colour {h.upper()}", "colour", h.lower()) for h in re.findall(r"#[0-9A-Fa-f]{6}\b", rest)]
        else:
            for n, unit in re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(ms|s)\b", rest):
                ms = float(n) * (1000 if unit == "s" else 1)
                musts.append((f"duration {ms:g}ms", "duration", ms))
    for ln in _section_lines(doc, "Direction"):
        m = re.match(r"\s*[-*]\s*must\s*:\s*(.{1,200}?)\s*$", ln, re.I)
        if m:
            musts.append((f"has {m.group(1)}", "has", m.group(1)))
    return list({x[0]: x for x in musts}.values())


def _found(kind, value, text):
    """Whether one UI file's text holds the promise, case-blind."""
    low = text.lower()
    if kind in ("colour", "font", "has"):
        return value.lower() in low
    sec = f"{value / 1000:g}".lstrip("0") if value < 1000 else f"{value / 1000:g}"  # 200 → .2, 1500 → 1.5
    return bool(re.search(rf"(?<![\w.]){value:g}ms\b|(?<![\w.])0?{re.escape(sec)}s\b", low))


def check_gates(root):
    """{design, gates: [{gate, mode, musts: [{must, pass, why}]}], notes}: the gates DESIGN.md under root opts into,
    each run over the UI files under root. Nothing opted in: no gates."""
    path = os.path.join(root, "DESIGN.md")
    text, why = _read(path) if os.path.isfile(path) else (None, "no DESIGN.md")
    out = {"design": path, "gates": [], "notes": []}
    if text is None:
        out["notes"].append(f"{os.path.relpath(path)}: {why}")
        return out
    doc = text.split("\n")
    files, *_ = collect([root])
    bodies = []
    for f in files:
        body, _ = _read(f)
        if body is not None:
            bodies.append((os.path.relpath(f, root), body))
    for ln in _section_lines(doc, "Gates"):
        m = re.match(r"\s*[-*]\s*([\w-]+)\s*:\s*([\w-]+)", ln)
        if not m:
            continue
        gate, mode = m.group(1).lower(), m.group(2).lower()
        if gate not in GATES:
            out["notes"].append(f"unknown gate '{gate}' (known: {', '.join(GATES)})")
            continue
        if mode not in MODES:
            out["notes"].append(f"unknown mode '{mode}' for {gate}: read as advisory ({' or '.join(MODES)})")
            mode = "advisory"
        musts = []
        for label, kind, value in brief_musts(doc):
            where = [rel for rel, body in bodies if _found(kind, value, body)]
            musts.append({"must": label, "pass": bool(where),
                          "why": f"in {', '.join(where[:3])}" + (f" and {len(where) - 3} more" if len(where) > 3 else "")
                          if where else f"not in the {len(bodies)} UI file(s) under {os.path.basename(os.path.abspath(root))}"})
        out["gates"].append({"gate": gate, "mode": mode, "musts": musts})
    return out


def render_gates(got):
    """The gates as text; DESIGN.md's words (labels, file names) reach the terminal with control and bidi
    characters replaced."""
    safe = lambda s: re.sub(r"[\x00-\x1f\x7f-\x9f​-‏ -‮⁦-⁩]", "?", s)  # noqa: E731
    if not got["gates"]:
        return "\n".join([safe(n) for n in got["notes"]]
                         + ["no design gates opted in (DESIGN.md's ## Gates: '- brief: advisory')"])
    lines = []
    for g in got["gates"]:
        ok = sum(m["pass"] for m in g["musts"])
        lines.append(f"{g['gate']} ({g['mode']}): {ok} of {len(g['musts'])} must-have(s) found")
        lines += [f"  {'✓' if m['pass'] else '✗'} {safe(m['must'])}: {safe(m['why'])}" for m in g["musts"]]
    return "\n".join(lines + [safe(n) for n in got["notes"]])


if __name__ == "__main__":  # T-1507: a CI without Foreman copies this file (stdlib only) and runs the proof
    import sys
    if sys.argv[1:2] != ["contrast"] or len(sys.argv) < 3:
        print("usage: python3 fmdesign.py contrast TOKENS.css [fg/bg[:need[,dark need]] ...]", file=sys.stderr)
        sys.exit(2)
    try:
        _proved, _warned = contrast_file(sys.argv[2], sys.argv[3:])
    except ValueError as e:
        print(f"fmdesign: {e}", file=sys.stderr)
        sys.exit(2)
    print(render_proofs(_proved, _warned))
    sys.exit(1 if any(not p["pass"] for p in _proved) else 0)
