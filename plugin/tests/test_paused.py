"""T-0136: what other work changes while a task is paused isn't the task's own change: re-focus moves its start point
past that work (its own changes taken back out of the files as they are then), so scope, commit and audit see only it."""
import os
import subprocess
import unittest

from helpers import ForemanTestCase


class PausedTask(ForemanTestCase):
    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def new(self, title, scope):
        self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--scope", scope, "--ac", "ok :: true",
                "--step", "s", "--focus")

    def test_work_done_while_a_task_was_paused_is_not_its_own(self):
        self.fm("init")
        self.new("A", "a.py")
        self.write("a.py", "a = 1\n")
        self.new("B", "b.py")  # pauses A
        self.write("b.py", "b = 1\n")
        self.fm("task", "finish", "T-0002", "--run", "true", "--audit", "self check", "--commit", "Add b")
        self.write("c.py", "c = 1\n")  # the user's own edit, no task active
        self.fm("focus", "T-0001")
        self.write("a.py", "a = 2\n")
        p = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check", "--commit", "Add a", check=False)
        self.assertEqual(p.returncode, 0, p.stderr)  # b.py and c.py aren't edits outside its scope
        names = subprocess.run(["git", "-C", self.repo, "show", "--name-only", "--format="], capture_output=True,
                               text=True).stdout.split()
        self.assertEqual(names, ["a.py"])

    def test_a_file_written_as_the_task_started_is_committed(self):
        # T-0192 (found in T-0181): one command wrote a file and then focused the task, so the focus snapshot held the
        # edit and the commit left the file out; the hooks had seen the task touch it
        self.fm("init")
        self.write("b.txt", "unrelated\n")  # the person's own uncommitted file, never touched by the task
        self.write("a.py", "a = 1\n")
        self.new("A", "a.py")
        self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(self.repo, "a.py")}})
        p = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check", "--commit", "Add a", check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        names = subprocess.run(["git", "-C", self.repo, "show", "--name-only", "--format="], capture_output=True,
                               text=True).stdout.split()
        self.assertEqual(names, ["a.py"])

    def test_when_the_other_work_overlaps_the_start_point_stays_and_the_log_says_so(self):
        self.fm("init")
        self.new("A", "a.py")
        self.write("a.py", "a = 1\n")
        self.new("B", "a.py")
        self.write("a.py", "a = 3\n")  # the same line A changed
        self.fm("focus", "T-0001")
        self.assertIn("other work changed", self.fm("task", "show", "T-0001").stdout)


if __name__ == "__main__":
    unittest.main()
