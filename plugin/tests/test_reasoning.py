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
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", tier, "--interpretation", "Reading 1: a. Reading 2: b.", "--approach",
                "1) a; fails if: x 2) use what exists: b; fails if: y 3) do less: c; fails if: z Choice 1 (80%): a", "--ac", "ok :: true", "--step", "s", "--focus")
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


class Race(Base):  # T-2271 (Mission 5, #2): stuck with a runner-up approach on file, race it before more hypotheses
    def brief(self, tier="S", approach="1) a regex scan 2) a real parser. Choice 1 (80%): smaller"):
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", tier, "--interpretation", "Reading 1: a. Reading 2: b.", "--approach",
                approach, "--ac", "ok :: true", "--step", "s", "--focus")
        self.fail_runs("T-0001", "KeyError col", "KeyError col", "KeyError col")
        return self.fm("next").stdout

    def test_three_failed_runs_with_an_alternative_race_the_runner_up(self):
        self.assertRegex(self.brief(), r"stuck, rung 3.*fm lane race T-0001")

    def test_one_approach_keeps_the_hypothesis_rung(self):
        out = self.brief(approach="a regex scan")
        self.assertNotIn("fm lane race", out)
        self.assertRegex(out, r"stuck, rung 3.*hypotheses")

    def test_a_task_already_raced_keeps_the_hypothesis_rung(self):
        self.brief()
        b = c.find_brief(self.p, "T-0001")
        b.meta["race"] = "T-0002"
        c.save_brief(self.p, b)
        self.assertNotIn("fm lane race", self.fm("next").stdout)


class Confidence(Base):  # T-2338 (Mission 5, #8): a choice under the race bar, with a runner-up, races before any edit
    OPTS = "1) a regex scan; fails if: slow 2) use what exists: a real parser; fails if: heavy 3) do less: skip it; fails if: unmet. "

    def task(self, tier="S", choice="Choice 1 (40%): smaller", opts=None, focus=True):
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", tier, "--interpretation", "Reading 1: a. Reading 2: b.",
                "--approach", (opts or self.OPTS) + choice, "--ac", "ok :: ls", "--step", "s", *(["--focus"] if focus and tier != "L" else []))
        if tier == "L":
            self.fm("task", "set", "T-0001", "--section", "Risks and rollback", "--text", "It breaks; revert.")
            b = c.find_brief(self.p, "T-0001")
            b.meta["approved"] = "true"  # the approval gate has its own tests; this one is about the race ask
            c.save_brief(self.p, b)
            if focus:
                self.fm("focus", "T-0001")
        return "T-0001"

    def nxt(self):
        return self.fm("next").stdout

    def test_an_s_choice_under_the_race_bar_with_a_runner_up_names_the_race_before_any_edit(self):
        self.task("S")
        self.assertRegex(self.nxt(), r"confidence 40%.*fm lane race T-0001")

    def test_an_m_choice_under_the_race_bar_with_a_runner_up_names_the_race_before_any_edit(self):
        self.task("M")
        self.assertRegex(self.nxt(), r"confidence 40%.*fm lane race T-0001")

    def test_a_confident_choice_is_not_raced(self):
        self.task(choice="Choice 1 (90%): smaller")
        self.assertNotIn("fm lane race", self.nxt())

    def test_a_lone_approach_is_not_raced(self):
        self.task(opts="a regex scan only. ", choice="Choice 1 (40%): the only way")
        self.assertNotIn("fm lane race", self.nxt())

    def test_a_task_with_work_on_it_is_not_asked(self):
        tid = self.task()
        self.assertIn("fm lane race", self.nxt())
        self.fm("task", "evidence", tid, "--step", "1", "--run", "ls")
        self.assertNotIn("confidence 40%", self.nxt())

    def test_a_raced_task_and_its_b_side_are_never_asked_again(self):
        tid = self.task()
        b = c.find_brief(self.p, tid)
        for key in ("race", "race_of"):
            b.meta[key] = "T-0002"
            c.save_brief(self.p, b)
            self.assertNotIn("fm lane race", self.nxt(), key)
            b.meta.pop(key)

    def test_the_race_the_next_action_names_starts(self):
        tid = self.task()
        self.assertEqual(self.fm("lane", "race", tid, "--json", check=False).returncode, 0)
        self.assertNotIn("fm lane race", self.nxt())

    def test_a_race_that_cant_start_gives_the_released_task_back_focused(self):  # T-2338 review
        import argparse
        from unittest import mock
        import fmlanes
        tid = self.task()
        self.assertEqual(c.find_brief(self.p, tid).status, "active")
        with mock.patch.object(fmlanes, "builder_brief", side_effect=RuntimeError("no lane")):
            with self.assertRaises(RuntimeError):
                fmlanes.race(self.p, c.find_brief(self.p, tid), argparse.Namespace(confidence=None, json=True))
        b = c.find_brief(self.p, tid)
        self.assertEqual(b.status, "active")
        self.assertNotIn("race", b.meta)
        self.assertEqual(c.find_brief(self.p, "T-0002").status, "dropped")

    def test_a_ready_task_is_raced_before_it_is_focused(self):
        self.task(focus=False)
        self.assertRegex(self.nxt(), r"fm lane race T-0001")

    def test_an_l_task_names_the_design_race(self):
        self.task("L")
        self.assertRegex(self.nxt(), r"design race.*fm second plan T-0001")
        self.assertNotIn("fm lane race", self.nxt())

    def test_the_stuck_rung_names_what_race_line_builds(self):
        tid = self.task(choice="Choice 1 (90%): smaller")
        line = c.race_line(c.find_brief(self.p, tid))
        self.assertIn("fm lane race T-0001", line)
        self.fail_runs(tid, "KeyError col", "KeyError col", "KeyError col")
        self.assertIn(line, self.nxt())

    def test_the_trigger_names_what_race_line_builds(self):
        tid = self.task()
        self.assertIn(c.race_line(c.find_brief(self.p, tid)), self.nxt())


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
