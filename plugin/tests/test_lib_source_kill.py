"""T-1412: fm lib source update (source_add with replace) killed at any step leaves the previous source listed and
searchable, and no .tmp- or .old- folder behind as a source. A child process runs the update and SIGKILLs itself at
one step; the parent then reads the sources the way the next fm call would."""
import os
import subprocess
import sys
from unittest import mock

from helpers import LIB, ForemanTestCase

import fmcore as c
import fmlib

CHILD = r"""
import os, signal, sys
sys.path.insert(0, sys.argv[1])
import fmlib
point, repo = sys.argv[2], sys.argv[3]
die = lambda: os.kill(os.getpid(), signal.SIGKILL)
git, index, replace, calls = fmlib._git_src, fmlib._index_source, os.replace, []
if point == "clone":
    fmlib._git_src = lambda r, *a, **k: die() if a[0] == "clone" else git(r, *a, **k)
if point == "index":
    fmlib._index_source = lambda *a, **k: die()
def rep(a, b):
    calls.append(a)
    if point == "aside-before":
        die()
    replace(a, b)
    if (point, len(calls)) in (("aside", 1), ("in", 2)):
        die()
os.replace = rep
fmlib.source_add(repo, "kit", replace=True)
"""


class SourceKill(ForemanTestCase):
    def _git(self, *args):
        subprocess.run(["git", "-C", self.kit, "-c", "user.email=t@t", "-c", "user.name=t", *args], check=True,
                       capture_output=True)

    def _skill(self, name, desc):
        os.makedirs(os.path.join(self.kit, "skills", name), exist_ok=True)
        with open(os.path.join(self.kit, "skills", name, "SKILL.md"), "w") as f:
            f.write(f"---\nname: {name}\ndescription: {desc}\n---\nbody\n")
        self._git("add", "-A")
        self._git("commit", "-qm", name)

    def setUp(self):
        super().setUp()
        self.kit = os.path.join(self.tmp, "kit")
        os.makedirs(self.kit)
        self._git("init", "-q")
        self._skill("reverse-engineer", "Reverse engineer a binary with Ghidra")
        fmlib.source_add(self.kit, "kit")
        self._skill("decompile", "Decompile machine code")  # the update would add this
        self.base = os.path.join(c.state_dir(), "lib-sources")

    def _check_previous_kept(self):
        self.assertEqual([m["name"] for m, _ in fmlib.sources()], ["kit"])
        self.assertIn("kit:reverse-engineer", self.fm("lib", "search", "reverse", "engineer", "binary").stdout)
        listed = self.fm("lib", "source", "list").stdout
        self.assertNotIn(".tmp-", listed)
        self.assertNotIn(".old-", listed)
        self.assertEqual(os.listdir(self.base), ["kit"], "stale temp folders of a dead add are swept")

    def test_a_kill_at_each_step_keeps_the_previous_source(self):
        for point in ("clone", "index", "aside-before", "aside", "in"):
            with self.subTest(point):
                p = subprocess.run([sys.executable, "-c", CHILD, LIB, point, self.kit], capture_output=True, text=True,
                                   timeout=60)
                self.assertEqual(p.returncode, -9, p.stderr)  # it really died at that step
                self._check_previous_kept()
                if point != "in":  # the previous index, unchanged
                    self.assertNotIn("kit:decompile", self.fm("lib", "search", "decompile", "machine").stdout)
        # and the next update works (the kill after the move in had already installed the new index)
        self.assertIn("kit @", self.fm("lib", "source", "update", "kit").stdout)
        self.assertIn("kit:decompile", self.fm("lib", "search", "decompile", "machine").stdout)
        self.assertEqual(os.listdir(self.base), ["kit"])

    def test_a_failed_move_in_puts_the_previous_source_back(self):
        replace, calls = os.replace, []

        def rep(a, b):
            calls.append(a)
            if len(calls) == 2:
                raise OSError("disk gone")
            replace(a, b)
        with mock.patch.object(fmlib.os, "replace", rep), self.assertRaises(OSError):
            fmlib.source_add(self.kit, "kit", replace=True)
        self._check_previous_kept()
        self.assertNotIn("kit:decompile", self.fm("lib", "search", "decompile", "machine").stdout)

    def test_a_live_adds_folders_are_left_alone(self):
        os.makedirs(os.path.join(self.base, f".tmp-kit-{os.getpid()}"))
        os.rename(os.path.join(self.base, "kit"), os.path.join(self.base, f"kit.old-{os.getpid()}"))
        self.assertEqual(fmlib.sources(), [])  # mid-swap in a live process: neither folder is a source
        self.assertEqual(sorted(os.listdir(self.base)), [f".tmp-kit-{os.getpid()}", f"kit.old-{os.getpid()}"])
