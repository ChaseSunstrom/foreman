"""T-2645: FOREMAN_NOW pins c.clock(), so a window's edge can be tested exactly: a close at a window's end counts as
finished, one a second before does not (fm outcomes' survival window, fm digest's weekly window)."""
import datetime
import json
import re
import subprocess
import sys
import os
import unittest
from unittest import mock

from helpers import ForemanTestCase

import fmcore as c

T0 = datetime.datetime(2026, 9, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
LIB = os.path.dirname(c.__file__)


def at(days, seconds=0):
    return (T0 + datetime.timedelta(days=days, seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


class ClockWindows(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Add thing", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus",
                env={"FOREMAN_NOW": at(0)})
        self.tid = c.load_briefs(c.find_project(self.repo))[-1].id
        self.fm("task", "finish", self.tid, "--audit", "self", "--run", "true", env={"FOREMAN_NOW": at(0)})

    def outcome(self, now):
        return json.loads(self.fm("outcomes", "--json", env={"FOREMAN_NOW": now}).stdout)

    def test_survival_window_ends_exactly_at_thirty_days(self):
        def row(now):
            return self.outcome(now)["tasks"][self.tid]
        self.assertIs(row(at(30))["window_done"], True)
        self.assertEqual(row(at(30))["survival"], "survived")
        self.assertIs(row(at(30, -1))["window_done"], False)
        self.assertEqual(row(at(30, -1))["survival"], "settling")

    def test_digest_week_includes_a_close_exactly_seven_days_old_not_one_a_second_older(self):
        def seen(now):
            return self.tid in self.fm("digest", "--days", "7", env={"FOREMAN_NOW": now}).stdout
        self.assertTrue(seen(at(7)))
        self.assertFalse(seen(at(7, 1)))

    def test_clock_reads_and_ignores_a_bad_value(self):
        def run(v):
            e = dict(os.environ, PYTHONPATH=LIB, FOREMAN_NOW=v)
            return subprocess.run([sys.executable, "-c", "import fmcore as c;print(c.clock().isoformat(), c.now())"],
                                  env=e, capture_output=True, text=True, cwd=self.tmp).stdout
        self.assertEqual(run("2026-09-01T12:00:00Z"), "2026-09-01T12:00:00+00:00 2026-09-01T12:00:00Z\n")
        self.assertEqual(run("2026-09-01T14:00:00+02:00"), "2026-09-01T12:00:00+00:00 2026-09-01T12:00:00Z\n")
        self.assertRegex(run("junk"), r"^20\d\d-")  # malformed: the real clock, no crash

    def test_no_raw_datetime_now_in_the_windowed_readers(self):
        for mod in ("fmoutcomes.py", "fmcost.py"):
            with open(os.path.join(LIB, mod), encoding="utf-8") as f:
                self.assertNotRegex(f.read(), r"datetime\.now\(")


class PinnedClockDoctor(unittest.TestCase):
    """T-2645 review: FOREMAN_NOW left set outside a test pins every timestamp; fm doctor says so."""

    def test_doctor_warns_while_the_clock_is_pinned(self):
        import fmdoctor
        with mock.patch.dict(os.environ, {"FOREMAN_NOW": "2026-01-01T00:00:00Z"}):
            self.assertEqual(fmdoctor.check_pinned_clock().status, "WARN")
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("FOREMAN_NOW", None)
            self.assertEqual(fmdoctor.check_pinned_clock().status, "PASS")
