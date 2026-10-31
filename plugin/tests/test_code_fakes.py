"""T-1361: every misbehaving fake runner (helpers.fake_cli) ends an fm code run within its bound and names the reason."""
import os
import time
import unittest

from helpers import FAKE_MODES, fake_cli
from test_code import CodeCase

VERIFY = "python3 test_calc.py"
BOUND = 40  # s: the fakes sleep 60; the step turn and 3 fix rounds stop at --worker-timeout 2 each (~10 s, more on a loaded host); a run past this hung


class Fakes(CodeCase):
    def run_fake(self, mode):
        bin_ = os.path.join(self.tmp, "bin")
        fake_cli(bin_, "fake", mode, secs=60)
        t0 = time.monotonic()
        r = self.code("FIX: make calc.add add", "--worker", "fake {prompt}", "--verify", VERIFY, "--worker-timeout", "2",
                      check=False, env={"PATH": bin_ + os.pathsep + os.environ["PATH"], "FM_STALL": "0.5", "FM_HEARTBEAT": "0.3"})
        self.assertLess(time.monotonic() - t0, BOUND, f"{mode} hung fm code")  # wall clock: --worker-timeout 2 deadline of a child fm code
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("a - b", self.calc(), "no fake fixed anything")
        return r.stdout + r.stderr

    def test_hang(self):
        out = self.run_fake("hang")
        self.assertIn("timed out after 2 s", out)
        self.assertIn("no output since launch", out)

    def test_silent(self):
        out = self.run_fake("silent")
        self.assertIn("timed out after 2 s", out)
        self.assertIn("silent", out)

    def test_tty_prompt(self):
        out = self.run_fake("tty-prompt")
        self.assertIn("waiting at a prompt", out)
        self.assertIn("timed out after 2 s", out)

    def test_usage_limit(self):
        out = self.run_fake("usage-limit")
        self.assertIn("hit a rate or usage limit", out)
        self.assertIn("timed out after 2 s", out)

    def test_garbage_json(self):
        out = self.run_fake("garbage-json")
        self.assertIn("worker fake: exit 0", out)  # it ended; the verify, not its reply, decided
        self.assertIn("changed nothing", out)

    def test_fork_exit(self):
        out = self.run_fake("fork-exit")
        self.assertIn("worker fake: exit 0", out)
        self.assertIn("changed nothing", out)

    def test_every_mode_is_covered(self):
        covered = {n[5:].replace("_", "-") for n in dir(self) if n.startswith("test_") and n != "test_every_mode_is_covered"}
        self.assertEqual(covered | {"ok"}, set(FAKE_MODES))


if __name__ == "__main__":
    unittest.main()
