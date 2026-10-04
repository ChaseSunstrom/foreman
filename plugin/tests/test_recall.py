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
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
        return self.fm("task", "done", tid, *(["--lesson", lesson] if lesson else []), check=False)

    def test_a_note_whose_cited_file_changed_is_marked_stale(self):
        # T-0210: research about code goes stale when that code changes after it
        import os
        import subprocess
        import time
        path = os.path.join(self.repo, "auth", "session.py")
        os.makedirs(os.path.dirname(path))
        with open(path, "w") as f:
            f.write("TIMEOUT = 30\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "session"], check=True)
        note = os.path.join(c.find_project(self.repo).dir, "research", "auth-notes.md")
        os.utime(note, (time.time() + 60, time.time() + 60))  # written after that commit
        out = self.fm("recall", "session renewal timeout on login").stdout
        self.assertIn("auth-notes", out)
        self.assertNotIn("stale", out, "the file didn't change after the note")
        os.utime(note, (time.time() - 3600, time.time() - 3600))
        with open(path, "w") as f:
            f.write("TIMEOUT = 60\n")
        subprocess.run(["git", "-C", self.repo, "commit", "-qam", "longer"], check=True)
        out = self.fm("recall", "session renewal timeout on login").stdout
        line = next(x for x in out.splitlines() if "auth-notes" in x)
        self.assertIn("stale", line)
        self.assertIn("auth/session.py", line)

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


class RedGreen(ForemanTestCase):
    """T-0045: a FIX is proven by its regression test failing before and passing after."""

    def fix(self):
        self.fm("init")
        tid = json.loads(self.fm("task", "new", "Fix the parser", "--type", "FIX", "--tier", "S", "--ac", "parses",
                                 "--step", "fix it", "--json").stdout)["id"]
        self.fm("focus", tid)
        self.fm("task", "audit", tid, "self", "x", "ok")
        return tid

    def close(self, tid):
        self.fm("task", "step", tid, "done", "1", check=False)
        self.fm("task", "ac", tid, "check", "1", "--evidence", "true", "ok", check=False)
        return self.fm("task", "done", tid, check=False)

    def test_a_fix_without_a_failing_run_first_is_not_done(self):
        tid = self.fix()
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        p = self.close(tid)
        self.assertEqual(p.returncode, 2)
        self.assertIn("red→green", p.stderr)
        self.assertIn(f"fm task prove {tid}", p.stderr)  # T-0085: the rules no longer say it, so the refusal does

    def test_fail_then_pass_of_the_same_command_proves_it(self):
        tid = self.fix()
        flag = f"{self.tmp}/fixed"
        cmd = f"test -e {flag}"
        self.fm("task", "evidence", tid, "--step", "1", "--run", cmd, check=False)  # red
        open(flag, "w").close()
        self.fm("task", "evidence", tid, "--step", "1", "--run", cmd)  # green
        self.assertEqual(self.close(tid).returncode, 0)

    def test_a_stated_reason_for_no_regression_test_is_accepted(self):
        tid = self.fix()
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: a config typo, nothing to test")
        self.assertEqual(self.close(tid).returncode, 0)


class FailureMemory(ForemanTestCase):
    """T-0046: a failure seen and fixed in an earlier task is pointed out when it happens again."""
    ERR = "Exit code 1\nTraceback (most recent call last):\n  File \"/tmp/a/{f}.py\", line {n}\nModuleNotFoundError: No module named 'yaml'"

    def failing(self, n=12, f="parser"):
        return self.hook("PostToolUseFailure", {"tool_name": "Bash", "tool_input": {"command": "python3 x.py"},
                                                "error": self.ERR.format(n=n, f=f)})

    def task(self, title, lesson=None):
        tid = json.loads(self.fm("task", "new", title, "--type", "CLEAN", "--tier", "S", "--ac", "ok", "--step", "do",
                                 "--json").stdout)["id"]
        self.fm("focus", tid)
        return tid

    def test_a_failure_fixed_in_an_earlier_task_is_pointed_out(self):
        import fmrecall
        self.fm("init")
        first = self.task("Tidy the YAML loader")
        sighting = json.loads(self.failing().stdout or "null") or {}
        self.assertNotIn("came up in", json.dumps(sighting), "first sighting: no earlier task to point to")
        self.fm("task", "step", first, "done", "1", "--evidence", "x", "ok")
        self.fm("task", "ac", first, "check", "1", "--evidence", "x", "ok")
        self.fm("task", "audit", first, "self", "x", "ok")
        self.fm("task", "done", first, "--lesson", "add PyYAML to requirements.txt")
        self.task("Tidy the config reader")
        ctx = json.loads(self.failing(n=40, f="config").stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn(first, ctx)
        self.assertIn("PyYAML", ctx)
        self.assertEqual(fmrecall.failure_signature(self.ERR.format(n=1, f="a")),
                         fmrecall.failure_signature(self.ERR.format(n=99, f="b")))
        other = self.hook("PostToolUseFailure", {"tool_name": "Bash", "tool_input": {"command": "make"},
                                                 "error": "Exit code 2\nmake: *** No rule to make target 'all'"})
        self.assertEqual(other.stdout.strip(), "")
