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

    def test_a_send_without_its_text_says_how_instead_of_crashing(self):
        p = self.fm("bus", "send", "sess-2", check=False)
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn('fm bus send <session|all> "<text>"', p.stderr)

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

    def test_a_watcher_ended_by_a_signal_drops_its_heartbeat(self):
        # T-0819: Claude Code ends a monitor with a signal, which skipped the finally: watch-<sid> outlived the session
        import signal
        import subprocess
        import sys
        import time
        import fmbus
        from helpers import FM
        beat = os.path.join(fmbus._dir(), "watch-sess-sig")
        for sig in (signal.SIGTERM, signal.SIGHUP):
            w = subprocess.Popen([sys.executable, FM, "bus", "watch", "sess-sig"], cwd=self.repo,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                for _ in range(200):
                    if os.path.exists(beat):
                        break
                    time.sleep(0.05)
                self.assertTrue(os.path.exists(beat))
                w.send_signal(sig)
                w.wait(10)
            finally:
                w.kill()
            self.assertFalse(os.path.exists(beat), f"{sig.name} left the heartbeat")

    def test_session_start_survives_a_racing_cleanup_and_keeps_to_its_own_claude(self):
        # T-0820 (round-1 review): an overlapping SessionStart removing the same dead entry crashed record_pid, and a
        # claude -p run from a session's Bash re-mapped that session's claude to itself
        import fmbus
        d = os.path.join(self.home, "state", "sessions", "by-pid")
        os.makedirs(d, exist_ok=True)
        real_remove, real_chain = os.remove, fmbus._chain
        def racing_remove(path):
            real_remove(path)
            raise FileNotFoundError(path)  # the other SessionStart got there first
        open(os.path.join(d, "999999"), "w").close()  # a dead pid's entry
        names = {101: "sh", 102: "claude", 103: "bash", 104: "claude"}  # hook → sh → child claude -p → bash → parent
        os.remove, fmbus._chain = racing_remove, lambda pid, depth: [(p, "t") for p in names][:depth]
        real_comm = fmbus._comm if hasattr(fmbus, "_comm") else None
        fmbus._comm = lambda pid: names.get(pid, "")
        try:
            fmbus.record_pid("sess-child")
        finally:
            os.remove, fmbus._chain = real_remove, real_chain
            if real_comm:
                fmbus._comm = real_comm
        self.assertEqual(sorted(os.listdir(d)), ["101", "102"], "up to its own claude, not the parent session's")

    def test_it_finds_its_session_from_the_session_start_hook(self):
        import fmbus
        saved = {k: os.environ.pop(k, None) for k in ("CLAUDE_CODE_SESSION_ID", "FOREMAN_SESSION_ID")}
        try:
            self.assertIsNone(fmbus.own_session())
            self.hook("SessionStart", {"session_id": "sess-pid", "source": "startup"})
            self.assertEqual(fmbus.own_session(), "sess-pid", "this process is the hook's parent")
        finally:
            os.environ.update({k: v for k, v in saved.items() if v})

    def test_a_resumed_session_keeps_its_watcher(self):
        # T-0841 (live, 2026-10-15): Claude Code started as one session, then resumed this conversation under another
        # id; the monitor kept the first id from its environment, so the resumed session's mail never printed
        import io
        import threading
        import time
        import fmbus
        saved = {k: os.environ.pop(k, None) for k in ("CLAUDE_CODE_SESSION_ID", "FOREMAN_SESSION_ID")}
        buf, done = io.StringIO(), threading.Event()
        try:
            self.hook("SessionStart", {"session_id": "sess-first", "source": "startup"})
            t = threading.Thread(target=fmbus.watch, kwargs={"interval": 0.05, "out": buf, "stop": done.is_set})
            t.start()
            time.sleep(0.3)
            self.hook("SessionStart", {"session_id": "sess-resumed", "source": "resume"})
            time.sleep(0.3)
            fmbus.send("sess-resumed", "picked up after the resume", sender="sess-1")
            for _ in range(100):
                if "picked up" in buf.getvalue():
                    break
                time.sleep(0.05)
        finally:
            done.set()
            t.join(5)
            os.environ.update({k: v for k, v in saved.items() if v})
        self.assertIn("picked up after the resume", buf.getvalue())

    def test_a_resume_in_the_same_claude_process_is_not_another_session(self):
        # T-0841: the same live resume told the session another one (its own first id) was active 0m ago
        import fmhooks
        now = c.now()
        self.assertIsNone(fmhooks._other_session({"id": "sess-first", "seen": now, "pid": 4242}, "sess-b", 4242))
        self.assertIn("Another Claude Code session",
                      fmhooks._other_session({"id": "sess-first", "seen": now, "pid": 4242}, "sess-b", 999) or "")
        self.assertIn("Another Claude Code session",
                      fmhooks._other_session({"id": "sess-first", "seen": now}, "sess-b", None) or "", "unknown: as before")

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

    def test_drop_confirms_what_it_dropped_and_lists_no_other_lease(self):
        # T-1729: a drop printed another session's lease line as its result, not the caller's own drop
        a, b = {"CLAUDE_CODE_SESSION_ID": "sess-a"}, {"CLAUDE_CODE_SESSION_ID": "sess-b"}
        self.fm("lease", "take", "a.py::f", "b.py", env=a)
        self.fm("lease", "take", "c.py", env=b)
        out = self.fm("lease", "drop", env=a).stdout
        self.assertIn("Dropped 2 lease(s)", out)
        self.assertIn("dropped: a.py::f", out)
        self.assertIn("dropped: b.py::*", out)
        self.assertNotIn("c.py", out, "another session's lease isn't the drop's result")
        self.assertIn("c.py", self.fm("lease", "list").stdout)


    def test_a_fm_code_workers_edits_lease_as_the_run_so_the_run_and_its_next_worker_edit_on(self):
        """T-1294: each worker turn is its own Claude session; leasing under it made fm code's judge put the
        worker's fix back, and the next turn's session was refused the same function."""
        path = os.path.join(self.repo, "mod.py")
        with open(path, "w") as f:
            f.write(MOD.replace("x + 1", "x + 2"))
        run = {"FOREMAN_WORKER_OF": "fm-code-T-0001"}
        self.hook("PostToolUse", {"tool_name": "Edit", "session_id": "worker-turn-1", "tool_response": {},
                                  "tool_input": {"file_path": path, "old_string": "x + 1", "new_string": "x + 2"}},
                  env=run)
        edit = {"tool_name": "Edit", "tool_input": {"file_path": path, "old_string": "a = x + 2", "new_string": "a = x"}}
        for sid, env in (("fm-code-T-0001", None), ("worker-turn-2", run)):
            out = (parse(self.hook("PreToolUse", dict(edit, session_id=sid), env=env)) or {}).get(
                "hookSpecificOutput") or {}
            self.assertNotEqual(out.get("permissionDecision"), "deny", f"{sid}: the run's own lease")
        out = (parse(self.hook("PreToolUse", dict(edit, session_id="someone-else"))) or {}).get("hookSpecificOutput") or {}
        self.assertEqual(out.get("permissionDecision"), "deny", "a session outside the run is still refused")
        stray = {"FOREMAN_WORKER_OF": "my-shell-rc"}  # only fm code's own value names a run
        out = (parse(self.hook("PreToolUse", dict(edit, session_id="someone-else"), env=stray)) or {}).get(
            "hookSpecificOutput") or {}
        self.assertEqual(out.get("permissionDecision"), "deny", "a stray FOREMAN_WORKER_OF isn't a run")


class Conductor(Base):
    def test_a_session_whose_claude_is_gone_or_a_one_off_isnt_listed(self):
        # T-1001: killed UI-harness sessions stayed 'live' for 15 minutes and filled the pane's More lines
        import subprocess
        from helpers import PLUGIN
        self.snap("live0001")
        self.snap("dead0001")
        gone = subprocess.Popen(["true"])
        gone.wait()
        d = os.path.join(self.home, "state", "sessions", "by-pid")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, str(gone.pid)), "w") as f:
            json.dump({"sid": "dead0001", "start": "1"}, f)
        out = self.fm("conductor").stdout
        self.assertIn("live0001", out)
        self.assertNotIn("dead0001", out)
        subprocess.run([os.path.join(PLUGIN, "hooks", "statusline")], input=json.dumps({"session_id": "sess-oneoff", "cwd": self.repo}),
                       text=True, capture_output=True, timeout=15, cwd=self.repo,
                       env=dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_ONEOFF="1"))
        self.assertFalse(os.path.exists(os.path.join(self.home, "state", "sessions", "sess-oneoff.json")))

    def test_a_snapshot_naming_a_dead_or_reused_claude_pid_isnt_listed(self):
        # T-1003: a later SessionStart swept the by-pid records, so the snapshot has to carry its own pid
        import subprocess
        self.snap("live0002", claude_pid=os.getpid(), claude_start=self.start_of(os.getpid()))
        self.snap("reuse002", claude_pid=os.getpid(), claude_start="1")
        gone = subprocess.Popen(["true"])
        gone.wait()
        self.snap("dead0002", claude_pid=gone.pid, claude_start="1")
        out = self.fm("conductor").stdout
        self.assertIn("live0002", out)
        self.assertNotIn("dead0002", out)
        self.assertNotIn("reuse002", out)

    @staticmethod
    def start_of(pid):  # T-1249: as fmbus reads it, ps where there's no /proc (macOS)
        import fmbus
        return fmbus._proc(pid)[1]

    def test_it_lists_live_sessions_and_its_steer_reaches_them(self):
        self.snap("sess-x", context_pct=41)
        self.snap("sess-y", ts="2020-01-01T00:00:00Z")
        out = self.fm("conductor").stdout
        self.assertIn("sess-x", out)
        self.assertNotIn("sess-y", out, "not seen for years: not live")
        self.fm("conductor", "steer", "stop touching the guard")
        self.assertIn("stop touching the guard", self.note("sess-x")[1].get("additionalContext", ""))


class FailingMark(HookCase):
    """T-1449: one note builder raising (a full disk failed the bus's seen-mark write) dropped every PreToolUse note."""

    def test_a_failing_mark_write_keeps_the_other_notes_and_the_mail(self):
        self.fm("init")
        tid = self.task(scope=["src/auth/**"])
        self.fm("bus", "send", "sess-2", "use the new parser", env={"CLAUDE_CODE_SESSION_ID": "sess-1"})
        bus = os.path.join(self.home, "state", "bus")
        os.chmod(bus, 0o555)  # the mark can't be written, as on a full disk
        try:
            r = self.hook("PreToolUse", {"tool_name": "Edit", "session_id": "sess-2", "tool_input": {
                "file_path": os.path.join(self.repo, "docs", "x.md"), "old_string": "a", "new_string": "b"}})
        finally:
            os.chmod(bus, 0o755)
        ctx = ((parse(r) or {}).get("hookSpecificOutput") or {}).get("additionalContext", "")
        self.assertIn(f"outside {tid} scope", ctx)
        self.assertIn("use the new parser", ctx)
