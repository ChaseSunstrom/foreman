"""T-0071 round C: memory that reaches the right moment — start-here files, effort, playbooks and age in recall,
lesson tripwires on edits, decision kinds and reversals, ruled-out digests, corrections, the focus preflight."""
import json
import os
import re
import subprocess

from helpers import ForemanTestCase

import fmcore as c
import fmrecall


class Memory(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def finished(self, title, files=(), lesson="keep the cache keyed by locale"):
        """A finished FEATURE S task that touched files (as the hooks record edits) and left a lesson."""
        self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--step", "do it", "--ac", "works", "--focus")
        tid = c.active_brief(c.load_briefs(self.p)).id
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            for rel in files:
                f.write(json.dumps({"ts": c.now(), "task": tid, "event": "touched",
                                    "data": {"file": os.path.join(self.repo, rel), "tool": "Edit"}}) + "\n")
        self.fm("task", "evidence", tid, "--ac", "1", "--run", "true")
        self.fm("task", "ac", tid, "check", "1")
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        self.fm("task", "step", tid, "done", "1")
        self.fm("task", "audit", tid, "self", "checked", "ok")
        self.fm("task", "done", tid, "--lesson", lesson)
        return tid

    def test_recall_says_where_to_start_and_how_big_similar_work_was(self):
        self.finished("translate the checkout page into german", ["web/checkout.py", "web/i18n.py"])
        out = self.fm("recall", "translate", "the", "checkout", "page", "into", "french").stdout
        self.assertIn("start here (files T-0001 touched): web/checkout.py, web/i18n.py", out)
        self.assertIn("the similar finished task took 1 steps", out)
        self.assertGreater(fmrecall._age("2000-01-01T00:00:00Z"), 9000)

    def test_recall_can_point_at_a_playbook(self):
        out = self.fm("recall", "benchmark", "optimization", "loop", "latency", "throughput", "variants").stdout
        self.assertEqual(out.count("playbook "), 1, out)
        self.assertIn("skills/playbooks/references/perf/", out)

    def test_editing_a_file_a_finished_task_left_a_lesson_about_says_it_once(self):
        self.finished("speed up the price cache", ["shop/cache.py"], lesson="invalidate on currency change")
        self.fm("task", "new", "cache warmup", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a",
                "--focus")

        def edit(rel, sid="s1"):
            r = self.hook("PreToolUse", {"tool_name": "Edit", "session_id": sid, "tool_input": {
                "file_path": os.path.join(self.repo, rel), "old_string": "a", "new_string": "b"}})
            return r.stdout
        self.assertIn("T-0001 (done) also changed this file; its lesson: invalidate on currency change",
                      edit("shop/cache.py"))
        self.assertNotIn("lesson", edit("shop/cache.py"), "once per session")
        self.assertNotIn("lesson", edit("shop/other.py"))
        self.assertIn("lesson", edit("shop/cache.py", sid="s2"))

    def test_decisions_have_kinds_and_reversals(self):
        self.fm("decide", "use sqlite for the queue", "--why", "simple", "--kind", "costly")
        self.fm("decide", "ship without a migration", "--why", "no users yet")
        self.fm("decide", "move the queue to postgres", "--why", "concurrency", "--reverses", "use sqlite")
        review = self.fm("decide", "--review").stdout
        self.assertIn("[costly] use sqlite", review)
        self.assertNotIn("migration", review)
        listing = self.fm("decide", "--list").stdout
        self.assertIn("use sqlite for the queue", listing)
        self.assertRegex(listing, r"use sqlite for the queue.*reversed later")
        self.assertIn("[reverses: use sqlite] move the queue", listing)

    def test_checkpoint_carries_what_was_ruled_out(self):
        self.fm("task", "new", "fix flaky upload", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a",
                "--focus")
        self.fm("task", "log", "T-0001", "ruled out: raising the timeout — the stall is a deadlock")
        fmrecall.note_failure(self.p, "T-0001", "Traceback\nTimeoutError: upload stalled after 30s")
        self.fm("checkpoint")
        resume = c.find_brief(self.p, "T-0001").section("Resume here")
        self.assertIn("ruled out: raising the timeout", resume)
        self.assertIn("failures met: timeouterror: upload stalled", resume)

    def test_user_corrections_are_kept_for_reflect(self):
        self.hook("UserPromptSubmit", {"prompt": "no, don't rewrite the parser, patch it"})
        self.hook("UserPromptSubmit", {"prompt": "please add a --verbose flag"})
        out = self.fm("recall", "--corrections").stdout
        self.assertIn("don't rewrite the parser", out)
        self.assertNotIn("verbose", out)

    def test_focus_warns_when_scope_files_changed_since_planning(self):
        self.fm("task", "new", "tune search", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a",
                "--scope", "src/**")
        path = c.find_brief(self.p, "T-0001").path
        with open(path) as f:
            text = f.read()
        with open(path, "w") as f:
            f.write(re.sub(r"(?m)^created: .*$", "created: 2000-01-01T00:00:00Z", text, count=1))
        os.makedirs(os.path.join(self.repo, "src"))
        with open(os.path.join(self.repo, "src", "search.py"), "w") as f:
            f.write("x = 1\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "search"], check=True)
        out = self.fm("focus", "T-0001").stdout
        self.assertIn("Changed in scope since this was planned (2000-01-01): src/search.py", out)
        self.assertIn("src/search.py", c.find_brief(self.p, "T-0001").section("Preflight"), "kept for fresh sessions")
