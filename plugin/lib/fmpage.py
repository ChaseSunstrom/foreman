"""fm page (T-0786): what's on now (active task and step, queue, inbox and blocked counts, last closes) and, with
--catalogue NAME, a research catalogue's clusters with a Build/Veto pick each, as one self-contained HTML file for a
claude.ai Artifact (private, phone-reachable; picks live in its db collection "picks"). Only ids, titles, tiers, marks
and counts go in; every string is redacted and the write is refused while any still holds an absolute path. fm page
never publishes: it prints the Artifact line for the main thread. T-1649: fm page looks writes the looks gallery
instead, one living specimen per look card (looks.html)."""
import html
import json
import os
import re
import time

import fmcore as c

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "page.html")
LOOKS_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "looks.html")
# T-1649: a look card's type class → faces already on the device (the gallery loads no web font); longest name first
FACES = {
    "condensed grotesk": '"Barlow Condensed", "Roboto Condensed", "Avenir Next Condensed", "Arial Narrow", '
                         '"Nimbus Sans Narrow", "Liberation Sans Narrow", sans-serif',
    "transitional serif": 'Charter, "Bitstream Charter", "Sitka Text", Cambria, "Source Serif 4", "Noto Serif", '
                          'Georgia, serif',
    "old-style serif": '"Iowan Old Style", "Palatino Linotype", Palatino, "URW Palladio L", P052, "EB Garamond", '
                       'Garamond, serif',
    "geometric sans": 'Futura, "Century Gothic", Avenir, "URW Gothic", Jost, Montserrat, Corbel, sans-serif',
    "humanist sans": 'Seravek, "Gill Sans Nova", "Source Sans 3", "Fira Sans", Ubuntu, Calibri, "Noto Sans", '
                     'sans-serif',
    "neo-grotesk": 'Inter, "Adwaita Sans", Roboto, "Helvetica Neue", "Arial Nova", "Nimbus Sans", Arial, sans-serif',
    "grotesk": 'Archivo, "Schibsted Grotesk", "Libre Franklin", "Franklin Gothic Medium", "Helvetica Neue", Arial, '
               'sans-serif',
    "slab": 'Rockwell, "Rockwell Nova", "Roboto Slab", "Zilla Slab", "Sitka Small", "DejaVu Serif", serif',
    "mono": 'ui-monospace, "SF Mono", "Cascadia Code", "Source Code Pro", Menlo, Consolas, "Adwaita Mono", monospace',
}
FACE = re.compile(r"(?i)(?<![\w-])(" + "|".join(map(re.escape, FACES)) + r")(?![\w-])")
ROLE = re.compile(r"(?m)^\|\s*`(--[a-z][a-z-]*)`\s*\|\s*(#[0-9A-Fa-f]{6})\s*\|")
PLATE = re.compile(r"<!--look (look-[a-z0-9-]+)-->\n?(.*?)<!--/look-->\n?", re.S)
ABSOLUTE = re.compile(r"(?<![\w.-])(?:/home/|/Users/|/root/)")  # a bare ~/ names no user (review of T-0786)
CLUSTER = ("id", "capability", "mark", "why", "grounding", "value", "effort", "risk")
IDEA = ("n", "title", "type", "value", "effort", "lens")


class Leak(Exception):
    pass


def _private():
    """Review of T-0786: the user's home in any spelling a path takes (/var/home/x, -home-x- in an encoded folder
    name), not only the three prefixes. T-0821: plus the bare username as a /, \\ or - delimited word, which clean()
    replaces with 'user' rather than refusing (a repo named after the user isn't a path)."""
    import getpass
    home, user = os.path.expanduser("~").rstrip("/"), getpass.getuser()
    parts = [re.escape(home), re.escape(home.replace("/", "-")) + "(?![^/\\\\-])"] if home not in ("", "/") else []
    word = rf"(?:^|(?<=[/\\-])){re.escape(user)}(?=[/\\-]|$)" if user and len(user) >= 2 else None
    return (re.compile("|".join(parts), re.I) if parts else None), (re.compile(word, re.I) if word else None)


