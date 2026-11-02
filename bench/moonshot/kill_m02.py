"""M-02 kill test (T-2679): can a module be rebuilt from its spec and tests alone?

Builds the spec suite (bench/spec-suite/make.py) in OUT/kit, then for each module deletes kit/<m>.py and asks a
tool-less child (fmideas.run_child: no tools, no hooks, no MCP) for it, given only the task commit's message (the
complete spec), the module's test file and the package's base files. Two attempts each; a module passes when either
attempt passes every original test. Pass (viable) if at least 2 of 3 modules pass. Prints one JSON object."""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "plugin", "lib"))
import fmideas  # noqa: E402

OUT = sys.argv[1]
MODULES = ("semver", "table", "ranges")
SYSTEM = ("You write one Python module from its specification and its tests. Python 3.10+, standard library only. "
          "Reply with only the module's complete source in one ```python block, nothing else.")


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout


def main():
    repo = os.path.join(OUT, "kit")
    subprocess.run([sys.executable, os.path.join(ROOT, "bench", "spec-suite", "make.py"), repo], check=True,
                   capture_output=True)
    base = {f: open(os.path.join(repo, f), encoding="utf-8").read()
            for f in ("README.md", "kit/__init__.py") if os.path.exists(os.path.join(repo, f))}
    res = {}
    for m in MODULES:
        path, test = f"kit/{m}.py", f"tests/test_{m}.py"
        sha = git(repo, "log", "--format=%H", "--diff-filter=A", "--", path).split()[-1]
        spec = git(repo, "log", "-1", "--format=%B", sha).strip()
        tests = open(os.path.join(repo, test), encoding="utf-8").read()
        prompt = (f"Specification (the commit message that added {path}):\n{spec}\n\n"
                  f"The tests it must pass ({test}):\n```python\n{tests}\n```\n\n"
                  + "".join(f"Base file {f}:\n```\n{t}\n```\n\n" for f, t in base.items())
                  + f"Write {path}.")
        tries = []
        for attempt in (1, 2):
            text = fmideas.run_child("moonshot-kill", SYSTEM, prompt, "sonnet", 600, project="foreman-4a056f",
                                     detail=f"M-02 {m} attempt {attempt}") or ""
            code = re.search(r"```python\n(.*?)```", text, re.S)
            with open(os.path.join(repo, path), "w", encoding="utf-8") as f:
                f.write(code.group(1) if code else "")
            run = subprocess.run([sys.executable, "-m", "unittest", f"tests.test_{m}"], cwd=repo, capture_output=True,
                                 text=True, timeout=120)
            last = (run.stderr or run.stdout).strip().splitlines()[-1:] or [""]
            tries.append({"attempt": attempt, "passed": run.returncode == 0, "summary": last[0][:120]})
            if run.returncode == 0:
                break
        res[m] = {"passed": any(t["passed"] for t in tries), "tries": tries}
    n = sum(r["passed"] for r in res.values())
    print(json.dumps({"modules": res, "passed": n, "of": len(MODULES), "verdict": "viable" if n >= 2 else "not-yet"},
                     indent=1))


main()
