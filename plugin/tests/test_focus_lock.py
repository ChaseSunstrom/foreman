"""T-3558 (T-3556 folded in): focus and every task edit hold the project lock only for the brief's read-modify-write;
git snapshots, recall, predict and the view regeneration run outside it, and no edit made meanwhile is lost."""
import contextlib
import fcntl
import json
import os
from unittest import mock

from helpers import ForemanTestCase

from sampo import cli
from sampo import core as c
from sampo import outcomes, recall


class FocusLock(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        for t in ("Fix the login", "Fix the logout"):
            self.fm("task", "new", t, "--type", "FIX", "--tier", "S", "--ac", "works :: true", "--step", "do it")
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

    def run_fm(self, *argv, spy=()):
        """fm in this process; each (module, name) in spy records whether the project lock was held at each call."""
        seen = []
        with contextlib.ExitStack() as st:
            for mod, name in spy:
                real = getattr(mod, name)
                st.enter_context(mock.patch.object(mod, name, lambda *a, _r=real, _n=name, **kw: (
                    seen.append((_n, self.locked())), _r(*a, **kw))[1]))
            st.enter_context(contextlib.chdir(self.repo))
            self.assertEqual(cli.main(list(argv)), 0)
        return seen

    def test_an_edit_made_while_focus_reads_git_survives(self):
        real, calls = c.worktree_tree, []

        def snapshot(root, *a, **kw):  # another fm call edits the brief while focus snapshots the files
            if not calls:
                calls.append(self.fm("task", "set", "T-0001", "--section", "Notes", "--text", "written meanwhile"))
            return real(root, *a, **kw)
        with mock.patch.object(c, "worktree_tree", snapshot), contextlib.chdir(self.repo):
            self.assertEqual(cli.main(["focus", "T-0001"]), 0)
        b = c.find_brief(self.p, "T-0001")
        self.assertIn("written meanwhile", b.section("Notes"))
        self.assertEqual((b.status, bool(b.meta.get("base_tree")), bool(b.meta.get("base"))), ("active", True, True))

    def test_git_recall_predict_and_views_run_outside_the_lock(self):
        spy = [(c, "worktree_tree"), (c, "git_head"), (recall, "recall"), (outcomes, "predict"), (c, "state_dict")]
        seen = self.run_fm("focus", "T-0001", spy=spy)
        self.assertEqual({n for n, _ in seen}, {n for _, n in spy})
        self.assertEqual([x for x in seen if x[1]], [])
        with open(os.path.join(self.p.dir, "STATE.md")) as f:
            self.assertIn("T-0001", f.read())
        seen = self.run_fm("focus", "T-0002", spy=spy)  # a switch: the paused task's snapshot is the one just taken
        self.assertEqual([x for x in seen if x[1]], [])
        one, two = c.find_brief(self.p, "T-0001"), c.find_brief(self.p, "T-0002")
        self.assertEqual((one.status, two.status), ("planned", "active"))
        self.assertTrue(one.meta.get("paused_tree"))
        self.assertEqual(one.meta.get("paused_tree"), two.meta.get("base_tree"))
        seen = self.run_fm("task", "step", "T-0002", "add", "and test it", spy=[(c, "state_dict")])
        self.assertEqual(seen, [("state_dict", False)])  # T-3556: a plain task edit regenerates after the lock
        with open(os.path.join(self.p.dir, "status.json")) as f:
            self.assertEqual(json.load(f)["active"]["total"], 2)

    def test_the_sync_mirror_still_exports_under_the_lock(self):
        from sampo import sync
        self.fm("sync", "on")
        seen = self.run_fm("task", "set", "T-0001", "--section", "Notes", "--text", "x",
                           spy=[(sync, "export"), (c, "state_dict")])
        self.assertEqual(sorted(seen), [("export", True), ("state_dict", False)])
