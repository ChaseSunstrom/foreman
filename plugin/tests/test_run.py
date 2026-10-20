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
