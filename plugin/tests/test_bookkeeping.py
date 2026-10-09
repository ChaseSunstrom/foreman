"""T-0704 (Frontier 04, first slice): bookkeeping that takes no model turns. Over 14 days 618 fm task evidence calls
re-ran a command the session had just run and 135 finishes were refused and retried; a handoff is trusted only while
its failure still reproduces."""
import os

from helpers import ForemanTestCase
from test_hooks import HookCase

import fmcore as c

OK = {"stdout": "3 passed", "stderr": "", "interrupted": False}


class StepEvidence(HookCase):
    def ran(self, cmd):
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}, "tool_response": OK})
        return c.find_brief(self.project(), self.tid)

    def test_a_passing_run_through_a_criterion_runner_verifies_the_current_step(self):
        self.fm("init")
        self.tid = self.task(steps=("build it", "wire it"))
        self.fm("task", "ac", self.tid, "add", "all pass", "--verify", "python3 tests/run.py -p all")
        self.assertFalse(self.ran("ls").has_evidence(step=1), "not a test run")
        self.assertFalse(self.ran("python3 tests/run.py -k one | tail -3").has_evidence(step=1), "a pipe hides its exit")
        b = self.ran("cd /x && python3 tests/run.py -k one")
        self.assertTrue(b.has_evidence(step=1))
        self.assertTrue(any("(step 1)" in l and "[ran]" in l for l in b.evidence()), b.evidence())
        self.assertFalse(b.has_evidence(step=2), "one run verifies one step")

    def test_a_step_about_failing_tests_is_not_verified_by_a_pass(self):
        self.fm("init")
        self.tid = self.task(steps=("failing tests first", "fix"))
        self.fm("task", "ac", self.tid, "add", "all pass", "--verify", "pytest tests")
        self.assertFalse(self.ran("pytest -k login").has_evidence(step=1))


class FinishGaps(HookCase):
    def test_one_refusal_names_every_gap(self):
        self.fm("init")
        tid = self.task(type_="FEATURE", tier="M", steps=("build it",))
        r = self.fm("task", "finish", tid, "--audit", "self review", "--lens", "edge: fine", check=False)
        self.assertNotEqual(r.returncode, 0)
        for gap in ("step 1", "intent", "docs", "lesson"):
            self.assertIn(gap, r.stderr + r.stdout)


class Reproduce(ForemanTestCase):
    def test_a_handoff_is_accepted_only_while_its_failure_reproduces(self):
        self.fm("init")
        with open(os.path.join(self.repo, "check.py"), "w") as f:
            f.write("raise SystemExit(1)\n")
        self.fm("task", "new", "Fix check", "--type", "FIX", "--tier", "S", "--ac", "check passes :: python3 check.py",
                "--step", "fix", "--focus")
        self.fm("task", "evidence", "T-0001", "--run", "python3 check.py", check=False)
        self.fm("task", "packet", "T-0001")
        with open(os.path.join(self.home, "state", "projects", c.find_project(self.repo).slug, "handoffs",
                               "T-0001.md")) as f:
            packet = f.read()
        self.assertIn("## Reproduce", packet)
        self.assertIn("python3 check.py", packet.split("## Reproduce")[1])
        r = self.fm("task", "packet", "T-0001", "--check")
        self.assertIn("reproduces", r.stdout)
        with open(os.path.join(self.repo, "check.py"), "w") as f:
            f.write("pass\n")
        r = self.fm("task", "packet", "T-0001", "--check", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("stale", r.stdout + r.stderr)
