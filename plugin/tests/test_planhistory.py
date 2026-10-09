"""T-0692 (Intelligence — planning and decomposition 2): steps a plan forgot come back for the next similar plan, and
steps can name what they require and produce, linted at focus."""
import os

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)


class History(Base):
    def test_steps_added_late_are_kept_and_offered_to_the_next_similar_plan(self):
        self.fm("task", "new", "Add CSV export to the reports page", "--type", "FEATURE", "--tier", "S",
                "--ac", "ok :: true", "--step", "Write the exporter", "--focus")
        self.fm("task", "step", "T-0001", "add", "Escape commas inside quoted cells")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true")
        self.assertIn("Escape commas inside quoted cells", c.find_brief(self.p, "T-0001").section("Plan gaps"))
        self.fm("task", "new", "Add CSV export to the invoices page", "--type", "FEATURE", "--tier", "S",
                "--ac", "ok :: true", "--step", "Write the exporter")
        out = self.fm("focus", "T-0002").stdout
        self.assertRegex(out, r"steps similar plans added late.*Escape commas inside quoted cells \(T-0001\)")


class Contracts(Base):
    def test_focus_lints_produced_paths_that_exist_and_required_ones_nothing_makes(self):
        os.makedirs(os.path.join(self.repo, "lib"))
        with open(os.path.join(self.repo, "lib", "parser.py"), "w") as f:
            f.write("X = 1\n")
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "Write the parser (produces: lib/parser.py)",
                "--step", "Write the lexer (produces: lib/lexer.py)",
                "--step", "Wire both up (requires: lib/lexer.py, lib/config.py)")
        out = self.fm("focus", "T-0001").stdout
        self.assertRegex(out, r"step 1 produces lib/parser\.py, which already exists")
        self.assertRegex(out, r"step 3 requires lib/config\.py")
        self.assertNotRegex(out, r"requires lib/lexer\.py")
