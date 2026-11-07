"""T-3558 (T-3556 folded in): focus and every task edit hold the project lock only for the brief's read-modify-write;
git snapshots, recall, predict and the view regeneration run outside it, and no edit made meanwhile is lost."""
import contextlib
import fcntl
import json
import os
import threading
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

    def run_fm(self, *argv, spy=(), code=0):
        """fm in this process; each (module, name) in spy records whether the project lock was held at each call."""
        seen = []
        with contextlib.ExitStack() as st:
            for mod, name in spy:
                real = getattr(mod, name)
                st.enter_context(mock.patch.object(mod, name, lambda *a, _r=real, _n=name, **kw: (
                    seen.append((_n, self.locked())), _r(*a, **kw))[1]))
            st.enter_context(contextlib.chdir(self.repo))
            self.assertEqual(cli.main(list(argv)), code)
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

    def active(self):
        with open(os.path.join(self.p.dir, "status.json")) as f:
            return (json.load(f)["active"] or {}).get("id")

    def test_a_refused_focus_reads_no_git_recall_or_predict(self):
        """T-3583: the refusals are checked on the peek, so a focus refused pays for none of the slow reads."""
        self.fm("task", "new", "Fix the signup", "--type", "FIX", "--tier", "S")  # T-0003: no criteria or steps
        with c.lock(self.p.dir):
            for tid, meta in (("T-0001", {"lane_only": True}), ("T-0002", {"lane": "/srv/devbox/lane"})):
                b = c.find_brief(self.p, tid)
                b.meta.update(meta)
                c.save_brief(self.p, b)
        spy = [(c, "worktree_tree"), (c, "git_head"), (recall, "recall"), (outcomes, "predict")]
        for tid in ("T-0001", "T-0002", "T-0003"):  # lane-only on main, held by a lane, not planned
            with self.subTest(tid):
                self.assertEqual(self.run_fm("focus", tid, spy=spy, code=2), [])

    def test_views_regenerate_when_the_dirty_snapshot_fails(self):
        """T-3583: the brief is saved active before _save_dirty; a failure there still leaves the views current."""
        with mock.patch.object(cli, "_save_dirty", side_effect=OSError("disk full")), contextlib.chdir(self.repo):
            with self.assertRaises(OSError):
                cli.main(["focus", "T-0001"])
        self.assertEqual(c.find_brief(self.p, "T-0001").status, "active")
        self.assertEqual(self.active(), "T-0001")

    def test_an_input_edited_during_the_peek_is_read_again_under_the_lock(self):
        """T-3583: the recall key families: an edit to the request text or the scope made while the peek runs recall
        is a new key, so the locked pass recalls again with it."""
        real = recall.recall
        for tid, edit, word in (("T-0001", ("--section", "Interpretation", "--text", "the cookie expires"), "cookie"),
                                ("T-0002", ("scope=[src/auth.py]",), "src/auth.py")):
            with self.subTest(tid):
                queries = []

                def spy(p, query, *a, **kw):
                    if not queries:
                        self.fm("task", "set", tid, *edit)
                    queries.append(query)
                    return real(p, query, *a, **kw)
                with mock.patch.object(recall, "recall", spy), contextlib.chdir(self.repo):
                    self.assertEqual(cli.main(["focus", tid]), 0)
                self.assertEqual([word in q for q in queries], [False, True])

    def test_a_pause_snapshot_moved_during_the_peek_is_re_based_again(self):
        """T-3583: the rebase key family: a resume whose pause snapshot changed while the peek re-based it re-bases
        again under the lock, from the snapshot the brief holds then."""
        self.fm("focus", "T-0001")
        with open(os.path.join(self.repo, "a.txt"), "w") as f:
            f.write("its own work\n")
        self.fm("focus", "T-0002")  # T-0001 paused with a.txt
        with open(os.path.join(self.repo, "b.txt"), "w") as f:
            f.write("work done meanwhile\n")
        one = c.find_brief(self.p, "T-0001")
        base, paused = one.meta["base_tree"], one.meta["paused_tree"]
        real, calls = c.rebase_snapshot, []

        def spy(root, b, was, now):
            if not calls:  # the pause point moves meanwhile (here: back to its start point)
                with c.lock(self.p.dir):
                    x = c.find_brief(self.p, "T-0001")
                    x.meta["paused_tree"] = base
                    c.save_brief(self.p, x)
            calls.append(was)
            return real(root, b, was, now)
        with mock.patch.object(c, "rebase_snapshot", spy), contextlib.chdir(self.repo):
            self.assertEqual(cli.main(["focus", "T-0001"]), 0)
        self.assertEqual(calls, [paused, base])

    def test_two_focuses_at_once_leave_one_active(self):
        """T-3583: the peeks overlap, the locked passes don't: one ends active, the other paused, and the views show
        the one active (the last regen saw both saves)."""
        gate, codes = threading.Barrier(2), {}

        def go(tid):
            gate.wait()
            codes[tid] = self.fm("focus", tid, check=False).returncode
        ts = [threading.Thread(target=go, args=(t,)) for t in ("T-0001", "T-0002")]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertEqual(codes, {"T-0001": 0, "T-0002": 0})
        status = {t: c.find_brief(self.p, t).status for t in ("T-0001", "T-0002")}
        self.assertEqual(sorted(status.values()), ["active", "planned"], status)
        self.assertEqual(self.active(), next(t for t, s in status.items() if s == "active"))

    def test_a_wedged_views_lock_costs_the_views_not_the_focus(self):
        """T-3583: a views lock held past its timeout: the focus is saved and exits 0, the views wait for the next
        regen, which writes them."""
        real = c.lock
        os.makedirs(os.path.join(self.p.dir, "views"), exist_ok=True)
        fd = os.open(os.path.join(self.p.dir, "views", ".lock"), os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            short = lambda d, timeout=5.0: real(d, 0.2 if d.endswith("views") else timeout)  # noqa: E731  not 30 s
            with mock.patch.object(c, "lock", short), contextlib.chdir(self.repo):
                self.assertEqual(cli.main(["focus", "T-0001"]), 0)
            self.assertEqual(c.find_brief(self.p, "T-0001").status, "active")
            self.assertIsNone(self.active())
        finally:
            os.close(fd)
        c.regen_views(self.p)
        self.assertEqual(self.active(), "T-0001")
