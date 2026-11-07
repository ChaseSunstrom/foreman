"""T-3329 (Fleet): next_id reserves blocks of 32 T-numbers on refs/sampo/<slug>/ids by compare-and-swap push, so two
machines never mint the same id. Needs FOREMAN_CLAIMS_REMOTE; the remote here is a file:// bare repo in a temp dir
and the two machines are two `git clone`s of one repo (the real, repo-shared slug)."""
import os
import subprocess
import threading
import unittest
from unittest import mock

import helpers
from sampo import claims, core


def git(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class IdBlocks(helpers.SampoTestCase):
    def setUp(self):
        super().setUp()
        self.bare = os.path.join(self.tmp, "remote.git")
        subprocess.run(["git", "init", "-q", "--bare", self.bare], check=True)
        self._remote = os.environ.get("FOREMAN_CLAIMS_REMOTE")
        self.url = "file://" + self.bare
        os.environ["FOREMAN_CLAIMS_REMOTE"] = self.url
        self.addCleanup(self.restore)
        clone = os.path.join(self.tmp, "app2")
        git(self.tmp, "clone", "-q", self.repo, clone)
        self.a, self.b = core.init_project(self.repo), core.init_project(clone)
        self.ca, self.cb = claims.Claims(self.repo), claims.Claims(clone)
        self.assertEqual(self.ca.slug, self.cb.slug)

    def restore(self):
        if self._remote is None:
            os.environ.pop("FOREMAN_CLAIMS_REMOTE", None)
        else:
            os.environ["FOREMAN_CLAIMS_REMOTE"] = self._remote

    def offline(self):
        os.environ["FOREMAN_CLAIMS_REMOTE"] = self.url + ".gone"

    def mint(self, p, n, **kw):
        return [core.next_id(p, **kw) for _ in range(n)]

    def test_two_clones_mint_40_each_with_no_overlap(self):
        got = []
        for _ in range(2):  # interleaved, so blocks alternate
            got += self.mint(self.a, 20) + self.mint(self.b, 20)
        a_ids = set(got[:20] + got[40:60])
        b_ids = set(got[20:40] + got[60:])
        self.assertEqual(len(a_ids | b_ids), 80)
        self.assertFalse(a_ids & b_ids)
        for i in got:
            self.assertRegex(i, r"T-\d{4,}")

    def test_offline_mints_inside_the_block_then_refuses_and_says_why(self):
        first = self.mint(self.a, 1)[0]
        self.offline()
        rest = self.mint(self.a, 31)
        n = core.id_num(first)
        self.assertEqual([core.id_num(i) for i in rest], list(range(n + 1, n + 32)))
        with self.assertRaises(core.PolicyError) as e:
            core.next_id(self.a)
        self.assertIn("id block", str(e.exception))
        self.assertIn("sampo sync", str(e.exception))

    def test_hook_paths_never_reserve_and_refuse_when_the_block_is_spent(self):
        with self.assertRaises(core.PolicyError):  # no block yet: a hook does not reach the network for one
            core.next_id(self.a, net=False)
        self.mint(self.a, 1)
        self.assertEqual(len(self.mint(self.a, 5, net=False)), 5)

    def test_the_next_block_is_prefetched_when_8_remain_so_going_offline_later_is_fine(self):
        self.mint(self.a, 25)  # 7 left in the first block: the second is already held
        self.offline()
        got = self.mint(self.a, 20)
        self.assertEqual(len(set(got)), 20)

    def test_an_unreadable_counter_is_never_reset(self):
        self.mint(self.a, 1)
        ref = f"refs/sampo/{self.ca.slug}/ids"
        bad = git(self.bare, "commit-tree", claims.EMPTY_TREE, "-m", "not json")
        git(self.bare, "update-ref", ref, bad)
        self.assertIsNone(self.cb.reserve_ids(floor=1))
        self.assertEqual(git(self.bare, "rev-parse", ref), bad)

    def test_a_lost_compare_and_swap_retries_on_the_new_counter(self):
        real, fired = self.cb._push, []

        def push(updates):
            if not fired:  # the other machine reserves between this one's read and its push
                fired.append(self.ca.reserve_ids(floor=1))
            return real(updates)
        with mock.patch.object(self.cb, "_push", push):
            start = self.cb.reserve_ids(floor=1)
        self.assertEqual(fired, [1])
        self.assertEqual(start, 33)

    def test_the_creation_race_gives_each_machine_its_own_block(self):
        out, gate = {}, threading.Barrier(2)

        def run(k, c):
            gate.wait()
            out[k] = c.reserve_ids(floor=1)
        ts = [threading.Thread(target=run, args=(k, c)) for k, c in (("a", self.ca), ("b", self.cb))]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertEqual(sorted(out.values()), [1, 33])

    def test_no_remote_configured_is_unchanged(self):
        os.environ.pop("FOREMAN_CLAIMS_REMOTE")
        self.assertEqual(self.mint(self.a, 3), ["T-0001", "T-0002", "T-0003"])
        self.assertEqual(core.next_id(self.a, net=False), "T-0004")


if __name__ == "__main__":
    unittest.main()
