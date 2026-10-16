"""fm contract (T-1158): an unattended run's time and spend bounds; past either, the drive stops and a receipt says why."""
import json
import os
import time

from test_hooks import HookCase, parse

import fmbudget as bud
import fmcontract as con
import fmcore as c


class Contract(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = self.task()

    def stop(self):
        return self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "On to the next step.",
                                  "session_id": "s1"})

    def test_no_contract_changes_nothing(self):
        self.assertIsNone(con.over(self.project()))
        self.assertEqual((parse(self.stop()) or {}).get("decision"), "block")
        self.assertNotIn("contract", self.fm("next").stdout.lower())

    def test_time_bound_stops_the_drive_with_a_fake_clock(self):
        self.fm("contract", "--until", "23:59")
        p = self.project()
        self.assertIsNone(con.over(p, now=time.time()))
        self.assertEqual(con.over(p, now=time.time() + 3 * 86400), "time")
        c.update_meta(p, contract={**c.read_meta(p)["contract"], "until": time.time() - 5})
        self.assertNotEqual((parse(self.stop()) or {}).get("decision"), "block")
        self.assertIn("contract ended", self.fm("next").stdout)

    def test_spend_bound_stops_the_drive_and_the_receipt_says_so(self):
        self.fm("contract", "--usd", "1.5")
        p = self.project()
        bud.record("run", 0.5, project=p.slug)
        self.assertIsNone(con.over(p))
        bud.record("run", 1.25, project=p.slug)
        self.assertEqual(con.over(p), "spend")
        self.assertNotEqual((parse(self.stop()) or {}).get("decision"), "block")
        c.update_meta(p, contract={**c.read_meta(p)["contract"], "ended_at": None})  # receipt recomputes if unfrozen
        self.fm("task", "log", self.tid, "x")
        r = self.fm("contract", "receipt").stdout
        self.assertIn("spend", r)
        self.assertIn("$1.75", r)
        self.assertIn("0 task(s) closed", r)

    def test_receipt_lists_tasks_closed_since_it_began(self):
        self.fm("contract", "--usd", "0.1")
        p = self.project()
        with c.lock(p.dir):
            c.log_event(p, "task_done", task="T-9999")
        bud.record("run", 0.2, project=p.slug)
        r = self.fm("contract", "receipt").stdout
        self.assertIn("1 task(s) closed: T-9999", r)
        self.assertIn("bound that ended it: spend", r)

    def seed(self, **costs):
        import fmcost
        path = fmcost._cache_path(self.project())
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"size": 0, "ts": time.time(), "costs": costs}, f)

    def test_token_bound_counts_what_this_projects_sessions_used_since_it_began(self):
        self.seed(**{"T-1": 500})
        self.fm("contract", "--tokens", "2k")
        p = self.project()
        self.assertIsNone(con.over(p))
        self.seed(**{"T-1": 1700})  # 1200 more
        self.assertIsNone(con.over(p))
        self.seed(**{"T-1": 1700, "T-2": 900})  # 2100 more
        self.assertEqual(con.over(p), "tokens")
        self.assertNotEqual((parse(self.stop()) or {}).get("decision"), "block")
        r = self.fm("contract", "receipt").stdout
        self.assertIn("2k tokens", r)
        self.assertIn("bound that ended it: tokens", r)
        self.assertIn("--tokens takes", self.fm("contract", "--tokens", "lots", check=False).stderr)

    def test_another_projects_spend_is_not_counted(self):
        self.fm("contract", "--usd", "1")
        bud.record("run", 5, project="elsewhere")
        bud.record("run", 5)
        self.assertIsNone(con.over(self.project()))

    def test_the_stop_hook_that_first_sees_the_bound_freezes_it_without_waiting_on_its_own_lock(self):
        self.fm("contract", "--until", "23:59")
        p = self.project()
        c.update_meta(p, contract={**c.read_meta(p)["contract"], "until": time.time() - 5})
        t0 = time.time()
        r = self.stop()
        self.assertLess(time.time() - t0, 4, "over() relocked the project inside the Stop hook's own lock")
        self.assertNotEqual((parse(r) or {}).get("decision"), "block")
        self.assertEqual(c.read_meta(p)["contract"]["ended"], "time")

    def test_a_new_session_clears_an_ended_contract_and_the_receipt_stays_readable(self):
        self.fm("contract", "--usd", "0.1")
        p = self.project()
        bud.record("run", 0.5, project=p.slug)
        self.assertNotEqual((parse(self.stop()) or {}).get("decision"), "block")
        self.hook("SessionStart", {"source": "compact", "session_id": "s1"})
        self.assertIn("contract", c.read_meta(p), "a compaction is the same session")
        self.hook("SessionStart", {"source": "startup", "session_id": "s2"})
        self.assertNotIn("contract", c.read_meta(p))
        self.assertIn("bound that ended it: spend", self.fm("contract", "receipt").stdout)
        self.assertEqual((parse(self.stop()) or {}).get("decision"), "block")

    def test_an_ended_contract_turns_off_the_loops_next_round_in_fm_next(self):
        self.fm("task", "drop", self.tid, "not needed")
        self.fm("loop", "on")
        self.assertIn("forever loop", self.fm("next").stdout)
        self.fm("contract", "--usd", "0")
        self.assertNotIn("forever loop", self.fm("next").stdout)

    def test_the_cost_refresh_child_is_spawned_at_most_once_a_minute(self):
        import subprocess
        import fmcost
        calls = []
        real, subprocess.Popen = subprocess.Popen, lambda *a, **k: calls.append(a)
        try:
            os.environ.pop("FOREMAN_NO_BACKGROUND")
            fmcost._refresh_detached(self.project())
            fmcost._refresh_detached(self.project())
        finally:
            subprocess.Popen = real
            os.environ["FOREMAN_NO_BACKGROUND"] = "1"
        self.assertEqual(len(calls), 1)

    def test_off_ends_it(self):
        self.fm("contract", "--usd", "0.1")
        self.assertIn("contract", self.fm("contract").stdout)
        self.fm("contract", "off")
        self.assertNotIn("contract", c.read_meta(self.project()))
        bud.record("run", 5, project=self.project().slug)
        self.assertEqual((parse(self.stop()) or {}).get("decision"), "block")

    def test_until_rolls_to_tomorrow_when_past(self):
        t = con.parse_until("00:00", now=time.mktime((2026, 1, 1, 12, 0, 0, 0, 0, -1)))
        self.assertEqual(time.localtime(t)[2:5], (2, 0, 0))
