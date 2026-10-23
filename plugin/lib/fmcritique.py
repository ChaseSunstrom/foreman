"""fm critique (T-1642): what a page really uses, held to DESIGN.md. fm critique URL|FILE loads the page in a headless
Chromium already here (fm shot's, T-1636; nothing is installed) and takes a computed-style census: every colour,
font family, font size, radius, shadow and spacing value its visible elements use, with counts, read under fm shot's
frozen profile. Like fm flow it opens files and localhost only unless --any-url, and every request the page makes is
held to that rule (T-1639); a request blocked or a page that ends up at another URL is noted. A .json FILE is a
census already taken (fm critique URL --json writes one under "census"). The census is critiqued against DESIGN.md's
## Tokens table (fm design extract writes it): values no token names, near-duplicates (colours under NEAR_DE apart in
OKLab, lengths within NEAR_REL of each other) and outliers (a value no token names, used once or twice). Exit 1 on
any finding, 0 clean, 2 when it couldn't run (no browser: "not run") or --design can't be read. With no tokens to
hold the census to, the last line says it wasn't checked against DESIGN.md.

fm critique URL --why SELECTOR prints the cascade behind the first element the selector matches: its matched rules,
winner first, and the winning declaration per property (inherited ones from the nearest ancestor that sets them), with
each rule's stylesheet and the computed value where it differs; WHY_RULES rules and WHY_WINNERS declarations at most.

Page text is untrusted: every value has its Cc/Cf/Co/Cs characters replaced (fmshot.safe) and is capped before it is
printed."""
import functools
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request

import fmdesign
import fmflow
import fmshot

KINDS = ("colour", "font", "size", "radius", "shadow", "spacing")
NEAR_DE = 0.02  # OKLab distance: about one just-noticeable difference
NEAR_REL = 0.07  # lengths: 15px and 16px are near, 1px and 2px aren't
MAX_ELEMENTS, MAX_VALUES, MAX_TEXT, MAX_NEAR, SHOW = 5000, 300, 80, 100, 20
WHY_RULES, WHY_WINNERS = 20, 60
REM = 16  # ponytail: rem tokens taken at the browser default; a page that sets html's font-size reads them wrong
SHAPE = "a census is {url, elements, values: {kind: {value: count}}} with kinds " + ", ".join(KINDS)
# Runs in the page with one JSON argument {max, values, text}; returns {elements, capped, values, dropped}. Fixed: no
# page or user text is ever spliced into it.
CENSUS_JS = r"""(function (opt) {
  const out = {}, seen = {}, dropped = {};
  for (const k of ["colour", "font", "size", "radius", "shadow", "spacing"]) {
    out[k] = Object.create(null); seen[k] = 0; dropped[k] = 0;
  }
  const add = (k, v) => {
    if (!v) return;
    v = String(v).slice(0, opt.text);
    if (v in out[k]) out[k][v]++;
    else if (seen[k] < opt.values) { out[k][v] = 1; seen[k]++; }
    else dropped[k]++;
  };
  const all = document.querySelectorAll("*");
  let n = 0;
  for (const el of all) {
    if (n >= opt.max) break;
    if (!el.getClientRects().length) continue;
    n++;
    const s = getComputedStyle(el), own = {colour: new Set(), radius: new Set(), spacing: new Set(), shadow: new Set()};
    if ([...el.childNodes].some(c => c.nodeType === 3 && c.data.trim())) {
      own.colour.add(s.color); add("font", s.fontFamily); add("size", s.fontSize);
    }
    if (!/^transparent$|^rgba\(.*,\s*0\)$|\/\s*0\)$/.test(s.backgroundColor))  // rgb(0, 255, 0) is green
      own.colour.add(s.backgroundColor);
    for (const side of ["Top", "Right", "Bottom", "Left"]) {
      if (parseFloat(s["border" + side + "Width"]) > 0 && s["border" + side + "Style"] !== "none")
        own.colour.add(s["border" + side + "Color"]);
      for (const p of ["padding", "margin"]) if (parseFloat(s[p + side])) own.spacing.add(s[p + side]);
    }
    for (const g of [s.rowGap, s.columnGap]) if (parseFloat(g)) own.spacing.add(g);
    for (const c of ["TopLeft", "TopRight", "BottomRight", "BottomLeft"])
      if (parseFloat(s["border" + c + "Radius"])) own.radius.add(s["border" + c + "Radius"]);
    for (const sh of [s.boxShadow, s.textShadow]) if (sh && sh !== "none") own.shadow.add(sh);
    for (const k in own) for (const v of own[k]) add(k, v);
  }
  return {elements: n, capped: n < all.length && n >= opt.max, values: out, dropped: dropped};
})"""
INHERITS = {"color", "cursor", "direction", "letter-spacing", "line-height", "list-style", "list-style-type",
            "list-style-position", "list-style-image", "quotes", "text-align", "text-indent", "text-transform",
            "text-shadow", "visibility", "white-space", "word-spacing", "word-break", "overflow-wrap", "hyphens",
            "tab-size", "caret-color", "accent-color", "color-scheme", "writing-mode"}  # and font*, --custom
