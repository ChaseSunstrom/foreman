"""T-0112: a taste profile from what the user kept, dropped, steered and corrected: fm taste shows it with its evidence,
and a brainstorm pack carries the same lines so ideas lean toward what they accept."""
import json
import os
import sys
import unittest

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))


class Taste(ForemanTestCase):
    def test_kept_dropped_and_steered_work_make_the_profile_and_reach_the_pack(self):
        import fmcore as c
        import fmideas
        self.fm("init")
        self.fm("capture", "Animated band", "--type", "FEATURE", "--tier", "M")
        self.fm("capture", "Telemetry upload", "--type", "FEATURE", "--tier", "M")
        self.fm("task", "drop", "T-0002", "no network calls, keep it local")
        self.fm("task", "new", "Quiet output", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                "--focus")
        self.fm("task", "log", "T-0003", "steer: spell out codes, no jargon")
        self.fm("task", "finish", "T-0003", "--run", "true", "--audit", "self check")
        out = self.fm("taste").stdout
        for needle in ("no network calls, keep it local", "spell out codes, no jargon", "Quiet output"):
            self.assertIn(needle, out)
        data = json.loads(self.fm("taste", "--json").stdout)
        self.assertTrue(data["dropped"] and data["steered"] and data["kept"])
        pack = fmideas.user_voice(c.find_project(self.repo))
        self.assertIn("dropped: Telemetry upload — no network calls, keep it local", pack)
        self.assertIn("steered: spell out codes, no jargon", pack)


class CorrectionClusters(ForemanTestCase):
    """T-1042: a correction met twice, in similar words, is proposed as a ready fm rule add line."""
    def setUp(self):
        import fmcore as c
        super().setUp()
        self.fm("init")
        self.c, self.p = c, c.find_project(self.repo)

    def correct(self, *texts):
        for t in texts:
            self.c.log_event(self.p, "correction", data={"text": t})

    def corrections(self):
        return self.fm_json("taste")["corrections"]

    def test_two_similar_corrections_propose_a_ready_rule_and_one_does_not(self):
        import shlex
        self.correct("no, don't use mocks in db tests")
        self.assertEqual(self.corrections(), [], "one correction is not a pattern")
        self.correct("stop mocking the database")
        got = self.corrections()
        self.assertEqual([(x["words"], x["count"]) for x in got], [(["mock"], 2)])
        self.assertIn("fm rule add", got[0]["suggest"])
        self.assertIn("Corrections met twice", self.fm("taste").stdout)
        self.fm(*shlex.split(got[0]["suggest"])[1:])  # the line runs as given
        self.assertEqual(self.corrections(), [], "a rule that covers it ends the proposal")

    def test_a_veto_or_a_decline_suppresses_it(self):
        self.correct("no, don't use mocks in db tests", "stop mocking the database")
        self.c.add_veto(self.p, "never use mocks")
        self.assertEqual(self.corrections(), [], "a recorded veto covers it")
        self.correct("never touch the lockfile", "don't edit the lockfile by hand")
        self.assertEqual([x["words"] for x in self.corrections()], [["lockfile"]])
        self.fm("taste", "decline", "1")
        self.assertEqual(self.corrections(), [], "a declined cluster isn't proposed again")

    def test_one_shared_common_word_is_not_a_cluster(self):
        for i in range(20):
            self.c.log_event(self.p, "prompt", data={"text": f"run the tests for part {i}"})
        self.correct("no, the tests are flaky", "wrong, those tests time out")
        self.assertEqual(self.corrections(), [], "a word the user says all the time isn't a shared correction")

    def test_a_common_word_drops_out_of_a_wider_cluster(self):
        for i in range(20):
            self.c.log_event(self.p, "prompt", data={"text": f"run the tests for part {i}"})
        self.correct("no, the tests are flaky", "wrong, those flaky tests")
        self.assertEqual([x["words"] for x in self.corrections()], [["flaky"]])

    def test_shared_filler_words_are_not_a_cluster(self):
        self.correct("no, I already said it would break because you didn't wait",
                     "wrong, I think it would fail because you already didn't check")
        self.assertEqual(self.corrections(), [])

    def test_bare_adopt_and_decline_leave_corrections_alone(self):
        self.correct("no, don't use mocks in db tests", "stop mocking the database")
        for action in ("adopt", "decline"):
            self.assertNotEqual(self.fm("taste", action, check=False).returncode, 0, f"a bare {action} is steers only")
        self.assertEqual(self.c.vetoes(self.p), [])
        self.assertEqual(len(self.corrections()), 1)
        self.fm("taste", "adopt", "1")  # an explicit N takes it
        self.assertEqual([v["words"] for v in self.c.vetoes(self.p)], [["mock"]])
        self.assertEqual(self.corrections(), [])

    def test_es_plurals_stem_so_the_rule_matches_the_command(self):
        import re
        import shlex
        self.correct("stop deleting branches", "no, leave my branches alone")
        got = self.corrections()
        self.assertEqual([x["words"] for x in got], [["branch"]])
        self.assertTrue(re.search(shlex.split(got[0]["suggest"])[3], "git branch -D x"))
        meta = self.c.read_meta(self.p)
        meta["taste_declined"] = [["branches"]]  # a steer proposal's decline keeps its words unstemmed
        self.c.write_meta(self.p, meta)
        self.assertEqual(self.corrections(), [], "a decline matches on stems")

    def test_the_prompt_hook_feeds_it_and_its_own_vetoes_do_not_hide_it(self):
        for text in ("no, don't use mocks in db tests", "stop mocking the database"):
            self.hook("UserPromptSubmit", {"prompt": text})
        self.assertEqual(len(self.c.vetoes(self.p)), 2, "each correction records its veto")
        self.assertEqual([(x["words"], x["count"]) for x in self.corrections()], [(["mock"], 2)])


if __name__ == "__main__":
    unittest.main()
