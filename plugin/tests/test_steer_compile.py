"""T-1063: a steer that recurs is typed (safety, scope, style, wrong approach) and `fm taste compile N` turns it into a rule."""
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

    def test_classify_types_four_fixtures(self):
        import fmideas
        for text, kind in (("never force push", "safety"), ("only touch the pane file", "scope"),
                           ("don't change the naming format", "style"), ("no polling, use events", "wrong approach")):
            self.assertEqual(fmideas.classify(text), kind, text)

    def test_three_force_push_steers_are_a_safety_proposal_and_compile_blocks_it(self):
        self.steer(*FORCE)
        prop = self.fm_json("taste")["proposed"]
        self.assertEqual([x["type"] for x in prop], ["safety"])
        self.fm("taste", "compile", "1")
        rules = self.c.rules(self.p)
        self.assertEqual([(r["on"], r["action"]) for r in rules], [("bash", "block")])
        self.assertIn("safety", rules[0]["why"])
        self.assertTrue(self.c.rule_hits(self.p, "bash", "git push --force origin main"))
        self.assertEqual(self.fm_json("taste")["proposed"], [], "a compiled proposal is gone")
        self.assertNotEqual(self.fm("taste", "compile", "1", check=False).returncode, 0)
        self.assertEqual(len(self.c.rules(self.p)), 1, "nothing left to compile twice")

    def test_a_declined_proposal_does_not_compile(self):
        self.steer(*FORCE)
        self.fm("taste", "decline", "1")
        self.assertNotEqual(self.fm("taste", "compile", "1", check=False).returncode, 0)
        self.assertEqual(self.c.rules(self.p), [])

    def test_a_style_steer_is_a_path_warn(self):
        self.steer("no camelCase names", "don't use camelCase names", "never camelCase for names, format snake")
        self.fm("taste", "compile", "1")
        self.assertEqual([(r["on"], r["action"]) for r in self.c.rules(self.p)], [("path", "warn")])
