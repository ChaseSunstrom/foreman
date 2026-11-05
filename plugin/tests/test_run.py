"""T-0808: run.py takes test module names positionally, so fm check affected can hand it {names}."""
import contextlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import run  # noqa: E402


def nested(args, seed=None, env=None):
    """T-3166: run.py as a child with its own times file (never the real one); returns (result, the file's times after)."""
    import json
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "t.json")
        if seed is not None:
            with open(p, "w") as f:
                json.dump(seed, f)
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "run.py"), *args],
                           capture_output=True, text=True, timeout=300, env=dict(os.environ, FM_TEST_TIMES=p, **(env or {})))
        return r, (json.load(open(p)) if os.path.exists(p) else None)


class Args(unittest.TestCase):
    def test_names_are_k_patterns(self):
        a = run.parse(["test_lanes", "-k", "Stop", "test_cli"])
        self.assertEqual((sorted(a.names), a.k), (["test_cli", "test_lanes"], ["Stop"]))
        self.assertEqual(run.parse([]).k, [])

    def test_a_name_and_a_k_select_only_the_tests_matching_both(self):
        # T-1994: "run.py test_run -k shards" ran every test_run test (names and -k were unioned)
        hit = set()
        self.assertEqual(run.classes(["test_run.py"], ["shards"], hit, names=["test_run"]), ["test_run.Args"])
        self.assertEqual(hit, {"shards", "test_run"})
        self.assertEqual(run.classes(["test_run.py"], ["no_such_test"], set(), names=["test_run"]), [])
        self.assertGreater(len(run.classes(["test_run.py"], [], set(), names=["test_run"])), 1)  # a name alone: all

    def test_shards_split_the_classes_disjointly_and_cover_them_all(self):  # T-1842: one CI job ran out of time
        import contextlib
        import io
        from unittest import mock
        self.assertEqual(run.parse(["--shard", "2/3"]).shard, (2, 3))
        self.assertIsNone(run.parse([]).shard)
        for bad in ("0/2", "3/2", "2", "a/b", "1/0"):
            with self.assertRaises(SystemExit, msg=bad), contextlib.redirect_stderr(io.StringIO()):
                run.parse(["--shard", bad])
        ids = [f"test_m.C{i}" for i in range(7)]
        got = []
        for k in (1, 2):
            ran = []
            with mock.patch.object(run, "classes", return_value=list(ids)), \
                    mock.patch.object(run, "run_one", lambda c, *a: ran.append(c) or (c, 0, "", 1, 0.0)), \
                    mock.patch.object(sys, "argv", ["run.py", "--shard", f"{k}/2"]), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(run.main(), 0)
            got.append(ran)
        self.assertEqual(sorted(got[0] + got[1]), sorted(ids))
        self.assertFalse(set(got[0]) & set(got[1]))
        self.assertLessEqual(abs(len(got[0]) - len(got[1])), 1)


