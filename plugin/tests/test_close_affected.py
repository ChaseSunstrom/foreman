"""T-3526: a close whose linked tests are a gate's runner plus module names, after the gates' full pass on the same
code tree (a merge train's), runs nothing: the suite already ran them. No pass, or another runner: they run once."""
import os
import shutil
import subprocess
import unittest

from helpers import ForemanTestCase

from sampo import core as c

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "def add(a, b):\n    return a + b\n"


class CloseAffectedReuse(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.count = os.path.join(self.tmp, "count")  # outside the repo: a run must not change the tree it's judged on
        os.makedirs(os.path.join(self.repo, "tests"))
        shutil.copy(os.path.join(HERE, "run.py"), os.path.join(self.repo, "tests", "run.py"))
        self.write("calc.py", SRC)
        self.write("tests/test_calc.py",
                   "import os, sys, unittest\nsys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))\n"
                   "import calc\n\n\nclass Calc(unittest.TestCase):\n    def test_add(self):\n"
                   f"        open({self.count!r}, 'a').write('x\\n')\n        self.assertEqual(calc.add(1, 2), 3)\n")
        self.write(".gitignore", "__pycache__/\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "suite"], check=True)
        self.fm("check", "add", "python3 tests/run.py")
        self.fm("check", "affected", "python3 tests/run.py {names}")
        self.p = c.find_project(self.repo)

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def runs(self):
        try:
            with open(self.count) as f:
                return len(f.read().split())
        except OSError:
            return 0

    def close(self):
        tid = self.fm_json("task", "new", "Change add", "--type", "FEATURE", "--tier", "S", "--ac", "works :: true",
                           "--step", "s", "--scope", "calc.py")["id"]
        self.fm("focus", tid)
        self.write("calc.py", SRC + "# tidy\n")
        return tid

    def finish(self, tid):
        r = self.fm("task", "finish", tid, "--audit", "self", "--run", "true", check=False,
                    env={"FOREMAN_SENTINEL": "off"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout, c.ledger_events(self.p, ("close_affected",))[-1]["data"]

    def test_a_green_full_pass_on_the_same_tree_covers_the_linked_tests(self):
        tid = self.close()
        self.fm("check", env={"FOREMAN_SENTINEL": "off"})  # the train's full pass, on the merged code
        before = self.runs()
        out, ev = self.finish(tid)
        self.assertEqual(self.runs(), before, "the linked tests ran again on code the gates just passed")
        self.assertIn("linked tests: covered by the gates' pass (run ", out)
        self.assertEqual(ev["exit"], 0)
        self.assertIn("code_tree", ev["reused"])

    def test_no_pass_runs_them_once(self):
        out, ev = self.finish(self.close())
        self.assertEqual(self.runs(), 1)
        self.assertNotIn("reused", ev)
        self.assertNotIn("covered by the gates", out)

    def test_another_runner_runs_them_once_despite_the_pass(self):
        self.fm("check", "affected", "python3 -B tests/run.py {names}")
        tid = self.close()
        self.fm("check", env={"FOREMAN_SENTINEL": "off"})
        before = self.runs()
        out, ev = self.finish(tid)
        self.assertEqual(self.runs(), before + 1)
        self.assertNotIn("reused", ev)


if __name__ == "__main__":
    unittest.main()
