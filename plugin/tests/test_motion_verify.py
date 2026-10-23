"""T-1628: the afterglow rule of fm design lint: a state change with no transition reads as a glitch."""
import os
import unittest

from helpers import ForemanTestCase

import fmdesign

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "design", "afterglow")


class Afterglow(ForemanTestCase):
    def found(self, name):
        return [f["line"] for f in fmdesign.lint([os.path.join(FIX, name)]) if f["rule"] == "afterglow"]

    def test_hover_colour_change_with_no_transition_is_flagged(self):
        self.assertEqual(self.found("slop.css"), [2, 4, 5, 6, 9, 11, 13, 14, 15, 17])
        msg = fmdesign.lint([os.path.join(FIX, "slop.css")])[0]["detail"]
        self.assertIn("design-lint: allow afterglow", msg)

    def test_transition_animation_or_reduced_motion_is_clean(self):
        self.assertEqual(self.found("crafted.css"), [])

    def test_a_duration_token_counts_as_a_transition(self):
        # T-1707: the web template times its button with var(--dur-quick), as the lint itself asks; a 0s one still flags
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.css")
            with open(p, "w") as f:
                f.write(".b { transition: transform var(--dur-quick) var(--ease-out); }\n"
                        ".b:hover { transform: translateY(-1px); }\n"
                        ".c { transition: color 0s; }\n.c:hover { color: red; }\n")
            self.assertEqual([x["line"] for x in fmdesign.lint([p]) if x["rule"] == "afterglow"], [4])

    def test_an_ancestor_or_descendant_state_matches_the_element_that_moves(self):
        # T-1707: the looks gallery's false findings; a transition only on a different element still flags
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.css")
            with open(p, "w") as f:
                f.write(".k .mark { transition: background-color 120ms; }\n"
                        ".k .tile:hover .mark { background: red; }\n"
                        ".t button { transition: background-color 120ms; }\n"
                        ".t [aria-pressed=\"true\"] { background: red; }\n"
                        ".x .b { transition: color 120ms; }\n"
                        ".b:hover { color: red; }\n")
            self.assertEqual([x["line"] for x in fmdesign.lint([p]) if x["rule"] == "afterglow"], [6])


if __name__ == "__main__":
    unittest.main()
