"""T-1183: fm task block/defer --until "installed NAME" | "exists PATH": fm next names the task again once it holds.
Conditions are structured, never shell commands."""
import os
import unittest

from helpers import ForemanTestCase


class UntilConditions(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.bindir = os.path.join(self.tmp, "bin")
        os.makedirs(self.bindir)
        self.tool = os.path.join(self.bindir, "fmfaketool")

    def _task(self):
        self.fm("task", "new", "Waits", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "do it")
        return "T-0001" if "T-0001" in self.fm("task", "list").stdout else self.fm("task", "list").stdout.split()[0]

    def _next(self):
        return self.fm("next", env={"PATH": self.bindir + os.pathsep + os.environ["PATH"]}).stdout

    def _install(self):
        with open(self.tool, "w") as f:
            f.write("#!/bin/sh\n")
        os.chmod(self.tool, 0o755)

    def test_block_installed_is_offered_only_once_on_path(self):
        tid = self._task()
        self.fm("task", "block", tid, "needs the tool", "--until", "installed fmfaketool")
        self.assertNotIn(tid, self._next())
        self._install()
        self.assertIn(tid, self._next())

    def test_defer_exists_is_offered_only_once_the_file_appears(self):
        tid = self._task()
        self.fm("task", "defer", tid, "later", "--until", "exists build/ready.flag")
        self.assertNotIn("due back", self._next())
        os.makedirs(os.path.join(self.repo, "build"))
        open(os.path.join(self.repo, "build", "ready.flag"), "w").close()
        self.assertIn(tid, self._next())

    def test_block_exists_is_offered_once_the_file_appears(self):
        tid = self._task()
        self.fm("task", "block", tid, "needs login", "--until", "exists login.ok")
        self.assertNotIn(tid, self._next())
        open(os.path.join(self.repo, "login.ok"), "w").close()
        self.assertIn(tid, self._next())

    def test_shell_looking_and_outside_conditions_are_refused(self):
        tid = self._task()
        for bad in ("when true", "installed foo; rm -rf /", "installed $(id)", "installed ", "exists /etc/passwd",
                    "exists ../../outside", "command -v codex"):
            r = self.fm("task", "block", tid, "x", "--until", bad, check=False)
            self.assertNotEqual(r.returncode, 0, bad)
        self.assertNotIn("blocked", self.fm("task", "list").stdout)


if __name__ == "__main__":
    unittest.main()
