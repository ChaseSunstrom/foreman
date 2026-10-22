"""T-1624: the Motion Score. One file (motion.toml at the project root, or a .json with the same schema) names each
motion the UI uses, so timing and the reduced-motion path are decided once and checked, not scattered through CSS:

    [[motion]]                           # or a [motion.menu-enter] table, whose key is the name
    name = "menu-enter"                  # letters, digits, - and _
    duration = "--dur-enter"             # ms (220), "220ms"/"0.2s", or a token in DESIGN.md's Tokens table
    easing = "ease-enter"                # a CSS keyword, cubic-bezier(…), steps(…), linear(…), motion.md's
                                         # ease-enter/-exit/-move, or a token
    properties = ["opacity", "transform"]
    reduced = "fade"                     # under prefers-reduced-motion, one of:
                                         #   none: the element sits in its rest state; the motion never plays
                                         #   fade: opacity only, over the same duration, in place of any travel
                                         #   instant: the change happens at once (0 ms) to its end state

check(path) lists its problems; fm motion check [PATH] prints them (exit 1 on any). compile_score(path, to) (T-1625,
fm motion compile [PATH] --to css|waapi|three [--out FILE]) emits a clean score as CSS custom properties and
@keyframes, a WAAPI options module or three.js tween parameters: every target carries the score's own durations and
easings, and each motion's reduced form keeps the three meanings above."""
import json
import os
import re
import textwrap
import tomllib

import fmdesign

KEYS = ("name", "duration", "easing", "properties", "reduced")
REDUCED = ("none", "fade", "instant")
MAX_MS = 2000
KEYWORDS = {"linear", "ease", "ease-in", "ease-out", "ease-in-out", "step-start", "step-end"}
CURVES = {"ease-enter": "cubic-bezier(0.05, 0.7, 0.1, 1)", "ease-exit": "cubic-bezier(0.3, 0, 0.8, 0.15)",
          "ease-move": "cubic-bezier(0.45, 0, 0.2, 1)"}  # motion.md's defaults; DESIGN.md's tokens of the name win
NAME = re.compile(r"[A-Za-z][\w-]{0,63}", re.ASCII)  # T-1625 review: ASCII, as the messages say
PROP = re.compile(r"(?:--|-[a-z]+-)?[A-Za-z][\w-]{0,63}", re.ASCII)
NUM = r"-?(?:\d{1,9}(?:\.\d{0,9})?|\.\d{1,9})"  # bounded: no input makes these regexes backtrack for long
TIME = re.compile(r"(" + NUM + r")\s*(ms|s)")
_N = r"\s*(" + NUM + r")\s*"
BEZIER = re.compile(r"cubic-bezier\(" + ",".join([_N] * 4) + r"\)")
STEPS = re.compile(r"steps\(\s*(\d{1,4})\s*(?:,\s*(jump-start|jump-end|jump-none|jump-both|start|end)\s*)?\)")
_STOP = NUM + r"(?:\s+" + NUM + r"%){0,2}"
LINEAR = re.compile(r"linear\(\s*(" + _STOP + r"(?:\s*,\s*" + _STOP + r"){1,63})\s*\)")
SEP = re.compile(r":?-+:?")
NO_DESIGN = "no DESIGN.md (fm design extract writes its Tokens table)"


def _show(v):
    r = repr(v)
    return r if len(r) <= 60 else r[:59] + "…"


def design_path(score):
    """DESIGN.md next to the score, else at its repo's root or in docs/ there, else None."""
    import fmcore
    here = os.path.dirname(os.path.abspath(score))
    root = fmcore.git_root(here) or here
    return next((p for p in (os.path.join(d, "DESIGN.md") for d in (here, root, os.path.join(root, "docs")))
                 if os.path.isfile(p)), None)


def _cells(ln):
    cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", ln.strip())[1:]]
    if cells and not cells[-1]:
        cells.pop()
    return cells