class Load(unittest.TestCase):
    """T-1730: --load N runs the tests beside N busy processes, the way a load flake reproduces on demand."""

    def test_load_parses_and_defaults_to_zero(self):
        self.assertEqual(run.parse(["--load", "3", "test_cli"]).load, 3)
        self.assertEqual(run.parse([]).load, 0)

    def test_burn_keeps_n_busy_children_and_kills_them_after(self):
        import time
        with run.burn(2) as procs:
            self.assertEqual(len(procs), 2)
            time.sleep(0.3)
            self.assertTrue(all(p.poll() is None for p in procs))
            if os.path.isdir("/proc"):  # T-1828: macOS has no /proc; the children running is checked above
                from helpers import read_text
                cpu = [float(read_text(f"/proc/{p.pid}/stat").rsplit(")", 1)[1].split()[11]) for p in procs]
                self.assertTrue(all(t > 0 for t in cpu), "each child spins")
        self.assertTrue(all(p.poll() is not None for p in procs), "none outlives the run")

    def test_hang_guards_stretch_with_the_load_and_stay_bounded(self):
        # T-1719: a hook call's 10 s guard tripped beside 24 busy processes; it scales with runnable tasks per core
        from unittest import mock
        import helpers
        cores = os.cpu_count() or 1
        cases = [("0.50 0.4 0.3 1/900 1\n", 1.0), (f"{4 * cores} 1 1 3/900 1\n", 4.0),
                 (f"0.1 0.1 0.1 {3 * cores}/900 1\n", 3.0), (f"{100 * cores} 1 1 1/9 1\n", 8.0), ("garbage\n", None)]
        for text, want in cases:
            with mock.patch("builtins.open", mock.mock_open(read_data=text)):
                got = helpers.busy_factor()
            self.assertGreaterEqual(got, 1.0, text)
            self.assertLessEqual(got, 8.0, text)
            if want is not None:
                self.assertAlmostEqual(got, want, msg=text)
        case = helpers.ForemanTestCase()
        case.home, case.repo = "/nonexistent-home", "/"
        with mock.patch.object(helpers, "busy_factor", return_value=3.0), \
                mock.patch.object(helpers.subprocess, "run") as run_:
            case.hook("Stop", {})
            case.fm("status", check=False)
        self.assertEqual([c.kwargs["timeout"] for c in run_.call_args_list], [30.0, 90.0])

    def test_frames_are_judged_by_animation_time_and_rest_not_by_wall_windows(self):
        # T-1728: a loaded machine's slow frames (a 2 s gap) count as one capped step, as the pages count them
        import helpers
        self.assertAlmostEqual(helpers.anim_time([0, 16, 32, 2032, 2048]), 0.016 + 0.016 + 0.1 + 0.016)
        self.assertAlmostEqual(helpers.anim_time([0, 100, 200, 300], since=200), 0.2)
        self.assertEqual(helpers.anim_time([]), 0)
        rest = {"raf": 5, "waiting": 0}
        self.assertTrue(helpers.at_rest([None, rest, rest, rest]))
        self.assertFalse(helpers.at_rest([rest, rest]), "too few polls")
        self.assertFalse(helpers.at_rest([None, rest, rest]), "a failed poll is no rest")
        self.assertFalse(helpers.at_rest([rest, dict(rest, waiting=1), rest]), "a frame was asked for")
        self.assertFalse(helpers.at_rest([rest, rest, dict(rest, raf=6)]), "a frame was drawn")
        self.assertFalse(helpers.at_rest([dict(rest, raf=0)] * 3), "no frames yet is not rest")

    def test_a_killed_run_leaves_no_spinner(self):
        import signal
        import subprocess
        import time
        code = ("import sys, time; sys.path.insert(0, sys.argv[1]); import run\n"
                "with run.burn(1) as p:\n    print(p[0].pid, flush=True); time.sleep(60)")
        parent = subprocess.Popen([sys.executable, "-c", code, os.path.dirname(os.path.abspath(__file__))],
                                  stdout=subprocess.PIPE, text=True)
        child = int(parent.stdout.readline())
        parent.send_signal(signal.SIGKILL)
        parent.wait()
        parent.stdout.close()
        def alive():  # a zombie waiting for its new parent to reap it spins no more
            try:
                with open(f"/proc/{child}/stat") as f:
                    return f.read().rsplit(")", 1)[1].split()[0] != "Z"
            except OSError:
                return False
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and alive():
            time.sleep(0.05)
        left = alive()
        if left:
            os.kill(child, signal.SIGKILL)
        self.assertFalse(left, "the spinner outlived its run")

    def test_burn_zero_starts_nothing(self):
        with run.burn(0) as procs:
            self.assertEqual(procs, [])


