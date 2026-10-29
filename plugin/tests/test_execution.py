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
        self.write("x.py", "def f():\n    breakpoint()\n    print('ok')\n    msg = 'left a breakpoint() in'\n    print('DEBUG rows', 3)\n    return 1\n")
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, "T-0001"), ["x.py"])
        hit = [w for w in warns if "debug scaffolding" in w]
        self.assertTrue(hit and "x.py:2" in hit[0], warns)
        self.assertNotIn("x.py:3", hit[0])
        self.assertNotIn("x.py:4", hit[0])
        self.assertIn("x.py:5", hit[0])

    def test_prose_files_that_mention_debug_calls_stay_quiet(self):
        self.write("NOTES.md", "# notes\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "notes"], check=True)
        self.task()
        self.write("NOTES.md", "# notes\n- warns about `breakpoint()` and `console.log` left in code\n")
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, "T-0001"), ["NOTES.md"])
        self.assertFalse([w for w in warns if "debug scaffolding" in w], warns)


class BoardClose(Base):
    # T-0956: one verdict line before the close warnings, a Landed line last, conflict markers caught
    def committed(self, rel, text):
        self.write(rel, text)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "base"], check=True)

    def finish(self, *extra):
        return self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", *extra)

    def test_conflict_markers_and_debug_lines_in_changed_files_warn(self):
        self.committed("x.py", "A = 1\n")
        self.committed("app.js", "let a = 1;\n")
        self.task()
        self.write("x.py", "<" * 7 + " HEAD\nA = 1\n" + "=" * 7 + "\nA = 2\n" + ">" * 7 + " theirs\n")
        self.write("app.js", "let a = 1;\ndebugger;\nconsole.log(a);\n  debugger\n")
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, "T-0001"), ["x.py", "app.js"])
        conflict = [w for w in warns if "conflict marker" in w]
        self.assertTrue(conflict and all(f"x.py:{n}" in conflict[0] for n in (1, 3, 5)), warns)
        debug = [w for w in warns if "debug scaffolding" in w]
        self.assertTrue(debug and all(f"app.js:{n}" in debug[0] for n in (2, 3, 4)), warns)  # with or without ;

    def test_finish_prints_one_verdict_line_before_the_warnings(self):
        self.committed("x.py", "A = 1\n")
        self.task()
        self.write("x.py", "A = 1\nbreakpoint()\n" + ">" * 7 + " theirs\n")
        err = self.finish().stderr.splitlines()
        warns = [i for i, ln in enumerate(err) if ln.startswith("fm: warning: ")]
        verdict = [i for i, ln in enumerate(err) if ln.startswith(f"fm: {len(warns)} warnings: ")]
        self.assertTrue(warns and verdict and verdict[0] < warns[0], err)
        self.assertIn("debug scaffolding", err[verdict[0]])
        self.assertIn("conflict marker", err[verdict[0]])

    def test_a_fetched_ticket_s_close_names_the_post_back_command(self):  # T-1870: outward only when asked
        import fmcli
        self.committed("x.py", "A = 1\n")
        self.task()
        fmcli.mutate(self.p, "T-0001", lambda x: x.set_section("Raw request", "> Parser\n> CONTEXT: ticket jira "
                                                               "PROJ-12 0123456789ab, fetched by fm inbox ticket"), "t")
        self.write("x.py", "A = 2\n")
        out = self.finish("--commit", "Parser").stdout.strip().splitlines()
        self.assertEqual((out[-2], out[-1][:18]), ("Post it back (outward, only when wanted, once pushed): fm inbox ticket --post "
                                                   "T-0001 — one comment on jira PROJ-12", "Landed: committed "))

    def test_finish_ends_with_a_landed_line(self):
        self.committed("x.py", "A = 1\n")
        self.task()
        self.write("x.py", "A = 2\n")
        self.assertEqual(self.finish().stdout.strip().splitlines()[-1], "Landed: not committed (1 file uncommitted)")
        self.fm("task", "new", "Again", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.write("x.py", "A = 3\n")
        last = self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true", "--commit", "Again",
                       "--with", "x.py").stdout.strip().splitlines()[-1]  # T-1169: x.py was left dirty at focus
        sha = subprocess.run(["git", "-C", self.repo, "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True).stdout.strip()
        self.assertEqual(last, f"Landed: committed {sha} · not pushed")
        remote = os.path.join(self.tmp, "remote.git")
        subprocess.run(["git", "init", "-q", "--bare", remote], check=True)
        subprocess.run(["git", "-C", self.repo, "push", "-q", remote, "HEAD:refs/heads/main"], check=True)
        subprocess.run(["git", "-C", self.repo, "fetch", "-q", remote, "main:refs/remotes/origin/main"], check=True)
        import fmcli
        self.assertEqual(fmcli._landed(self.p, c.find_brief(self.p, "T-0002")), f"Landed: committed {sha} · pushed")

    def test_landed_counts_only_this_tasks_files_and_shows_on_a_commit_retry(self):
        self.committed("x.py", "A = 1\n")
        self.committed("y.py", "B = 1\n")
        self.task()
        self.write("x.py", "A = 2\n")
        self.write("y.py", "B = 2\n")  # another task's edit, still uncommitted
        c.log_event(self.p, "touched", task="T-0009", data={"file": os.path.join(self.repo, "y.py")})
        out = self.finish("--commit", "x").stdout
        sha = subprocess.run(["git", "-C", self.repo, "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True).stdout.strip()
        self.assertEqual(out.strip().splitlines()[-1], f"Landed: committed {sha} · not pushed")
        self.assertIn("Landed: committed", self.fm("task", "finish", "T-0001", "--commit", "again").stdout)

    def test_tier_drift_has_a_short_kind_in_the_verdict(self):
        import fmcli
        self.assertEqual(fmcli._warning_kind("T-0956 was planned S, but its diff is M-sized (3 files, 90 lines): x"),
                         "tier drift")
        self.assertEqual(fmcli._warning_kind("debug scaffolding in added lines: a.py:3"), "debug scaffolding")
