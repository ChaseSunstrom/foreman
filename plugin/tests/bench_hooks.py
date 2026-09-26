#!/usr/bin/env python3
"""Hook latency benchmark: runs every fixture payload through hooks/hook N times in a scratch project.

Usage: bench_hooks.py [--runs N] [--json]. Exits 1 if any hook's p95 exceeds its budget (BUILD_PROMPT §2.8).
Also imported by `fm doctor`.
"""
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)
HOOK = os.path.join(PLUGIN, "hooks", "hook")
FM = os.path.join(PLUGIN, "bin", "fm")
BUDGET_MS = {"default": 150, "MessageDisplay": 100}


def _scratch_project(tmp):
    repo = os.path.join(tmp, "app")
    os.makedirs(os.path.join(repo, "src"))
    env = dict(os.environ, FOREMAN_HOME=os.path.join(tmp, "fhome"))
    git_env = dict(env, GIT_AUTHOR_NAME="b", GIT_AUTHOR_EMAIL="b@x", GIT_COMMITTER_NAME="b", GIT_COMMITTER_EMAIL="b@x")
    for cmd in (["git", "init", "-q", "-b", "main", repo], ["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", "i"]):
        subprocess.run(cmd, check=True, env=git_env)

    def fm(*a):
        subprocess.run([sys.executable, FM, *a], cwd=repo, env=env, check=True, capture_output=True)
    fm("task", "new", "Benchmark task", "--type", "FIX", "--tier", "S", "--scope", "src/**")
    fm("task", "step", "T-0001", "add", "reproduce")
    fm("task", "step", "T-0001", "add", "fix")
    fm("focus", "T-0001")
    for i in range(10):
        fm("task", "new", f"queued {i}", "--type", "CLEAN", "--tier", "S")
        fm("capture", f"idea {i}")
    return repo, env


def run_bench(runs=30):
    with open(os.path.join(HERE, "fixtures", "hook_payloads.json")) as f:
        fixtures = json.load(f)
    results = {}
    with tempfile.TemporaryDirectory() as tmp:
        repo, env = _scratch_project(tmp)
        env["CLAUDE_ENV_FILE"] = os.path.join(tmp, "envfile")
        for name, payload in fixtures.items():
            event = name.split(":")[0]
            body = json.dumps(dict({"session_id": "bench", "cwd": repo, "hook_event_name": event},
                                   **json.loads(json.dumps(payload).replace("{cwd}", repo))))
            times, codes = [], set()
            for _ in range(runs):
                t0 = time.perf_counter()
                p = subprocess.run([HOOK, event], input=body, capture_output=True, text=True, env=env, cwd=repo)
                times.append((time.perf_counter() - t0) * 1000)
                codes.add(p.returncode)
            times.sort()
            budget = BUDGET_MS.get(event, BUDGET_MS["default"])
            p95 = times[min(len(times) - 1, int(len(times) * 0.95))]
            results[name] = {"p50": round(statistics.median(times), 1), "p95": round(p95, 1), "budget": budget,
                             "ok": p95 <= budget, "exit_codes": sorted(codes)}
    return results


def main():
    runs = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 30
    res = run_bench(runs)
    if "--json" in sys.argv:
        print(json.dumps(res, indent=2))
    else:
        print(f"{'hook':<24}{'p50 ms':>8}{'p95 ms':>8}{'budget':>8}  exit")
        for k, v in res.items():
            print(f"{k:<24}{v['p50']:>8}{v['p95']:>8}{v['budget']:>8}  {v['exit_codes']}{'' if v['ok'] else '  OVER BUDGET'}")
    return 0 if all(v["ok"] for v in res.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
