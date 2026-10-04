"""fm bench (T-0212): Foreman's own benchmark, made of the project's finished work. A finished task whose work is one
commit naming it, with test files in that commit and verify commands on its criteria, becomes a case: the repo at the
commit's parent, the task's original request as the prompt, the commit's test files as hidden tests and the verify
commands as the grade. `build` keeps a case only if its verify commands fail at the parent with the hidden tests in
place and pass at the commit (SWE-bench's fail-to-pass check), so a case tells a fix from no fix.

`run` replays cases headless: a temporary git worktree at the parent, a fresh Foreman state (FOREMAN_STATE, seeded with
full autonomy and drive on), `claude -p` with the candidate plugin (--plugin-dir; user settings left out so the
installed Foreman doesn't load beside it); then the hidden tests are restored and the verify commands decide. Cost,
turns and time come from claude's JSON result. Results are kept per label; `compare` sets two side by side, which is
how /foreman:improve judges a candidate on real past work instead of synthetic cases."""
import collections
import contextlib
import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time

import fmbudget
import fmcore as c

TEST_FILE = re.compile(r"(^|/)(tests?|spec|__tests__)/|(^|/)test_[^/]*\.py$|_test\.\w+$|\.(test|spec)\.\w+$")


def _git(root, *args, timeout=120):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}  # nothing points it at another repo
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, timeout=timeout, env=env)


@contextlib.contextmanager
def _worktree(root, rev):
    """A detached worktree of the repo at rev in a temporary folder: (folder, worktree). Always removed."""
    tmp = tempfile.mkdtemp(prefix="fm-bench-")
    wt = os.path.join(tmp, "repo")
    r = _git(root, "worktree", "add", "--detach", "-q", wt, rev)
    if r.returncode:
        shutil.rmtree(tmp, ignore_errors=True)
        raise OSError(f"git worktree add {rev[:10]}: {r.stderr.strip()[:200]}")
    try:
        yield tmp, wt
    finally:
        _git(root, "worktree", "remove", "--force", wt)
        shutil.rmtree(tmp, ignore_errors=True)
        _git(root, "worktree", "prune")


# Credentials a replay never needs (claude's own login stays): forge, cloud and package-registry tokens.
# ponytail: a denylist (names that look like credentials); an allowlist of env names if replays ever run untrusted code
CREDENTIALS = re.compile(r"^(GITHUB_|GH_|GITLAB_|AWS_|AZURE_|GOOGLE_|GCP_|GCLOUD_|NPM_|PYPI_|TWINE_|DOCKER_|HF_|OPENAI_|"
                         r"CARGO_REGISTRY_|SSH_AUTH_SOCK$|DATABASE_URL$|.*_(TOKEN|SECRET|PASSWORD|KEY|CREDENTIALS)$)")


def _env(plugin, state):
    """Foreman isolated: its own state, the candidate's fm first on PATH, no session or project pinned from outside,
    no credentials beyond Claude's own."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("FOREMAN_", "CLAUDECODE", "CLAUDE_CODE_ENTRY"))
           and (k.startswith(("ANTHROPIC_", "CLAUDE_")) or not CREDENTIALS.match(k))}  # claude's own login stays
    env.update(FOREMAN_STATE=state, PATH=os.path.join(plugin, "bin") + os.pathsep + os.environ.get("PATH", ""))
    return env


def has_guard(plugin):
    """Whether a plugin ships Foreman's guard: a PreToolUse hook on Bash. Replays run in bypass mode, as the user's own
    sessions do, so the guard is what stands between a replay and the machine."""
    try:
        with open(os.path.join(plugin, "hooks", "hooks.json"), encoding="utf-8") as f:
            pre = json.load(f).get("hooks", {}).get("PreToolUse") or []
    except (OSError, ValueError, AttributeError):
        return False
    return os.path.isfile(os.path.join(plugin, "lib", "fmguard.py")) and any(
        isinstance(h, dict) and "Bash" in str(h.get("matcher", "")) for h in pre)


def _grade(wt, case, env, timeout=900):
    """[(cmd, exit code, last lines)] of the case's verify commands, with its hidden tests restored."""
    r = _git(wt, "checkout", case["commit"], "--", *case["tests"])
    if r.returncode:  # grading without the hidden tests would grade whatever the session left
        return [("restore the hidden tests", r.returncode, r.stderr.strip()[-200:])]
    out = []
    for cmd in case["verify"]:
        code, output = c.run_command(wt, cmd, timeout, env=env)
        out.append((cmd, code, " / ".join(x.strip() for x in output.strip().splitlines()[-2:])[:200]))
    return out


