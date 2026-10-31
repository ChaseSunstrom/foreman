"""fm exam long (T-2258): the long-horizon exam tier. A past task's change (commits ending '(T-NNNN)') replayed from its
base commit as a fresh one-commit repo with no future history; the hidden checks are the tests the change added, kept
only when they fail at the base and pass with the change's files laid over it. Answers are work trees; two zero-token
arms (oracle lays the shipped files over, empty changes nothing). Scores go to the tower's exam.jsonl as tier long.
Local history only: nothing is cloned or fetched, and a repo's tests run only in a tree the user trusts, in a throwaway
copy, by a runner outside the tree that loads each hidden test by its path (an answer can't shadow the stdlib or a
test module)."""
import ast
import concurrent.futures
import json
import os
import random
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

import fmcore as c
import fmfind
import fmprove

TASK = re.compile(r"\(T-(\d+)\)$")
RUN = re.compile(r"l\d{3,}")
GOAL_ID = re.compile(r"T-\d+")  # a task id, as TASK finds it in a commit subject
ID = re.compile(r"([A-Za-z0-9_./-]+\.py)::[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*")
REV = re.compile(r"[0-9a-f]{40}")
AGENTS = ("oracle", "empty")
SESSIONS = ("foreman", "plain")  # T-2262: a headless claude session a goal, in a temp copy of the goal's repo
FAULTS = ("kill", "pause", "compaction", "misleading")
KILL_T, PAUSE_GAP, COMPACT_AT, SESSION_T = 3, 30, 20000, 60  # min the kill lets a turn run; s a pause lasts; tokens; min a turn
PLANT = "test_planted_old_behaviour.py"
GOAL = "{goal}\n\nWork in this repo until the change is done and its tests pass."
PAUSE = (" Mid-way, at a natural checkpoint, stop and say PAUSED: you will be asked to continue later (this is a "
         "usage-limit stop).")
CONTINUE = "Continue where you left off and finish the change."
# commits read; goals; checks a goal; new ids tried a goal; regression sample; s a run; s a gen
SCAN, CAP_N, MAX_CHECKS, MAX_NEW, SAMPLE, RUN_T, GEN_T = 600, 20, 5, 50, 10, 120, 900
RUNNER = """import importlib.util, json, os, sys, unittest
spec = json.load(open(sys.argv[1]))
os.chdir(spec["tree"])
sys.path.extend(spec["paths"])
ok = []
for i in spec["ids"]:
    try:
        f, name = i.split("::")
        mod, rest = name.split(".", 1)
        s = importlib.util.spec_from_file_location(mod, os.path.join(spec["tree"], f))
        m = importlib.util.module_from_spec(s)
        sys.modules[mod] = m
        s.loader.exec_module(m)
        r = unittest.TestResult()
        unittest.defaultTestLoader.loadTestsFromName(rest, m).run(r)
        if r.testsRun == 1 and r.wasSuccessful() and not r.skipped:
            ok.append(i)
    except BaseException:
        pass
json.dump(ok, open(spec["out"], "w"))
"""


def _root(p):
    return os.path.join(p.dir, "exam", "long")


def _own():
    """Foreman's own repo: the toplevel holding this plugin (never an enclosing repo that merely contains it), else None."""
    top = fmfind._git(c.PLUGIN_ROOT, "rev-parse", "--show-toplevel")
    top = os.path.realpath(top.decode().strip()) if top else None
    return top if top and os.path.isfile(os.path.join(top, "plugin", "lib", "fmlong.py")) else None


def _top(path):
    top = fmfind._git(path, "rev-parse", "--show-toplevel")
    if not top:
        raise ValueError(f"not a git repo: {c.plain(path)}")
    return os.path.realpath(top.decode().strip())


def _may_run(p, src):
    if src != _own() and not fmprove.trusted(src) and not fmprove._lane_trusted(p, src):
        raise ValueError(f"{c.plain(src)} is not a tree you trusted, so its tests don't run: fm prove {c.plain(src)} "
                         "--yes-run says yes to it (only Foreman's own repo runs without)")


