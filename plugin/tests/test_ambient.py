"""T-0705 (Frontier 05, first slice): ambient verification. Affected tests run after each edit, out of the model's
turns; only a flip reaches it, once, and a pass is the step's evidence."""
import os
import subprocess

from test_hooks import HookCase, parse

import fmcore as c

SYNC = {"FOREMAN_AMBIENT_SYNC": "1"}
GOOD = "def add(a, b):\n    return a + b\n"
TEST = "import unittest\nimport calc\n\n\nclass T(unittest.TestCase):\n    def test_add(self):\n" \
       "        self.assertEqual(calc.add(1, 2), 3)\n"


class Ambient(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.write("calc.py", GOOD)
        self.write("test_calc.py", TEST)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "calc"], check=True)
        self.fm("check", "affected", "python3 -m unittest -q {names}")
        self.tid = self.task(type_="FEATURE", steps=("change add", "wire it"))

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def edit(self, text):
        self.write("calc.py", text)
        self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(self.repo, "calc.py")},
                                  "tool_response": {}}, env=SYNC, timeout=60)

    def note(self):
        r = parse(self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "ls"}})) or {}
        return (r.get("hookSpecificOutput") or {}).get("additionalContext") or ""

    def test_off_by_default(self):
        self.edit("def add(a, b):\n    return a - b\n")
        self.assertNotIn("Ambient", self.note())

    def test_a_flip_is_reported_once_and_a_pass_is_the_steps_evidence(self):
        self.fm("check", "ambient", "on")
        self.edit("def add(a, b):\n    return a - b\n")
        first = self.note()
        self.assertIn("now fail", first)
        self.assertIn("test_calc", first)
        self.assertNotIn("Ambient", self.note(), "a flip is said once")
        self.edit("def add(a, b):\n    return a - b  # still wrong\n")
        self.assertNotIn("Ambient", self.note(), "still failing is not a flip")
        self.edit(GOOD)
        self.assertIn("pass again", self.note())
        b = c.find_brief(self.project(), self.tid)
        self.assertTrue(b.has_evidence(step=1), b.evidence())
