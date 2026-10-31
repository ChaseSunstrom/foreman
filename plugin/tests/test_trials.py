"""T-1059: a self-change is a pre-registered trial: the metric it should move and by when; the digest grades it."""
import datetime
from unittest import mock

from helpers import ForemanTestCase

import fmcore as c
import fmtrials as tr


def ago(days):
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


class Trials(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def events(self, per_day_before, per_day_after, age=10):
        """Corrections over the `age` days before the trial's registration and the `age` days after."""
        for d in range(1, 2 * age + 1):
            n = per_day_before if d > age else per_day_after
            for _ in range(n):
                with mock.patch.object(c, "now", lambda d=d: ago(d - 0.5)):
                    c.log_event(self.p, "correction", data={"text": "no"})

    def register(self, age=10, by=10):
        with mock.patch.object(c, "now", lambda: ago(age)):
            tr.add(self.p, "rule X", "corrections", by)

    def test_unchanged_rate_proposes_revert_and_halved_moved(self):
        self.events(5, 5)
        self.register()
        self.assertIn("no movement: propose revert", tr.lines(self.p)[-1])
        self.setUp()
        self.events(6, 3)
        self.register()
        self.assertIn("moved", tr.lines(self.p)[-1])
        self.assertNotIn("revert", tr.lines(self.p)[-1])

    def test_pending_before_due(self):
        self.register(age=4, by=10)
        self.assertIn("pending, 6 days left", tr.lines(self.p)[-1])

    def test_rule_add_with_moves_writes_a_trial_the_digest_prints(self):
        self.fm("rule", "add", "rm -rf", "--why", "no", "--moves", "corrections", "--by", "30")
        out = self.fm("digest").stdout
        self.assertIn("rule add rm -rf", out)
        self.assertIn("pending, 30 days left", out)

    def test_by_below_one_is_refused(self):
        import fmcli
        for by in (0, -3):
            with self.assertRaises(fmcli.UsageError):
                tr.add(self.p, "rule X", "corrections", by)
        self.assertEqual(tr.load(self.p), [])

    def test_malformed_trial_record_is_skipped_by_lines(self):
        c.write_atomic(tr._path(self.p), '[{"what": "x", "by": 0, "at": "bad"}, 5, {"what": "ok", "moves": "corrections", "by": 10, "at": "%s"}]' % ago(1))
        out = "\n".join(tr.lines(self.p))
        self.assertIn("ok: pending", out)
        self.assertNotIn("x:", out)

    def test_no_moves_records_nothing(self):
        self.fm("rule", "add", "rm -rf", "--why", "no")
        self.assertEqual(tr.load(self.p), [])
        self.assertNotIn("Trials", self.fm("digest").stdout)


class SelfFixTrials(ForemanTestCase):
    """T-2351: a task a trigger filed is a trial on its trigger's own key: the digest says whether that key came back."""
    KEY = "CONTEXT: https://ci.example/run/7, "

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def capture(self, days, source="ci", key=KEY, title="FIX: CI red on main"):
        import fmeco
        with mock.patch.object(c, "now", lambda: ago(days)):
            return fmeco.capture_once(self.p, f"{title}\n{key}", "FIX", source, key=key)[0]

    def fixed(self, sightings_before, finished=20):
        """A ci capture seen sightings_before times (the filing included), focused and finished `finished` days ago."""
        b = self.capture(finished + 5)
        for i in range(1, sightings_before):
            self.capture(finished + 5 - i * 0.1)
        with mock.patch.object(c, "now", lambda: ago(finished + 1)):
            c.log_event(self.p, "focus", task=b.id)
        with mock.patch.object(c, "now", lambda: ago(finished)):
            tr.register_fix(self.p, c.find_brief(self.p, b.id))
        return b

    def test_a_trigger_filed_capture_carries_its_trigger_and_key_and_a_user_one_registers_nothing(self):
        b = self.capture(1)
        self.assertEqual(b.meta.get("trigger"), "ci")
        self.assertTrue(b.meta.get("trigger_key"))
        self.assertIsNotNone(tr.register_fix(self.p, b))
        self.assertIsNone(tr.register_fix(self.p, b))  # once per task
        u = self.capture(1, source="user", key="CONTEXT: mine, ", title="FIX: my own")
        self.assertIsNone(tr.register_fix(self.p, u))
        self.assertEqual([t["task"] for t in tr.load(self.p) if t.get("kind") == "self-fix"], [b.id])

    def test_fm_task_done_registers_the_trial(self):
        b = self.capture(1)
        self.fm("task", "set", b.id, "--section", "Interpretation", "--text", "Reading 1: fix it. Reading 2: no.")
        self.fm("task", "ac", b.id, "add", "ok :: true")
        self.fm("task", "step", b.id, "add", "fix")
        self.fm("focus", b.id)
        self.fm("task", "evidence", b.id, "--step", "1", "--run", "true")
        self.fm("task", "check", b.id, "1", "--run", "true", check=False)
        self.fm("task", "set", b.id, "--section", "Regression test", "--text", "none: a test fixture")
        r = self.fm("task", "finish", b.id, "--run", "true", "--audit", "self: fixture", "--lesson", "x", check=False)
        self.assertEqual(c.find_brief(self.p, b.id).status, "done", r.stderr[:600])
        self.assertEqual([t["task"] for t in tr.load(self.p) if t.get("kind") == "self-fix"], [b.id])

    def verdict(self):
        return [ln for ln in tr.lines(self.p) if "Self-fix" in ln][-1]

    def test_held_when_the_key_stays_gone(self):
        self.fixed(3)
        self.assertIn("held: its key was seen 3 times", self.verdict())

    def test_didnt_hold_when_the_key_comes_back_and_the_fix_is_filed_once(self):
        b = self.fixed(3)
        self.capture(10)  # seen again inside the 14 days after the fix landed
        line = self.verdict()
        self.assertIn("didn't hold: its key was seen 3 times before the fix, 1 since", line)
        fixes = lambda: [x for x in c.load_briefs(self.p) if x.title.startswith(f"Self-fix {b.id} didn't hold")]  # noqa
        self.assertEqual(fixes(), [])  # fm trial only reads; the digest files it
        tr.lines(self.p, act=True)
        tr.lines(self.p, act=True)  # the digest runs again: the verdict is stored, nothing new is filed or logged
        self.assertEqual(len(fixes()), 1, [x.title for x in c.load_briefs(self.p)])
        self.assertIn("git revert", fixes()[0].section("Raw request"))
        self.assertIsNone(tr.register_fix(self.p, fixes()[0]))  # the trial's own FIX never trials itself (no loop)
        self.assertEqual([t.get("verdict") for t in tr.load(self.p)], ["didn't hold"])

    def test_a_signal_filed_as_discovered_registers_by_its_trigger(self):  # T-2351 review: ci-red, did-not-hold, …
        import fmeco
        b = fmeco.capture_once(self.p, "FIX: CI on main is red at abc1234 (test)\nCI-red: abc1234", "FIX", "discovered",
                               key="CI-red: abc1234", trigger="ci-red", trial_key="ci:main:test")[0]
        self.assertEqual(b.meta.get("trigger"), "ci-red")
        mine = fmeco.capture_once(self.p, "FIX: something I noticed", "FIX", "discovered")[0]
        self.assertIsNone(mine.meta.get("trigger_key"))  # the session's own capture: no signal fired

    def test_a_ci_failure_on_a_new_run_is_the_same_key(self):  # T-2351 review: the run URL changes every run
        import fmeco
        keys = []
        for run in (7, 8):
            with mock.patch.object(c, "now", lambda: ago(1)):
                fmeco.capture_once(self.p, f"CI failed on main: run {run}\nCONTEXT: https://ci/{run}, ", "FIX", "ci",
                                   key=f"CONTEXT: https://ci/{run}, ", trial_key="ci:main:test")
        seen = [e["data"]["key"] for e in c.ledger_events(self.p, ("trigger_seen",))]
        self.assertEqual(len(seen), 2)
        self.assertEqual(len(set(seen)), 1)

    def test_a_key_seen_only_when_filed_is_unmeasured_never_held(self):
        self.fixed(1)
        self.assertIn("unmeasured", self.verdict())

    def test_pending_until_due(self):
        self.fixed(3, finished=3)
        self.assertIn("pending", self.verdict())
