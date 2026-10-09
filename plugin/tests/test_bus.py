"""T-0708 (Frontier 08, first slice): sessions on one machine message each other through the hooks that already run,
lease the functions they edit, and one conductor lists and steers them all."""
import json
import os

from test_hooks import HookCase, parse

import fmcore as c

MOD = "def f(x):\n    a = x + 1\n    return a\n\n\ndef g(y):\n    b = y * 2\n    return b\n"


class Base(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.task()

    def note(self, session, tool="Bash", ti=None):
        r = self.hook("PreToolUse", {"tool_name": tool, "tool_input": ti or {"command": "ls"}, "session_id": session})
        return r, (parse(r) or {}).get("hookSpecificOutput") or {}

    def snap(self, sid, **kw):
        d = os.path.join(self.home, "state", "sessions")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"{sid}.json"), "w") as f:
            json.dump(dict({"ts": c.now(), "session_id": sid, "project": self.project().slug, "cwd": self.repo,
                            "context_pct": 30}, **kw), f)


class Bus(Base):
    def test_a_message_reaches_its_session_once_and_all_reach_everyone(self):
        self.fm("bus", "send", "sess-2", "use the new parser", env={"CLAUDE_CODE_SESSION_ID": "sess-1"})
        _, out = self.note("sess-2")
        self.assertIn("use the new parser", out.get("additionalContext", ""))
        self.assertNotIn("use the new parser", self.note("sess-2")[1].get("additionalContext", ""), "once")
        self.assertNotIn("use the new parser", self.note("sess-3")[1].get("additionalContext", ""), "not addressed")
        self.fm("bus", "send", "all", "freeze the API", "--type", "steer")
        self.assertIn("freeze the API", self.note("sess-3")[1].get("additionalContext", ""))
        self.assertIn("freeze the API", self.note("sess-2")[1].get("additionalContext", ""))

    def test_unread_mail_keeps_a_session_from_stopping(self):
        self.fm("bus", "send", "sess-9", "one more thing: bump the version")
        r = parse(self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Done.", "session_id": "sess-9"}))
        self.assertEqual((r or {}).get("decision"), "block")
        self.assertIn("bump the version", r["reason"])


class Lease(Base):
    def test_an_edit_leases_its_function_against_other_sessions(self):
        path = os.path.join(self.repo, "mod.py")
        with open(path, "w") as f:
            f.write(MOD.replace("x + 1", "x + 2"))
        self.hook("PostToolUse", {"tool_name": "Edit", "session_id": "sess-a", "tool_response": {},
                                  "tool_input": {"file_path": path, "old_string": "x + 1", "new_string": "x + 2"}})
        r, out = self.note("sess-b", "Edit", {"file_path": path, "old_string": "a = x + 2", "new_string": "a = x"})
        self.assertEqual(out.get("permissionDecision"), "deny", r.stdout + r.stderr)
        self.assertIn("leased", out.get("permissionDecisionReason", ""))
        _, out = self.note("sess-b", "Edit", {"file_path": path, "old_string": "b = y * 2", "new_string": "b = y"})
        self.assertNotEqual(out.get("permissionDecision"), "deny", "another function is free")
        _, out = self.note("sess-a", "Edit", {"file_path": path, "old_string": "a = x + 2", "new_string": "a = x"})
        self.assertNotEqual(out.get("permissionDecision"), "deny", "the holder edits on")
        self.assertIn("mod.py", self.fm("lease", "list").stdout)


class Conductor(Base):
    def test_it_lists_live_sessions_and_its_steer_reaches_them(self):
        self.snap("sess-x", context_pct=41)
        self.snap("sess-y", ts="2020-01-01T00:00:00Z")
        out = self.fm("conductor").stdout
        self.assertIn("sess-x", out)
        self.assertNotIn("sess-y", out, "not seen for years: not live")
        self.fm("conductor", "steer", "stop touching the guard")
        self.assertIn("stop touching the guard", self.note("sess-x")[1].get("additionalContext", ""))
