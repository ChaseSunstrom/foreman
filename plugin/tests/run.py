#!/usr/bin/env python3
"""The test suite across the cores (T-0133): the tests `unittest discover` finds, one test class per process (each
test already gets its own FOREMAN_HOME and repo), so the gate waits for the slowest class instead of the sum of all.
Exit 1 on any failure, with each failing class's report.

  python3 plugin/tests/run.py [-j N] [-k PATTERN] [-p GLOB]
"""
import argparse
import concurrent.futures
import os
import re
import subprocess
import sys
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def classes(pattern, k):
    """Every test class id (module.Class) discover would run, biggest first so the long ones start early."""
    sys.path.insert(0, HERE)
    counts = {}

    def walk(suite):
        for t in suite:
            if isinstance(t, unittest.TestSuite):
                walk(t)
            elif not k or any(x in t.id() for x in k):
                cid = f"{type(t).__module__}.{type(t).__name__}"
                counts[cid] = counts.get(cid, 0) + 1
    walk(unittest.defaultTestLoader.discover(HERE, pattern=pattern))
    return sorted(counts, key=lambda c: -counts[c])


def run_one(cid, k):
    t0 = time.time()
    extra = [a for x in k for a in ("-k", x)]
    p = subprocess.run([sys.executable, "-m", "unittest", "-q", cid, *extra], cwd=HERE, capture_output=True,
                       text=True, stdin=subprocess.DEVNULL)
    m = re.search(r"Ran (\d+) tests?", p.stderr)
    return cid, p.returncode, p.stderr, int(m.group(1)) if m else 0, time.time() - t0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("-j", type=int, default=os.cpu_count() or 4)
    ap.add_argument("-k", action="append", default=[], help="only tests whose id contains this (repeatable)")
    ap.add_argument("-p", default="test*.py", help="module glob, as unittest discover's -p")
    a = ap.parse_args()
    t0 = time.time()
    todo = classes(a.p, a.k)
    with concurrent.futures.ThreadPoolExecutor(max(1, a.j)) as ex:
        results = list(ex.map(lambda c: run_one(c, a.k), todo))
    failed = [r for r in results if r[1] != 0]
    for cid, _, err, _, _ in failed:
        sys.stderr.write(f"\n==== {cid}\n{err}")
    total = sum(r[3] for r in results)
    slow = ", ".join(f"{c.split('.')[-1]} {s:.0f}s" for c, _, _, _, s in sorted(results, key=lambda r: -r[4])[:3])
    sys.stderr.write(f"\nRan {total} tests in {time.time() - t0:.1f}s ({len(todo)} classes, {a.j} at a time; "
                     f"slowest: {slow})\n\n{'FAILED (' + str(len(failed)) + ' classes)' if failed else 'OK'}\n")
    return 1 if failed or not total else 0


if __name__ == "__main__":
    sys.exit(main())
