"""T-0855 (newcomer walkthrough, 2026-10-15): what a first-time user's shell shows — fm check finding the test runner,
the digest counting folded tasks."""
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c
import fmmap


class FirstCheck(ForemanTestCase):
    def test_a_runnable_gate_is_offered_for_plain_python_tests(self):
        # T-0850: a root-level test_app.py found no gate, and the old hint "pytest (or python3 -m unittest)" isn't a command
        self.assertIn("python3 -m unittest discover -q", fmmap._gates(self.repo, ["app.py", "test_app.py"], []))
        self.assertIn("python3 -m unittest discover -s tests -q", fmmap._gates(self.repo, ["tests/test_a.py"], []))
        self.assertIn("python3 -m pytest -q", fmmap._gates(self.repo, ["pytest.ini", "tests/test_a.py"], []))
        self.assertIn("python3 -m pytest -q", fmmap._gates(self.repo, ["conftest.py", "test_a.py"], []))
        # T-0987 (T-0978: Haiku ran unittest discover, which import-errors here, not the repo's runner)
        self.assertEqual(fmmap._gates(self.repo, ["plugin/tests/run.py", "plugin/tests/test_a.py"], [])[0],
                         "python3 plugin/tests/run.py")
        self.assertEqual(fmmap._gates(self.repo, ["run_tests.py", "test_a.py"], [])[0], "python3 run_tests.py")

    def test_check_with_no_gates_prints_the_line_to_add_one(self):
        self.fm("init")
        for name, text in (("app.py", "def hi():\n    return 1\n"),
                           ("test_app.py", "import unittest\nimport app\n\n\nclass T(unittest.TestCase):\n"
                                           "    def test_hi(self):\n        self.assertEqual(app.hi(), 1)\n")):
            with open(os.path.join(self.repo, name), "w") as f:
                f.write(text)
        subprocess.run(["git", "-C", self.repo, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "app"], check=True)
        r = self.fm("check", check=False)
        self.assertIn("fm check add 'python3 -m unittest discover -q'", r.stderr + r.stdout)


class Digest(ForemanTestCase):
    def test_a_task_folded_into_another_counts_as_folded(self):
        # T-0852: 159 of 370 tasks last week read "ungraded": every one had been closed as done in another task
        self.fm("init")
        self.fm("task", "new", "Host", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.fm("capture", "Same thing, said again")
        self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check")
        self.fm("task", "drop", "T-0002", "same request", "--done-in", "T-0001")
        out = self.fm("digest").stdout
        self.assertIn("folded", out)
        self.assertNotIn("ungraded", out.splitlines()[0])
