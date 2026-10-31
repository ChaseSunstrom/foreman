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
        got = json.loads(self.fm("goal", "show", "--json").stdout)
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


if __name__ == "__main__":
    unittest.main()
