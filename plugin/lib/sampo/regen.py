"""T-2918 (M-02 slice): `sampo moons regen PATH` deletes one module in a throwaway worktree and regrows it on a model from the
module's intent alone: the briefs that name it, its MASTER.md entry, its tests, the names its importers use. Never its
code. The reply is checked before it runs (it compiles, imports nothing the original didn't), written in the worktree,
the module's own tests run and each one's result reported. Nothing lands: the main checkout is never written.
`sampo moons regen --leaves` prints the sample; `--slice` runs it, local model first, Haiku second."""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

from sampo import core as c

MAX_LINES, TRIES, TIMEOUT, CAP = 260, 2, 900, 60_000
SYSTEM = ("You rebuild one Python module from its intent. The module was deleted. You get the task briefs that "
          "changed it, its entry in the project map, its tests and the names its importers use. Reply with the whole "
          "module in one ```python fence and nothing else. Import only what the briefs and tests make necessary; "
          "the standard library and the project's own modules named in the intent are all you may use.")


def leaves(root, links, under=""):
    """Modules under `under` and MAX_LINES with a linked test, `fm*.py` import aliases left out; links is the map's
    tests→sources."""
    mods = sorted({s for srcs in links.values() for s in srcs if s.endswith(".py") and s.startswith(under)})
    out = []
    for s in mods:
        if re.match(r"fm[a-z]", os.path.basename(s)) or "/tests/" in s or s.startswith("tests/"):
            continue
        try:
            with open(os.path.join(root, s), encoding="utf-8") as f:
                n = sum(1 for _ in f)
        except OSError:
            continue
        if n < MAX_LINES:
            out.append(s)
    return out


def imports(source):
    """Every module a source imports, as dotted names (`from a import b` gives a and a.b); __import__ counts as one."""
    tree, got = ast.parse(source), set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            got |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mod = "." * n.level + (n.module or "")
            got |= {mod} | {f"{mod}.{a.name}" for a in n.names}
        elif isinstance(n, ast.Name) and n.id in ("__import__", "importlib"):
            got.add(n.id)
    return got


def check_reply(text, allowed):
    """(code, "") when the reply's python fence compiles and imports nothing outside `allowed`, else (None, why)."""
    m = re.search(r"```(?:python|py)?[ \t]*\n(.*?)```", text or "", re.S)
    if not m:
        return None, "no python code fence in the reply"
    code = m.group(1)
    try:
        compile(code, "<regen>", "exec")
        extra = imports(code) - set(allowed)
    except (SyntaxError, ValueError) as e:
        return None, f"the reply doesn't compile: {e}"
    if extra:
        return None, "the reply imports outside the original's imports: " + ", ".join(sorted(extra))
    return code, ""


def gather_briefs(p, rel):
    """(id, raw request, interpretation, criteria) of every brief whose scope or touched files name rel, archive
    included, read as foresight._requests reads them."""
    touched = {}
    for e in c.ledger_events(p, ("touched",)):
        f = (e.get("data") or {}).get("file")
        if e.get("task") and isinstance(f, str):
            touched.setdefault(e["task"], set()).add(os.path.relpath(f, p.root) if os.path.isabs(f) else f)
    out = []
    for b in c.load_briefs(p, include_archive=True):
        scope = b.meta.get("scope") if isinstance(b.meta.get("scope"), list) else []
        if rel in {str(x) for x in scope} | touched.get(b.id, set()):
            out.append((b.id, b.section("Raw request"), b.section("Interpretation"), b.section("Acceptance criteria")))
    return out


def master_entry(text, rel):
    """The MASTER.md paragraphs that name the module (`sampo/X`, `sampo.X`, `fmX` or its path)."""
    name = os.path.splitext(os.path.basename(rel))[0]
    pat = re.compile(rf"\b{re.escape(rel)}\b|\bsampo[/.]{re.escape(name)}\b|\bfm{re.escape(name)}\b")
    return "\n\n".join(x.strip() for x in re.split(r"\n\s*\n", text or "") if pat.search(x))