def _cases_path(p):
    return os.path.join(p.dir, "bench", "cases.json")


def build(p, ids=None, last=30):
    """(cases, skipped reasons) from finished tasks, newest first, each validated fail-to-pass."""
    cases, skipped = [], []
    done = sorted((b for b in c.load_briefs(p, include_archive=True) if b.status == "done"),
                  key=lambda b: b.meta.get("updated") or "", reverse=True)
    for b in done:
        if ids and b.id not in ids or not ids and len(cases) + len(skipped) >= last:
            continue
        commits = _git(p.root, "log", "--format=%H", "-F", f"--grep=({b.id})").stdout.split()
        if len(commits) != 1:
            skipped.append(f"{b.id}: {len(commits)} commits name it (one is needed)")
            continue
        sha = commits[0]
        base = _git(p.root, "rev-parse", "-q", "--verify", f"{sha}^").stdout.strip()
        # added or changed files only (a deleted test can't be restored), NUL-separated (no quoted names)
        files = _git(p.root, "show", "--name-only", "--diff-filter=AM", "-z", "--format=", sha).stdout.split("\0")
        tests = sorted(f for f in files if f and TEST_FILE.search(f))
        verify = [v for _, v in b.verify_cmds() if v]
        prompt = c.plain(re.sub(r"(?m)^>\s?", "", b.section("Raw request")).strip()) or b.title
        if not base or not tests or not verify:
            skipped.append(f"{b.id}: " + ("a root commit" if not base else "no test files in its commit" if not tests
                                          else "no verify commands"))
            continue
        case = {"id": b.id, "title": b.title, "tier": b.tier, "type": b.type, "commit": sha, "base": base,
                "tests": tests, "verify": verify, "prompt": prompt}
        why = validate(p, case)
        (skipped.append(f"{b.id}: {why}") if why else cases.append(case))
    return cases, skipped


DOC_FILE = re.compile(r"\.(md|rst|txt|adoc)$|(^|/)(docs?|CHANGELOG|LICENSE)", re.I)


def build_commits(p, rng, verify, last=30):
    """T-0222: (cases, skipped) from a repo's own commits: one that adds or changes test files and source becomes a
    case (prompt: its message; verify: the given command, {tests} → its test files), validated fail-to-pass."""
    cases, skipped = [], []
    for sha in _git(p.root, "rev-list", "--no-merges", f"--max-count={last}", rng).stdout.split():
        cid = f"C-{sha[:10]}"
        base = _git(p.root, "rev-parse", "-q", "--verify", f"{sha}^").stdout.strip()
        files = [f for f in _git(p.root, "show", "--name-only", "--diff-filter=AM", "-z", "--format=", sha)
                 .stdout.split("\0") if f]
        tests = sorted(f for f in files if TEST_FILE.search(f))
        src = [f for f in files if not TEST_FILE.search(f) and not DOC_FILE.search(f)]
        msg = _git(p.root, "log", "-1", "--format=%B", sha).stdout.strip()
        if not base or not tests or not src:
            skipped.append(f"{cid}: " + ("a root commit" if not base else "no test files" if not tests else "tests only"))
            continue
        case = {"id": cid, "title": c.fit(msg.splitlines()[0] if msg else sha, 100), "tier": "?", "type": "COMMIT",
                "commit": sha, "base": base, "tests": tests, "prompt": c.plain(msg) or cid,
                "verify": [verify.replace("{tests}", " ".join(shlex.quote(t) for t in tests))]}
        why = validate(p, case)
        (skipped.append(f"{cid}: {why}") if why else cases.append(case))
    return cases, skipped


