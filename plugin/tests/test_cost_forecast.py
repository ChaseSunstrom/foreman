"""T-0973: fm cost --forecast says when the 5-hour and weekly windows fill at the current pace."""
import json
import os
import time

from helpers import ForemanTestCase

import fmcore as c


class CostForecast(ForemanTestCase):
    def snapshot(self, five, five_left_h, week, week_left_d):
        d = os.path.join(c.state_dir(), "sessions")
        os.makedirs(d, exist_ok=True)
        now = time.time()
        with open(os.path.join(d, "s1.json"), "w") as f:
            json.dump({"rate_limits": {
                "five_hour": {"used_percentage": five, "resets_at": now + five_left_h * 3600},
                "seven_day": {"used_percentage": week, "resets_at": now + week_left_d * 86400}}}, f)

    def test_a_window_on_pace_to_fill_says_when(self):
        self.fm("init")
        self.snapshot(60, 2, 30, 3.5)  # 60% in 3 of 5 h: full in 2 h at that pace (exactly at reset); week on pace 60%
        d = json.loads(self.fm("cost", "--forecast", "--json").stdout)
        five = d["windows"]["five_hour"]
        self.assertEqual(five["used"], 60)
        self.assertAlmostEqual(five["projected"], 100, delta=1)
        week = d["windows"]["seven_day"]
        self.assertAlmostEqual(week["projected"], 60, delta=1)
        self.assertIsNone(week["full_at"])  # won't fill before it resets
        self.snapshot(80, 3, 30, 3.5)  # 80% in 2 h: full in 30 min, long before the reset
        d = json.loads(self.fm("cost", "--forecast", "--json").stdout)
        self.assertLess(d["windows"]["five_hour"]["full_at"] - time.time(), 40 * 60)
        out = self.fm("cost", "--forecast").stdout
        self.assertIn("5-hour", out)
        self.assertIn("fills", out)

    def test_no_snapshot_says_so(self):
        self.fm("init")
        self.assertIn("no usage snapshot", self.fm("cost", "--forecast").stdout)
