"""T-3582: the prompt and session-start hooks, sampo capture and task new hold the project lock only for their writes;
the brief load, the state and the view regeneration run after it (T-3558's pattern), and what they record still lands."""
import contextlib
import fcntl
import io
import json
import os
from unittest import mock

from helpers import ForemanTestCase

from sampo import cli, hooks
from sampo import core as c


class PromptLock(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Fix the login", "--type", "FIX", "--tier", "S", "--ac", "works :: true", "--step", "do it",
                "--focus")
        self.p = c.find_project(self.repo)

    def locked(self):
        """Whether someone holds the project lock now (flock conflicts across descriptors, this process's too)."""
        fd = os.open(os.path.join(self.p.dir, ".lock"), os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return False
        except BlockingIOError:
            return True
        finally:
            os.close(fd)

    def spied(self, fn):
        """Runs fn in the repo; returns (name, lock held) for each brief load and state build, and what fn printed."""
        seen, printed = [], io.StringIO()
        with contextlib.ExitStack() as st:
            for name in ("load_briefs", "state_dict", "worktree_tree"):
                real = getattr(c, name)
                st.enter_context(mock.patch.object(c, name, lambda *a, _r=real, _n=name, **kw: (
                    seen.append((_n, self.locked())), _r(*a, **kw))[1]))
            st.enter_context(contextlib.chdir(self.repo))
            st.enter_context(contextlib.redirect_stdout(printed))
            fn()
        return seen, printed.getvalue()

    def run_hook(self, event, **payload):
        return self.spied(lambda: hooks.run(event, json.dumps(
            dict({"session_id": "s1", "cwd": self.repo, "hook_event_name": event}, **payload))))

    def test_hooks_read_the_state_with_the_lock_free(self):
        for event, payload in (("SessionStart", {"source": "startup"}), ("UserPromptSubmit", {"prompt": "continue"})):
            seen, printed = self.run_hook(event, **payload)
            self.assertIn("state_dict", {n for n, _ in seen}, event)
            self.assertEqual([x for x in seen if x[1]], [], event)
            self.assertIn("T-0001", printed, event)

    def test_the_rewind_check_snapshots_the_files_before_the_lock_and_still_reopens(self):
        with open(os.path.join(self.repo, "a.py"), "w") as f:
            f.write("x = 1\n")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "1")
        seen, _ = self.run_hook("UserPromptSubmit", prompt="continue")
        self.assertIn("worktree_tree", {n for n, _ in seen})
        self.assertEqual([x for x in seen if x[1]], [])
        os.remove(os.path.join(self.repo, "a.py"))  # a /rewind to before the proof
        seen, printed = self.run_hook("UserPromptSubmit", prompt="continue")
        self.assertEqual([x for x in seen if x[1]], [])
        self.assertIn("T-0001 step(s) 1", printed)
        self.assertIn("1. [ ] do it", self.fm("task", "show", "T-0001").stdout)

    def test_an_override_word_still_regenerates_the_views_after_the_lock(self):
        seen, printed = self.run_hook("UserPromptSubmit", prompt="PAUSE")
        self.assertEqual([x for x in seen if x[1]], [])
        self.assertIn("PAUSE", printed)
        with open(os.path.join(self.p.dir, "state.line")) as f:
            self.assertIn("PAUSED", f.read())

    def test_capture_and_task_new_regenerate_after_the_lock(self):
        for argv in (["capture", "Fix the logout"], ["task", "new", "Fix the signup", "--type", "FIX", "--tier", "S"]):
            seen, _ = self.spied(lambda: self.assertEqual(cli.main(argv), 0))
            self.assertIn("state_dict", {n for n, _ in seen}, argv)
            self.assertEqual([x for x in seen if x[1]], [], argv)
        with open(os.path.join(self.p.dir, "STATE.md")) as f:
            text = f.read()
        self.assertIn("T-0002", text)
        self.assertIn("T-0003", text)
