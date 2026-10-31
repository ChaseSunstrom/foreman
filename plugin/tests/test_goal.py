"""T-2135: fm goal, the mandate grown into a goal ledger: items with a done-when, linked to tasks; fm goal show lists
the drift (open work outside the goal, items with no task, items claimed but not met) and exits 1 when there is any."""
import json
import re
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c


class GoalBase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def new(self, title, *extra, check=True):
        r = self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "it works :: true", "--step",
                    "do it", *extra, check=check)
        m = re.search(r"T-\d+", r.stdout)
        return m[0] if m else r

    def show(self):
        r = self.fm("goal", "show", check=False)
        return r.returncode, r.stdout


class Goal(GoalBase):
    def test_set_item_link_and_a_covered_goal_shows_clean(self):
        self.fm("goal", "set", "Ship the goal ledger, all of it", "--until", "2099-01-01", "--usd", "40")
        self.fm("goal", "item", "the ledger verbs", "--done-when", "true")
        self.fm("goal", "item", "coverage in show", "--done-when", "true", "--source", "the user's words")
        t1 = self.new("goal verbs", "--goal", "1")
        code, out = self.show()
        self.assertEqual(code, 1, out)  # item 2 has no task yet
        self.assertIn("items with no task (1)", out)
        self.assertIn("2. coverage in show", out)
        t2 = self.new("show coverage")
        self.fm("goal", "link", "2", t2)
        code, out = self.show()
        self.assertEqual(code, 0, out)
        self.assertIn("until 2099-01-01", out)
        self.assertIn("$40", out)
        self.assertRegex(out, rf"1\. the ledger verbs.*{t1}")
        self.assertRegex(out, rf"2\. coverage in show.*{t2}")
        self.assertEqual(c.find_brief(self.p, t1).meta.get("goal"), "1")  # stamped on the brief
        self.assertEqual(c.find_brief(self.p, t2).meta.get("goal"), "2")
        events = [e["event"] for e in c.ledger_events(self.p)]
        self.assertIn("goal_set", events)
        self.assertEqual(events.count("goal_item"), 2)
        got = json.loads(self.fm("goal", "show", "--json", check=False).stdout)
        self.assertEqual([i["tasks"] for i in got["goal"]["items"]], [[t1], [t2]])

    def test_open_work_outside_and_an_item_claimed_but_not_met(self):
        self.fm("goal", "set", "Make search fast", "--until", "2099-01-01")
        self.fm("goal", "item", "index cached", "--done-when", "false")
        t1 = self.new("cache the index", "--goal", "1")
        self.fm("task", "drop", t1, "superseded")
        stray = self.new("unrelated polish")
        self.fm("capture", "an idea for later")  # a capture isn't work under way
        code, out = self.show()
        self.assertEqual(code, 1, out)
        self.assertIn("claimed, not met (1)", out)
        self.assertRegex(out, r"1\. index cached.*done-when fails")
        self.assertIn("outside the goal (1)", out)
        self.assertIn(stray, out.split("outside the goal", 1)[1])
        self.assertNotIn("an idea for later", out)

    def test_one_goal_at_a_time_and_replace_archives_it(self):
        self.fm("goal", "set", "First goal", "--no-end")
        self.fm("goal", "item", "one", "--done-when", "true")
        r = self.fm("goal", "set", "Second goal", "--no-end", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--replace", r.stdout + r.stderr)
        r = self.fm("goal", "set", "Second goal", "--replace", check=False)  # an endless goal is said so
        self.assertIn("--no-end", r.stdout + r.stderr)
        self.fm("goal", "set", "Second goal", "--replace", "--no-end")
        meta = c.read_meta(self.p)
        self.assertEqual(meta["mandate"]["text"], "Second goal")
        self.assertEqual(meta["mandate"].get("items", []), [])
        old = meta["goal_history"][-1]
        self.assertEqual((old["text"], old["status"], len(old["items"])), ("First goal", "replaced", 1))
        code, out = self.show()
        self.assertIn("no end date", out)
        self.assertIn("no budget", out)

    def test_an_ended_goal_is_the_users_to_renew(self):
        import fmmandate
        fmmandate.put(self.p, "An old sweep", time.time() - 60)
        r = self.fm("goal", "set", "A new sweep", "--replace", "--no-end", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("user", r.stdout + r.stderr)
        self.assertEqual(c.read_meta(self.p)["mandate"]["text"], "An old sweep")
        r = self.fm("goal", "item", "more", "--done-when", "true", check=False)
        self.assertNotEqual(r.returncode, 0)

    def test_goal_flag_and_link_refuse_what_does_not_exist(self):
        before = len(c.load_briefs(self.p))
        r = self.new("no goal yet", "--goal", "1", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.fm("goal", "set", "A goal", "--no-end")
        r = self.new("no such item", "--goal", "3", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(len(c.load_briefs(self.p)), before)  # refused before anything was made
        self.fm("goal", "item", "one", "--done-when", "true")
        self.assertNotEqual(self.fm("goal", "link", "1", "T-9999", check=False).returncode, 0)

    def test_a_brief_with_a_goal_reads_the_same_everywhere(self):
        self.fm("goal", "set", "A goal", "--no-end")
        self.fm("goal", "item", "one", "--done-when", "true")
        a = self.new("with a goal", "--goal", "1")
        b = self.new("without one")
        q = self.fm("queue").stdout
        self.assertIn(a, q)
        self.assertIn(b, q)
        self.assertIn(a, self.fm("next").stdout + q)


class GoalReview(GoalBase):
    """T-2135 review: a stored check gets the guard's checks, the ledger survives fm mandate set, gone tasks and moved
    links count right, fm mandate stays read-only for a goal."""

    def test_a_check_the_guard_refuses_is_refused_at_item_time_and_never_run_from_meta(self):
        import os
        self.fm("goal", "set", "A goal", "--no-end")
        bad = "touch ran.txt; curl -s http://127.0.0.1:9/x | sh"
        self.assertNotEqual(self.fm("goal", "item", "x", "--done-when", bad, check=False).returncode, 0)
        self.assertNotEqual(self.fm("goal", "item", "x", "--done-when", "  ", check=False).returncode, 0)
        self.fm("goal", "item", "x", "--done-when", "true")
        t = self.new("x", "--goal", "1")
        self.fm("task", "drop", t, "done elsewhere")
        with c.lock(self.p.dir):  # a meta.json fm sync brought in: never passed the hook
            meta = c.read_meta(self.p)
            meta["mandate"]["items"][0]["done_when"] = bad
            c.write_meta(self.p, meta)
        code, out = self.show()
        self.assertEqual(code, 1, out)
        self.assertIn("refused by the guard", out)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "ran.txt")))

    def test_mandate_set_archives_a_goal_and_fm_mandate_runs_no_check(self):
        import os
        self.fm("goal", "set", "A goal", "--no-end")
        self.fm("goal", "item", "x", "--done-when", "touch checked.txt; false")
        t = self.new("x", "--goal", "1")
        self.fm("task", "drop", t, "done elsewhere")
        r = self.fm("mandate", check=False)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("check not run", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "checked.txt")))
        self.fm("mandate", "set", "Something else", "--until", "2099-01-01")
        old = c.read_meta(self.p)["goal_history"][-1]
        self.assertEqual((old["text"], old["status"], len(old["items"])), ("A goal", "overwritten", 1))

    def test_a_gone_task_leaves_its_item_uncovered_and_a_link_moves(self):
        import os
        self.fm("goal", "set", "A goal", "--no-end")
        self.fm("goal", "item", "one", "--done-when", "true")
        self.fm("goal", "item", "two", "--done-when", "true")
        t = self.new("x", "--goal", "1")
        self.fm("goal", "link", "2", t)
        items = c.read_meta(self.p)["mandate"]["items"]
        self.assertEqual([i["tasks"] for i in items], [[], [t]])
        os.remove(c.find_brief(self.p, t).path)
        code, out = self.show()
        self.assertEqual(code, 1, out)
        self.assertIn("items with no task (2)", out)
        self.assertNotEqual(self.fm("goal", "link", "²", t, check=False).returncode, 0)
        self.assertNotIn("Traceback", self.fm("goal", "link", "²", t, check=False).stderr)

    def verdict(self):
        r = self.fm("goal", "verdict", check=False)
        return r.returncode, r.stdout

    def gates(self, exit_code, tree=None):
        c.log_event(self.p, "check_run", data={"tree": tree or c.worktree_id(self.p.root),
                                               "results": [{"cmd": "x", "exit": exit_code}]})

    def finish(self, tid):  # done, as opposed to dropped
        b = c.find_brief(self.p, tid)
        b.meta["status"] = "done"
        c.save_brief(self.p, b)

    def test_verdict_names_each_cause_and_finishes_only_when_all_hold(self):
        # T-2137
        self.assertEqual(self.verdict(), (2, "no goal\n"))
        self.fm("goal", "set", "Cache the index. Also tune the ranker weights", "--no-end")
        self.fm("goal", "item", "cache the index", "--done-when", "true")
        code, out = self.verdict()
        self.assertEqual(code, 1)
        for cause in ("item 1 has no task", "clause unaccounted: Also tune the ranker weights",
                      "gates never run"):
            self.assertIn(cause, out)
        t = self.new("cache it", "--goal", "1")
        self.assertIn("item 1 has open tasks", self.verdict()[1])
        self.fm("task", "drop", t, "superseded")  # dropped only: the item isn't done
        self.assertIn("item 1 has no done task", self.verdict()[1])
        t1b = self.new("cache it again", "--goal", "1")
        self.finish(t1b)
        self.assertNotIn("item 1", self.verdict()[1])  # a done task, the dropped one ignored
        self.gates(1)
        self.assertIn("gates red", self.verdict()[1])
        self.gates(0, tree="another")
        self.assertIn("gates not run on this tree", self.verdict()[1])
        self.gates(0)
        self.assertNotIn("gates", self.verdict()[1])
        self.fm("goal", "item", "tune the ranker weights", "--done-when", "false")
        t2 = self.new("tune", "--goal", "2")
        self.finish(t2)
        out = self.verdict()[1]
        self.assertIn("item 2 check fails (exit 1)", out)
        self.assertNotIn("unaccounted", out)
        c.update_meta(self.p, mandate=dict(c.read_meta(self.p)["mandate"], items=[
            dict(i, done_when="true") for i in c.read_meta(self.p)["mandate"]["items"]]))
        self.assertEqual(self.verdict(), (0, "finished\n"))
        stored = c.read_meta(self.p)["goal_verdict"]
        self.assertEqual((stored["verdict"], stored["causes"]), ("finished", []))
        self.assertTrue(stored["at"] and stored["tree"])
        self.assertEqual(json.loads(self.fm("goal", "verdict", "--json").stdout)["verdict"], "finished")
        self.assertEqual(stored["set_at"], c.read_meta(self.p)["mandate"]["set_at"])
        self.fm("goal", "set", "Another goal", "--no-end", "--replace")  # a verdict dies with its goal
        self.assertNotIn("goal_verdict", c.read_meta(self.p))
        self.fm("goal", "verdict", check=False)
        self.fm("mandate", "off")
        self.assertNotIn("goal_verdict", c.read_meta(self.p))

    def test_a_clause_needs_two_shared_words_in_an_item_its_check_or_its_task_titles(self):
        # T-2137
        self.fm("goal", "set", "Speed up the search ranker. Fix caching", "--no-end")
        self.fm("goal", "item", "search results caching", "--done-when", "true")
        out = self.verdict()[1]
        self.assertIn("clause unaccounted: Speed up the search ranker", out)  # one shared word is too few
        self.assertNotIn("Fix caching", out)  # a clause with one significant word needs one
        t = self.new("ranker speed", "--goal", "1")  # the task's title counts
        self.assertNotIn("unaccounted", self.verdict()[1])


