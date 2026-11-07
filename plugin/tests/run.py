#!/usr/bin/env python3
"""The test suite across the cores (T-0133): the tests `unittest discover` finds, one test class per process (each
test already gets its own FOREMAN_HOME and repo), so the gate waits for the slowest class instead of the sum of all.
Exit 1 on any failure, with each failing class's report.

  python3 plugin/tests/run.py [-j N] [-k PATTERN] [-p GLOB] [--load N] [NAME ...]
"""
import argparse
import concurrent.futures
import contextlib
import hashlib
import json
import math
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

try:
    import fcntl
except ImportError:  # Windows: no flock, so no slot pool; classes run as before
    fcntl = None

HERE = os.path.dirname(os.path.abspath(__file__))


def child_env(tmp):
    """A class's environment: its own TMPDIR, and local models hidden as on CI unless the caller set the switch
    (T-3229: the moons tests leaned on this box's Ollama embedders, passed here and failed on every CI run)."""
    return dict(os.environ, TMPDIR=tmp, FOREMAN_NO_LOCAL_MODELS=os.environ.get("FOREMAN_NO_LOCAL_MODELS", "1"))


SLOT_ENV = "SAMPO_SLOT"  # T-3252: set in a class's children, so a run.py inside a slot never waits on its parent's pool
CGROUP_ROOT = "/sys/fs/cgroup"


def _env(name):
    """T-3442: SAMPO_X, or FOREMAN_X once importing sampo renamed it (core.mirror_env), as in every test process."""
    return os.environ.get(name) or os.environ.get("FOREMAN_" + name[len("SAMPO_"):])


def _cgroup_dir():
    """This process's cgroup v2 folder, or None."""
    try:
        with open("/proc/self/cgroup") as f:
            rel = next((ln.split("::", 1)[1].strip() for ln in f if ln.startswith("0::")), None)
    except OSError:
        return None
    return os.path.join(CGROUP_ROOT, rel.lstrip("/")) if rel else None


def slot_count():
    """T-3252: the CPUs every run.py on the machine shares: SAMPO_SLOTS, else the CPU count cut to the tightest cgroup
    quota above this process (sampo cpu cap 50 on 16 CPUs gives 8)."""
    try:
        return max(0, int(_env("SAMPO_SLOTS")))
    except (TypeError, ValueError):
        pass
    n, d = os.cpu_count() or 4, _cgroup_dir()
    while d and os.path.realpath(d).startswith(os.path.realpath(CGROUP_ROOT)):
        try:
            with open(os.path.join(d, "cpu.max")) as f:
                quota, period = f.read().split()[:2]
            if quota != "max":
                n = min(n, max(1, math.ceil(int(quota) / int(period))))
        except (OSError, ValueError):
            pass
        if os.path.realpath(d) == os.path.realpath(CGROUP_ROOT):
            break
        d = os.path.dirname(d)
    return n