class UnknownNames(unittest.TestCase):
    """T-1287: a module name that matches no test was dropped silently while another name matched, so a criterion
    naming a test file that doesn't exist passed."""

    def run_py(self, *names):
        return nested(names)[0]

    def test_a_name_matching_no_test_fails_the_run_and_is_named(self):
        r = self.run_py("test_run.Args", "test_nosuch_module")  # not test_run itself: that would run this test
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("test_nosuch_module", r.stderr)

    def test_a_name_whose_tests_a_k_filters_out_names_the_k(self):
        # T-1999: "no test matches test_run.Args" read as if the module were missing
        r = self.run_py("test_run.Args", "-k", "no_such_test")
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("no test matches test_run.Args with -k no_such_test", r.stderr)
        r = self.run_py("test_run.Args", "-k", "names_are_K_PATTERNS")  # T-2003: case and underscores aside, it exists
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("did you mean -k test_names_are_k_patterns?", r.stderr)
        self.assertNotIn("did you mean", self.run_py("test_run.Args", "-k", "no_such_test").stderr)

    def test_names_that_all_match_still_pass(self):
        self.assertEqual(self.run_py("test_run.Args").returncode, 0)

    def test_a_red_runs_last_line_names_the_failing_class(self):
        # T-2319: 'FAILED (1 classes)' alone sent a builder into a full re-run to learn which class failed
        r = nested(["test_run.AskedToFail"], env={"FM_RUN_ASKED_TO_FAIL": "1"})[0]
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertEqual(r.stderr.strip().splitlines()[-1], "FAILED (1 classes: test_run.AskedToFail)")


class AskedToFail(unittest.TestCase):
    """Fails only when test_a_red_runs_last_line_names_the_failing_class asks it to, through the environment."""

    def test_fails_when_asked(self):
        if os.environ.get("FM_RUN_ASKED_TO_FAIL") != "1":
            self.skipTest("fails only inside the summary test")
        self.fail("asked to fail")


class Tmp(unittest.TestCase):
    """T-2019: classes leaked 45k temp dirs, some with 68k files, until /tmp ran out of inodes and git failed."""

    def test_tmp_a_class_leaves_nothing_behind(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "made")
            with open(os.path.join(d, "test_leak.py"), "w") as f:
                f.write(f"import tempfile, unittest\nclass S(unittest.TestCase):\n    def test_s(self):\n"
                        f"        open({out!r}, 'w').write(tempfile.mkdtemp())\n")
            with mock.patch.object(run, "HERE", d):
                _, code, err, _, _ = run.run_one("test_leak.S", [])
            self.assertEqual(code, 0, err)
            made = open(out).read()
        self.assertNotEqual(os.path.dirname(made), tempfile.gettempdir())  # in the class's own dir
        self.assertFalse(os.path.exists(made))
        self.assertFalse(os.path.exists(os.path.dirname(made)))

    def test_tmp_a_dead_runs_dirs_are_swept_and_a_live_ones_kept(self):
        import subprocess
        import tempfile
        p = subprocess.Popen(["true"])
        p.wait()  # its pid is now a dead run's
        with tempfile.TemporaryDirectory() as base:
            dead = os.path.join(base, f"{run.TMP_PREFIX}{p.pid}-abc")
            live = os.path.join(base, f"{run.TMP_PREFIX}{os.getpid()}-def")
            other = os.path.join(base, "tmpkeepme1")
            for x in (dead, live, other):
                os.makedirs(os.path.join(x, "sub"))
            run.sweep(base)
            self.assertEqual(sorted(os.listdir(base)), sorted(os.path.basename(x) for x in (live, other)))


