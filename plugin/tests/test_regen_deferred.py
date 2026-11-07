"""T-3613: c.regen_views called while the project lock is held waits for the lock's release (the mirror export stays under
it); so every caller (intake, autonomy, tidy, grants, incident, ...) holds the lock for its writes only."""
import contextlib
import fcntl
import os
from unittest import mock

from helpers import ForemanTestCase

from sampo import core as c


class RegenDeferred(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def locked(self):
        fd = os.open(os.path.join(self.p.dir, ".lock"), os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return False
        except BlockingIOError:
            return True
        finally:
            os.close(fd)

    def test_views_are_built_after_the_lock_is_released(self):
        seen = []
        real = c.state_dict
        with mock.patch.object(c, "state_dict", lambda *a, **kw: (seen.append(self.locked()), real(*a, **kw))[1]):
            with c.lock(self.p.dir):
                c.regen_views(self.p)
                self.assertEqual(seen, [], "nothing built while held")
            self.assertEqual(seen, [False])

    def test_the_mirror_still_exports_under_the_lock(self):
        held = []
        with mock.patch.object(c, "export_mirror", lambda p: held.append(self.locked())):
            with c.lock(self.p.dir):
                c.regen_views(self.p)
        self.assertEqual(held, [True])

    def test_outside_a_lock_it_is_immediate_and_a_snapshot_is_honoured(self):
        seen = []
        real = c.state_dict
        with mock.patch.object(c, "state_dict", lambda *a, **kw: (seen.append(1), real(*a, **kw))[1]):
            c.regen_views(self.p)
            self.assertEqual(len(seen), 1)
            with c.lock(self.p.dir):
                c.regen_views(self.p, [])
            self.assertEqual(len(seen), 2)

    def test_a_command_under_the_lock_leaves_fresh_views(self):
        self.fm("autonomy", "full")
        with open(os.path.join(self.p.dir, "status.json")) as f:
            self.assertIn('"autonomy": "full"', f.read())

    def boom(self, *a, **kw):
        raise OSError("rebuild failed")

    def test_a_failed_rebuild_is_swallowed_and_logged_when_the_block_failed(self):
        from sampo import hooks
        logged = []
        with mock.patch.object(c, "state_dict", self.boom), \
                mock.patch.object(hooks, "log_error", lambda ev, text: logged.append((ev, text))):
            with self.assertRaises(RuntimeError):
                with c.lock(self.p.dir):
                    c.regen_views(self.p)
                    raise RuntimeError("block")
        self.assertEqual(len(logged), 1)
        self.assertIn("rebuild failed", logged[0][1])

    def test_a_failed_rebuild_raises_on_a_clean_exit_even_inside_an_except(self):
        with mock.patch.object(c, "state_dict", self.boom):
            try:
                raise ValueError("someone else's")
            except ValueError:
                with self.assertRaises(OSError):
                    with c.lock(self.p.dir):
                        c.regen_views(self.p)

    def test_two_projects_each_get_their_own_rebuild(self):
        other = os.path.join(self.p.dir, "..", "other-proj")
        seen = []
        q = c.Project("other", self.repo, os.path.abspath(other))
        real = c.state_dict
        with mock.patch.object(c, "state_dict", lambda pr, *a, **kw: (seen.append(pr.dir), real(self.p, *a, **kw))[1]):
            with c.lock(self.p.dir), c.lock(q.dir):
                c.regen_views(self.p)
                c.regen_views(q, mirror=False)
                self.assertEqual(seen, [])
        self.assertEqual(sorted(seen), sorted([self.p.dir, q.dir]))

    def test_a_nested_lock_on_another_dir_neither_triggers_nor_misplaces_the_rebuild(self):
        seen = []
        real = c.state_dict
        sub = os.path.join(self.p.dir, "postmerge")
        with mock.patch.object(c, "state_dict", lambda *a, **kw: (seen.append(self.locked()), real(*a, **kw))[1]):
            with c.lock(self.p.dir):
                with c.lock(sub):
                    pass
                self.assertEqual(seen, [])
                c.regen_views(self.p)
                with c.lock(sub):
                    pass
                self.assertEqual(seen, [])
            self.assertEqual(seen, [False])

    def test_an_error_in_the_block_still_leaves_fresh_views(self):
        c.update_meta(self.p, autonomy="full")
        with contextlib.suppress(RuntimeError), c.lock(self.p.dir):
            c.regen_views(self.p)
            raise RuntimeError("x")
        with open(os.path.join(self.p.dir, "status.json")) as f:
            self.assertIn('"autonomy": "full"', f.read())
