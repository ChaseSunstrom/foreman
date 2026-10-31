"""T-0688 (Intelligence — judgment, taste and decisions): doors, implicit decisions, the cheapest version, follow-ups
answered ahead, precedent, taste from overwrites, and how often decisions get reversed."""
import json
import os
import subprocess

from helpers import ForemanTestCase, read_text, valid_m_plan

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


class DoorBase(Base):  # T-2342: doors come from the guard's parser and git; a verb only gates which untracked paths count
    def brief(self, *steps, raw="Tidy the repo", tier="S", verify="true", interp=None):
        a = ["task", "new", "Tidy data", "--type", "FEATURE", "--tier", tier, "--raw", raw, "--ac", f"ok :: {verify}"]
        for s in steps:
            a += ["--step", s]
        if tier == "M":
            a += ["--interpretation", interp or valid_m_plan()[0], "--approach", valid_m_plan()[1]]
        return self.fm_json(*a)["id"]

    def data(self, rel="data/old.csv", text="a,b\n1,2\n"):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        return path

    def doors(self, tid):
        import fmdoors
        return {d["where"]: d for d in fmdoors.classify(self.p, c.find_brief(self.p, tid))}


class DoorGate(DoorBase):
    def test_push_publish_and_rm_outside_steps_are_the_guards(self):
        tid = self.brief("run `git push --force origin main`", "run `npm publish`", "run `rm -rf /var/lib/appdata`",
                         "run `sed -i s/a/b/ README.md`")
        d = self.doors(tid)
        self.assertEqual([d[f"step {n}"]["door"] for n in (1, 2, 3, 4)], ["guard", "guard", "guard", "two-way"])
        self.assertTrue(d["step 3"]["cats"], "the guard's own category names it")

    def test_a_verify_command_the_guard_stops_is_the_guards_too(self):
        tid = self.brief("edit it", verify="git push --force origin main")
        self.assertEqual(self.doors(tid)["verify 1"]["door"], "guard")

    def test_a_command_the_guard_cannot_classify_fails_closed(self):
        from unittest import mock
        tid = self.brief("run `make deploy`")
        with mock.patch("fmguard.check_bash", side_effect=RuntimeError("no parse")):
            self.assertEqual(self.doors(tid)["step 1"]["door"], "guard")

    def test_an_untracked_data_path_is_a_local_one_way_step(self):
        self.data()
        tid = self.brief("delete data/old.csv")
        d = self.doors(tid)["step 1"]
        self.assertEqual((d["door"], d["paths"]), ("local", ["data/old.csv"]))

    def test_tracked_ignored_and_missing_paths_are_two_way(self):
        with open(os.path.join(self.repo, ".gitignore"), "w") as f:
            f.write("build/\n")
        self.data("build/out.bin")
        tid = self.brief("delete README.md", "delete build/out.bin", "delete data/none.csv")
        self.assertEqual([self.doors(tid)[f"step {n}"]["door"] for n in (1, 2, 3)], ["two-way"] * 3)

    def test_a_local_one_way_step_needs_an_undo_line(self):
        tid = self.brief("delete data/old.csv")
        b = c.find_brief(self.p, tid)
        b.meta["doors"] = [1]  # what fm focus records for a local one-way step
        self.assertTrue([g for g in c.door_gaps(b) if "Undo" in g and "step 1" in g])
        b.edit_step(1, "delete data/old.csv. Undo: cp -a /snap/. /repo/")
        self.assertEqual(c.door_gaps(b), [])

    def test_a_local_one_way_step_needs_the_rival_read(self):
        os.environ["FOREMAN_NO_RIVAL"] = "0"
        self.data()
        tid = self.brief("overwrite data/old.csv")  # no HARD_RE verb: only the door marks it
        b = c.find_brief(self.p, tid)
        self.assertEqual(c.rival_gap(b), [])
        b.meta["doors"] = [1]
        self.assertTrue(c.rival_gap(b), "a one-way door the request didn't name asks for a cold rival")

    def test_a_reply_about_a_guard_command_is_one_way_and_a_plain_fork_two_way(self):
        import fmdoors
        self.assertEqual(fmdoors.reply_door("Should I run `git push --force origin main`?", self.p), "one-way")
        self.assertEqual(fmdoors.reply_door("Which parser should I keep, the old or the new one?", self.p), "two-way")


