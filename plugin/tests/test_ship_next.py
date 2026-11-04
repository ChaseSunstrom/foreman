"""T-2682: with the queue closed and commits main lacks, fm next names fm ship (under the user's push grant) or the count."""
import os
import subprocess

from helpers import ForemanTestCase


def sh(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


class ShipNext(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", self.origin], check=True)
        sh(self.repo, "remote", "add", "origin", self.origin)
        sh(self.repo, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "fetch", "-q", "origin")

    def commit(self, name):
        with open(os.path.join(self.repo, name), "w") as f:
            f.write(name + "\n")
        sh(self.repo, "add", name)
        sh(self.repo, "commit", "-qm", "add " + name)

    def grant(self):
        self.fm("decide", "push to main whenever work waits", "--cites", "user steer: you may push to main")

    def nxt(self):
        return self.fm("next").stdout

    def test_nothing_waiting_is_silent(self):
        self.assertNotIn("fm ship", self.nxt())

    def test_without_the_grant_one_line_names_the_count_and_the_command(self):
        self.commit("a.txt")
        self.commit("b.txt")
        out = self.nxt()
        self.assertIn("2 commit(s) main lacks", out)
        self.assertIn("sampo ship", out)

    def test_with_the_grant_ship_is_the_action(self):
        self.commit("a.txt")
        self.grant()
        out = self.nxt()
        self.assertIn("ship 1 commit(s) main lacks under the user's standing push grant", out)
        self.assertIn("sampo task set ID --allow publish, sampo ship", out)  # sampo ship needs the active task's grant

    def test_an_open_genesis_tower_does_not_hide_the_ship_step(self):  # T-2722: the tower's stage is never idle
        self.fm("genesis", "init", "--file", "-",
                input="go\n\n## 2. The capability spec\n\n1. **Correctness.** Fixes. Exam: bug.\n\n## 3. The tower\n")
        self.commit("a.txt")
        self.grant()
        out = self.nxt()
        self.assertIn("Genesis", out)  # the tower's step is still named
        self.assertTrue(out.startswith("Next: ship 1 commit(s) main lacks under the user's standing push grant"), out)

    def test_a_steer_that_forbids_pushing_to_main_is_no_grant(self):
        self.commit("a.txt")
        self.grant()
        self.fm("decide", "never push to main again: the user holds pushes", "--cites", "user steer: hold pushes")
        self.assertIn("1 commit(s) main lacks: sampo ship (needs a publish grant)", self.nxt())

    def test_since_the_last_ship_only_new_commits_wait_though_main_took_other_pushes(self):
        self.commit("a.txt")
        sh(self.repo, "update-ref", "refs/foreman/shipped", "HEAD")  # what fm ship records
        other = os.path.join(self.tmp, "other")  # main moves on its own (fm genesis live's site/)
        subprocess.run(["git", "clone", "-q", self.origin, other], check=True)
        with open(os.path.join(other, "site.md"), "w") as f:
            f.write("site\n")
        sh(other, "add", "site.md")
        sh(other, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "site")
        sh(other, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "fetch", "-q", "origin")
        self.assertNotIn("fm ship", self.nxt())
        self.commit("b.txt")
        self.assertIn("1 commit(s) main lacks", self.nxt())

    def test_open_work_is_never_preempted(self):
        self.commit("a.txt")
        self.grant()
        self.fm("task", "new", "real work", "--type", "FIX", "--tier", "S")
        self.assertNotIn("fm ship", self.nxt())

    def test_commits_main_already_holds_are_not_waiting(self):
        self.commit("a.txt")
        sh(self.repo, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "fetch", "-q", "origin")
        self.assertNotIn("fm ship", self.nxt())

    def test_a_commit_main_holds_by_patch_under_another_sha_is_not_waiting(self):
        self.commit("a.txt")
        sha = sh(self.repo, "rev-parse", "HEAD").strip()
        sh(self.repo, "reset", "-q", "--hard", "HEAD~1")
        sh(self.repo, "cherry-pick", sha)  # same patch, another sha: what a ship's re-pick leaves
        sh(self.repo, "commit", "-q", "--amend", "-m", "re-picked")
        sh(self.repo, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "reset", "-q", "--hard", sha)
        sh(self.repo, "fetch", "-q", "origin")
        self.assertNotEqual(sh(self.repo, "rev-parse", "HEAD").strip(), sh(self.repo, "rev-parse", "origin/main").strip())
        self.assertNotIn("fm ship", self.nxt())
