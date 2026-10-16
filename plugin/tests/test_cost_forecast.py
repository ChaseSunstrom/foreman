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
        self.assertNotIn(t, self.stop_reason(), "the second Stop doesn't push the capped task")
        self.assertNotIn(t, self.stop_reason())
        self.fm("task", "set", t, "cost_cap=250k")  # a changed cap lifts the hold: still hit, said again
        self.assertIn("cost cap", self.stop_reason())

    def test_every_dispatcher_holds_a_capped_task(self):
        # T-1127: only the interactive drive held it; fm run and fm next still dispatched it
        import fmserve
        self.fm("init")
        t = self.task("Current", type_="FEATURE", tier="M")
        self.history(t)
        self.fm("task", "set", t, "cost_cap=200k")
        p = self.project()
        self.assertIsNone(fmserve._next_runnable(p, set(), set()), "fm run's picker skips the capped task")
        self.assertIn("cost cap", self.fm("next").stdout)
        self.fm("task", "set", t, "cost_cap=5M")  # a new cap lifts the hold
        got = fmserve._next_runnable(p, set(), set())
        self.assertEqual(getattr(got, "id", None), t)

    def test_the_brief_readers_show_the_cost_line(self):
        self.fm("init")
        t = self.task("Current", type_="FEATURE", tier="M")
        self.history(t)
        self.assertNotIn("Cost:", self.fm("task", "show", t).stdout, "no cap, no cache: nothing")
        self.fm("task", "set", t, "cost_cap=2M")
        line = [x for x in self.fm("task", "show", t).stdout.splitlines() if x.startswith("Cost:")][0]
        self.assertRegex(line, r"forecast ≈ 100k \(median of 2 FEATURE M, rough\), cap 2\.0M, spent 300k")
        self.assertIn("Cost: forecast", self.fm("focus", t).stdout)
        self.fm("task", "set", t, "cost_cap=")  # T-1083 review / T-1126: empty clears it; readers use the cache
        self.assertNotIn("cost_cap", c.find_brief(self.project(), t).meta)
        self.assertIn("Cost: forecast", self.fm("task", "show", t).stdout)

    def test_the_cache_lives_outside_the_session_snapshots_and_heals(self):
        # review: state/sessions/cost-*.json was read as the newest session snapshot and crowded rate limits out
        self.fm("init")
        t = self.task("Current", type_="FEATURE", tier="M")
        self.history(t)
        self.fm("task", "set", t, "cost_cap=2M")
        self.fm("task", "show", t)
        self.assertFalse([n for n in os.listdir(os.path.join(self.home, "state", "sessions")) if n.startswith("cost-")]
                         if os.path.isdir(os.path.join(self.home, "state", "sessions")) else [])
        cache = os.path.join(self.home, "state", "cache", f"cost-{self.project().slug}.json")
        self.assertTrue(os.path.exists(cache))
        with open(cache, "w") as f:
            f.write("[]")  # the wrong shape: treated as no cache, rewritten
        self.assertIn("spent 300k", self.fm("task", "show", t).stdout)

    def test_turns_go_to_the_task_their_own_session_was_on(self):
        # review: attribution by global time put session A's turns on session B's task
        self.fm("init")
        p = self.project()
        folder = fmcost.transcripts_dir(p.root)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:
            f.write(json.dumps({"ts": self.day(1, 1), "task": "T-0911", "event": "touched", "session_id": "A"}) + "\n")
            f.write(json.dumps({"ts": self.day(1, 2), "task": "T-0912", "event": "touched", "session_id": "B"}) + "\n")
        with open(os.path.join(folder, "A.jsonl"), "w") as f:  # A works at 03:00, after B's 02:00 event
            f.write(json.dumps({"type": "assistant", "timestamp": self.day(1, 3), "sessionId": "A",
                                "message": {"id": "a1", "usage": {"input_tokens": 50000}, "content": []}}) + "\n")
        costs = fmcost.task_costs(p, 7)
        self.assertEqual(costs.get("T-0911"), 50000)
        self.assertFalse(costs.get("T-0912"))

    def test_a_cap_raise_is_on_the_record(self):
        self.fm("init")
        t = self.task("Current", type_="FEATURE", tier="M")
        self.fm("task", "set", t, "cost_cap=200k")
        self.fm("task", "set", t, "cost_cap=2M")
        self.assertIn("cost_cap 200000 → 2000000", c.find_brief(self.project(), t).section("Log"))
        self.assertRegex(self.fm("digest").stdout, rf"Cost caps raised: {t} 200k → 2\.0M")
