"""Backlog hygiene. T-1663 (Reverify): a later commit touching a closed task's files queues that task's verify for
the sentinel, and a failing re-run captures a FIX naming the task."""
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


class Reverify(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.write("a.py", "x = 1\n")
        self.write("flag", "1")
        self.commit("start")
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--scope", "a.py", "--step", "do it",
                "--ac", "flag", "--focus")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "test -f flag")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "audit", "T-0001", "self", "checked", "ok")
        self.fm("task", "done", "T-0001")

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def commit(self, msg):
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)
        return subprocess.run(["git", "-C", self.repo, "rev-parse", "HEAD"], capture_output=True, text=True,
                              check=True).stdout.strip()

    def test_a_commit_to_a_closed_tasks_file_queues_its_verify(self):
        import fmreverify
        self.assertEqual(fmreverify.scan(self.p), [], "the first scan only sets the watermark: no backlog flood")
        self.write("b.py", "y = 1\n")
        self.commit("unrelated")
        self.write("a.py", "x = 2\n")
        self.commit("follow-up of its own (T-0001)")  # the task's own commit isn't a later change to it
        self.write("a.py", "x = 3\n")
        sha = self.commit("later change")
        q = fmreverify.scan(self.p)
        self.assertEqual([(e["task"], e["cmd"], e["sha"]) for e in q], [("T-0001", "test -f flag", sha)])
        self.assertEqual(len(fmreverify.scan(self.p)), 1, "a second scan neither re-queues nor duplicates")

    def test_the_sentinel_runs_the_queue_and_a_failure_captures_a_fix(self):
        import fmreverify
        fmreverify.scan(self.p)
        self.write("a.py", "x = 2\n")
        os.remove(os.path.join(self.repo, "flag"))
        self.commit("later change")
        p = self.fm("sentinel", "--last", "0", check=False)  # no recent-task checks: only the queue runs
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("✗ T-0001: test -f flag", p.stdout)
        fixes = [b for b in c.load_briefs(self.p) if b.type == "FIX" and b.status not in c.CLOSED]
        self.assertEqual(len(fixes), 1)
        self.assertIn("T-0001", fixes[0].title)
        self.assertEqual(fmreverify.load(self.p)["queue"], [], "a queued check that ran leaves the queue")
        self.fm("sentinel", "--last", "0", check=False)
        self.assertEqual(len([b for b in c.load_briefs(self.p) if b.type == "FIX"]), 1, "no second capture")