class Hang(unittest.TestCase):
    def test_a_class_that_hangs_is_killed_and_named_with_its_stack(self):  # T-1808: CI's job cap hid where
        import tempfile
        import time
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "test_stuck.py"), "w") as f:
                f.write("import subprocess, time, unittest\nclass S(unittest.TestCase):\n    def test_s(self):\n"
                        "        subprocess.Popen(['sleep', '60'])  # a child holding the pipes\n"
                        "        time.sleep(60)\n")
            t0 = time.time()
            with mock.patch.object(run, "HERE", d):
                cid, code, err, _, _ = run.run_one("test_stuck.S", [], timeout=2)
        self.assertLess(time.time() - t0, 30)  # wall clock: the timeout=2 kill deadline
        self.assertNotEqual(code, 0)
        self.assertIn("still running after 2s", err)
        self.assertIn("test_s", err)  # where it hung

    @unittest.skipUnless(sys.platform.startswith("linux"), "PR_SET_PDEATHSIG is Linux's")
    def test_a_class_still_running_dies_with_an_orphaning_kill_of_the_run(self):  # T-2034: one spun a core for a day
        import contextlib
        import subprocess
        import tempfile
        import time

        def gone(pid):
            try:
                with open(f"/proc/{pid}/stat") as f:
                    return f.read().rsplit(")", 1)[1].split()[0] == "Z"  # dead, not yet reaped
            except (FileNotFoundError, ProcessLookupError):  # T-2115: /proc reads ESRCH while the task exits
                return True

        with tempfile.TemporaryDirectory() as d:
            pidf = os.path.join(d, "pid")
            with open(os.path.join(d, "test_orphan.py"), "w") as f:
                f.write(f"import os, time, unittest\nclass S(unittest.TestCase):\n    def test_s(self):\n"
                        f"        with open({pidf!r}, 'w') as f:\n            f.write(str(os.getpid()))\n"
                        "        time.sleep(60)\n")
            boss = subprocess.Popen([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import run; "
                                     "run.HERE = sys.argv[2]; run.run_one('test_orphan.S', [], timeout=60)",
                                     os.path.dirname(os.path.abspath(run.__file__)), d])
            pid = None
            try:
                for _ in range(400):
                    with contextlib.suppress(OSError, ValueError):
                        with open(pidf) as f:
                            pid = int(f.read())
                        break
                    time.sleep(0.05)
                self.assertIsNotNone(pid, "the class never started")
                boss.kill()  # a Bash timeout's SIGKILL: run.py gets no chance to clean up
                boss.wait()
                for _ in range(100):
                    if gone(pid):
                        break
                    time.sleep(0.05)
                self.assertTrue(gone(pid), "the class outlived the run that started it")
            finally:
                boss.kill()
                if pid and not gone(pid):
                    with contextlib.suppress(ProcessLookupError):  # it may exit between the check and the kill
                        os.kill(pid, 9)

    def test_the_run_deadline_kills_a_running_class_and_skips_unstarted_ones(self):
        # T-1809: macOS hit its 35 min job cap with no annotation at all; the run now ends itself first
        import tempfile
        import time
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "test_slow.py"), "w") as f:
                f.write("import time, unittest\nclass S(unittest.TestCase):\n    def test_s(self):\n"
                        "        time.sleep(60)\n")
            t0 = time.time()
            with mock.patch.object(run, "HERE", d):
                _, code, err, _, _ = run.run_one("test_slow.S", [], timeout=480, deadline=time.time() + 2)
                self.assertLess(time.time() - t0, 30)  # wall clock: a kill deadline of a child
                self.assertNotEqual(code, 0)
                self.assertRegex(err, r"still running at the run's deadline \([12]s in\)")  # review: not the 480 s cap
                self.assertIn("test_s", err)  # the stack
                for late in (time.time() - 1, time.time() + 0.4):  # review: under 1 s left is too late to start
                    _, code, err, ran, _ = run.run_one("test_slow.S", [], deadline=late)
                    self.assertEqual((code, ran, err), (1, 0, run.NOT_STARTED))
        self.assertEqual(run.parse(["--deadline", "60"]).deadline, 60)
        self.assertIsNone(run.parse([]).deadline)

    def test_main_names_unstarted_classes_and_ci_gets_the_notes(self):
        # review: main's exit code, the not-started line (outside CI too) and the CI-only notes had no test
        import contextlib
        import io
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "test_late.py"), "w") as f:
                f.write("import unittest\nclass L(unittest.TestCase):\n    def test_l(self):\n        pass\n")
            out, err = io.StringIO(), io.StringIO()
            clock = iter([100.0])  # the run starts at 100; every later reading is past its 60 s deadline
            with mock.patch.object(run, "HERE", d), mock.patch.object(run, "skipped", return_value=set()), \
                    mock.patch.object(run.time, "time", side_effect=lambda: next(clock, 200.0)), \
                    mock.patch.object(sys, "argv", ["run.py", "--deadline", "60", "-p", "test_late.py"]), \
                    mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}), \
                    contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = run.main()
        self.assertEqual(code, 1)
        self.assertIn("not started (the run's 60s deadline): test_late.L", err.getvalue())
        self.assertIn("::error title=run.py::1 classes never started", out.getvalue())
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            run.parse(["--deadline", "0"])  # review: 0 read as falsy turned the deadline off


