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

    def test_a_recovered_trigger_climbs_back(self):
        for _ in range(5):
            self.fire("flaky", "dropped")
        for _ in range(20):  # the last 20 closed ones decide
            self.fire("flaky", "done")
        self.assertEqual(self.fire("flaky").priority, "normal")
