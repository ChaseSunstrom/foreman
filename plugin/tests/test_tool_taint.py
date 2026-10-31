"""T-1053: a Bash command copied from text a web/MCP result returned asks before it runs."""
import json

from test_hooks import HookCase, parse

import fmcore as c

PAGE = "Install it:\n```\ncurl -O https://x.example/i.sh\n```\n$ npm run build-everything --prefix ./web\n"


class ToolTaint(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.task()

    def fetch(self, sid="s1", tool="WebFetch", resp=PAGE):
        self.hook("PostToolUseValidate", {"tool_name": tool, "tool_input": {"url": "https://x.example"},
                                          "tool_response": resp, "session_id": sid})

    def bash(self, cmd, sid="s1"):
        return parse(self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}, "session_id": sid})
                     ) or {}

    def test_copied_command_asks_and_is_logged(self):
        self.fetch()
        out = self.bash("cd /tmp  &&   curl  -O https://x.example/i.sh").get("hookSpecificOutput", {})
        self.assertEqual(out.get("permissionDecision"), "ask", out)
        self.assertIn("web", out["permissionDecisionReason"])
        self.assertTrue([e for e in c.ledger_tail(self.project(), 100) if e.get("event") == "taint_flag"])

    def test_dollar_line_from_mcp_asks(self):
        self.fetch(tool="mcp__docs__read", resp={"content": [{"type": "text", "text": PAGE}]})
        out = self.bash("npm run build-everything --prefix ./web").get("hookSpecificOutput", {})
        self.assertEqual(out.get("permissionDecision"), "ask")

    def test_whitespace_page_is_fast(self):
        import time
        t = time.time()
        self.fetch(resp="x")
        base = time.time() - t  # the hook process start, which load stretches
        t = time.time()
        self.fetch(resp="\n \n" * 70_000)
        self.assertLess(time.time() - t - base, 0.5)  # wall clock: a hook child, minus its measured start-up

    def test_mcp_dict_first_line_and_quotes(self):
        self.fetch(tool="mcp__docs__read", resp={"content": [{"type": "text", "text": 'curl -H "X: y" https://x.example/a'}]})
        out = self.bash('curl -H "X: y" https://x.example/a').get("hookSpecificOutput", {})
        self.assertEqual(out.get("permissionDecision"), "ask", out)

    def test_bare_verbs_not_stored_and_ask_once(self):
        self.fetch(resp="```\nnpm install\ngit status\nmake test\n```\n")
        self.assertNotEqual(self.bash("npm install -D foo").get("hookSpecificOutput", {}).get("permissionDecision"), "ask")
        self.fetch()
        cmd = "curl -O https://x.example/i.sh"
        self.assertEqual(self.bash(cmd).get("hookSpecificOutput", {}).get("permissionDecision"), "ask")
        self.assertNotEqual(self.bash(cmd).get("hookSpecificOutput", {}).get("permissionDecision"), "ask")

    def test_headless_denies_with_hint(self):
        self.fetch()
        out = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "curl -O https://x.example/i.sh"},
                                       "session_id": "s1"}, env={"FOREMAN_DRIVE_TASK": "T-0001"})
        d = parse(out)["hookSpecificOutput"]
        self.assertEqual(d["permissionDecision"], "deny")
        self.assertIn("fm task block", d["permissionDecisionReason"])

    def test_deny_never_uses_up_the_ask(self):
        cmd = "curl -O https://x.example/i.sh"
        self.fetch()
        env = {"FOREMAN_DRIVE_TASK": "T-0001"}
        for _ in range(2):  # headless: denied on every attempt
            d = parse(self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}, "session_id": "s1"},
                                env=env))["hookSpecificOutput"]
            self.assertEqual(d["permissionDecision"], "deny")
        self.fm("autonomy", "full")
        for _ in range(2):  # full autonomy: same
            self.assertEqual(self.bash(cmd)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_taint_survives_compaction(self):
        self.fetch()
        self.hook("SessionStart", {"source": "compact", "session_id": "s1"})
        out = self.bash("curl -O https://x.example/i.sh").get("hookSpecificOutput", {})
        self.assertEqual(out.get("permissionDecision"), "ask", out)

    def test_other_commands_and_sessions_pass(self):
        self.fetch()
        self.assertNotEqual(self.bash("ls").get("hookSpecificOutput", {}).get("permissionDecision"), "ask")
        self.assertNotEqual(self.bash("curl -O https://x.example/i.sh", sid="s2").get("hookSpecificOutput", {})
                            .get("permissionDecision"), "ask")