def _ids(text, rel):
    """Ids 'dir/test_x.py::test_x.Class.test_y' of the test methods of a source text's module-level TestCase subclasses
    (none when it doesn't parse)."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return set()
    mod = os.path.basename(rel)[:-3]
    return {f"{rel}::{mod}.{k.name}.{f.name}" for k in tree.body if isinstance(k, ast.ClassDef)
            and any((b.attr if isinstance(b, ast.Attribute) else getattr(b, "id", "")).endswith("TestCase") for b in k.bases)
            for f in k.body if isinstance(f, ast.FunctionDef) and f.name.startswith("test_")}


def _is_test(rel):
    return os.path.basename(rel).startswith("test_") and rel.endswith(".py")


def _safe(rel):
    return bool(rel) and not os.path.isabs(rel) and ".." not in rel.split("/") and not rel.startswith(".git/")


def _check_key(key):
    """A key.json is data: forged ids, paths or revisions are refused before they reach git or an import."""
    bad = (not all(isinstance(i, str) and ID.fullmatch(i) and _safe(i.split("::")[0]) for i in key["checks"] + key["sample"])
           or not all(isinstance(f, str) and _safe(f) for f in key["files"] + key["test_files"] + key["pypath"])
           or not all(isinstance(key.get(k), str) and REV.fullmatch(key[k]) for k in ("base", "target")))
    if bad:
        raise ValueError(f"{key.get('id')}: key.json holds an id, path or revision that isn't one")


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


def _passed(tree, ids, pypath, end=None):
    """The ids that pass in tree, or None when the runner failed or timed out (distinct from all red): run by a script
    outside the tree under -I (the stdlib first, the tree appended), in its own process group (c.run_command kills it
    whole), a throwaway home, no credentials, no Foreman state."""
    import fmbench
    if not ids:
        return set()
    home = tempfile.mkdtemp(prefix="fm-long-")
    try:
        env = {k: v for k, v in os.environ.items() if not k.startswith(("FOREMAN_", "CLAUDE")) and not fmbench.CREDENTIALS.match(k)}
        env["HOME"] = home
        out, script = os.path.join(home, "ok.json"), os.path.join(home, "runner.py")
        c.write_atomic(script, RUNNER)
        c.write_atomic(os.path.join(home, "spec.json"), json.dumps(
            {"tree": tree, "out": out, "ids": ids, "paths": [tree] + [os.path.join(tree, d) for d in pypath]}))
        t = max(1, min(RUN_T, int(end - time.time()))) if end else RUN_T
        code, _ = c.run_command(tree, shlex.join([sys.executable, "-I", "-B", script, os.path.join(home, "spec.json")]),
                                timeout=t, env=env)
        if code == 124:
            return None
        try:
            with open(out) as f:
                return {i for i in json.load(f) if i in ids}
        except (OSError, ValueError):
            return None
    finally:
        shutil.rmtree(home, ignore_errors=True)


def _tests_in(tree):
    """{id: its folder relative to tree} for every test method in the tree's test files."""
    found = {}
    for d, names, files in os.walk(tree):
        names[:] = [n for n in names if n not in (".git", "node_modules", "__pycache__")]
        for n in files:
            if _is_test(n) and os.path.getsize(os.path.join(d, n)) < 2 ** 20:
                rel = os.path.relpath(os.path.join(d, n), tree)
                with open(os.path.join(d, n), encoding="utf-8", errors="replace") as f:
                    for i in _ids(f.read(), rel):
                        found[i] = os.path.dirname(rel) or "."
    return found


def _windows(src):
    """[{task, base, target, goal, files}] one per task id."""
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