@contextlib.contextmanager
def cpu_slot(wait=3600.0, poll=0.05):
    """T-3252: one of the machine's CPU slots, shared by every run.py on it (mine, each builder's, the ship's, the
    post-merge verify), held while the block runs: its number, or None when nested, off (SAMPO_SLOTS=0) or the wait ran
    out (the class then runs anyway: a slow run beats a hung one). A slot is a lock file, so the kernel frees it when
    its holder dies and a crashed runner leaks nothing."""
    n = slot_count()
    folder = _slot_folder() if n and not _env(SLOT_ENV) and fcntl else None
    if not folder:  # nested, off, no flock (Windows) or a folder that isn't safely ours: run without one
        yield None
        return
    end, order = time.monotonic() + wait, random.sample(range(n), n)
    while True:
        for i in order:
            try:
                fd = os.open(os.path.join(folder, str(i)), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
            except OSError:
                continue
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                os.close(fd)
                continue
            try:
                yield i
            finally:
                os.close(fd)  # closing it frees the slot
            return
        if time.monotonic() >= end:
            yield None
            return
        time.sleep(poll * random.uniform(1, 5))  # spread the retries of many waiters


def _slot_folder():
    """The pool's folder, made if missing: None unless it's a real folder of mine that nobody else may write (a
    squatted /tmp path or an unwritable XDG_RUNTIME_DIR runs the class without a slot)."""
    uid = getattr(os, "getuid", lambda: 0)()
    folder = os.path.join(os.environ.get("XDG_RUNTIME_DIR") or tempfile.gettempdir(), f"sampo-slots-{uid}")
    try:
        os.makedirs(folder, mode=0o700, exist_ok=True)
        st = os.lstat(folder)
    except OSError:
        return None
    import stat
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != uid or st.st_mode & 0o022:
        return None
    return folder


SUITE_ENV = "SAMPO_NO_SUITE_SLOT"  # T-3541: =1 runs a full suite without the machine-wide slot


def _holder(fd):
    """Who holds the suite slot, from what it wrote into the lock file."""
    try:
        h = json.loads(os.pread(fd, 4096, 0))
        return f"the full suite running in {h['cwd']} (pid {int(h['pid'])}, {(time.time() - float(h['at'])) // 60:.0f} min)"
    except (OSError, ValueError, TypeError, KeyError):  # not written yet, or garbled
        return "another full suite"


@contextlib.contextmanager
def suite_slot(until):
    """T-3541: the machine's one full-suite slot, held while the block runs: three full suites at once (two builders'
    and the ship's) each took 3x as long and slowed everything else. A second full run waits, saying for whom every
    minute, and goes ahead beside the holder once until (an epoch) passes. None when nested in a class (SAMPO_SLOT),
    SAMPO_NO_SUITE_SLOT=1 or no flock. The holder's pid, cwd and start are in the lock file; the kernel frees the lock
    when the holder dies."""
    fd = None
    if not (_env(SLOT_ENV) or _env(SUITE_ENV) or not fcntl):
        path = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "sampo", "suite.lock")
        with contextlib.suppress(OSError):
            os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
            fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    said = 0.0
    try:
        while fd is not None:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                pass
            else:
                with contextlib.suppress(OSError):
                    os.ftruncate(fd, 0)
                    os.pwrite(fd, json.dumps({"pid": os.getpid(), "cwd": os.getcwd(), "at": time.time()}).encode(), 0)
                break
            now = time.time()
            if now >= until:
                sys.stderr.write(f"run.py: {_holder(fd)} still holds the slot; going ahead beside it\n")
                break
            if now - said >= 60:
                sys.stderr.write(f"run.py: waiting for {_holder(fd)}\n")
                sys.stderr.flush()
                said = now
            time.sleep(0.2)  # the next suite starts within 0.2 s of the slot freeing
        yield
    finally:
        if fd is not None:
            os.close(fd)  # closing it frees the slot


def skipped():
    """T-1101: the modules FOREMAN_SKIP_TESTS names (fm check: another open task's red-first test files)."""
    return {x.strip() for x in os.environ.get("FOREMAN_SKIP_TESTS", "").split(",") if x.strip()}


SPLIT_S = 5.0  # T-3166: a class whose last run took this long runs a job per test
START_S = 0.3  # ... what each job's interpreter start-up costs, left out of a split class's work time
# Classes seen slow (tonight's measurements): split with no times yet (a first run, a --shard), where every other class
# stays one job (an interpreter per test of 1400 classes would swamp a 2-core runner).
SEEDED = {"LeanKind", "Stop", "ExamAuthors", "ExamGen", "Page", "ClockWindows", "PreToolUse", "SessionStart",
          "Worker", "GenesisRead"}


def keeps_whole(t):
    """T-3166: a class with setUpClass/tearDownClass, a module with setUpModule/tearDownModule, a module that won't
    import, or a class marked `run_whole = True` shares state between its tests: one job."""
    c, tc = type(t), unittest.TestCase
    m = sys.modules.get(c.__module__)
    own = lambda n: getattr(getattr(c, n, None), "__func__", None) is not getattr(tc, n).__func__  # noqa: E731  (None: whole)
    return (isinstance(t, unittest.loader._FailedTest) or getattr(c, "run_whole", False)
            or own("setUpClass") or own("tearDownClass")
            or any(hasattr(m, n) for n in ("setUpModule", "tearDownModule")))