LENGTH_WORDS = (("radius", {"radius", "rounded", "round", "corner"}), ("size", {"size", "text", "fs", "type"}),
                ("spacing", {"space", "spacing", "gap", "pad", "padding", "margin", "gutter", "inset"}))


def clean(v, n=MAX_TEXT):
    """Page text for the terminal: one line, every Cc/Cf/Co/Cs character a ? (fmshot.safe), at most n characters."""
    s = fmshot.safe(" ".join(str(v).split()))
    return s if len(s) <= n else s[:n - 1] + "…"


def _px(v):
    m = re.fullmatch(r"(-?\d*\.?\d+)(px|rem)?", v.strip().lower())
    if not m or (m[2] is None and float(m[1]) != 0):
        return None
    x = float(m[1]) * (REM if m[2] == "rem" else 1)
    return x if math.isfinite(x) else None


def _fmt(x):
    return f"{round(x, 2):g}px"


RGBA = re.compile(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)\s*[,/]\s*([\d.]+)(%?)\s*\)")


def _colour(v):
    """#RRGGBB, or #RRGGBB/alpha for a translucent rgba() or #rrggbbaa; None for anything else."""
    rgb = fmdesign.parse_colour(v)
    if rgb:
        return fmdesign.hex_of(rgb)
    t = v.strip().lower()
    m = RGBA.fullmatch(t)
    if m:
        rgb, a = [float(m[i]) / 255 for i in (1, 2, 3)], float(m[4]) / (100 if m[5] else 1)
    elif re.fullmatch(r"#[0-9a-f]{8}", t):
        rgb, a = [int(t[i:i + 2], 16) / 255 for i in (1, 3, 5)], int(t[7:], 16) / 255
    else:
        return None
    return f"{fmdesign.hex_of([min(max(x, 0.0), 1.0) for x in rgb])}/{round(min(a, 1.0), 2):g}"


def _shadow(v):
    """One spelling for a shadow list: per shadow its four lengths in px, then its colour (the computed form and the
    authored one meet here); the cleaned text when a part isn't read."""
    t = v.strip().lower()
    parts = []
    for one in re.split(r",(?![^(]*\))", t):
        col = re.search(r"(?:rgba?|hsla?|oklch|color)\([^)]*\)|#[0-9a-f]{3,8}\b|\b[a-z]+\b(?<!inset)", one)
        rest = (one[:col.start()] + " " + one[col.end():]) if col else one
        words = rest.split()
        nums = [_px(w) for w in words if w != "inset"]
        if None in nums or not 2 <= len(nums) <= 4:
            return clean(t)
        parts.append(("inset " if "inset" in words else "") + " ".join(_fmt(x) for x in (nums + [0.0] * 2)[:4]) + " "
                     + ((_colour(col[0]) or clean(col[0])) if col else "currentcolor"))
    return clean(", ".join(parts), 200)


def key(kind, v):
    """The value as the critique compares it: colours as hex, a font as its first family, lengths in px."""
    if kind == "colour":
        return _colour(v) or clean(v).lower()
    if kind == "font":
        return clean(re.split(r",", v)[0].strip().strip("'\"").lower())
    if kind == "shadow":
        return "none" if v.strip().lower() == "none" else _shadow(v)
    x = _px(v)
    return _fmt(x) if x is not None else clean(v).lower()