def _scenario(src, w, seed, d, end):
    """The key for one window, or None when it is no exam. The hidden checks are every test id the window added (any
    task's commit interleaved in it too) that goes green with the window's files laid over the base, and red on the
    base's code under the same tests; at least one is needed, five are kept. The regression sample is base tests that
    pass at the base and stay green with the change. A runner failure or timeout drops the window.
    Hidden test files, and the support files the window changed beside them (helpers, conftest, fixtures), are what
    grade lays over an answer (ponytail: the same folder as a changed test file; a nested fixture folder isn't)."""
    tests = [f for f in w["files"] if _is_test(f)]
    dirs = {os.path.dirname(f) for f in tests}
    hidden = [f for f in w["files"] if os.path.dirname(f) in dirs]  # tests and their support files
    new = set()
    for f in tests:
        new |= _ids(_show(src, w["target"], f) or "", f) - _ids(_show(src, w["base"], f) or "", f)
    new = sorted(new)[:MAX_NEW]
    if not new:
        return None
    base, red, green = (os.path.join(d, x) for x in ("base", "red", "green"))
    _archive(src, w["base"], base)
    have = _tests_in(base)
    pypath = sorted({os.path.dirname(f) or "." for f in tests} | set(have.values()))
    others = sorted(set(have) - set(new))
    pool = random.Random(f"{seed}{w['task']}").sample(others, min(len(others), SAMPLE))
    shutil.copytree(base, red)
    _overlay(red, src, w["target"], hidden)  # the hidden tests over the base's code: the checks must fail there
    at_base = _passed(red, new + pool, pypath, end)
    shutil.copytree(base, green)
    _overlay(green, src, w["target"], w["files"])
    ok = _passed(green, new + pool, pypath, end)
    if at_base is None or ok is None:
        return None
    checks = [i for i in new if i in ok and i not in at_base][:MAX_CHECKS]
    if not checks:
        return None
    return {"checks": checks, "sample": sorted(i for i in pool if i in ok and i in at_base), "pypath": pypath,
            "test_files": hidden, "command": "fm exam long grade (its runner loads each id by its path)"}


def gen(p, src=None, n=6, seed=0):
    n = int(n)
    if not 1 <= n <= CAP_N:
        raise ValueError(f"--n is how many goals to make: 1 to {CAP_N}")
    src = _top(src or _own() or p.root)
    _may_run(p, src)
    end = time.time() + GEN_T
    wins = [w for w in _windows(src) if any(_is_test(f) for f in w["files"])]
    random.Random(seed).shuffle(wins)
    os.makedirs(_root(p), exist_ok=True)
    nums = [int(x[1:]) for x in os.listdir(_root(p)) if RUN.fullmatch(x)]
    run = f"l{max(nums, default=0) + 1:03d}"
    kept = []
    for w in wins[:3 * n]:  # ponytail: three tries a goal; a repo with few red-green windows yields fewer
        if len(kept) == n or time.time() >= end:
            break
        tmp = tempfile.mkdtemp(prefix="fm-long-")
        try:
            k = _scenario(src, w, seed, tmp, end)
            if not k:
                continue
            base = os.path.join(_root(p), run, w["task"])
            _archive(src, w["base"], os.path.join(base, "repo"))
            for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.name=exam", "-c", "user.email=exam@example.com",
                                                      "-c", "commit.gpgsign=false", "commit", "-qm", "base"]):
                subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", os.path.join(base, "repo"), *cmd],
                               check=True, capture_output=True)
            key = dict(k, id=w["task"], base=w["base"], target=w["target"], goal=w["goal"], files=w["files"], src=src)
            c.write_atomic(os.path.join(base, "key.json"), json.dumps(key, indent=1))
            kept.append({"id": w["task"], "goal": w["goal"], "repo": os.path.join(base, "repo")})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if not kept:
        raise ValueError(f"no goal in {c.plain(src)}: no (T-NNNN) task change adds a test that fails at its base and passes "
                         "with the change")
    meta = {"run": run, "src": src, "scenarios": kept}
    c.write_atomic(os.path.join(_root(p), run, "run.json"), json.dumps(meta, indent=1))
    return meta


