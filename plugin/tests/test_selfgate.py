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


class WhichDiffsAreTimed(unittest.TestCase):  # T-3139: time hooks only when the diff touches what a hook process imported
    MAP = {"Stop": ["plugin/lib/sampo/hooks.py", "plugin/lib/sampo/core.py"], "PostToolUse": ["plugin/lib/sampo/core.py"]}

    def timed(self, *files, hmap=None):
        from sampo import selfgate as g
        return g.needs_timing(list(files), self.MAP if hmap is None else hmap)

    def test_a_page_script_no_hook_reads_skips_timing(self):
        self.assertFalse(self.timed("plugin/web/live/live.js"))

    def test_a_module_a_hook_imported_is_timed(self):
        self.assertTrue(self.timed("plugin/lib/sampo/hooks.py"))

    def test_a_module_no_hook_imported_skips_timing(self):
        self.assertFalse(self.timed("plugin/lib/sampo/louhi.py"))

    def test_a_top_level_lib_file_can_shadow_the_stdlib_so_is_timed(self):  # lib/ is first on the hook's sys.path
        self.assertTrue(self.timed("plugin/lib/json.py"))
        self.assertTrue(self.timed("plugin/lib/fmguard.py", hmap={"Stop": ["plugin/lib/sampo/core.py"]}))

    def test_the_cache_refreshes_on_the_bench_harness_but_not_the_changelog(self):
        from sampo import selfgate as g
        m = self.MAP
        for f in ("plugin/tests/bench_hooks.py", "plugin/tests/fixtures/hook_payloads.json",
                  "plugin/tests/fixtures/other.json", "plugin/lib/sampo/hooks.py"):
            self.assertTrue(g._refresh([f], m), f)
        self.assertFalse(g._refresh(["CHANGELOG.md", "plugin/web/live/live.js"], m))

    def test_a_hook_entry_hooks_json_or_data_file_is_timed(self):
        for f in ("plugin/hooks/hook", "plugin/hooks/hooks.json", "plugin/settings.json", "plugin/lib/sampo/data.json",
                  "plugin/bin/sampo", "CHANGELOG.md"):
            self.assertTrue(self.timed(f), f)

    def test_one_mapped_file_among_unmapped_ones_is_timed(self):
        self.assertTrue(self.timed("plugin/web/live/live.js", "plugin/lib/sampo/core.py"))

    def test_an_empty_map_times_as_before(self):
        self.assertTrue(self.timed("plugin/web/live/live.js", hmap={}))

    def test_the_map_is_reused_until_a_hook_file_changes_then_unioned(self):
        import os
        import tempfile
        from types import SimpleNamespace
        from sampo import selfgate as g
        p = SimpleNamespace(dir=tempfile.mkdtemp())
        runs = [{"Stop": ["plugin/lib/sampo/a.py"]}, {"Stop": ["plugin/lib/sampo/b.py"], "Pre": ["plugin/lib/sampo/c.py"]}]
        changed = [["plugin/web/x.js", "CHANGELOG.md"], ["plugin/lib/sampo/a.py"]]
        with mock.patch.object(g, "_hook_modules", side_effect=runs) as run, \
                mock.patch.object(g, "_changed", side_effect=changed):
            first = g.hook_map(p, "m", "s1", "base")
            self.assertEqual(g.hook_map(p, "m", "s2", "base"), first, "no mapped file changed: reused")
            self.assertEqual(run.call_count, 1)
            third = g.hook_map(p, "m", "s3", "base")
        self.assertEqual(run.call_count, 2)
        self.assertEqual(third["Stop"], ["plugin/lib/sampo/a.py", "plugin/lib/sampo/b.py"], "union over runs")
        self.assertIn("Pre", third)
        self.assertTrue(os.path.isfile(os.path.join(p.dir, "hook-modules.json")))

    def test_a_failed_map_run_is_an_empty_map(self):
        import tempfile
        from types import SimpleNamespace
        from sampo import selfgate as g
        with mock.patch.object(g, "_hook_modules", side_effect=RuntimeError("no")):
            self.assertEqual(g.hook_map(SimpleNamespace(dir=tempfile.mkdtemp()), "m", "s1", "base"), {})


class GateEndToEnd(unittest.TestCase):  # T-3139: git-built trees, the timing bench faked
    def run_gate(self, path, text):
        import os
        import subprocess
        import tempfile
        from types import SimpleNamespace
        from sampo import selfgate as g
        main = tempfile.mkdtemp()
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@x")

        def git(*a):
            return subprocess.run(["git", "-C", main, *a], check=True, capture_output=True, text=True, env=env).stdout.strip()
        git("init", "-q", "-b", "main")
        for rel in ("plugin/lib/fmguard.py", "plugin/lib/sampo/core.py", "plugin/web/live/live.js"):
            os.makedirs(os.path.dirname(os.path.join(main, rel)), exist_ok=True)
            open(os.path.join(main, rel), "w").write("x = 1\n")
        git("add", "-A")
        git("commit", "-q", "-m", "base")
        os.makedirs(os.path.dirname(os.path.join(main, path)), exist_ok=True)
        open(os.path.join(main, path), "w").write(text)
        git("add", "-A")
        git("commit", "-q", "-m", "branch")
        tip, base = git("rev-parse", "HEAD"), git("rev-parse", "HEAD~1")
        git("checkout", "-q", base)
        p, b, events = SimpleNamespace(dir=tempfile.mkdtemp()), SimpleNamespace(id="T-9"), []
        with mock.patch.object(g, "approved", return_value=False), mock.patch.object(g, "_corpus", return_value=[]), \
                mock.patch.object(g, "_verdicts", return_value=[]), mock.patch.object(g, "_footprint", return_value={}), \
                mock.patch("sampo.doctor.grown", return_value=[]), \
                mock.patch.object(g, "_hook_modules", return_value={"Stop": ["plugin/lib/sampo/core.py"]}), \
                mock.patch.object(g, "_paired", return_value=({}, {}, {})) as paired, \
                mock.patch.object(g.c, "log_event", side_effect=lambda *a, **k: events.append(a[1])):
            out = g.gate(p, b, main, tip, [path])
        return out, paired, events

    def test_a_web_only_diff_skips_the_timing_bench_and_says_so(self):
        out, paired, events = self.run_gate("plugin/web/live/live.js", "x = 2\n")
        self.assertEqual(out, [])
        paired.assert_not_called()
        self.assertIn("self_gate_timing_skipped", events)

    def test_a_lib_file_shadowing_the_stdlib_is_timed(self):
        out, paired, events = self.run_gate("plugin/lib/json.py", "x = 1\n")
        paired.assert_called_once()
        self.assertNotIn("self_gate_timing_skipped", events)


if __name__ == "__main__":
    unittest.main()