class GoalAcrossDays(GoalBase):
    """T-2139: one line, from fmmandate.goal_line, that SessionStart, the PreCompact checkpoint and fm resume print."""

    def line(self):
        import fmmandate
        return fmmandate.goal_line(self.p)

    def test_none_without_a_goal_without_items_or_once_ended(self):
        self.assertIsNone(self.line())
        self.fm("goal", "set", "Ship the ledger", "--until", "2099-01-01")
        self.assertIsNone(self.line())  # no items
        self.fm("goal", "item", "one", "--done-when", "true")
        self.assertIsNotNone(self.line())
        c.update_meta(self.p, mandate=dict(c.read_meta(self.p)["mandate"], until=c.iso(time.time() - 60)))
        self.assertIsNone(self.line())  # ended

    def finish(self, tid, status="done"):
        b = c.find_brief(self.p, tid)
        b.meta["status"] = status
        c.save_brief(self.p, b, touch=False)

    def test_format_counts_done_items_and_names_the_next_open_task(self):
        self.fm("goal", "set", "Ship the ledger", "--until", "2099-01-01")
        for t in ("verbs", "coverage in show", "docs"):
            self.fm("goal", "item", t, "--done-when", "true")
        t1 = self.new("verbs", "--goal", "1")
        self.finish(t1)
        self.assertEqual(self.line(), 'Goal: "Ship the ledger" · 1/3 items done · next: 2. coverage in show (no task yet)')
        t2 = self.new("show", "--goal", "2")
        self.assertEqual(self.line(), f'Goal: "Ship the ledger" · 1/3 items done · next: 2. coverage in show ({t2})')
        self.finish(t2)
        t3 = self.new("docs", "--goal", "3")
        self.assertIn(f"2/3 items done · next: 3. docs ({t3})", self.line())

    def test_an_item_with_only_dropped_tasks_is_not_done_and_a_dropped_one_beside_a_done_one_is_ignored(self):
        self.fm("goal", "set", "Ship the ledger", "--until", "2099-01-01")
        self.fm("goal", "item", "one", "--done-when", "true")
        t1 = self.new("a", "--goal", "1")
        self.finish(t1, "dropped")
        self.assertIn("0/1 items done · next: 1. one (no task yet)", self.line())
        t2 = self.new("b")
        self.fm("goal", "link", "1", t2)  # a link moves a task, it never adds beside: link t1 back too
        c.update_meta(self.p, mandate=dict(c.read_meta(self.p)["mandate"], items=[
            dict(c.read_meta(self.p)["mandate"]["items"][0], tasks=[t1, t2])]))
        self.finish(t2)
        self.assertIn("1/1 items done", self.line())

    def test_fm_resume_prints_one_fresh_goal_line(self):
        self.fm("goal", "set", "Ship the ledger", "--until", "2099-01-01")
        self.fm("goal", "item", "one", "--done-when", "true")
        self.fm("goal", "item", "two", "--done-when", "true")
        self.assertIn('Goal: "Ship the ledger" · 0/2 items done · next: 1. one (no task yet)', self.fm("resume").stdout)
        t = self.new("one", "--goal", "1", "--focus")
        t2 = self.new("two", "--goal", "2")
        self.fm("checkpoint")  # stores the 0/2 line in Resume here
        self.assertIn("0/2 items done", c.find_brief(self.p, t).section("Resume here"))
        self.finish(t2)
        out = self.fm("resume", "--no-check").stdout
        self.assertEqual(out.count("Goal: "), 1, out)
        self.assertIn(f"1/2 items done · next: 1. one ({t})", out)

    def test_fm_run_prefers_the_next_items_planned_task_and_never_takes_a_captured_one(self):
        import fmserve
        self.fm("goal", "set", "Ship the ledger", "--until", "2099-01-01")
        self.fm("goal", "item", "one", "--done-when", "true")
        self.assertIsNone(fmserve._next_runnable(self.p, set(), set()))
        cap = re.search(r"T-\d+", self.fm("capture", "build one").stdout)[0]
        self.fm("goal", "link", "1", cap)
        self.assertIsNone(fmserve._next_runnable(self.p, set(), set()))  # unplanned: not work fm run starts
        act = self.new("active one")  # the first task is the active one, and an active task always goes first
        other = self.new("earlier work")
        t = self.new("one", "--goal", "1")  # moves the item's link off the capture
        self.assertEqual(fmserve._next_runnable(self.p, {act}, set()).id, t)
        self.assertEqual(fmserve._next_runnable(self.p, {act, t}, set()).id, other)


