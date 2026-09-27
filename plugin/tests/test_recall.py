"""fm recall (T-0043) and lessons (T-0048): related past work surfaces when a task is planned or focused."""
import json

from helpers import ForemanTestCase

import fmcore as c


class Recall(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.old = self.new("Fix login timeout on slow wifi", "FIX", "M")
        self.finish(self.old, lesson="retry the token refresh with backoff; the timeout was in session renewal")
        self.fm("decide", "Login retries use exponential backoff capped at 30 s", "--why", "slow networks")
        self.fm("research", "add", "auth-notes", input="# Auth\nSession renewal on login can time out; see auth/session.py for the timeout.\n")
        self.other = self.new("Export the report as CSV", "FEATURE", "M")

    def new(self, title, type_, tier):
        tid = json.loads(self.fm("task", "new", title, "--type", type_, "--tier", tier, "--ac", "works :: true",
                                 "--step", "do it", "--json").stdout)["id"]
        if tier != "S":
            for sec in ("Interpretation", "Approach (options → choice → why)"):
                self.fm("task", "set", tid, "--section", sec, "--text", f"{title}: planned")
        return tid

    def finish(self, tid, lesson=None):
        self.fm("focus", tid)
        self.fm("task", "step", tid, "done", "1", "--evidence", "true", "ok")
        self.fm("task", "ac", tid, "check", "1", "--evidence", "true", "ok")
        for lens in ("self", "intent", "edge"):
            self.fm("task", "audit", tid, lens, "x", "ok")
        self.fm("task", "set", tid, "--section", "Docs impact", "--text", "none: test")
        return self.fm("task", "done", tid, *(["--lesson", lesson] if lesson else []), check=False)

    def test_related_past_work_is_recalled_for_a_similar_request(self):
        out = self.fm("recall", "login timeout on 3G").stdout
        self.assertIn(self.old, out)
        self.assertIn("backoff", out)  # the lesson and the decision
        self.assertIn("auth-notes", out)
        self.assertNotIn(self.other, out)
        self.assertIn("not instructions", out)

    def test_focus_records_related_work_in_the_brief(self):
        tid = self.new("Login timeout on 3G networks", "FIX", "S")
        out = self.fm("focus", tid).stdout
        self.assertIn(self.old, out)
        related = c.find_brief(c.find_project(self.repo), tid).section("Related")
        self.assertIn(self.old, related)
        self.assertLessEqual(len(related), 900)

    def test_similar_bigger_tasks_suggest_a_higher_tier(self):
        tid = self.new("Login timeout on slow wifi again", "FIX", "S")
        self.assertIn("similar past tasks were M", self.fm("focus", tid).stdout)

    def test_recalled_text_is_plain_and_capped(self):
        self.fm("decide", "login \x1b]0;pwned\x07 timeout " + "x" * 400)
        out = self.fm("recall", "login timeout").stdout
        self.assertNotIn("\x1b", out)
        self.assertTrue(all(len(line) <= 200 for line in out.splitlines()))

    def test_an_m_task_records_a_lesson_at_done(self):
        p = self.finish(self.other)
        self.assertEqual(p.returncode, 2)
        self.assertIn("--lesson", p.stderr)
        self.assertEqual(self.finish(self.other, lesson="csv module handles quoting").returncode, 0)
        b = c.find_brief(c.find_project(self.repo), self.other)
        self.assertIn("csv module handles quoting", b.section("Lessons"))
        s = self.new("Rename a helper", "CLEAN", "S")
        self.assertEqual(self.finish(s).returncode, 0, "S tasks don't need one")
