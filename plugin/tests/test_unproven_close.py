"""T-2635: a close that fm prove still lists records its unproven kinds: the receipt names them beside the grade, the
brief and its task_done event keep them, and the weekly line doesn't count it as strongly verified."""
import json

from helpers import ForemanTestCase

from sampo import core as c
from sampo import cost


class UnprovenClose(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def close(self, type, *extra):
        tid = json.loads(self.fm("task", "new", "Do a thing", "--type", type, "--tier", "S", "--ac", "ok :: true",
                                 "--step", "s", "--focus", "--json").stdout)["id"]
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        out = self.fm("task", "finish", tid, "--audit", "self", "--lens", "edge: none", *extra).stdout
        return tid, out

    def test_a_close_fm_prove_still_lists_keeps_its_kinds(self):
        tid, out = self.close("PERFORMANCE", "--numbers", "1 s → 0.5 s")
        b = c.find_brief(self.p, tid)
        self.assertEqual(b.meta.get("unproven"), ["perf-typed"])
        self.assertIn("unproven: perf-typed", out)
        done = [e for e in c.ledger_events(self.p, ("task_done",)) if e.get("task") == tid]
        self.assertEqual((done[-1].get("data") or {}).get("unproven"), ["perf-typed"])
        self.assertIn("0 strongly verified", cost.weekly_line(self.p))
        self.assertIn("1 closed unproven", cost.weekly_line(self.p))

    def test_a_close_with_nothing_unproven_stores_nothing(self):
        tid, out = self.close("FEATURE")
        self.assertNotIn("unproven", c.find_brief(self.p, tid).meta)
        self.assertNotIn("unproven:", out)
        self.assertNotIn("unproven", cost.weekly_line(self.p))