def validate(p, case):
    """None if the verify commands fail at the base with the hidden tests and pass at the commit, else why not."""
    try:
        with _worktree(p.root, case["commit"]) as (tmp, wt):
            after = _grade(wt, case, _env(c.PLUGIN_ROOT, os.path.join(tmp, "state")))
        if any(code for _, code, _ in after):
            return "its verify commands fail at its own commit (environment-dependent?)"
        with _worktree(p.root, case["base"]) as (tmp, wt):
            before = _grade(wt, case, _env(c.PLUGIN_ROOT, os.path.join(tmp, "state")))
    except (OSError, subprocess.SubprocessError) as e:
        return str(e)[:160]
    return None if any(code for _, code, _ in before) else "its verify commands already pass before the change"


def _diagnose(state):
    """T-0220: what the replay's own Foreman did, from its state before the worktree goes: ledger events by kind, its
    tasks' type, tier and final status, guard blocks by category, and the tools used most."""
    ledger, blocks, tools, tasks = collections.Counter(), collections.Counter(), collections.Counter(), {}
    for path in glob.glob(os.path.join(state, "projects", "*", "ledger.jsonl")):
        ledger.update(str(e.get("event")) for e in c.tail_jsonl(path, 20000))
    for path in sorted(glob.glob(os.path.join(state, "projects", "*", "tasks", "*.md"))):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                head = f.read(2000)
        except OSError:
            continue
        meta = dict(re.findall(r"(?m)^(id|type|tier|status): *(\S+)", head))
        if meta.get("id"):
            tasks[meta["id"]] = f"{meta.get('type', '?')} {meta.get('tier', '?')} {meta.get('status', '?')}"
    for e in c.tail_jsonl(os.path.join(state, "events.jsonl"), 50000):
        if e.get("kind") == "guard_block":
            blocks[str(e.get("category"))] += 1
        elif e.get("kind") == "tool":
            tools[str(e.get("tool"))] += 1
    return {"ledger": dict(ledger), "tasks": tasks, "guard_blocks": dict(blocks), "tools": dict(tools.most_common(8))}


def _result_json(text):
    """claude -p --output-format json's result object (the last JSON line that has one)."""
    for line in reversed((text or "").strip().splitlines()):
        try:
            data = json.loads(line)
        except ValueError:
            continue
        if isinstance(data, dict) and ("total_cost_usd" in data or data.get("type") == "result"):
            return data
    return {}


def run_case(p, case, plugin, model=None, budget=3.0, timeout=30):
    t0 = time.monotonic()
    with _worktree(p.root, case["base"]) as (tmp, wt):
        state = os.path.join(tmp, "state")
        env = _env(plugin, state)
        fm = os.path.join(plugin, "bin", "fm")
        for args in (["init"], ["autonomy", "full"], ["drive", "on"]):
            subprocess.run([fm, *args], cwd=wt, env=env, capture_output=True, timeout=60)
        prompt = (f"Task: {case['prompt']}\n\n(Unattended benchmark run: the user is away and granted full autonomy; "
                  f"finish the work with Foreman, deciding with your defaults.)")
        cmd = ["claude", "-p", prompt, "--plugin-dir", plugin, "--setting-sources", "project,local",
               "--output-format", "json", "--permission-mode", "bypassPermissions", "--no-session-persistence",
               "--max-budget-usd", f"{budget:g}"] + (["--model", model] if model else [])
        error, res = None, {}
        try:  # its own process group: a timeout takes the session's tools down with it
            pr = subprocess.Popen(cmd, cwd=wt, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                  stdin=subprocess.DEVNULL, start_new_session=True)
            try:
                so, se = pr.communicate(timeout=timeout * 60)
                res = _result_json(so)
                if pr.returncode and not res:
                    error = f"exit {pr.returncode}: {(se or so).strip()[-160:]}"
            except subprocess.TimeoutExpired:
                os.killpg(pr.pid, 9)
                pr.communicate()
                error = f"timed out after {timeout} min"
        except OSError as e:
            error = f"can't start claude: {e}"
        graded = _grade(wt, case, env)
        diag = _diagnose(state)
    fmbudget.record("bench", res.get("total_cost_usd"), project=p.slug, detail=case["id"])  # T-0227
    return {"id": case["id"], "pass": not error and all(code == 0 for _, code, _ in graded), "diag": diag,
            "verify": [{"cmd": x, "exit": code, "tail": tail} for x, code, tail in graded],
            "cost_usd": res.get("total_cost_usd"), "turns": res.get("num_turns"),
            "seconds": round(time.monotonic() - t0), "error": error or (res.get("result") if res.get("is_error") else None)}