def _kinds(name, kind, v):
    """The census kinds a token's value can name."""
    words = set(re.split(r"[-_]+", name.lower().strip("-")))
    if kind == "colour" or not kind and _colour(v):
        return ("colour",)
    if kind == "shadow" or "shadow" in words:
        return ("shadow",)
    if _px(v) is not None:
        return tuple(k for k, w in LENGTH_WORDS if w & words) or ("size", "radius", "spacing")
    return ("font",) if kind == "font" or words & {"font", "family"} else ()


def token_index(tokens):
    """{kind: {key: token name}}: each value a DESIGN.md token holds (the first token of a value wins)."""
    idx = {k: {} for k in KINDS}
    for name, row in tokens.items():
        for v in (row["light"], row["light_hex"], row["dark"], row["dark_hex"]):
            if v and not v.endswith("…"):
                for k in _kinds(name, row["kind"], v):
                    idx[k].setdefault(key(k, v), name)
    return idx


def load(data):
    """The census cleaned: {url, elements, capped, values: {kind: {key: count}}}, at most MAX_VALUES a kind (the
    commonest); ValueError for a malformed one."""
    if not isinstance(data, dict) or not isinstance(data.get("values"), dict):
        raise ValueError(SHAPE)
    values, dropped = {}, 0
    for kind in KINDS:
        got = data["values"].get(kind) or {}
        if not isinstance(got, dict) or not all(isinstance(n, int) and not isinstance(n, bool) and n > 0
                                                for n in got.values()):
            raise ValueError(f"{SHAPE}; {kind} isn't")
        merged = {}
        for v, n in got.items():
            k = key(kind, str(v))
            merged[k] = merged.get(k, 0) + n
        top = sorted(merged.items(), key=lambda kv: (-kv[1], kv[0]))
        dropped += max(0, len(top) - MAX_VALUES)
        values[kind] = dict(top[:MAX_VALUES])
    el, gone = data.get("elements"), data.get("dropped")
    page = sum(n for n in gone.values() if isinstance(n, int) and not isinstance(n, bool) and n > 0) \
        if isinstance(gone, dict) else 0
    return {"url": clean(data.get("url") or "", 200), "elements": el if isinstance(el, int) else None,
            "capped": data.get("capped") is True, "dropped": dropped, "page_dropped": page, "values": values}


@functools.lru_cache(maxsize=4096)
def _oklab(hexed):
    L, C, h = fmdesign.oklch_of(fmdesign.parse_colour(hexed))
    return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))


def _near(kind, a, b):
    """The distance between two values of a kind when they are near-duplicates, else None."""
    if kind == "colour":
        (ha, _, aa), (hb, _, ab) = a.partition("/"), b.partition("/")
        if aa != ab or not re.fullmatch(r"#[0-9A-F]{6}", ha) or not re.fullmatch(r"#[0-9A-F]{6}", hb):
            return None
        d = math.dist(_oklab(ha), _oklab(hb))
        return round(d, 4) if d < NEAR_DE else None
    if kind in ("size", "radius", "spacing") and _px(a) is not None and _px(b) is not None:  # not "8px 4px"
        x, y = abs(_px(a)), abs(_px(b))
        d = abs(x - y) / max(x, y, 1e-9)
        return round(d, 3) if 0 < d <= NEAR_REL else None
    return None


