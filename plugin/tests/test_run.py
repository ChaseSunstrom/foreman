"""T-0808: run.py takes test module names positionally, so fm check affected can hand it {names}."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import run  # noqa: E402


class Args(unittest.TestCase):
    def test_names_are_k_patterns(self):
        self.assertEqual(sorted(run.parse(["test_lanes", "-k", "Stop", "test_cli"]).k), ["Stop", "test_cli", "test_lanes"])
        self.assertEqual(run.parse([]).k, [])


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
        import subprocess
        return subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "run.py"), *names],
                              capture_output=True, text=True, timeout=300)

    def test_a_name_matching_no_test_fails_the_run_and_is_named(self):
        r = self.run_py("test_run.Args", "test_nosuch_module")  # not test_run itself: that would run this test
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("test_nosuch_module", r.stderr)

    def test_names_that_all_match_still_pass(self):
        self.assertEqual(self.run_py("test_run.Args").returncode, 0)


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
        self.assertLess(time.time() - t0, 30)
        self.assertNotEqual(code, 0)
        self.assertIn("still running after 2s", err)
        self.assertIn("test_s", err)  # where it hung
