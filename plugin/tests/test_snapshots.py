"""T-0884: before a Bash command throws away uncommitted work, Foreman saves the working files as a commit under
refs/foreman/snapshots; fm snapshots lists them with the command that brings one back."""
import json
import os
import subprocess
import sys
import unittest

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))


class Snapshots(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Tidy", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus")

    def refs(self):
        return subprocess.run(["git", "-C", self.repo, "for-each-ref", "--format=%(refname)", "refs/foreman/snapshots"],
                              capture_output=True, text=True).stdout.split()

    def bash(self, cmd):
        return self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}})

    def test_a_discarding_command_saves_the_work_first_and_it_comes_back(self):
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("my unsaved paragraph\n")
        with open(os.path.join(self.repo, "notes.txt"), "w") as f:
            f.write("an untracked draft\n")
        r = self.bash("git checkout -- . && git clean -fd")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(self.refs()), 1, "one snapshot for one command")
        note = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("fm snapshots", note)
        listed = self.fm("snapshots").stdout
        self.assertIn("git checkout -- .", listed)
        restore = next(ln.split("restore: ", 1)[1] for ln in listed.splitlines() if "restore: " in ln)
        subprocess.run(["git", "-C", self.repo, "checkout", "-q", "--", "."], check=True)
        subprocess.run(["git", "-C", self.repo, "clean", "-qfd"], check=True)
        subprocess.run(restore, shell=True, cwd=self.repo, check=True)
        with open(os.path.join(self.repo, "README.md")) as f:
            self.assertIn("my unsaved paragraph", f.read())
        self.assertTrue(os.path.exists(os.path.join(self.repo, "notes.txt")))

    def test_nothing_to_lose_or_a_harmless_command_saves_nothing(self):
        self.bash("git checkout -- .")  # clean tree: nothing differs from HEAD
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("x\n")
        for cmd in ("git status", "git checkout -b feature", "git restore --staged README.md", "git clean -n",
                    "echo git reset --hard"):
            self.bash(cmd)
        self.assertEqual(self.refs(), [])

    def test_which_commands_discard_work(self):
        import fmguard as g
        yes = ["git reset --hard HEAD~1", "git reset --merge", "git checkout -f main", "git checkout -- src",
               "git checkout .", "git checkout README.md", "git restore README.md", "git restore -SW .",
               "git clean -xdf", "git clean --force", "git switch --discard-changes main", "git rm -f a.py",
               "git merge --abort", "git rebase --abort", "sudo git -C sub reset --hard", "FOO=1 git stash; git reset --hard"]
        no = ["git checkout -b x", "git checkout main", "git restore --staged a.py", "git clean -n -f", "git reset HEAD~1",
              "git status", "echo git reset --hard", "git stash", "git log --hard"]
        os.makedirs(os.path.join(self.repo, "src"))
        for cmd in yes:
            self.assertTrue(g.discards_work(cmd, self.repo), cmd)
        for cmd in no:
            self.assertFalse(g.discards_work(cmd, self.repo), cmd)
        sub = os.path.join(self.repo, "sub")
        home = os.path.expanduser("~")
        where = lambda cmd: [w for w, _ in g.discards_work(cmd, self.repo)]  # noqa: E731
        self.assertEqual(where("git -C sub reset --hard"), [sub])
        # review: a cd before it, a shell -c, a ~ in -C, another worktree removed by force
        self.assertEqual(where("cd sub && git checkout -- ."), [sub])
        self.assertEqual(where("bash -c 'git reset --hard'"), [self.repo])
        self.assertEqual(where("git -C ~/proj reset --hard"), [os.path.join(home, "proj")])
        self.assertEqual(where("git worktree remove --force ../lane"), [os.path.join(self.tmp, "lane")])
        self.assertEqual([k for _, k in g.discards_work("git stash drop stash@{1}; git stash clear", self.repo)],
                         ["stash drop stash@{1}", "stash clear"])
        os.makedirs(os.path.join(self.repo, "main"))  # a folder named like the branch isn't a path checkout
        self.assertFalse(g.discards_work("git checkout main", self.repo))

    def test_a_dropped_stash_is_kept(self):
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("stashed words\n")
        subprocess.run(["git", "-C", self.repo, "stash", "-q"], check=True)
        sha = subprocess.run(["git", "-C", self.repo, "rev-parse", "stash@{0}"], capture_output=True, text=True).stdout.strip()
        self.bash("git stash drop")
        listed = self.fm("snapshots").stdout
        self.assertIn(f"stash apply {sha[:12]}", listed)

    def test_the_restore_line_works_from_a_subdirectory_and_a_failure_is_said(self):
        import fmcore as c
        os.makedirs(os.path.join(self.repo, "docs"))
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("top-level words\n")
        sha = c.snapshot(self.repo, "test")[0]
        rows = json.loads(self.fm("snapshots", "--json", cwd=os.path.join(self.repo, "docs")).stdout)["snapshots"]
        subprocess.run(["git", "-C", self.repo, "checkout", "-q", "--", "."], check=True)
        subprocess.run(rows[0]["restore"], shell=True, cwd=os.path.join(self.repo, "docs"), check=True)
        with open(os.path.join(self.repo, "README.md")) as f:
            self.assertIn("top-level words", f.read())
        self.assertTrue(rows[0]["sha"].startswith(sha[:7]))
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("more\n")
        from unittest import mock
        with mock.patch.object(c, "worktree_tree", return_value=None), self.assertRaises(RuntimeError):
            c.snapshot(self.repo, "test", timeout=3)  # review: a snapshot that can't finish in its time says so

    def test_tidy_prunes_old_snapshots(self):
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("x\n")
        self.bash("git checkout -- .")  # (reset --hard on main is the guard's to refuse: nothing runs, nothing saved)
        old = self.refs()[0]
        sha = subprocess.run(["git", "-C", self.repo, "rev-parse", old], capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "-C", self.repo, "update-ref", "refs/foreman/snapshots/20200101T000000Z-aaaaaaa", sha],
                       check=True)
        self.fm("tidy", "--apply")
        self.assertEqual(self.refs(), [old], "the 2020 one goes, today's stays")


if __name__ == "__main__":
    unittest.main()