def critique(census, tokens=None):
    """{census, tokens, named, unnamed, near, outliers}: tokens is read_design's dict, or None (no naming)."""
    idx = token_index(tokens) if tokens else None
    named, unnamed, near, outliers, total = {}, [], [], [], 0
    for kind in KINDS:
        vals = census["values"][kind]
        # a negative margin is its token's value negated
        names = {v: idx and (idx[kind].get(v) or v.startswith("-") and idx[kind].get(v[1:])) or None for v in vals}
        named[kind] = {v: n for v, n in names.items() if n}
        for v, n in vals.items():
            if not names[v]:
                if idx:
                    unnamed.append({"kind": kind, "value": v, "count": n})
                if n <= 2:
                    outliers.append({"kind": kind, "value": v, "count": n})
        items = list(vals.items())  # commonest first: a is the one to keep
        for i, (a, na) in enumerate(items):
            for b, nb in items[i + 1:]:
                if names[a] and names[b]:
                    continue  # two tokens: the scale's own choice
                d = _near(kind, a, b)  # at most MAX_VALUES² / 2 pairs a kind, each colour's OKLab memoised
                if d is not None:
                    total += 1
                    if len(near) < MAX_NEAR:
                        near.append({"kind": kind, "a": a, "a_count": na, "b": b, "b_count": nb, "distance": d})
    return {"census": census, "tokens": len(tokens or {}), "named": named, "unnamed": unnamed, "near": near,
            "near_total": total, "outliers": outliers}


def _list(title, rows, fmt):
    if not rows:
        return []
    return ["", f"{title} ({len(rows)}):"] + [f"  {fmt(r)}" for r in rows[:SHOW]] + \
        ([f"  … {len(rows) - SHOW} more (--json lists them all)"] if len(rows) > SHOW else [])


def report(res, notes):
    c = res["census"]
    els = f"{c['elements']} elements; " if c["elements"] is not None else ""
    lines = [f"fm critique: {c['url'] or 'census'} ({els}DESIGN.md: {res['tokens']} tokens)"]
    lines += [f"note: {clean(n, 300)}" for n in notes]
    for kind in KINDS:
        vals = c["values"][kind]
        if vals:
            shown = [f"{v} ×{n}" + (f" {res['named'][kind][v]}" if v in res["named"][kind] else "")
                     for v, n in list(vals.items())[:10]]
            lines.append(f"  {kind} ({len(vals)}): " + " · ".join(shown) + (f" · +{len(vals) - 10} more"
                                                                               if len(vals) > 10 else ""))
    lines += _list("Not named by DESIGN.md", res["unnamed"], lambda r: f"{r['kind']} {r['value']} ×{r['count']}"
                   + (" (outlier)" if r["count"] <= 2 else ""))  # the outliers, marked, not listed twice
    near = _list(f"Near-duplicates (colours under ΔE_OK {NEAR_DE:g}, lengths within {NEAR_REL:.0%})", res["near"],
                 lambda r: f"{r['kind']} {r['a']} ×{r['a_count']} ≈ {r['b']} ×{r['b_count']} ({r['distance']:g})")
    if near and res["near_total"] > len(res["near"]):
        near[1] = near[1].replace(f"({len(res['near'])}):", f"({res['near_total']}, the first {len(res['near'])} "
                                                             "kept):")
    lines += near
    if not res["tokens"]:
        lines += _list("Outliers (used once or twice)", res["outliers"],
                       lambda r: f"{r['kind']} {r['value']} ×{r['count']}")
    found = (len(res["unnamed"]), res["near_total"], len(res["outliers"]))
    last = f"critique: {found[0]} unnamed, {found[1]} near-duplicate pair(s), {found[2]} outlier(s)" if any(found) \
        else f"critique: clean, {sum(map(len, c['values'].values()))} values"
    lines += ["", last + ("" if res["tokens"] else "; not checked against DESIGN.md (no tokens)")]
    return "\n".join(lines)


# ---------------------------------------------------------------- the browser side


def _eval(b, expression):
    got = b.call("Runtime.evaluate", b.sid, expression=expression, returnByValue=True)
    if got.get("exceptionDetails"):
        raise RuntimeError("the page script failed: " + clean((got["exceptionDetails"].get("exception") or {})
                                                              .get("description") or "an exception", 200))
    return (got.get("result") or {}).get("value")


def _page(b, url, root, any_url):
    """Open url (fm shot's load) with every request it makes held to fm flow's rule: notes (what was blocked, a page
    that ended up elsewhere); RuntimeError when the page itself left the allowed pages."""
    seen = fmflow.guard(b, root, any_url)
    notes = fmshot.load(b, url)
    if seen["doc"]:
        raise RuntimeError(f"the page went outside the allowed pages, to {clean(seen['doc'], 200)} (blocked; "
                           "--any-url opens any http(s) page)")
    notes += [f"blocked {clean(u, 200)}: outside the allowed pages" for u in seen["other"]]
    href = _eval(b, "location.href")
    if isinstance(href, str) and href != url:
        notes.append(f"the page is at {clean(href, 200)}, not the URL asked for")
    return notes


