"""fm exam long (T-2258): the long-horizon exam tier. A past task's change (commits ending '(T-NNNN)') replayed from its
base commit as a fresh one-commit repo with no future history; the hidden checks are the tests the change added, kept
only when they fail at the base and pass with the change's files laid over it. Answers are work trees; two zero-token
arms (oracle lays the shipped files over, empty changes nothing). Scores go to the tower's exam.jsonl as tier long.
Local history only: nothing is cloned or fetched, and a repo's tests run only in a tree the user trusts."""
import ast
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

import fmcore as c
import fmfind
import fmprove

TASK = re.compile(r"\(T-(\d+)\)$")
RUN = re.compile(r"l\d{3,}")
AGENTS = ("oracle", "empty")
SCAN, CAP_N, MAX_CHECKS, SAMPLE, RUN_T = 600, 20, 5, 10, 120  # commits read; goals; checks a goal; regression sample; s a run
RUNNER = ("import io, json, sys, unittest\n"
          "class R(unittest.TestResult):\n"
          "    ok = []\n"
          "    def addSuccess(self, t):\n        self.ok.append(t.id())\n"
          "out, ids = sys.argv[1], sys.argv[2:]\n"
          "s = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(i) for i in ids)\n"
          "s.run(R())\n"
          "json.dump(R.ok, open(out, 'w'))\n")


def _root(p):
    return os.path.join(p.dir, "exam", "long")


def _own():
    """Foreman's own repo: the one holding this plugin, else None."""
    top = fmfind._git(c.PLUGIN_ROOT, "rev-parse", "--show-toplevel")
    return os.path.realpath(top.decode().strip()) if top else None


def _top(path):
    top = fmfind._git(path, "rev-parse", "--show-toplevel")
    if not top:
        raise ValueError(f"not a git repo: {c.plain(path)}")
    return os.path.realpath(top.decode().strip())


def _may_run(p, src):
    if src != _own() and not fmprove.trusted(src) and not fmprove._lane_trusted(p, src):
        raise ValueError(f"{c.plain(src)} is not a tree you trusted, so its tests don't run: fm prove {c.plain(src)} "
                         "--yes-run says yes to it (only Foreman's own repo runs without)")


def _ids(text, mod):
    """unittest ids of the test methods in a source text (none when it doesn't parse)."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return set()
    return {f"{mod}.{k.name}.{f.name}" for k in ast.walk(tree) if isinstance(k, ast.ClassDef)
            for f in k.body if isinstance(f, ast.FunctionDef) and f.name.startswith("test_")}


def _is_test(rel):
    return os.path.basename(rel).startswith("test_") and rel.endswith(".py")


def _safe(rel):
    return bool(rel) and not os.path.isabs(rel) and ".." not in rel.split("/") and not rel.startswith(".git/")


def _show(src, rev, rel):
    d = fmfind._git(src, "show", f"{rev}:{rel}")
    return None if d is None else d.decode("utf-8", "replace")


def _archive(src, rev, dst):
    os.makedirs(dst)
    a = subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", src, "archive", rev], capture_output=True, timeout=120)
    if a.returncode:
        raise ValueError(f"git archive {rev} failed")
    subprocess.run(["tar", "-x", "-C", dst], input=a.stdout, check=True, timeout=120)


def _overlay(dst, src, target, files):
    """The target's version of each file laid over dst (a file gone at the target is removed)."""
    for rel in files:
        path = os.path.join(dst, rel)
        data = fmfind._git(src, "show", f"{target}:{rel}")
        if data is None:
            if os.path.isfile(path):
                os.remove(path)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(data)


def _passed(tree, ids, pypath):
    """The ids that pass in tree: a throwaway home, no credentials, no Foreman state; a timeout passes none."""
    import fmbench
    if not ids:
        return set()
    home = tempfile.mkdtemp(prefix="fm-long-")
    try:
        env = {k: v for k, v in os.environ.items() if not k.startswith(("FOREMAN_", "CLAUDE")) and not fmbench.CREDENTIALS.match(k)}
        env.update(HOME=home, PYTHONDONTWRITEBYTECODE="1",
                   PYTHONPATH=os.pathsep.join([tree] + [os.path.join(tree, d) for d in pypath]))
        out = os.path.join(home, "ok.json")
        try:
            subprocess.run([sys.executable, "-c", RUNNER, out, *ids], cwd=tree, env=env, timeout=RUN_T,
                           stdin=subprocess.DEVNULL, capture_output=True)
            with open(out) as f:
                return set(json.load(f))
        except (subprocess.TimeoutExpired, OSError, ValueError):
            return set()
    finally:
        shutil.rmtree(home, ignore_errors=True)


