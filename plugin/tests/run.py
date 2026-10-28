#!/usr/bin/env python3
"""The test suite across the cores (T-0133): the tests `unittest discover` finds, one test class per process (each
test already gets its own FOREMAN_HOME and repo), so the gate waits for the slowest class instead of the sum of all.
Exit 1 on any failure, with each failing class's report.

  python3 plugin/tests/run.py [-j N] [-k PATTERN] [-p GLOB] [--load N]
"""
import argparse
import concurrent.futures
import contextlib
import os
import re
import signal
import subprocess
import sys
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def skipped():
    """T-1101: the modules FOREMAN_SKIP_TESTS names (fm check: another open task's red-first test files)."""
    return {x.strip() for x in os.environ.get("FOREMAN_SKIP_TESTS", "").split(",") if x.strip()}


def classes(patterns, k, hit=None):
    """Every test class id (module.Class) discover would run, biggest first so the long ones start early; hit (a set)
    gets each -k pattern or name that matched a test."""
    sys.path.insert(0, HERE)
    counts, skip, hit = {}, skipped(), set() if hit is None else hit

    def walk(suite):
        for t in suite:
            if isinstance(t, unittest.TestSuite):
                walk(t)
            elif skip and (t.id().rsplit(".", 1)[-1] if type(t).__name__ == "_FailedTest"  # a module that won't import
                           else type(t).__module__) in skip:
                continue
            elif not k or any(x in t.id() for x in k):
                hit.update(x for x in k if x in t.id())
                cid = f"{type(t).__module__}.{type(t).__name__}"
                counts[cid] = counts.get(cid, 0) + 1
    for pattern in dict.fromkeys(patterns):
        walk(unittest.TestLoader().discover(HERE, pattern=pattern))  # not the shared one: unittest -k filters it
    return sorted(counts, key=lambda c: -counts[c])


def annotations(cid, err):
    """T-1248: one GitHub ::error line per failing test (its title, the line that failed and the exception); output
    with no FAIL:/ERROR: blocks (an import error) keeps its last four lines."""
    out = []
    for name, block in re.findall(r"(?m)^(?:FAIL|ERROR): (\w+) \([^)]*\)\n-+\n(.*?)(?=\n=+\n|\n-+\nRan |\Z)", err, re.S):
        lines = [x.strip() for x in block.splitlines() if x.strip()]
        code = [x for x in lines if not x.startswith(("Traceback", "File ")) and lines.index(x) < len(lines) - 1]
        body = ([code[-1]] if code else []) + lines[-1:]
        out.append(f"::error title={cid}.{name}::" + "%0A".join(body).replace("::", ": :"))
    if not out:
        tail = [x.strip() for x in err.splitlines() if x.strip() and not set(x.strip()) <= set("-=~^")][-4:]
        out.append(f"::error title={cid}::" + "%0A".join(tail).replace("::", ": :"))
    return out


NOT_STARTED = "run.py: not started: the run reached its --deadline (T-1809)\n"


def run_one(cid, k, timeout=480, deadline=None):
    """T-1808: a class still running after timeout s is killed and fails by name, with every thread's stack
    (faulthandler on SIGABRT); its own session, so a child holding the pipes dies with it. T-1809: the run's deadline
    (an epoch) shortens that, and a class not started by then fails as NOT_STARTED."""
    t0 = time.time()
    why = f"still running after {timeout}s: killed (T-1808)"
    if deadline is not None:
        if deadline - t0 < 1:  # review: round() of under 0.5 s left would start the class and kill it at once
            return cid, 1, NOT_STARTED, 0, 0.0
        if deadline - t0 < timeout:  # review: said apart from the per-class cap
            timeout = round(deadline - t0)
            why = f"still running at the run's deadline ({timeout}s in): killed (T-1809)"
    extra = [a for x in k for a in ("-k", x)]
    p = subprocess.Popen([sys.executable, "-X", "faulthandler", "-m", "unittest", "-q", cid, *extra], cwd=HERE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL,
                         start_new_session=True)
    try:
        _, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.send_signal(signal.SIGABRT)  # the stack, to stderr
        try:
            p.wait(5)
        except subprocess.TimeoutExpired:
            pass
        with contextlib.suppress(ProcessLookupError):
            os.killpg(p.pid, signal.SIGKILL)
        _, err = p.communicate()
        err += f"\nrun.py: {cid} {why}\n"
    m = re.search(r"Ran (\d+) tests?", err)
    return cid, p.returncode, err, int(m.group(1)) if m else 0, time.time() - t0  # killed: negative


def slowest(results, n):
    return ", ".join(f"{c.split('.')[-1]} {s:.0f}s" for c, _, _, _, s in sorted(results, key=lambda r: -r[4])[:n])


def summary_notes(results, elapsed, deadline):
    """T-1809: the run's time and five slowest classes as a public ::notice, a ::warning past 75% of the deadline,
    and one ::error for the classes the deadline left unstarted."""
    notes = [f"::notice title=run.py::Ran {sum(r[3] for r in results)} tests in {elapsed:.0f}s; "
             f"slowest: {slowest(results, 5)}"]
    if deadline and elapsed > 0.75 * deadline:
        notes.append(f"::warning title=run.py::the suite took {elapsed:.0f}s, {100 * elapsed / deadline:.0f}% of its "
                     f"{deadline}s deadline: speed up the slowest classes or raise the job's timeout")
    unstarted = sum(r[2] == NOT_STARTED for r in results)
    if unstarted:
        notes.append(f"::error title=run.py::{unstarted} classes never started: the run reached its {deadline}s deadline")
    return notes


