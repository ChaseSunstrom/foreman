"""The claude -p helpers' reaper (T-1044): every child runs in its own process group, so a timeout kills its
grandchildren too; each is registered in state/children/<pid>, and SessionStart sweeps the ones a dead run left
behind — only when the pid is still the same process (its start time) running a helper (its command line)."""
import os
import signal
import subprocess
import time
from unittest import mock

from helpers import ForemanTestCase

# a helper that starts a grandchild, says where it is, and waits on it (the grandchild off the pipes, so a runner that
# kills only the leader still returns, and the test fails instead of hanging for the sleep)
STUB = '#!/bin/sh\nsleep 300 </dev/null >/dev/null 2>&1 &\necho $! > "$STUB_PIDFILE"\nwait\n'


def gone(pid, wait=5):
    """The pid has exited (a zombie waiting on init counts) within `wait` seconds."""
    end = time.time() + wait
    while time.time() < end:
        try:
            with open(f"/proc/{pid}/stat") as f:
                if f.read().rsplit(")", 1)[1].split()[0] == "Z":
                    return True
        except OSError:
            return True
        time.sleep(0.05)
    return False


class _Stubbed(ForemanTestCase):
    def setUp(self):
        super().setUp()
        import fmcore as c
        import fmideas
        self.c, self.fmideas = c, fmideas
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        self.stub = os.path.join(bindir, "claude")
        with open(self.stub, "w") as f:
            f.write(STUB)
        os.chmod(self.stub, 0o755)
        self.pidfile = os.path.join(self.tmp, "grandchild.pid")
        env = mock.patch.dict(os.environ, {"PATH": bindir + os.pathsep + os.environ["PATH"],
                                           "STUB_PIDFILE": self.pidfile})
        env.start()
        self.addCleanup(env.stop)
        self.fm("init")
        self.reg = os.path.join(c.state_dir(), "children")

    def grandchild_reaped(self):
        """The stub's grandchild exited; one that didn't is killed here, so a failing test leaves no sleep behind."""
        for _ in range(100):
            try:
                with open(self.pidfile) as f:
                    pid = int(f.read())
                break
            except (OSError, ValueError):
                time.sleep(0.05)
        else:
            self.fail("the stub never started its grandchild")
        if gone(pid):
            return True
        os.kill(pid, signal.SIGKILL)
        return False

    def entries(self):
        return sorted(os.listdir(self.reg)) if os.path.isdir(self.reg) else []


class Timeout(_Stubbed):
    def test_run_child_kills_the_whole_group(self):
        with self.assertRaises(ValueError) as e:
            self.fmideas.run_child("ideas", "sys", "a prompt", "haiku", 1)
        self.assertIn("timed out", str(e.exception))
        self.assertTrue(self.grandchild_reaped(), "the grandchild outlived the timeout")
        self.assertEqual(self.entries(), [], "the reaped child left its registry entry")

    def test_run_children_kills_every_group(self):
        out = self.fmideas.run_children([([self.stub, "-p"], "a prompt", "lens")], 1, "ideas")
        self.assertEqual(out, [(None, "timed out after 1s")])
        self.assertTrue(self.grandchild_reaped(), "the grandchild outlived the timeout")
        self.assertEqual(self.entries(), [])

    def test_a_child_that_finishes_leaves_no_entry(self):
        with open(self.stub, "w") as f:
            f.write('#!/bin/sh\ncat >/dev/null\necho \'{"result": "ok", "total_cost_usd": 0.01}\'\n')
        self.assertEqual(self.fmideas.run_child("ideas", "sys", "a prompt", "haiku", 30), "ok")
        self.assertEqual(self.fmideas.run_children([([self.stub, "-p"], "a prompt", "lens")], 30, "ideas"),
                         [("ok", None)])
        self.assertEqual(self.entries(), [])


class Sweep(_Stubbed):
    def setUp(self):
        super().setUp()
        self.procs = []

    def tearDown(self):
        for pr in self.procs:  # the groups, before the wait (the pid is still ours) and before tmp goes
            if pr.poll() is None:
                os.killpg(pr.pid, signal.SIGKILL)
            pr.wait()
        super().tearDown()

    def helper(self, argv=None, start=None, age=4000):
        """A helper started by a run that then died: registered, its entry aged (and its start time forged)."""
        pr = self.fmideas._popen(argv or [self.stub, "-p", "--no-session-persistence"], 1, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.procs.append(pr)
        path = os.path.join(self.reg, str(pr.pid))
        with open(path) as f:
            st, _, timeout = f.read().split()
        with open(path, "w") as f:
            f.write(f"{start or st} {time.time() - age:.0f} {timeout}")
        return pr

    def test_a_stale_helper_is_killed_with_its_group(self):
        pr = self.helper()
        for _ in range(100):  # the stub has started its grandchild
            if os.path.exists(self.pidfile):
                break
            time.sleep(0.05)
        self.assertEqual(self.fmideas.sweep_orphans(), 1)
        self.assertEqual(pr.wait(5), -signal.SIGKILL)
        self.assertTrue(self.grandchild_reaped())
        self.assertEqual(self.entries(), [])

    def test_a_reused_pid_a_stranger_and_a_fresh_helper_are_left_alone(self):
        reused = self.helper(start="1")  # the pid now belongs to another process: its start time differs
        stranger = self.helper(argv=["sleep", "300"])  # the same process, but not a helper's command line
        fresh = self.helper(age=0)
        self.assertEqual(self.fmideas.sweep_orphans(), 0)
        for pr in (reused, stranger, fresh):
            self.assertIsNone(pr.poll(), pr.args)
        self.assertEqual(self.entries(), [str(fresh.pid)], "a stale entry is dropped, a fresh one kept")

    def test_garbage_and_no_registry_are_harmless(self):
        self.assertEqual(self.fmideas.sweep_orphans(), 0)  # no folder yet
        os.makedirs(self.reg, exist_ok=True)
        for name, body in (("notapid", "1 2 3"), ("999999999", "garbled")):
            with open(os.path.join(self.reg, name), "w") as f:
                f.write(body)
        self.assertEqual(self.fmideas.sweep_orphans(), 0)
        self.assertEqual(self.entries(), [])


class Hook(_Stubbed):
    def session_start(self, background):
        import fmhooks
        with mock.patch.dict(os.environ, {"FOREMAN_NO_BACKGROUND": background}), \
                mock.patch("subprocess.Popen"), \
                mock.patch.object(self.fmideas, "sweep_orphans", side_effect=RuntimeError("sweep boom")) as sweep:
            out = fmhooks.session_start({"source": "compact", "session_id": "s-1", "cwd": self.repo})
        return out, sweep

    def test_session_start_sweeps_and_survives_a_sweep_error(self):
        out, sweep = self.session_start("")
        sweep.assert_called_once()
        self.assertIn("additionalContext", out["hookSpecificOutput"])
        with open(os.path.join(self.c.state_dir(), "logs", "hooks.log")) as f:
            self.assertIn("sweep boom", f.read())

    def test_a_background_free_child_never_sweeps(self):
        out, sweep = self.session_start("1")
        sweep.assert_not_called()
        self.assertIn("additionalContext", out["hookSpecificOutput"])