def _load(p, run):
    path = os.path.join(_root(p), run or "", "run.json")
    if not (run and RUN.fullmatch(run) and os.path.isfile(path)):
        raise ValueError(f"no long run {run!r} (fm exam long gen makes one)")
    with open(path, encoding="utf-8") as f:
        meta = json.load(f)
    ids = [s.get("id") if isinstance(s, dict) else None for s in meta.get("scenarios") or []]
    if not all(isinstance(i, str) and GOAL_ID.fullmatch(i) for i in ids) or len(set(ids)) != len(ids):  # run.json is data
        raise ValueError(f"{run}: run.json holds a goal id that fm exam long gen never writes")
    return meta


def _key(p, run, sid):
    with open(os.path.join(_root(p), run, sid, "key.json"), encoding="utf-8") as f:
        key = json.load(f)
    _check_key(key)
    return key


def _work(p, run, agent, sid):
    return os.path.join(_root(p), run, "work", agent, sid)


def _agent(agent):
    if agent not in AGENTS + SESSIONS:
        raise ValueError(f"--agent {', '.join(AGENTS + SESSIONS)}, not {c.plain(str(agent))!r}")


def _stamp(p, run, agent):
    return os.path.join(_root(p), run, "answers", agent, "model")


def _goal_session(agent, base, key, work, model, budget, timeout, faults):
    """One goal in a temp copy of its repo (with .git), as fmexam._session_arm does it, with the faults planted: a
    misleading test before the session; a kill (the first turn capped at KILL_T minutes, then resumed by its id); a pause
    (the turn told to stop at a checkpoint, PAUSE_GAP seconds, then resumed); a forced small compaction window.
    (known cost, error, fault log, run info for fm exam long grade: T-2263); the tree it leaves is copied to work."""
    import fmbench
    unknown = []  # turns that reported no cost: counted apart, never as 0

    def num(r):
        v = r.get("total_cost_usd")
        unknown.append(not isinstance(v, (int, float)))
        return v if isinstance(v, (int, float)) else 0
    log, t0, sid = [], time.monotonic(), str(uuid.uuid4())
    since = lambda: round(time.monotonic() - t0, 1)
    with tempfile.TemporaryDirectory() as tmp:
        wt, state = os.path.join(tmp, "repo"), os.path.join(tmp, "state")
        shutil.copytree(os.path.join(base, "repo"), wt)
        env = fmbench._env(c.PLUGIN_ROOT, state)
        if agent == "foreman":
            fmbench._seed(c.PLUGIN_ROOT, wt, env)
            plugins, settings = [c.PLUGIN_ROOT], None
        else:
            env.update(FOREMAN_QUIET="1", PATH=os.environ.get("PATH", ""))
            plugins, settings = [], fmbench._bare_guard(c.PLUGIN_ROOT)
        if "compaction" in faults:
            env["CLAUDE_CODE_AUTO_COMPACT_WINDOW"] = str(COMPACT_AT)
        if "misleading" in faults:  # ponytail: an always-red decoy (no per-goal knowledge needed), so any goal's checks contradict it
            plant = os.path.join(os.path.dirname(next((f for f in key["test_files"] if _is_test(f)), "tests/x")), PLANT)
            c.write_atomic(os.path.join(wt, plant), "import unittest\n\n\nclass Planted(unittest.TestCase):\n"
                           "    def test_old_behaviour_must_stay(self):\n"
                           "        self.fail('expects the behaviour from before the goal: do not change it')\n")
            log.append({"kind": "misleading", "at": since(), "file": plant})
        ask = GOAL.format(goal=key["goal"]) + (PAUSE if "pause" in faults else "")
        sids = [sid]
        res, err = fmbench._session(wt, env, plugins, ask, model, budget, min(KILL_T, timeout) if "kill" in faults else timeout,
                                    keep=True, settings=settings, sid=sid)
        cost, last = num(res), res
        killed = "kill" in faults and str(err).startswith("timed out")
        paused = "pause" in faults and "PAUSED" in str(res.get("result") or "")
        if "kill" in faults:  # a killed turn reports no cost: unknown, not zero
            log.append({"kind": "kill", "at": since(), "fired": killed, "resumed": False, **({"cost_unknown": True} if killed else {})})
        if "pause" in faults:
            log.append({"kind": "pause", "at": since(), "gap_s": PAUSE_GAP, "fired": paused, "resumed": False})
        if killed or paused:
            time.sleep(PAUSE_GAP if paused else 0)
            again, err = fmbench._session(wt, env, plugins, CONTINUE, model, budget, timeout, resume=sid, keep=True,
                                          settings=settings)
            cost, last = cost + num(again), again
            fresh = bool(err) and not again  # no result at all: the resume itself failed (the kill beat the session file)
            if fresh:
                sid2 = str(uuid.uuid4())
                sids.append(sid2)
                again, err = fmbench._session(wt, env, plugins, GOAL.format(goal=key["goal"]), model, budget, timeout,
                                              keep=True, settings=settings, sid=sid2)
                cost, last = cost + num(again), again
            for f in log:
                if f["kind"] in ("kill", "pause") and f["fired"]:
                    f.update(resumed=True, resume_ok=not fresh and not err, resumed_at=since(), **({"fresh": True} if fresh else {}))
        n = sum(fmbench._compactions(x) for x in sids)  # also removes each transcript from claude's projects dir
        if "compaction" in faults:
            log.append({"kind": "compaction", "at": since(), "compactions": n, "ok": n >= 1})
        for f in log:
            if f["kind"] == "misleading":
                f["kept"] = os.path.isfile(os.path.join(wt, f["file"]))
        shutil.copytree(wt, work, symlinks=True, ignore=shutil.ignore_patterns(".git"))
        import fmhooks
        events = os.path.join(state, "events.jsonl")  # a guard block is an event in the session's own state
        blocks = sum(fmbench._diagnose(state)["guard_blocks"].values()) if os.path.isfile(events) else None
        info = {"cost": cost, "cost_unknown": any(unknown) or any(f.get("cost_unknown") for f in log),
                "said_done": bool(last.get("result")) and not err and fmhooks.claims_done(str(last["result"])), "secs": since(),
                "ended_ok": not err, "resume_failed": sum(bool(f.get("resumed") and not f.get("resume_ok")) for f in log),
                "guard_blocks": blocks}
    return cost, err, log, info


