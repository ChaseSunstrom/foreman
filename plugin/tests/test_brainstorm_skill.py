"""T-2659: the brainstorm skill's grounding step holds a grounding pass to what found built work it missed: three of four
slate items brainstorm-20261102's pass marked new or partial were already built (fm task prove --hunks, survival by
close grade, decision --sunset)."""
import os
import unittest

SKILL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills", "brainstorm", "SKILL.md")


class Grounding(unittest.TestCase):
    def test_step_4_names_master_three_phrasings_help_strings_and_a_spot_check(self):
        with open(SKILL, encoding="utf-8") as f:
            step = f.read().split("4. **Merge, cluster, ground", 1)[1].split("\n5. ", 1)[0]
        for want in ("MASTER.md", "three phrasings", "help strings", "spot-check"):
            self.assertIn(want, step)


if __name__ == "__main__":
    unittest.main()
