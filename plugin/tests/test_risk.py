"""T-1080: one daily risk budget (destructive guard blocks, failed closes, reverts) that steps autonomy down a notch."""
import json
import os
import subprocess
import time

from test_hooks import HookCase

import fmbudget
import fmcore as c


class Risk(HookCase):
    def spend(self, blocks=0, failed=0, routine=0):
        p = self.project()
        for _ in range(blocks):
            c.log_event(p, "guard_block", data={"category": "rm-outside"})
        for _ in range(routine):
            c.log_event(p, "guard_block", data={"category": "core"})  # routine: never counts
        for _ in range(failed):
            c.log_event(p, "close_affected", task="T-0001", data={"exit": 1})
        c.log_event(p, "close_affected", task="T-0001", data={"exit": 0})  # a green close costs nothing
        return p

    def test_points_cap_and_slowed(self):
        self.fm("init")
        self.spend(blocks=3, failed=1, routine=5)
        d = self.fm_json("risk")
        self.assertEqual(d["spent"], 5)
        self.assertFalse(d["slowed"])
        self.fm("risk", "set", "--day", "4", "--because", "a tight day")
        d = self.fm_json("risk")
        self.assertEqual((d["cap"], d["slowed"]), (4, True))
        self.assertIn("slowed", self.fm("risk").stdout)
        self.assertIn("a tight day", json.dumps(c.ledger_tail(self.project(), 5)))

    def test_past_the_cap_autonomy_steps_down_a_notch_and_degrade_says_why(self):
        self.fm("init")
        p = self.spend(blocks=2)
        self.fm("risk", "set", "--day", "2", "--because", "test")
        self.fm("autonomy", "full")
        self.assertEqual(c.effective_autonomy(p), "standard")
        self.assertIn("risk", fmbudget.degrade(p) or "")
        self.fm("autonomy", "standard")
        self.assertEqual(c.effective_autonomy(p), "slow")
        self.fm("risk", "set", "--day", "50", "--because", "test")
        self.assertEqual(c.effective_autonomy(p), "standard")
        self.assertIsNone(fmbudget.degrade(p))

    def test_every_reader_of_autonomy_sees_the_step_down(self):
        # review: fm decide --ask read the stored autonomy and self-decided under a spent budget; fm autonomy blamed plans
        self.fm("init")
        self.fm("autonomy", "full")
        self.spend(blocks=2)
        self.fm("risk", "set", "--day", "2", "--because", "test")
        d = self.fm_json("autonomy")
        self.assertEqual((d["autonomy"], d["effective"]), ("full", "standard"))
        self.assertIn("risk budget", self.fm("autonomy").stdout)
        self.fm("decide", "--ask", "Ship it?", "--default", "yes", check=False)
        self.assertIn("ask_queued", [e.get("event") for e in c.ledger_tail(self.project(), 10)], "asked, not self-decided")

    def test_fm_next_says_why_autonomy_slowed(self):
        self.fm("init")
        self.task("Current", type_="FEATURE", tier="M")
        self.spend(blocks=2)
        self.fm("risk", "set", "--day", "2", "--because", "test")
        self.assertIn("risk budget", self.fm("next").stdout)

    def test_yesterday_is_not_today(self):
        self.fm("init")
        p = self.project()
        old = time.strftime("%Y-%m-%dT23:00:00Z", time.gmtime(time.time() - 86400))
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:
            for _ in range(9):
                f.write(json.dumps({"ts": old, "event": "guard_block", "data": {"category": "rm-outside"}}) + "\n")
        self.assertEqual(self.fm_json("risk")["spent"], 0)

    def test_a_revert_commit_today_costs_three(self):
        self.fm("init")
        g = lambda *a: subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True)  # noqa: E731
        g("-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "--allow-empty", "-m", 'Revert "x"')
        self.assertEqual(self.fm_json("risk")["spent"], 3)