def run(p, run, agent, model=None, budget=None, timeout=None, faults=(), limit=None, jobs=1):
    _agent(agent)
    import fmexam
    jobs = fmexam._jobs(jobs)
    bad = [f for f in faults if f not in FAULTS]
    if bad or (faults and agent not in SESSIONS):
        raise ValueError(f"--faults {', '.join(FAULTS)} go with a session agent ({', '.join(SESSIONS)}), not "
                         f"{c.plain(str(bad or agent))}")
    timeout = timeout or SESSION_T
    meta = _load(p, run)
    picked = meta["scenarios"]
    if agent in SESSIONS:
        import fmbudget
        picked = picked[:3 if limit is None else max(0, int(limit))]  # ponytail: a spend guard as in fmexam.run_agent; --limit raises it
        per = 0.5 * (2 if {"kill", "pause"} & set(faults) else 1)  # a resumed goal is two or more turns
        est = lambda n: fmbudget.estimate("exam-arm", n, per)
        fmbudget.check("exam-arm", est(len(picked)), "a smaller --limit")
        shutil.rmtree(os.path.join(_root(p), run, "work", agent), ignore_errors=True)  # no stale goal outside the limit
        for d in (os.path.join(_root(p), run, x, agent) for x in ("answers", "faults")):
            shutil.rmtree(d, ignore_errors=True)  # this run's, not a rerun's
        c.write_atomic(_stamp(p, run, agent), c.plain(model or "default")[:60])
    errors = {}

    def session(s):
        key, work = _key(p, run, s["id"]), _work(p, run, agent, s["id"])
        shutil.rmtree(work, ignore_errors=True)
        with fmbudget.reserve("exam-arm", est(1), "a smaller --limit"):  # the day's spend may have moved since the last goal
            cost, err, log, info = _goal_session(agent, os.path.join(_root(p), run, s["id"]), key, work, model, budget, timeout, faults)
            fmbudget.record("exam-arm", cost, project=p.slug, detail=f"long {agent} {s['id']}")
        c.write_atomic(os.path.join(_root(p), run, "faults", agent, s["id"] + ".json"), json.dumps(log, indent=1))
        c.write_atomic(os.path.join(_root(p), run, "faults", agent, s["id"] + ".run.json"), json.dumps(info, indent=1))
        if err:
            errors[s["id"]] = c.fit(c.plain(str(err)), 200)
    if agent in SESSIONS:  # T-2292: up to `jobs` goals at once, each in its own temp copy; the files written are per goal
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            list(pool.map(session, picked))
    for s in () if agent in SESSIONS else picked:
        key, work = _key(p, run, s["id"]), _work(p, run, agent, s["id"])
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(os.path.join(_root(p), run, s["id"], "repo"), work, ignore=shutil.ignore_patterns(".git"))
        if agent == "oracle":
            _overlay(work, key["src"], key["target"], key["files"])
    return {"run": run, "agent": agent, "answered": [s["id"] for s in picked], "errors": errors}


