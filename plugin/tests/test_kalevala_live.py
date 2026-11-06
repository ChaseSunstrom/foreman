"""Kalevala part 3, criterion 5 (T-3082): planted faults in a real round. A seed line that is off gen-0's rules is caught
by rune.drift and paused by Väinämöinen's act; a planted stall is caught and snapshotted before its restart. The round
runs kalevala.step with a no-op runner (exit 0): no model is called, so this is fast and deterministic."""
import os
import time
from unittest import mock

from helpers import ForemanTestCase


class KalevalaLive(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        path = os.path.join(self.tmp, "gen0.md")
        with open(path, "w") as f:  # a MUST line gives gen-0 a constraint the planted seed line can break
            f.write("root charter\n\nMUST: keep every change tested.\n\n"
                    "## 2. Capabilities\n1. **Bugs.** finds and fixes broken code. Exam: bug.\n")
        self.fm("genesis", "init", "--file", path)
        self.fm("kalevala", "start")
        from sampo import budget
        budget.set_caps(day=5.0)
        budget.RUN["usd"] = 0.0

    def project(self):
        from sampo import core as c
        return c.find_project(self.repo, create=False)

    def in_tower(self, tower, fn):
        from sampo import rune
        rune.set_tower(tower)
        try:
            return fn(rune.home(self.project()))
        finally:
            rune.set_tower(None)

    def noop(self):
        calls = []

        def run(argv, cwd, env):
            calls.append(list(argv))
            return 0
        return run, calls

    def test_an_off_intent_seed_line_is_caught_by_rune_drift_and_paused_in_a_round(self):
        from sampo import kalevala, rune
        p = self.project()

        def plant(home):  # gen-1 of memory: a MUST gen-0 never wrote
            d = os.path.join(home, "gen-1")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "seed.md"), "w") as f:
                f.write("# Seed\n\nMUST: publish every change to the public site.\n")
        self.in_tower("memory", plant)

        verdict = self.in_tower("memory", lambda home: rune.drift(p, 1))
        self.assertEqual(verdict["verdict"], "drifted", verdict)
        self.assertTrue(any("not one of gen-0's" in x for x in verdict["found"]), verdict["found"])
        self.assertTrue(verdict["read"].startswith("skipped"), verdict["read"])  # no paid cold read on a failed check
        self.in_tower("memory", lambda home: rune._log(p, "genesis_drift",
                                                       data={"gen": 1, "verdict": verdict["verdict"]}))

        run, calls = self.noop()
        res = kalevala.step(p, runner=run)
        status = {x["tower"]: x["status"] for x in res["results"]}
        self.assertEqual(status["memory"], "paused", status)
        self.assertFalse(any("memory" in " ".join(a) for a in calls), calls)
        act = [a for a in kalevala.acts(p) if a["act"] == "pause" and a["tower"] == "memory"]
        self.assertEqual(len(act), 1, act)
        self.assertIn("drift", act[0]["reason"])
        self.assertIn(f"fm kalevala resume", act[0]["undo"])

    def test_a_planted_stall_is_snapshotted_before_its_restart_in_a_real_round(self):
        from sampo import kalevala
        p = self.project()

        def plant(home):  # gen-1 of memory last written 30 hours ago: past the 24-hour window
            d = os.path.join(home, "gen-1")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "seed.md"), "w") as f:
                f.write("# Seed\n")
            old = time.time() - 30 * 3600
            os.utime(d, (old, old))
        self.in_tower("memory", plant)

        run, _ = self.noop()
        kalevala.step(p, runner=run)
        act = [a for a in kalevala.acts(p) if a["act"] == "restart" and a["tower"] == "memory"]
        self.assertEqual(len(act), 1, act)
        self.assertTrue(os.path.isfile(os.path.join(act[0]["snapshot"], "gen-1", "seed.md")))
        self.assertIn(act[0]["snapshot"], act[0]["undo"])