def tokens_of(text):
    """({name without leading dashes: value}, [line of each table with no Light or Value column]) from a DESIGN.md's
    ## Tokens section, or (None, []) when it has none. Every table there counts: a row followed by a separator row is a
    header, and its Token and Light (fm design extract's) or Value column hold for the rows under it."""
    doc = text.replace("\r\n", "\n").split("\n")
    heads, _ = fmdesign.headings(doc)
    start = next((i for i, h in heads if re.fullmatch(r"##\s+tokens\s*#*", h, re.I)), None)
    if start is None:
        return None, []
    end = next((i for i, _ in heads if i > start), len(doc))
    rows = [(i, _cells(doc[i]) if doc[i].strip().startswith("|") else None) for i in range(start + 1, end)]
    out, blind, cols = {}, [], None
    for k, (i, cells) in enumerate(rows):
        if not cells:  # a line that isn't a row ends the table
            cols = None
            continue
        if all(SEP.fullmatch(c) for c in cells):
            continue
        nxt = rows[k + 1][1] if k + 1 < len(rows) else None
        if nxt and all(SEP.fullmatch(c) for c in nxt):  # a header
            low = [c.strip("`* ").lower() for c in cells]
            value = next((low.index(w) for w in ("light", "value") if w in low), None)
            cols = None if value is None else (low.index("token") if "token" in low else 0, value)
            if value is None:
                blind.append(i + 1)
            continue
        if cols and len(cells) > max(cols):
            name, value = cells[cols[0]].strip("`").strip(), cells[cols[1]]
            quoted = re.search(r"`([^`]*)`", value)
            if name:
                out.setdefault(name.lstrip("-"), (quoted.group(1) if quoted else value).strip())
    return out, blind


def _curve(text):
    """(curve, None) for a CSS easing (any case, spaces trimmed), (None, why) for a malformed bezier or steps(),
    None for anything else."""
    s = text.strip().lower()
    if s in KEYWORDS:
        return s, None
    m = BEZIER.fullmatch(s)
    if m:
        x1, y1, x2, y2 = m.groups()
        if not (0 <= float(x1) <= 1 and 0 <= float(x2) <= 1):
            return None, f"easing {_show(text)}: x1 and x2 must lie in 0–1"
        return f"cubic-bezier({x1}, {y1}, {x2}, {y2})", None
    m = STEPS.fullmatch(s)
    if m:
        n, pos = int(m.group(1)), m.group(2)
        if n < 1 or (pos == "jump-none" and n < 2):
            return None, f"easing {_show(text)}: steps() needs at least 1 step (2 with jump-none)"
        return f"steps({n}{', ' + pos if pos else ''})", None
    m = LINEAR.fullmatch(s)
    if m:
        return "linear(" + ", ".join(" ".join(p.split()) for p in m.group(1).split(",")) + ")", None
    return None


def _duration(v, look):
    """(ms, problem)."""
    if isinstance(v, bool) or not isinstance(v, (int, float, str)):
        return None, f"duration {_show(v)} must be a number of ms or a token name"
    if not isinstance(v, str):
        if 0 < v < 10:
            return None, f"duration {v:g}: bare numbers are ms; write '{v:g}s' (or '{v:g}ms' if you mean it)"
    else:
        s = shown = v.strip()
        if re.fullmatch(NUM, s):
            return None, f"duration {_show(v)} has no unit: write {s} (ms) or '{s}ms'"
        if not TIME.fullmatch(s):
            s, bad = look(shown, "duration")
            if bad:
                return None, bad
            if not TIME.fullmatch(s):
                return None, f"duration token {_show(shown)} is {_show(s)} in DESIGN.md, not a time"
        m = TIME.fullmatch(s)
        v = float(m.group(1)) * (1 if m.group(2) == "ms" else 1000)
        if v < 0:
            return None, f"duration {_show(shown)} is negative"
    v = round(v, 3)
    if not 0 <= v <= MAX_MS:  # nan and inf fail here too
        return None, f"duration {v:g} ms is outside 0–{MAX_MS}" if isinstance(v, float) else \
            f"duration {_show(v)} ms is outside 0–{MAX_MS}"
    return (int(v) if v == int(v) else v), None


def _easing(v, tokens, look):
    """(curve, problem)."""
    if not isinstance(v, str):
        return None, f"easing {_show(v)} must be a string"
    got = _curve(v)
    if got:
        return got
    s = v.strip()
    if s.lstrip("-") in tokens or s.startswith("--"):
        t, bad = look(s, "easing")
        if bad:
            return None, bad
        return _curve(t) or (None, f"easing token {_show(s)} is {_show(t)} in DESIGN.md, not an easing")
    if s.lower() in CURVES:
        return CURVES[s.lower()], None
    return None, f"unknown easing {_show(v)} (a CSS keyword, cubic-bezier(…), steps(…), linear(…), " \
                 "ease-enter/-exit/-move or a token)"