def _metrics(p, run, agent, g):
    """T-2263: one goal's false-done claim, cost, interventions, seconds and guard blocks, from the run info `run` stored
    beside its fault log. A goal with no info (a zero-token arm, an older run) or no answer has each of them as None:
    unknown is never 0. A false-done is the session's last reply claiming done while a hidden check fails.
    resumes_needed is where a person would have to step in: a planned resume that failed, or a session that ended in
    error. unfinished is a session that ended with no done claim and no error: it stopped short, which is no
    intervention. secs is the session's wall time: the tree is only checked once, at its end, so
    the time to the first true-done is bounded by it."""
    none = {"false_done": None, "cost": None, "cost_unknown": None, "resumes_needed": None, "unfinished": None, "secs": None, "guard_blocks": None}
    try:
        with open(os.path.join(_root(p), run, "faults", agent, g["id"] + ".run.json"), encoding="utf-8") as f:
            info = json.load(f)
    except (OSError, ValueError):
        return none
    if not (g["answered"] and isinstance(info, dict)):
        return none
    num = lambda k, kind=(int, float): info[k] if isinstance(info.get(k), kind) and not isinstance(info.get(k), bool) else None
    flag = lambda k: info[k] if isinstance(info.get(k), bool) else None  # a flag the run didn't store is unknown
    said, ok = flag("said_done"), flag("ended_ok")
    return {"false_done": None if said is None else said and not g["true_done"], "cost": num("cost"),
            "cost_unknown": info.get("cost_unknown") is not False,
            "resumes_needed": None if ok is None else (num("resume_failed", int) or 0) + (not ok),
            "unfinished": None if ok is None or said is None else int(ok and not said), "secs": num("secs"),
            "guard_blocks": num("guard_blocks", int)}


