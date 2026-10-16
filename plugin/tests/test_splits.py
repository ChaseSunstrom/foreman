"""T-1078: speedrun splits: the active task's time in each stage against this project's typical time for its type and
tier (median over closed tasks, 3+ samples), carried in fm ui --json active.splits."""
import json
import os
import time

from helpers import ForemanTestCase


def ts(ago_min):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - ago_min * 60))


class Splits(ForemanTestCase):
    def test_stage_times_against_typical(self):
        import fmcore as c
        self.fm("init")
        tid = "T-0001"
        self.fm("task", "new", "slow one", "--type", "FIX", "--tier", "M", "--interpretation", "x", "--approach", "x",
                "--ac", "x :: true", "--step", "s", "--focus")
        p = c.find_project(self.repo)
        rows = []
        for i in range(3):  # closed FIX/M: planning 5, executing 20, verifying 5 (two of them have that stage)
            t, base = f"T-09{i}", 1000 + i * 100
            rows += [{"ts": ts(base), "event": "task_new", "task": t, "data": {"type": "FIX", "tier": "M"}},
                     {"ts": ts(base - 5), "event": "task_plan", "task": t}]
            if i < 2:
                rows.append({"ts": ts(base - 25), "event": "ac_check", "task": t})
            rows.append({"ts": ts(base - (30 if i < 2 else 25)), "event": "task_done", "task": t})
        rows += [{"ts": ts(180), "event": "task_new", "task": tid, "data": {"type": "FIX", "tier": "M"}},
                 {"ts": ts(175), "event": "task_plan", "task": tid},
                 {"ts": ts(5), "event": "ac_check", "task": tid}]  # executing took 170 min, verifying runs 5
        led = os.path.join(p.dir, "ledger.jsonl")
        with open(led) as f:  # an older task: no stage events, so the proxies apply
            keep = [x for x in f if '"event": "stage"' not in x and '"event":"stage"' not in x]
        with open(led, "w") as f:
            f.writelines(keep + [json.dumps(r) + "\n" for r in rows])
        sp = {s["stage"]: s for s in json.loads(self.fm("ui", "--json").stdout)["active"]["splits"]}
        self.assertGreater(sp["executing"]["delta"], 0)
        self.assertEqual(sp["executing"]["sign"], "over")
        self.assertEqual(sp["executing"]["typical"], 20 * 60)
        self.assertIsNone(sp["verifying"]["typical"], "two samples are too few")
        self.assertIsNone(sp["verifying"]["sign"])

    def test_stage_events_logged_once_per_transition(self):
        import fmcore as c
        self.fm("init")
        self.fm("task", "new", "t", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        self.fm("task", "log", "T-0001", "noise")  # no stage move: no event
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "true", "ok")  # executing -> verifying
        self.fm("task", "log", "T-0001", "more noise")
        p = c.find_project(self.repo)
        evs = [json.loads(x) for x in open(os.path.join(p.dir, "ledger.jsonl"))]
        st = [(e["data"]["from"], e["data"]["to"]) for e in evs if e["event"] == "stage" and e["task"] == "T-0001"]
        self.assertEqual(st[-1], ("executing", "verifying"))
        self.assertEqual(len(st), len(set(st)), "one event per transition")

    def test_splits_prefer_stage_events(self):
        import fmwatch
        evs = [{"ts": ts(100), "event": "task_new", "task": "T-1"},
               {"ts": ts(90), "event": "stage", "task": "T-1", "data": {"from": "planning", "to": "executing"}},
               {"ts": ts(30), "event": "stage", "task": "T-1", "data": {"from": "executing", "to": "verifying"}},
               {"ts": ts(10), "event": "task_plan", "task": "T-1"}]  # a proxy that would say otherwise
        import fmcore as c
        got = fmwatch._stage_secs(evs, c.parse_ts(ts(0)))
        self.assertAlmostEqual(got["executing"], 60 * 60, delta=2)
        self.assertAlmostEqual(got["verifying"], 30 * 60, delta=2)
        self.assertNotIn("planning", got)
