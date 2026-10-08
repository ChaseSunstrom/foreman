"""fmpy (T-0368): fm and the hooks re-run under a supported Python when python3 on PATH is below Foreman's floor."""
import os
import stat
import sys

from helpers import ForemanTestCase

import fmpy


class Fmpy(ForemanTestCase):
    def fake(self, name, version):
        """A stand-in interpreter that answers fmpy's version probe, counting its runs."""
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir, exist_ok=True)
        path = os.path.join(bindir, name)
        with open(path, "w") as f:
            f.write(f"#!/bin/sh\necho x >> {bindir}/{name}.runs\necho {version}\n")
        os.chmod(path, 0o755)
        return path

    def runs(self, name):
        try:
            with open(os.path.join(self.tmp, "bin", f"{name}.runs")) as f:
                return len(f.read().split())
        except OSError:
            return 0

    def target(self, v, path=None):
        old = os.environ["PATH"], os.environ.get("HOME")
        os.environ["PATH"], os.environ["HOME"] = path or os.path.join(self.tmp, "bin"), self.tmp
        try:
            return fmpy.target(v)
        finally:
            os.environ["PATH"] = old[0]
            if old[1] is None:
                os.environ.pop("HOME")
            else:
                os.environ["HOME"] = old[1]

    def test_old_python_reruns_under_a_saved_supported_one(self):
        # JARVIS: python3 is 3.11.2 and argparse there dropped `fm task evidence ID --step N CMD RESULT`
        self.assertTrue(fmpy.ok((3, 12, 7)) and fmpy.ok((3, 14, 0)))
        self.assertFalse(fmpy.ok((3, 11, 2)) or fmpy.ok((3, 13, 0)) or fmpy.ok((3, 12, 6)))
        good = self.fake("python3.12", "3 12 14")
        self.fake("python3.13", "3 13 0")  # 3.13.0 is below the floor too: skipped
        self.assertIsNone(self.target((3, 13, 1)), "a supported python3 never re-execs")
        self.assertFalse(os.path.exists(fmpy.saved_path()))
        self.assertEqual(self.target((3, 11, 2)), good)
        with open(fmpy.saved_path()) as f:
            self.assertEqual(f.read().strip(), good)
        self.assertEqual(self.target((3, 11, 2), path="/nonexistent"), good, "found once, then read back")
        self.assertEqual(self.runs("python3.12"), 1)
        os.chmod(fmpy.saved_path(), 0o666)
        self.assertIsNone(self.target((3, 11, 2)), "a file others can write would choose the guard's interpreter")
        os.chmod(fmpy.saved_path(), 0o644)
        real = sys.executable
        try:
            sys.executable = good
            self.assertIsNone(self.target((3, 11, 2)), "already running under it: no loop")
        finally:
            sys.executable = real

    def test_none_found_is_remembered_until_doctor_looks_again(self):
        self.fake("python3.12", "3 11 9")
        self.assertIsNone(self.target((3, 11, 2)))
        self.assertIsNone(self.target((3, 11, 2)))
        self.assertEqual(self.runs("python3.12"), 1, "one search, not one per hook call")
        good = self.fake("python3.14", "3 14 0")
        self.assertIsNone(self.target((3, 11, 2)))
        old = os.environ["PATH"]
        os.environ["PATH"] = os.path.join(self.tmp, "bin")
        try:
            self.assertEqual(fmpy.refresh(), good)  # fm doctor searches again
        finally:
            os.environ["PATH"] = old
        self.assertEqual(self.target((3, 11, 2)), good)
        self.assertEqual(stat.S_IMODE(os.stat(fmpy.saved_path()).st_mode) & 0o022, 0)


class HookUnderOldPython(ForemanTestCase):
    """The dispatcher on a python3 below the floor (faked with a sitecustomize), with a saved interpreter."""

    def setUp(self):
        super().setUp()
        site = os.path.join(self.tmp, "site")
        os.makedirs(site)
        with open(os.path.join(site, "sitecustomize.py"), "w") as f:
            f.write("import sys\nsys.version_info = (3, 11, 2, 'final', 0)\n")
        self.old = {"PYTHONPATH": site}
        self.marker = os.path.join(self.tmp, "child.runs")

    def save(self, body):
        exe = os.path.join(self.tmp, "py312")
        with open(exe, "w") as f:
            f.write(f"#!/bin/sh\necho x >> {self.marker}\n{body}\n")
        os.chmod(exe, 0o755)
        os.makedirs(os.path.join(self.home, "state"), exist_ok=True)
        with open(os.path.join(self.home, "state", "python"), "w") as f:
            f.write(exe + "\n")
        os.chmod(os.path.join(self.home, "state", "python"), 0o644)

    def wipe(self):
        return self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {
            "command": f"rm -rf {os.path.join(self.home, 'plugin', 'lib')}"}}, env=self.old)

    def test_the_saved_interpreter_answers_for_the_hook(self):
        self.save(f'PYTHONPATH= exec {sys.executable} "$@"')  # the real (supported) python, without the fake
        p = self.wipe()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn("core", p.stderr)
        self.assertTrue(os.path.exists(self.marker), "the hook ran under the saved interpreter")

    def test_a_crashing_interpreter_never_opens_the_guard(self):
        # Claude Code reads exit 1 as allow: the dispatcher runs the guard itself when its child fails
        self.save("exit 1")
        p = self.wipe()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertTrue(os.path.exists(self.marker))