def times_path():
    return os.environ.get("FM_TEST_TIMES") or os.path.join(
        tempfile.gettempdir(), f"fmtest-times-{getattr(os, 'getuid', lambda: 0)()}-{hashlib.sha1(HERE.encode()).hexdigest()[:10]}.json")


def load_times():
    """T-3166: seconds each job took the last time it ran ({job id: s}); {} when there is none yet."""
    try:
        with open(times_path()) as f:
            if os.fstat(f.fileno()).st_uid != getattr(os, "getuid", lambda: 0)():  # someone else's file in a shared /tmp
                return {}
            d = json.load(f)
        return {k: float(v) for k, v in d.items()}
    except Exception:  # OverflowError, RecursionError ...: times only order the jobs
        return {}


def save_times(new):
    """Merged into the file's, so a run of a few modules keeps the rest's; capped, newest kept."""
    d = load_times()
    for k, v in new.items():
        d.pop(k, None)
        d[k] = round(v, 2)
    d = dict(list(d.items())[-20000:])
    p = f"{times_path()}.{os.getpid()}"
    try:
        with contextlib.suppress(OSError):
            os.unlink(p)  # a stale or planted one: O_EXCL below then never follows a symlink
        with os.fdopen(os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600), "w") as f:
            json.dump(d, f)
        os.replace(p, times_path())  # atomic: a run beside this one reads the old file or the new, never half
    except OSError:
        pass  # times only order the jobs


def work_time(secs):
    """A split class's work: its tests' seconds less each one's start-up, so it stays split only while it is slow."""
    return round(max(0.0, sum(secs) - START_S * len(secs)), 2)


def plan(todo, parts, whole, times):
    """T-3166: the jobs for these classes, longest first. A class that may be split (not in whole) is, once its work
    took SPLIT_S or more last time (or, never timed, when SEEDED names it): its tests become jobs."""
    jobs = []
    for cid in todo:
        ids = parts.get(cid, [])
        split = cid not in whole and len(ids) > 1 and (times[cid] >= SPLIT_S if cid in times else cid.rsplit(".", 1)[-1] in SEEDED)
        jobs += ids if split else [cid]

    def est(j):
        if j in times:
            return times[j]
        if j in parts:  # a whole class never timed: half a second a test
            return 0.5 * len(parts[j])
        c = j.rsplit(".", 1)[0]  # a test never timed: its class's average
        return times[c] / len(parts[c]) if c in times and c in parts else 0.5
    return sorted(jobs, key=lambda j: -est(j))  # stable: ties keep the biggest-class-first order


def classes(patterns, k, hit=None, names=(), ids=None, parts=None, whole=None):
    """Every test class id (module.Class) discover would run, biggest first so the long ones start early; hit (a set)
    gets each -k pattern or name that matched a test. T-1994: with names and -k both, a test matches one of each.
    ids (a list) gets every test id walked, before any filter. T-3166: parts (a dict) gets each class's matching
    test ids, and whole (a set) the classes that keeps_whole."""
    sys.path.insert(0, HERE)
    counts, skip, hit = {}, skipped(), set() if hit is None else hit

    def walk(suite):
        for t in suite:
            if isinstance(t, unittest.TestSuite):
                walk(t)
                continue
            if skip and (t.id().rsplit(".", 1)[-1] if type(t).__name__ == "_FailedTest"  # a module that won't import
                           else type(t).__module__) in skip:
                continue
            if ids is not None:
                ids.append(t.id())
            if (not k or any(x in t.id() for x in k)) and (not names or any(x in t.id() for x in names)):
                hit.update(x for x in (*k, *names) if x in t.id())
                cid = f"{type(t).__module__}.{type(t).__name__}"
                counts[cid] = counts.get(cid, 0) + 1
                if parts is not None and t.id() not in parts.setdefault(cid, []):  # an imported TestCase is walked twice
                    parts[cid].append(t.id())
                if whole is not None and keeps_whole(t):
                    whole.add(cid)
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
        out.append(f"::error title={cid}.{name}::" + "%0A".join(x[:250] for x in body).replace("::", ": :"))
    if not out:  # T-1911: lines cut to 250, and a class that wrote nothing says so (an empty message isn't shown)
        tail = [x.strip()[:120] for x in err.splitlines() if x.strip() and not set(x.strip()) <= set("-=~^")][-4:]
        out.append(f"::error title={cid}::" + ("%0A".join(tail) or "no output").replace("::", ": :"))
    return out