def run_case_n(p, case, plugin, model=None, budget=3.0, timeout=30, runs=1):
    """T-0221: a case run `runs` times: pass rate, mean cost, turns and time; the first attempt's details kept."""
    tries = [run_case(p, case, plugin, model, budget, timeout) for _ in range(max(1, runs))]
    rate = sum(t["pass"] for t in tries) / len(tries)

    def mean(k):
        vals = [t[k] for t in tries if t[k] is not None]
        return round(sum(vals) / len(vals), 4) if vals else None
    return dict(tries[0], runs=len(tries), pass_rate=rate, cost_usd=mean("cost_usd"), turns=mean("turns"),
                seconds=mean("seconds"), **{"pass": rate >= 0.5},
                attempts=[{k: t[k] for k in ("pass", "cost_usd", "turns", "seconds", "error")} for t in tries])


def _rate(x):
    return x.get("pass_rate", 1.0 if x.get("pass") else 0.0)


def gate(a, b, tolerance=0.15):
    """(ok, lines): candidate b is no worse than a on their shared cases — no fewer passes in total, and mean cost per
    case at most `tolerance` higher. Old results without repeats count each pass as 1.0."""
    shared = sorted({x["id"] for x in a["cases"]} & {x["id"] for x in b["cases"]})
    if not shared:
        return False, ["no shared cases: run both on the same cases (fm bench run --ids …)"]
    A, B = ({x["id"]: x for x in r["cases"]} for r in (a, b))
    sa, sb = sum(_rate(A[i]) for i in shared), sum(_rate(B[i]) for i in shared)
    lost = [i for i in shared if _rate(B[i]) < _rate(A[i])]
    costs = [[r[i]["cost_usd"] for i in shared if r[i].get("cost_usd") is not None] for r in (A, B)]
    ca, cb = (sum(x) / len(x) if x else None for x in costs)
    lines, ok = [f"{a['label']} → {b['label']}: passes {sa:g} → {sb:g} over {len(shared)} shared case(s)"
                 + (f"; cost/case ${ca:.2f} → ${cb:.2f}" if ca is not None and cb is not None else "")], True
    if sb < sa:
        ok = False
        lines.append(f"✗ fewer passes (lost ground on {', '.join(lost)})")
    elif lost:
        lines.append(f"  (lost ground on {', '.join(lost)}, made up elsewhere)")
    if ca and cb is not None and cb > ca * (1 + tolerance):
        ok = False
        lines.append(f"✗ cost per case up {round(100 * (cb / ca - 1))}% (over {round(100 * tolerance)}%)")
    if all(r[i].get("runs", 1) == 1 for r in (A, B) for i in shared):
        lines.append("  single runs: a flipped case may be noise (--runs 3 measures it)")
    lines.append("✓ no worse: may be proposed" if ok else "✗ not proposed")
    return ok, lines


