"""T-0693 (Intelligence — reasoning and thought process): the stuck ladder names the kind of stall, a devil's advocate
role for the plan read, a typed case file in the brief, and beliefs with kill criteria."""
import os

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def task(self, tier="S"):
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", tier, "--interpretation", "x", "--approach",
                "a vs b: a", "--ac", "ok :: true", "--step", "s", "--focus")
        return "T-0001"

    def fail_runs(self, tid, *outputs):
        for o in outputs:
            self.fm("task", "evidence", tid, "--step", "1", "--run", f"sh -c 'echo {o}; exit 1'", check=False)


class Stall(Base):
    def test_the_same_error_again_is_named_as_a_stall_on_the_cause(self):
        tid = self.task()
        self.fail_runs(tid, "KeyError col", "KeyError col")
        self.assertRegex(self.fm("next").stdout, r"stuck, rung 2.*same error 2×")

    def test_changing_errors_are_progress_toward_the_smallest_next_step(self):
        tid = self.task()
        self.fail_runs(tid, "KeyError col", "TypeError none")
        self.assertRegex(self.fm("next").stdout, r"stuck, rung 2.*errors change.*smallest next step")

    def test_an_environment_failure_points_at_the_setup(self):
        tid = self.task()
        self.fail_runs(tid, "pytest: command not found", "pytest: command not found")
        self.assertRegex(self.fm("next").stdout, r"stuck, rung 2.*environment")


class Devil(Base):
    def test_second_plan_has_a_devils_advocate_role(self):
        import fmsecond
        self.assertIn("rejected", fmsecond.ROLES["devil"])
        self.assertIn("devil", self.fm("second", "--help").stdout)


class Notes(Base):
    def test_typed_notes_live_in_the_brief_and_print_at_checkpoint_and_resume(self):
        tid = self.task()
        self.fm("task", "note", tid, "fact", "the API caps pages at 100")
        self.fm("task", "note", tid, "question", "does the export need headers?")
        self.assertIn("- [question] does the export need headers?", c.find_brief(self.p, tid).section("Notes"))
        self.assertIn("the API caps pages at 100", self.fm("checkpoint").stdout)
        self.assertIn("does the export need headers?", self.fm("resume").stdout)


class Beliefs(Base):
    def test_an_open_assumption_with_a_kill_criterion_shows_in_fm_next(self):
        tid = self.task("M")
        self.fm("task", "assume", tid, "add", "the cache is warm", "--kill", "a cold start takes over 2 s")
        self.assertRegex(self.fm("next").stdout, r"open beliefs: A1 the cache is warm \(dead if a cold start takes")
        self.fm("task", "assume", tid, "verify", "1", "--run", "true")
        self.assertNotIn("open beliefs", self.fm("next").stdout)
