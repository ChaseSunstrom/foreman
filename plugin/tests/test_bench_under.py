"""T-2651: fm task evidence --bench CMD --under MS is a pass/fail proof on the current tree's median."""
import json

from test_evidence_quality import Bench


class BenchUnder(Bench):
    def _slow(self):
        self._commit("import time\ntime.sleep(0.3)\n")
        tid = self._perf()
        self.fm("focus", tid)
        self._commit("import time\ntime.sleep(0.2)\n")
        return tid

    def test_over_the_bar_fails(self):
        tid = self._slow()
        r = self.fm("task", "evidence", tid, "--bench", "python3 work.py", "--repeat", "1", "--under", "50", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertRegex(r.stdout, r"median \d+ms over --under 50ms")
        self.assertIn("✗ exit 1", self.fm("task", "show", tid).stdout)

    def test_under_the_bar_passes(self):
        tid = self._slow()
        r = self.fm("task", "evidence", tid, "--bench", "python3 work.py", "--repeat", "1", "--under", "5000")
        self.assertEqual(r.returncode, 0)
        self.assertRegex(r.stdout, r"under --under 5000ms")

    def test_under_without_bench_is_a_usage_error(self):
        tid = self._slow()
        r = self.fm("task", "evidence", tid, "--run", "true", "--under", "50", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--under", r.stderr + r.stdout)
        r = self.fm("task", "evidence", tid, "--bench", "true", "--under", "0", check=False)
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    import unittest
    unittest.main()
