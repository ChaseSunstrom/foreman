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


class Watch(Base):
    """T-0777: a plugin monitor runs fm bus watch for the whole session; each line it prints wakes Claude."""

    def test_it_prints_each_new_message_for_its_session_once(self):
        import io
        import threading
        import time
        import fmbus
        fmbus.send("sess-w", "old news", sender="sess-1")
        buf, done = io.StringIO(), threading.Event()
        t = threading.Thread(target=fmbus.watch, kwargs={"sid": "sess-w", "interval": 0.05, "out": buf,
                                                         "stop": done.is_set})
        t.start()
        try:
            beat = os.path.join(fmbus._dir(), "watch-sess-w")
            for _ in range(100):
                if os.path.exists(beat):
                    break
                time.sleep(0.05)
            self.assertTrue(os.path.exists(beat), "the watcher keeps a heartbeat")
            fmbus.send("sess-w", "use the new parser", sender="sess-1")
            fmbus.send("sess-z", "not yours", sender="sess-1")
            fmbus.send("all", "freeze the API", kind="steer", sender="sess-1")
            for _ in range(100):
                if buf.getvalue().count("\n") >= 2:
                    break
                time.sleep(0.05)
            time.sleep(0.3)  # more polls: nothing printed twice
        finally:
            done.set()
            t.join(5)
        lines = buf.getvalue().splitlines()
        self.assertEqual(len(lines), 2, lines)
        self.assertIn("use the new parser", lines[0])
        self.assertIn("freeze the API", lines[1])
        self.assertIn("fm bus read", lines[0])
        self.assertNotIn("not yours", buf.getvalue())
        self.assertNotIn("old news", buf.getvalue())
        self.assertFalse(os.path.exists(beat), "a stopped watcher drops its heartbeat")
        self.assertIn("use the new parser", self.note("sess-w")[1].get("additionalContext", ""), "never marks read")

    def test_it_finds_its_session_from_the_session_start_hook(self):
        import fmbus
        saved = {k: os.environ.pop(k, None) for k in ("CLAUDE_CODE_SESSION_ID", "FOREMAN_SESSION_ID")}
        try:
            self.assertIsNone(fmbus.own_session())
            self.hook("SessionStart", {"session_id": "sess-pid", "source": "startup"})
            self.assertEqual(fmbus.own_session(), "sess-pid", "this process is the hook's parent")
        finally:
            os.environ.update({k: v for k, v in saved.items() if v})

    def test_wake_prefers_a_fresh_watcher_over_tmux(self):
        import time
        import fmbus
        bin_ = os.path.join(self.tmp, "bin")
        os.makedirs(bin_)
        log = os.path.join(self.tmp, "tmux.log")
        with open(os.path.join(bin_, "tmux"), "w") as f:
            f.write(f"#!/bin/sh\necho \"$@\" >> {log}\n")
        os.chmod(os.path.join(bin_, "tmux"), 0o755)
        env = {"PATH": bin_ + os.pathsep + os.environ["PATH"]}
        self.snap("sess-w", tmux_pane="%7")
        beat = os.path.join(fmbus._dir(), "watch-sess-w")
        open(beat, "w").close()
        self.assertIn("woke 1", self.fm("bus", "send", "sess-w", "hi", "--wake", env=env).stdout)
        self.assertFalse(os.path.exists(log), "the watcher delivers it: nothing typed into tmux")
        os.utime(beat, (time.time() - 60, time.time() - 60))
        self.assertIn("woke 1", self.fm("bus", "send", "sess-w", "hi again", "--wake", env=env).stdout)
        self.assertTrue(os.path.exists(log), "a stale watcher: tmux stays the fallback")

    def test_the_monitor_entry_uses_only_the_keys_claude_code_reads(self):
        # strict keys, and `claude plugin validate --strict` doesn't check them
        root = os.path.join(os.path.dirname(__file__), "..")
        with open(os.path.join(root, "monitors", "monitors.json")) as f:
            entries = json.load(f)
        for e in entries:
            self.assertLessEqual(set(e), {"name", "command", "description", "when"}, e)
            self.assertIn("${CLAUDE_PLUGIN_ROOT}/bin/fm bus watch", e["command"])
            self.assertTrue(os.access(os.path.join(root, "bin", "fm"), os.X_OK))


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
