"""fm page (T-0786): what's on now (active task and step, queue, inbox and blocked counts, last closes) and, with
--catalogue NAME, a research catalogue's clusters with a Build/Veto pick each, as one self-contained HTML file for a
claude.ai Artifact (private, phone-reachable; picks live in its db collection "picks"). Only ids, titles, tiers, marks
and counts go in; every string is redacted and the write is refused while any still holds an absolute path. fm page
never publishes: it prints the Artifact line for the main thread."""
import html
import json
import os
import re
import time

import fmcore as c

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "page.html")
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


def cmd_page(args):
    import fmcli
    p = fmcli.resolve(args)
    meta = c.read_meta(p)
    if args.url:
        if not re.fullmatch(r"https://claude\.ai/(?:code/)?artifact/[\w-]{6,80}", args.url):
            raise fmcli.UsageError("--url must be the https://claude.ai/... link the Artifact tool returned")
        meta = c.update_meta(p, page_url=args.url)
    catalogue = load_catalogue(p, args.catalogue) if args.catalogue else []
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
    path = os.path.abspath(args.out) if args.out else os.path.join(p.dir, "page.html")
    if not path.endswith(".html") or os.path.islink(path):  # review: --out never overwrites another kind of file
        raise fmcli.UsageError(f"--out must be a .html file that isn't a link: {path}")
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
