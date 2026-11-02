"""T-2651: fm task evidence --bench CMD --under MS is a pass/fail proof on the current tree's median."""
import test_evidence_quality as q


class BenchUnder(q._Base):  # the helpers only: subclassing Bench would rerun its tests
    _commit, _perf = q.Bench._commit, q.Bench._perf

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

    def test_a_bench_that_fails_is_recorded_as_a_failed_run(self):
        tid = self._slow()
        r = self.fm("task", "evidence", tid, "--step", "1", "--bench", "python3 work.py; exit 3", "--repeat", "1",
                    check=False)
        self.assertNotEqual(r.returncode, 0)
        shown = self.fm("task", "show", tid).stdout
        self.assertIn("→ ✗ exit 3", shown)  # the finish gate's failed-run mark
        self.assertIn("1. [ ] speed it up", shown)  # a failed bench closes no step


if __name__ == "__main__":
    import unittest
    unittest.main()
