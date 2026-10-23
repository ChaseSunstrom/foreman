"""Backlog hygiene. T-1662 (Capture): fm capture refuses a near-duplicate of an open task of its type, naming it
(--anyway keeps it), and a FEATURE close to done work is flagged with that task's id. T-1663 (Reverify): a later
commit touching a closed task's files queues that task's verify for the sentinel, and a failing re-run captures a FIX
naming the task."""
import json
import os
import subprocess
from unittest import mock

from helpers import ForemanTestCase

import fmcli
import fmcore as c


class Capture(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def done(self, tid):
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, tid)
            b.meta["status"] = "done"
            c.save_brief(self.p, b)

    def test_a_near_duplicate_of_an_open_task_is_refused_with_its_id(self):
        self.fm("capture", "Export the weekly report as CSV")
        r = self.fm("capture", "export weekly reports as a CSV", check=False)
        self.assertEqual(r.returncode, fmcli.REFUSED_NEAR, "its own code, not a usage error's 1 or a lock's 3")
        self.assertIn("T-0001", r.stderr)
        self.assertIn("add --anyway to keep both, or fm task log T-0001", r.stderr)
        self.assertNotIn("…", r.stderr)
        self.assertIsNone(c.find_brief(self.p, "T-0002"), "a refused capture makes no brief")
        r = self.fm("capture", "export weekly reports as a CSV", "--json", check=False)
        self.assertEqual(r.returncode, fmcli.REFUSED_NEAR)
        self.assertEqual(json.loads(r.stdout), {"refused": "near-duplicate", "of": "T-0001",
                                                "title": "Export the weekly report as CSV"})
        out = self.fm("capture", "export weekly reports as a CSV", "--anyway").stdout
        self.assertIn("T-0002", out)

    def test_a_refused_paste_leaves_no_attachment(self):
        self.fm("capture", "Export the weekly report as CSV")
        r = self.fm("capture", "export weekly reports as a CSV", "--from-file", "-", input="log line\n", check=False)
        self.assertEqual(r.returncode, fmcli.REFUSED_NEAR)
        self.assertFalse(os.path.isdir(os.path.join(self.p.dir, "attachments")), "checked before the paste is kept")

    def test_a_different_type_is_kept_with_a_note(self):
        self.fm("capture", "Export the weekly report as CSV")
        out = self.fm("capture", "export weekly reports as a CSV", "--type", "FIX").stdout
        self.assertIn("T-0002", out)
        self.assertIn("Similar open T-0001", out)

    def test_sibling_module_names_are_not_one_request(self):
        self.fm("capture", "Fix fmcodetui crash on resume", "--type", "FIX")
        self.fm("capture", "Fix fmcode crash on resume", "--type", "FIX")
        self.fm("capture", "fmdoctor repair loses the hooks")
        self.fm("capture", "fmdocs repair loses the hooks")
        self.assertEqual(len(c.load_briefs(self.p)), 4)

    def test_recurring_obstacles_with_different_signatures_are_both_captured(self):
        import fmfixes
        fmfixes._escalate(self.p, "ModuleNotFoundError: No module named 'yaml'")
        fmfixes._escalate(self.p, "ModuleNotFoundError: No module named 'toml'")
        self.assertEqual(len(c.load_briefs(self.p)), 2)

    def test_unrelated_or_differently_scoped_requests_are_kept(self):
        self.fm("capture", "Export the weekly report as CSV", "--scope", "report/csv.py")
        self.fm("capture", "fix the login timeout on slow wifi")
        self.fm("capture", "export the weekly report as CSV", "--scope", "billing/ledger.py")  # other files: kept
        self.fm("capture", "export")  # one shared word is not a duplicate
        self.fm("capture", "Crash in what T-0001 added")
        self.fm("capture", "Crash in what T-0002 added")  # other numbers: other work
        self.assertEqual(len(c.load_briefs(self.p)), 6)

    def test_a_closed_task_is_not_a_duplicate_and_a_close_feature_is_flagged(self):
        self.fm("capture", "Export the weekly report as CSV")
        self.done("T-0001")
        out = self.fm("capture", "export weekly reports as a CSV").stdout
        self.assertIn("T-0002", out)
        self.assertIn("Close to done work: T-0001", out)
        self.assertNotIn("Close to done", self.fm("capture", "export weekly reports as a CSV file", "--type", "FIX",
                                                  "--anyway").stdout, "only a FEATURE is flagged")
        self.assertNotIn("Close to done", self.fm("capture", "fix the login timeout on slow wifi").stdout)


class _Repo(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.write("a.py", "x = 1\n")
        self.write("flag", "1")
        self.commit("start")

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo, *args], capture_output=True, text=True, check=True).stdout.strip()

    def commit(self, msg, *extra):
        self.git("add", "-A")
        self.git("commit", "-qm", msg, *extra)
        return self.git("rev-parse", "HEAD")


class _Fake:
    """A closed brief with one passing criteria check, for scan()'s matching alone."""
    def __init__(self, tid):
        self.id, self.status = tid, "done"
        self.meta = {"scope": ["a.py"], "updated": "2020-01-01T00:00:00Z"}

    def evidence(self):
        return [f"- (ac 1) `test -n {self.id}` → exit 0 · ok [ran] (2020-01-01T00:00:00Z)"]


