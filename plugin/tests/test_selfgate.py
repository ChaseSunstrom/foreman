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

    def test_the_exams_planted_wait_still_doubles_a_hook_slowed_by_load_3_per_cpu(self):  # T-3605: the train's flake
        import os
        from sampo import core as c, louhi, selfgate as g
        line = next(e for m in louhi.GATE_MUTATIONS if m[0] == "hook-delay" for e in m[3])[2].splitlines()[-1]
        waits = []
        with mock.patch.dict(os.environ, FOREMAN_HOST="load=48,cpus=16"):
            exec(line.strip(), {"time": mock.Mock(sleep=waits.append), "c": c})
        base = {"Stop": {"p50": 300.0, "cpu_p50": 40.0, "cpu_p95": 45.0, "load": 3.0}}  # its fastest hook, past 250 ms
        self.assertIn("Stop", g._slower(base, {"Stop": dict(base["Stop"], p50=300.0 + waits[0] * 1000)}))


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


class BaseCache(unittest.TestCase):  # T-3176: the base tree's bench and guard replay are kept per base tree hash
    def setUp(self):
        import os
        import tempfile
        from types import SimpleNamespace
        from sampo import selfgate as g
        self.p, self.base = SimpleNamespace(dir=tempfile.mkdtemp()), tempfile.mkdtemp()
        os.makedirs(os.path.join(self.base, "lib"))
        self.put("lib/a.py", "x = 1\n")
        self.keyfile, self.load, self.logged = os.path.join(tempfile.mkdtemp(), "selfgate.key"), 0.5, []
        for m in (mock.patch.object(g, "_keyfile", lambda: self.keyfile),
                  mock.patch.object(g, "_load_pc", lambda: self.load),
                  mock.patch.object(g.c, "log_event", lambda p, ev, **k: self.logged.append(ev))):
            m.start()
            self.addCleanup(m.stop)

    def cache_path(self):
        import os
        return os.path.join(self.p.dir, "selfgate-base.json")

    def edit_cache(self, fn):
        import json
        with open(self.cache_path()) as f:
            d = json.load(f)
        fn(d)
        with open(self.cache_path(), "w") as f:
            json.dump(d, f)

    def test_the_cache_and_key_files_are_private(self):
        import os
        self.gate_side()
        self.assertEqual(os.stat(self.cache_path()).st_mode & 0o777, 0o600)
        self.assertEqual(os.stat(self.keyfile).st_mode & 0o777, 0o600)
        self.assertEqual(len(open(self.keyfile, "rb").read()), 32)

    def test_a_forged_cache_reruns_the_base_half(self):
        def slow(d):
            d["bench"][0][0]["Stop"]["p95"] = 1.0
        for name, forge in (("a tampered bench value", slow), ("a tampered key", lambda d: d.update(key="x")),
                            ("a missing MAC", lambda d: d.pop("mac")), ("a bad MAC", lambda d: d.update(mac="0" * 64))):
            with self.subTest(name):
                import os
                if os.path.exists(self.cache_path()):
                    os.remove(self.cache_path())
                self.gate_side()
                self.edit_cache(forge)
                self.assertEqual(self.gate_side()[0], 3)
        self.assertIn("self_gate_cache_ignored", self.logged)

    def test_a_cache_written_with_another_key_reruns_it(self):
        import os
        self.gate_side()
        os.remove(self.keyfile)
        self.assertEqual(self.gate_side()[0], 3)

    def test_an_unsafe_key_file_ignores_the_cache(self):
        import os
        self.gate_side()
        os.chmod(self.keyfile, 0o644)
        self.assertEqual(self.gate_side()[0], 3)
        real = self.keyfile + ".real"
        os.rename(self.keyfile, real)
        os.symlink(real, self.keyfile)
        self.assertEqual(self.gate_side()[0], 3)

    def test_the_bench_is_reused_only_within_a_load_band_of_1_5(self):
        self.gate_side()  # benched at load 0.5 per CPU
        for load, reused in ((0.74, True), (0.34, True), (0.80, False), (0.32, False)):
            with self.subTest(load=load):
                self.load = load
                self.assertEqual(self.gate_side()[0], 0 if reused else 3)
                self.load = 0.5
                self.gate_side()

    def put(self, rel, text):
        import os
        with open(os.path.join(self.base, rel), "w") as f:
            f.write(text)

    def gate_side(self, key=None):
        """One gate's base half with a fake bench and replay; returns (bench calls on base, replayed cmds, rows)."""
        from sampo import selfgate as g
        key = key or g._key(self.base)
        cache = g._load(self.p, key)
        seen = {"base": 0, "cmds": []}

        def bench(tree):
            seen["base"] += tree == "base"
            return {"Stop": {"p95": 100.0, "load": 0, "budget": 500}}, {}

        def verdicts(tree, cmds):
            seen["cmds"] += cmds
            return ["allow"] * len(cmds)
        with mock.patch.object(g, "_bench", bench), mock.patch.object(g, "_verdicts", verdicts):
            rows = g._paired("base", "new", cache)[0]
            g._base_verdicts(self.base, [["ls", ""], ["pwd", ""]], cache)
        g._save(self.p, key, cache)
        return seen["base"], seen["cmds"], rows

    def test_a_second_gate_on_the_same_base_skips_the_base_half(self):
        self.assertEqual(self.gate_side()[:2], (3, [["ls", ""], ["pwd", ""]]))
        self.assertEqual(self.gate_side()[:2], (0, []))

    def test_a_changed_base_or_setting_reruns_it(self):
        self.gate_side()
        self.put("lib/a.py", "x = 2\n")
        self.assertEqual(self.gate_side()[0], 3)
        from sampo import selfgate as g
        with mock.patch.object(g, "RUNS", 5):
            self.assertEqual(self.gate_side()[0], 3)

    def test_tests_and_pycache_do_not_change_the_key(self):
        import os
        from sampo import selfgate as g
        k = g._key(self.base)
        os.makedirs(os.path.join(self.base, "tests"))
        os.makedirs(os.path.join(self.base, "lib", "__pycache__"))
        self.put("tests/test_x.py", "1\n")
        self.put("lib/__pycache__/a.pyc", "1\n")
        self.assertEqual(g._key(self.base), k)

    def test_a_cache_older_than_a_day_reruns_it(self):
        import time
        from sampo import selfgate as g
        self.gate_side()
        with mock.patch.object(time, "time", return_value=time.time() + 86500):
            self.assertEqual(g._load(self.p, g._key(self.base)), {})

    def test_a_new_command_is_replayed_alone(self):
        from sampo import selfgate as g
        self.gate_side()
        cache = g._load(self.p, g._key(self.base))
        with mock.patch.object(g, "_verdicts", lambda t, cmds: ["deny"] * len(cmds)) as _:
            got = g._base_verdicts(self.base, [["ls", ""], ["rm", ""]], cache)
        self.assertEqual(got, ["allow", "deny"])

    def test_a_corrupt_cache_is_empty(self):
        import os
        from sampo import selfgate as g
        with open(os.path.join(self.p.dir, "selfgate-base.json"), "w") as f:
            f.write("{")
        self.assertEqual(g._load(self.p, g._key(self.base)), {})


