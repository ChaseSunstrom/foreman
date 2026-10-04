"""T-0125: the self-improvement loop. fm friction digests Foreman's own friction since the last pass; fm next calls for a
pass every N closed tasks; a marked pass starts the next digest after it, which then reports what became of its items."""
import json
import os
import unittest

from helpers import ForemanTestCase

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # --focus prints its own lines after the JSON


class Friction(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def close_one(self, n):
        tid = first(self.fm("task", "new", f"tidy {n}", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus",
                                 "--json").stdout)["id"]
        self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        return tid

    def test_the_digest_names_each_kind_of_friction_and_a_pass_starts_the_next_after_it(self):
        self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "npm publish"}})  # a guard block
        tid = first(self.fm("task", "new", "Fix", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus",
                                 "--json").stdout)["id"]
        self.fm("task", "log", tid, "steer: make it faster")
        self.fm("capture", "Gates by path", "--source", "self")
        out = self.fm("friction").stdout
        for needle in ("publish", "steer: make it faster", "Gates by path"):
            self.assertIn(needle, out)
        self.assertIn("e.g. `npm publish`", out)  # T-0172: the command itself, so a false block can be grounded
        path = self.fm("friction", "--brief").stdout.strip().split()[-1]
        with open(path, encoding="utf-8") as f:
            brief = f.read()
        self.assertIn("publish", brief)  # self-contained: the digest is in it
        self.assertIn("at most 5", brief)
        self.fm("friction", "--mark")
        out = self.fm("friction").stdout
        self.assertNotIn("steer: make it faster", out)  # the next pass starts after this one
        self.assertIn("Gates by path", out)  # and reports what became of the last pass's self items (open)

    def test_failed_calls_say_why_and_a_background_wait_isnt_a_stop(self):
        # T-0301: five failed Reads of different scratch files read as one cause, and a wait isn't friction
        for i in range(3):
            self.hook("PostToolUseFailure", {"tool_name": "Read", "tool_input": {"file_path": f"/tmp/scratch{i}.md"},
                                             "error": "File does not exist."})
        self.fm("task", "new", "Fix login", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus")
        self.hook("SubagentStart", {"agent_id": "a1", "agent_type": "foreman:fm-reviewer", "session_id": "sess-1"})
        self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Waiting for the audit.",
                           "session_id": "sess-1"})
        out = self.fm("friction").stdout
        self.assertIn("3× Read: File does not exist.", out)
        self.assertNotIn("wait on background work", out)

    def test_fm_next_calls_for_a_pass_every_n_closed_tasks_at_a_task_boundary(self):
        nxt = lambda: self.fm("next").stdout
        self.close_one(1)
        self.close_one(2)
        self.assertNotIn("self-improvement pass", nxt(), "off unless the project asks for it")
        self.fm("friction", "--every", "2")
        self.assertIn("self-improvement pass", nxt())
        first(self.fm("task", "new", "Busy", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus",
                           "--json").stdout)
        self.assertNotIn("self-improvement pass", nxt(), "never in the middle of a task")

    def test_a_pass_waits_two_hours_after_the_last_so_it_has_friction_to_read(self):
        # T-0154: pass 2 came due 13 minutes after pass 1 with one new friction line
        import fmcore as c
        nxt = lambda: self.fm("next").stdout
        self.fm("friction", "--every", "1")
        self.fm("friction", "--mark")
        self.close_one(1)
        self.assertNotIn("self-improvement pass", nxt())
        p = c.find_project(self.repo)
        meta = c.read_meta(p)
        meta["rsi_at"] = c.iso(c.time.time() - 3 * 3600)
        c.write_meta(p, meta)
        self.assertIn("self-improvement pass", nxt())

    def test_the_digest_rechecks_guard_blocks_and_shows_the_trend(self):
        # T-0187: 'done since: T-0178' said nothing of whether the fix removed its friction. Each guard block is re-run
        # through today's guard (its full command from the session's transcript); a mark keeps the window's counts
        import fmcore as c
        claude = os.path.join(self.tmp, "claude")
        os.makedirs(os.path.join(claude, "projects", "x"))
        cmds = {"ls -la\npwd": "state-direct", "npm publish": "publish"}  # a block a later fix cleared; a real one
        with open(os.path.join(claude, "projects", "x", "s1.jsonl"), "w") as f:
            for cmd in cmds:
                f.write(json.dumps({"type": "assistant", "cwd": self.repo, "sessionId": "s1", "message": {"content": [
                    {"type": "tool_use", "name": "Bash", "input": {"command": cmd}}]}}) + "\n")
        at = lambda s: c.iso(c.time.time() + s)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a") as f:
            for cmd, cat in cmds.items():
                f.write(json.dumps({"ts": at(-60), "kind": "guard_block", "session_id": "s1", "category": cat,
                                    "tool": "Bash", "target": cmd, "cmd": cmd.replace("\n", " ")}) + "\n")  # as logged
            for i in range(10):
                f.write(json.dumps({"ts": at(-60), "kind": "tool", "tool": "Bash", "target": "x"}) + "\n")
        env = {"CLAUDE_CONFIG_DIR": claude}
        out = self.fm("friction", env=env).stdout
        self.assertIn("e.g. `ls -la pwd` — today's guard allows it", out)
        self.assertRegex(out, r"publish: npm publish .*still blocks")
        self.fm("friction", "--mark", env=env)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a") as f:
            for i in range(10):
                f.write(json.dumps({"ts": at(5), "kind": "tool", "tool": "Bash", "target": "x"}) + "\n")
        out = self.fm("friction", env=env).stdout
        self.assertIn("guard blocks 20 → 0", out)  # per 100 tool calls, the last pass's window against this one


if __name__ == "__main__":
    unittest.main()
