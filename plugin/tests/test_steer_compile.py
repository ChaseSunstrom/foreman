"""T-1063: a steer that recurs is typed (safety, scope, style, wrong approach) and `fm taste compile N` turns it into a
warn rule; a block is `--block`, the user's alone."""
import os
import sys

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

# not "never": said as a rule, one such steer is already a proposal alone
FORCE = ("no force push to main", "no force push, ever", "don't force push my branches")


class SteerCompile(ForemanTestCase):
    def setUp(self):
        import fmcore as c
        super().setUp()
        self.fm("init")
        self.c, self.p = c, c.find_project(self.repo)

    def steer(self, *texts):
        for t in texts:
            self.c.log_event(self.p, "note", data={"text": "steer: " + t})

    def hit(self, on, text):
        return bool(self.c.rule_hits(self.p, on, text))

    def test_classify_by_whole_words_on_the_shape(self):
        import fmideas
        for text, kind in (("force push", "safety"), ("only pane", "scope"), ("naming format", "style"),
                           ("polling events", "wrong approach"), ("in that case", "wrong approach"),
                           ("filename justify", "wrong approach"), ("forced", "wrong approach")):
            self.assertEqual(fmideas.classify(text), kind, text)

    def test_force_push_steers_are_a_safety_proposal_and_compile_adds_a_warn_rule(self):
        self.steer(*FORCE)
        self.assertEqual([x["type"] for x in self.fm_json("taste")["proposed"]], ["safety"])
        out = self.fm("taste", "compile", "1").stdout
        self.assertIn("warn rule 1 added (fm rule rm 1 is yours to run)", out)
        self.assertEqual([(r["on"], r["action"]) for r in self.c.rules(self.p)], [("bash", "warn")])
        self.assertIn("safety", self.c.rules(self.p)[0]["why"])
        self.assertTrue(self.hit("bash", "git push --force origin main"))
        self.assertFalse(self.hit("bash", 'git commit -m "push the fix"'))
        self.assertFalse(self.hit("bash", "pushd x"))
        self.assertEqual(self.fm_json("taste")["proposed"], [], "a compiled proposal is gone")
        self.assertNotEqual(self.fm("taste", "compile", "1", check=False).returncode, 0)
        self.assertEqual(len(self.c.rules(self.p)), 1)

    def test_bare_compile_needs_a_number(self):
        self.steer(*FORCE)
        self.assertNotEqual(self.fm("taste", "compile", check=False).returncode, 0)
        self.assertEqual(self.c.rules(self.p), [])

    def test_block_is_a_flag_and_the_agent_cannot_pass_it(self):
        self.steer(*FORCE)
        self.fm("taste", "compile", "1", "--block")  # the CLI takes it (the guard stops the agent, not the CLI)
        self.assertEqual([r["action"] for r in self.c.rules(self.p)], ["block"])

    def test_one_shape_word_does_not_compile(self):
        self.steer("no mocks", "don't use mocks", "avoid mocks in tests")
        self.assertEqual([x["words"] for x in self.fm_json("taste")["proposed"]][0][:1], ["mocks"])
        self.assertNotEqual(self.fm("taste", "compile", "1", check=False).returncode, 0)
        self.assertEqual(self.c.rules(self.p), [])

    def test_a_declined_proposal_does_not_compile(self):
        self.steer(*FORCE)
        self.fm("taste", "decline", "1")
        self.assertNotEqual(self.fm("taste", "compile", "1", check=False).returncode, 0)
        self.assertEqual(self.c.rules(self.p), [])

    def test_a_style_steer_is_a_bash_warn_that_matches_its_command(self):
        self.steer("no camelCase names", "don't use camelCase names", "never camelCase for names, format snake")
        self.fm("taste", "compile", "1")
        self.assertEqual([(r["on"], r["action"]) for r in self.c.rules(self.p)], [("bash", "warn")])
        self.assertTrue(self.hit("bash", "sed -i s/names/camelCase names/ a.py"))

    def test_an_unrelated_rule_sharing_a_word_does_not_hide_a_proposal(self):
        self.c.add_rule(self.p, r"(?i)\bforce\b", "bash", "warn", "other")
        self.steer(*FORCE)
        self.assertEqual(len(self.fm_json("taste")["proposed"]), 1)