def take(b, url, root, any_url):
    """(census as load() takes it, notes) for the page at url, under fm shot's frozen profile (clock fixed, finite
    animations finished, endless ones held at their start), so a census reads the same on every run."""
    b.call("Page.addScriptToEvaluateOnNewDocument", b.sid, source=fmshot.FREEZE)
    notes = _page(b, url, root, any_url)
    _eval(b, fmshot.HOLD)
    opt = {"max": MAX_ELEMENTS, "values": MAX_VALUES * 2, "text": 400}
    raw = _eval(b, f"({CENSUS_JS})({json.dumps(opt)})")
    if not isinstance(raw, dict):
        raise RuntimeError("the census script returned nothing")
    if raw.get("capped"):
        notes.append(f"read the first {MAX_ELEMENTS} visible elements only")
    return dict(raw, url=url), notes


def _source(style, line, sheets):
    """name:line of the rule's stylesheet (its URL's last part; an inline <style>: the page's line), or None."""
    h = (sheets or {}).get(style.get("styleSheetId"))
    if not isinstance(h, dict) or not isinstance(line, int):
        return None
    name = re.sub(r"[?#].*", "", str(h.get("sourceURL") or "")).rstrip("/").rsplit("/", 1)[-1] or "page"
    start = h.get("startLine") if h.get("isInline") and isinstance(h.get("startLine"), int) else 0
    return f"{name}:{start + line + 1}"


def _rules(block, inherited, sheets=None):
    """A matched-styles block's rules, lowest precedence first, its inline style last."""
    out = []
    for m in block.get("matchedCSSRules") or []:
        rule = m.get("rule") or {}
        sels = [s.get("text", "") for s in (rule.get("selectorList") or {}).get("selectors") or []]
        at = [i for i in m.get("matchingSelectors") or range(len(sels)) if isinstance(i, int) and 0 <= i < len(sels)]
        style = rule.get("style") or {}
        line = (style.get("range") or {}).get("startLine")
        out.append({"selector": ", ".join(sels[i] for i in at) or ", ".join(sels), "origin": rule.get("origin") or
                    "regular", "line": line + 1 if isinstance(line, int) else None,
                    "source": _source(style, line, sheets), "layered": bool(rule.get("layers")),
                    "decls": style.get("cssProperties") or [], "inherited": inherited})
    if (block.get("inlineStyle") or {}).get("cssProperties"):  # every element has one, mostly empty
        out.append({"selector": "style attribute", "origin": "inline", "line": None, "source": None,
                    "layered": False, "decls": block["inlineStyle"].get("cssProperties") or [],
                    "inherited": inherited})
    return out


def _winners(rules):
    """{property: (declaration, rule)}: a later rule wins, an !important one beats every normal one, a user-agent
    !important beats an author one. ponytail: cascade layers and @scope aren't weighed; DevTools' order is trusted."""
    best = {}
    for i, r in enumerate(rules):
        for d in r["decls"]:
            name = d.get("name")
            if not name or d.get("parsedOk") is False or d.get("disabled"):
                continue
            imp = bool(d.get("important"))
            rank = (imp, imp and r["origin"] == "user-agent", i)
            if name not in best or rank >= best[name][0]:
                best[name] = (rank, d, r)
    return {n: (d, r) for n, (_, d, r) in best.items()}