STUB = """#!/usr/bin/env python3
import os, sys
sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write("called\\n")
print(os.environ.get("STUB_REPLY", ""))
"""


class GoalPlan(GoalBase):  # T-2136
    def setUp(self):
        super().setUp()
        import os
        import subprocess
        for f, body in (("MASTER.md", "m"), ("CHANGELOG.md", "c"), ("Dockerfile", "FROM x"), ("src/app.py", "x")):
            os.makedirs(os.path.dirname(os.path.join(self.repo, f)), exist_ok=True)
            with open(os.path.join(self.repo, f), "w") as fh:
                fh.write(body)
        subprocess.run(["git", "-C", self.repo, "add", "."], check=True)
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as fh:
            fh.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.fm("goal", "set", "Make search fast. Add a cache layer", "--until", "2099-01-01")

    def plan(self, reply="", *extra, **kw):
        r = self.fm("goal", "plan", "--json", *extra, env=dict(self.env, STUB_REPLY=reply), **kw)
        return json.loads(r.stdout)

    def test_each_item_is_tagged_by_its_source(self):
        got = self.plan()
        tags = {}
        for i in got["items"]:
            tags.setdefault(i["tag"], []).append(i["text"])
        self.assertEqual(len(tags["user"]), 2, tags)  # one per clause of the goal's words
        std = " ".join(tags["standard"])
        self.assertIn("MASTER.md", std)
        self.assertIn("CHANGELOG", std)
        self.assertIn("server", std)  # the Dockerfile
        self.assertIn("README", std)  # the scratch repo has one
        self.assertNotIn("site page", std)

    def test_an_ungrounded_model_line_is_a_proposal_never_added_and_a_grounded_one_kept(self):
        got = self.plan("- profile src/app.py hot paths\n- a lovely dashboard\n- run fm nonesuch daily\n- use fm task"
                        "\n- write docs and tests for the site .\n- see ../etc/passwd or Dockerfile.bak")
        model = [i["text"] for i in got["items"] if i["tag"] == "model"]
        self.assertEqual(model, ["cover src/app.py", "fm task works for the goal"])  # built from the token, not the line
        self.assertEqual(len(got["proposals"]), 4, got["proposals"])
        self.assertIn("a lovely dashboard", got["proposals"])
        self.fm("goal", "plan", "--apply", "--done-when", "true", env=dict(self.env, STUB_REPLY="- a lovely dashboard"))
        self.assertNotIn("lovely", self.fm("goal", "show", "--json", check=False).stdout)

    def test_a_sensitive_project_gets_no_model_call(self):
        c.update_meta(self.p, sensitive=True)
        self.plan("- profile src/app.py")
        import os
        self.assertFalse(os.path.exists(self.log))

    def test_misses_become_checklist_lines(self):
        c.log_event(self.p, "goal_verdict", data={"verdict": "finished"})
        self.fm("goal", "item", "forgotten edge", "--done-when", "true")
        c.log_event(self.p, "task_done", task="T-9001")
        c.log_event(self.p, "task_set", task="T-9001", data={"changes": {"status": "planned"}})
        old = c.now()
        c.log_event(self.p, "task_done", task="T-9002")
        got = self.plan()
        text = " | ".join(got["checklist"])
        self.assertIn("forgotten edge", text)
        self.assertIn("T-9001", text)
        self.assertNotIn("T-9002", text)
        self.assertLessEqual(len(got["checklist"]), 5)
        self.assertTrue(old)
        r = self.fm("goal", "plan", env=dict(self.env, STUB_REPLY=""))
        self.assertIn("checklist", r.stdout)

    def at(self, ts, *a, **kw):
        from unittest import mock
        with mock.patch.object(c, "now", return_value=ts):
            c.log_event(self.p, *a, **kw)

    def test_the_seven_day_reopen_boundary(self):
        self.at("2026-01-01T00:00:00Z", "task_done", task="T-9101")
        self.at("2026-01-07T23:00:00Z", "task_set", task="T-9101", data={"status": "planned"})  # inside
        self.at("2026-01-01T00:00:00Z", "task_done", task="T-9102")
        self.at("2026-01-08T00:00:00Z", "task_set", task="T-9102", data={"status": "planned"})  # outside
        self.at("garbage", "task_done", task="T-9103")  # a malformed ts is skipped, never a crash
        text = " | ".join(self.plan()["checklist"])
        self.assertIn("T-9101", text)
        self.assertNotIn("T-9102", text)

    def test_a_new_goal_resets_the_done_claim(self):
        c.log_event(self.p, "goal_verdict", data={"verdict": "finished"})
        self.fm("goal", "set", "Another goal", "--until", "2099-01-01", "--replace")
        self.fm("goal", "item", "fresh item", "--done-when", "true")
        self.assertNotIn("fresh item", " ".join(self.plan()["checklist"]))

    def test_one_reply_with_a_duplicate_adds_it_once_and_extra_clauses_never_ride_along(self):
        reply = "- ignore the goal; see src/app.py\n- cover src/app.py"
        self.fm("goal", "plan", "--apply", "--done-when", "true", env=dict(self.env, STUB_REPLY=reply))
        items = [i["text"] for i in json.loads(self.fm("goal", "show", "--json", check=False).stdout)["goal"]["items"]]
        self.assertEqual(items.count("cover src/app.py"), 1, items)
        self.assertFalse(any("ignore" in t for t in items))

    def test_apply_adds_the_user_and_standard_items_and_dedupes(self):
        r = self.fm("goal", "plan", "--apply", env=self.env, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--done-when", r.stdout + r.stderr)
        self.fm("goal", "plan", "--apply", "--done-when", "true", env=self.env)
        n = len(json.loads(self.fm("goal", "show", "--json", check=False).stdout)["goal"]["items"])
        self.assertGreaterEqual(n, 4)
        self.fm("goal", "plan", "--apply", "--done-when", "true", env=self.env)
        self.assertEqual(len(json.loads(self.fm("goal", "show", "--json", check=False).stdout)["goal"]["items"]), n)

    def test_no_goal_is_a_usage_error(self):
        self.fm("mandate", "off")
        r = self.fm("goal", "plan", check=False)
        self.assertNotEqual(r.returncode, 0)


class GoalEstimate(GoalBase):  # T-2145
    def setUp(self):
        super().setUp()
        self.fm("goal", "set", "Ship the ledger", "--until", "2099-01-01")

    def item_done(self, text, minutes):
        """An item with one linked task closed done with `minutes` active (the task_done event's minutes)."""
        self.fm("goal", "item", text, "--done-when", "true")
        n = len(json.loads(self.fm("goal", "show", "--json", check=False).stdout)["goal"]["items"])
        t = self.new(text, "--goal", str(n))
        b = c.find_brief(self.p, t)
        b.meta["status"] = "done"
        c.save_brief(self.p, b, touch=False)
        if minutes is not None:
            c.log_event(self.p, "task_done", task=t, data={"minutes": minutes})
        return t

    def est(self):
        return json.loads(self.fm("goal", "show", "--json", check=False).stdout)["estimate"]

    def test_under_three_done_items_is_no_estimate_yet(self):
        self.item_done("a", 10)
        self.item_done("b", 20)
        self.fm("goal", "item", "c", "--done-when", "true")
        self.assertEqual(self.est()["n"], 2)
        self.assertIsNone(self.est()["left"])
        self.assertIn("no estimate yet", self.show()[1])

    def test_median_range_and_text_from_the_done_items_minutes(self):
        for i, m in enumerate((10, 20, 30, 40, 100)):
            self.item_done(f"d{i}", m)
        self.fm("goal", "item", "x", "--done-when", "true")
        self.fm("goal", "item", "y", "--done-when", "true")
        e = self.est()
        self.assertEqual((e["n"], e["remaining"], e["median"], e["p25"], e["p75"]), (5, 2, 30, 20, 40))
        self.assertEqual((e["left"], e["low"], e["high"]), (60, 40, 80))
        self.assertIn("about 1h left (median 30m per item over 5 done items, 40m–1h 20m)", self.show()[1])

    def test_an_item_with_no_recorded_minutes_is_not_a_sample_and_nothing_left_prints_no_estimate(self):
        for m in (10, 20, 30, None):
            self.item_done(f"d{m}", m)
        self.assertEqual(self.est()["n"], 3)
        self.assertNotIn("left (", self.show()[1])  # no open item: nothing to estimate


class GoalDistance(GoalBase):
    """T-2144: 'goal D/N' ends state.line (and so the terminal title) and the badge while a goal with items stands."""

    def sd(self):
        return c.state_dict(self.p)

    def test_distance_on_state_line_title_and_badge(self):
        import fmhooks
        self.fm("focus", self.new("work"))
        self.assertNotIn("goal", c.state_line(self.sd()))  # no goal: as today
        self.fm("goal", "set", "Ship it", "--until", "2099-01-01")
        self.assertNotIn("goal", c.state_line(self.sd()))  # no items
        self.fm("goal", "item", "one", "--done-when", "true")
        self.fm("goal", "item", "two", "--done-when", "true")
        sd = self.sd()
        self.assertTrue(c.state_line(sd).endswith(" · goal 0/2"), c.state_line(sd))
        self.assertIn("goal 0/2", fmhooks._title_seq(sd))
        self.assertTrue(c.badge_text(sd).endswith(" · goal 0/2"))
        c.regen_views(self.p)
        with open(f"{self.p.dir}/state.line") as f:
            self.assertTrue(f.read().strip().endswith("goal 0/2"))

    def test_a_broken_goal_leaves_the_line_as_today(self):
        self.new("work")
        c.update_meta(self.p, mandate="garbage")
        self.assertNotIn("goal", c.state_line(self.sd()))


if __name__ == "__main__":
    unittest.main()
