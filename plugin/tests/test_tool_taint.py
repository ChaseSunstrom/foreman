"""T-1053: a Bash command copied from text a web/MCP result returned asks before it runs."""
import json
import os

from test_hooks import HookCase, parse

from sampo import core as c

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
        self.assertIn("sampo task block", d["permissionDecisionReason"])

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

    CMD = "curl -O https://x.example/i.sh"

    def store(self, data):
        from sampo import hooks
        path = hooks._taint_path("s1")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(data)
        return path

    def test_a_store_read_mid_write_still_asks(self):
        # T-3577: the store is read once without the lock; a read that finds it cut short (a writer mid-write) falls
        # through to the locked read, which decides
        from unittest import mock
        from sampo import hooks
        path, whole, reads = self.store(json.dumps({"lines": [self.CMD]})), json.load, []
        cut = json.dumps({"lines": [self.CMD]})[:-1]  # {"lines": ["…"] cut short

        def load(f, *a, **k):
            if getattr(f, "name", None) == path:
                reads.append(f)
                if len(reads) == 1:
                    return json.loads(cut)  # the unlocked read finds it cut short: ValueError
            return whole(f, *a, **k)
        with mock.patch.object(hooks.json, "load", load):
            got = hooks._taint_check({"session_id": "s1", "tool_input": {"command": self.CMD}}, self.project())
        self.assertEqual((got[0], len(reads)), ("ask", 2), got)
        with open(path) as f:
            self.assertEqual(json.load(f)["asked"], [self.CMD])

    def test_a_line_already_asked_passes_without_the_lock(self):
        path = self.store(json.dumps({"lines": [self.CMD], "asked": [self.CMD]}))
        before = os.stat(path)
        self.assertNotEqual(self.bash(self.CMD).get("hookSpecificOutput", {}).get("permissionDecision"), "ask")
        self.assertFalse(os.path.exists(path[:-5] + ".lock"), "no lock taken, no store rewritten")
        self.assertEqual(os.stat(path).st_mtime_ns, before.st_mtime_ns)

    def test_other_commands_and_sessions_pass(self):
        self.fetch()
        self.assertNotEqual(self.bash("ls").get("hookSpecificOutput", {}).get("permissionDecision"), "ask")
        self.assertNotEqual(self.bash("curl -O https://x.example/i.sh", sid="s2").get("hookSpecificOutput", {})
                            .get("permissionDecision"), "ask")
