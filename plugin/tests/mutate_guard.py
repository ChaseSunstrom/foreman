#!/usr/bin/env python3
"""Test the guard's tests (T-0496): flip one operator or constant inside fmguard's check functions, run the guard
test files against that copy, and report each mutant the tests don't notice (it "survived": a weak spot).

    python3 plugin/tests/mutate_guard.py [--max 20] [--seed N] [--list]

Each mutant runs in a scratch copy of the plugin; the real tree is never touched. It's a report: it exits 0."""
import argparse
import ast
import glob
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(PLUGIN, "lib", "fmguard.py")
FLIPS = [(" == ", " != "), (" != ", " == "), (" not in ", " in "), (" >= ", " < "), (" <= ", " > "),
         (" > ", " <= "), (" < ", " >= "), (" and ", " or "), (" or ", " and "), ("True", "False"), ("False", "True")]


def mutants():
    """[(line number, old, new)] for every flip inside a check function (names starting check or _check)."""
    src = open(GUARD, encoding="utf-8").read()
    lines = src.splitlines()
    spans = [(n.lineno, n.end_lineno) for n in ast.walk(ast.parse(src))
             if isinstance(n, ast.FunctionDef) and re.match(r"_?check", n.name)]
    out = []
    for a, b in spans:
        for i in range(a, b + 1):
            code = lines[i - 1].split("#", 1)[0]
            if code.strip().startswith(("def ", '"""')) or '"' in code and code.count('"') % 2:
                continue
            for old, new in FLIPS:
                if old in code:
                    out.append((i, old, new))
    return sorted(set(out))


def judge(m):
    """'killed' when the guard tests fail on the mutant, 'survived' when they pass."""
    n, old, new = m
    with tempfile.TemporaryDirectory() as tmp:
        copy = os.path.join(tmp, "plugin")
        shutil.copytree(PLUGIN, copy, ignore=shutil.ignore_patterns("__pycache__", "fixtures"))
        path = os.path.join(copy, "lib", "fmguard.py")
        lines = open(path, encoding="utf-8").read().split("\n")
        lines[n - 1] = lines[n - 1].replace(old, new, 1)
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        tests = sorted(os.path.basename(t) for t in glob.glob(os.path.join(copy, "tests", "test_guard*.py")))
        args = [x for t in tests for x in ("-p", t)]
        r = subprocess.run([sys.executable, os.path.join(copy, "tests", "run.py"), *args], capture_output=True,
                           text=True, timeout=900)
        return "survived" if r.returncode == 0 else "killed"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--max", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--list", action="store_true", help="list the mutants, run nothing")
    a = ap.parse_args()
    every = mutants()
    pick = random.Random(a.seed).sample(every, min(a.max, len(every)))
    src = open(GUARD, encoding="utf-8").read().splitlines()
    if a.list:
        print(f"{len(every)} mutants in fmguard's check functions; {len(pick)} shown")
        for n, old, new in pick:
            print(f"fmguard.py:{n} {old.strip()} → {new.strip()}: {src[n - 1].strip()[:100]}")
        return
    survived = []
    for m in pick:
        verdict = judge(m)
        print(f"{verdict:8} fmguard.py:{m[0]} {m[1].strip()} → {m[2].strip()}", flush=True)
        if verdict == "survived":
            survived.append(m)
    print(f"{len(pick) - len(survived)} killed, {len(survived)} survived of {len(pick)} (of {len(every)} possible)"
          + "".join(f"\n  weak: fmguard.py:{n}: {src[n - 1].strip()[:100]}" for n, _, _ in survived))


if __name__ == "__main__":
    main()
