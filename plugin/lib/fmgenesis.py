"""fm genesis (T-2078): the Genesis tower's home, research/genesis in the project's state. gen-0 is kept byte for byte and
read-only; the other tower docs (gap map, lineage, exam results, each generation's seed, missions and critiques) are
filed only in the tower's shape; the status lists every generation."""
import os
import re
import sys

import fmcore as c

# not-yet.md: ideas no approach has landed yet, with their blockers (retried each generation, never dropped);
# coverage.md: the capability-area x surface x stage grid every generation fills.
SHAPE = re.compile(r"(gap-map|lineage|catalogue|report|not-yet|coverage)\.md|exam\.jsonl"
                   r"|gen-[1-9][0-9]*/(seed|(mission|critique)-[a-z0-9][a-z0-9-]*)\.md")
GEN = re.compile(r"gen-([1-9][0-9]*)")


def home(p):
    return os.path.join(p.dir, "research", "genesis")


def init(p, data):
    """Save gen-0 as given (bytes) and make it read-only; refuses a second one."""
    path = os.path.join(home(p), "gen-0.md")
    kinds = c.secret_kinds(data.decode("utf-8", "replace"))
    if kinds:  # gen-0 is never redacted, so a secret would sit in it for good
        raise ValueError(f"gen-0 holds what looks like {', '.join(kinds)}; reword that line first (gen-0 is kept verbatim)")
    with c.lock(p.dir):  # the check sits inside the lock: two inits can't both pass it
        if os.path.exists(path):
            raise ValueError(f"gen-0 is already saved ({path}) and is never edited")
        c.write_atomic(path, data)
        os.chmod(path, 0o444)
    return path


def put(p, name, text):
    if not SHAPE.fullmatch(name):
        raise ValueError(f"{name!r} isn't a tower doc: gap-map.md, lineage.md, catalogue.md, report.md, exam.jsonl, "
                         "not-yet.md, coverage.md, or gen-N/seed.md, gen-N/mission-NAME.md, gen-N/critique-NAME.md (N from 1)")
    path = os.path.join(home(p), name)
    with c.lock(p.dir):
        c.write_atomic(path, c.redact(text))
    return path


def status(p):
    d = home(p)
    gens = []
    for name in os.listdir(d) if os.path.isdir(d) else ():
        m, sub = GEN.fullmatch(name), os.path.join(d, name)
        if not (m and os.path.isdir(sub)):
            continue
        files = sorted(os.listdir(sub))
        gens.append({"n": int(m.group(1)), "seed": "seed.md" in files,
                     "missions": [f[8:-3] for f in files if f.startswith("mission-") and f.endswith(".md")],
                     "critiques": [f[9:-3] for f in files if f.startswith("critique-") and f.endswith(".md")]})
    try:
        with open(os.path.join(d, "exam.jsonl"), encoding="utf-8", errors="replace") as f:
            exam = sum(1 for line in f if line.strip())
    except OSError:
        exam = 0
    have = {x: os.path.isfile(os.path.join(d, x))
            for x in ("gen-0.md", "gap-map.md", "lineage.md", "not-yet.md", "coverage.md")}
    return {"dir": d, "gen0": have["gen-0.md"], "gap_map": have["gap-map.md"], "lineage": have["lineage.md"],
            "not_yet": have["not-yet.md"], "coverage": have["coverage.md"],
            "exam_lines": exam, "generations": sorted(gens, key=lambda g: g["n"])}


CAP = re.compile(r"^(\d+)\. \*\*(.+?)\.\*\*\s*(.*)$", re.M)  # gen-0 §2: "1. **Initiative.** what it means"
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(mission-[a-z0-9][a-z0-9-]*)\.md\s*\|([^|]*)\|([^|]*)\|([^|]*)\|", re.M)
TIERED = re.compile(r"(.+?)\s*\((\d)\)\W*$")  # "value ranking (3)." -> tier 3


