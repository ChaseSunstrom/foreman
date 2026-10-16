"""The UI snapshot harness (mods/foreman-ui/tools/shot.py) never leaks FOREMAN_* into a tmux server's global
environment, where every later session would inherit it (T-0138: a leaked FOREMAN_STATE pointed the user's own
Claude Code session at the demo state)."""
import os
import shutil
import subprocess
import sys
import unittest

SHOT = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "foreman-ui", "tools", "shot.py")


@unittest.skipUnless(shutil.which("tmux"), "needs tmux")
class Harness(unittest.TestCase):
    def test_foreman_variables_stay_in_the_harness_session(self):
        env = dict(os.environ, FOREMAN_STATE="/tmp/fm-demo-state", FOREMAN_SESSION_ID="x",
                   FM_SHOT_SOCKET=f"fm-shot-test-{os.getpid()}")  # T-0744: two suites at once never share it
        p = subprocess.run([sys.executable, SHOT, "selftest"], env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_watch_refuses_outside_tmux_and_stops_on_time(self):
        # T-0143: 'add a hook to screenshot every few seconds'; run detached, it must never outlive --for
        env = {k: v for k, v in os.environ.items() if k not in ("TMUX", "TMUX_PANE")}
        p = subprocess.run([sys.executable, SHOT, "watch", os.devnull, "--every", "1", "--for", "0"], env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("not inside tmux", p.stderr)


class OneOff(unittest.TestCase):
    def test_a_session_with_its_own_state_is_a_working_session(self):
        # T-1013: the demo recorder runs its session on a state of its own; marked one-off (T-0995) it was never driven
        # to close its task, and the recording timed out with nothing written
        import argparse
        import importlib.util
        spec = importlib.util.spec_from_file_location("shot_t1013", SHOT)
        shot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(shot)
        seen = []
        shot.tmux = lambda *args, check=True: seen.append(args)
        a = argparse.Namespace(dir=".", cols=10, rows=5, model=None)
        saved = os.environ.pop("FOREMAN_STATE", None)
        try:
            shot.start(a, cmd="true")  # the user's own state: a one-off, never driven
            shared = " ".join(seen[-1])
            os.environ["FOREMAN_STATE"] = "/tmp/fm-demo-state"
            shot.start(a, cmd="true")
            own = " ".join(seen[-1])
        finally:
            os.environ.pop("FOREMAN_STATE", None)
            if saved is not None:
                os.environ["FOREMAN_STATE"] = saved
        self.assertIn("FOREMAN_ONEOFF=1", shared)
        self.assertNotIn("FOREMAN_STATE=", shared)
        self.assertIn("FOREMAN_STATE=/tmp/fm-demo-state", own)
        self.assertNotIn("FOREMAN_ONEOFF", own)

