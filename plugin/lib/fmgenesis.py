"""fm genesis (T-2078): the Genesis tower's home, research/genesis in the project's state. gen-0 is kept byte for byte and
read-only; the other tower docs (gap map, lineage, exam results, each generation's seed, missions and critiques) are
filed only in the tower's shape; the status lists every generation."""
import json
import os
import re
import time
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


def status(p, with_check=True):
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
            rows = [line for line in f if line.strip()]
    except OSError:
        rows = []
    exam, last = len(rows), None
    try:
        last = json.loads(rows[-1]) if rows else None
    except ValueError:
        pass
    have = {x: os.path.isfile(os.path.join(d, x))
            for x in ("gen-0.md", "gap-map.md", "lineage.md", "not-yet.md", "coverage.md")}
    out = {"dir": d, "gen0": have["gen-0.md"], "gap_map": have["gap-map.md"], "lineage": have["lineage.md"],
            "not_yet": have["not-yet.md"], "coverage": have["coverage.md"],
            "exam_lines": exam, "exam_last": last if isinstance(last, dict) else None, "generations": sorted(gens, key=lambda g: g["n"]),
            "live": c.read_meta(p).get("genesis_live") or False}
    if with_check and have["gen-0.md"]:
        out["check"] = check(p)
    return out


CAP = re.compile(r"^(\d+)\. \*\*(.+?)\.\*\*\s*(.*)$", re.M)  # gen-0 §2: "1. **Initiative.** what it means"
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(mission-[a-z0-9][a-z0-9-]*)\.md\s*\|([^|]*)\|([^|]*)\|([^|]*)\|", re.M)
TIERED = re.compile(r"(.+?)\s*\((\d)\)\W*$")  # "value ranking (3)." -> tier 3

# Standing rule 2 (gen-1 seed): coverage.md is one '## <area>' per row and one '- <stage> × <surface>: F|I|N/A: …' line
# per cell; F names an existing path, I an idea plus the existing (file) it builds on, N/A its reason.
STAGES = ("find", "understand", "plan", "build", "verify", "ship", "operate", "learn")
SURFACES = ("Claude Code", "fm code", "other agents", "MCP", "Desktop", "site", "CLI", "headless/server")
CELL = re.compile(r"- (.+?) × (.+?):\s*(F|I|N/A):\s*(.*)")
NOT_YET = re.compile(r"^- (blocker|tried|unblocks-with|retried|added):[ \t]*(.*?)[ \t]*$", re.M)


