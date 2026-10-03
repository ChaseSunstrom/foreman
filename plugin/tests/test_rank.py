"""T-0111: the inbox is ranked by value for effort inside the intake type order: urgent first, then type, then (who asked,
how many items wait on it, how long it waited) per tier; an item never comes before a captured item it depends on."""
import json
import unittest

from helpers import ForemanTestCase


class RankInbox(ForemanTestCase):
    def test_value_for_effort_within_the_type_order(self):
        self.fm("init")
        cap = lambda title, typ, tier, source="user", *extra: self.fm("capture", title, "--type", typ, "--tier", tier,
                                                                        "--source", source, *extra)
        cap("big user feature", "FEATURE", "L")                       # T-0001: 3 / 4
        cap("small followup", "FEATURE", "S", "followup")             # T-0002: 1 / 1
        cap("medium user feature", "FEATURE", "M")                    # T-0003: 3 / 2, and T-0004 waits on it
        cap("small user feature", "FEATURE", "S", "user")             # T-0004: 3 / 1, after T-0003
        self.fm("task", "set", "T-0004", "depends_on=T-0003")
        cap("a large fix", "FIX", "L")                                # T-0005: FIX before FEATURE
        inbox = [q["id"] for q in json.loads(self.fm("state", "--json").stdout)["inbox"]]
        self.assertEqual(inbox, ["T-0005", "T-0003", "T-0004", "T-0002", "T-0001"])
        self.assertIn("T-0005", self.fm("next").stdout)


if __name__ == "__main__":
    unittest.main()
