"""T-1506: fm design lint: the tells of generated design and craft slips in UI source, by text rules (stdlib only).

Precision first: a rule fires only where its text pattern is unambiguous, and a rule that can't be precise is left out.
ponytail: regex and small tokenizers over source text, not computed style; a headless browser would see cascade and
inheritance this can't. Rules that need the whole design (fonts, radius, shadows, tokens, keyframes, a reduced-motion
path) look across every file of one run, so lint the UI's root rather than one component.
An inline `design-lint: allow RULE why` comment silences RULE on its own line (and the next, when the comment stands on
a line of its own); it needs the why."""
import bisect
import colorsys
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
]
BY_ID = {r["id"]: r for r in RULES}
NOT_COVERED = ("not read: computed style and the cascade; .js/.ts files; tailwind.config theme values (but a fontFamily "
               "there keeps font-sans from counting as the system face); class names built in code other than "
               "class/className attributes, cn/clsx/twMerge/cva calls and @apply; side-specific rounded-t-* classes; an "
               "unquoted JSX style value past its line; animation longhands other than name, duration, iteration "
               "count and direction; animations run from JS (the Web Animations API, framer-motion props); Math.random in Vue and Svelte scripts")

EXTS = {".css", ".scss", ".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}
MARKUP = {".html", ".htm", ".vue", ".svelte"}
LINE_COMMENTS = {".scss", ".jsx", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", "bower_components", "vendor", "dist", "build", "out", "target", "venv"}
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
        ends = _closers(self.css)
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

    def check(self):
        for rule in (self.generic_font, self.gradient, self.one_radius, self.same_shadow, self.img_alt, self.motion,
                     self.flash, self.unseeded_random, self.untokened_duration):
            rule()
        by_path = {s.path: s for s in self.sources}
        kept = [f for f in self.found if f["rule"] not in by_path[f["file"]].allowed.get(f["line"], ())]
        return sorted(kept, key=lambda f: (self.order[f["file"]], f["line"], f["rule"]))


def _in_template(code, pos):
    """A Vue or Svelte template expression, unless it is an event handler's (on:click, @click, v-on:)."""
    return not re.search(r"(?:\bon:\w+|@\w+|v-on:\w+)\s*=\s*[\"{][^\"}]*$", code[max(0, pos - 300):pos])


def _read(path):
    """(text, None) for a regular file up to MAX_BYTES, else (None, why). Never blocks on a FIFO or device."""
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
    return data.decode("utf-8", errors="replace"), None


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


def cmd_design(args):
    import sys
    import fmcli
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
