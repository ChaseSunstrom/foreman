"""T-2135: fm mandate stays as it was for a mandate with no items (its words, exit codes and JSON), and fm goal show
prints the same for it, open work or not: the goal ledger only speaks once a goal has items."""
import json
import unittest

from helpers import ForemanTestCase

import fmcore as c


class MandateAsBefore(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def test_a_mandate_with_no_items_prints_exactly_as_before(self):
        r = self.fm("mandate")
        self.assertEqual(r.stdout, 'No mandate. fm mandate set "<request>" --until YYYY-MM-DD sets one.\n')
        r = self.fm("mandate", "set", "Speed up fm check. And the docs too.", "--until", "2099-01-01")
        self.assertEqual(r.stdout, "Mandate set until 2099-01-01: Speed up fm check. And the docs too. (2 clause(s)); "
                                   "fm scout and fm night read it.\n")
        self.fm("task", "new", "open work", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        shown = self.fm("mandate")
        m = c.read_meta(c.find_project(self.repo))["mandate"]
        self.assertEqual(shown.stdout, "Mandate stands (until 2099-01-01): Speed up fm check. And the docs too.\n"
                         + "".join(f"  - {x}\n" for x in m["clauses"]))
        self.assertEqual(shown.returncode, 0)
        goal = self.fm("goal", "show", check=False)
        self.assertEqual((goal.returncode, goal.stdout), (0, shown.stdout))
        self.assertNotIn("items", json.loads(self.fm("mandate", "--json").stdout)["mandate"])
        self.assertEqual(self.fm("mandate", "off").stdout, "Mandate cleared.\n")


if __name__ == "__main__":
    unittest.main()
