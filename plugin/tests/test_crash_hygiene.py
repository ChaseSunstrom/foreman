"""Crash hygiene (T-1405): a hung long verb leaves a stack dump; a stale .git/index.lock left by a crashed git is
removed only when no live git owns the repo; fm doctor probes whether the state filesystem's flock excludes."""
import glob
import os
import shutil
import signal
import subprocess
import sys
import time
import unittest
from unittest import mock

from helpers import FM, ForemanTestCase, read_text
from test_hooks import HookCase

import fmcli
import fmcore as c


def _wait(cond, secs=20):
    end = time.time() + secs
    while time.time() < end:
        if cond():
            return True
        time.sleep(0.05)
    return False


class StackDumps(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.started, self.pid = os.path.join(self.tmp, "started"), os.path.join(self.tmp, "gate.pid")
        self.fm("check", "add", f"echo $$ > {self.pid}; touch {self.started}; exec sleep 30")
        self.stacks = os.path.join(self.home, "state", "logs", "stacks")
        self.procs = []

    def tearDown(self):
        for pr in self.procs:
            pr.kill()
            pr.wait()
        try:
            with open(self.pid) as f:
                os.kill(int(f.read()), signal.SIGKILL)
        except (OSError, ValueError):
            pass
        super().tearDown()

    def hung_check(self, **env):
        e = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1", **env)
        pr = subprocess.Popen([sys.executable, FM, "check"], cwd=self.repo, env=e, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.procs.append(pr)
        self.assertTrue(_wait(lambda: os.path.exists(self.started)), "the gate never started")
        return pr, os.path.join(self.stacks, f"check-{pr.pid}.txt")

    def dumped(self, path):
        return _wait(lambda: os.path.exists(path) and "cmd_check" in read_text(path))

    def test_sigusr1_writes_a_stack_dump(self):
        pr, path = self.hung_check()
        os.kill(pr.pid, signal.SIGUSR1)
        self.assertTrue(self.dumped(path), f"no stack in {path}")
        self.assertIsNone(pr.poll(), "SIGUSR1 must not end the verb")

    def test_a_verb_past_its_timeout_writes_a_stack_dump(self):
        pr, path = self.hung_check(FOREMAN_STACK_AFTER="1")
        self.assertTrue(self.dumped(path), f"no stack in {path}")

    def test_a_run_that_ends_leaves_no_empty_dump(self):
        self.fm("check", "rm", "1")
        self.fm("check", check=False)
        self.assertEqual(glob.glob(os.path.join(self.stacks, "*")), [])

    def test_a_short_verb_installs_nothing(self):
        shutil.rmtree(self.stacks, ignore_errors=True)
        self.fm("state", check=False)
        self.assertFalse(os.path.isdir(self.stacks))


class IndexLock(HookCase):
    def setUp(self):
        super().setUp()
        self.lock = os.path.join(self.repo, ".git", "index.lock")
        self.procs = []

    def tearDown(self):
        for pr in self.procs:
            pr.kill()
            pr.wait()
        super().tearDown()

    def make_lock(self, age):
        open(self.lock, "w").close()
        t = time.time() - age
        os.utime(self.lock, (t, t))

    def live_git(self):
        git = os.path.join(self.tmp, "bin", "git")  # a process whose comm is git, with the repo as its cwd
        os.makedirs(os.path.dirname(git))
        shutil.copy("/bin/sleep", git)
        pr = subprocess.Popen([git, "30"], cwd=self.repo)
        self.procs.append(pr)
        return pr

    @unittest.skipUnless(os.path.isdir("/proc/self"), "the live-git scan reads /proc")
    def test_a_stale_lock_with_no_live_git_is_removed(self):
        self.make_lock(20 * 60)
        removed, why = fmcli._stale_index_lock(self.repo)
        self.assertTrue(removed, why)
        self.assertFalse(os.path.exists(self.lock))
        self.assertIn("removed", why)

    def test_a_fresh_lock_is_kept_and_named(self):
        self.make_lock(30)
        removed, why = fmcli._stale_index_lock(self.repo)
        self.assertFalse(removed)
        self.assertTrue(os.path.exists(self.lock))
        self.assertIn(self.lock, why)

    @unittest.skipUnless(os.path.isdir("/proc/self"), "the live-git scan reads /proc")
    def test_a_stale_lock_with_a_live_git_in_the_repo_is_kept(self):
        pr = self.live_git()
        self.make_lock(20 * 60)
        removed, why = fmcli._stale_index_lock(self.repo)
        self.assertFalse(removed)
        self.assertTrue(os.path.exists(self.lock))
        self.assertIn(self.lock, why)
        self.assertIn(str(pr.pid), why)

    def test_without_proc_it_is_never_removed(self):
        self.make_lock(20 * 60)
        with mock.patch.object(fmcli.os.path, "isdir", lambda d: False if d == "/proc" else os.path.lexists(d)):
            removed, why = fmcli._stale_index_lock(self.repo)
        self.assertFalse(removed)
        self.assertTrue(os.path.exists(self.lock))

    @unittest.skipUnless(os.path.isdir("/proc/self"), "the live-git scan reads /proc")
    def test_finish_commits_past_a_stale_lock_and_logs_it(self):
        self.fm("init")
        self.fm("task", "new", "First", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        path = os.path.join(self.repo, "a.py")
        with open(path, "w") as f:
            f.write("A = 1\n")
        self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": path}, "tool_response": {}})
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "true")
        self.make_lock(20 * 60)
        out = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--commit", "First").stdout
        self.assertIn("committed", out)
        self.assertIn("stale", out)
        self.assertFalse(os.path.exists(self.lock))
        p = c.find_project(self.repo)
        self.assertTrue(any(e.get("event") == "index_lock_removed" for e in c.ledger_tail(p)))


class LockProbe(ForemanTestCase):
    def test_flock_that_excludes_passes(self):
        import fmdoctor
        r = fmdoctor.check_lock_probe(c.state_dir())
        self.assertEqual(r.status, "PASS", r.detail)
        self.assertEqual(glob.glob(os.path.join(c.state_dir(), "*probe*")), [])  # the probe file is gone

    def test_flock_that_does_not_exclude_fails_naming_the_filesystem(self):
        import fmdoctor
        with mock.patch("fcntl.flock"):  # the parent's LOCK_NB "succeeds", as on a filesystem that ignores flock
            r = fmdoctor.check_lock_probe(c.state_dir())
        self.assertEqual(r.status, "FAIL")
        self.assertIn(fmdoctor._fs_type(c.state_dir()), r.detail)

    def test_doctor_reports_it(self):
        out = self.fm("doctor", "-v", check=False).stdout
        self.assertRegex(out, r"PASS\s+lock probe\s+flock excludes")


if __name__ == "__main__":
    unittest.main()