def _tests_in(tree):
    """{id: its folder relative to tree} for every test method in the tree's test files."""
    found = {}
    for d, names, files in os.walk(tree):
        names[:] = [n for n in names if n not in (".git", "node_modules", "__pycache__")]
        for n in files:
            if _is_test(n) and os.path.getsize(os.path.join(d, n)) < 2 ** 20:
                with open(os.path.join(d, n), encoding="utf-8", errors="replace") as f:
                    for i in _ids(f.read(), n[:-3]):
                        found[i] = os.path.relpath(d, tree)
    return found


def _windows(src):
    """[{task, base, target, goal, files}] newest task first: one per task id."""
    raw = fmfind._git(src, "log", "--no-merges", "-n", str(SCAN), "--format=%H%x1f%P%x1f%s")
    groups = {}
    for line in (raw or b"").decode("utf-8", "replace").splitlines():
        h, par, subj = (line.split("\x1f") + ["", ""])[:3]
        m = TASK.search(subj)
        if m and par:
            groups.setdefault("T-" + m.group(1), []).append((h, par.split()[0], subj))
    out = []
    for task, cs in groups.items():  # cs is newest first
        files = []
        for h, _, _ in cs:
            names = fmfind._git(src, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", h) or b""
            files += [f for f in names.decode("utf-8", "replace").split("\0") if f and f not in files and _safe(f)]
        out.append({"task": task, "base": cs[-1][1], "target": cs[0][0], "files": files,
                    "goal": "\n".join(c.plain(s) for _, _, s in reversed(cs))})
    return out


def _scenario(p, src, w, seed, d):
    """The key (checks, sample) for one window, or None when it is no exam: no new test, or one that isn't red at the
    base and green with the change's files laid over it."""
    tests = [f for f in w["files"] if _is_test(f)]
    checks = []
    for f in tests:
        new, old = _show(src, w["target"], f), _show(src, w["base"], f)
        checks += sorted(_ids(new or "", os.path.basename(f)[:-3]) - _ids(old or "", os.path.basename(f)[:-3]))
    if not checks:
        return None
    checks = checks[:MAX_CHECKS]
    base, work = os.path.join(d, "base"), os.path.join(d, "work")
    _archive(src, w["base"], base)
    have = _tests_in(base)
    pypath = sorted({os.path.dirname(f) or "." for f in tests} | set(have.values()))
    others = sorted(set(have) - set(checks))
    pool = random.Random(f"{seed}{w['task']}").sample(others, min(len(others), SAMPLE))
    shutil.copytree(base, work)
    _overlay(work, src, w["target"], tests)  # the hidden tests laid over the base's code: they must fail there
    at_base = _passed(work, checks + pool, pypath)
    if at_base & set(checks):
        return None
    shutil.rmtree(work)
    shutil.copytree(base, work)
    _overlay(work, src, w["target"], w["files"])
    if _passed(work, checks, pypath) != set(checks):
        return None
    return {"checks": checks, "sample": sorted(at_base & set(pool)), "pypath": pypath, "test_files": tests,
            "command": "python3 -m unittest " + " ".join(checks)}


def gen(p, src=None, n=6, seed=0):
    src = _top(src or _own() or p.root)
    _may_run(p, src)
    n = max(1, min(int(n), CAP_N))
    wins = [w for w in _windows(src) if any(_is_test(f) for f in w["files"])]
    random.Random(seed).shuffle(wins)
    os.makedirs(_root(p), exist_ok=True)
    nums = [int(x[1:]) for x in os.listdir(_root(p)) if RUN.fullmatch(x)]
    run = f"l{max(nums, default=0) + 1:03d}"
    kept = []
    for w in wins[:3 * n]:  # ponytail: three tries a goal; a repo with few red-green windows yields fewer
        if len(kept) == n:
            break
        tmp = tempfile.mkdtemp(prefix="fm-long-")
        try:
            k = _scenario(p, src, w, seed, tmp)
            if not k:
                continue
            base = os.path.join(_root(p), run, w["task"])
            _archive(src, w["base"], os.path.join(base, "repo"))
            for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.name=exam", "-c", "user.email=exam@example.com",
                                                      "commit", "-qm", "base"]):
                subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", os.path.join(base, "repo"), *cmd],
                               check=True, capture_output=True)
            key = dict(k, id=w["task"], base=w["base"], target=w["target"], goal=w["goal"], files=w["files"], src=src)
            c.write_atomic(os.path.join(base, "key.json"), json.dumps(key, indent=1))
            kept.append({"id": w["task"], "goal": w["goal"], "repo": os.path.join(base, "repo")})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    meta = {"run": run, "src": src, "scenarios": kept}
    c.write_atomic(os.path.join(_root(p), run, "run.json"), json.dumps(meta, indent=1))
    return meta