class SplitMe(unittest.TestCase):
    """T-3166: no class-level setup, so run.py runs each of these as its own job."""

    def test_a(self):
        pass

    def test_b(self):
        self.assertFalse(os.environ.get("FM_RUN_SPLIT_FAIL"))

    def test_c(self):
        pass


class WithSetUpClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = 1

    def test_a(self):
        self.assertEqual(self.shared, 1)

    def test_b(self):
        pass


class OptedOut(unittest.TestCase):
    run_whole = True  # T-3166: the marker for a class whose tests lean on each other

    def test_a(self):
        pass

    def test_b(self):
        pass


class PerTestJobs(unittest.TestCase):
    """T-3166: a class's tests are separate jobs in the pool, longest first, so no one class holds the run."""

    def walk(self):
        parts, whole = {}, set()
        run.classes(["test_run.py"], [], set(), names=["test_run"], parts=parts, whole=whole)
        return parts, whole

    def test_classes_with_setup_or_the_marker_stay_whole(self):
        parts, whole = self.walk()
        self.assertEqual(sorted(parts["test_run.SplitMe"]), [f"test_run.SplitMe.test_{x}" for x in "abc"])
        self.assertEqual(whole, {"test_run.WithSetUpClass", "test_run.OptedOut"})
        self.assertEqual(len(parts["test_run.OptedOut"]), 2)  # still counted, for the order

    def test_a_module_with_setUpModule_stays_whole(self):
        from unittest import mock
        with mock.patch.object(sys.modules[__name__], "setUpModule", lambda: None, create=True):
            self.assertIn("test_run.SplitMe", self.walk()[1])

    def test_plan_splits_known_slow_classes_and_orders_longest_first(self):
        parts = {"m.Slow": ["m.Slow.t1", "m.Slow.t2"], "m.Fast": ["m.Fast.t1", "m.Fast.t2"], "m.Held": ["m.Held.t1"]}
        times = {"m.Slow": 100.0, "m.Slow.t1": 30.0, "m.Slow.t2": 70.0, "m.Fast": 1.0, "m.Held": 500.0}
        got = run.plan(["m.Fast", "m.Slow", "m.Held"], parts, {"m.Held"}, times)
        self.assertEqual(got, ["m.Held", "m.Slow.t2", "m.Slow.t1", "m.Fast"])

    def test_plan_without_times_splits_only_the_seeded_slow_classes(self):
        # review: a shard (or a first run) must not start an interpreter per test of every class
        parts = {"m.LeanKind": ["m.LeanKind.t1", "m.LeanKind.t2"], "m.Big": [f"m.Big.t{i}" for i in range(50)]}
        got = run.plan(["m.Big", "m.LeanKind"], parts, set(), {})
        self.assertEqual(sorted(got), sorted(["m.Big", *parts["m.LeanKind"]]))
        self.assertEqual(run.plan(["m.Big"], parts, set(), {"m.Big": 0.5}), ["m.Big"])

    def test_work_time_leaves_out_each_jobs_start_up_so_a_class_is_not_ratcheted_split(self):
        self.assertEqual(run.work_time([run.START_S + 0.1] * 10), round(0.1 * 10, 2))
        self.assertLess(run.work_time([run.START_S] * 100), run.SPLIT_S)  # 100 trivial tests: back to one job
        self.assertEqual(run.work_time([]), 0.0)

    def test_a_k_run_keeps_a_whole_class_time_and_a_full_run_records_it(self):
        r, got = nested(["test_run.WithSetUpClass", "-k", "test_a"], seed={"test_run.WithSetUpClass": 99.0})
        self.assertEqual(got["test_run.WithSetUpClass"], 99.0, r.stderr)  # review: -k's partial time overwrote it
        r, got = nested(["test_run.WithSetUpClass"], seed={"test_run.WithSetUpClass": 99.0})
        self.assertLess(got["test_run.WithSetUpClass"], 50, r.stderr)

    def test_a_testcase_imported_into_a_second_module_is_planned_once(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "test_dedup_a.py"), "w") as f:
                f.write("import unittest\nclass Lake(unittest.TestCase):\n    def test_1(self): pass\n"
                        "    def test_2(self): pass\n")
            with open(os.path.join(d, "test_dedup_b.py"), "w") as f:
                f.write("from test_dedup_a import Lake  # noqa\n")
            parts = {}
            with mock.patch.object(run, "HERE", d), mock.patch.object(sys, "path", list(sys.path)):
                run.classes(["test_dedup_*.py"], [], set(), parts=parts)
            for m in ("test_dedup_a", "test_dedup_b"):
                sys.modules.pop(m, None)
        self.assertEqual(parts, {"test_dedup_a.Lake": ["test_dedup_a.Lake.test_1", "test_dedup_a.Lake.test_2"]})

    def test_a_non_classmethod_setUpClass_keeps_the_class_whole_not_a_crash(self):
        class Odd(unittest.TestCase):
            setUpClass = None

            def test_x(self):
                pass
        self.assertTrue(run.keeps_whole(Odd("test_x")))
        self.assertFalse(run.keeps_whole(SplitMe("test_a")))

    def test_an_unreadable_times_file_is_empty_and_a_planted_symlink_is_not_followed(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            p, victim = os.path.join(d, "t.json"), os.path.join(d, "victim")
            with mock.patch.dict(os.environ, {"FM_TEST_TIMES": p}):
                with open(p, "w") as f:
                    f.write('{"a": 1' + "0" * 400 + "}")  # float() of it is an OverflowError
                self.assertEqual(run.load_times(), {})
                os.remove(p)
                with open(victim, "w") as f:
                    f.write("mine")
                os.symlink(victim, f"{p}.{os.getpid()}")
                run.save_times({"a.B": 1.0})
                with open(victim) as f:
                    self.assertEqual(f.read(), "mine")
                self.assertEqual(run.load_times(), {"a.B": 1.0})
        self.assertIn(str(getattr(os, "getuid", lambda: 0)()), os.path.basename(run.times_path()))

    def test_times_round_trip_and_a_corrupt_file_is_empty(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.json")
            with mock.patch.dict(os.environ, {"FM_TEST_TIMES": p}):
                self.assertEqual(run.load_times(), {})
                run.save_times({"a.B": 2.5})
                run.save_times({"a.C": 1.0})
                self.assertEqual(run.load_times(), {"a.B": 2.5, "a.C": 1.0})
                with open(p, "w") as f:
                    f.write("{not json")
                self.assertEqual(run.load_times(), {})

    def test_a_split_class_runs_as_one_job_per_test_and_a_failure_names_the_test(self):
        # SplitMe is not a seeded name: the seeded time is what splits it
        seed = {"test_run.SplitMe": 99}
        r, got = nested(["test_run.SplitMe"], seed)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Ran 3 tests", r.stderr)
        self.assertIn("(3 jobs", r.stderr)
        self.assertIn("test_run.SplitMe.test_a", got)  # the run left its times for the next
        r, _ = nested(["test_run.SplitMe"], seed, {"FM_RUN_SPLIT_FAIL": "1"})
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertEqual(r.stderr.strip().splitlines()[-1], "FAILED (1 classes: test_run.SplitMe.test_b)")
        self.assertIn("FAIL: test_b", r.stderr)

    def test_a_class_with_setup_runs_whole(self):
        r, _ = nested(["test_run.WithSetUpClass"], {"test_run.WithSetUpClass": 99})
        self.assertIn("(1 jobs", r.stderr)
        self.assertIn("Ran 2 tests", r.stderr)