def _names(root, rel):
    """The attributes the other modules of the package use from this one."""
    pkg, name = os.path.basename(os.path.dirname(rel)), os.path.splitext(os.path.basename(rel))[0]
    folder, found = os.path.join(root, os.path.dirname(rel)), set()
    for f in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if not f.endswith(".py") or f == os.path.basename(rel):
            continue
        try:
            with open(os.path.join(folder, f), encoding="utf-8") as fh:
                text = fh.read(400_000)
        except OSError:
            continue
        aliases = {name} | set(re.findall(rf"from {pkg} import [^\n]*?\b{name} as (\w+)", text))
        for a in aliases:
            found |= set(re.findall(rf"\b{a}\.([A-Za-z_]\w*)", text)) if re.search(
                rf"from {pkg} import [^\n]*\b{name}\b|import {pkg}\.{name}\b", text) else set()
        for m in re.findall(rf"from {pkg}\.{name} import ([^\n(]+)", text):
            found |= {x.split(" as ")[0].strip() for x in m.split(",") if x.strip()}
    return sorted(found)


def intent(root, rel, briefs, master, links):
    """The prompt: intent only. The module's own code never enters it."""
    parts = [f"Rebuild the module {rel}."]
    for tid, raw, interp, crit in briefs:
        parts.append(f"## Brief {tid}\nRequest: {raw.strip()}\nInterpretation: {interp.strip()}\nCriteria:\n{crit.strip()}")
    if master:
        parts.append("## Its entry in the project map\n" + master)
    names = _names(root, rel)
    if names:
        parts.append("## Names other modules use from it\n" + ", ".join(names))
    for t in sorted(t for t, srcs in links.items() if rel in srcs):
        try:
            with open(os.path.join(root, t), encoding="utf-8") as f:
                parts.append(f"## Its test {t}\n{f.read(40_000)}")
        except OSError:
            continue
    return "\n\n".join(parts)[:CAP]


_RESULT = re.compile(r"^(\w+) \([\w.]+\)(?:\n.*)? \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure)$", re.M)


def run_tests(wt, tests):
    """{test name: passed} over the module's own test files, run in the worktree."""
    res = {}
    for t in tests:
        d, mod = os.path.dirname(os.path.join(wt, t)), os.path.splitext(os.path.basename(t))[0]
        try:
            r = subprocess.run([sys.executable, "-m", "unittest", "-v", mod], cwd=d, capture_output=True, text=True,
                               timeout=300)
            out = r.stderr
        except subprocess.TimeoutExpired:
            res[f"{mod} (timed out)"] = False
            continue
        for name, state in _RESULT.findall(out):
            res[name] = state == "ok" or state.startswith("skipped")
        if r.returncode and not any(not v for v in res.values()):
            res[f"{mod} (did not run)"] = False  # an import error fails the file before any test names itself
    return res


def regen(root, rel, ask, intent_text, links, tries=TRIES):
    """Delete rel in a throwaway worktree of root's HEAD, regrow it with ask(system, prompt)->text, run its tests:
    {module, round_trip, tries, tests, refused}. The throwaway worktree is the only place written."""
    tmp = tempfile.mkdtemp(prefix="fm-regen-")
    wt = os.path.join(tmp, "repo")
    try:
        target = os.path.realpath(os.path.join(wt, rel))
        if os.path.isabs(rel) or not target.startswith(os.path.realpath(wt) + os.sep):
            raise ValueError(f"{rel}: not a path inside the repo")
        r = subprocess.run(["git", "-C", root, "worktree", "add", "--detach", "-q", wt, "HEAD"], capture_output=True,
                           text=True)
        if r.returncode:
            raise OSError(f"git worktree add: {r.stderr.strip()[:200]}")
        try:
            with open(os.path.join(wt, rel), encoding="utf-8") as f:
                allowed = imports(f.read())
        except OSError as e:
            raise ValueError(f"{rel}: can't read it at HEAD: {e}")
        os.remove(os.path.join(wt, rel))
        tests = sorted(t for t, srcs in links.items() if rel in srcs)
        out, prompt = {"module": rel, "round_trip": False, "tries": 0, "tests": {}, "refused": []}, intent_text
        for n in range(1, tries + 1):
            out["tries"] = n
            code, why = check_reply(ask(SYSTEM, prompt), allowed)
            if not code:
                out["refused"].append(why)
                prompt = intent_text + f"\n\n## Your last reply was refused without running\n{why}. Fix that."
                continue
            with open(target, "w", encoding="utf-8") as f:
                f.write(code)
            out["tests"] = run_tests(wt, tests)
            out["round_trip"] = bool(out["tests"]) and all(out["tests"].values())
            if out["round_trip"]:
                break
            bad = ", ".join(k for k, v in out["tests"].items() if not v)
            prompt = intent_text + f"\n\n## Your last reply failed these tests\n{bad}. Fix the module."
        return out
    finally:
        subprocess.run(["git", "-C", root, "worktree", "remove", "--force", wt], capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)
        subprocess.run(["git", "-C", root, "worktree", "prune"], capture_output=True)


