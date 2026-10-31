"""T-0689 (Intelligence — learning from outcomes): each finished task's fate (reverted, fixed later, held), lessons with
ids and a record of when they were shown, which audit lenses and passes find anything, a track record by type and tier,
bench cases that never discriminate, blocked tasks reopened when what they waited on changed, and process mining."""
import json
import os
import re
import subprocess
import time

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo, *args], check=True, capture_output=True, text=True).stdout

    def commit(self, msg, name="x.py", text=None):
        with open(os.path.join(self.repo, name), "w") as f:
            f.write(text if text is not None else msg + "\n")
        self.git("add", "-A")
        self.git("commit", "-qm", msg)

    def done(self, title, typ="FEATURE", run="true", *extra):
        self.fm("task", "new", title, "--type", typ, "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        tid = c.load_briefs(self.p)[-1].id
        self.fm("task", "finish", tid, "--audit", "self", "--run", run, *extra)
        return tid

    def age(self, tid, days):
        """Backdate a brief (its updated stamp and log) by days."""
        b = c.find_brief(self.p, tid)
        old = c.iso(time.time() - days * 86400)
        with open(b.path, encoding="utf-8") as f:
            text = f.read()
        text = re.sub(r"(?m)^updated: .*$", f"updated: {old}", text)
        text = re.sub(r"(?m)^- \d{4}-\d\d-\d\dT[\d:]+Z done$", f"- {old} done", text)
        with open(b.path, "w", encoding="utf-8") as f:
            f.write(text)


class Outcomes(Base):
    def test_a_reverted_task_and_one_a_later_fix_names_get_their_fate(self):
        a = self.done("Add session cache")
        self.commit(f"Add session cache ({a})")
        self.git("revert", "--no-edit", "HEAD")
        b = self.done("Add export button")
        self.fm("capture", f"Export button crashes on empty table (from {b})", "--type", "FIX", "--tier", "S")
        held = self.done("Rename module")
        out = self.fm("outcomes").stdout
        self.assertRegex(out, rf"{a}\b.*reverted")
        self.assertRegex(out, rf"{b}\b.*fixed later.*T-0003")
        self.assertNotRegex(out, rf"{held}\b.*(reverted|fixed later)")
        data = json.loads(self.fm("outcomes", "--json").stdout)
        self.assertEqual(data["tasks"][held]["fate"], "held")


class Survival(Base):
    """T-1060 (wild C1): each close graded by a 30-day window: survived, lost (and why, when), settling (days left);
    a settle event per grade, the digest's line, the pane's history, and the reports that read the grades."""
    def created(self, tid, days):
        b = c.find_brief(self.p, tid)
        old = c.iso(time.time() - days * 86400)
        with open(b.path, encoding="utf-8") as f:
            text = f.read()
        with open(b.path, "w", encoding="utf-8") as f:
            f.write(re.sub(r"(?m)^created: .*$", f"created: {old}", text))

    def setup_five(self):
        ok = self.done("Old and fine")
        self.age(ok, 40)
        late = self.done("Old, fixed late")
        self.age(late, 40)
        self.fm("capture", f"Late fix for {late}", "--type", "FIX", "--tier", "S")  # 40 days on: outside the window
        early = self.done("Old, fixed early")
        self.age(early, 40)
        self.fm("capture", f"Crash after {early}", "--type", "FIX", "--tier", "S")
        self.created(c.load_briefs(self.p)[-1].id, 35)  # 5 days after its close: inside
        fresh = self.done("Recent and fine")
        gone = self.done("Recent then reverted")
        self.commit(f"Recent then reverted ({gone})")
        self.git("revert", "--no-edit", "HEAD")
        return ok, late, early, fresh, gone

    def test_the_window_grades_each_close(self):
        ok, late, early, fresh, gone = self.setup_five()
        t = json.loads(self.fm("outcomes", "--json").stdout)["tasks"]
        self.assertEqual(t[ok]["survival"], "survived")
        self.assertEqual(t[late]["survival"], "survived")  # a fix 40 days on is a fate, not a loss in the window
        self.assertEqual(t[late]["fate"], "fixed later")
        self.assertEqual(t[early]["survival"], "lost")
        self.assertEqual(t[gone]["survival"], "lost")
        self.assertEqual(t[fresh]["survival"], "settling")
        self.assertGreater(t[fresh]["days_left"], 25)
        out = self.fm("outcomes").stdout
        # T-2037: lost counts every close and survived only those past the window, so give the total and the share
        self.assertIn("Survival (30 days): of 5 closes, 2 lost (40%), 2 survived the window, 1 settling", out)
        self.assertIn("days since a lost task: 0", out)

    def test_settling_logs_one_grade_per_task_and_shows_in_digest_and_history(self):
        ok, late, early, fresh, gone = self.setup_five()
        self.assertIn("4 graded", self.fm("outcomes", "--settle").stdout)
        self.assertIn("0 graded", self.fm("outcomes", "--settle").stdout)  # once per task
        graded = [e for e in c.ledger_tail(self.p, 2000) if e.get("event") == "outcome"]
        self.assertEqual(sorted(e["task"] for e in graded), sorted([ok, late, early, gone]))
        self.assertIn("Survival (30 days)", self.fm("digest").stdout)
        hist = self.fm_json("ui")["history"]
        self.assertTrue(any(h["text"] in ("survived 30 days", "lost") for h in hist), hist[-6:])

    def test_grades_read_the_archived_ledger_and_smoke_is_no_loss(self):
        # review: corrections and earlier grades rolled into archive/ledger-YYYY-MM.jsonl still count; a failing smoke
        # run (it covers the whole UI) never marks a task lost
        ok, late, early, fresh, gone = self.setup_five()
        c.log_event(self.p, "correction", task=ok, data={"text": "no, that broke the parser"})
        c.log_event(self.p, "smoke", data={"defects": 2})
        live = os.path.join(self.p.dir, "ledger.jsonl")
        os.makedirs(os.path.join(self.p.dir, "archive"), exist_ok=True)
        with open(live) as f:
            lines = f.readlines()
        for e in map(json.loads, lines[-2:]):  # backdate them into the window, then roll them out
            e["ts"] = c.iso(time.time() - 38 * 86400)
            with open(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl"), "a") as f:
                f.write(json.dumps(e) + "\n")
        with open(live, "w") as f:
            f.writelines(lines[:-2])
        t = json.loads(self.fm("outcomes", "--json").stdout)["tasks"]
        self.assertEqual(t[ok]["survival"], "lost")
        self.assertEqual(t[ok]["lost_by"], "corrected")
        self.assertEqual(t[fresh]["survival"], "settling", "smoke is no loss")
        self.assertIn("4 graded", self.fm("outcomes", "--settle").stdout)
        with open(live) as f:
            settled = [ln for ln in f if '"outcome"' in ln]
        with open(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl"), "a") as f:
            f.writelines(settled)
        with open(live) as f:
            rest = [ln for ln in f if '"outcome"' not in ln]
        with open(live, "w") as f:
            f.writelines(rest)
        self.assertIn("0 graded", self.fm("outcomes", "--settle").stdout, "a rolled grade still counts as settled")

    def test_history_shows_only_losses(self):
        self.setup_five()
        self.fm("outcomes", "--settle")
        texts = [h["text"] for h in self.fm_json("ui")["history"]]
        self.assertIn("lost", texts)
        self.assertNotIn("survived 30 days", texts)

    def test_empty_claims_say_so(self):
        self.assertIn("nothing graded yet", self.fm("outcomes", "--claims").stdout)

    def test_reports_read_the_grades(self):
        ok, late, early, fresh, gone = self.setup_five()
        self.fm("task", "drop", self.fm_json("task", "new", "Abandoned", "--type", "FEATURE", "--tier", "S")["id"], "no")
        self.assertIn("Survival by close grade", self.fm("outcomes", "--claims").stdout)
        regret = self.fm("outcomes", "--regret").stdout
        self.assertIn(early, regret)
        grave = self.fm("outcomes", "--graveyard").stdout
        self.assertIn(gone, grave)
        self.assertIn("Abandoned", grave)
        self.assertIn("corrected during the task", self.fm("outcomes", "--seen").stdout)


class Lessons(Base):
    def test_lessons_get_ids_shown_counts_and_flags(self):
        a = self.done("Quote shell paths in the deploy script", "FEATURE", "true", "--lesson", "quote every path")
        b = self.done("Cache the parser tables", "FEATURE", "true", "--lesson", "invalidate on schema change")
        self.age(b, 30)
        with open(os.path.join(self.p.dir, "failures.jsonl"), "a") as f:
            f.write(json.dumps({"sig": "keyerror: 'col'", "task": b, "at": c.iso(time.time() - 40 * 86400)}) + "\n")
            f.write(json.dumps({"sig": "keyerror: 'col'", "task": "T-0009", "at": c.now()}) + "\n")
        self.fm("task", "new", "Quote shell paths in the backup script", "--type", "FEATURE", "--tier", "S",
                "--ac", "ok :: true", "--step", "s")
        self.fm("focus", "T-0003")
        out = self.fm("recall", "--lessons").stdout
        self.assertRegex(out, rf"{a}\.1\b.*shown 1")
        self.assertRegex(out, rf"never recalled.*{b}\.1")
        self.assertRegex(out, rf"recurred.*{b}\.1.*T-0009")


class Yield(Base):
    def test_usage_agents_reports_what_each_lens_and_pass_found(self):
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "audit", "T-0001", "edge", "review", "fixed: empty input crashed the parser")
        self.fm("task", "audit", "T-0001", "intent", "self", "no findings")
        self.fm("task", "audit", "T-0001", "adversary", "review", "1 false positive: flagged eval, it is ast.literal_eval")
        self.fm("task", "set", "T-0001", "--section", "Plan review", "--text", "second plan by sonnet")
        self.fm("task", "set", "T-0001", "--section", "Dissent", "--text", "- [ ] the cache can go stale")
        c.log_event(self.p, "second_session", data={"read": 3, "captured": 1})
        c.log_event(self.p, "second_session", data={"read": 2, "captured": 0})
        out = self.fm("usage", "--agents").stdout
        self.assertRegex(out, r"edge: 1 of 1 found something")
        self.assertRegex(out, r"intent: 0 of 1")
        self.assertRegex(out, r"adversary: .*1 false positive")
        self.assertRegex(out, r"second plan: 1 of 1 left dissent")
        self.assertRegex(out, r"second session: 1 of 2 captured")


class TrackRecord(Base):
    def test_track_record_and_would_do_differently_in_digest_and_focus(self):
        self.done("First", "FEATURE", "true", "--differently", "write the failing test before the parser")
        self.fm("task", "new", "Second", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "false", check=False)
        self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true")
        self.assertIn("write the failing test", c.find_brief(self.p, "T-0001").section("Would do differently"))
        out = self.fm("digest").stdout
        self.assertRegex(out, r"Track record.*FEATURE S: 1 of 2 closed on the first finish, 2 of 2 held")
        self.assertIn("write the failing test", out)
        self.fm("task", "new", "Third", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.assertRegex(self.fm("focus", "T-0003").stdout, r"Track record for FEATURE S here: 1 of 2 closed")


class Predictions(Base):
    """T-2290: focus predicts minutes and attempts from the closes of the same tier and type; the close scores them."""

    def seed(self, n, minutes=10, attempts=1, typ="FEATURE", tier="S"):
        import fmoutcomes
        for i in range(n):
            fmoutcomes.record_close(self.p, dict(type=typ, tier=tier, minutes=minutes + i, attempts=attempts))

    def new(self, title="Work", **kw):
        tid = self.fm_json("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")["id"]
        for k, v in kw.items():
            self.fm("task", "set", tid, f"{k}={v}")
        return tid

    def test_focus_predicts_the_median_of_same_tier_and_type(self):
        self.seed(5, minutes=10)  # 10..14: median 12
        self.seed(9, minutes=500, typ="FIX")  # another type never counts
        t = self.new()
        self.fm("focus", t)
        m = c.find_brief(self.p, t).meta
        self.assertEqual((int(m["predict_minutes"]), int(m["predict_attempts"])), (12, 1))

    def test_under_five_samples_predicts_nothing_and_a_typed_one_stays(self):
        self.seed(4)
        a, b = self.new("A"), self.new("B", predict_minutes=7)
        self.fm("focus", a)
        self.assertIsNone(c.find_brief(self.p, a).meta.get("predict_minutes"))
        self.seed(1)
        self.fm("focus", b)
        self.assertEqual(int(c.find_brief(self.p, b).meta["predict_minutes"]), 7)

    def test_the_close_logs_its_stats_and_the_prediction_scored(self):
        self.seed(5)
        t = self.new()
        self.fm("focus", t)
        self.fm("task", "finish", t, "--audit", "self", "--run", "true")
        d = next(e["data"] for e in c.ledger_events(self.p, ("task_done",)) if e["task"] == t)
        self.assertEqual((d["predict_minutes"], d["minutes"], d["attempts"]), (12, 0, 1))
        import fmoutcomes
        self.assertEqual(len(fmoutcomes.history(self.p, "FEATURE", "S")), 6, "the close joins the history")

    def test_calibration_prints_the_median_ratio_per_tier(self):
        import fmoutcomes
        for actual in (10, 20, 40):
            fmoutcomes.record_close(self.p, dict(type="FEATURE", tier="S", minutes=actual, predict_minutes=10))
        out = self.fm("outcomes", "--calibration").stdout
        self.assertRegex(out, r"S: median actual/predicted 2\.0x over 3")

    def test_next_notes_a_task_past_three_times_its_prediction(self):
        t = self.new(predict_minutes=5)
        self.fm("focus", t)
        self.assertNotIn("3x", self.fm("next").stdout)
        live = os.path.join(self.p.dir, "ledger.jsonl")  # the focus happened 25 minutes ago
        with open(live) as f:
            evs = [json.loads(ln) for ln in f]
        for e in evs:
            if e.get("event") == "focus" and e.get("task") == t:
                e["ts"] = c.iso(time.time() - 1500)
        with open(live, "w") as f:
            f.writelines(json.dumps(e) + "\n" for e in evs)
        self.assertEqual(self.fm("next").stdout.count("3x its prediction"), 1)
        self.assertTrue(c.find_brief(self.p, t).meta.get("predict_noted"))
        self.assertNotIn("3x its prediction", self.fm("next").stdout, "said once")

    def test_first_use_backfills_the_history_from_task_done_events(self):
        import fmoutcomes
        ids = [self.new(f"Old {i}") for i in range(5)]
        for i, tid in enumerate(ids):  # closes logged before closes.jsonl existed: no type or tier in the event
            c.log_event(self.p, "task_done", task=tid, data={"minutes": 10 + i, "attempts": 2})
        c.log_event(self.p, "task_done", task=ids[0], data={"attempts": 2})  # no minutes: skipped
        path = os.path.join(self.p.dir, "closes.jsonl")
        self.assertFalse(os.path.exists(path))
        t = self.new("Fresh")
        self.fm("focus", t)
        m = c.find_brief(self.p, t).meta
        self.assertEqual((int(m["predict_minutes"]), int(m["predict_attempts"])), (12, 2))
        self.assertEqual(len(fmoutcomes.history(self.p, "FEATURE", "S")), 5)
        self.assertTrue(os.path.exists(path), "written once")


class Hygiene(Base):
    def test_bench_lists_cases_that_never_discriminate(self):
        d = os.path.join(self.p.dir, "bench", "results")
        os.makedirs(d)
        for label, c2 in (("v1", True), ("v2", False)):
            with open(os.path.join(d, label + ".json"), "w") as f:
                json.dump({"label": label, "cases": [{"id": "same-case", "pass": True}, {"id": "split-case", "pass": c2}]}, f)
        out = self.fm("bench", "hygiene").stdout
        self.assertRegex(out, r"same-case.*passed in all 2 runs")
        self.assertNotIn("split-case", out)


class Reopen(Base):
    def test_tidy_reopens_a_blocked_task_once_what_it_waited_on_changed(self):
        os.makedirs(os.path.join(self.repo, "lib"))
        self.commit("lib", "lib/shim.py", "X = 1\n")
        self.fm("task", "new", "Upstream", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "new", "Downstream", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "set", "T-0002", "depends_on=T-0001")
        self.fm("task", "block", "T-0002", "waits for T-0001")
        self.fm("task", "new", "Waits on shim", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "block", "T-0003", "lib/shim.py returns the wrong type until upstream fixes it")
        self.fm("task", "new", "Waits on a person", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "block", "T-0004", "needs the owner's phone")
        self.fm("task", "drop", "T-0001", "done elsewhere")
        time.sleep(1.1)
        self.commit("shim fixed upstream", "lib/shim.py", "X = 2\n")  # T-1106: a real change, not a new mtime
        self.assertRegex(self.fm("next").stdout, r"2 blocked task\(s\) waited on changed.*fm tidy --apply")
        self.fm("tidy", "--apply")
        self.assertEqual(c.find_brief(self.p, "T-0002").status, "planned")
        self.assertEqual(c.find_brief(self.p, "T-0003").status, "planned")
        self.assertEqual(c.find_brief(self.p, "T-0004").status, "blocked")
        self.assertIn("lib/shim.py changed", c.find_brief(self.p, "T-0003").section("Log"))

    def test_reverted_commits_come_back_in_recall_as_wrong_turns(self):
        self.commit("Use a global lock for the session cache")
        self.git("revert", "--no-edit", "HEAD")
        self.assertRegex(self.fm("recall", "session", "cache", "lock").stdout,
                         r"wrong turn.*global lock for the session cache")


class Mining(Base):
    def test_friction_mines_paths_smooth_unverified_and_give_up_points(self):
        def ev(event, task, **data):
            c.log_event(self.p, event, task=task, data=data)
        ev("focus", "T-0005")
        ev("task_done", "T-0005", verified="weak", type="FEATURE", tier="S")
        ev("focus", "T-0006")
        for _ in range(3):
            ev("evidence", "T-0006", cmd="pytest", result=c.run_result(1, "2 failed"))  # the real format
        ev("task_block", "T-0006", reason="can't reproduce")
        out = self.fm("friction").stdout
        self.assertRegex(out, r"smooth but unverified[^\n]*\n\s+- T-0005")
        self.assertRegex(out, r"give-up points[^\n]*\n\s+- [^\n]*after 3 failed run\(s\)[^\n]*T-0006")
        self.assertRegex(out, r"common paths[^\n]*\n\s+- focus → done")
