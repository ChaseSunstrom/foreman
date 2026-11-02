"""T-2656: a capture that near-duplicates a deferred task of its type wakes that task instead of being refused: the
words are logged on it and it's due back today, so fm next names it; no new task is made."""
import datetime
import json

from helpers import ForemanTestCase

import fmcore as c


class WakeDeferred(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.fm("capture", "Export the weekly report as CSV")
        self.fm("task", "defer", "T-0001", "no user wants it yet", "--until", "2099-01-01")

    def test_a_matching_capture_wakes_the_deferred_task(self):
        r = self.fm("capture", "export weekly reports as a CSV, a customer asked")
        self.assertIn("woke deferred T-0001", r.stdout)
        self.assertIsNone(c.find_brief(self.p, "T-0002"), "no second task")
        b = c.find_brief(self.p, "T-0001")
        self.assertEqual(b.status, "deferred")
        self.assertEqual(b.meta.get("revisit"), datetime.date.today().isoformat())
        self.assertIn("a customer asked", b.section("Log"))
        self.assertIn("T-0001 is due back", self.fm("next").stdout)
        r = self.fm("capture", "export weekly reports as a CSV again", "--json")
        self.assertEqual(json.loads(r.stdout).get("woke"), "T-0001")

    def test_an_open_match_is_still_refused(self):
        self.fm("capture", "Import the monthly ledger from XLSX")
        r = self.fm("capture", "import monthly ledgers from an XLSX", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("near-duplicate of open T-0002", r.stderr)
