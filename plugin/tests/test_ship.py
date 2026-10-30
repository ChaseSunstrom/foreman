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

    def test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check(self):
        # T-1978: the ship's suite had no marker (a full fm check ran beside it) and ran beside a live check here
        import threading
        self.grant()
        p = c.find_project(self.repo)
        seen = os.path.join(self.tmp, "seen.json")
        busy = subprocess.Popen(["sleep", "2"])
        threading.Thread(target=busy.wait, daemon=True).start()
        c.update_meta(p, gates_running={"task": None, "pid": busy.pid, "at": c.now(), "root": p.root})
        r = self.ship("--test", f"cp {os.path.join(p.dir, 'meta.json')} {seen}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("waiting for a running fm check", r.stdout + r.stderr)
        with open(seen) as f:
            self.assertEqual(json.load(f)["ship_testing"]["pid"] > 0, True)
        self.assertFalse(c.read_meta(p).get("ship_testing"), "cleared after the run")

    def test_the_default_fm_check_in_the_scratch_tree_never_waits_for_its_own_ship(self):
        # T-1978: the ship's marker names its scratch tree; the fm check it runs there must not wait 10 minutes on it
        self.grant()
        self.fm("check", "add", "true")
        r = self.ship()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("waiting for fm ship", r.stdout + r.stderr)
        self.assertIn("add b", self.main_log())

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

    def test_ship_on_a_named_tasks_grant(self):
        # T-2007: a finished task ships on its own grant: no separate ship task focused to hold one
        r = self.ship("--task", self.tid.lower(), "--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(f"{self.tid} has no publish grant", r.stdout + r.stderr)
        self.assertNotIn("add a", self.main_log())
        r = self.ship("--task", "T-9999", "--test", "true")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no task T-9999", r.stdout + r.stderr)
        self.grant()
        other = json.loads(self.fm("task", "new", "other", "--type", "CLEAN", "--tier", "S", "--ac", "x :: true",
                                    "--step", "x", "--json").stdout)["id"]
        self.fm("checkpoint")
        self.fm("focus", other)  # the active task has no grant; the named one does
        r = self.ship("--task", self.tid, "--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add b", "add a"])
        self.assertFalse(self.granted(), "the named task's yes is spent")

    def test_check_says_whether_main_has_the_commits_without_the_grant(self):
        # T-1960: a ship task's verify was git log -n3 | grep, which a later ship pushes out of view
        first = sh(self.repo, "rev-parse", "HEAD~1").strip()
        r = self.ship("--check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("add a", r.stdout)
        self.grant()
        self.assertEqual(self.ship(first, "--test", "true").returncode, 0)
        self.assertTrue(self.granted() is False)
        self.assertEqual(self.ship("--check", first).returncode, 0)
        r = self.ship("--check")
        self.assertEqual(r.returncode, 1, "add b is still missing")
        self.assertIn("add b", r.stdout)
        self.assertNotRegex(r.stdout, r"\badd a\b", "a word: a hash ending in 'add' before 'add b' reads as 'add a'")

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

    def test_a_plain_ship_starts_after_the_shipped_ref(self):
        # T-1945: main held shipped commits under another patch (a merge), so git cherry listed them every time
        self.grant()
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        other = os.path.join(self.tmp, "other")
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        sh(other, "reset", "-q", "--hard", "HEAD~2")
        for name in ("a", "b"):
            with open(os.path.join(other, f"{name}.txt"), "w") as f:
                f.write(name + "\n")
        sh(other, "add", ".")
        sh(other, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "a and b squashed")
        sh(other, "push", "-qf", "origin", "HEAD:main")
        with open(os.path.join(self.repo, "c.txt"), "w") as f:
            f.write("c\n")
        sh(self.repo, "add", "c.txt")
        sh(self.repo, "commit", "-qm", "add c")
        self.grant()
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add c", "a and b squashed"])
        self.assertEqual(sh(self.repo, "rev-parse", "refs/foreman/shipped"), sh(self.repo, "rev-parse", "HEAD"))

    def test_a_merged_lane_whose_merge_settled_a_conflict_ships_through_the_merge(self):
        # T-2054: a builder lane's own commit didn't cherry-pick onto main alone; its merge on the branch had settled it
        self.grant()
        self.assertEqual(self.ship("--test", "true").returncode, 0)
        shipped = sh(self.repo, "rev-parse", "HEAD").strip()
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("one\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "branch writes shared")
        sh(self.repo, "checkout", "-q", "-b", "lane", shipped)
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("two\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "lane writes shared")
        sh(self.repo, "checkout", "-q", "work")
        subprocess.run(["git", "-C", self.repo, "merge", "-q", "lane"], capture_output=True)
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("one\ntwo\n")
        sh(self.repo, "add", "shared.txt")
        sh(self.repo, "commit", "-qm", "Merge lane")
        self.grant()
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sh(self.origin, "show", "main:shared.txt"), "one\ntwo\n")
        self.assertEqual(self.main_log()[:2], ["Merge lane", "branch writes shared"])
        self.assertEqual(sh(self.repo, "rev-parse", "refs/foreman/shipped"), sh(self.repo, "rev-parse", "HEAD"))

    def test_a_remembered_test_runs_when_test_is_left_out(self):
        # T-1950: the oldest runtime's suite was retyped on every ship
        mark = os.path.join(self.tmp, "ran")
        self.grant()
        self.assertEqual(self.ship("--test", f"touch {mark}").returncode, 0)
        os.remove(mark)
        with open(os.path.join(self.repo, "c.txt"), "w") as f:
            f.write("c\n")
        sh(self.repo, "add", "c.txt")
        sh(self.repo, "commit", "-qm", "add c")
        self.grant()
        r = self.ship()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(mark), "the remembered --test ran")
        self.assertIn(f"touch {mark}", r.stdout)

    def test_a_failed_ref_write_after_the_push_still_reports_the_ship(self):
        # T-1951: main got the commits, so a refs/foreman/shipped lock must not read as a failed ship
        lock = os.path.join(self.repo, ".git", "refs", "foreman", "shipped.lock")
        os.makedirs(os.path.dirname(lock))
        open(lock, "w").close()
        self.grant()
        r = self.ship("--test", "true")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.main_log()[:2], ["add b", "add a"])
        self.assertIn("shipped 2 commits", r.stdout)
        self.assertIn("refs/foreman/shipped", r.stdout + r.stderr)

    def test_watch_watches_the_pushed_commit(self):
        # T-1946: ship, then CI on the pushed sha, in one background job
        import sys
        bin_dir = os.path.join(self.tmp, "bin")
        os.makedirs(bin_dir)
        with open(os.path.join(bin_dir, "gh"), "w") as f:
            f.write(f"#!{sys.executable}\nimport json, subprocess, sys\n"
                    "if sys.argv[1:3] != ['run', 'list']: sys.exit(3)\n"
                    f"sha = subprocess.run(['git', '-C', {self.origin!r}, 'rev-parse', 'main'], capture_output=True, text=True).stdout.strip()\n"
                    "print(json.dumps([{'databaseId': 1, 'status': 'completed', 'conclusion': 'success', 'headSha': sha, "
                    "'url': 'https://github.com/o/r/actions/runs/1'}]))\n")
        os.chmod(os.path.join(bin_dir, "gh"), 0o755)
        self.grant()
        r = self.fm("ship", "--remote", "origin", "--test", "true", "--watch",
                    env={"PATH": bin_dir + os.pathsep + os.environ["PATH"]}, check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        tip = sh(self.origin, "rev-parse", "main").strip()
        self.assertIn(f"watching {tip[:7]} on main", r.stdout)
        self.assertIn("CI green", r.stdout)

    def test_a_remote_or_commit_that_reads_as_an_option_is_refused(self):
        self.grant()
        for argv in (["--remote=--upload-pack=touch x"], ["--remote", "origin", "--", "--output=x"]):
            r = self.fm("ship", *argv, "--test", "true", check=False)
            self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("add a", self.main_log())
        self.assertTrue(self.granted())
