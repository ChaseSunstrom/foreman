"""T-1059: a self-change is a pre-registered trial: the metric it should move and by when; the digest grades it."""
import datetime
from unittest import mock

from helpers import ForemanTestCase

import fmcore as c
import fmtrials as tr


def ago(days):
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


class Trials(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def events(self, per_day_before, per_day_after, age=10):
        """Corrections over the `age` days before the trial's registration and the `age` days after."""
        for d in range(1, 2 * age + 1):
            n = per_day_before if d > age else per_day_after
            for _ in range(n):
                with mock.patch.object(c, "now", lambda d=d: ago(d - 0.5)):
                    c.log_event(self.p, "correction", data={"text": "no"})

    def register(self, age=10, by=10):
        with mock.patch.object(c, "now", lambda: ago(age)):
            tr.add(self.p, "rule X", "corrections", by)

    def test_unchanged_rate_proposes_revert_and_halved_moved(self):
        self.events(5, 5)
        self.register()
        self.assertIn("no movement: propose revert", tr.lines(self.p)[-1])
        self.setUp()
        self.events(6, 3)
        self.register()
        self.assertIn("moved", tr.lines(self.p)[-1])
        self.assertNotIn("revert", tr.lines(self.p)[-1])

    def test_pending_before_due(self):
        self.register(age=4, by=10)
        self.assertIn("pending, 6 days left", tr.lines(self.p)[-1])

    def test_rule_add_with_moves_writes_a_trial_the_digest_prints(self):
        self.fm("rule", "add", "rm -rf", "--why", "no", "--moves", "corrections", "--by", "30")
        out = self.fm("digest").stdout
        self.assertIn("rule add rm -rf", out)
        self.assertIn("pending, 30 days left", out)

    def test_no_moves_records_nothing(self):
        self.fm("rule", "add", "rm -rf", "--why", "no")
        self.assertEqual(tr.load(self.p), [])
        self.assertNotIn("Trials", self.fm("digest").stdout)
