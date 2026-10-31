"""T-2276: fm triggers counts each trigger's captures by outcome; a trigger whose closed captures are mostly dropped
files at low priority; urgent triggers and triggers with too few closes are left alone."""
from helpers import ForemanTestCase

import fmcore as c
import fmeco


class Triggers(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.n = 0

    def fire(self, trigger, status=None, **kw):
        self.n += 1
        b, new = fmeco.capture_once(self.p, f"FIX: {trigger} finding {self.n}", "FIX", "discovered", trigger=trigger, **kw)
        self.assertTrue(new)
        if status:
            b.meta["status"] = status
            c.save_brief(self.p, b, touch=False)
        return b

    def rows(self):
        return {r["trigger"]: r for r in self.fm_json("triggers")["triggers"]}

    def test_counts_per_trigger_from_captures_and_their_final_status(self):
        for st in ["done", "done", "done", "dropped", "dropped", None]:
            self.fire("scout", st)
        self.fire("spec", "done")
        r = self.rows()
        self.assertEqual({k: r["scout"][k] for k in ("fired", "done", "dropped", "open")},
                         {"fired": 6, "done": 3, "dropped": 2, "open": 1})
        self.assertAlmostEqual(r["scout"]["precision"], 0.6)
        self.assertEqual(r["spec"]["precision"], 1.0)

    def test_trigger_defaults_to_the_source_and_a_user_capture_is_not_a_trigger(self):
        b, _ = fmeco.capture_once(self.p, "FIX: from a sweep", "FIX", "cross-project")
        fmeco.capture_once(self.p, "FIX: typed by hand", "FIX", "user")
        r = self.rows()
        self.assertEqual(r["cross-project"]["fired"], 1)
        self.assertNotIn("user", r)
        self.assertIsNone(r["cross-project"]["precision"])  # nothing closed yet

    def test_mostly_dropped_trigger_files_at_low_priority_with_a_note(self):
        for _ in range(5):
            self.fire("noisy", "dropped")
        b = self.fire("noisy")
        self.assertEqual(b.priority, "low")
        self.assertIn("precision 0.00", b.section("Raw request"))
        self.assertEqual(c.find_brief(self.p, b.id).priority, "low")

    def test_few_closed_captures_or_good_precision_stay_normal(self):
        for _ in range(4):
            self.fire("young", "dropped")
        self.assertEqual(self.fire("young").priority, "normal")
        for st in ["done", "done", "dropped", "dropped", "dropped"]:  # 0.4
            self.fire("mixed", st)
        self.assertEqual(self.fire("mixed").priority, "normal")

    def test_urgent_triggers_are_never_demoted(self):
        for _ in range(6):
            self.fire("baseline", "dropped")
        self.assertEqual(self.fire("baseline").priority, "normal")

    def test_state_names_the_noisiest_trigger_and_a_second_state_reloads_no_briefs(self):
        import unittest.mock as mock

        import fmtriggers
        for _ in range(5):
            self.fire("noisy", "dropped")
        self.assertEqual(fmtriggers.noisiest(self.p)["trigger"], "noisy")
        real = c.load_briefs
        with mock.patch.object(c, "load_briefs", side_effect=lambda *a, **k: real(*a, **k)) as m:
            self.assertEqual(fmtriggers.noisiest(self.p)["trigger"], "noisy")
            self.assertEqual(m.call_count, 0)
        self.assertIn("Noisiest trigger: noisy", self.fm("state").stdout)

    def test_noisiest_uses_the_rule_that_demotes_the_last_20_closed(self):
        import fmtriggers
        for _ in range(40):
            self.fire("healed", "dropped")
        for _ in range(10):
            self.fire("healed", "done")
        for _ in range(10):
            self.fire("healed", "dropped")  # last 20: 0.5, though over all 60 it is 0.17
        self.assertIsNone(fmtriggers.noisiest(self.p))
        self.assertEqual(self.fire("healed").priority, "normal")

    def test_a_failing_precision_read_never_loses_the_capture(self):
        import unittest.mock as mock
        with mock.patch("fmtriggers.noisy", side_effect=RuntimeError("boom")):
            b = self.fire("any")
        self.assertEqual(b.priority, "normal")

    def test_fm_triggers_is_read_only_and_days_is_clamped(self):
        import os
        self.fire("scout", "done")
        r = self.fm_json("triggers", "--days", "0")
        self.assertEqual(r["days"], 1)
        self.assertEqual(self.fm_json("triggers", "--days", "999999")["days"], 3650)
        self.assertFalse(os.path.exists(os.path.join(self.p.dir, "triggers.json")))

    def test_ad_hoc_sources_count_as_triggers(self):
        c.log_event(self.p, "capture", task="T-0099", data={"source": "sentinel"})  # as fm sentinel logs it
        self.fm("capture", "a follow-up", "--source", "followup")
        r = self.rows()
        self.assertEqual((r["sentinel"]["fired"], r["followup"]["fired"]), (1, 1))

    def test_a_recovered_trigger_climbs_back(self):
        for _ in range(5):
            self.fire("flaky", "dropped")
        for _ in range(20):  # the last 20 closed ones decide
            self.fire("flaky", "done")
        self.assertEqual(self.fire("flaky").priority, "normal")
