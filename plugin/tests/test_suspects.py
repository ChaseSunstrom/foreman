"""T-0706 (Frontier 06, first slice): a red run arrives with ranked suspects, the minimal failing delta and the failure
state, before the agent starts guessing."""
import os
import subprocess
import sys
import unittest

from test_hooks import HookCase, parse

CALC = "def add(a, b):\n    return a + b\n" + "".join(f"\n\ndef f{i}(x):\n    return x * {i}\n" for i in range(6)) \
       + "\n\ndef sub(a, b):\n    return a - b\n"
TEST = ("import unittest\nimport calc\n\n\nclass T(unittest.TestCase):\n    def test_add(self):\n"
        "        got = calc.add(1, 2)\n        self.assertEqual(got, 3)\n\n    def test_sub(self):\n"
        "        self.assertEqual(calc.sub(3, 1), 2)\n")
RUN = "python3 -m unittest -q test_calc"


class Base(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.write("calc.py", CALC)
        self.write("util.py", "def helper():\n    return 1\n")
        self.write("test_calc.py", TEST)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "calc"], check=True)
        self.task(type_="FIX", steps=("find it", "fix it"))

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def break_it(self):
        self.write("calc.py", CALC.replace("return a - b\n", "return a - b  # sub\n").replace("return a + b",
                                                                                                "return a - b"))
        self.write("util.py", "def helper():\n    return 1  # tidied\n")
        self.write("notes.py", "NOTE = 1\n")  # untracked, benign

    def run_tests(self):
        return subprocess.run(RUN.split(), cwd=self.repo, capture_output=True, text=True)


class Suspects(Base):
    def test_the_changed_file_on_the_stack_ranks_first_with_its_reasons(self):
        self.break_it()
        out = self.fm("suspects", input=self.run_tests().stderr).stdout
        first = next(l for l in out.splitlines() if l.strip().startswith("1."))
        self.assertIn("calc.py", first)
        self.assertIn("changed", first)
        self.assertNotIn("util.py", first)

    def test_a_failing_test_run_note_names_the_top_suspects(self):
        self.break_it()
        err = self.run_tests().stderr
        r = parse(self.hook("PostToolUseFailure", {"tool_name": "Bash", "tool_input": {"command": RUN},
                                                   "error": "Exit code 1\n" + err})) or {}
        self.assertIn("Suspects", (r.get("hookSpecificOutput") or {}).get("additionalContext") or "")


class WhyRed(Base):
    def test_the_one_hunk_that_turns_it_red_is_named(self):
        self.break_it()
        out = self.fm("whyred", RUN, check=False).stdout
        self.assertIn("calc.py", out)
        self.assertIn("return a - b", out.split("Minimal")[1] if "Minimal" in out else "")
        self.assertNotIn("# sub", out.split("Minimal")[1] if "Minimal" in out else "x# sub")
        self.assertNotIn("tidied", out)


@unittest.skipIf(sys.version_info < (3, 12), "sys.monitoring needs Python 3.12")
class Record(Base):
    def test_the_locals_where_the_failure_unwound_are_shown(self):
        self.break_it()
        out = self.fm("record", RUN, check=False).stdout
        self.assertIn("test_add", out)
        self.assertRegex(out, r"got\s*=\s*-1")