def _load(p, run):
    path = os.path.join(_root(p), run or "", "run.json")
    if not (run and RUN.fullmatch(run) and os.path.isfile(path)):
        raise ValueError(f"no long run {run!r} (fm exam long gen makes one)")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _key(p, run, sid):
    with open(os.path.join(_root(p), run, sid, "key.json"), encoding="utf-8") as f:
        return json.load(f)


def _work(p, run, agent, sid):
    return os.path.join(_root(p), run, "work", agent, sid)


def _agent(agent):
    if agent not in AGENTS:
        raise ValueError(f"--agent {', '.join(AGENTS)} (session arms come later), not {c.plain(str(agent))!r}")


def run(p, run, agent):
    _agent(agent)
    meta = _load(p, run)
    for s in meta["scenarios"]:
        key, work = _key(p, run, s["id"]), _work(p, run, agent, s["id"])
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(os.path.join(_root(p), run, s["id"], "repo"), work, ignore=shutil.ignore_patterns(".git"))
        if agent == "oracle":
            _overlay(work, key["src"], key["target"], [f for f in key["files"] if _safe(f)])
    return {"run": run, "agent": agent, "answered": [s["id"] for s in meta["scenarios"]]}


def grade(p, run, agent):
    import fmgenesis
    _agent(agent)
    meta = _load(p, run)
    goals = []
    for s in meta["scenarios"]:
        key, work = _key(p, run, s["id"]), _work(p, run, agent, s["id"])
        if not os.path.isdir(work):
            continue
        _may_run(p, key["src"])
        tmp = tempfile.mkdtemp(prefix="fm-long-")
        try:  # the answer's copy with the hidden tests laid over it: an answer can't edit the checks away
            shutil.copytree(work, os.path.join(tmp, "w"))
            _overlay(os.path.join(tmp, "w"), key["src"], key["target"], [f for f in key["test_files"] if _safe(f)])
            ok = _passed(os.path.join(tmp, "w"), key["checks"] + key["sample"], key["pypath"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        goals.append({"id": s["id"], "true_done": set(key["checks"]) <= ok, "checks": len(key["checks"]),
                      "regressions": [i for i in key["sample"] if i not in ok]})
    if not goals:
        raise ValueError(f"no answers from {agent!r} in {run} (fm exam long run {run} --agent {agent})")
    res = {"tier": "long", "agent": agent, "run": run, "at": c.now(), "gen": fmgenesis.current(p), "model": "default",
           "scenarios": len(goals), "true_done": sum(g["true_done"] for g in goals),
           "regressions": sum(len(g["regressions"]) for g in goals), "goals": goals}
    fmgenesis.exam_line(p, res)
    return res


def cmd(p, args):
    import fmcli
    verb, rest = args.run, getattr(args, "rest", None) or []
    if verb == "gen":
        meta = gen(p, args.from_, args.n or 6, args.seed)
        return fmcli.out(args, meta, f"{meta['run']}: {len(meta['scenarios'])} goal(s) from {c.plain(meta['src'])}\n"
                         + "\n".join(f"  {s['id']}: {s['goal'].splitlines()[0]}" for s in meta["scenarios"]))
    if verb in ("run", "grade") and rest:
        agent = args.agent or "oracle"
        r = run(p, rest[0], agent) if verb == "run" else grade(p, rest[0], agent)
        text = (f"{agent} answered {len(r['answered'])} goal(s) of {rest[0]}" if verb == "run" else
                f"{agent} {rest[0]}: {r['true_done']}/{r['scenarios']} true done, {r['regressions']} regressions")
        return fmcli.out(args, r, text)
    raise ValueError("fm exam long gen [--from PATH] [--n N] | run RUN --agent oracle|empty | grade RUN --agent oracle|empty")
