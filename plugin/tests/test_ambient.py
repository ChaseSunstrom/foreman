"""T-0705 (Frontier 05, first slice): ambient verification. Affected tests run after each edit, out of the model's
turns; only a flip reaches it, once; a pass never closes a step (T-0994)."""
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

    def test_a_flip_is_reported_once_and_a_pass_never_closes_the_step(self):
        self.fm("check", "ambient", "on")
        self.edit("def add(a, b):\n    return a - b\n")
        first = self.note()
        self.assertIn("now fail", first)
        self.assertIn("test_calc", first)
        self.assertNotIn("Ambient", self.note(), "a flip is said once")
        self.edit("def add(a, b):\n    return a - b  # still wrong\n")
        self.assertNotIn("Ambient", self.note(), "still failing is not a flip")
        self.edit(GOOD)
        back = self.note()
        self.assertIn("pass again", back)
        # T-0994: a pass mid-step says nothing about the step being done (it closed T-0989's 'docs' step); the note
        # says how to record it when it is
        self.assertIn(f"fm task evidence {self.tid} --step 1 --run", back)
        b = c.find_brief(self.project(), self.tid)
        self.assertFalse(b.has_evidence(step=1), b.evidence())

    def test_a_failing_note_names_the_failing_tests_not_the_runners_timing(self):
        # T-1275: 'Ran 44 tests in 1.6s (12 classes …)' made these notes 23 KB over 92 edits
        self.fm("check", "ambient", "on")
        self.write("test_calc.py", TEST + "\n    def test_sub(self):\n        self.assertEqual(calc.add(3, 1), 4)\n")
        self.edit("def add(a, b):\n    return a - b\n")
        first = self.note()
        self.assertIn("test_add", first)
        self.assertIn("test_sub", first)
        self.assertNotIn("Ran ", first)
        self.assertNotIn("classes", first)
        self.assertLessEqual(len(first.split("Ambient tests:")[1]) + len("Ambient tests:"), 220, first)
        self.edit(GOOD)
        back = self.note()
        self.assertIn("pass again", back)
        self.assertLessEqual(len(back), 200, back)

    def test_a_test_the_runner_cant_run_is_left_out(self):
        # T-0994: a .tsx test went to 'python3 plugin/tests/run.py widget.test', which ran nothing and read as a pass
        import json
        self.write("widget.test.tsx", "test('x', () => {})\n")
        self.write("calc.py", "def add(a, b):\n    return a + b  # touched\n")
        out = json.loads(self.fm("check", "--affected", "--json").stdout)
        self.assertIn("test_calc.py", out["tests"])
        self.assertNotIn("widget.test.tsx", out["tests"])