def _properties(v):
    if not isinstance(v, list) or not v or not all(isinstance(p, str) for p in v):
        return None, [f"properties must be a non-empty list of CSS property names, not {_show(v)}"]
    bad = [f"property {_show(p)} is not a CSS property name" for p in v if p != "all" and not PROP.fullmatch(p)]
    return v, bad + (["properties: list them, not all"] if "all" in v else [])


def parse(path):
    """The score's data: TOML, or JSON for a .json file. ValueError when it can't be read or parsed."""
    text, why = fmdesign._read(path, strict=True)
    if text is None:
        raise ValueError(f"{path}: {why}")
    try:
        data = json.loads(text) if path.lower().endswith(".json") else tomllib.loads(text)
    except (ValueError, RecursionError) as e:  # both decoders raise ValueErrors naming the line
        raise ValueError(f"{path}: {e or 'nested too deep'}") from None
    if not isinstance(data, dict):
        raise ValueError(f"{path}: the score is a table holding [[motion]] entries, not {type(data).__name__}")
    return data


def _lookup(design):
    """(tokens, look): DESIGN.md's tokens, and look(name, kind) -> (value, problem) for a token a motion names."""
    tokens, why, note = {}, NO_DESIGN, None
    if design:
        text, err = fmdesign._read(design, strict=True)
        found, blind = tokens_of(text) if text is not None else ({}, [])
        tokens = found or {}
        note = blind and f"DESIGN.md's Tokens table at line {blind[0]} has no Light or Value column"
        why = f"DESIGN.md: {err}" if text is None else None if tokens else \
            "DESIGN.md has no ## Tokens table (fm design extract writes one)" if found is None else \
            note or "DESIGN.md's Tokens table lists no tokens"

    def look(name, kind):
        t = tokens.get(name.lstrip("-"))
        if t is None:
            return None, f"{kind} {_show(name)}: {why}" if why else \
                f"DESIGN.md has no token {_show(name)}" + (f" ({note})" if note else "")
        if t.endswith("…"):
            return None, f"{kind} token {_show(name)}: its DESIGN.md value {_show(t)} was truncated by fm design " \
                         "extract; rerun it, or write the value in the score"
        return t, None
    return tokens, look


def check(path):
    """{score, design, motions, problems}: each motion resolved (ms, curve; None where it can't be) and each problem
    as {motion: its name, or "motion N" when the name is bad, or None for the file; problem: text}."""
    data = parse(path)
    design = design_path(path)
    tokens, look = _lookup(design)
    problems, motions, seen = [], [], set()

    def flag(who, text):
        problems.append({"motion": who, "problem": text})

    for k in sorted(set(data) - {"motion"}):
        flag(None, f"unknown key {_show(k)} (the score holds [[motion]] entries or [motion.NAME] tables)")
    entries, keys = data.get("motion"), None
    if not entries:
        flag(None, "no motions ([[motion]] entries or [motion.NAME] tables)")
        entries = []
    elif isinstance(entries, dict):  # [motion.NAME] tables: the key is the name
        keys, entries = list(entries), list(entries.values())
    elif not isinstance(entries, list):
        flag(None, "motion must be [[motion]] entries or [motion.NAME] tables")
        entries = []
    for i, m in enumerate(entries, 1):
        if not isinstance(m, dict):
            flag(f"motion {i}", f"not a table: {_show(m)}")
            continue
        clash = None
        if keys:
            clash = m["name"] if "name" in m and m["name"] != keys[i - 1] else None
            m = {**m, "name": keys[i - 1]}
        name = m.get("name")
        who = name if isinstance(name, str) and NAME.fullmatch(name) else f"motion {i}"
        if "name" not in m:
            flag(who, "no name")
        elif who != name:
            flag(who, f"name {_show(name)} must be letters, digits, - or _, starting with a letter (at most 64)")
        elif name in seen:
            flag(who, "the name is used twice")
        if clash is not None:
            flag(who, f"name {_show(clash)} differs from its table key")
        seen.add(who)
        for k in sorted(set(m) - set(KEYS), key=str):
            flag(who, f"unknown key {_show(k)} ({', '.join(KEYS)})")
        ms, bad = _duration(m["duration"], look) if "duration" in m else (None, "no duration")
        curve, bad2 = _easing(m["easing"], tokens, look) if "easing" in m else (None, "no easing")
        props, bad3 = _properties(m["properties"]) if "properties" in m else \
            (None, ["no properties (list what it animates)"])
        reduced = m.get("reduced")
        bad4 = "no reduced form (none, fade or instant)" if "reduced" not in m else None if reduced in REDUCED \
            else f"reduced form {_show(reduced)} is not none, fade or instant"
        for b in [bad, bad2, *bad3, bad4]:
            if b:
                flag(who, b)
        motions.append({"name": who, "ms": ms, "curve": curve, "properties": props,
                        "reduced": reduced if reduced in REDUCED else None})
    return {"score": path, "design": design, "motions": motions, "problems": problems}