def clean(obj, where=""):
    """obj with every string redacted; Leak names the first field that still holds an absolute path."""
    if isinstance(obj, dict):
        return {k: clean(v, f"{where}.{k}" if where else k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean(v, f"{where}[{i}]") for i, v in enumerate(obj)]
    if isinstance(obj, str):
        obj = c.redact(obj)
        home, user = _private()
        if ABSOLUTE.search(obj) or re.search(r"(?i)\b[a-z]:\\users\\", obj) or home and home.search(obj):
            raise Leak(where)
        obj = user.sub("user", obj) if user else obj
    return obj


def now_data(p):
    briefs = c.load_briefs(p)
    sd = c.state_dict(p, briefs)
    a = sd["active"]
    closed = sorted((b for b in c.lane_view(briefs, p.lane) if b.status == "done"),
                    key=lambda b: str(b.meta.get("updated") or ""), reverse=True)[:5]
    return {"active": a and {"id": a["id"], "title": a["title"], "type": a["type"], "tier": a["tier"],
                             "step": a["step"] and {"n": a["step"]["n"], "of": a["step"]["of"]}},
            "queue": [{k: q[k] for k in ("id", "type", "tier", "title")} for q in sd["queue"]],
            "inbox": len(sd["inbox"]), "blocked": len(sd["blocked"]),
            "closed": [{"id": b.id, "type": b.type, "title": b.title} for b in closed]}


def load_catalogue(p, name):
    import fmcli
    if name.endswith(".json") and os.path.lexists(name):  # a catalogue file anywhere (the brainstorm's scratch copy)
        if os.path.islink(name) or not os.path.isfile(name):
            raise fmcli.UsageError(f"{name} must be a plain file, not a link")
        with open(name, encoding="utf-8") as f:
            return _clusters(fmcli, name, json.load(f))
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", name):
        raise fmcli.UsageError(f"catalogue name must be a plain file name, got {name!r}")
    folder = os.path.join(p.dir, "research")
    for path in (os.path.join(folder, name + ".json"), os.path.join(folder, name, "catalogue.json")):
        if os.path.isfile(path) and not os.path.islink(path):
            with open(path, encoding="utf-8") as f:
                rows = json.load(f)
            break
    else:
        raise fmcli.UsageError(f"no catalogue {name!r}: save it as research/{name}.json or research/{name}/catalogue.json")
    return _clusters(fmcli, name, rows)


def _clusters(fmcli, name, rows):
    if not isinstance(rows, list):
        raise fmcli.UsageError(f"catalogue {name!r} must be a list of clusters")
    rows = [r for r in rows if isinstance(r, dict) and r.get("id") is not None]  # T-0821: no id, no pick: skipped
    bad = [r["id"] for r in rows if not re.fullmatch(r"[\w-]{1,100}", str(r["id"]))]
    if bad:  # the page keeps picks at db doc picks/<id>: a slash would reach elsewhere in the store
        raise fmcli.UsageError(f"catalogue {name!r}: cluster id {bad[0]!r} must be letters, digits, _ or -")
    ideas = lambda r: [i for i in r.get("ideas") if isinstance(i, dict)] if isinstance(r.get("ideas"), list) else []
    return [dict({k: r.get(k) for k in CLUSTER}, ideas=[{k: i.get(k) for k in IDEA} for i in ideas(r)]) for r in rows]


def embed(data):
    """JSON for a <script> block: no '<' survives, so nothing in it can close the tag or open a comment."""
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


def save_picks(p, args, catalogue):
    """T-0962: the Build/Veto picks read back from the Artifact ({cluster id: add|veto}) into state picks.json, every
    id checked against the catalogue the page showed."""
    import sys
    import fmcli
    if not args.catalogue:
        raise fmcli.UsageError("--picks needs --catalogue NAME: the cluster ids it checks against")
    try:
        if args.picks == "-":
            picks = json.load(sys.stdin)
        else:
            with open(args.picks, encoding="utf-8") as f:
                picks = json.load(f)
    except (OSError, ValueError) as e:
        raise fmcli.UsageError(f"--picks: can't read {args.picks}: {e}")
    if not isinstance(picks, dict):
        raise fmcli.UsageError('--picks must be a JSON object {"cluster-id": "add" | "veto"}')
    known = {str(r["id"]) for r in catalogue}
    unknown = sorted(k for k in picks if k not in known)
    if unknown:
        raise fmcli.UsageError(f"--picks: unknown cluster id(s) {', '.join(map(repr, unknown))}; "
                               f"{args.catalogue} has {', '.join(sorted(known)) or 'none'}")
    bad = sorted(k for k, v in picks.items() if v not in ("add", "veto"))
    if bad:
        raise fmcli.UsageError(f"--picks: each choice must be add or veto, not {picks[bad[0]]!r} ({bad[0]})")
    name = os.path.basename(args.catalogue).removesuffix(".json")
    path = os.path.join(p.dir, "picks.json")
    c.write_atomic(path, json.dumps({"catalogue": name, "at": c.now(), "picks": picks}, indent=1) + "\n")
    by = {ch: sorted(k for k, v in picks.items() if v == ch) for ch in ("add", "veto")}
    return fmcli.out(args, {"path": path, "catalogue": name, **by},
                     f"Picks for {name}: {len(by['add'])} add ({', '.join(by['add']) or '-'}), "
                     f"{len(by['veto'])} veto ({', '.join(by['veto']) or '-'}); saved to {path}")


def look_cards(folder=None):
    """T-1649: [{name, title, line, roles {--role: #HEX}, faces [type class…], motion, texture}] for each look card,
    the set fmtaste.looks finds (the one rule for what a look card is)."""
    import fmtaste
    folder = folder or fmtaste.LOOKS
    out = []
    for name, look in fmtaste.looks(folder).items():
        part = lambda h: fmtaste.section(look["body"], h)
        faces = list(dict.fromkeys(m.group(1).lower() for m in FACE.finditer(part("Type"))))
        out.append({"name": re.sub(r"[^a-z0-9-]", "-", name.lower()), "title": look["title"], "line": look["line"],
                    "roles": dict(ROLE.findall(part("Palette"))), "faces": faces or ["neo-grotesk"],
                    "motion": part("Motion"), "texture": part("Texture")})
    return out


def _prose(text):
    """A card's first sentence as HTML: escaped, `code` spans kept."""
    first = re.split(r"(?<=\.)\s", " ".join(text.split()), 1)[0]
    return re.sub(r"`([^`<]+)`", r"<code>\1</code>", html.escape(first))


def looks_html(cards):
    """T-1649: the gallery, one section per card: its own plate from looks.html's <!--look NAME--> block (a plain
    palette-and-type plate when it has none), wearing the card's palette roles and type pair."""
    with open(LOOKS_TEMPLATE, encoding="utf-8") as f:
        page = f.read()
    plates = dict(PLATE.findall(page))
    styles, index, sections = [], [], []
    for i, x in enumerate(cards, 1):
        n, esc, faces = x["name"], html.escape(x["title"]), x["faces"] + x["faces"][:1]
        styles.append(f"#{n} {{ " + "; ".join([f"{k}: {v}" for k, v in x["roles"].items()]
                                              + [f"--f1: {FACES[faces[0]]}", f"--f2: {FACES[faces[1]]}"]) + " }")
        dots = f'--s: {x["roles"].get("--surface", "Canvas")}; --a: {x["roles"].get("--accent", "CanvasText")}'
        index.append(f'<li><a href="#{n}"><span class="dots" style="{dots}" aria-hidden="true"></span>{esc}</a></li>')
        type_ = " + ".join(f'<span class="face" style="font-family: var(--f{j})">{html.escape(f)}</span>'
                           for j, f in enumerate([faces[0].capitalize()] + x["faces"][1:2], 1))
        swatches = "".join(f'<li><span class="chip" style="background: {v}"></span><code>{k[2:]}</code> '
                           f'<code>{v}</code></li>' for k, v in x["roles"].items())
        plate = (f'<div class="plate" data-plate="own">{plates[n]}</div>' if n in plates else
                 f'<div class="plate" data-plate="fallback"><p class="plain-a">Aa</p>'
                 f'<p class="plain-b">{html.escape(x["line"])}</p></div>')
        sections.append(
            f'<section class="specimen" id="{n}" aria-labelledby="{n}-h">\n<div class="caption">'
            f'<p class="no">{i:02d}</p><h2 id="{n}-h">{esc}</h2><p class="line">{html.escape(x["line"])}</p>'
            f'<dl><dt>Type</dt><dd>{type_}</dd>'
            f'<dt>Motion</dt><dd>{_prose(x["motion"])}</dd><dt>Texture</dt><dd>{_prose(x["texture"])}</dd></dl>'
            f'<button type="button" class="replay" data-replay>Replay motion</button></div>\n'
            f'{plate}\n<ul class="swatches" aria-label="{esc} palette">{swatches}</ul>\n</section>')
    fill = {"STYLES": "\n".join(styles), "INDEX": "\n".join(index), "SPECIMENS": "\n".join(sections),
            "COUNT": str(len(cards))}
    return re.sub(r"__([A-Z]+)__", lambda m: fill.get(m.group(1), m.group(0)), PLATE.sub("", page))


def _out(args, default, mark):
    """Where the page goes. Review of T-1649: an --out that already exists is replaced only when it holds mark, the
    template's own opening comment, so the user's own page is never overwritten (the default path is Foreman's)."""
    import fmcli
    path = os.path.abspath(args.out) if args.out else default
    if not path.endswith(".html") or os.path.islink(path):  # review: --out never overwrites another kind of file
        raise fmcli.UsageError(f"--out must be a .html file that isn't a link: {path}")
    if args.out and os.path.lexists(path):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                ours = mark in f.read(4096)
        except OSError:
            ours = False
        if not ours:
            raise fmcli.UsageError(f"--out {path} already exists and isn't one fm page wrote; pick a new file or "
                                   "move that one")
    return path


def looks_page(p, args):
    import fmcli
    if args.catalogue or args.picks or args.url:
        raise fmcli.UsageError("fm page looks takes only --out: the gallery shows the look cards, not a catalogue")
    cards = look_cards()
    path = _out(args, os.path.join(p.dir, "looks.html"), "/* fm page looks (T-1649):")
    c.write_atomic(path, looks_html(cards))
    return fmcli.out(args, {"path": path, "looks": len(cards)},
                     f"Wrote {path}: {len(cards)} looks, one living specimen each; it loads nothing from another host")


def cmd_page(args):
    import fmcli
    p = fmcli.resolve(args)
    if getattr(args, "what", None) == "looks":
        return looks_page(p, args)
    meta = c.read_meta(p)
    if args.url:
        if not re.fullmatch(r"https://claude\.ai/(?:code/)?artifact/[\w-]{6,80}", args.url):
            raise fmcli.UsageError("--url must be the https://claude.ai/... link the Artifact tool returned")
        meta = c.update_meta(p, page_url=args.url)
    catalogue = load_catalogue(p, args.catalogue) if args.catalogue else []
    if getattr(args, "picks", None):
        return save_picks(p, args, catalogue)
    data = {"eyebrow": f"Foreman · {time.strftime('%Y-%m-%d')} · {p.slug}" + (f" · {os.path.basename(args.catalogue).removesuffix('.json')}" if args.catalogue else ""),
            "title": f"{os.path.basename(p.root.rstrip('/')).replace('-', ' ').title()} Board",  # a name, stable
            "lede": "What Foreman is working on, what waits, and what just closed.",
            "now": now_data(p), "catalogue": catalogue}
    try:
        data = clean(data)
    except Leak as e:
        raise fmcli.UsageError(f"refused: {e} still holds an absolute path after redaction; fix that text "
                               "(repo-relative paths are fine) and run fm page again")
    with open(TEMPLATE, encoding="utf-8") as f:
        page = f.read()
    page = page.replace("__TITLE__", html.escape(data["title"])).replace("__DATA__", embed(data))
    path = _out(args, os.path.join(p.dir, "page.html"), "/* fm page (T-0786):")
    c.write_atomic(path, page)
    url = meta.get("page_url")
    publish = ("Publish: refused here, this repo is marked sensitive (the Artifact tool is denied); fm sensitive off "
               "if the user wants it shared" if meta.get("sensitive") else  # T-0821: the outward gate's rule
               f"Publish (main thread): Artifact file_path {path} capabilities {{\"db\": {{}}, \"user\": {{}}}}"
               + (f" url {url}" if url else "") + "\n"
               "Picks: read with ArtifactData list collection picks (one doc per cluster id: {choice: add|veto|\"\", "
               "at}); after a first publish, record its link with fm page --url URL")
    fmcli.out(args, {"path": path, "url": url, "queue": len(data["now"]["queue"]), "clusters": len(catalogue),
                     "sensitive": bool(meta.get("sensitive"))},
              f"Wrote {path} ({len(data['now']['queue'])} queued, {len(catalogue)} clusters)\n" + publish)