def recommend(by_model, cases):
    """T-0223: {tier: model}: per tier, the model with the most passes on that tier's cases, the lowest mean cost
    among ties. by_model: {model: [case result]}."""
    tiers = {x["id"]: x.get("tier") for x in cases}
    out = {}
    for tier in sorted({t for t in tiers.values() if t in ("S", "M", "L")}):
        scores = []
        for model, results in by_model.items():
            mine = [r for r in results if tiers.get(r["id"]) == tier]
            costs = [r["cost_usd"] for r in mine if r.get("cost_usd") is not None]
            scores.append((-sum(_rate(r) for r in mine), sum(costs) / len(costs) if costs else float("inf"), model))
        best = min(scores)
        if best[0] < 0:  # a tier no model passed keeps its current choice
            out[tier] = best[2]
    return out


def run_arm(p, cases, plugin, label, model=None, budget=3.0, timeout=30, runs=1, quiet=False, head=None):
    """Every case on one plugin, results written after each case (a crash or Ctrl-C keeps what was paid for). Refuses a
    plugin without the guard here, so no caller can skip it (replays run in bypass mode)."""
    fmbudget.check("bench", fmbudget.estimate("bench", len(cases) * max(1, runs), min(budget, 0.5)),
                   "fewer cases (--max) or --runs")
    if not has_guard(plugin):
        raise ValueError(f"{plugin} doesn't ship Foreman's guard (a PreToolUse Bash hook and lib/fmguard.py); "
                         f"replays run in bypass mode, so they never run without it")
    results = []
    res = {"label": label, "plugin": plugin, "model": model, "at": c.now(), "head": head, "cases": results}
    os.makedirs(_results_dir(p), exist_ok=True)
    _git(p.root, "worktree", "prune")  # a killed earlier run's worktree
    for case in cases:
        print(f"bench {label}: {case['id']} …", flush=True) if not quiet else None
        try:
            results.append(run_case_n(p, case, plugin, model, budget, timeout, runs))
        except (OSError, subprocess.SubprocessError, ValueError) as e:  # one case, not the run's paid results
            results.append({"id": case["id"], "pass": False, "verify": [], "cost_usd": None, "turns": None,
                            "seconds": 0, "error": f"{type(e).__name__}: {c.fit(str(e), 160)}"})
        c.write_atomic(os.path.join(_results_dir(p), label + ".json"), json.dumps(res, indent=1))
    return res


def _results_dir(p):
    return os.path.join(p.dir, "bench", "results")


