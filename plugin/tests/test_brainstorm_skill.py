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

    def test_step_3_names_the_grid_lens_for_exhaustive_requests(self):  # T-2672
        with open(SKILL, encoding="utf-8") as f:
            step = f.read().split("3. **Fan out", 1)[1].split("\n4. ", 1)[0]
        self.assertIn("--lens grid", step)



class Canary(unittest.TestCase):
    """T-2674: an empty search proves absence only if the same search finds something known to be there."""

    def test_step_4_runs_a_canary_before_any_not_found(self):
        with open(SKILL, encoding="utf-8") as f:
            step = f.read().split("4. **Merge, cluster, ground", 1)[1].split("\n5. ", 1)[0]
        self.assertIn("canary", step)
        self.assertIn("same tool and scope", step)
        self.assertIn("canary:", step)  # the verdict records it, so a catalogue can count the "new" verdicts that carry one



if __name__ == "__main__":
    unittest.main()
