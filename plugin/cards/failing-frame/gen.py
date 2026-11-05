"""failing-frame: run the tests in a copy of the scratch tree and report the first failure's project frames."""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

from cardkit import emit, fail, read_input

BUDGET = 48  # seconds for every test run together (the card's run has 60)
inp = read_input()["inputs"]
runner, target = inp.get("runner", "auto"), inp.get("target") or ""
tmp = os.environ["TMPDIR"]
run = os.path.join(tmp, "run")
shutil.copytree(os.getcwd(), run, symlinks=True)  # the tests may write files: never in the card's own copy
harness = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness.py")
has_pytest = importlib.util.find_spec("pytest") is not None


def text(rel):
    with open(os.path.join(run, rel), encoding="utf-8", errors="replace") as f:
        return f.read()


def is_test(rel):
    base, parts = os.path.basename(rel), rel.split("/")[:-1]
    return base.startswith("test") or base.endswith("_test.py") or base == "conftest.py" or "tests" in parts \
        or "test" in parts


def test_files():
    out = []
    for top, dirs, files in os.walk(run):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in ("node_modules", "venv", "__pycache__"))
        out += [os.path.relpath(os.path.join(top, n), run) for n in sorted(files)
                if n.endswith(".py") and (n.startswith("test") or n.endswith("_test.py"))]
    return out


def mode_of(rel):
    return "unittest" if "unittest" in text(rel) else "script"


if runner == "pytest" and not has_pytest:
    fail("environment: missing pytest: use runner 'unittest' or 'script' (script runs one test file as python3 FILE)")
if runner == "script" and not target:
    fail("runner 'script' needs a target, the file to run" + (f", e.g. {test_files()[0]!r}" if test_files() else ""))
if runner == "auto":
    if has_pytest:
        plans = [("pytest", target)]
    elif target:
        plans = [(mode_of(target), target)]
    else:
        plans = [(mode_of(f), f) for f in test_files()]
        if not plans:
            fail("there are no test*.py or *_test.py files here: name the file to run as target")
else:
    plans = [(runner, target)]

result = os.path.join(tmp, "frame.json")
deadline, ran, used = time.monotonic() + BUDGET, 0, []
failure = None
for mode, t in plans:
    left = deadline - time.monotonic()
    if left < 1:
        fail(f"the tests ran past {BUDGET} s after {', '.join(used)}: name one test file as target")
    if os.path.exists(result):
        os.unlink(result)
    used.append(t or mode)
    try:
        p = subprocess.run([sys.executable, "-I", "-B", harness, mode, t, result], cwd=run, capture_output=True,
                           text=True, errors="replace", timeout=left)
    except subprocess.TimeoutExpired:
        fail(f"{t or 'the tests'} ran past {BUDGET} s: name one test file as target")
    try:
        with open(result) as f:
            state = json.load(f)
    except (OSError, ValueError):
        state = {"ran": 1, "failure": {"test": t, "exception": None, "frames": [],
                                       "message": f"the tests exited {p.returncode} before reporting: "
                                                  + (p.stderr or p.stdout)[-1500:].strip()}}
    ran += state.get("ran", 0)
    if state.get("failure"):
        failure, runner = state["failure"], mode
        break
    runner = mode

if failure is None:
    emit({"failed": False, "runner": runner, "ran": ran, "summary": (
        f"{ran} test{'s' if ran != 1 else ''} ran in {', '.join(used)} and passed" if ran else
        "no test ran: name the test file as target, with runner 'script' to run it as python3 FILE")})
    sys.exit(0)


def ours(top):
    """True when the project has a module or package named top (then a failed import of it is the project's bug)."""
    for base, dirs, files in os.walk(run):
        if top in dirs or top + ".py" in files or top + ".pyi" in files:
            return True
    return False


missing = re.search(r"No module named '([^']+)'", failure["message"] or "")
if missing and not ours(missing.group(1).split(".")[0]):  # not installed here: the machine's gap, not the code's
    fail(f"environment: missing {missing.group(1).split('.')[0]} (the tests import it and it isn't installed)")

root = os.path.realpath(run)


def project(path):
    """path relative to the worktree, or None outside it (the standard library, site-packages, the harness)."""
    if not os.path.isabs(path):  # <frozen importlib._bootstrap>, <string>
        return None
    p = os.path.realpath(path)
    return os.path.relpath(p, root) if p.startswith(root + os.sep) and os.path.isfile(p) else None


frames = []
for path, line, func, code in failure["frames"]:
    rel = project(path)
    if rel and line:
        frames.append({"file": rel, "line": line, "function": func, "code": code.strip()})
syn = failure.get("syntax")
if syn and project(syn[0]) and syn[1]:
    frames.append({"file": project(syn[0]), "line": syn[1], "function": "<syntax>", "code": syn[2]})
code_frames = [f for f in frames if not is_test(f["file"])]
where = dict((code_frames or frames)[-1]) if frames else None
tests = [f for f in frames if is_test(f["file"])]
test_frame = tests[-1] if tests else None
if where:
    lines = text(where["file"]).splitlines()
    n = where["line"]
    where["context"] = "\n".join(f"{'>' if i == n else ' '}{i:>4} | {lines[i - 1]}"
                                 for i in range(max(1, n - 3), min(len(lines), n + 3) + 1))
test = failure["test"]
if str(test).endswith(".py") and test_frame and test_frame["function"] != "<module>":
    test = f"{test}::{test_frame['function']}"
at = where and f" at {where['file']}:{where['line']} in {where['function']}"
via = test_frame and where and (test_frame["file"], test_frame["line"]) != (where["file"], where["line"]) \
    and f", reached from {test_frame['file']}:{test_frame['line']}"
emit({"failed": True, "runner": runner, "test": test, "exception": failure["exception"], "message": failure["message"],
      "frames": frames, "where": where, "test_frame": test_frame,
      "summary": f"{failure['exception'] or 'the run'}: {failure['message'][:200]}{at or ''}{via or ''}"})
