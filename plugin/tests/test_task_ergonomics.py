"""T-1231: the duel's transcripts showed Foreman's extra turns going to its own commands: a lost task id, an action on
the wrong side of the id, drop --reason, a broken check that could only be fixed by dropping the task, and steps that
needed evidence of their own on a small task whose criteria already prove it."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


class TaskErgonomics(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def task(self, *extra, ac="works :: true"):
        tid = json.loads(self.fm("task", "new", "Small change", "--type", "FIX", "--tier", "S", "--ac", ac,
                                 "--step", "change it", "--json", *extra).stdout)["id"]
        self.fm("focus", tid)
        return tid

    def brief(self, tid):
        return c.find_brief(c.find_project(self.repo), tid)

    def test_a_task_command_without_an_id_means_the_active_task(self):
        tid = self.task()
        r = self.fm("task", "evidence", "--step", "1", "--run", "true")
        self.assertIn(tid, r.stdout + r.stderr, "says which task it used")
        self.assertTrue(self.brief(tid).has_evidence(step=1))
        self.assertIn(tid, self.fm("task", "show").stdout)
        self.fm("task", "log", "a note")
        self.assertIn("a note", self.brief(tid).section("Log"))

    def test_with_no_active_task_the_id_is_still_required(self):
        r = self.fm("task", "show", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("id", r.stderr)

    def test_ac_and_step_take_their_action_on_either_side_of_the_id(self):
        tid = self.task()
        self.fm("task", "ac", "add", tid, "second :: true")
        self.fm("task", "ac", tid, "third :: true")  # no action: add
        self.fm("task", "step", "add", tid, "another step")
        b = self.brief(tid)
        self.assertEqual([a.text.split(" — ")[0] for a in b.acceptance()][1:], ["second", "third"])
        self.assertEqual(len(b.steps()), 2)

    def test_drop_block_and_defer_take_reason_as_an_option_too(self):
        tid = self.task()
        self.fm("task", "drop", tid, "--reason", "not needed")
        self.assertEqual(self.brief(tid).status, "dropped")
        self.assertIn("not needed", self.brief(tid).section("Log"))

    def test_a_check_that_couldnt_import_its_test_module_can_be_corrected(self):
        os.makedirs(os.path.join(self.repo, "tests"))
        with open(os.path.join(self.repo, "tests", "test_x.py"), "w") as f:
            f.write("import helpers_that_only_exist_on_tests_path\n")
        with open(os.path.join(self.repo, "tests", "helpers_that_only_exist_on_tests_path.py"), "w") as f:
            f.write("")  # it exists in the repo; run from the root, it isn't on the path
        tid = self.task(ac="works :: python3 -m unittest tests.test_x")
        self.fm("task", "evidence", tid, "--ac", "1", "--run", "python3 -m unittest tests.test_x", check=False)
        self.fm("task", "ac", tid, "edit", "1", "--verify", "true")
        self.assertIn("verify with `true`", self.brief(tid).section("Acceptance criteria"))
        self.assertIn("criterion 1 verify", self.brief(tid).section("Log"), "the change is logged")

    def test_a_check_that_ran_and_failed_still_cant_be_edited(self):
        tid = self.task(ac="works :: false")
        self.fm("task", "evidence", tid, "--ac", "1", "--run", "false", check=False)
        r = self.fm("task", "ac", tid, "edit", "1", "--verify", "true", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already has evidence", r.stderr)

    def test_a_small_tasks_steps_close_on_its_passing_criteria(self):
        tid = json.loads(self.fm("task", "new", "Small change", "--type", "FIX", "--tier", "S", "--ac", "works :: true",
                                 "--step", "write the test", "--step", "change it", "--json").stdout)["id"]
        self.fm("focus", tid)
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "covered by the criterion's check")
        r = self.fm("task", "finish", tid, "--audit", "self: small, criteria prove it", check=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.brief(tid).status, "done")

    def test_an_id_in_any_case_or_after_an_option_is_still_the_task_named(self):
        # review: `fm task defer --until … T-5` and `fm task drop t-5` acted on the active task instead
        other = json.loads(self.fm("task", "new", "Other", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step",
                                   "s", "--json").stdout)["id"]
        tid = self.task()
        self.fm("task", "defer", "--until", "2099-01-01", other)
        self.assertEqual(self.brief(tid).status, "active")
        self.fm("task", "drop", other.lower(), "dup")
        self.assertEqual(self.brief(other).status, "dropped")
        self.assertEqual(self.brief(tid).status, "active")

    def test_a_one_word_typo_is_not_added_as_a_criterion_or_step(self):
        tid = self.task()
        self.assertNotEqual(self.fm("task", "step", tid, "3", check=False).returncode, 0)
        self.assertEqual(len(self.brief(tid).steps()), 1)

    def test_a_broken_module_under_test_keeps_its_check_locked(self):
        # review: renaming the function a test imports is a real failure, not a check that never ran
        os.makedirs(os.path.join(self.repo, "tests"))
        with open(os.path.join(self.repo, "app.py"), "w") as f:
            f.write("def renamed():\n    return 1\n")
        with open(os.path.join(self.repo, "tests", "test_y.py"), "w") as f:
            f.write("from app import parse_duration\n")
        tid = self.task(ac="works :: python3 -m unittest tests.test_y")
        self.fm("task", "evidence", tid, "--ac", "1", "--run", "python3 -m unittest tests.test_y", check=False)
        r = self.fm("task", "ac", tid, "edit", "1", "--verify", "true", check=False)
        self.assertNotEqual(r.returncode, 0, "a module the change broke is a failing check")

    def test_an_import_gap_doesnt_mask_another_modules_real_failure(self):
        os.makedirs(os.path.join(self.repo, "tests"))
        with open(os.path.join(self.repo, "tests", "test_x.py"), "w") as f:
            f.write("import helpers_that_only_exist_on_tests_path\n")
        with open(os.path.join(self.repo, "tests", "helpers_that_only_exist_on_tests_path.py"), "w") as f:
            f.write("")
        with open(os.path.join(self.repo, "tests", "test_z.py"), "w") as f:
            f.write("import unittest\nclass Z(unittest.TestCase):\n    def test_z(self):\n        self.fail('real')\n")
        cmd = "python3 -m unittest tests.test_x tests.test_z"
        tid = self.task(ac=f"works :: {cmd}")
        self.fm("task", "evidence", tid, "--ac", "1", "--run", cmd, check=False)
        self.assertNotEqual(self.fm("task", "ac", tid, "edit", "1", "--verify", "true", check=False).returncode, 0)