NOT_STARTED = "run.py: not started: the run reached its --deadline (T-1809)\n"
TMP_PREFIX = "fmtest-"  # not fm-: fm tidy reads ~/.claude/projects/-tmp-fm-* as its own claude -p runs' folders


# T-2034: a class dies with run.py, even a SIGKILLed one (a Bash timeout): its own session kept it alive, and one
# orphan spun a core for a day. Like -m unittest after that; off Linux the prctl is a no-op.
BOOT = ("import ctypes, os, signal, sys, unittest\n"
        "try:\n    ctypes.CDLL(None).prctl(1, signal.SIGKILL)  # PR_SET_PDEATHSIG\nexcept Exception:\n    pass\n"
        "if sys.argv[1] != '0' and os.getppid() != int(sys.argv[1]):\n    os._exit(1)  # run.py was gone before the prctl\n"
        "unittest.main(module=None, argv=['python -m unittest', *sys.argv[2:]])\n")


SANDBOX = []  # T-3222: run.py --sandbox, once its job sandbox is known to work here


def sandboxed(argv, tmp, env):
    """T-3222: argv and env for a class in Sampo's job sandbox: the repo read-only, only its own temp folder
    writable, no network, credential folders empty, secret variables gone."""
    lib = os.path.join(os.path.dirname(HERE), "lib")
    if lib not in sys.path:
        sys.path.insert(0, lib)
    from sampo import sandbox
    repo = os.path.dirname(os.path.dirname(HERE))  # T-3246: readable even under /tmp (sampo ship's scratch tree)
    return (sandbox.argv(argv, tmp, cwd=HERE, nest=True, reads=[repo]),  # nest: tests that run bwrap themselves
            sandbox.job_env(env, tmp))


def run_one(cid, k, timeout=480, deadline=None):
    """T-3252: the class runs in one of the machine's CPU slots; waiting for it counts against neither its timeout nor
    its recorded time, and the run's deadline still applies once it starts."""
    wait = max(0.0, deadline - time.time()) if deadline is not None else 3600.0
    with cpu_slot(wait) as slot:
        return _run_one(cid, k, timeout, deadline, slot)


def _run_one(cid, k, timeout, deadline, slot):
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
    try:
        tmp = tempfile.mkdtemp(prefix=f"{TMP_PREFIX}{os.getpid()}-")  # T-2019: whatever the class leaks goes with it
    except OSError as e:  # T-3236: /tmp out of space or inodes fails this class by name, not the whole run
        return cid, 1, f"run.py: couldn't make the class's temp folder: {e}\n", 0, 0.0
    argv, env =[sys.executable, "-X", "faulthandler", "-c", BOOT, "0" if SANDBOX else str(os.getpid()), "-q", cid,
                 *extra], child_env(tmp)
    env[SLOT_ENV] = "none" if slot is None else str(slot)  # T-3442: with no slot too, its runs never queue again
    if SANDBOX:  # its own pid namespace: it dies with bwrap (--die-with-parent), not by a parent pid check
        argv, env = sandboxed(argv, tmp, env)
    p = subprocess.Popen(argv, cwd=HERE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL,
                         start_new_session=True, env=env)
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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    m = re.search(r"Ran (\d+) tests?", err)
    return cid, p.returncode, err, int(m.group(1)) if m else 0, time.time() - t0  # killed: negative


def sweep(base=None):
    """T-2019: a run killed before its cleanup leaves its classes' temp dirs; the next run removes dead runs' ones."""
    base = base or tempfile.gettempdir()
    for name in os.listdir(base):
        m = re.match(rf"{TMP_PREFIX}(\d+)-", name)
        if not m:
            continue
        try:
            os.kill(int(m.group(1)), 0)
        except ProcessLookupError:
            shutil.rmtree(os.path.join(base, name), ignore_errors=True)
        except PermissionError:
            pass  # alive, someone else's


