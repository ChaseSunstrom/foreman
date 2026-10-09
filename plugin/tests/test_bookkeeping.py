"""T-0704 (Frontier 04, first slice): bookkeeping that takes no model turns. Over 14 days 618 fm task evidence calls
re-ran a command the session had just run and 135 finishes were refused and retried; a handoff is trusted only while
its failure still reproduces."""
import os
import subprocess

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


class CommitOwnFiles(HookCase):
    """T-0738: T-0706's commit took T-0707's new files: both edited neighbouring lines of shared files, so re-basing
    T-0706's start snapshot failed and its commit fell back to everything changed since; T-0707's then had nothing."""

    def edit(self, rel, text):
        path = os.path.join(self.repo, rel)
        with open(path, "w") as f:
            f.write(text)
        self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": path}, "tool_response": {}})

    def setUp(self):
        super().setUp()
        self.fm("init")
        with open(os.path.join(self.repo, "shared.py"), "w") as f:
            f.write("X = 0\nY = 0\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "shared"], check=True)
        self.fm("task", "new", "First", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.edit("shared.py", "X = 1\nY = 0\n")
        self.fm("task", "new", "Second", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.edit("shared.py", "X = 1\nY = 2\n")  # the next line: the paused task's snapshot can't be re-based

    def shown(self):
        return subprocess.run(["git", "-C", self.repo, "show", "--stat", "--format=", "HEAD"], capture_output=True,
                              text=True).stdout

    def test_a_file_only_another_task_edited_stays_out(self):
        self.edit("theirs.py", "B = 1\n")
        self.fm("focus", "T-0001")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--commit", "First")
        self.assertIn("shared.py", self.shown())
        self.assertNotIn("theirs.py", self.shown())

    def test_a_commit_with_nothing_left_says_so(self):
        self.fm("focus", "T-0001")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--commit", "First")
        self.fm("focus", "T-0002")
        r = self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true", "--commit", "Second", check=False)
        self.assertIn("nothing to commit", r.stdout + r.stderr)


class CommitAfterFocus(HookCase):
    def test_a_file_another_task_edited_before_this_one_started_is_still_committed(self):
        # T-0739: T-0684's own shell edits of CHANGELOG.md were left out because T-0683 had edited it after T-0684 was
        # captured (but before it was focused)
        self.fm("init")
        self.fm("capture", "Later work")  # T-0001, captured long before it is worked
        self.fm("task", "new", "First", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        notes = os.path.join(self.repo, "notes.md")
        with open(notes, "w") as f:
            f.write("one\n")
        self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": notes}, "tool_response": {}})
        self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true", "--commit", "First")
        self.fm("task", "new", "Later work", "--from", "T-0001", "--type", "FEATURE", "--tier", "S")
        self.fm("task", "ac", "T-0001", "add", "ok", "--verify", "true")
        self.fm("task", "step", "T-0001", "add", "s")
        self.fm("focus", "T-0001")
        with open(notes, "a") as f:  # through the shell: no touched event of its own
            f.write("two\n")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--commit", "Later")
        shown = subprocess.run(["git", "-C", self.repo, "show", "--stat", "--format=%s", "HEAD"], capture_output=True,
                               text=True).stdout
        self.assertTrue(shown.startswith("Later"), shown)  # its own commit, not the one before
        self.assertIn("notes.md", shown)


class FinalRun(ForemanTestCase):
    def test_run_is_the_final_check_even_when_every_step_has_evidence(self):
        # T-0742: T-0686's close skipped --run (every step had evidence), so the full suite never ran at the close
        self.fm("init")
        self.fm("task", "new", "Two steps", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "a", "--focus")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        r = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "false", check=False)
        self.assertNotEqual(r.returncode, 0, "a failing final check stops the close")
        self.assertNotEqual(c.find_brief(c.find_project(self.repo), "T-0001").status, "done")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true")
        self.assertTrue(any("`true` → exit 0" in l and "[ran]" in l
                            for l in c.find_brief(c.find_project(self.repo), "T-0001").evidence()))