TARGETS = ("css", "waapi", "three")
NAMED = {"linear": "linear(0, 1)", "ease": "cubic-bezier(0.25, 0.1, 0.25, 1)", "ease-in": "cubic-bezier(0.42, 0, 1, 1)",
         "ease-out": "cubic-bezier(0, 0, 0.58, 1)", "ease-in-out": "cubic-bezier(0.42, 0, 0.58, 1)",
         "step-start": "steps(1, jump-start)", "step-end": "steps(1, jump-end)"}  # CSS Easing's own definitions
REDUCED_NOTE = ('form "none" plays nothing (it stays in its rest state), "instant" goes to the end state at once '
                '(duration 0), "fade" animates opacity only over the same duration')


def curve_data(curve):
    """A resolved curve as data for three.js, which has no CSS easings: ["bezier", x1, y1, x2, y2], ["steps", n,
    "jump-…"] or ["linear", [[x, y], …]] with every x filled in as CSS Easing 2's linear() does."""
    curve = NAMED.get(curve, curve)
    m = BEZIER.fullmatch(curve)
    if m:
        return ["bezier", *map(float, m.groups())]
    m = STEPS.fullmatch(curve)
    if m:
        pos = m.group(2) or "end"
        return ["steps", int(m.group(1)), pos if pos.startswith("jump-") else "jump-" + pos]
    stops = LINEAR.fullmatch(curve).group(1).split(",")
    pts, top = [], float("-inf")
    for i, stop in enumerate(stops):  # a missing x: 0 first, max(1, the largest so far) last, else spaced evenly
        y, *xs = stop.split()
        bare = 0.0 if i == 0 else max(1.0, top) if i == len(stops) - 1 else None
        for x in [float(x[:-1]) / 100 for x in xs] or [bare]:
            if x is not None:
                x = top = max(top, x)  # an x below an earlier one is raised to it
            pts.append([x, float(y)])
    known = [i for i, p in enumerate(pts) if p[0] is not None]
    for a, b in zip(known, known[1:]):
        for k in range(a + 1, b):
            pts[k][0] = pts[a][0] + (pts[b][0] - pts[a][0]) * (k - a) / (b - a)
    return ["linear", pts]


def _variants(m):
    """(a motion's parameters, its reduced form's), each {duration ms, easing, properties}; the reduced one names its
    form too."""
    form = m["reduced"]
    return ({"duration": m["ms"], "easing": m["curve"], "properties": m["properties"]},
            {"form": form, "duration": m["ms"] if form == "fade" else 0, "easing": m["curve"],
             "properties": ["opacity"] if form == "fade" else m["properties"] if form == "instant" else []})


def _label(name):
    """The score's file name for a header comment: quoted, ASCII, and unable to end a /* */ comment or a <script>."""
    return json.dumps(name).replace("*/", "*\\/").replace("</", "<\\/")


