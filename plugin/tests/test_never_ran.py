"""T-0985: a run that never reached the check (its command, file or test module didn't exist) doesn't lock the
criterion, so a wrong verify path is fixed with fm task ac edit instead of dropping and recreating the task (both
recorded demo sessions did that). A check that ran and failed stays locked (T-0342)."""
from helpers import ForemanTestCase


class NeverRanUnlocks(ForemanTestCase):
    def task(self, verify):
        self.fm("init")
        self.fm("task", "new", "x", "--type", "FIX", "--tier", "S", "--ac", f"works :: {verify}", "--step", "s",
                "--focus")

    def edit(self):
        return self.fm("task", "ac", "T-0001", "edit", "1", "--verify", "true", check=False)

    def test_a_missing_test_module_or_file_or_command_does_not_lock(self):
        for verify in ("python3 -m unittest test_nowhere_x", "python3 tests/missing_test_x.py", "nosuchtool_x --check"):
            with self.subTest(verify=verify):
                self.setUp()
                self.task(verify)
                self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", verify, check=False)
                r = self.edit()
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_a_check_that_ran_and_failed_stays_locked(self):
        self.task("python3 -c 'assert 1 == 2'")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "python3 -c 'assert 1 == 2'", check=False)
        r = self.edit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already has evidence", r.stderr)
