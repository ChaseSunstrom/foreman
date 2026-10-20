"""T-1257: fm cost says how much of what entered the context was Foreman's own: its hook notes, fm commands' output,
its rules, skill and agent listing lines and output style, read from the transcripts Claude Code keeps."""
import datetime
import json
import os

from test_hooks import HookCase


class ForemanShare(HookCase):
    def test_cost_counts_foremans_own_share_of_the_context(self):
        self.fm("init")
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", "".join(ch if ch.isalnum() else "-" for ch in self.repo))
        os.makedirs(folder)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        att = lambda a: {"type": "attachment", "timestamp": now, "attachment": a}
        bash = lambda i, cmd: {"type": "tool_use", "id": i, "name": "Bash", "input": {"command": cmd}}
        lines = [
            {"type": "assistant", "timestamp": now, "sessionId": "s1", "message": {
                "id": "m1", "usage": {"input_tokens": 10, "output_tokens": 5},
                "content": [bash("t1", "fm task show T-0001"), bash("t2", "ls -la")]}},
            {"type": "user", "timestamp": now, "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t1", "content": "x" * 998},
                {"type": "tool_result", "tool_use_id": "t2", "content": "y" * 498}]}},
            att({"type": "hook_additional_context", "content": ["Foreman: " + "a" * 491], "hookEvent": "PreToolUse"}),
            att({"type": "hook_additional_context", "content": ["Ambient tests: " + "a" * 85], "hookEvent": "PreToolUse"}),
            att({"type": "hook_additional_context", "content": ["[from another plugin] " + "b" * 278]}),
            att({"type": "skill_listing", "content": "- foreman:next: " + "c" * 83 + "\n- graphify: " + "d" * 187}),
            att({"type": "agent_listing_delta", "addedLines": ["- foreman:fm-scout: " + "e" * 30, "- Explore: f"]}),
            att({"type": "output_style_instructions", "style": {"name": "foreman:Foreman", "prompt": "p" * 200}}),
            att({"type": "instructions", "files": [{"path": "/x/foreman/plugin/rules/foreman.md", "content": "r" * 300},
                                                   {"path": "/home/u/.claude/CLAUDE.md", "content": "u" * 100}]}),
        ]
        with open(os.path.join(folder, "s1.jsonl"), "w") as f:
            f.write("\n".join(json.dumps(x) for x in lines) + "\n")
        env = {"CLAUDE_CONFIG_DIR": cfg}
        share = self.fm_json("cost", env=env)["foreman_share"]
        got = share["chars"]
        self.assertEqual(got["hook notes"], 600, "Foreman's two notes, not the other plugin's")
        self.assertEqual(got["fm output"], 1000, "the fm command's result, not ls's")
        self.assertEqual(got["rules"], 300)
        self.assertEqual(got["output style"], 200)
        self.assertEqual(got["skill listing"], 100)
        self.assertEqual(got["agent listing"], 51)
        self.assertGreater(share["all"], sum(got.values()))
        self.assertIn("Foreman's own share of what entered the context", self.fm("cost", env=env).stdout)


if __name__ == "__main__":
    import unittest
    unittest.main()