def _load_cases(p):
    try:
        with open(_cases_path(p), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def _summary(res):
    cases = res["cases"]
    cost = sum(x["cost_usd"] or 0 for x in cases)
    turns = [x["turns"] for x in cases if x["turns"] is not None]
    return (f"{sum(x['pass'] for x in cases)}/{len(cases)} passed · ${cost:.2f} · "
            f"{sum(turns) / len(turns):.1f} turns/case" if turns else
            f"{sum(x['pass'] for x in cases)}/{len(cases)} passed · ${cost:.2f}")


def cmd_bench(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.bench_cmd == "build":
        if bool(args.commits) != bool(args.verify):
            raise fmcli.UsageError("--commits RANGE and --verify CMD go together (CMD may use {tests})")
        if args.commits:
            cases, skipped = build_commits(p, args.commits, args.verify, args.last)
        else:
            cases, skipped = build(p, ids=set(args.ids or []) or None, last=args.last)
        new = {y["id"] for y in cases}
        # --ids and --commits add or refresh their cases; a full rebuild from briefs keeps the commit cases
        keep = (lambda x: x["id"] not in new) if args.commits else \
            (lambda x: x["id"] not in new | set(args.ids)) if args.ids else \
            (lambda x: x["id"].startswith("C-") and x["id"] not in new)
        cases += [x for x in _load_cases(p) if keep(x)]
        os.makedirs(os.path.dirname(_cases_path(p)), exist_ok=True)
        c.write_atomic(_cases_path(p), json.dumps(cases, indent=1))
        return fmcli.out(args, {"cases": cases, "skipped": skipped},
                         f"{len(cases)} bench case(s) in {_cases_path(p)}: {', '.join(x['id'] for x in cases) or 'none'}"
                         + "".join(f"\n  skipped {s}" for s in skipped[:12]))
    if args.bench_cmd == "list":
        cases = _load_cases(p)
        lines = [f"{len(cases)} case(s): " + (", ".join(f"{x['id']} [{x['type']} {x['tier']}]" for x in cases) or
                                              "none (fm bench build)")]
        folder = _results_dir(p)
        names = [n for n in (os.listdir(folder) if os.path.isdir(folder) else []) if n.endswith(".json")]
        for n in sorted(names, key=lambda n: os.path.getmtime(os.path.join(folder, n)))[-8:]:
            try:
                with open(os.path.join(folder, n), encoding="utf-8") as f:
                    lines.append(f"  {n[:-5]}: {_summary(json.load(f))}")
            except (OSError, ValueError, KeyError, TypeError):
                lines.append(f"  {n[:-5]}: unreadable")
        return fmcli.out(args, {"cases": cases}, "\n".join(lines))
    if args.bench_cmd == "run":
        cases = [x for x in _load_cases(p) if not args.ids or x["id"] in args.ids][:args.max]
        if not cases:
            raise fmcli.UsageError("no bench cases: fm bench build first (or --ids names none of them)")
        plugin = os.path.abspath(args.plugin or c.PLUGIN_ROOT)
        if not os.path.isfile(os.path.join(plugin, ".claude-plugin", "plugin.json")):
            raise fmcli.UsageError(f"{plugin} isn't a plugin folder (no .claude-plugin/plugin.json)")
        if not has_guard(plugin):  # ponytail: the guard is a speed bump; an OS sandbox (bwrap) if candidates are untrusted
            raise fmcli.UsageError(f"{plugin} doesn't ship Foreman's guard (a PreToolUse Bash hook and lib/fmguard.py); "
                                   f"replays run in bypass mode, so they never run without it")
        label = args.label or time.strftime("%Y%m%d-%H%M%S")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}", label):
            raise fmcli.UsageError(f"label must be a plain name, got {label!r}")
        try:
            res = run_arm(p, cases, plugin, label, args.model, args.budget, args.timeout, args.runs, quiet=args.json)
        except ValueError as e:
            raise fmcli.UsageError(str(e))
        results = res["cases"]
        with c.lock(p.dir):
            c.log_event(p, "bench", data={"label": label, "passed": sum(x["pass"] for x in results),
                                          "cases": len(results)}, session=fmcli.session())
        fmcli.out(args, res, f"bench {label}: {_summary(res)}\n" + "\n".join(
            f"  {'✓' if x['pass'] else '✗'} {x['id']} · {x['turns']} turns · ${x['cost_usd'] or 0:.2f} · {x['seconds']} s"
            + (f" · {x['error']}" if x["error"] else "") for x in results))
        return 0 if all(x["pass"] for x in results) else 1
    if args.bench_cmd == "models":
        cases = [x for x in _load_cases(p) if not args.ids or x["id"] in args.ids][:args.max]
        models = [m.strip() for m in args.models.split(",") if m.strip()]
        if not cases or not models or not all(re.fullmatch(r"[\w.:-]+", m) for m in models):
            raise fmcli.UsageError("fm bench models needs cases (fm bench build) and --models like haiku,sonnet,opus")
        try:
            fmbudget.check("bench", fmbudget.estimate("bench", len(cases) * len(models) * max(1, args.runs),
                                                      min(args.budget, 0.5)), "fewer --models or --max")
        except fmbudget.BudgetError as e:
            raise fmcli.UsageError(str(e))
        stamp, by_model = time.strftime("%Y%m%d-%H%M%S"), {}
        os.makedirs(_results_dir(p), exist_ok=True)
        _git(p.root, "worktree", "prune")
        for m in models:
            results = []
            for case in cases:
                try:
                    results.append(run_case_n(p, case, c.PLUGIN_ROOT, m, args.budget, args.timeout, args.runs))
                except (OSError, subprocess.SubprocessError, ValueError) as e:
                    results.append({"id": case["id"], "pass": False, "pass_rate": 0.0, "cost_usd": None,
                                    "turns": None, "error": f"{type(e).__name__}: {c.fit(str(e), 120)}"})
            by_model[m] = results
            c.write_atomic(os.path.join(_results_dir(p), f"models-{m}-{stamp}.json"),
                           json.dumps({"label": f"models-{m}-{stamp}", "model": m, "at": c.now(), "cases": results}))
        rec = recommend(by_model, cases)
        lines = [f"{m}: " + _summary({"cases": r}) for m, r in by_model.items()]
        lines.append("recommend: " + (",".join(f"{t}={m}" for t, m in rec.items()) or "nothing (no model passed)")
                     + (" — saved for fm run" if args.save and rec else " (fm bench models --save keeps it for fm run)"
                        if rec else ""))
        if args.save and rec:
            c.update_meta(p, run_models=dict(c.read_meta(p).get("run_models") or {}, **rec))
        return fmcli.out(args, {"recommend": rec, "models": {m: _summary({"cases": r}) for m, r in by_model.items()}},
                         "\n".join(lines))
    if args.bench_cmd == "gate":
        runs = []
        for label in (args.a, args.b):
            try:
                with open(os.path.join(_results_dir(p), label + ".json"), encoding="utf-8") as f:
                    runs.append(json.load(f))
            except (OSError, ValueError):
                raise fmcli.UsageError(f"no bench results named {label!r} (fm bench list)")
        ok, lines = gate(runs[0], runs[1], args.cost_tolerance)
        fmcli.out(args, {"ok": ok, "lines": lines}, "\n".join(lines))
        return 0 if ok else 1
    if args.bench_cmd == "show":
        try:
            with open(os.path.join(_results_dir(p), args.label + ".json"), encoding="utf-8") as f:
                res = json.load(f)
        except (OSError, ValueError):
            raise fmcli.UsageError(f"no bench results named {args.label!r} (fm bench list)")
        lines = [f"bench {res['label']}: {_summary(res)}"]
        for x in res["cases"]:
            d = x.get("diag") or {}
            led = d.get("ledger") or {}
            lines.append(f"{'✓' if x['pass'] else '✗'} {x['id']} · {x['turns']} turns · ${x['cost_usd'] or 0:.2f}"
                         + (f" · {x['error']}" if x.get("error") else ""))
            lines.append("  tasks: " + (", ".join(f"{k} {v}" for k, v in (d.get("tasks") or {}).items()) or "none made"))
            lines.append("  ledger: " + (", ".join(f"{k} {v}" for k, v in sorted(led.items(), key=lambda kv: -kv[1])[:10])
                                         or "nothing recorded"))
            if d.get("guard_blocks"):
                lines.append("  guard blocks: " + ", ".join(f"{k} {v}" for k, v in d["guard_blocks"].items()))
            lines += [f"  verify: {v['cmd']} → exit {v['exit']} · {v['tail']}" for v in x.get("verify") or []]
        return fmcli.out(args, res, "\n".join(lines))
    # compare
    runs = []
    for label in (args.a, args.b):
        try:
            with open(os.path.join(_results_dir(p), label + ".json"), encoding="utf-8") as f:
                runs.append(json.load(f))
        except (OSError, ValueError):
            raise fmcli.UsageError(f"no bench results named {label!r} (fm bench list)")
    shared = sorted({x["id"] for x in runs[0]["cases"]} & {x["id"] for x in runs[1]["cases"]})
    by = [{x["id"]: x for x in r["cases"] if x["id"] in shared} for r in runs]
    lines = [f"{r['label']}: " + _summary({"cases": list(b.values())}) for r, b in zip(runs, by)]
    lines += [f"  {i}: {' → '.join('✓' if b[i]['pass'] else '✗' for b in by)}" for i in shared
              if by[0][i]["pass"] != by[1][i]["pass"]]
    fmcli.out(args, {"shared": shared, "runs": [r["label"] for r in runs]}, "\n".join(lines))