def cascade(matched, computed=None, sheets=None):
    """{rules, winners, notes} from CSS.getMatchedStylesForNode's answer: the element's rules winner first, and per
    property the winning declaration (inherited properties from the nearest ancestor setting them). sheets: {id:
    CSS.styleSheetAdded's header}, for each rule's source."""
    own = _rules(matched, False, sheets)
    win, layered = _winners(own), any(r["layered"] for r in own)
    for block in matched.get("inherited") or []:  # nearest ancestor first
        rules = _rules(block, True, sheets)
        layered = layered or any(r["layered"] for r in rules)
        for name, dr in _winners(rules).items():
            if name not in win and (name in INHERITS or name.startswith(("font", "--"))):
                win[name] = dr
    comp = {c.get("name"): c.get("value") for c in computed or [] if isinstance(c, dict)}
    pick = ("selector", "origin", "line", "source", "inherited")
    return {"rules": [{k: r[k] for k in pick} for r in reversed(own)],
            "winners": [dict({k: r[k] for k in pick}, property=n,  # DevTools' value keeps an !important in it
                             value=re.sub(r"\s*!\s*important\s*$", "", str(d.get("value", "")), flags=re.I),
                             important=bool(d.get("important")), computed=comp.get(n))
                        for n, (d, r) in sorted(win.items())],
            "notes": ["some matched rules sit in an @layer: the reversed layer order of !important declarations "
                      "isn't modelled, so an !important winner may be another"] if layered else []}


def why(b, url, selector, root, any_url):
    """(cascade, notes) for the first element selector matches, or (None, notes) when it matches none."""
    sheets = {}

    def added(p):  # each stylesheet's URL, for the rules' sources; capped, a page can add endless sheets
        h = p.get("header") or {}
        if len(sheets) < 5000 and isinstance(h, dict):
            sheets[h.get("styleSheetId")] = {k: h.get(k) for k in ("sourceURL", "isInline", "startLine")}
    b.on["CSS.styleSheetAdded"] = added
    notes = _page(b, url, root, any_url)
    b.call("DOM.enable", b.sid)
    b.call("CSS.enable", b.sid)  # sends styleSheetAdded for every sheet already there
    top = b.call("DOM.getDocument", b.sid, depth=0)["root"]["nodeId"]
    node = b.call("DOM.querySelector", b.sid, nodeId=top, selector=selector).get("nodeId")
    if not node:
        return None, notes
    matched = b.call("CSS.getMatchedStylesForNode", b.sid, nodeId=node)
    computed = b.call("CSS.getComputedStyleForNode", b.sid, nodeId=node).get("computedStyle")
    return cascade(matched, computed, sheets), notes


def _more(rows, cap):
    return [f"  … {len(rows) - cap} more (--json)"] if len(rows) > cap else []


def why_report(res, url, selector, notes):
    def where(r):
        return (f" ({clean(r['source'], 120)})" if r.get("source") else f" (line {r['line']})" if r["line"] else "") \
            + (f" [{r['origin']}]" if r["origin"] not in ("regular", "inline") else "")
    lines = [f"fm critique --why {clean(selector, 200)}: {clean(url, 200)}"]
    lines += [f"note: {clean(n, 300)}" for n in notes + res.get("notes", [])]
    lines += ["Matched rules, winner first:"] + [f"  {clean(r['selector'], 200)}{where(r)}"
                                                 for r in res["rules"][:WHY_RULES]] + _more(res["rules"], WHY_RULES)
    lines.append("Winning declarations:")
    for w in res["winners"][:WHY_WINNERS]:
        val = clean(w["value"], 200) + (" !important" if w["important"] else "")
        comp = w["computed"] is not None and clean(w["computed"], 200)
        lines.append(f"  {clean(w['property'])}: {val}  ← {clean(w['selector'], 120)}{where(w)}"
                     + (" (inherited)" if w["inherited"] else "") + (f"  = {comp}" if comp and comp != val else ""))
    return "\n".join(lines + _more(res["winners"], WHY_WINNERS))


# ---------------------------------------------------------------- the command


def _fail(msg):
    print(f"fm critique: {msg}", file=sys.stderr)
    return 2


def _tokens(design):
    """(tokens or None, notes) from DESIGN.md: --design (ValueError when it can't be read or has no tokens), else the
    one fm motion finds from here (a note when there is none or it has no tokens)."""
    import fmmotion
    if design:
        return fmdesign.read_design(design), []
    path = fmmotion.design_path(os.path.join(os.getcwd(), "DESIGN.md"))
    if not path:
        return None, [fmmotion.NO_DESIGN + ": nothing to name the values against"]
    try:
        return fmdesign.read_design(path), []
    except ValueError as e:
        return None, [str(e)]


