#!/usr/bin/env python3
# FEATURE T-1169: a file already dirty when the task was focused stays out of its commit unless finish gets --with FILE
import os
import subprocess

from helpers import ForemanTestCase


class DirtyAtFocus(ForemanTestCase):
    def write(self, name, text):
        with open(os.path.join(self.repo, name), "w") as f:
            f.write(text)

    def git(self, *a):
        return subprocess.run(["git", "-C", self.repo, *a], capture_output=True, text=True, check=True).stdout

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.write("mine.py", "a = 0\n")
        self.write("clean.py", "b = 0\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "files")
        self.write("mine.py", "a = 1  # the user's own\n")  # dirty before the focus
        self.fm("task", "new", "T", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.write("mine.py", "a = 2\n")  # the task edits it too
        self.write("clean.py", "b = 1\n")

    def finish(self, *extra):
        return self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--commit", "Do it", *extra)

    def committed(self):
        return self.git("show", "--name-only", "--format=").splitlines()

    def test_dirty_file_is_named_and_left_out(self):
        r = self.finish()
        self.assertEqual(self.committed(), ["clean.py"])
        self.assertIn("mine.py", r.stdout)
        self.assertIn("--with", r.stdout)
        self.assertIn("mine.py", self.git("status", "--porcelain"))

    def test_with_commits_it(self):
        self.finish("--with", "mine.py")
        self.assertEqual(sorted(self.committed()), ["clean.py", "mine.py"])

    def test_old_brief_without_a_snapshot_commits_both(self):
        import fmcore as c
        p = c.find_project(self.repo, create=False)
        os.remove(os.path.join(p.dir, "audits", "T-0001.dirty.json"))
        self.finish()
        self.assertEqual(sorted(self.committed()), ["clean.py", "mine.py"])

    def test_a_file_an_earlier_task_edited_is_not_the_users(self):
        # task A leaves CHANGELOG uncommitted; B edits it and commits it
        path = os.path.join(self.repo, "CHANGELOG.md")
        self.write("CHANGELOG.md", "a\n")  # T-0001 edits it through the tool the hooks watch
        self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": path}, "tool_response": {}})
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true")
        self.fm("task", "new", "B", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.write("CHANGELOG.md", "a\nb\n")
        self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true", "--commit", "B")
        self.assertIn("CHANGELOG.md", self.committed())

    def test_odd_paths_and_with_spellings(self):
        for n in ("a, b.txt", "x #y.txt"):
            self.write(n, "0\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "odd")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true")
        for n in ("a, b.txt", "x #y.txt"):
            self.write(n, "1\n")
        self.fm("task", "new", "O", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        for n in ("a, b.txt", "x #y.txt"):
            self.write(n, "2\n")
        self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true", "--commit", "O",
                "--with", "./a, b.txt", "--with", os.path.join(self.repo, "x #y.txt"))
        self.assertEqual(sorted(self.committed()), ["a, b.txt", "x #y.txt"])


if __name__ == "__main__":
    import unittest
    unittest.main()
