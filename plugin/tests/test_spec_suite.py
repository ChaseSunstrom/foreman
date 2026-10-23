"""Spec suite round 3 (T-1377): tasks no change can do prove themselves impossible, every attempt failing."""
import os
import subprocess
import sys
import unittest

MAKE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "bench", "spec-suite", "make.py")


class ImpossibleRound(unittest.TestCase):
    def test_every_attempt_at_every_task_fails(self):
        r = subprocess.run([sys.executable, MAKE, "--check", "--suite", "impossible"], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=300)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-1000:])
        self.assertIn("spec suite (impossible): 3 tasks, each one no attempt passes", r.stdout)
        for name in ("caseslug", "rates", "vault", "base tests", "reproducible"):
            self.assertRegex(r.stdout, rf"(?m)^ok\s+{name}\b")


if __name__ == "__main__":
    unittest.main()
