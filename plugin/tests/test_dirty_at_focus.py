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
        return self.git("show", "--name-only", "--format=").split()

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
        b = c.find_brief(p, "T-0001")
        b.meta.pop("dirty_at_focus", None)
        c.save_brief(p, b)
        self.finish()
        self.assertEqual(sorted(self.committed()), ["clean.py", "mine.py"])


if __name__ == "__main__":
    import unittest
    unittest.main()
