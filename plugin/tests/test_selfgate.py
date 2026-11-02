"""T-2605: the self-change gate's hook check (fmselfgate._slower) on a loaded bench: a hook that waits shows in the
median wall time even when load inflates the p95, and a small median wobble is noise."""
import unittest

import helpers  # noqa: F401  (puts plugin/lib on the path)


class LoadedWallCheck(unittest.TestCase):
    def test_a_waiting_hook_is_caught_when_load_inflates_the_base_p95(self):  # T-2605: the LeanKind flake
        import fmselfgate as g
        base = {"Stop": {"p95": 400.0, "p50": 50.0, "cpu_p95": 30.0, "load": 3.0, "budget": 150}}
        rows = g._slower(base, {"Stop": {"p95": 600.0, "p50": 300.0, "cpu_p95": 31.0, "load": 3.0, "budget": 150}})
        self.assertIn("Stop", rows)
        self.assertIn("50.0 -> 300.0", rows["Stop"])
        self.assertEqual(g._slower(base, {"Stop": {"p95": 450.0, "p50": 70.0, "cpu_p95": 31.0, "load": 3.0,
                                                   "budget": 150}}), {}, "a 20 ms median wobble is load noise")


if __name__ == "__main__":
    unittest.main()
