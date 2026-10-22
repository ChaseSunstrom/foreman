"""T-1624: the Motion Score. One file (motion.toml at the project root, or a .json with the same schema) names each
motion the UI uses, so timing and the reduced-motion path are decided once and checked, not scattered through CSS:

    [[motion]]
    name = "menu-enter"                  # letters, digits, - and _
    duration = "--dur-enter"             # ms (220), "220ms"/"0.2s", or a token in DESIGN.md's Tokens table
    easing = "ease-enter"                # a CSS keyword, cubic-bezier(…), motion.md's ease-enter/-exit/-move, a token
    properties = ["opacity", "transform"]
    reduced = "fade"                     # under prefers-reduced-motion: none (dropped: a pulse that changes no state),
                                         # fade (opacity only, same duration) or instant (jumps to the end state)

check(path) lists its problems; fm motion check [PATH] prints them (exit 1 on any). Compilers to CSS, WAAPI and
three.js read the same resolved motions."""
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
PROP = re.compile(r"(?:--)?[A-Za-z][\w-]{0,63}")
_N = r"\s*(-?(?:\d+\.?\d*|\.\d+))\s*"
BEZIER = re.compile(r"cubic-bezier\(" + ",".join([_N] * 4) + r"\)")
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


def tokens_of(text):
    """{name without leading dashes: value} from the ## Tokens table of a DESIGN.md (the Light column fm design
    extract writes, or a Value column)."""
    doc = text.replace("\r\n", "\n").split("\n")
    heads, _ = fmdesign.headings(doc)
    start = next((i for i, h in heads if h == "## Tokens"), None)
    if start is None:
        return {}
    end = next((i for i, _ in heads if i > start), len(doc))
    out, cols = {}, None
    for ln in doc[start + 1:end]:
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", ln)[1:]]
        if cells and not cells[-1]:
            cells.pop()
        if cols is None:  # the header row
            low = [c.lower() for c in cells]
            cols = (low.index("token") if "token" in low else 0,
                    next((low.index(k) for k in ("light", "value") if k in low), 2))
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells) or len(cells) <= max(cols):
            continue
        name, value = cells[cols[0]].strip("`").strip(), cells[cols[1]]
        quoted = re.search(r"`([^`]*)`", value)
        out.setdefault(name.lstrip("-"), (quoted.group(1) if quoted else value).strip())
    return out


def _curve(text):
    """(curve, None) for a CSS keyword or a well-formed cubic-bezier(), (None, why) for a bad bezier, None else."""
    if text in KEYWORDS:
        return text, None
    m = BEZIER.fullmatch(text.strip())
    if not m:
        return None
    x1, y1, x2, y2 = m.groups()
    if not (0 <= float(x1) <= 1 and 0 <= float(x2) <= 1):
        return None, f"easing {_show(text)}: x1 and x2 must lie in 0–1"
    return f"cubic-bezier({x1}, {y1}, {x2}, {y2})", None


def _duration(v, tokens, why):
    """(ms, problem)."""
    if isinstance(v, bool) or not isinstance(v, (int, float, str)):
        return None, f"duration {_show(v)} must be a number of ms or a token name"
    if isinstance(v, str):
        if fmdesign.TIME.fullmatch(v.strip()):
            v = fmdesign._seconds(v.strip()) * 1000
        elif v.lstrip("-") in tokens:
            t = tokens[v.lstrip("-")]
            if not fmdesign.TIME.fullmatch(t):
                return None, f"duration token {v} is {_show(t)} in DESIGN.md, not a time"
            v = fmdesign._seconds(t) * 1000
        else:
            return None, f"duration {_show(v)}: {why}" if why else f"DESIGN.md has no token {_show(v)}"
    v = round(v, 3)
    if not 0 <= v <= MAX_MS:  # nan and inf fail here too
        return None, f"duration {v:g} ms is outside 0–{MAX_MS}" if isinstance(v, float) else \
            f"duration {_show(v)} ms is outside 0–{MAX_MS}"
    return (int(v) if v == int(v) else v), None


def _easing(v, tokens, why):
    """(curve, problem)."""
    if not isinstance(v, str):
        return None, f"easing {_show(v)} must be a string"
    got = _curve(v)
    if got:
        return got
    key = v.lstrip("-")
    if key in tokens:
        got = _curve(tokens[key])
        return got or (None, f"easing token {v} is {_show(tokens[key])} in DESIGN.md, not an easing")
    if v in CURVES:
        return CURVES[v], None
    if v.startswith("--"):
        return None, f"easing {_show(v)}: {why}" if why else f"DESIGN.md has no token {_show(v)}"
    return None, f"unknown easing {_show(v)} (a CSS keyword, cubic-bezier(…), ease-enter/-exit/-move or a token)"


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


def check(path):
    """{score, design, motions, problems}: each motion resolved (ms, curve; None where it can't be) and each problem
    as {motion: its name, or "motion N" when the name is bad, or None for the file; problem: text}."""
    data = parse(path)
    design = design_path(path)
    tokens, why = {}, NO_DESIGN
    if design:
        text, err = fmdesign._read(design, strict=True)
        tokens = tokens_of(text) if text is not None else {}
        why = f"DESIGN.md: {err}" if text is None else None if tokens else "DESIGN.md has no ## Tokens table " \
            "(fm design extract writes one)"
    problems, motions, seen = [], [], set()

    def flag(who, text):
        problems.append({"motion": who, "problem": text})

    for k in sorted(set(data) - {"motion"}):
        flag(None, f"unknown key {_show(k)} (the score holds [[motion]] entries)")
    entries = data.get("motion")
    if not entries:
        flag(None, "no [[motion]] entries")
    elif not isinstance(entries, list):
        flag(None, "motion must be an array of tables: [[motion]], one per motion")
        entries = []
    for i, m in enumerate(entries or [], 1):
        if not isinstance(m, dict):
            flag(f"motion {i}", f"not a table: {_show(m)}")
            continue
        name = m.get("name")
        who = name if isinstance(name, str) and NAME.fullmatch(name) else f"motion {i}"
        if "name" not in m:
            flag(who, "no name")
        elif who != name:
            flag(who, f"name {_show(name)} must be letters, digits, - or _, starting with a letter (at most 64)")
        elif name in seen:
            flag(who, "the name is used twice")
        seen.add(who)
        for k in sorted(set(m) - set(KEYS), key=str):
            flag(who, f"unknown key {_show(k)} ({', '.join(KEYS)})")
        ms, bad = _duration(m["duration"], tokens, why) if "duration" in m else (None, "no duration")
        curve, bad2 = _easing(m["easing"], tokens, why) if "easing" in m else (None, "no easing")
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
    except ValueError as e:
        print(f"fm: motion check: {e}", file=sys.stderr)
        return 2
    label = os.path.basename(path)
    n, m = len(got["problems"]), len(got["motions"])
    text = "\n".join([f"{p['motion'] or label}: {p['problem']}" for p in got["problems"]]
                     + [f"motion check: {n} problem(s) in {m} motion(s) ({path})" if n else
                        f"motion check: clean, {m} motion(s) ({path})"])
    fmcli.out(args, got, text)
    return 1 if n else 0
