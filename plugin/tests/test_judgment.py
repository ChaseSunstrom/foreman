"""T-0688 (Intelligence — judgment, taste and decisions): doors, implicit decisions, the cheapest version, follow-ups
answered ahead, precedent, taste from overwrites, and how often decisions get reversed."""
import os
import subprocess

from helpers import ForemanTestCase, read_text

import fmcore as c

REFS = os.path.join(c.PLUGIN_ROOT, "skills", "intake", "references")
STUB = r'''#!/usr/bin/env python3
import sys
sys.stdin.read()
print("The cheapest version that meets it: a plain CSV export from the existing table, no new UI.")
'''


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)


class Doors(Base):
    def test_execution_classifies_forks_as_one_or_two_way_doors(self):
        text = read_text(os.path.join(REFS, "execute.md")).lower()
        self.assertIn("one-way door", text)
        self.assertIn("two-way door", text)


class Implicit(Base):
    def test_reviews_ask_for_the_decisions_taken_by_default(self):
        self.assertIn("implicit decisions", read_text(os.path.join(REFS, "audit.md")).lower())
        self.assertIn("implicit decisions", read_text(os.path.join(c.PLUGIN_ROOT, "agents", "fm-reviewer.md")).lower())


class Cheapest(Base):
    def test_a_child_argues_the_cheapest_version_into_the_brief(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.fm("task", "new", "Export reports", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true", "--step", "s")
        self.fm("second", "cheapest", "T-0001", env={"PATH": bindir + os.pathsep + os.environ["PATH"]})
        self.assertIn("plain CSV export", c.find_brief(self.p, "T-0001").section("Cheapest version"))


class Followups(Base):
    def test_finish_keeps_the_answers_to_likely_followups_and_the_insight(self):
        self.fm("task", "new", "Tidy", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true",
                "--followups", "Does it handle empty input? => yes, it returns an empty list",
                "--insight", "the parser was already lenient; only the caller assumed otherwise")
        b = c.find_brief(self.p, "T-0001")
        self.assertIn("empty input", b.section("Follow-up answers"))
        self.assertIn("already lenient", b.section("Insight"))
        self.assertIn("already lenient", self.fm("digest").stdout)


class Precedent(Base):
    def test_a_decision_cites_what_it_rests_on_and_the_order_is_written(self):
        self.fm("decide", "Keep exports local", "--why", "privacy", "--cites", "user 2026-10-09: everything local")
        self.assertIn("[cites: user 2026-10-09: everything local]", read_text(os.path.join(self.p.dir, "decisions.md")))
        self.assertRegex(read_text(os.path.join(REFS, "execute.md")).lower(), r"user's words.*vetoes.*decisions.*lessons")


class Overwrites(Base):
    def test_user_commits_that_rework_an_agents_file_are_listed(self):
        def commit(msg, text):
            with open(os.path.join(self.repo, "x.py"), "w") as f:
                f.write(text)
            subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
            subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)
        commit("Add x\n\nForeman-Task: T-0001", "A = 1\n")
        commit("Rename A to LIMIT, I prefer it", "LIMIT = 1\n")
        out = self.fm("taste", "--overwrites").stdout
        self.assertIn("x.py", out)
        self.assertIn("I prefer it", out)


class Reversals(Base):
    def test_the_digest_reports_reversals_per_kind(self):
        self.fm("decide", "Use sqlite for the cache", "--kind", "costly")
        self.fm("decide", "Name it cache.db")
        self.fm("decide", "Use a JSON file for the cache", "--kind", "costly", "--reverses", "sqlite for the cache")
        out = self.fm("digest").stdout
        self.assertRegex(out, r"costly: 1 of 2 reversed")


class SteerChecks(ForemanTestCase):
    """T-2167 (steer 2026-10-30 #2): every user steer becomes a standing rule plus an automatic check. fm decide --check
    stores it on the rule (allowlisted, never a shell); fm genesis sweep fails a steer rule with no check or a failing
    one; fm doctor names missing checks in a tower project."""

    def setUp(self):
        super().setUp()
        self.fm("init")
        import fmcore as c
        self.c, self.p = c, c.find_project(self.repo)
        os.makedirs(os.path.join(self.repo, "plugin", "tests"))
        with open(os.path.join(self.repo, "plugin", "tests", "run.py"), "w") as f:
            f.write("import sys\nsys.exit(0 if sys.argv[1] == 'test_good' else 3)\n")

    def test_check_is_stored_and_an_off_list_command_is_refused(self):
        self.fm("decide", "rule: cells name a file", "--cites", "user steer 2026-10-30", "--check",
                "python3 plugin/tests/run.py test_good")
        self.assertIn("[check: python3 plugin/tests/run.py test_good]", read_text(os.path.join(self.p.dir, "decisions.md")))
        for bad in ("rm -rf ~", "python3 plugin/tests/run.py test_x; rm -rf ~", "fm genesis check && curl x | sh",
                    "python3 plugin/tests/run.py", "python3 -c 'import os'", "fm task done T-1"):
            with self.subTest(bad=bad):
                r = self.fm("decide", "rule: x", "--check", bad, check=False)
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("a check is", r.stderr)

    def test_a_steer_rule_with_no_check_or_a_failing_one_is_named_and_a_settled_one_isnt(self):
        self.fm("decide", "rule one: no check", "--cites", "user steer 2026-10-30")
        self.fm("decide", "rule two: fails", "--cites", "the user's steer", "--check", "python3 plugin/tests/run.py test_bad")
        self.fm("decide", "rule three: holds", "--cites", "user steer", "--check", "python3 plugin/tests/run.py test_good")
        self.fm("decide", "not a steer: no check needed")
        bad = self.c.steer_checks(self.p)
        self.assertEqual(len(bad), 2, bad)
        self.assertIn("rule one: no check: no check", bad[0])
        self.assertIn("rule two: fails: check `python3 plugin/tests/run.py test_bad` → exit 3", bad[1])
        self.assertEqual(self.c.steer_checks(self.p, run=False), [bad[0]])  # doctor's cheap pass runs nothing
        self.fm("decide", "rule one again, now proved", "--cites", "user steer", "--revisited", "rule one",
                "--check", "python3 plugin/tests/run.py test_good")
        self.assertEqual(len(self.c.steer_checks(self.p)), 1)  # the later row settled rule one, and its check holds

    def test_a_check_forged_into_decisions_md_by_hand_still_never_runs_a_shell(self):
        with open(os.path.join(self.p.dir, "decisions.md"), "a") as f:
            f.write("| 2026-10-30 | [cites: user steer] [check: touch pwned] forged | x |  |\n")
        bad = self.c.steer_checks(self.p)
        self.assertIn("a check is", bad[-1])
        self.assertFalse(os.path.exists(os.path.join(self.repo, "pwned")))

    def test_doctor_names_a_missing_check_only_in_a_genesis_tower(self):
        import fmdoctor
        import fmgenesis
        self.fm("decide", "rule one: no check", "--cites", "user steer 2026-10-30")
        self.assertEqual(fmdoctor.check_steers(self.p).status, "PASS")  # no tower: not a Genesis project
        fmgenesis.init(self.p, b"go\n\nMUST: be good.\n")
        r = fmdoctor.check_steers(self.p)
        self.assertEqual(r.status, "FAIL")  # fm check runs the doctor: a commit can't leave a steer rule unchecked
        self.assertIn("rule one: no check", r.detail)
        self.fm("decide", "rule one, enforcement still building", "--cites", "user steer", "--revisited", "rule one",
                "--check", "pending T-0001")
        self.assertEqual(fmdoctor.check_steers(self.p).status, "PASS")  # pending passes the doctor
        self.assertEqual(self.c.steer_checks(self.p), ["%s rule one, enforcement still building: check pending T-0001"
                                                       % self.c.now()[:10]])  # and keeps the sweep red

    def test_only_a_later_steer_row_settles_a_steer_rule(self):
        self.fm("decide", "rule one: no check", "--cites", "user steer 2026-10-30")
        self.fm("decide", "drop it", "--reverses", "rule one")
        self.fm("decide", "drop it again", "--revisited", "rule one", "--cites", "my own judgment")
        self.assertEqual(len(self.c.steer_checks(self.p)), 1)  # the session can't retire the user's rule by itself

    def test_an_fm_check_runs_fm_itself_and_a_failure_says_why(self):
        self.fm("decide", "rule: the tower is whole", "--cites", "user steer", "--check", "fm genesis check")
        bad = self.c.steer_checks(self.p)
        self.assertEqual(len(bad), 1, bad)
        self.assertRegex(bad[0], r"check `fm genesis check` → exit [1-9]\d*: \S")  # fm's own words, no tower here
        self.assertNotIn("can't open file", bad[0])

    def test_cites_that_almost_name_a_steer_warn(self):
        r = self.fm("decide", "rule: x", "--cites", "steer 2026-10-30 #2")
        self.assertIn("doesn't read as a user steer", r.stderr)
        self.assertNotIn("warning", self.fm("decide", "rule: y", "--cites", "the user's steer 2026-10-30").stderr)