def _totals(goals):
    """The run's rows over its answered goals: a sum over the goals that know it (None when none does) and the count of
    goals that don't, under "unknown"."""
    mine = [g for g in goals if g["answered"]]
    known = lambda k: [g[k] for g in mine if g.get(k) is not None]
    tot = lambda k: sum(known(k)) if known(k) else None
    secs = [g["secs"] for g in mine if g["true_done"] and g.get("secs") is not None]
    out = {"rate": round(sum(g["true_done"] for g in goals) / len(goals), 3) if goals else 0,
           "false_done": tot("false_done"), "resumes_needed": tot("resumes_needed"), "unfinished": tot("unfinished"), "guard_blocks": tot("guard_blocks"),
           "cost": round(tot("cost"), 4) if known("cost") else None,
           "cost_unknown": sum(g.get("cost") is None or g.get("cost_unknown") is not False for g in mine),
           "hours_to_done": round(min(secs) / 3600, 3) if secs else None,
           # a revert (a landed change taken back) can't be seen in the final tree the run keeps: unknown, not 0
           "reverts": None}
    out["unknown"] = {k: sum(g.get(k) is None for g in mine) for k in ("false_done", "resumes_needed", "unfinished", "guard_blocks")}
    out["unknown"]["hours_to_done"] = sum(g["true_done"] and g.get("secs") is None for g in mine)
    return out


def grade(p, run, agent):
    import fmgenesis
    _agent(agent)
    meta = _load(p, run)
    goals = []
    for s in meta["scenarios"]:  # every goal counts: one without an answer is not done
        key, work = _key(p, run, s["id"]), _work(p, run, agent, s["id"])
        g = {"id": s["id"], "answered": os.path.isdir(work), "true_done": False, "checks": len(key["checks"]), "regressions": []}
        if g["answered"]:
            _may_run(p, key["src"])
            tmp = tempfile.mkdtemp(prefix="fm-long-")
            try:  # the answer's copy with the hidden tests and their support files laid over it
                shutil.copytree(work, os.path.join(tmp, "w"))
                _overlay(os.path.join(tmp, "w"), key["src"], key["target"], key["test_files"])
                ok = _passed(os.path.join(tmp, "w"), key["checks"] + key["sample"], key["pypath"])
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            if ok is None:
                g["error"] = "the runner failed or timed out"
            else:
                g.update(true_done=set(key["checks"]) <= ok, regressions=[i for i in key["sample"] if i not in ok])
        g.update(_metrics(p, run, agent, g))
        goals.append(g)
    if not any(g["answered"] for g in goals):
        raise ValueError(f"no answers from {agent!r} in {run} (fm exam long run {run} --agent {agent})")
    try:  # a session arm's model, stamped at run so a Haiku line never decides; the zero-token arms have none
        with open(_stamp(p, run, agent), encoding="utf-8") as f:
            model = f.read().strip() or None
    except OSError:
        model = None
    res = {"tier": "long", "agent": agent, "run": run, "at": c.now(), "gen": fmgenesis.current(p), "model": model,
           "scenarios": len(goals), "true_done": sum(g["true_done"] for g in goals),
           "regressions": sum(len(g["regressions"]) for g in goals), "goals": goals, **_totals(goals)}
    fmgenesis.exam_line(p, res)
    return res


def cmd(p, args):
    import fmcli
    verb, rest = args.run, getattr(args, "rest", None) or []
    if verb == "gen":
        meta = gen(p, args.from_, 6 if args.n is None else args.n, args.seed)
        return fmcli.out(args, meta, f"{meta['run']}: {len(meta['scenarios'])} goal(s) from {c.plain(meta['src'])}\n"
                         + "\n".join(f"  {s['id']}: {s['goal'].splitlines()[0]}" for s in meta["scenarios"]))
    if verb in ("run", "grade") and rest:
        agent = args.agent or "oracle"
        faults = [f for f in (args.faults or "").split(",") if f]
        r = (run(p, rest[0], agent, args.model, args.budget, args.timeout, faults, args.limit, args.jobs) if verb == "run" else grade(p, rest[0], agent))
        text = (f"{agent} answered {len(r['answered'])} goal(s) of {rest[0]}" if verb == "run" else
                f"{agent} {rest[0]}: {r['true_done']}/{r['scenarios']} true done, {r['regressions']} regressions")
        return fmcli.out(args, r, text)
    raise ValueError("fm exam long gen [--from PATH] [--n N] | run RUN --agent oracle|empty|foreman|plain [--faults kill,pause,compaction,misleading] | "
                     "grade RUN --agent oracle|empty|foreman|plain")