def slowest(results, n):
    return ", ".join(f"{'.'.join(c.split('.')[1:][-2:])} {s:.0f}s" for c, _, _, _, s in sorted(results, key=lambda r: -r[4])[:n])


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
    broke = [f"{r[0]} (exit {r[1]})" for r in results if r[1] != 0 and r[2] != NOT_STARTED]
    if broke:  # T-1911: one line naming them all, should a class's own annotations go missing
        notes.append(f"::error title=run.py::{len(broke)} classes failed: {', '.join(broke)}"[:1000])
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


def load_room(n, cpus=None, load=None, spinners=None):
    """T-3441: how many of --load's n busy loops fit under twice the CPU count, given the 1-minute load and the burn
    spinners already running (counted from /proc: the average lags a run started seconds ago)."""
    cpus = cpus or os.cpu_count() or 4
    if load is None:
        load = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
    if spinners is None:
        spinners = 0
        for pid in os.listdir("/proc") if os.path.isdir("/proc") else ():
            try:
                with open(f"/proc/{pid}/cmdline", "rb") as f:
                    spinners += b"while os.getppid() == " in f.read()
            except OSError:
                continue
    return max(0, min(n, int(2 * cpus - max(load, spinners))))


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("-j", type=int, default=slot_count() or os.cpu_count() or 4)  # T-3252: the pool
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
    ap.add_argument("--sandbox", action="store_true", help="run each class in Sampo's job sandbox (T-3222): the repo "
                    "read-only, only its own temp folder writable, no network; plain, with a note, where it can't run")
    ap.add_argument("names", nargs="*", help="test module names (T-0808: fm check affected's {names}); with -k, only "
                                             "their tests that match a -k (T-1994)")
    a = ap.parse_intermixed_args(argv)  # names may sit on either side of -k
    for i, n in enumerate(a.names):  # T-3428: a path into the tests dir names its module
        if "/" in n or n.endswith(".py"):
            d, f = os.path.split(n)
            if not (f.startswith("test") and f.endswith(".py") and (not d or os.path.realpath(d) == os.path.realpath(HERE))):
                ap.error(f"{n}: not a test name or a test_*.py file in {HERE}")
            a.names[i] = f[:-3]
    if a.deadline is not None and a.deadline < 1:  # review: 0 is falsy and turned the deadline off
        ap.error("--deadline takes a number of seconds, 1 or more")
    if a.shard is not None:
        k, _, n = a.shard.partition("/")
        if not (k.isdigit() and n.isdigit() and 1 <= int(k) <= int(n)):
            ap.error("--shard takes K/N with 1 <= K <= N, like 1/2")
        a.shard = int(k), int(n)
    a.error = ap.error
    return a


