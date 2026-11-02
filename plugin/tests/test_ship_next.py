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
        self.assertIn("fm ship", out)

    def test_with_the_grant_ship_is_the_action(self):
        self.commit("a.txt")
        self.grant()
        out = self.nxt()
        self.assertIn("fm ship", out)
        self.assertNotIn("commit(s) main lacks", out)

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

    def test_a_commit_main_holds_by_content_under_another_sha_is_not_waiting(self):
        self.commit("a.txt")
        sh(self.repo, "commit", "-q", "--amend", "-m", "reworded")
        sh(self.repo, "push", "-q", "origin", "HEAD:main")
        sh(self.repo, "fetch", "-q", "origin")
        self.commit("b.txt")
        sh(self.repo, "reset", "-q", "--hard", "HEAD~1")
        sh(self.repo, "commit", "-q", "--allow-empty", "-m", "empty")  # '+' by cherry, tree equal to main's
        self.assertNotIn("fm ship", self.nxt())
