"""T-0707 (Frontier 07, first slice): one local graph joining code, tasks and commits, with time on every edge that has
one, so a query can be asked as of any moment (and backtested). sqlite in the project's Foreman folder; nothing leaves
the machine. Code edges come from graphify's graph.json when the project has one, else from the name-stem mentions
fm impact uses; test links from fm map; task→file edges from Foreman-Task commit trailers and touched events;
co-change from commits. fm graph blast: what a change reaches. fm graph pack: a task's ranked read-set (personalized
PageRank seeded by its words)."""
import collections
import json
import os
import re
import sqlite3

import fmcore as c

COMMITS = 3000      # newest commits read for co-change and trailers
CO_MAX = 20         # a commit touching more files than this says nothing about which belong together
WORD = re.compile(r"[a-z][a-z0-9]{2,}")
STOP = {"the", "and", "for", "with", "from", "this", "that", "into", "when", "not", "are", "was", "add", "fix", "make",
        "use", "new", "all", "its", "out", "one", "has", "can", "but", "now", "get", "set", "run", "too"}


def _words(text):
    return {w for w in WORD.findall(text.lower()) if w not in STOP}


def _stamp(p):
    import fmmap
    head = c._git(p.root, "rev-parse", "HEAD", timeout=10).strip()
    gj = os.path.join(p.root, "graphify-out", "graph.json")
    try:
        led = os.path.getsize(os.path.join(p.dir, "ledger.jsonl"))
    except OSError:
        led = 0
    return f"{head}:{led}:{os.path.getmtime(gj) if os.path.exists(gj) else 0}:{fmmap.__file__}"


def db(p):
    """The graph, rebuilt when HEAD, the ledger or graphify's graph moved since it was built."""
    con = sqlite3.connect(os.path.join(p.dir, "graph.sqlite"))
    con.execute("CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT)")
    stamp = _stamp(p)
    if (con.execute("SELECT v FROM meta WHERE k='stamp'").fetchone() or [None])[0] != stamp:
        _build(p, con)
        con.execute("INSERT OR REPLACE INTO meta VALUES ('stamp', ?)", (stamp,))
        con.commit()
    return con


def _build(p, con):
    """ponytail: a full rebuild whenever anything moved; incremental (new commits and ledger lines) if it gets slow."""
    import fmmap
    con.executescript("DROP TABLE IF EXISTS edges; DROP TABLE IF EXISTS tasks;"
                      "CREATE TABLE edges (src TEXT, dst TEXT, kind TEXT, t TEXT, w REAL);"
                      "CREATE TABLE tasks (id TEXT PRIMARY KEY, type TEXT, title TEXT, created TEXT)")
    rows = []
    tasks = {b.id: b for b in c.load_briefs(p)}
    con.executemany("INSERT INTO tasks VALUES (?,?,?,?)", [(b.id, b.type, b.title, str(b.meta.get("created") or ""))
                                                          for b in tasks.values()])
    log = c._git(p.root, "log", f"-{COMMITS}", "--no-renames", "--format=%x01%cI%x00%B%x00", "--name-only",
                 timeout=120) or ""
    files = set(c._git(p.root, "ls-files", timeout=60).splitlines())
    for entry in log.split("\x01")[1:]:
        when, body, names = (entry.split("\x00") + ["", ""])[:3]
        when = _utc(when)
        changed = [f for f in names.split("\n") if f.strip() and f in files]
        for tid in set(re.findall(r"(?m)^Foreman-Task:\s*(T-\d+)", body)):
            rows += [(f"task:{tid}", f, "touched", when, 1.0) for f in changed]
        if 2 <= len(changed) <= CO_MAX:
            w = 1.0 / (len(changed) - 1)
            rows += [(a, b, "cochange", when, w) for a in changed for b in changed if a != b]
    for e in c.ledger_tail(p, 50000):
        f = (e.get("data") or {}).get("file") if e.get("event") == "touched" and e.get("task") else None
        if f and f.startswith(p.root.rstrip("/") + "/"):
            rows.append((f"task:{e['task']}", os.path.relpath(f, p.root), "touched", _utc(str(e.get("ts", ""))), 1.0))
    m = fmmap.load(p)
    rows += [(t, s, "tests", None, 0.5) for t, srcs in m["tests"].items() for s in srcs]
    rows += _code_edges(p, files)
    con.executemany("INSERT INTO edges VALUES (?,?,?,?,?)", rows)
    con.execute("CREATE INDEX IF NOT EXISTS e_src ON edges (src)")
    con.execute("CREATE INDEX IF NOT EXISTS e_dst ON edges (dst)")