def _css(motions, label):
    root, reduced, frames = [], [], []
    for m in motions:
        n, full, red = m["name"], *_variants(m)
        for v, into, ind in ((full, root, "  "), (red, reduced, "    ")):
            ms, curve = f"{json.dumps(v['duration'])}ms", v["easing"]
            frame = f"reduced-motion-{n}" if v.get("form") == "fade" else f"motion-{n}"
            tr, an = ("all 0s", "none") if v.get("form") == "none" else \
                (", ".join(f"{p} {ms} {curve}" for p in v["properties"]), f"{frame} {ms} {curve} backwards")
            # all 0s, not none: none is only valid alone, so it would void a comma list holding other motions
            into += [f"{ind}--motion-{n}-duration: {ms};", f"{ind}--motion-{n}-easing: {curve};",
                     f"{ind}--motion-{n}-transition: {tr};", f"{ind}--motion-{n}-animation: {an};"]
        starts = " ".join(f"{p}: var(--motion-{n}-from-{p});" for p in full["properties"])
        frames.append(f"@keyframes motion-{n} {{\n  from {{ {starts} }}\n}}")
        if red["form"] == "fade":
            frames.append(f"@keyframes reduced-motion-{n} {{\n  from {{ opacity: var(--motion-{n}-from-opacity, 0); }}"
                          "\n}")
    plain = "\n".join(ln[2:] for ln in reduced)
    return "\n".join([
        f"/* fm motion compile --to css (T-1625): {len(motions)} motion(s) from {label}.",
        "   Each motion NAME sets --motion-NAME-duration, -easing, -transition (for transition:) and -animation (for",
        "   animation:, which starts from var(--motion-NAME-from-PROPERTY), set where it plays, and ends at the",
        "   element's own style). Under prefers-reduced-motion, unless <html data-motion=\"full\">, or with",
        "   <html data-motion=\"reduce\">, each motion takes its reduced form: none plays nothing (the element sits in",
        "   its rest state; transition all 0s, animation none), instant jumps to the end state (0ms), fade animates",
        "   opacity only over the same duration.",
        "*/", ":root {", *root, "}", *frames, "@media (prefers-reduced-motion: reduce) {",
        '  :root:not([data-motion="full"]) {', *reduced, "  }", "}", ':root[data-motion="reduce"] {', plain, "}", ""])


THREE_EASE = """\
const bezier = (x1, y1, x2, y2) => {
  const at = (a, b, t) => 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3;
  return (p) => {
    if (p <= 0 || p >= 1) return p <= 0 ? 0 : 1;
    let lo = 0, hi = 1;  // x(t) rises with t when x1 and x2 lie in 0-1, as fm motion check makes sure
    for (let i = 0; i < 40; i++) { const t = (lo + hi) / 2; if (at(x1, x2, t) < p) lo = t; else hi = t; }
    return at(y1, y2, (lo + hi) / 2);
  };
};
const steps = (n, pos) => {
  const jumps = pos === "jump-none" ? n - 1 : pos === "jump-both" ? n + 1 : n;
  const lead = pos === "jump-start" || pos === "jump-both" ? 1 : 0;
  return (p) => Math.min(Math.max(Math.floor(p * n) + lead, 0), jumps) / jumps;
};
const linear = (pts) => (p) => {
  let i = 1;
  while (i < pts.length - 1 && pts[i][0] <= p) i++;
  const [[x0, y0], [x1, y1]] = [pts[i - 1], pts[i]];
  return x1 === x0 ? y1 : y0 + ((y1 - y0) * (p - x0)) / (x1 - x0);
};
const ease = ([kind, ...a]) => (kind === "steps" ? steps(...a) : kind === "linear" ? linear(a[0]) : bezier(...a));
for (const m of Object.values(motion)) for (const v of [m, m.reduced]) v.ease = ease(v.curve);
"""
PICK = """\
// as the CSS: reduced under the system's prefers-reduced-motion unless <html data-motion="full">, and always with
// data-motion="reduce" (the motion playbook's app setting)
export const reduced = () => {
  const set = typeof document === "object" ? document.documentElement.dataset.motion : undefined;
  const system = typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion: reduce)").matches;
  return set === "reduce" || (set !== "full" && system);
};
export const pick = (name) => (reduced() ? motion[name].reduced : motion[name]);
"""
PLAY = """\
// play(el, NAME, frames): el.animate() in whichever form applies, keeping only the properties that form lists (a fade
// needs opacity in the frames); null for "none", which plays nothing: play(...)?.finished
export const play = (el, name, frames) => {
  const m = pick(name);
  if (m.form === "none") return null;
  const camel = (p) => (p === "float" ? "cssFloat" : p.startsWith("--") ? p : p.replace(/-([a-z])/g, (_, c) => c.toUpperCase()));
  const keep = new Set([...m.properties.map(camel), "offset", "easing", "composite"]);
  const only = (f) => Object.fromEntries(Object.entries(f).filter(([k]) => keep.has(k)));
  return el.animate(Array.isArray(frames) ? frames.map(only) : only(frames), { duration: m.duration, easing: m.easing });
};
"""


