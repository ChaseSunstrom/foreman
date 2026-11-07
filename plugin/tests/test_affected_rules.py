"""T-2992: the standing-rule tests (self-docs, model rules, left-out, rename scan) run in every affected set, so a
builder branch that misses a MASTER bullet or an fm shim fails in its own lane, not after the merge."""
import os
import subprocess

from helpers import ForemanTestCase

from sampo import core as c


class AffectedRules(ForemanTestCase):
    def test_every_affected_run_carries_the_rule_tests(self):
        from sampo import cli
        self.fm("init")
        self.fm("check", "affected", "python3 -m pytest -q {tests}")
        files = {"plugin/lib/sampo/other.py": "N = 1\n"}
        files.update({f"plugin/tests/{t}.py": "N = 1\n" for t in cli.RULE_TESTS})
        for rel, body in files.items():
            os.makedirs(os.path.dirname(os.path.join(self.repo, rel)), exist_ok=True)
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write(body)
        for args in (["add", "-A"], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "seed"]):
            subprocess.run(["git", "-C", self.repo, *args], check=True)
        self.fm("task", "new", "note it", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        p = c.find_project(self.repo, create=False)
        with open(os.path.join(self.repo, "plugin/lib/sampo/other.py"), "w") as f:
            f.write("N = 2\n")
        _, tests, _ = cli.affected(p)
        for t in cli.RULE_TESTS:
            self.assertIn(f"plugin/tests/{t}.py", tests)
        self.assertEqual(set(cli.RULE_TESTS), {"test_doctor", "test_models", "test_left_out", "test_rename_scan",
                                               "test_rename_aliases", "test_redefinitions", "test_suite_hygiene"})
