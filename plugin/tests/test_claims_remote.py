"""T-3321 (Fleet part 1): claims are refs refs/sampo/<slug>/claim/<key> taken by atomic compare-and-swap push, so the
remote picks exactly one winner. The remote here is always a file:// bare repo in a temp dir, never origin."""
import json
import os
import subprocess
import tempfile
import threading
import unittest

import helpers  # noqa: F401  (puts plugin/lib on the path)
from sampo import claims

T0 = 1_800_000_000.0


def git(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class ClaimsCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.bare = os.path.join(self.tmp.name, "remote.git")
        git(self.tmp.name, "init", "--bare", self.bare)
        self.url = "file://" + self.bare
        self.src = os.path.join(self.tmp.name, "src")  # the project: every clone shares its root commit
        os.makedirs(self.src)
        git(self.src, "init")
        git(self.src, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "--allow-empty", "-m", "root")
        self.a, self.b = self.clone("a"), self.clone("b")

    def clone(self, name):  # each in its own directory, no explicit slug
        d = os.path.join(self.tmp.name, "deep", name, "work")
        os.makedirs(os.path.dirname(d))
        git(self.tmp.name, "clone", "-q", self.src, d)
        return claims.Claims(d, remote=self.url, session=name)

    def one_winner(self, r):  # the loser saw the holder ("held") or lost the compare-and-swap ("lost")
        res = sorted(x["result"] for x in r.values())
        self.assertEqual(res.count("taken"), 1, r)
        self.assertIn(res[0], ("held", "lost"), r)

    def race(self, fn_a, fn_b):
        out, gate = {}, threading.Barrier(2)

        def run(k, fn):
            gate.wait()
            out[k] = fn()
        ts = [threading.Thread(target=run, args=(k, f)) for k, f in (("a", fn_a), ("b", fn_b))]
        [t.start() for t in ts]
        [t.join() for t in ts]
        return out


class Take(ClaimsCase):
    def test_two_clones_racing_for_one_claim_give_exactly_one_winner(self):
        for n in range(3):
            key = f"T-10{n}"
            r = self.race(lambda: self.a.take(key, now=T0), lambda: self.b.take(key, now=T0))
            self.one_winner(r)
            self.assertEqual(len(self.a.list(now=T0)), n + 1)

    def test_a_live_claim_is_held_against_another_session_and_renewed_by_its_owner(self):
        self.assertEqual(self.a.take("T-1", now=T0)["result"], "taken")
        r = self.b.take("T-1", now=T0 + 60)
        self.assertEqual(r["result"], "held")
        self.assertEqual(r["by"]["session"], "a")
        self.assertEqual(self.a.take("T-1", now=T0 + 60)["result"], "taken")

    def test_an_expired_claim_raced_by_two_clones_is_taken_over_once(self):
        self.a.take("T-2", now=T0)
        late = T0 + 30 * 60 + 5 * 60 + 1
        self.assertEqual(self.b.take("T-2", now=T0 + 30 * 60 + 60)["result"], "held", "5 min slack")
        c = self.clone("c")
        r = self.race(lambda: self.b.take("T-2", now=late), lambda: c.take("T-2", now=late))
        self.one_winner(r)
        self.assertIn(self.a.list(now=late)[0]["session"], ("b", "c"))

    def test_offline_says_so_and_the_caller_decides(self):
        dead = claims.Claims(self.a.root, remote="file://" + self.bare + ".gone", session="a")
        self.assertEqual(dead.take("T-3", now=T0)["result"], "offline")
        self.assertEqual(dead.list(now=T0), None)

    def test_clones_in_different_directories_share_one_slug(self):
        self.assertEqual(self.a.slug, self.b.slug)
        self.assertNotEqual(self.a.root, self.b.root)

    def test_an_unreadable_holder_is_never_taken_over(self):
        self.a.take("T-20", now=T0)
        real = self.b._git
        self.b._git = lambda *args, **kw: real("false") if args[0] == "fetch" else real(*args, **kw)
        self.assertEqual(self.b.take("T-20", now=T0 + 99 * 3600)["result"], "held")
        self.assertEqual(self.b.list(now=T0)[0]["expired"], False)
        self.b._git = real
        self.assertEqual(self.b.take("T-20", now=T0 + 99 * 3600)["result"], "taken", "readable and long expired")

    def test_a_refusing_remote_is_an_error_not_a_lost_race(self):
        hook = os.path.join(self.bare, "hooks", "pre-receive")
        with open(hook, "w") as f:
            f.write("#!/bin/sh\nexit 1\n")
        os.chmod(hook, 0o755)
        self.assertEqual(self.a.take("T-21", now=T0)["result"], "error")

    def test_a_writer_clock_far_ahead_blocks_a_takeover(self):
        body = {"until": claims.iso(T0 - 3600), "at": claims.iso(T0 + 3600)}
        self.assertFalse(claims.expired(body, T0))
        self.assertTrue(claims.expired({"until": claims.iso(T0 - 3600), "at": claims.iso(T0 - 3700)}, T0))
        self.assertFalse(claims.expired({}, T0), "no until: unreadable, not expired")

    def test_the_session_fallback_is_stable_across_calls_and_the_hostname_stays_home(self):
        x = claims.Claims(self.a.root, remote=self.url)
        y = claims.Claims(self.a.root, remote=self.url)
        self.assertEqual(x.session, y.session)
        self.assertEqual(x.take("T-22", now=T0)["result"], "taken")
        self.assertEqual(y.take("T-22", now=T0 + 5)["result"], "taken")
        if not x.me["named"]:
            self.assertIsNone(self.b.list(now=T0)[0]["name"], "the hostname is never written unasked")

    def test_tower_colon_and_dot_are_distinct_claims(self):
        self.assertEqual(self.a.take("tower:x", now=T0)["result"], "taken")
        self.assertEqual(self.b.take("tower.x", now=T0)["result"], "taken")
        self.assertEqual(sorted(r["key"] for r in self.a.list(now=T0)), ["tower.x", "tower:x"])

    def test_keys_are_checked(self):
        for bad in ("", "../x", "a b", "-x"):
            with self.assertRaises(ValueError):
                self.a.take(bad)
        self.assertEqual(self.a.take("tower:core", now=T0)["result"], "taken")
        self.assertEqual(self.a.take("kgen:7", now=T0)["result"], "taken")


class Lifecycle(ClaimsCase):
    def test_list_shows_holder_until_and_fingerprint(self):
        from sampo import eco
        self.a.take("T-4", now=T0)
        (row,) = self.b.list(now=T0)
        self.assertEqual((row["key"], row["machine"], row["fingerprint"]), ("T-4", eco.machine()["id"], ""))
        self.assertEqual(row["until"], claims.iso(T0 + 30 * 60))
        self.assertFalse(row["expired"])
        self.assertTrue(self.b.list(now=T0 + 40 * 60)[0]["expired"])

    def test_release_frees_the_claim_and_only_the_holder_may(self):
        self.a.take("T-5", now=T0)
        self.assertEqual(self.b.release("T-5")["result"], "held")
        self.assertEqual(self.a.release("T-5")["result"], "released")
        self.assertEqual(self.a.list(now=T0), [])
        self.assertEqual(self.b.take("T-5", now=T0)["result"], "taken")

    def test_renew_batches_every_claim_into_one_push_at_most_every_ten_minutes(self):
        for k in ("T-6", "T-7", "tower:x"):
            self.a.take(k, now=T0)
        pushes = []
        real = self.a._git
        self.a._git = lambda *args, **kw: (pushes.append(args) if args[0] == "push" else None) or real(*args, **kw)
        r = self.a.renew(now=T0 + 11 * 60)
        self.assertEqual((r["result"], sorted(r["keys"])), ("renewed", ["T-6", "T-7", "tower:x"]))
        self.assertEqual(len(pushes), 1)
        self.assertEqual(self.a.renew(now=T0 + 15 * 60)["result"], "skipped")
        self.assertEqual(len(pushes), 1)
        self.assertEqual(self.a.renew(now=T0 + 22 * 60)["result"], "renewed")
        self.assertTrue(all(x["until"] == claims.iso(T0 + 22 * 60 + 30 * 60) for x in self.b.list(now=T0)))

    def test_a_claim_lost_to_a_takeover_is_not_renewed_over_it(self):
        self.a.take("T-8", now=T0)
        late = T0 + 36 * 60 + 1
        self.assertEqual(self.b.take("T-8", now=late)["result"], "taken")
        self.assertEqual(self.a.renew(now=late + 11 * 60, force=True)["keys"], [])
        self.assertEqual(self.b.list(now=late)[0]["session"], "b")


if __name__ == "__main__":
    unittest.main()
