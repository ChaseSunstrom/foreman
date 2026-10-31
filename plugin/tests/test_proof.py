"""fm proof: done tasks whose claims no run here proved (T-2273): typed evidence, inconclusive runs, UI edits unshot."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


class Proof(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def task(self, *files, evidence=()):
        """A done task; evidence: (flags..., cmd, result) tuples handed to fm task evidence; files: its edits."""
        tid = self.fm_json("task", "new", "Do a thing", "--type", "FIX", "--tier", "S", "--ac", "ok :: true",
                           "--step", "s")["id"]
        for ev in evidence:
            self.fm("task", "evidence", tid, *ev)
        for f in files:
            c.log_event(self.p, "touched", task=tid, data={"file": os.path.join(self.repo, f)})
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, tid)
            b.meta["status"] = "done"
            c.save_brief(self.p, b)
        return tid

    def listed(self):
        return {x["id"]: x["kinds"] for x in self.fm_json("proof")["tasks"]}

    def test_typed_inconclusive_and_unshot_ui_are_each_listed(self):
        typed = self.task(evidence=[("--step", "1", "pytest", "9 passed")])
        inc = self.task(evidence=[("--step", "1", "--run", "true", "--inconclusive")])
        ui = self.task("web/app.css", evidence=[("--step", "1", "--run", "true")])
        got = self.listed()
        self.assertEqual(got[typed], ["typed"])
        self.assertEqual(got[inc], ["inconclusive"])
        self.assertEqual(got[ui], ["ui-unshot"])

    def test_a_task_whose_every_check_ran_green_is_never_listed(self):
        ok = self.task("calc.py", evidence=[("--step", "1", "--run", "true")])
        shot = self.task("web/app.css", evidence=[("--step", "1", "--run", "true"),
                                                  ("--step", "1", "--run", "echo fm shot app.css")])
        self.assertNotIn(ok, self.listed())
        self.assertNotIn(shot, self.listed(), "a shot named in the evidence covers the UI change")

    def test_a_later_green_run_supersedes_a_typed_or_inconclusive_line(self):
        t = self.task(evidence=[("--step", "1", "pytest", "ok"), ("--step", "1", "--run", "true")])
        self.assertNotIn(t, self.listed())

    def test_a_warm_status_reads_the_cache_not_the_briefs_or_the_ledger(self):
        from unittest import mock
        t = self.task(evidence=[("--step", "1", "pytest", "ok")])
        tdir = os.path.join(self.p.dir, "tasks")
        src = next(f for f in os.listdir(tdir) if f.startswith(t))
        text = open(os.path.join(tdir, src), encoding="utf-8").read()
        for i in range(500):  # 500 more closed briefs
            n = 900 + i
            with open(os.path.join(tdir, f"T-{n}-x.md"), "w", encoding="utf-8") as f:
                f.write(text.replace(t, f"T-{n}"))
        self.assertIn("unproven: 501", self.fm("status").stdout)  # cold: fills the cache
        with mock.patch.object(c, "ledger_tail", side_effect=AssertionError("ledger read")), \
                mock.patch.object(c, "load_briefs", wraps=c.load_briefs) as lb:
            self.assertGreaterEqual(c.unproven_cached(self.p), 0)
            self.assertEqual(lb.call_count, 0, "a warm call never loads the closed briefs")
        t2 = self.task(evidence=[("--step", "1", "pytest", "ok")])  # a new closed brief changes the key
        self.assertIn(t2, [r["id"] for r in c.unproven(self.p)])
        self.assertEqual(self.fm_json("status", "--json")["unproven"], c.unproven_cached(self.p))

    def test_the_window_bounds_the_list_and_the_count_is_on_status_and_digest(self):
        t = self.task(evidence=[("--step", "1", "pytest", "ok")])
        self.assertEqual(self.fm_json("proof", "--days", "7")["count"], 1)
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, t)
            b.meta["updated"] = "2020-01-01T00:00:00Z"
            c.save_brief(self.p, b, touch=False)
        self.assertEqual(self.fm_json("proof", "--days", "7")["count"], 0)
        self.assertEqual(self.fm_json("proof", "--days", "100000")["count"], 1)
        self.assertEqual(self.fm("proof").stdout.count(t), 0)
        t2 = self.task(evidence=[("--step", "1", "pytest", "ok")])
        self.assertIn("unproven: 1 (fm proof)", self.fm("status").stdout)
        self.assertIn("unproven: 1 (fm proof)", self.fm("digest").stdout)
        self.assertEqual(self.fm_json("status", "--json")["unproven"], 1)
        self.assertIn(t2, self.fm("proof").stdout)
        self.assertEqual(json.loads(self.fm("proof", "--json").stdout)["count"], 1)
