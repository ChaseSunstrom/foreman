"""T-2605: the self-change gate's hook check (fmselfgate._slower) on a loaded bench: a hook that waits shows in the
median wall time even when load inflates the p95, and a small median wobble is noise.
T-2992: base and branch are benched interleaved over 3 pairs; only a rise seen in 2 of 3 pairs holds."""
import unittest
from unittest import mock

import helpers  # noqa: F401  (puts plugin/lib on the path)


class LoadedWallCheck(unittest.TestCase):
    def test_a_waiting_hook_is_caught_when_load_inflates_the_base_p95(self):  # T-2605: the LeanKind flake
        from sampo import selfgate as g
        base = {"Stop": {"p95": 400.0, "p50": 50.0, "cpu_p95": 30.0, "load": 3.0, "budget": 150}}
        rows = g._slower(base, {"Stop": {"p95": 600.0, "p50": 300.0, "cpu_p95": 31.0, "load": 3.0, "budget": 150}})
        self.assertIn("Stop", rows)
        self.assertIn("50.0 -> 300.0", rows["Stop"])
        self.assertEqual(g._slower(base, {"Stop": {"p95": 450.0, "p50": 70.0, "cpu_p95": 31.0, "load": 3.0,
                                                   "budget": 150}}), {}, "a 20 ms median wobble is load noise")


class Interleaved(unittest.TestCase):  # T-2992: fake benches with fixed timings, never real load
    def run_pairs(self, base_p95, branch_p95):
        """The rows `_paired` holds when the base's benches read base_p95 in turn and the branch's branch_p95."""
        from sampo import selfgate as g
        calls, seq = [], {"base": iter(base_p95), "new": iter(branch_p95)}

        def bench(tree):
            calls.append(tree)
            return {"Stop": {"p95": next(seq[tree]), "load": 0, "budget": 500}}, {}
        with mock.patch.object(g, "_bench", bench):
            rows, _, _ = g._paired("base", "new")
        return rows, calls

    def test_the_trees_are_benched_in_turn_three_pairs(self):
        rows, calls = self.run_pairs([100] * 3, [100] * 3)
        self.assertEqual(calls, ["base", "new"] * 3)
        self.assertEqual(rows, {})

    def test_a_rise_in_one_pair_is_load_noise(self):
        self.assertEqual(self.run_pairs([100, 100, 100], [300, 100, 100])[0], {})

    def test_a_rise_in_two_of_three_pairs_holds(self):
        self.assertIn("Stop", self.run_pairs([100, 100, 100], [300, 100, 300])[0])

    def test_a_real_rise_in_every_pair_holds(self):
        rows, _ = self.run_pairs([100, 100, 100], [200, 210, 220])
        self.assertIn("Stop", rows)
        self.assertIn("100", rows["Stop"])


if __name__ == "__main__":
    unittest.main()