def main():
    try:  # T-3503: a worker killed with SIGABRT must not leave a core dump; children inherit the limit
        import resource
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, ValueError, OSError):
        pass
    a = parse()
    ap = a
    if any(re.search(r"\s", k) for k in a.k + a.names):  # T-0357: '-k "a or b"' matched nothing and failed only at the end
        ap.error("-k matches a substring of test ids; repeat -k for each pattern (-k test_guard -k test_cli)")
    if a.sandbox:
        lib = os.path.join(os.path.dirname(HERE), "lib")
        sys.path.insert(0, lib)
        from sampo import sandbox
        ok, why = sandbox.available()
        if ok:
            SANDBOX.append(why)
        else:
            sys.stderr.write(f"run.py: --sandbox: not available here ({why}); running plain\n")
    t0 = time.time()
    sweep()
    hit, ids = set(), []
    parts, whole = {}, set()
    todo = classes(a.p or ["test*.py"], a.k, hit, a.names, ids, parts, whole)
    missing = [n for n in a.names if n not in hit]
    if missing:  # T-1287: a name that matches nothing (a test file that doesn't exist) fails, not passes unseen
        fold = lambda s: s.lower().replace("_", "")  # noqa: E731
        near = dict.fromkeys(seg for i in ids if any(n in i for n in missing) for seg in i.split(".")
                             if any(fold(x) in fold(seg) for x in a.k))  # T-2003: -k core_integrity meant CoreIntegrity
        sys.stderr.write(f"run.py: no test matches {', '.join(missing)}"  # T-1999: say what filtered it out
                         + (f" with -k {' -k '.join(a.k)}" if a.k else "")
                         + (f"; did you mean {' or '.join('-k ' + s for s in list(near)[:3])}?" if near else "") + "\n")
        return 1
    if a.shard:
        todo = todo[a.shard[0] - 1::a.shard[1]]
    times = {} if a.shard else load_times()  # a shard's slice must not depend on this machine's last run
    todo = plan(todo, parts, whole, times)  # T-3166: jobs, a big class's tests apart
    if a.load and (room := load_room(a.load)) < a.load:
        sys.stderr.write(f"run.py: --load {a.load} cut to {room}: the host already runs near twice its CPU count\n")
        a.load = room
    try:
        import helpers  # T-3338: lazily, after classes() put the tests folder on sys.path
        busy = helpers.busy_factor()
    except ImportError:  # a copy of run.py alone (test_check_paths) has no helpers
        busy = 1
    cap = round(a.timeout * busy)  # a loaded host's class runs slower; the deadline still clamps
    # T-3338 review: --deadline, else the gate's (core.run_command sets FM_RUN_DEADLINE under its own timeout), else
    # 8 class timers: the scaled timers never outlast the caller's, so a kill names the class
    dl = a.deadline if a.deadline is not None else int(os.environ.get("FM_RUN_DEADLINE") or 0) or max(8 * cap, 600)
    a.deadline, end = dl, t0 + dl
    # T-3541: the whole suite (the gate: no names, -k or -p) waits for any other on the machine, at most half its deadline
    slot = suite_slot(t0 + dl / 2) if not (a.names or a.k or a.p) else contextlib.nullcontext()
    with slot, burn(a.load), concurrent.futures.ThreadPoolExecutor(max(1, a.j)) as ex:
        results = list(ex.map(lambda c: run_one(c, a.k or a.names, cap, end), todo))  # T-1994: the class is in a named module, so -k alone
    if not a.shard:
        seen = set(ids)
        # T-3338: a killed class (negative rc) counts as slow, so the next run splits it instead of killing it again
        timer = lambda r: r[1] < 0 and "killed (T-1808)" in r[2]  # noqa: E731  # not a deadline kill or a SIGKILL
        new = {r[0]: max(r[4], SPLIT_S) if timer(r) else r[4]
               for r in results if (r[1] >= 0 or timer(r)) and r[2] != NOT_STARTED and r[0] in seen | set(parts)}
        for cid, js in parts.items():  # a split class's work, so the next run still knows if it is slow
            if js and all(j in new for j in js):
                new[cid] = work_time([new[j] for j in js])
        if a.k:  # a -k run ran part of each class: its time is no class's
            new = {j: s for j, s in new.items() if j not in parts}
        if new:
            save_times(new)
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
    names = [r[0] for r in failed]  # T-2319: the last line says which classes, since tails cut the ==== blocks above
    said = ", ".join(names[:5]) + (f", +{len(names) - 5} more" if len(names) > 5 else "")
    sys.stderr.write("".join(f"\n  failed class: {n}" for n in names) + ("\n" if names else ""))  # T-3397: all of them, one per line
    sys.stderr.write(f"\nRan {total} tests in {time.time() - t0:.1f}s ({len(todo)} jobs, {a.j} at a time; "
                     f"slowest: {slow})\n\n{f'FAILED ({len(failed)} classes: {said})' if failed else 'OK' if total else 'NO TESTS RAN'}\n")
    # T-2944: stopped at its own deadline with nothing really failed: exit 124 and say so last, so a caller (the
    # sentinel's re-verify) reads a busy machine, not a regression
    stopped = [r for r in failed if r[2] == NOT_STARTED or "the run's deadline" in r[2]]
    if stopped and len(stopped) == len(failed):
        sys.stderr.write("run.py: stopped at its deadline\n")
        return 124
    return 1 if failed or not total else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # T-1911: a crash after the notes was a bare exit 1 in CI
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"::error title=run.py::run.py crashed: {e!r}"[:1000], flush=True)
        raise
