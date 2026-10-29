"""T-1943: fm ship lands the unpushed commits on the remote's main from a scratch worktree, behind the publish grant."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


def sh(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


class Ship(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", self.origin], check=True)
        sh(self.repo, "remote", "add", "origin", self.origin)
        sh(self.repo, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "checkout", "-q", "-b", "work")
        for name in ("a", "b"):
            with open(os.path.join(self.repo, f"{name}.txt"), "w") as f:
                f.write(name + "\n")
            sh(self.repo, "add", f"{name}.txt")
            sh(self.repo, "commit", "-qm", f"add {name}")
        self.tid = json.loads(self.fm("task", "new", "land", "--type", "FEATURE", "--tier", "S", "--json").stdout)["id"]
        self.fm("task", "step", self.tid, "add", "land it")
        self.fm("task", "ac", self.tid, "add", "landed", "--verify", "true")
        self.fm("focus", self.tid)

    def grant(self):
        p = c.find_project(self.repo)
        b = c.find_brief(p, self.tid)
        b.meta["allow"] = ["publish"]
        c.save_brief(p, b)

    def granted(self):
        return "publish" in (c.find_brief(c.find_project(self.repo), self.tid).meta.get("allow") or [])

    def main_log(self):
        return sh(self.origin, "log", "--format=%s", "main").split("\n")

    def ship(self, *a):
        return self.fm("ship", "--remote", "origin", *a, check=False)

    def test_without_the_grant_nothing_is_pushed(self):
        r = self.ship("--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("publish", r.stdout + r.stderr)
        self.assertNotIn("add a", self.main_log())

    def test_ships_the_unpushed_commits_after_the_test_and_spends_the_grant(self):
        self.grant()
        status = sh(self.repo, "status", "--porcelain")
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add b", "add a"])
        tip = sh(self.origin, "rev-parse", "main").strip()
        self.assertIn(tip, r.stdout, "the pushed sha, for fm ci-watch --commit")
        self.assertIn("ci-watch", r.stdout)
        self.assertFalse(self.granted(), "the yes covers one push")
        self.assertEqual(sh(self.repo, "worktree", "list").count("\n"), 1, "the scratch worktree is gone")
        self.assertEqual(sh(self.repo, "status", "--porcelain"), status, "the working tree is untouched")
        r = self.ship("--test", "true")  # main has these changes now (by patch, not sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("nothing to ship", r.stdout)

    def test_a_named_commit_ships_alone(self):
        self.grant()
        first = sh(self.repo, "rev-parse", "HEAD~1").strip()
        r = self.ship(first, "--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[0], "add a")
        self.assertNotIn("add b", self.main_log())

    def test_a_failed_test_pushes_nothing_and_keeps_the_grant(self):
        self.grant()
        r = self.ship("--test", "false")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())
        self.assertEqual(sh(self.repo, "worktree", "list").count("\n"), 1)

    def test_main_moving_during_the_test_pushes_nothing(self):
        self.grant()
        other = os.path.join(self.tmp, "other")
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        sh(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "someone else")
        r = self.ship("--test", f"git -C {other} push -q origin HEAD:main")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("main moved", r.stdout + r.stderr)
        self.assertEqual(self.main_log()[0], "someone else")
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())

    def test_a_rejected_push_keeps_the_grant(self):
        # review: the grant was spent before git push, so a rejected push cost the yes
        hook = os.path.join(self.origin, "hooks", "pre-receive")
        with open(hook, "w") as f:
            f.write("#!/bin/sh\necho no >&2\nexit 1\n")
        os.chmod(hook, 0o755)
        self.grant()
        r = self.ship("--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted(), "a push that failed gives the grant back")
        self.assertEqual(sh(self.repo, "worktree", "list").count("\n"), 1)

    def test_a_relative_remote_path_and_a_missing_test_program(self):
        self.grant()
        r = self.ship("--test", "no-such-program-1943")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertTrue(self.granted())
        sh(self.repo, "remote", "set-url", "origin", os.path.relpath(self.origin, self.repo))
        r = self.ship("--test", "true")  # fetched and pushed from the repo, not the scratch tree
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[0], "add b")

    def test_a_remote_or_commit_that_reads_as_an_option_is_refused(self):
        self.grant()
        for argv in (["--remote=--upload-pack=touch x"], ["--remote", "origin", "--", "--output=x"]):
            r = self.fm("ship", *argv, "--test", "true", check=False)
            self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())
