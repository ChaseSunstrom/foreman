"""T-2636: fm prove --steer runs each unsettled user-steer row's [check:] on the start tree of the task its text names;
a check that passes there too tests nothing about its rule."""
import json
import os
import subprocess

from helpers import ForemanTestCase

RUNNER = "import os, sys\nsys.exit(0 if os.path.exists(sys.argv[1] + '.flag') else 1)\n"


class ProveSteer(ForemanTestCase):
    def sh(self, *a):
        subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True)

    def put(self, rel, text=""):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def rule(self, text, check):
        self.fm("decide", text, "--cites", "user steer: a rule", "--check",
                f"python3 plugin/tests/run.py {check}" if check else "fm genesis check")

    def test_a_check_that_passes_on_the_start_tree_is_vacuous_and_one_that_fails_there_tests_its_rule(self):
        self.fm("init")
        self.put("plugin/tests/run.py", RUNNER)
        self.put("test_old.flag")  # already green before the task: its check can't test a new rule
        self.sh("add", "-A")
        self.sh("commit", "-qm", "base")
        tid = json.loads(self.fm("task", "new", "a rule", "--type", "FEATURE", "--tier", "S", "--ac",
                                 "done :: true", "--step", "s", "--focus", "--json").stdout)["id"]
        self.put("test_new.flag")  # the task's change makes this one green
        self.rule(f"{tid}: new rule", "test_new")
        self.rule(f"{tid}: old rule", "test_old")
        self.rule("no task named here", "test_new")
        self.rule("T-9999: unknown task", "test_new")
        r = self.fm("prove", "--steer", check=False)  # runs this tree's tests: never without the run consent
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("needs the user's yes, once per tree: fm prove --steer --yes-run", r.stderr)
        self.assertNotIn("pass --yes-run", r.stderr)  # T-2732: the flag is the user's; the agent was told to pass it
        self.assertNotIn("vacuous", r.stdout)
        r = self.fm("prove", "--steer", "--yes-run", check=False)
        out = r.stdout
        self.assertEqual(r.returncode, 1, out + r.stderr)
        line = {k: next(x for x in out.splitlines() if k in x) for k in ("new rule", "old rule", "no task", "unknown")}
        self.assertIn("tests its rule", line["new rule"])
        self.assertIn(tid, line["new rule"])  # the task used is named
        self.assertIn("vacuous", line["old rule"])
        self.assertIn("no task named", line["no task"])
        self.assertIn("no start snapshot", line["unknown"])

    def test_no_vacuous_row_exits_0(self):
        self.fm("init")
        self.put("plugin/tests/run.py", RUNNER)
        self.sh("add", "-A")
        self.sh("commit", "-qm", "base")
        tid = json.loads(self.fm("task", "new", "a rule", "--type", "FEATURE", "--tier", "S", "--ac",
                                 "done :: true", "--step", "s", "--focus", "--json").stdout)["id"]
        self.put("test_new.flag")
        self.rule(f"{tid}: new rule", "test_new")
        r = self.fm("prove", "--steer", "--yes-run", check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("tests its rule", r.stdout)


if __name__ == "__main__":
    import unittest
    unittest.main()
