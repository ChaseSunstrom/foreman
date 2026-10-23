"""T-1662: fm capture refuses a near-duplicate of an open task, naming it (--anyway keeps it), and a FEATURE close to
done work is flagged with that task's id."""
import json
import os

from helpers import ForemanTestCase

import fmcli
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
        self.assertEqual(r.returncode, fmcli.REFUSED_NEAR, "its own code, not a usage error's 1 or a lock's 3")
        self.assertIn("T-0001", r.stderr)
        self.assertIn("add --anyway to keep both, or fm task log T-0001", r.stderr)
        self.assertNotIn("…", r.stderr)
        self.assertIsNone(c.find_brief(self.p, "T-0002"), "a refused capture makes no brief")
        r = self.fm("capture", "export weekly reports as a CSV", "--json", check=False)
        self.assertEqual(r.returncode, fmcli.REFUSED_NEAR)
        self.assertEqual(json.loads(r.stdout), {"refused": "near-duplicate", "of": "T-0001",
                                                "title": "Export the weekly report as CSV"})
        out = self.fm("capture", "export weekly reports as a CSV", "--anyway").stdout
        self.assertIn("T-0002", out)

    def test_a_refused_paste_leaves_no_attachment(self):
        self.fm("capture", "Export the weekly report as CSV")
        r = self.fm("capture", "export weekly reports as a CSV", "--from-file", "-", input="log line\n", check=False)
        self.assertEqual(r.returncode, fmcli.REFUSED_NEAR)
        self.assertFalse(os.path.isdir(os.path.join(self.p.dir, "attachments")), "checked before the paste is kept")

    def test_a_different_type_is_kept_with_a_note(self):
        self.fm("capture", "Export the weekly report as CSV")
        out = self.fm("capture", "export weekly reports as a CSV", "--type", "FIX").stdout
        self.assertIn("T-0002", out)
        self.assertIn("Similar open T-0001", out)

    def test_sibling_module_names_are_not_one_request(self):
        self.fm("capture", "Fix fmcodetui crash on resume", "--type", "FIX")
        self.fm("capture", "Fix fmcode crash on resume", "--type", "FIX")
        self.fm("capture", "fmdoctor repair loses the hooks")
        self.fm("capture", "fmdocs repair loses the hooks")
        self.assertEqual(len(c.load_briefs(self.p)), 4)

    def test_recurring_obstacles_with_different_signatures_are_both_captured(self):
        import fmfixes
        fmfixes._escalate(self.p, "ModuleNotFoundError: No module named 'yaml'")
        fmfixes._escalate(self.p, "ModuleNotFoundError: No module named 'toml'")
        self.assertEqual(len(c.load_briefs(self.p)), 2)

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
