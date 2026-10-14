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
ABSOLUTE = re.compile(r"(?<![\w.-])(?:/home/|/Users/|/root/|~/)")
CLUSTER = ("id", "capability", "mark", "why", "grounding", "value", "effort", "risk")
IDEA = ("n", "title", "type", "value", "effort", "lens")


class Leak(Exception):
    pass


def clean(obj, where=""):
    """obj with every string redacted; Leak names the first field that still holds an absolute path."""
    if isinstance(obj, dict):
        return {k: clean(v, f"{where}.{k}" if where else k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean(v, f"{where}[{i}]") for i, v in enumerate(obj)]
    if isinstance(obj, str):
        obj = c.redact(obj)
        if ABSOLUTE.search(obj):
            raise Leak(where)
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
    if not isinstance(rows, list):
        raise fmcli.UsageError(f"catalogue {name!r} must be a list of clusters")
    return [dict({k: r.get(k) for k in CLUSTER}, ideas=[{k: i.get(k) for k in IDEA} for i in r.get("ideas") or []])
            for r in rows if isinstance(r, dict)]


def embed(data):
    """JSON for a <script> block: no '<' survives, so nothing in it can close the tag or open a comment."""
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


def cmd_page(args):
    import fmcli
    p = fmcli.resolve(args)
    meta = c.read_meta(p)
    if args.url:
        if not re.fullmatch(r"https://claude\.ai/\S+", args.url):
            raise fmcli.UsageError("--url must be the https://claude.ai/... link the Artifact tool returned")
        meta = c.update_meta(p, page_url=args.url)
    catalogue = load_catalogue(p, args.catalogue) if args.catalogue else []
    data = {"eyebrow": f"Foreman · {time.strftime('%Y-%m-%d')} · {p.slug}" + (f" · {args.catalogue}" if args.catalogue else ""),
            "title": f"{p.slug}: now" + (" and the catalogue" if catalogue else ""),
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
    c.write_atomic(path, page)
    url = meta.get("page_url")
    fmcli.out(args, {"path": path, "url": url, "queue": len(data["now"]["queue"]), "clusters": len(catalogue)},
              f"Wrote {path} ({len(data['now']['queue'])} queued, {len(catalogue)} clusters)\n"
              f"Publish (main thread): Artifact file_path {path} capabilities {{\"db\": {{}}, \"user\": {{}}}}"
              + (f" url {url}" if url else "") + "\n"
              "Picks: read with ArtifactData list collection picks (one doc per cluster id: {choice: add|veto|\"\", at}); "
              "after a first publish, record its link with fm page --url URL")