def _root(word):
    """The folder a page's own files may come from: a file's folder (for a URL on the web: here)."""
    if re.match(r"(?i)file:", word):
        return os.path.dirname(urllib.request.url2pathname(urllib.parse.urlsplit(word).path))
    if re.match(r"(?i)[a-z][a-z0-9+.-]*:", word):
        return os.getcwd()
    return os.path.dirname(os.path.abspath(word))


def cmd_critique(args):
    import fmcli
    target, selector = args.target, args.why
    census = target.lower().endswith(".json") and os.path.isfile(target)
    if census and selector is not None:
        return _fail("--why needs a page (a URL or an HTML file), not a census")
    if selector is not None and not 0 < len(selector) <= 500:
        return _fail("--why takes a CSS selector of 1 to 500 characters")
    tokens, more = None, []
    if selector is None:  # a mistyped --design fails before any browser starts
        try:
            tokens, more = _tokens(args.design)
        except ValueError as e:
            return _fail(f"--design: {clean(e, 300)}")
    if census:
        text, err = fmdesign._read(target, strict=True)
        try:
            if text is None:
                raise ValueError(err)
            data, notes = load(json.loads(text)), []
        except (ValueError, RecursionError) as e:
            return _fail(f"{clean(target, 200)}: not a census: {e or 'nested too deep'} ({SHAPE})")
    else:
        root = _root(target)
        try:
            url = fmflow.target(target, root, args.any_url)
        except ValueError as e:  # fm flow's own words for the rule itself are about goto: said here instead
            why_not = "" if str(e).startswith("goto opens") else f": {clean(e, 300)}"
            return _fail(f"opens an HTML file, or http(s) on localhost, 127.0.0.1 or [::1] (--any-url: any http(s) "
                         f"page), or reads a census .json; not {clean(target, 200)}{why_not}")
        path, note = fmshot.find_browser("fm critique")
        if not path:
            fmcli.out(args, {"skipped": note}, f"fm critique: not run: {note}")
            return 2
        with fmshot.killable():  # SIGTERM unwinds, so the browser's process group dies
            try:
                b = fmshot.Browser(path, fmshot.SIZE)
            except (OSError, RuntimeError, EOFError, ValueError) as e:
                why_not = f"the browser ({fmshot.safe(path)}) did not start: {clean(e, 300)}"
                fmcli.out(args, {"skipped": why_not}, f"fm critique: not run: {why_not}")
                return 2
            try:
                if selector is not None:
                    res, notes = why(b, url, selector, root, args.any_url)
                    notes = ([note] if note else []) + notes
                    if res is None:
                        fmcli.out(args, {"url": url, "selector": selector, "matched": None, "notes": notes},
                                  f"fm critique --why: {clean(selector, 200)} matches nothing on {clean(url, 200)}")
                        return 1
                    fmcli.out(args, dict(res, url=url, selector=selector, notes=notes + res["notes"]),
                              why_report(res, url, selector, notes))
                    return 0
                raw, notes = take(b, url, root, args.any_url)
                notes = ([note] if note else []) + notes
                data = load(raw)
            except (OSError, RuntimeError, EOFError, ValueError) as e:  # TimeoutError is an OSError
                return _fail(f"not run: {clean(e, 300)}")
            except (KeyError, TypeError, AttributeError) as e:  # an answer without the fields DevTools always sends
                return _fail(f"not run: the browser answered oddly: {type(e).__name__} {clean(e, 200)}")
            finally:
                b.close()
    notes += more + ([f"{data['dropped']} rarer value(s) past {MAX_VALUES} a kind left out"] if data["dropped"] else [])
    if data["page_dropped"]:
        notes.append(f"the page had {data['page_dropped']} more value(s) past {MAX_VALUES * 2} a kind, not counted")
    res = critique(data, tokens)
    res["notes"] = notes
    fmcli.out(args, res, report(res, notes))
    return 1 if res["unnamed"] or res["near"] or res["outliers"] else 0