@contextlib.contextmanager
def burn(n):
    """T-1730: n busy-loop children for the block's duration (a load flake on demand), killed after; each also stops
    by itself once its parent is gone (a run killed with SIGKILL leaves no spinner behind)."""
    procs, spin = [], f"import os\nwhile os.getppid() == {os.getpid()}: pass"
    try:
        for _ in range(max(0, n)):
            procs.append(subprocess.Popen([sys.executable, "-c", spin], stdin=subprocess.DEVNULL))
        yield procs
    finally:
        for p in procs:
            p.kill()
        for p in procs:
            p.wait()


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("-j", type=int, default=os.cpu_count() or 4)
    ap.add_argument("-k", action="append", default=[], help="only tests whose id contains this (repeatable)")
    ap.add_argument("-p", action="append", help="module glob, as unittest discover's -p (repeatable; default "
                                                "test*.py)")  # T-0389: a second -p replaced the first
    ap.add_argument("--load", type=int, default=0, metavar="N",
                    help="run beside N busy-loop processes (T-1730: reproduce a flake that shows only under load)")
    ap.add_argument("--timeout", type=int, default=480, metavar="S",
                    help="kill a test class still running after S seconds and fail it with its stack (T-1808)")
    ap.add_argument("--deadline", type=int, metavar="S",
                    help="end the whole run after S seconds: running classes are killed with their stacks, unstarted "
                         "ones fail (T-1809: set it below a CI job's cap, so the run names what was slow)")
    ap.add_argument("--shard", metavar="K/N",
                    help="run only the Kth of N interleaved slices of the classes (T-1842: CI splits the suite "
                         "across N jobs; biggest-first order keeps the slices even)")
    ap.add_argument("names", nargs="*", help="test module names, each like -k (T-0808: fm check affected's {names})")
    a = ap.parse_intermixed_args(argv)  # names may sit on either side of -k
    if a.deadline is not None and a.deadline < 1:  # review: 0 is falsy and turned the deadline off
        ap.error("--deadline takes a number of seconds, 1 or more")
    if a.shard is not None:
        k, _, n = a.shard.partition("/")
        if not (k.isdigit() and n.isdigit() and 1 <= int(k) <= int(n)):
            ap.error("--shard takes K/N with 1 <= K <= N, like 1/2")
        a.shard = int(k), int(n)
    a.k += a.names
    a.error = ap.error
    return a


def main():
    a = parse()
    ap = a
    if any(re.search(r"\s", k) for k in a.k):  # T-0357: '-k "a or b"' matched nothing and failed only at the end
        ap.error("-k matches a substring of test ids; repeat -k for each pattern (-k test_guard -k test_cli)")
    t0 = time.time()
    hit = set()
    todo = classes(a.p or ["test*.py"], a.k, hit)
    missing = [n for n in a.names if n not in hit]
    if missing:  # T-1287: a name that matches nothing (a test file that doesn't exist) fails, not passes unseen
        sys.stderr.write(f"run.py: no test matches {', '.join(missing)}\n")
        return 1
    if a.shard:
        todo = todo[a.shard[0] - 1::a.shard[1]]
    with burn(a.load), concurrent.futures.ThreadPoolExecutor(max(1, a.j)) as ex:
        end = t0 + a.deadline if a.deadline is not None else None
        results = list(ex.map(lambda c: run_one(c, a.k, a.timeout, end), todo))
    failed = [r for r in results if r[1] != 0]
    ci = os.environ.get("GITHUB_ACTIONS")  # T-1223: a run's log needs a login; its annotations are public
    for cid, _, err, _, _ in failed:
        if err == NOT_STARTED:
            continue  # one line for all of them, below
        sys.stderr.write(f"\n==== {cid}\n{err}")
        if ci:
            print("\n".join(annotations(cid, err)), flush=True)
    late = [r[0] for r in failed if r[2] == NOT_STARTED]
    if late:  # review: outside CI too, which classes the deadline left out
        sys.stderr.write(f"\nrun.py: not started (the run's {a.deadline}s deadline): {', '.join(late)}\n")
    if ci:
        print("\n".join(summary_notes(results, time.time() - t0, a.deadline)), flush=True)
    total = sum(r[3] for r in results)
    slow = slowest(results, 3)
    if skipped():
        sys.stderr.write(f"\nleft out (FOREMAN_SKIP_TESTS): {', '.join(sorted(skipped()))}")
    sys.stderr.write(f"\nRan {total} tests in {time.time() - t0:.1f}s ({len(todo)} classes, {a.j} at a time; "
                     f"slowest: {slow})\n\n{'FAILED (' + str(len(failed)) + ' classes)' if failed else 'OK' if total else 'NO TESTS RAN'}\n")
    return 1 if failed or not total else 0


if __name__ == "__main__":
    sys.exit(main())
