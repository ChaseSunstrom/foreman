"""T-0751 (runtime): revert with its dependents listed first, a queue that fits what's left, and spike lanes that
are never merged."""
import json
import os
import subprocess
import sys

from helpers import FM, ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo, *args], check=True, capture_output=True, text=True).stdout


class Revert(Base):
    def test_revert_lists_commits_and_dependents_and_never_reverts_itself(self):
        self.fm("task", "new", "Add x", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "new", "Build on x", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "set", "T-0002", "depends_on=T-0001")
        with open(os.path.join(self.repo, "x.py"), "w") as f:
            f.write("X = 1\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "Add x (T-0001)")
        sha = self.git("rev-parse", "--short", "HEAD").strip()
        out = self.fm("task", "revert", "T-0001").stdout
        self.assertIn(sha, out)
        self.assertRegex(out, r"T-0002 .*depends on it")
        self.assertIn(f"git revert --no-edit {sha}", out)
        self.assertIn("Add x (T-0001)", self.git("log", "-1", "--format=%s"))  # nothing undone by itself


class Fit(Base):
    def test_fit_runs_small_tasks_before_big_ones(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        calls = os.path.join(self.tmp, "calls")
        fm = f"{sys.executable} {FM}"
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(f'#!/usr/bin/env bash\necho "$FOREMAN_DRIVE_TASK" >> {calls}\nt=$FOREMAN_DRIVE_TASK\n'
                    f'{fm} focus $t >/dev/null\n{fm} task step $t done 1 --evidence x ok >/dev/null\n'
                    f'{fm} task ac $t check 1 --evidence x ok >/dev/null\n{fm} task audit $t self x ok >/dev/null\n'
                    f'{fm} task done $t >/dev/null\n')
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        big = json.loads(self.fm("task", "new", "Big", "--type", "FEATURE", "--tier", "M", "--interpretation", "x",
                                 "--approach", "a vs b: a", "--ac", "works", "--step", "s", "--json").stdout)["id"]
        small = json.loads(self.fm("task", "new", "Small", "--type", "FEATURE", "--tier", "S", "--ac", "works",
                                   "--step", "s", "--json").stdout)["id"]
        self.fm("run", "--fit", "--max", "1", env={"PATH": bindir + os.pathsep + os.environ["PATH"]}, check=False)
        with open(calls) as f:
            self.assertEqual(f.read().split()[0], small, big)


class Spike(Base):
    def test_a_spike_lane_is_never_merged(self):
        self.git("commit", "-q", "--allow-empty", "-m", "base")
        self.fm("task", "new", "Try the new parser", "--type", "RESEARCH", "--tier", "S", "--ac", "ok :: true",
                "--step", "s")
        self.fm("lane", "new", "T-0001", "--spike")
        r = self.fm("lane", "merge", "T-0001", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("spike", r.stderr)
