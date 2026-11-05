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

    def test_a_rise_in_two_of_three_pairs_is_chance(self):  # T-3131: 16 hooks x 3 pairs make 2-of-3 likely by chance
        self.assertEqual(self.run_pairs([100, 100, 100], [300, 100, 300])[0], {})

    def test_a_real_rise_in_every_pair_holds(self):
        rows, _ = self.run_pairs([100, 100, 100], [200, 210, 220])
        self.assertIn("Stop", rows)
        self.assertIn("100", rows["Stop"])


class MedianCpu(unittest.TestCase):  # T-3131: the p95 of 10 runs is the slowest run; the median CPU time is steady
    def test_the_median_cpu_time_is_judged_when_both_sides_have_it(self):
        from sampo import selfgate as g
        base = {"Stop": {"p95": 100.0, "cpu_p95": 100.0, "cpu_p50": 60.0, "load": 0, "budget": 500}}
        spike = {"Stop": {"p95": 140.0, "cpu_p95": 140.0, "cpu_p50": 61.0, "load": 0, "budget": 500}}
        self.assertEqual(g._slower(base, spike), {}, "one slow run moves the p95, not the median")
        # a bigger one-pair jump trips the tail bar in that pair, and _paired's every-pair rule drops it
        with mock.patch.object(g, "_bench", side_effect=[(base, {}), ({"Stop": dict(spike["Stop"], p95=180.0)}, {}),
                                                          (base, {}), (base, {}), (base, {}), (base, {})]):
            self.assertEqual(g._paired("base", "new")[0], {})
        real = {"Stop": {"p95": 101.0, "cpu_p95": 101.0, "cpu_p50": 80.0, "load": 0, "budget": 500}}
        self.assertIn("60.0 -> 80.0", g._slower(base, real)["Stop"])

    def test_a_hook_that_waits_holds_on_a_quiet_bench(self):  # T-3131 review: CPU time misses a sleep or an I/O wait
        from sampo import selfgate as g
        base = {"Stop": {"p50": 60.0, "p95": 70.0, "cpu_p95": 60.0, "cpu_p50": 55.0, "load": 0.4, "budget": 500}}
        waits = {"Stop": {"p50": 100.0, "p95": 110.0, "cpu_p95": 60.0, "cpu_p50": 55.0, "load": 0.4, "budget": 500}}
        self.assertIn("wall", g._slower(base, waits)["Stop"])

    def test_a_slowdown_in_the_tail_alone_holds(self):  # T-3131 review: extra work on a few calls leaves the median
        from sampo import selfgate as g
        base = {"Stop": {"p50": 60.0, "p95": 100.0, "cpu_p95": 100.0, "cpu_p50": 55.0, "load": 0.4, "budget": 500}}
        tail = {"Stop": {"p50": 60.0, "p95": 200.0, "cpu_p95": 200.0, "cpu_p50": 55.0, "load": 0.4, "budget": 500}}
        self.assertIn("tail", g._slower(base, tail)["Stop"])
        wobble = {"Stop": {"p50": 60.0, "p95": 130.0, "cpu_p95": 130.0, "cpu_p50": 55.0, "load": 0.4, "budget": 500}}
        self.assertEqual(g._slower(base, wobble), {}, "a +30% max of 10 runs is the noise the median basis avoids")

    def test_an_old_bench_without_the_median_is_judged_as_before(self):
        from sampo import selfgate as g
        base = {"Stop": {"p95": 100.0, "load": 0, "budget": 500}}
        self.assertIn("Stop", g._slower(base, {"Stop": {"p95": 130.0, "load": 0, "budget": 500}}))

    def test_the_bench_reports_the_median_cpu_time(self):
        import os
        src = open(os.path.join(os.path.dirname(__file__), "bench_hooks.py"), encoding="utf-8").read()
        self.assertIn('"cpu_p50"', src)


class AaFixtures(unittest.TestCase):  # T-3131: the same tree benched against itself (with cpu_p50), 2026-11-05 UTC, load ~2 per core
    def test_identical_trees_hold_nothing(self):
        import json
        import os
        from sampo import selfgate as g
        d = os.path.join(os.path.dirname(__file__), "fixtures", "selfgate-aa")
        seq = {"base": iter([f"{i}a" for i in (1, 2, 3)]), "new": iter([f"{i}b" for i in (1, 2, 3)])}

        def bench(tree):
            with open(os.path.join(d, next(seq[tree]) + ".json"), encoding="utf-8") as f:
                return json.load(f)["bench"], {}
        with mock.patch.object(g, "_bench", bench):
            rows, _, _ = g._paired("base", "new")
        self.assertEqual(rows, {})


if __name__ == "__main__":
    unittest.main()
