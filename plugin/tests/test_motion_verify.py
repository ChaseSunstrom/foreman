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
        self.assertEqual(self.found("slop.css"), [2, 4, 5, 6])

    def test_transition_animation_or_reduced_motion_is_clean(self):
        self.assertEqual(self.found("crafted.css"), [])


if __name__ == "__main__":
    unittest.main()
