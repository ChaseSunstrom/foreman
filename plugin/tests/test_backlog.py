"""T-1662: fm capture refuses a near-duplicate of an open task, naming it (--anyway keeps it), and a FEATURE close to
done work is flagged with that task's id."""
from helpers import ForemanTestCase

import fmcore as c


class Capture(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def done(self, tid):
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, tid)
            b.meta["status"] = "done"
            c.save_brief(self.p, b)

    def test_a_near_duplicate_of_an_open_task_is_refused_with_its_id(self):
        self.fm("capture", "Export the weekly report as CSV")
        r = self.fm("capture", "export weekly reports as a CSV", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("T-0001", r.stderr)
        self.assertIn("--anyway", r.stderr)
        self.assertIsNone(c.find_brief(self.p, "T-0002"), "a refused capture makes no brief")
        out = self.fm("capture", "export weekly reports as a CSV", "--anyway").stdout
        self.assertIn("T-0002", out)

    def test_unrelated_or_differently_scoped_requests_are_kept(self):
        self.fm("capture", "Export the weekly report as CSV", "--scope", "report/csv.py")
        self.fm("capture", "fix the login timeout on slow wifi")
        self.fm("capture", "export the weekly report as CSV", "--scope", "billing/ledger.py")  # other files: kept
        self.fm("capture", "export")  # one shared word is not a duplicate
        self.fm("capture", "Crash in what T-0001 added")
        self.fm("capture", "Crash in what T-0002 added")  # other numbers: other work
        self.assertEqual(len(c.load_briefs(self.p)), 6)

    def test_a_closed_task_is_not_a_duplicate_and_a_close_feature_is_flagged(self):
        self.fm("capture", "Export the weekly report as CSV")
        self.done("T-0001")
        out = self.fm("capture", "export weekly reports as a CSV").stdout
        self.assertIn("T-0002", out)
        self.assertIn("Close to done work: T-0001", out)
        self.assertNotIn("Close to done", self.fm("capture", "export weekly reports as a CSV file", "--type", "FIX",
                                                  "--anyway").stdout, "only a FEATURE is flagged")
        self.assertNotIn("Close to done", self.fm("capture", "fix the login timeout on slow wifi").stdout)
