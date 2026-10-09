"""T-0697 (Intelligence — verification reasoning): typed claims at the close, checks of the checks (zero tests ran,
stale evidence, a forged pass, catch rates), observable criteria and independent evidence."""
import json
import os
import time

from helpers import ForemanTestCase, read_text

import fmcore as c

REFS = os.path.join(c.PLUGIN_ROOT, "skills", "intake", "references")


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def task(self, *acs, focus=True):
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", "S",
                *[a for x in acs or ["ok :: true"] for a in ("--ac", x)], "--step", "s", *(["--focus"] if focus else []))
        return "T-0001"

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)


class Claims(Base):
    def test_finish_keeps_typed_claims_and_fm_pr_renders_them(self):
        tid = self.task()
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true",
                "--claim", "checked: empty input returns [] :: test_parser.py::test_empty",
                "--claim", "inferred: unicode works because the lexer is byte-agnostic")
        claims = c.find_brief(self.p, tid).section("Claims")
        self.assertIn("- [checked] empty input returns [] — evidence: test_parser.py::test_empty", claims)
        self.assertIn("- [inferred] unicode works", claims)
        self.assertIn("### Claims", self.fm("pr", tid).stdout)
        self.assertNotEqual(self.fm("task", "finish", tid, "--claim", "sure: x", check=False).returncode, 0)


class Verifier(Base):
    def test_a_run_where_zero_tests_ran_never_counts_as_a_pass(self):
        tid = self.task()  # already true before T-0697 (run_command); kept here as the member's check
        r = self.fm("task", "evidence", tid, "--step", "1", "--run",
                    "python3 -c \"print('Ran 0 tests in 0.0s'); print('OK')\"", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no tests ran", c.find_brief(self.p, tid).section("Verification evidence"))

    def test_the_oracle_asks_for_a_negative_twin(self):
        import fmideas
        self.assertIn("negative twin", fmideas.ORACLE)


class Stale(Base):
    def test_the_close_warns_when_a_file_a_check_names_changed_after_it_ran(self):
        self.write("a.txt", "ok\n")
        tid = self.task()
        self.fm("task", "evidence", tid, "--step", "1", "--run", "grep -q ok a.txt")
        later = time.time() + 5
        os.utime(os.path.join(self.repo, "a.txt"), (later, later))
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, tid), [])
        self.assertTrue(any("a.txt changed after" in w for w in warns), warns)


class Observable(Base):
    def test_criteria_name_what_the_user_will_see(self):
        self.assertIn("observable", read_text(os.path.join(REFS, "planning.md")).lower())
        self.assertIn("observable", read_text(os.path.join(REFS, "audit.md")).lower())
        self.assertIn("observable", self.fm("task", "new", "--help").stdout.lower())


class Independent(Base):
    def test_findings_need_a_reproducer_and_builders_name_their_weakest_link(self):
        import fmcli
        import fmlanes
        self.assertIn("reproducer", fmcli._REVIEW_OUT)
        self.assertIn("weakest link", fmlanes.CONTRACT)


class Forge(Base):
    def test_audit_prep_forge_asks_for_a_change_that_passes_the_check_but_breaks_the_criterion(self):
        self.write("a.txt", "ok\n")
        tid = self.task("the parser keeps headers :: grep -q ok a.txt")
        self.fm("audit", "prep", tid, "--forge")
        text = read_text(os.path.join(self.p.dir, "audits", f"{tid}.forge.md"))
        self.assertIn("the parser keeps headers", text)
        self.assertIn("grep -q ok a.txt", text)
        self.assertIn("forged pass", text)


class CatchRate(Base):
    def test_the_close_says_which_checks_have_ever_caught_a_failure(self):
        rows = []
        for t in ("T-0101", "T-0102"):
            rows += [{"ts": c.now(), "task": t, "event": "evidence", "data": {"cmd": "pytest -q", "result": "exit 1 · 1 failed"}},
                     {"ts": c.now(), "task": t, "event": "evidence", "data": {"cmd": "pytest -q", "result": "exit 0 · 3 passed"}}]
        rows += [{"ts": c.now(), "task": t, "event": "evidence", "data": {"cmd": "make lint", "result": "exit 0"}}
                 for t in ("T-0101", "T-0102", "T-0103")]
        rows += [{"ts": c.now(), "task": "T-0104", "event": "finish", "data": {"runs": 1, "failed": n, "ran": [["make test", n]]}}
                 for n in (1, 0)]  # T-0749: a failure the close itself recorded counts too
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
        tid = self.task("tests pass :: pytest -q", "lint is clean :: make lint", "suite :: make test")
        import fmcli
        warns = " ".join(fmcli._close_warnings(self.p, c.find_brief(self.p, tid), []))
        self.assertRegex(warns, r"`pytest -q` caught a failure in 2 task")
        self.assertRegex(warns, r"`make lint` never failed in 3 run")
        self.assertRegex(warns, r"`make test` caught a failure in 1 task")