class KeyPath(unittest.TestCase):  # T-3192: the MAC key lives in the account's own ~/.config/sampo, whatever SAMPO_SECRETS says
    def setUp(self):
        import os
        import tempfile
        from types import SimpleNamespace
        home, elsewhere = tempfile.TemporaryDirectory(), tempfile.TemporaryDirectory()
        self.addCleanup(home.cleanup)
        self.addCleanup(elsewhere.cleanup)
        self.home, self.elsewhere = home.name, elsewhere.name
        fake_pw = SimpleNamespace(pw_dir=self.home)
        env = {"SAMPO_SECRETS": os.path.join(self.elsewhere, "secrets.env"),
               "FOREMAN_SECRETS": os.path.join(self.elsewhere, "secrets.env")}
        for m in (mock.patch("pwd.getpwuid", lambda uid: fake_pw), mock.patch.dict(os.environ, env)):
            m.start()
            self.addCleanup(m.stop)

    def test_the_key_path_is_the_account_home_whatever_the_env_says(self):
        import os
        from sampo import selfgate as g
        self.assertEqual(g._keyfile(), os.path.join(self.home, ".config", "sampo", "selfgate.key"))

    def test_an_env_redirected_run_neither_reads_nor_writes_a_key_there(self):
        import os
        from sampo import selfgate as g
        planted = os.path.join(self.elsewhere, "selfgate.key")  # an agent-written key where the env points
        with open(planted, "wb") as f:
            f.write(b"k" * 32)
        key = g._secret()
        self.assertEqual(len(key), 32)
        self.assertNotEqual(key, b"k" * 32)
        self.assertTrue(os.path.isfile(os.path.join(self.home, ".config", "sampo", "selfgate.key")))
        self.assertEqual(os.listdir(self.elsewhere), ["selfgate.key"])


if __name__ == "__main__":
    unittest.main()
