"""T-1667: fm fsck reports what a crash or a hand edit left broken in Foreman's own state (a lane whose folder or branch
is gone, a *.pid lock whose process is dead, a journal whose last line is torn) and --fix removes only the stale locks.
Each test runs in its own temp FOREMAN_HOME."""
import json
import os
import subprocess
import time
import unittest

from helpers import ForemanTestCase, read_text

import fmcore as c
import fmdoctor as d

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # --json prints the task first


def dead_pid():
    proc = subprocess.Popen(["true"])
    proc.wait()  # reaped: the pid names no process now
    return proc.pid


def write(path, text, age=0):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    if age:
        os.utime(path, (time.time() - age, time.time() - age))
    return path


class Fsck(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.tid = self.task("Gone lane", lane=os.path.join(self.tmp, "gone-lane"), lane_branch="foreman/gone")
        self.stale = write(os.path.join(self.p.dir, "sentinel.pid"), f"{dead_pid()}\n", age=3600)
        self.live = write(os.path.join(self.p.dir, "ambient", "run.pid"), str(os.getpid()), age=3600)
        self.ledger = os.path.join(self.p.dir, "ledger.jsonl")
        with open(self.ledger, "a") as f:
            f.write('{"event": "cut sho')  # a crash mid-append
        self.ledger_bytes = read_text(self.ledger)

    def task(self, title, **meta):
        tid = first(self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                            "--step", "s", "--json").stdout)["id"]
        b = next(x for x in c.load_briefs(self.p) if x.id == tid)
        b.meta.update(meta)
        c.save_brief(self.p, b)
        return tid

    def kinds(self, res):
        return sorted((f["kind"], f.get("task") or os.path.basename(f["path"])) for f in res["findings"])

    def test_reports_the_broken_lane_the_stale_lock_and_the_torn_journal(self):
        r = self.fm("fsck", "--json", check=False)
        self.assertEqual(r.returncode, 1, r.stderr)
        res = json.loads(r.stdout)
        self.assertFalse(res["ok"])
        self.assertEqual(self.kinds(res), [("broken lane", self.tid), ("stale lock", "sentinel.pid"),
                                           ("torn journal", "ledger.jsonl")])
        self.assertTrue(os.path.exists(self.stale), "the report alone removes nothing")
        text = self.fm("fsck", check=False).stdout
        self.assertIn(f"{self.tid}: its folder is gone", text)
        self.assertIn("fm fsck --fix", text)

    def test_fix_removes_only_the_stale_lock(self):
        b = next(x for x in c.load_briefs(self.p) if x.id == self.tid)
        r = self.fm("fsck", "--fix", "--json", check=False)
        self.assertEqual(r.returncode, 1, "the lane and the journal are left for a person")
        res = json.loads(r.stdout)
        self.assertEqual(res["fixed"], [self.stale])
        self.assertEqual(self.kinds(res), [("broken lane", self.tid), ("torn journal", "ledger.jsonl")])
        self.assertFalse(os.path.exists(self.stale))
        self.assertTrue(os.path.exists(self.live), "a lock whose process lives is kept")
        self.assertEqual(read_text(self.ledger), self.ledger_bytes, "the hash-chained ledger is never rewritten")
        self.assertEqual(next(x for x in c.load_briefs(self.p) if x.id == self.tid).meta, b.meta)
        again = json.loads(self.fm("fsck", "--fix", "--json", check=False).stdout)  # a second run: nothing more to fix
        self.assertEqual(again["fixed"], [])
        self.assertEqual(len(again["findings"]), 2)

    def test_a_healthy_lane_passes_and_one_whose_branch_is_gone_is_broken(self):
        tree = os.path.join(self.tmp, "lane")
        subprocess.run(["git", "-C", self.repo, "worktree", "add", "-q", "-b", "foreman/lane", tree], check=True)
        tid = self.task("Live lane", lane=tree, lane_branch="foreman/lane")
        lanes = lambda: [f["task"] for f in d.fsck() if f["kind"] == "broken lane"]  # noqa: E731
        self.assertEqual(lanes(), [self.tid])
        subprocess.run(["git", "-C", tree, "checkout", "-q", "--detach"], check=True)
        subprocess.run(["git", "-C", self.repo, "branch", "-q", "-D", "foreman/lane"], check=True)
        self.assertEqual(sorted(lanes()), sorted([self.tid, tid]))
        self.assertIn("its branch foreman/lane is gone",
                      next(f["detail"] for f in d.fsck() if f.get("task") == tid))

    def test_a_closed_task_and_a_young_or_odd_lock_are_not_findings(self):
        b = next(x for x in c.load_briefs(self.p) if x.id == self.tid)
        b.meta["status"] = "dropped"  # a closed task's lane is fm tidy's to sweep
        c.save_brief(self.p, b)
        young = write(os.path.join(self.p.dir, "young.pid"), "")  # an empty pid file may still be getting its pid
        zero = write(os.path.join(self.p.dir, "zero.pid"), "0", age=3600)  # never os.kill(0): no process, stale
        big = write(os.path.join(self.p.dir, "big.pid"), "x" * 100, age=3600)  # not a pid file of ours: kept
        outside = write(os.path.join(self.tmp, "outside"), "1", age=3600)
        os.symlink(outside, os.path.join(self.p.dir, "link.pid"))  # a symlink is never followed nor removed
        os.mkfifo(os.path.join(self.p.dir, "pipe.jsonl"))  # a FIFO would block a plain open forever
        found = {os.path.basename(f["path"]): f for f in d.fsck() if f["kind"] == "stale lock"}
        self.assertEqual(sorted(found), ["sentinel.pid", "zero.pid"])
        self.assertNotIn("broken lane", [f["kind"] for f in d.fsck()])
        self.fm("fsck", "--fix", check=False)
        self.assertTrue(all(os.path.lexists(x) for x in (young, big, outside, os.path.join(self.p.dir, "link.pid"))))
        self.assertFalse(os.path.exists(zero))

    def test_a_journal_whose_last_line_is_whole_passes(self):
        with open(self.ledger, "a") as f:
            f.write('rt"}\n')  # the line completed
        self.assertNotIn("torn journal", [f["kind"] for f in d.fsck()])
        write(os.path.join(self.p.dir, "mail.jsonl"), '{"a": 1}\nnot json\n')
        self.assertEqual([os.path.basename(f["path"]) for f in d.fsck() if f["kind"] == "torn journal"], ["mail.jsonl"])

    def test_doctor_reports_the_one_line_summary(self):
        r = d.check_fsck()
        self.assertEqual(r.status, "WARN")
        self.assertIn("1 broken lane, 1 stale lock, 1 torn journal", r.detail)
        self.assertIn("fm fsck", r.detail)
        os.remove(self.stale)
        with open(self.ledger, "a") as f:
            f.write('rt"}\n')
        b = next(x for x in c.load_briefs(self.p) if x.id == self.tid)
        b.meta.pop("lane")
        c.save_brief(self.p, b)
        self.assertEqual(d.check_fsck().status, "PASS")


if __name__ == "__main__":
    unittest.main()
