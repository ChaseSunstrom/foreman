"""T-1053: a Bash command copied from text a web/MCP result returned asks before it runs."""
import json

from test_hooks import HookCase, parse

import fmcore as c

PAGE = "Install it:\n```\ncurl -O https://x.example/i.sh\n```\n$ npm run build-everything\n"


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
        out = self.bash("npm run build-everything").get("hookSpecificOutput", {})
        self.assertEqual(out.get("permissionDecision"), "ask")

    def test_other_commands_and_sessions_pass(self):
        self.fetch()
        self.assertNotEqual(self.bash("ls").get("hookSpecificOutput", {}).get("permissionDecision"), "ask")
        self.assertNotEqual(self.bash("curl -O https://x.example/i.sh", sid="s2").get("hookSpecificOutput", {})
                            .get("permissionDecision"), "ask")
