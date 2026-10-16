#!/usr/bin/env python3
# FEATURE T-1159: fm task finish says what it did not verify: typed-evidence criteria, unchecked claims, waived checks
import json

from helpers import ForemanTestCase


class NotVerified(ForemanTestCase):
    def new(self, *acs):
        self.fm("init")
        args = ["task", "new", "One", "--type", "FEATURE", "--tier", "S", "--step", "a", "--focus"]
        for a in acs:
            args += ["--ac", a]
        self.fm(*args)

    def test_typed_criterion_and_unchecked_claim_are_listed(self):
        self.new("typed by hand", "ran :: true")
        out = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check",
                      "--claim", "unchecked: the docs are right").stdout
        block = out.split("Not verified", 1)[1]
        self.assertIn("criterion 1", block)
        self.assertIn("typed by hand", block)
        self.assertIn("the docs are right", block)
        self.assertNotIn("criterion 2", block)
        self.assertEqual(out.count("typed by hand"), 1, "listed once")
        self.assertNotIn("Check by hand", out)
        self.assertNotIn("Nothing needed from you", out)
        self.assertLess(block.index("the docs are right"), block.index("typed by hand"), "claims first")

    def test_a_skip_that_was_never_used_is_not_reported(self):
        self.new("ran :: true")
        out = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check",
                      "--skip-affected", "slow").stdout
        self.assertNotIn("Not verified", out)

    def test_a_fully_verified_close_prints_none(self):
        self.new("ran :: true")
        out = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check",
                      "--claim", "checked: it works :: true").stdout
        self.assertNotIn("Not verified", out)

    def test_json_carries_the_list(self):
        self.new("typed by hand")
        out = self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check",
                      "--claim", "inferred: it scales", "--json").stdout
        nv = json.loads(out)["check_by_hand"]
        self.assertEqual(len(nv), 2)
        self.assertTrue(any("it scales" in x for x in nv))


if __name__ == "__main__":
    import unittest
    unittest.main()