def make_ask(p, name, sensitive=False):
    """ask(system, prompt)->text for a profile name ('haiku' goes through the claude CLI child; a sensitive project's
    only on loopback). Tool-less either way."""
    from sampo import ideas, models
    if name == "haiku":
        if sensitive:
            raise ValueError("a sensitive project's code goes to a loopback model only, never Haiku")
        return lambda system, prompt: ideas.run_child("regen", system, prompt, "haiku", TIMEOUT, project=p.slug)
    prof = models.resolve(name)
    host = urllib.parse.urlsplit(prof.get("base_url") or "").hostname or ""
    if sensitive and not models.is_loopback(host):
        raise ValueError(f"a sensitive project asks loopback models only; {name!r} is at {host or 'a cloud endpoint'}")

    def ask(system, prompt):
        r = models.complete(prof, [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                            max_tokens=min(prof.get("max_out", 4096), prof.get("context", 4096)), timeout=TIMEOUT)
        return r.get("text") or ""
    return ask


def slice_run(root, sample, attempt, out, profiles, on_sample=None):
    """Run attempt(module, profile)->result over the sample, each profile in turn until one round-trips; the sample is
    stated (printed, filed) before anything runs; the file is rewritten after each module. Advanced when 2 round-trip."""
    if on_sample:
        on_sample(list(sample))
    res = {"sample": list(sample), "profiles": list(profiles), "modules": [], "advanced": "not-yet", "ran": True}

    def save():
        res["round_trips"] = sum(1 for m in res["modules"] if m["round_trip"])
        res["advanced"] = "M-02 slice" if res["round_trips"] >= 2 else "not-yet"
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
    save()
    for m in sample:
        tried = []
        for prof in profiles:
            try:
                r = attempt(m, prof)
            except (ValueError, OSError) as e:
                r = {"module": m, "round_trip": False, "error": str(e)[:300]}
            tried.append(prof)
            if r.get("round_trip"):
                break
        res["modules"].append({**r, "module": m, "approaches": tried, "model": tried[-1]})
        save()
    return res


def cmd_regen(args):
    from sampo import cli, map as fmap
    p = cli.resolve(args)
    links = fmap.load(p)["tests"]
    sample = leaves(p.root, links, "plugin/lib/sampo/")  # ponytail: Sampo's own library; --under if another repo needs it
    sensitive = bool(c.read_meta(p).get("sensitive"))
    if args.leaves or (not args.path and not args.slice):
        return cli.out(args, {"leaves": sample}, f"{len(sample)} leaf modules (under {MAX_LINES} lines, with a test):\n"
                       + "\n".join(sample))
    from sampo import moonscale
    local = args.model or (moonscale._local(sensitive) or {}).get("name")
    if not local:
        raise SystemExit("regen: no local model answered; name one: --model PROFILE")
    try:
        master = open(os.path.join(p.root, "MASTER.md"), encoding="utf-8").read()
    except OSError:
        master = ""

    def attempt(mod, prof):
        return regen(p.root, mod, make_ask(p, prof, sensitive),
                     intent(p.root, mod, gather_briefs(p, mod), master_entry(master, mod), links), links)
    if args.path:
        rel = os.path.relpath(os.path.abspath(args.path), p.root)
        r = attempt(rel, local)
        lines = [f"{'round trip' if r['round_trip'] else 'no round trip'}: {rel} on {local}, {r['tries']} tries"]
        lines += [f"  {'PASS' if v else 'FAIL'} {k}" for k, v in r["tests"].items()] + [f"  refused: {x}" for x in r["refused"]]
        return cli.out(args, r, "\n".join(lines))
    profiles = [local] + ([] if sensitive else ["haiku"])
    out = os.path.join(p.root, "bench", "moonshot", "m02-slice-result.json")
    res = slice_run(p.root, sample, attempt, out, profiles,
                    on_sample=lambda s: print(f"sample ({len(s)}): " + ", ".join(s), flush=True))
    return cli.out(args, res, f"{res['round_trips']} of {len(sample)} round-trip; Advanced: {res['advanced']}; filed {out}")