class ReverifyScan(_Repo):
    def scan(self, *briefs):
        import fmreverify
        with mock.patch.object(c, "load_briefs", return_value=list(briefs)):
            return fmreverify.scan(self.p)

    def test_the_own_commit_is_read_from_the_trailer_and_the_subject_only_without_one(self):
        b = _Fake("T-0002")
        self.scan(b)
        self.write("a.py", "x = 2\n")
        self.commit("Add widget", "--trailer", "Foreman-Task: T-0002")  # fm task finish --commit's own close
        self.assertEqual(self.scan(b), [])
        self.write("a.py", "x = 3\n")
        sha = self.commit("Fix T-0002 regression", "--trailer", "Foreman-Task: T-0009")  # another task's work
        self.write("a.py", "x = 4\n")
        self.commit("Tidy up (T-0002)")  # no trailer: the subject decides
        self.assertEqual([(e["task"], e["sha"]) for e in self.scan(b)], [("T-0002", sha)])

    def test_one_commit_queues_five_tasks_at_most(self):
        briefs = [_Fake(f"T-01{i:02d}") for i in range(7)]
        self.scan(*briefs)
        self.write("a.py", "x = 2\n")
        self.commit("touch everything")
        self.assertEqual(len({e["task"] for e in self.scan(*briefs)}), 5)

    def test_a_git_failure_leaves_the_watermark_where_it_was(self):
        import fmreverify
        b = _Fake("T-0002")
        self.scan(b)
        before = fmreverify.load(self.p)["head"]
        self.write("a.py", "x = 2\n")
        sha = self.commit("later change")
        with mock.patch.object(fmreverify, "_commits", return_value=None):
            self.assertEqual(self.scan(b), [])
        self.assertEqual(fmreverify.load(self.p)["head"], before, "a failed git log must not skip its commits")
        self.assertEqual([e["sha"] for e in self.scan(b)], [sha])

    def test_rewritten_history_only_moves_the_watermark(self):
        import fmreverify
        b = _Fake("T-0002")
        self.scan(b)
        self.write("b.py", "y = 1\n")
        self.commit("unrelated")
        self.scan(b)
        self.write("a.py", "x = 2\n")
        head = self.commit("unrelated, amended to touch a.py", "--amend")  # the scanned head is gone
        self.assertEqual(self.scan(b), [], "commits that aren't descendants of the last scan aren't this tree's")
        self.assertEqual(fmreverify.load(self.p)["head"], head)


class Reverify(_Repo):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--scope", "a.py", "--step", "do it",
                "--ac", "flag", "--focus")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "test -f flag")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "audit", "T-0001", "self", "checked", "ok")
        self.fm("task", "done", "T-0001")

    def queue(self, *entries):
        """Seed the queue directly, the watermark at HEAD so the sentinel's scan adds nothing."""
        with open(os.path.join(self.p.dir, "reverify.json"), "w") as f:
            json.dump({"head": self.git("rev-parse", "HEAD"), "queue": list(entries)}, f)

    def fixes(self):
        return [b for b in c.load_briefs(self.p) if b.type == "FIX"]

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
        fixes = [b for b in self.fixes() if b.status not in c.CLOSED]
        self.assertEqual(len(fixes), 1)
        self.assertIn("T-0001", fixes[0].title)
        self.assertEqual(fmreverify.load(self.p)["queue"], [], "a queued check that ran leaves the queue")
        self.fm("sentinel", "--last", "0", check=False)
        self.assertEqual(len(self.fixes()), 1, "no second capture")

    def test_side_effects_and_tasks_no_longer_done_are_dropped_unrun(self):
        import fmreverify
        self.write("keep", "1")
        self.fm("capture", "not done yet")  # T-0002, captured
        self.queue({"task": "T-0001", "cmd": "rm -f keep"}, {"task": "T-0001", "cmd": "curl -s http://127.0.0.1:9"},
                   {"task": "T-0002", "cmd": "test -f gone"}, {"task": "T-0099", "cmd": "test -f gone2"})
        p = self.fm("sentinel", "--last", "0", check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "keep")), "a queued rm never runs")
        self.assertIn("4 queued re-verify entries dropped", p.stdout)
        self.assertEqual(self.fixes(), [])
        self.assertEqual(fmreverify.load(self.p)["queue"], [])

    def test_entries_past_max_stay_queued(self):
        import fmreverify
        self.queue(*({"task": "T-0001", "cmd": f"test -n {i}"} for i in range(3)))
        self.fm("sentinel", "--last", "0", "--max", "1")
        self.assertEqual([e["cmd"] for e in fmreverify.load(self.p)["queue"]], ["test -n 1", "test -n 2"])

    def test_a_fix_holds_no_secret_or_escape_and_long_commands_get_their_own(self):
        self.write("out.txt", "\x1b[31mtoken ghp_" + "a" * 36 + "\n")
        os.remove(os.path.join(self.repo, "flag"))
        long = "cat out.txt; test -f flag # " + "x" * 70
        self.queue({"task": "T-0001", "cmd": long + "1", "sha": "0" * 40, "subject": "\x1b[2J ghp_" + "b" * 36},
                   {"task": "T-0001", "cmd": long + "2"})
        self.fm("sentinel", "--last", "0", check=False)
        fixes = self.fixes()
        self.assertEqual(len(fixes), 2, "two commands sharing a long prefix are two FIXes")
        for b in fixes:
            with open(b.path, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("token [REDACTED]", text, "the failing output reaches the FIX, redacted")
            self.assertNotIn("ghp_aaaa", text)
            self.assertNotIn("ghp_bbbb", text)
            self.assertNotIn("\x1b", text)
