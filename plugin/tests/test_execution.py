"""T-0695 (Intelligence — steps and execution craft): steps with expected output, diff files checked against steps,
repeated failing commands noticed, a preflight at focus, a resume that re-runs the last green check, and debug
scaffolding caught at the close."""
import os
import subprocess

from helpers import ForemanTestCase, read_text

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def task(self, *steps, scope=None, focus=True):
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                *[a for s in steps or ["s"] for a in ("--step", s)], *(["--scope", scope] if scope else []),
                *(["--focus"] if focus else []))
        return "T-0001"

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def evidence(self, cmd, step="1"):
        r = self.fm("task", "evidence", "T-0001", "--step", step, "--run", cmd, check=False)
        return r.stdout + r.stderr


class Expect(Base):
    def test_a_steps_expected_output_is_compared_with_the_run(self):
        self.task("Count the rows (expect: 3 rows)")
        self.assertIn("expected \"3 rows\"", self.evidence("echo 2 rows"))
        self.assertIn("expect missed", c.find_brief(self.p, "T-0001").section("Verification evidence"))
        self.evidence("echo 3 rows")
        self.assertIn("expect ✓", c.find_brief(self.p, "T-0001").section("Verification evidence"))


class PlanCheck(Base):
    def test_audit_prep_maps_changed_files_to_the_steps_that_name_them(self):
        self.task("Edit parser.py to read headers")
        self.write("parser.py", "X = 1\n")
        self.write("other.py", "Y = 1\n")
        self.fm("audit", "prep", "T-0001")
        brief = read_text(os.path.join(self.p.dir, "audits", "T-0001.review.md"))
        self.assertIn("## Files vs steps", brief)
        self.assertIn("parser.py — step 1", brief)
        self.assertIn("other.py — no step names it", brief)


class Tried(Base):
    def test_a_third_identical_failing_command_is_noticed_and_resume_lists_it(self):
        self.task()
        self.evidence("sh -c 'exit 1'")
        self.evidence("sh -c 'exit 1'")
        self.assertIn("failed 3 times", self.evidence("sh -c 'exit 1'"))
        self.assertRegex(self.fm("resume", "--no-check").stdout, r"Tried on step 1: .*sh -c 'exit 1' ×3")


class Preflight(Base):
    def test_first_focus_reports_missing_scope_and_no_gate_baseline(self):
        self.task(scope="lib/missing.py", focus=False)
        out = self.fm("focus", "T-0001").stdout
        self.assertIn("Preflight", out)
        self.assertIn("lib/missing.py doesn't exist", out)
        self.assertIn("no fm check on this tree", out)


class ResumeCheck(Base):
    def test_resume_reruns_the_last_green_check_and_reports_drift(self):
        self.write("a.txt", "ok\n")
        self.task()
        self.evidence("test -f a.txt")
        self.assertIn("still passes", self.fm("resume").stdout)
        os.remove(os.path.join(self.repo, "a.txt"))
        self.assertIn("now fails", self.fm("resume").stdout)


class Scaffold(Base):
    def test_debug_scaffolding_in_added_lines_warns_at_close(self):
        self.write("x.py", "def f():\n    return 1\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "x"], check=True)
        self.task()
        self.write("x.py", "def f():\n    breakpoint()\n    print('ok')\n    return 1\n")
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, "T-0001"), ["x.py"])
        hit = [w for w in warns if "debug scaffolding" in w]
        self.assertTrue(hit and "x.py:2" in hit[0], warns)
        self.assertNotIn("x.py:3", hit[0])

    def test_prose_files_that_mention_debug_calls_stay_quiet(self):
        self.write("NOTES.md", "# notes\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "notes"], check=True)
        self.task()
        self.write("NOTES.md", "# notes\n- warns about `breakpoint()` and `console.log` left in code\n")
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, "T-0001"), ["NOTES.md"])
        self.assertFalse([w for w in warns if "debug scaffolding" in w], warns)