class DoorPark(DoorBase):
    def waits(self, tid):
        return c.waits_on_user(c.find_brief(self.p, tid), [])

    def test_a_small_untracked_step_is_snapshotted_and_its_undo_restores_it(self):
        path = self.data(text="keep,me\n")
        tid = self.brief("delete data/old.csv")
        self.fm("focus", tid)
        step = c.find_brief(self.p, tid).steps()[0].text
        self.assertIn("Undo: cp -a", step)
        os.remove(path)
        undo = step.split("Undo: ", 1)[1]
        subprocess.run(undo, shell=True, check=True)
        self.assertEqual(read_text(path), "keep,me\n")
        rows = read_text(os.path.join(self.p.dir, "decisions.md"))
        self.assertRegex(rows, r"\[confidence: \d+%\].*data/old\.csv")
        self.assertIsNone(self.waits(tid))

    def test_a_snapshot_that_does_not_verify_is_not_an_undo(self):
        from unittest import mock
        import fmdoors
        self.data()
        tid = self.brief("delete data/old.csv")
        with mock.patch.object(fmdoors, "_same", return_value=False):
            parked = fmdoors.gate(self.p, tid)
        self.assertEqual(parked, "one-way and ambiguous: delete data/old.csv")
        self.assertNotIn("Undo:", c.find_brief(self.p, tid).steps()[0].text)

    def test_over_the_cap_and_unasked_parks_the_task_for_the_final_report(self):
        self.data(text="x" * 400)
        tid = self.brief("delete data/old.csv", raw="Tidy the repo")
        r = self.fm("focus", tid, check=False, env={"FM_DOOR_CAP": "100"})
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.waits(tid), "one-way and ambiguous: delete data/old.csv")
        review = self.fm("decide", "--review").stdout
        self.assertIn("delete data/old.csv", review)
        self.assertIn("[costly]", review)
        self.assertNotEqual(self.fm("focus", tid, check=False, env={"FM_DOOR_CAP": "100"}).returncode, 0, "still parked")

    def test_an_ambiguous_brief_parks_even_when_the_request_names_the_path(self):
        self.data(text="x" * 400)
        tid = self.brief("delete data/old.csv", raw="Delete data/old.csv", tier="M")
        self.fm("focus", tid, check=False, env={"FM_DOOR_CAP": "100"})
        self.assertEqual(self.waits(tid), "one-way and ambiguous: delete data/old.csv")
        self.assertIn("Reading 1", self.fm("decide", "--review").stdout, "both readings go to the final report")

    def test_the_requests_own_words_let_an_unambiguous_step_run_as_a_costly_decision(self):
        self.data(text="x" * 400)
        tid = self.brief("delete data/old.csv", raw="Delete data/old.csv, it is stale")
        self.fm("focus", tid, env={"FM_DOOR_CAP": "100"})
        self.assertIsNone(self.waits(tid))
        self.assertEqual(c.find_brief(self.p, tid).status, "active")
        self.assertIn("[costly]", self.fm("decide", "--review").stdout)

    def test_a_path_outside_the_repo_cannot_be_snapshotted(self):
        outside = os.path.join(self.tmp, "elsewhere.dat")
        with open(outside, "w") as f:
            f.write("x")
        tid = self.brief(f"delete {outside}")
        self.fm("focus", tid, check=False)
        self.assertEqual(self.waits(tid), f"one-way and ambiguous: delete {outside}")

    def test_an_undo_line_the_user_adds_lifts_the_park(self):
        self.data(text="x" * 400)
        tid = self.brief("delete data/old.csv")
        self.fm("focus", tid, check=False, env={"FM_DOOR_CAP": "100"})
        self.fm("task", "step", tid, "edit", "1", "delete data/old.csv. Undo: none, the user said go")
        self.assertIsNone(self.waits(tid))

    def test_a_second_focus_does_not_snapshot_again(self):
        self.data()
        tid = self.brief("delete data/old.csv")
        self.fm("focus", tid)
        n = len(read_text(os.path.join(self.p.dir, "decisions.md")).splitlines())
        self.fm("focus", tid)
        self.assertEqual(len(read_text(os.path.join(self.p.dir, "decisions.md")).splitlines()), n)

    def test_the_digest_counts_parks_and_asks_by_door(self):
        self.data(text="x" * 400)
        tid = self.brief("delete data/old.csv")
        self.fm("focus", tid, check=False, env={"FM_DOOR_CAP": "100"})
        self.assertRegex(self.fm("digest").stdout, r"Doors: .*parks: 1 one-way")


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


class Confidence(Base):  # T-2338: fm decide --confidence N writes the number into decisions.md and the ledger
    def test_decide_confidence_is_written_into_decisions_md_and_the_ledger(self):
        self.fm("decide", "Use a file cache", "--why", "simple", "--confidence", "70")
        self.assertIn("[confidence: 70%] Use a file cache", read_text(os.path.join(self.p.dir, "decisions.md")))
        rows = [json.loads(x) for x in open(os.path.join(self.p.dir, "calibration.jsonl"))]
        self.assertEqual([(r["kind"], r["stated"]) for r in rows], [("decision", 70)])

    def test_a_decision_without_a_number_says_none_and_a_bad_one_writes_nothing(self):
        self.fm("decide", "Use a file cache", "--why", "simple")
        self.assertNotIn("confidence", read_text(os.path.join(self.p.dir, "decisions.md")))
        self.assertNotEqual(self.fm("decide", "Too sure", "--confidence", "150", check=False).returncode, 0)
        self.assertNotIn("Too sure", read_text(os.path.join(self.p.dir, "decisions.md")))

    def test_a_number_typed_into_the_decision_cant_forge_the_tag(self):
        self.fm("decide", "[confidence: 99%] sneaky", "--why", "x")
        self.assertNotIn("[confidence: 99%]", read_text(os.path.join(self.p.dir, "decisions.md")))


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