def _module(motions, label, to):
    data = {}
    for m in motions:
        full, red = _variants(m)
        if to == "three":
            full["curve"] = red["curve"] = curve_data(m["curve"])
        data[m["name"]] = {**full, "reduced": red}
    head = (f"fm motion compile --to {to} (T-1625): {len(motions)} motion(s) from {label}. " + (
        "motion[NAME] is el.animate()'s options: duration in ms, easing as CSS writes it, and properties, what its "
        "keyframes may animate." if to == "waapi" else
        "three.js has no tweens or easings of its own, so motion[NAME] holds tween parameters: duration in ms (the "
        "same numbers as CSS and WAAPI; / 1000 for an AnimationClip's seconds), easing as CSS writes it, curve as data, "
        "and ease(p), that curve as a function from progress 0-1 to 0-1 (tween.js: .easing(m.ease)); steps() and "
        "linear() map exactly; a fade is material.opacity with transparent: true.")
        + f" motion[NAME].reduced is its reduced form: {REDUCED_NOTE}. pick(NAME) gives whichever applies now"
        + (", play(el, NAME, frames) runs it." if to == "waapi" else "."))
    rows = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in data.items())  # one motion a line: diffable
    body = [f"export const motion = {{\n{rows}\n}};"] + ([THREE_EASE] if to == "three" else [])
    return "\n".join(["// " + ln for ln in textwrap.wrap(head, 114)] + body + [PICK + (PLAY if to == "waapi" else "")])


def compile_score(path, to):
    """(the score at path compiled for to, one of TARGETS, [] ) or (None, check's problems) when it isn't clean.
    ValueError when it can't be read."""
    if to not in TARGETS:
        raise ValueError(f"--to {_show(to)}: one of {', '.join(TARGETS)}")
    got = check(path)
    if got["problems"]:
        return None, got["problems"]
    label = _label(os.path.basename(path))
    return (_css(got["motions"], label) if to == "css" else _module(got["motions"], label, to)), []


def _report(problems, label):
    return [f"{p['motion'] or label}: {p['problem']}" for p in problems]


def cmd_motion(args):
    import sys
    import fmcli
    import fmcore
    act, path = args.action, args.path
    for flag, v in (("--to", args.to), ("--out", args.out)):
        if act == "check" and v is not None:
            print(f"fm: motion check: {flag} is for compile (fm motion compile [PATH] {flag} …)", file=sys.stderr)
            return 2
    if not path:
        root = fmcore.git_root(os.getcwd()) or os.getcwd()
        path = os.path.join(root, "motion.toml")
        if not os.path.lexists(path):
            print(f"fm: motion {act}: no motion.toml at {root} (fm motion {act} PATH names another)", file=sys.stderr)
            return 2
    label = os.path.basename(path)
    try:
        if act == "compile":
            to = args.to or "css"
            text, problems = compile_score(path, to)
            out = os.path.abspath(args.out) if args.out else None  # write_atomic makes dirname(path): "" if bare
            if problems:  # stdout stays for the compiled text; --json puts {problems} there, as check does
                if getattr(args, "json", False):
                    fmcli.out(args, {"problems": problems}, None)
                else:
                    print("\n".join(_report(problems, label) + [f"motion compile: {len(problems)} problem(s), "
                                                                f"nothing compiled ({path})"]), file=sys.stderr)
                return 1
            if out and os.path.exists(out) and os.path.samefile(out, path):
                raise ValueError(f"--out {args.out} is the score it compiles")
            if out:
                fmcore.write_atomic(out, text)  # via a temp file: a symlink at out is replaced, never written through
                fmcli.out(args, {"out": args.out, "to": to, "bytes": len(text.encode())}, f"wrote {args.out}")
            else:
                fmcli.out(args, {"to": to, "text": text}, text.rstrip("\n"))
            return 0
        got = check(path)
    except (OSError, ValueError, RecursionError) as e:
        print(f"fm: motion {act}: {e or 'nested too deep'}", file=sys.stderr)
        return 2
    n, m = len(got["problems"]), len(got["motions"])
    text = "\n".join(_report(got["problems"], label)
                     + [f"motion check: {n} problem(s) in {m} motion(s) ({path})" if n else
                        f"motion check: clean, {m} motion(s) ({path})"])
    fmcli.out(args, got, text)
    return 1 if n else 0
