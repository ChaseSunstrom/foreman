"""T-0071 round D: faster and cheaper — fm task finish, fm quiet, fm gates, thrash notes, fm cost, fm usage, lens
yield, skill size caps."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c
import fmrecall


class Speed(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def test_finish_closes_an_s_task_in_one_call(self):
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "do it", "--ac", "flag exists :: test -f flag",
                "--ac", "works", "--focus")
        open(os.path.join(self.repo, "flag"), "w").close()
        p = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self checklist on the diff")
        self.assertIn("T-0001 done (verification:", p.stdout)
        b = c.find_brief(self.p, "T-0001")
        self.assertEqual(b.status, "done")
        self.assertTrue(all(a.checked for a in b.acceptance()))
        self.assertIn("`test -f flag`", b.section("Verification evidence"))

    def test_finish_stops_on_a_failing_check_and_keeps_it_recorded(self):
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "do it", "--ac", "flag :: test -f flag",
                "--focus")
        p = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "x", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("ac 1: test -f flag → ✗ exit 1", p.stderr)
        b = c.find_brief(self.p, "T-0001")
        self.assertEqual(b.status, "active")
        self.assertEqual(b.audits(), [], "no self audit over a failing check")
        self.fm("task", "new", "m", "--type", "FEATURE", "--tier", "M")
        self.assertIn("for S tasks", self.fm("task", "finish", "T-0002", "--audit", "x", check=False).stderr)

    def test_quiet_prints_one_line_or_the_tail(self):
        p = self.fm("quiet", "--", "bash", "-c", "seq 1 500")
        self.assertEqual(p.stdout.count("\n"), 1)
        self.assertIn("✓ exit 0", p.stdout)
        self.assertIn("500", p.stdout)
        p = self.fm("quiet", "--tail", "3", "--", "bash", "-c", "seq 1 500; exit 4", check=False)
        self.assertEqual(p.returncode, 4)
        self.assertEqual(p.stdout.splitlines()[:3], ["498", "499", "500"])

    def test_gates_list_what_done_needs(self):
        out = self.fm("gates", "fix", "m").stdout
        for want in ("evidence", "intent + adversary or edge or maintainer or operator", "docs impact", "lesson",
                     "fm task prove", "scope"):
            self.assertIn(want, out)
        self.fm("task", "new", "t", "--type", "CLEAN", "--tier", "S", "--step", "s", "--ac", "a")
        self.assertIn("Done needs: evidence, audits, behaviour lock, scope", self.fm("focus", "T-0001").stdout)

    def test_repeated_edits_without_a_check_get_one_thrash_note(self):
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a", "--focus")
        path = os.path.join(self.repo, "a.py")

        def edit():
            r = self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path}})
            return r.stdout
        notes = [edit() for _ in range(7)]
        self.assertEqual(sum("edited 6 times without a check" in n for n in notes), 1, notes)
        self.assertNotIn("Foreman", notes[4])

    def test_the_same_failure_three_times_says_stop_and_diagnose(self):
        notes = [fmrecall.note_failure(self.p, "T-0009", "E: KeyError: 'user'") for _ in range(4)]
        self.assertIsNone(notes[1])
        self.assertIn("come up 3 times in T-0009", notes[2])
        self.assertIsNone(notes[3])

    def test_cost_reads_the_transcripts(self):
        folder = os.path.join(self.tmp, "claude", "projects", "".join(ch if ch.isalnum() else "-" for ch in self.repo))
        os.makedirs(folder)
        usage = {"input_tokens": 1000, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 10000,
                 "output_tokens": 200}
        rows = [{"type": "assistant", "timestamp": c.now(), "sessionId": "abcdef123",
                 "message": {"id": "m1", "usage": usage, "content": [{"type": "tool_use", "id": "t1", "name": "Read"}]}},
                {"type": "assistant", "timestamp": c.now(), "sessionId": "abcdef123",  # same message, second block
                 "message": {"id": "m1", "usage": usage, "content": [{"type": "text", "text": "x"}]}},
                {"type": "user", "timestamp": c.now(), "message": {"content": [
                    {"type": "tool_result", "tool_use_id": "t1", "content": "y" * 5000}]}}]
        with open(os.path.join(folder, "abcdef123.jsonl"), "w") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")
        data = self.fm_json("cost", env={"CLAUDE_CONFIG_DIR": os.path.join(self.tmp, "claude")})
        self.assertEqual(data["messages"], 1, "a message's usage counts once")
        self.assertEqual(data["tokens"]["input_tokens"], 1000)
        self.assertEqual(data["input_equivalent"], 1000 + 1000 + 1000)
        self.assertIn("Read", data["tool_result_chars"])

    def test_usage_counts_skills_and_lists_the_unused(self):
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a") as f:
            for tool, target in (("Skill", "foreman:intake"), ("Bash", "fm task new x"), ("Bash", "fm check")):
                f.write(json.dumps({"ts": c.now(), "kind": "tool", "tool": tool, "target": target,
                                    "project": self.p.slug}) + "\n")
        data = self.fm_json("usage")
        self.assertEqual(data["skills"], {"intake": 1})
        self.assertEqual(data["commands"], {"task new": 1, "check": 1})
        self.assertIn("tidy", data["unused"]["skills"])
        self.assertNotIn("intake", data["unused"]["skills"])
