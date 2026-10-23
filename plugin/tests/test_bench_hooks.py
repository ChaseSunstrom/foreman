"""T-0805: the hook benchmark's verdict: load alone never fails it, a code regression always does."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import bench_hooks  # noqa: E402


class Verdict(unittest.TestCase):
    def test_load_alone_never_fails_the_gate(self):
        # three gate runs on one machine (load 23-74) put every hook over 150 ms; alone they were 30-45 ms
        ok = bench_hooks.within
        self.assertTrue(ok(wall_p95=40, cpu_p95=30, budget=150, load=0.3))
        self.assertFalse(ok(wall_p95=400, cpu_p95=30, budget=150, load=0.3), "quiet machine: wall time decides")
        self.assertTrue(ok(wall_p95=400, cpu_p95=30, budget=150, load=4.0), "busy: CPU time decides")
        self.assertFalse(ok(wall_p95=400, cpu_p95=200, budget=150, load=4.0), "a real regression shows in CPU time")


class ScriptBudget(unittest.TestCase):  # T-1777
    def test_the_script_case_is_a_hook_plus_the_guards_time_box(self):
        # the bench's 37 KB script never finishes inside the guard's CPU box (a full read took 124 s), so the case
        # costs a hook's startup plus that box: a hook's budget plus the box, moving with it
        import fmguard
        self.assertEqual(bench_hooks.BUDGET_MS["PreToolUse:Bash:script"],
                         bench_hooks.BUDGET_MS["default"] + round(fmguard._script_budget() * 1000))


if __name__ == "__main__":
    unittest.main()
