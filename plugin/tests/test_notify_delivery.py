"""T-2684: _notify records each delivery's result; fm doctor warns after three failures in a row."""
from helpers import ForemanTestCase

import fmcore as c
import fmdoctor
import fmserve


class NotifyDeliveryCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def test_three_failures_warn_and_a_success_resets(self):
        self.assertIn("no notify command", fmdoctor.check_notify([self.p]).detail)
        self.fm("notify", "exit 1")
        for _ in range(2):
            fmserve._notify(self.p, "x")
        self.assertEqual(fmdoctor.check_notify([self.p]).status, "PASS")
        fmserve._notify(self.p, "x")
        r = fmdoctor.check_notify([self.p])
        self.assertEqual(r.status, "WARN")
        self.assertIn("exit 1", r.detail)
        self.assertEqual(c.read_meta(self.p)["notify_result"]["fails"], 3)
        self.fm("notify", "true")
        fmserve._notify(self.p, "x")
        self.assertEqual(c.read_meta(self.p)["notify_result"]["fails"], 0)
        self.assertEqual(fmdoctor.check_notify([self.p]).status, "PASS")
