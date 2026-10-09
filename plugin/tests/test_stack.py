"""T-0710 (Frontier 10, first slice): a milestone built in one pass lands as a stack of commits, one per step, each
checked alone."""
import os
import subprocess

from test_hooks import HookCase


class Stack(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        for f in ("a.py", "b.py"):
            self.write(f, "V = 0\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        self.fm("task", "new", "Two parts", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "part a", "--step", "part b", "--focus")

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def edit(self, rel, text):
        self.write(rel, text)
        self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": os.path.join(self.repo, rel)},
                                  "tool_response": {}})

    def git(self, *a):
        return subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True, text=True).stdout

    def build(self):
        self.edit("a.py", "V = 1\n")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.edit("b.py", "V = 2\n")
        self.fm("task", "evidence", "T-0001", "--step", "2", "--run", "true")

    def test_one_commit_per_step_each_checked_alone(self):
        self.build()
        out = self.fm("task", "finish", "T-0001", "--audit", "self", "--commit", "Two parts", "--stack",
                      "--stack-check", "python3 -c 'import a, b'").stdout
        subjects = self.git("log", "--format=%s", "-3").splitlines()
        self.assertEqual(len([s for s in subjects if s.startswith("Two parts")]), 2, subjects)
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD~1").split(), ["a.py"])
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD").split(), ["b.py"])
        self.assertIn("checked", out)
        self.assertEqual(self.git("status", "--porcelain").strip(), "")

    def test_a_commit_that_fails_alone_folds_into_the_next(self):
        self.build()
        check = "python3 -c 'import a, b; assert a.V + b.V in (0, 3)'"  # a alone gives 1: red
        out = self.fm("task", "finish", "T-0001", "--audit", "self", "--commit", "Two parts", "--stack",
                      "--stack-check", check).stdout
        self.assertEqual(sorted(self.git("show", "--name-only", "--format=", "HEAD").split()), ["a.py", "b.py"])
        self.assertIn("folded", out)