def _doc(d, name):
    try:
        with open(os.path.join(d, name), encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def _sections(text):
    """[(heading, body)] for each '## ' section."""
    return [(s[3:].partition("\n")[0].strip(), s.partition("\n")[2]) for s in re.split(r"^(?=## )", text, flags=re.M)
            if s.startswith("## ")]


def _caps(gen0):
    sec2 = re.search(r"^## 2\..*?(?=^## |\Z)", gen0 or "", re.M | re.S)
    return CAP.findall(sec2.group(0) if sec2 else "")


def _cell(root, kind, rest):
    """What's wrong with one filled cell, or ''."""
    if kind == "N/A":
        return "" if re.search(r"\w", rest) else "N/A needs its reason"
    if kind == "I":
        m = re.search(r"\(([^()\s]+)\)\s*\W*$", rest)
        if not m:
            return "an I cell names the file it builds on: I: <idea> (<file>)"
        path = m.group(1)
    else:
        path = (rest.split() or [""])[0].strip("`").rstrip(",;.")
        if not path:
            return "F needs the feature's path"
    path = re.sub(r":\d+$", "", path)
    full = os.path.realpath(os.path.join(root, path))
    if not (full == root or full.startswith(root.rstrip("/") + "/")):
        return f"{path} is outside the project"
    return "" if os.path.exists(full) else f"{path} doesn't exist"


def coverage(p, text, gen0=""):
    """Standing rule 2: every area row has all stage × surface cells, each grounded; gen-0 §2's capabilities each have
    a row. Returns areas, cells (expected), filled (valid), empty (missing) and problems."""
    if text is None:
        return {"areas": 0, "cells": 0, "filled": 0, "empty": 0,
                "problems": ["coverage.md doesn't exist (every generation fills the grid: fm genesis put coverage.md)"]}
    root, probs, filled, empty = os.path.realpath(p.root), [], 0, 0
    secs = [(a, b) for a, b in _sections(text) if a]
    if not secs:
        probs.append("coverage.md has no '## <area>' rows")
    for area, body in secs:
        seen = set()
        for line in (x.strip() for x in body.splitlines()):
            if not line.startswith("- "):
                continue
            m = CELL.fullmatch(line)
            if not m:
                probs.append(f"{area}: not a cell line: {c.plain(line)[:80]}")
                continue
            stage, kind, rest = m.group(1).strip().lower(), m.group(3), m.group(4)
            surface = next((s for s in SURFACES if s.lower() == m.group(2).strip().lower()), None)
            if stage not in STAGES or not surface:
                probs.append(f"{area}: {c.plain(m.group(1).strip())} × {c.plain(m.group(2).strip())} isn't a stage × "
                             "surface of the grid")
                continue
            if (stage, surface) in seen:
                probs.append(f"{area}: {stage} × {surface} appears twice")
                continue
            seen.add((stage, surface))
            bad = _cell(root, kind, rest.strip())
            if bad:
                probs.append(f"{area}: {stage} × {surface}: {c.plain(bad)}")
            else:
                filled += 1
        gone = [f"{s} × {f}" for s in STAGES for f in SURFACES if (s, f) not in seen]
        empty += len(gone)
        probs += [f"{area}: {g}: empty" for g in gone]
    heads = " | ".join(a.lower() for a, _ in secs)
    probs += [f"no row for capability {n}. {name}" for n, name, _ in _caps(gen0) if name.lower() not in heads]
    return {"areas": len(secs), "cells": len(secs) * len(STAGES) * len(SURFACES), "filled": filled, "empty": empty,
            "problems": probs}


def not_yet(text, gen):
    """Standing rule 1: each open item has a blocker, 2+ different tried approaches (split on ';'), what unblocks it,
    and a try in the current generation (added or retried there); removals are only for proven harm or a duplicate."""
    probs, items, open_ = [], 0, 0
    for head, body in _sections(text or ""):
        if head.lower() == "removed":
            for line in re.findall(r"^- (.+)$", body, re.M):
                if not re.search(r"\b(harm|duplicate)", line, re.I):
                    probs.append(f"{c.plain(line.partition(':')[0])[:60]}: removed only for proven harm or an exact duplicate")
            continue
        items += 1
        f = {}
        for k, v in NOT_YET.findall(body):
            f.setdefault(k, []).append(v)
        mine = []
        if not any(f.get("blocker", [])):
            mine.append("no blocker")
        tries = {t.strip().lower() for t in ";".join(f.get("tried", [])).split(";")} - {""}
        if len(tries) < 2:
            mine.append(f"tried {len(tries)} approach{'es' if len(tries) != 1 else ''}; 2 different ones first")
        if not any(f.get("unblocks-with", [])):
            mine.append("no unblocks-with")
        if gen and not any(re.match(rf"gen-{gen}\b", v) for v in f.get("retried", []) + f.get("added", [])):
            mine.append(f"not retried in gen-{gen}")
        if mine:
            open_ += 1
            probs += [f"{c.plain(head)[:60]}: {m}" for m in mine]
    return {"items": items, "open": open_, "problems": probs}


def check(p):
    """Standing rules 1-3 over the tower: the coverage grid and the not-yet ledger, against the newest generation."""
    d, s = home(p), status(p, with_check=False)
    gens = [g["n"] for g in s["generations"] if g["seed"]]
    return {"gen": max(gens) if gens else None, "coverage": coverage(p, _doc(d, "coverage.md"), _doc(d, "gen-0.md") or ""),
            "not_yet": not_yet(_doc(d, "not-yet.md"), max(gens) if gens else None)}


def _check_lines(r, limit=6):
    cov, ny, out = r["coverage"], r["not_yet"], []
    if cov["problems"]:
        more = len(cov["problems"]) - limit
        out.append(f"✗ coverage: {cov['empty']} empty, {len(cov['problems']) - cov['empty']} other problem(s); "
                   f"{cov['filled']} of {cov['cells']} cells filled")
        out += [f"    {x}" for x in cov["problems"][:limit]] + ([f"    … {more} more (--json lists all)"] if more > 0 else [])
    else:
        out.append(f"✓ coverage: {cov['areas']} areas, {cov['filled']} of {cov['cells']} cells filled")
    n, more = ny["items"], len(ny["problems"]) - limit
    if ny["problems"]:
        out.append(f"✗ not-yet: {ny['open']} of {n} item{'s' if n != 1 else ''} need work")
        out += [f"    {x}" for x in ny["problems"][:limit]] + ([f"    … {more} more (--json lists all)"] if more > 0 else [])
    else:
        out.append(f"✓ not-yet: {n} item{'s' if n != 1 else ''}" + (f", each tried twice and retried in gen-{r['gen']}"
                                                                   if n and r["gen"] else ""))
    return out


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
    gens = []
    for g in status(p, with_check=False)["generations"]:
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
    chk = check(p)
    chk["coverage"]["problems"] = chk["coverage"]["problems"][:50]
    rev = c.run_command(p.root, "git rev-parse --short HEAD", timeout=10)[1].strip()
    data = {"updated": c.now(), "rev": rev,
            "capabilities": [{"n": int(n), "name": name, "text": t.strip()} for n, name, t in _caps(gen0)],
            "gaps": _gaps(docs.get("gap-map.md", "")), "generations": gens, "exam": exam,
            "coverage": chk["coverage"], "not_yet": chk["not_yet"]["items"], "not_yet_open": chk["not_yet"]["open"],
            "docs": docs}
    data = scrub(data)
    for rel, text in data["docs"].items():
        path = os.path.join(out, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        c.write_atomic(path, text)
    path = os.path.join(out, "genesis.json")
    c.write_atomic(path, json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    return {"path": path, "docs": len(docs), "generations": len(gens)}


LIVE_EVERY = 300  # seconds between auto publishes; a change inside the window goes out when it ends
STAMP = "genesis-publish.last"  # mtime: the last publish that reached the network
PENDING = "genesis-publish.pending"  # a detached publish waits out the window; one at a time
REF = "refs/foreman/genesis-main"  # main fetched here, never FETCH_HEAD, which any other fetch rewrites


def live(p, on, tid=None):
    """T-2090: switch auto publishing on, spending one publish grant (the active task's, or tid's), or off."""
    if not on:
        c.update_meta(p, genesis_live=None)
        return None
    cur = c.read_meta(p).get("genesis_live")
    if cur:
        return cur  # already on: no second grant spent
    import fmrelease
    b = fmrelease._named_grant(p, tid) if tid else fmrelease._grant(p)
    if not b:
        raise ValueError("fm genesis live on needs a publish grant: fm task set ID --allow publish on the active task, "
                         "or name it with --task ID")
    try:  # before the grant is spent: nowhere to publish keeps it
        fmrelease._git(p.root, "ls-remote", "--exit-code", "origin", "refs/heads/main")
    except Exception as e:
        raise ValueError(f"no origin main to publish to ({c.fit(c.redact(c.plain(str(e))), 160)}); the grant is kept") from None
    fmrelease._spend(p, b.id, "fm genesis live on")
    state = {"remote": "origin", "since": c.now(), "task": b.id}
    c.update_meta(p, genesis_live=state)
    return state


def kick(p):
    """Schedule one detached fm genesis publish --settle while live is on: it waits out the rest of the LIVE_EVERY
    window, then publishes whatever changed by then. True when scheduled; False when off or one already waits."""
    if not c.read_meta(p).get("genesis_live"):
        return False
    pending = os.path.join(p.dir, PENDING)
    try:
        if time.time() - os.path.getmtime(pending) < LIVE_EVERY + 600:
            return False  # older than any wait: a dead waiter's leftover
    except OSError:
        pass
    try:
        open(pending, "w").close()
    except OSError:
        return False  # no marker, no spawn: never one per call
    if not os.environ.get("FOREMAN_NO_BACKGROUND"):  # tests: publish() is run directly
        import subprocess
        try:
            subprocess.Popen([os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "genesis", "publish", "--settle"], cwd=p.root,
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        except OSError:
            pass
    return True


def _wait(p):
    """Seconds left in the window since the last publish reached the network."""
    try:
        return max(0.0, LIVE_EVERY - (time.time() - os.path.getmtime(os.path.join(p.dir, STAMP))))
    except OSError:
        return 0.0


def _body(path):
    import json
    with open(path, encoding="utf-8") as f:
        return {k: v for k, v in json.load(f).items() if k not in ("updated", "rev")}  # these change every export


def _record(p, result, digest=None, sha=None):
    with c.lock(p.dir):
        meta = c.read_meta(p)
        lv = meta.get("genesis_live")
        if lv:  # switched off meanwhile: stays off
            lv["last"] = {"at": c.now(), "result": result}
            if digest:
                lv["hash"] = digest
            if sha:
                lv["pushed"] = {"at": c.now(), "sha": sha}
            c.write_meta(p, meta)
    return {"result": result, **({"sha": sha} if sha else {})}


def publish(p, settle=False):
    """Push the tower's export to the remote's main as one data-only commit (site/genesis only), from a scratch
    worktree at the fetched main, when it differs from what main has (the per-export updated/rev fields aside).
    One run at a time; an unchanged tower costs one export and no network. settle: the detached form kick starts,
    which first waits out the window, then frees the next kick, so a change from then on schedules its own."""
    import hashlib
    import json
    import shutil
    import tempfile
    import fmrelease
    if settle:
        time.sleep(_wait(p))
        try:
            os.remove(os.path.join(p.dir, PENDING))
        except OSError:
            pass
    lv = c.read_meta(p).get("genesis_live")
    if not lv:
        raise ValueError("live publishing is off: fm genesis live on (spends one publish grant)")
    if c.gates_live(p, key="ship_testing"):
        return _record(p, "waiting: fm ship is testing")  # a push now would send it back to the start
    remote, git = lv.get("remote") or "origin", fmrelease._git
    try:
        with c.lock(os.path.join(p.dir, "genesis-publish"), timeout=120 if settle else 0), \
                tempfile.TemporaryDirectory() as tmp:
            out, wt = os.path.join(tmp, "export"), os.path.join(tmp, "main")
            export(p, out)
            new = _body(os.path.join(out, "genesis.json"))
            digest = hashlib.sha256(json.dumps(new, sort_keys=True).encode()).hexdigest()
            if digest == lv.get("hash"):
                return _record(p, "up to date")
            open(os.path.join(p.dir, STAMP), "w").close()
            git(p.root, "fetch", "-q", remote, f"+refs/heads/main:{REF}")
            base = git(p.root, "rev-parse", REF).strip()
            git(p.root, "worktree", "add", "-q", "--detach", wt, base)
            try:
                dest = os.path.join(wt, "site", "genesis")
                try:
                    old = _body(os.path.join(dest, "genesis.json"))
                except (OSError, ValueError):
                    old = None
                if old == new:
                    return _record(p, "up to date", digest)
                shutil.copytree(out, dest, dirs_exist_ok=True)
                git(wt, "add", "--", "site/genesis")
                git(wt, "commit", "-q", "-m", "Genesis: tower update (fm genesis live)")
                sha = git(wt, "rev-parse", "HEAD").strip()
                stray = [f for f in git(wt, "diff", "--name-only", base, sha).splitlines() if not f.startswith("site/genesis/")]
                if stray:
                    raise ValueError(f"refusing to push: the commit touches {stray[:3]} outside site/genesis")
                git(p.root, "push", "-q", remote, f"{sha}:refs/heads/main")
            finally:
                git(p.root, "worktree", "remove", "--force", wt, ok=True)
    except c.LockTimeout:
        return {"result": "already publishing"}
    except Exception as e:  # a moved main, no network: recorded; the next kick tries again
        why = c.fit(c.redact(c.plain(str(e))), 200)
        _record(p, f"failed: {why}")
        raise ValueError(f"genesis publish failed: {why}") from None
    c.log_event(p, "genesis_publish", data={"sha": sha, "remote": remote})
    return _record(p, "pushed", digest, sha)


def _text(s):
    def n(k, xs):
        return f"{len(xs)} {k}{'s' * (len(xs) != 1)}" + (f" ({', '.join(xs)})" if xs else "")
    lines = [f"Genesis — {s['dir']}",
             "gen-0: saved, read-only" if s["gen0"] else "gen-0: none yet (fm genesis init --file F)",
             " · ".join(f"{k}: {'yes' if s[f] else 'none yet'}" for k, f in
                        (("gap map", "gap_map"), ("lineage", "lineage"), ("coverage", "coverage"), ("not-yet", "not_yet")))]
    lines += [f"gen-{g['n']}: {'seed' if g['seed'] else 'no seed'}, {n('mission', g['missions'])}, "
              f"{n('critique', g['critiques'])}" for g in s["generations"]]
    lv = s["live"]
    if lv:
        site = f"site: live → {lv['remote']} main"
        if lv.get("pushed"):
            site += f", last push {lv['pushed']['at']} ({lv['pushed']['sha'][:8]})"
        if lv.get("last"):
            site += f", last check {lv['last']['at']}: {lv['last']['result']}"
    else:
        site = "site: off (fm genesis live on pushes every tower change to the site)"
    exam = f"exam: {s['exam_lines']} results"
    if s.get("exam_last"):
        import fmexam
        exam += f", last: {fmexam.summary(s['exam_last'])}"
    if s.get("check"):
        cov, ny = s["check"]["coverage"], s["check"]["not_yet"]
        lines.append(f"coverage: {cov['filled']} of {cov['cells']} cells filled, {cov['empty']} empty"
                     + (f", {len(cov['problems'])} problem(s)" if cov["problems"] else "")
                     + f" · not-yet: {ny['items']} item(s), {ny['open']} need work"
                     + (" (fm genesis check)" if cov["problems"] or ny["problems"] else ""))
    return "\n".join(lines + [exam, site])


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
            kick(p)
            return fmcli.out(args, {"dir": home(p), "path": path}, f"gen-0 saved, read-only: {path}")
        if action == "put":
            if not args.path:
                raise fmcli.UsageError("fm genesis put NAME --file F")
            text = read()
            path, kinds = put(p, args.path, text), c.secret_kinds(text)
            c.log_event(p, "genesis_put", data={"name": args.path}, session=fmcli.session())
            kick(p)
            return fmcli.out(args, {"dir": home(p), "path": path, "redacted": kinds},
                             f"Filed: {path}" + (f" (redacted: {', '.join(kinds)})" if kinds else ""))
        if action == "live":
            if args.path not in ("on", "off"):
                raise fmcli.UsageError("fm genesis live on|off")
            state = live(p, args.path == "on", args.task)
            c.log_event(p, "genesis_live", data={"on": bool(state)}, session=fmcli.session())
            return fmcli.out(args, {"live": state or False},
                             "Live: every tower change reaches the site within minutes (undo: fm genesis live off)"
                             if state else "Live publishing off.")
        if action == "check":
            r = check(p)
            fmcli.out(args, r, "\n".join(_check_lines(r)))
            return 1 if r["coverage"]["problems"] or r["not_yet"]["problems"] else 0
        if action == "publish":
            res = publish(p, settle=args.settle)
            return fmcli.out(args, res, f"Genesis publish: {res['result']}" + (f" ({res['sha'][:8]})" if "sha" in res else ""))
        if action == "export":
            if not args.path:
                raise fmcli.UsageError("fm genesis export DIR (site/genesis in the Foreman repo)")
            res = export(p, os.path.abspath(args.path))
            return fmcli.out(args, res, f"Exported {res['docs']} docs and {res['generations']} generation(s): {res['path']}")
    except (OSError, ValueError) as e:
        raise fmcli.UsageError(str(e))
    s = status(p)
    return fmcli.out(args, s, _text(s))