def _tiered(parts):
    out = []
    for part in (x.strip() for x in parts):
        m = TIERED.match(part)
        if m or part.strip(" ."):
            out.append({"text": m.group(1).strip(), "tier": int(m.group(2))} if m else {"text": part.strip(" ."), "tier": None})
    return out


def _gaps(text):
    """gap-map.md: each '## N. Capability' section's '- Gaps:' bullet (wrapped lines joined), split on ' · '."""
    out = {}
    for sec in re.split(r"^(?=## )", text, flags=re.M):
        m, g = re.match(r"## (\d+)\.", sec), re.search(r"^- Gaps: (.*?)(?=^- |\Z)", sec, re.M | re.S)
        if m and g:
            out[m.group(1)] = _tiered(" ".join(g.group(1).split()).split(" · "))
    return out


def _task(b):
    steps = b.steps()
    cur = next((s.text for s in steps if s.current), "")
    return {"id": b.id, "title": b.title, "status": b.status, "type": b.meta.get("type", ""), "tier": b.meta.get("tier", ""),
            "steps": len(steps), "done": sum(s.done for s in steps), "current": c.plain(cur)}


def export(p, out):
    """The tower as data for a page (genesis.json) plus each doc as a file beside it, home paths shown as ~ and
    secrets redacted, so the run can be followed from the repo or its site."""
    import json
    d, home_dir = home(p), os.path.expanduser("~")
    if not os.path.isfile(os.path.join(d, "gen-0.md")):
        raise ValueError(f"no Genesis tower here ({d}): fm genesis init first, or run from the project that has one")
    def scrub(x):  # every string the page gets: home paths as ~, secrets redacted
        if isinstance(x, str):
            return c.redact(x.replace(home_dir, "~") if len(home_dir) > 1 else x)
        if isinstance(x, list):
            return [scrub(v) for v in x]
        return {k: scrub(v) for k, v in x.items()} if isinstance(x, dict) else x
    docs = {}
    for root, dirs, files in os.walk(d):
        dirs.sort()
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), d).replace(os.sep, "/")
            if rel == "gen-0.md" or (SHAPE.fullmatch(rel) and rel.endswith(".md")):
                with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                    docs[rel] = scrub(fh.read())
    briefs = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    def tasks(text):
        return [_task(briefs[t]) for t in dict.fromkeys(re.findall(r"\bT-\d{4,}\b", text)) if t in briefs]
    gen0 = docs.get("gen-0.md", "")
    sec2 = re.search(r"^## 2\..*?(?=^## |\Z)", gen0, re.M | re.S)
    gens = []
    for g in status(p)["generations"]:
        pre = f"gen-{g['n']}/"
        seed = docs.get(pre + "seed.md", "")
        missions, seen = [], set()
        for n, file, caps, gaps, deps in ROW.findall(seed):
            name = file[8:]
            seen.add(name)
            missions.append({"n": int(n), "name": name, "caps": [int(x) for x in re.findall(r"#(\d+)", caps)],
                             "caps_text": caps.strip(), "gaps": _tiered(gaps.split(";")),
                             "depends": [int(x) for x in re.findall(r"\d+", deps)]})
        missions += [{"n": None, "name": m, "caps": [], "caps_text": "", "gaps": [], "depends": []}
                     for m in g["missions"] if m not in seen]  # a mission doc the seed's table doesn't list
        for m in missions:
            doc = docs.get(f"{pre}mission-{m['name']}.md", "")
            m.update(written=bool(doc), critiqued=m["name"] in g["critiques"], tasks=tasks(doc))
        rules = re.search(r"^## Standing rules.*?\n(.*?)(?=^## |\Z)", seed, re.M | re.S)
        gens.append({"n": g["n"], "seed": g["seed"], "missions": missions, "critiques": g["critiques"],
                     "tasks": tasks(seed),
                     "rules": [" ".join(r.split()) for r in re.split(r"^\d+\. ", rules.group(1), flags=re.M)[1:]]
                     if rules else []})
    exam = []
    try:
        with open(os.path.join(d, "exam.jsonl"), encoding="utf-8", errors="replace") as f:
            for line in f.readlines()[-200:]:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict):
                    exam.append(row)
    except OSError:
        pass
    cov = docs.get("coverage.md", "")
    cells = re.findall(r"^- [^:\n]+ × [^:\n]+:(.*)$", cov, re.M)
    rev = c.run_command(p.root, "git rev-parse --short HEAD", timeout=10)[1].strip()
    data = {"updated": c.now(), "rev": rev, "capabilities": [{"n": int(n), "name": name, "text": t.strip()} for n, name, t in
                                                            CAP.findall(sec2.group(0) if sec2 else "")],
            "gaps": _gaps(docs.get("gap-map.md", "")), "generations": gens, "exam": exam,
            "coverage": {"cells": len(cells), "filled": sum(bool(re.match(r"\s*(F|I|N/A):", x)) for x in cells)},
            "not_yet": len([h for h in re.findall(r"^## (.+)$", docs.get("not-yet.md", ""), re.M) if h.strip() != "Removed"]),
            "docs": docs}
    data = scrub(data)
    for rel, text in data["docs"].items():
        path = os.path.join(out, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        c.write_atomic(path, text)
    path = os.path.join(out, "genesis.json")
    c.write_atomic(path, json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    return {"path": path, "docs": len(docs), "generations": len(gens)}


def _text(s):
    def n(k, xs):
        return f"{len(xs)} {k}{'s' * (len(xs) != 1)}" + (f" ({', '.join(xs)})" if xs else "")
    lines = [f"Genesis — {s['dir']}",
             "gen-0: saved, read-only" if s["gen0"] else "gen-0: none yet (fm genesis init --file F)",
             " · ".join(f"{k}: {'yes' if s[f] else 'none yet'}" for k, f in
                        (("gap map", "gap_map"), ("lineage", "lineage"), ("coverage", "coverage"), ("not-yet", "not_yet")))]
    lines += [f"gen-{g['n']}: {'seed' if g['seed'] else 'no seed'}, {n('mission', g['missions'])}, "
              f"{n('critique', g['critiques'])}" for g in s["generations"]]
    return "\n".join(lines + [f"exam: {s['exam_lines']} results"])


def cmd_genesis(args):
    import fmcli
    p = fmcli.resolve(args)
    action = args.action or "status"
    if action in ("init", "put") and not args.file:
        raise fmcli.UsageError(f"fm genesis {action} needs --file F")
    def read(binary=False):  # --file - reads stdin, so a tower doc never needs a draft file first
        if args.file == "-":
            return sys.stdin.buffer.read() if binary else sys.stdin.read()
        with open(args.file, "rb" if binary else "r", **({} if binary else {"encoding": "utf-8", "errors": "replace"})) as f:
            return f.read()
    try:
        if action == "init":
            path = init(p, read(binary=True))
            c.log_event(p, "genesis_init", data={"path": path}, session=fmcli.session())
            return fmcli.out(args, {"dir": home(p), "path": path}, f"gen-0 saved, read-only: {path}")
        if action == "put":
            if not args.path:
                raise fmcli.UsageError("fm genesis put NAME --file F")
            text = read()
            path, kinds = put(p, args.path, text), c.secret_kinds(text)
            c.log_event(p, "genesis_put", data={"name": args.path}, session=fmcli.session())
            return fmcli.out(args, {"dir": home(p), "path": path, "redacted": kinds},
                             f"Filed: {path}" + (f" (redacted: {', '.join(kinds)})" if kinds else ""))
        if action == "export":
            if not args.path:
                raise fmcli.UsageError("fm genesis export DIR (site/genesis in the Foreman repo)")
            res = export(p, os.path.abspath(args.path))
            return fmcli.out(args, res, f"Exported {res['docs']} docs and {res['generations']} generation(s): {res['path']}")
    except (OSError, ValueError) as e:
        raise fmcli.UsageError(str(e))
    s = status(p)
    return fmcli.out(args, s, _text(s))
