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
        env = dict(os.environ, FOREMAN_STATE="/tmp/fm-demo-state", FOREMAN_SESSION_ID="x")
        p = subprocess.run([sys.executable, SHOT, "selftest"], env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