def _utc(iso):
    """An ISO time as UTC 'YYYY-MM-DDTHH:MM:SSZ' so times compare as strings."""
    import datetime
    try:
        return datetime.datetime.fromisoformat(iso.strip().replace("Z", "+00:00")).astimezone(
            datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return iso.strip()


def _code_edges(p, files):
    """(user, used, 'uses') file pairs: graphify's when it has a graph here, else name-stem mentions."""
    import fmmap
    gj = os.path.join(p.root, "graphify-out", "graph.json")
    if os.path.exists(gj):
        try:
            with open(gj) as f:
                g = json.load(f)
            where = {}
            for n in g.get("nodes") or []:
                sf = str(n.get("source_file") or "")
                rel = os.path.relpath(sf, p.root) if os.path.isabs(sf) else sf
                if rel in files:
                    where[n.get("id")] = rel
            out = {(where[e.get("source")], where[e.get("target")]) for e in (g.get("links") or g.get("edges") or [])
                   if e.get("source") in where and e.get("target") in where
                   and where[e.get("source")] != where[e.get("target")]}
            if out:
                return [(a, b, "uses", None, 1.0) for a, b in sorted(out)]
        except (OSError, ValueError, AttributeError):
            pass
    code = sorted(f for f in files if fmmap._CODE.search(f))[:3000]  # ponytail: O(files × stems) regex scan
    stems = {f: fmmap._name_stem(f) for f in code if not fmmap._TEST.search(f)}
    stems = {f: s for f, s in stems.items() if len(s) >= 4 and s.lower() not in fmmap._COMMON_STEMS}
    if not stems:
        return []
    pat = re.compile(r"\b(" + "|".join(sorted({re.escape(s) for s in stems.values()}, key=len, reverse=True)) + r")\b")
    by_stem = collections.defaultdict(list)
    for f, s in stems.items():
        by_stem[s].append(f)
    out = []
    for f in code:
        try:
            with open(os.path.join(p.root, f), encoding="utf-8", errors="replace") as fh:
                found = set(pat.findall(fh.read(200_000)))
        except OSError:
            continue
        out += [(f, g, "uses", None, 1.0) for s in found for g in by_stem[s] if g != f]
    return out


def _edges(con, as_of, where="", args=()):
    q = f"SELECT src, dst, kind, t, w FROM edges WHERE (t IS NULL OR t <= ?){where}"
    return con.execute(q, (as_of or "9999", *args)).fetchall()


def blast(p, paths, as_of=None):
    con = db(p)
    marks = ",".join("?" * len(paths))
    ins = _edges(con, as_of, f" AND dst IN ({marks})", paths)
    outs = _edges(con, as_of, f" AND src IN ({marks})", paths)
    co = collections.Counter()
    for s, d, k, t, w in outs:
        if k == "cochange" and d not in paths:
            co[d] += w
    titles = {r[0]: (r[1], r[2]) for r in con.execute("SELECT id, type, title FROM tasks")}
    fixes = sorted({s[5:] for s, d, k, t, w in ins if k == "touched" and titles.get(s[5:], ("",))[0] == "FIX"})
    return {"paths": paths,
            "dependents": sorted({s for s, d, k, t, w in ins if k == "uses" and s not in paths}),
            "tests": sorted({s for s, d, k, t, w in ins if k == "tests"}),
            "cochange": [f for f, _ in co.most_common(8)],
            "fixes": [{"id": t, "title": titles[t][1]} for t in fixes]}


def pack(p, text, as_of=None, top=15):
    """Files ranked for a task: personalized PageRank over the graph, restarting at the files whose paths and the past
    tasks whose titles share the text's words."""
    con = db(p)
    words = _words(text)
    nbr = collections.defaultdict(lambda: collections.defaultdict(float))
    for s, d, k, t, w in _edges(con, as_of):
        nbr[s][d] += w
        nbr[d][s] += w
    seeds = collections.Counter()
    for node in list(nbr):
        if not node.startswith("task:"):
            seeds[node] += len(words & _words(node.replace("/", " ").replace("_", " ").replace(".", " ")))
    for tid, title, created in con.execute("SELECT id, title, created FROM tasks"):
        if (not as_of or created < as_of) and f"task:{tid}" in nbr:
            seeds[f"task:{tid}"] += len(words & _words(title))
    seeds = {k: v for k, v in seeds.items() if v}
    if not seeds:
        return []
    total = sum(seeds.values())
    restart = {k: v / total for k, v in seeds.items()}
    rank = dict(restart)
    for _ in range(25):  # power iteration, restart probability 0.25
        nxt = collections.defaultdict(float, {k: 0.25 * v for k, v in restart.items()})
        for u, r in rank.items():
            out = nbr[u]
            tw = sum(out.values())
            for v, w in out.items():
                nxt[v] += 0.75 * r * w / tw
        rank = nxt
    files = [(f, s) for f, s in rank.items() if not f.startswith("task:") and os.path.exists(os.path.join(p.root, f))]
    return sorted(files, key=lambda x: -x[1])[:top]


def cmd_graph(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "build":
        con = db(p)
        n = con.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        return fmcli.out(args, {"edges": n}, f"Graph: {n} edges (code, tests, tasks, co-change).")
    if not args.words:
        raise fmcli.UsageError("fm graph blast PATH… | pack \"<task text>\" [--as-of ISO time]")
    as_of = _utc(args.as_of) if args.as_of else None
    if args.action == "blast":
        paths = [os.path.relpath(os.path.abspath(w), p.root) if os.path.exists(w) else w for w in args.words]
        b = blast(p, paths, as_of)
        text = (f"Blast radius of {', '.join(paths)}" + (f" as of {as_of}" if as_of else "") + ":\n"
                f"  dependents: {', '.join(b['dependents'][:15]) or 'none'}\n"
                f"  tests: {', '.join(b['tests'][:15]) or 'none linked'}\n"
                f"  co-change: {', '.join(b['cochange']) or 'none'}\n"
                f"  fixes that touched it: " + (", ".join(f"{x['id']} {c.fit(x['title'], 50)}" for x in b["fixes"][-6:])
                                                or "none"))
        return fmcli.out(args, b, text)
    files = pack(p, " ".join(args.words), as_of, args.top)
    return fmcli.out(args, {"files": [{"path": f, "score": round(s, 4)} for f, s in files]},
                     ("Read first (personalized PageRank from the words, past tasks and the code graph):\n"
                      + "\n".join(f"  {i}. {f}" for i, (f, _) in enumerate(files, 1))) if files else
                     "Nothing in the graph shares those words.")
