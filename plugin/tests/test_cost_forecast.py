"""T-0973: fm cost --forecast says when the 5-hour and weekly windows fill at the current pace."""
import json
import os
import time

from helpers import ForemanTestCase
from test_hooks import HookCase, parse

import fmcore as c
import fmcost


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


class TaskCostCap(HookCase):
    """T-1083: fm cost --task forecasts from finished same-type, same-tier tasks; a cap hit asks for a checkpoint."""

    def day(self, n, hour=0):
        return time.strftime("%Y-%m-%dT", time.gmtime(time.time() - n * 86400)) + f"{hour:02d}:00:00Z"

    def history(self, active):
        p = self.project()
        folder = fmcost.transcripts_dir(p.root)
        os.makedirs(folder, exist_ok=True)
        events, lines = [], []
        for i, (tid, tokens) in enumerate([("T-0901", 100000), ("T-0902", 100000), (active, 300000)]):
            if tid != active:
                c.save_brief(p, c.Brief.parse(f"---\nid: {tid}\ntype: FEATURE\ntier: M\nstatus: done\n---\n# old {tid}\n"))
            events.append({"ts": self.day(3 - i), "task": tid, "event": "touched"})
            lines.append({"type": "assistant", "timestamp": self.day(3 - i, 1), "sessionId": "s",
                          "message": {"id": f"m{i}", "usage": {"input_tokens": tokens}, "content": []}})
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:
            f.writelines(json.dumps(e) + "\n" for e in events)
        with open(os.path.join(folder, "s.jsonl"), "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in lines)

    def setUp(self):
        super().setUp()
        os.environ["CLAUDE_CONFIG_DIR"] = os.path.join(self.tmp, "claude")
        self.addCleanup(os.environ.pop, "CLAUDE_CONFIG_DIR", None)

    def stop_reason(self):
        return (parse(self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Working.",
                                         "session_id": "sess-1"})) or {}).get("reason", "")

    def test_the_forecast_is_the_median_of_finished_same_tier_tasks(self):
        self.fm("init")
        t = self.task("Current", type_="FEATURE", tier="M")
        self.history(t)
        d = self.fm_json("cost", "--task", t)
        self.assertAlmostEqual(d["forecast"], 100000, delta=5000)
        self.assertAlmostEqual(d["spent"], 300000, delta=5000)
        self.assertIn("forecast", self.fm("cost", "--task", t).stdout)

    def test_a_cap_hit_asks_for_a_checkpoint_and_no_cap_changes_nothing(self):
        self.fm("init")
        t = self.task("Current", type_="FEATURE", tier="M")
        self.history(t)
        self.assertNotIn("cost cap", self.stop_reason())
        self.fm("task", "set", t, "cost_cap=200k")
        self.assertIn("cost cap", self.stop_reason())
        self.assertNotIn("cost cap", self.stop_reason(), "said once")
