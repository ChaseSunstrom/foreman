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

check(path) lists its problems; fm motion check [PATH] prints them (exit 1 on any). Compilers to CSS, WAAPI and
three.js read the same resolved motions and must keep those three meanings."""
import json
import os
import re
import tomllib

import fmdesign

KEYS = ("name", "duration", "easing", "properties", "reduced")
REDUCED = ("none", "fade", "instant")
MAX_MS = 2000
KEYWORDS = {"linear", "ease", "ease-in", "ease-out", "ease-in-out", "step-start", "step-end"}
CURVES = {"ease-enter": "cubic-bezier(0.05, 0.7, 0.1, 1)", "ease-exit": "cubic-bezier(0.3, 0, 0.8, 0.15)",
          "ease-move": "cubic-bezier(0.45, 0, 0.2, 1)"}  # motion.md's defaults; DESIGN.md's tokens of the name win
NAME = re.compile(r"[A-Za-z][\w-]{0,63}")
PROP = re.compile(r"(?:--|-[a-z]+-)?[A-Za-z][\w-]{0,63}")
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


def cmd_motion(args):
    import sys
    import fmcli
    import fmcore
    path = args.path
    if not path:
        root = fmcore.git_root(os.getcwd()) or os.getcwd()
        path = os.path.join(root, "motion.toml")
        if not os.path.lexists(path):
            print(f"fm: motion check: no motion.toml at {root} (fm motion check PATH names another)", file=sys.stderr)
            return 2
    try:
        got = check(path)
    except (ValueError, RecursionError) as e:
        print(f"fm: motion check: {e or 'nested too deep'}", file=sys.stderr)
        return 2
    label = os.path.basename(path)
    n, m = len(got["problems"]), len(got["motions"])
    text = "\n".join([f"{p['motion'] or label}: {p['problem']}" for p in got["problems"]]
                     + [f"motion check: {n} problem(s) in {m} motion(s) ({path})" if n else
                        f"motion check: clean, {m} motion(s) ({path})"])
    fmcli.out(args, got, text)
    return 1 if n else 0
