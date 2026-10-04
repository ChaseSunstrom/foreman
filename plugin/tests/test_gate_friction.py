"""Gate and CLI friction (T-0274): a flaky test is recorded, never hidden (T-0272); an fm typo names the nearest real
command or flag (T-0273)."""
import os

from helpers import ForemanTestCase


class Flakes(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.flag = os.path.join(self.tmp, "flag")  # outside the repo: the tree doesn't change between runs
        self.fm("check", "add", f"test -f {self.flag} || {{ echo 'FAIL: test_login (auth.tests.Login.test_login)'; "
                                f"echo 'FAILED api/test_api.py::test_list - AssertionError'; exit 1; }}")

    def test_a_fail_then_pass_on_the_same_tree_is_flaky(self):
        first = self.fm("check", check=False)
        self.assertNotEqual(first.returncode, 0)
        open(self.flag, "w").close()
        second = self.fm("check")
        self.assertIn("flaky", second.stdout)
        self.assertIn("auth.tests.Login.test_login", second.stdout)
        self.assertIn("api/test_api.py::test_list", second.stdout)
        os.remove(self.flag)
        third = self.fm("check", "--fresh", check=False)  # a cached pass on this tree would skip the run
        self.assertNotEqual(third.returncode, 0)  # a known flake still fails the gate
        self.assertIn("known flaky", third.stdout)

    def test_a_pass_on_the_in_run_rerun_records_the_names(self):
        self.fm("check", "rm", "1")
        marker = os.path.join(self.tmp, "ran-once")  # fails the first time it runs, passes the rerun
        self.fm("check", "add", f"test -f {marker} || {{ touch {marker}; echo 'FAIL: test_x (pkg.T.test_x)'; exit 1; }}")
        out = self.fm("check").stdout
        self.assertIn("flaky: pkg.T.test_x", out)

    def test_log_lines_are_not_test_names(self):
        import fmcore as c
        self.assertEqual(c.failing_tests("ERROR: timeout (30)\nERROR: failed (retrying)\n"), [])
        self.assertEqual(c.failing_tests("FAIL: test_a (m.C.test_a) (i=1)\n--- FAIL: TestX (0.01s)\n"),
                         ["TestX", "m.C.test_a"])

    def test_a_fix_in_between_is_not_a_flake(self):
        self.fm("check", check=False)
        with open(os.path.join(self.repo, "fix.py"), "w") as f:
            f.write("x = 1\n")  # the tree changed: the pass is the fix, not luck
        open(self.flag, "w").close()
        self.assertNotIn("flaky", self.fm("check").stdout)


class Typos(ForemanTestCase):
    def test_a_parse_outside_main_still_gives_a_usage_error(self):  # found by fm task prove --hunks
        import contextlib
        import io
        import fmcli
        with contextlib.redirect_stderr(io.StringIO()) as err, self.assertRaises(SystemExit):
            fmcli.build_parser().parse_args(["tsk"])
        self.assertIn("did you mean task", err.getvalue())

    def test_nearest_subcommand_and_flag(self):
        self.fm("init")
        for argv, want in ((["tsk", "show", "T-0001"], "task"), (["task", "evidense", "T-1"], "evidence"),
                           (["check", "--evidance", "T-1"], "--evidence"), (["capture", "x", "--tyep", "FIX"], "--type")):
            p = self.fm(*argv, check=False)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn(f"did you mean {want}", p.stderr, argv)
