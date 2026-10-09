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
        later = time.time() + 5
        os.utime(os.path.join(self.repo, "lib", "shim.py"), (later, later))
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
