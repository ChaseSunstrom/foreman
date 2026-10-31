"""T-1057: the forever loop. With fm loop on, an empty queue starts an improvement round on its own (fm next names it,
the Stop drive continues into it); a round's brief says what shipped since the last one and runs a brainstorm past every
earlier one; two dry rounds in a row end the loop with a recorded decision."""
import json
import os
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c


def parse(proc):
    out = proc.stdout.strip()
    return json.loads(out) if out.startswith("{") else None


class Loop(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def stop(self, msg="Done."):
        return parse(self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": msg, "session_id": "sess-1"})) or {}

    def project_dir(self):
        return c.find_project(self.repo).dir

    def test_on_off_and_an_empty_queue_names_the_round(self):
        self.assertIn("off", self.fm("loop").stdout)
        self.assertIn("queue is empty", self.fm("next").stdout)
        self.fm("loop", "on")
        self.assertIn("on", self.fm("loop").stdout)
        nxt = self.fm("next").stdout
        self.assertIn("forever loop round 1", nxt)
        self.assertIn("fm loop round", nxt)
        tid = json.loads(self.fm("task", "new", "Real work", "--type", "FIX", "--tier", "S", "--json").stdout)["id"]
        self.assertNotIn("forever loop", self.fm("next").stdout, "queued work comes first")
        self.fm("task", "drop", tid, "test")
        self.fm("loop", "off")
        self.assertIn("queue is empty", self.fm("next").stdout)

    def test_a_round_brief_says_what_shipped_and_runs_past_earlier_brainstorms(self):
        d = os.path.join(self.project_dir(), "research", "brainstorm-20260101-000000")
        os.makedirs(d)
        with open(os.path.join(d, "ideas.md"), "w", encoding="utf-8") as f:
            f.write("# Ideas\n- an old idea\n")
        self.fm("loop", "on")  # the round reports what shipped since the loop began
        tid = self.fm_json("task", "new", "Shipped thing", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true",
                           "--step", "a")["id"]
        self.fm("focus", tid)
        self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        brief = self.fm("loop", "round").stdout
        self.assertIn("round 1", brief)
        self.assertIn("Shipped thing", brief)  # what shipped since the loop started
        self.assertIn("fm ideas", brief)
        self.assertIn(os.path.join(d, "ideas.md"), brief)  # --seen every earlier run
        self.assertIn("fm loop yield", brief)
        self.assertIn("forever loop round 2", self.fm("next").stdout)

    def test_a_round_ahead_of_pace_drops_the_ideas_fan_out(self):
        # T-1966: the brief sent the model to fm ideas while usage was ahead of pace and its lens subagents waited
        from unittest import mock
        import fmloop
        self.fm("loop", "on")
        p = c.find_project(self.repo)
        with mock.patch("fmbudget.degrade", return_value=None):
            self.assertIn("fm ideas --pack", fmloop.round_brief(p))
        with mock.patch("fmbudget.degrade", return_value="weekly usage 80%"):
            brief = fmloop.round_brief(p)
        self.assertNotIn("fm ideas", brief)
        self.assertIn("Optional work is dropped (weekly usage 80%)", brief)  # or the spent risk budget: not usage
        self.assertIn("isn't counted dry", brief)  # T-1990: T-1986's rule, said where the yield is asked for

    def test_a_main_thread_round_names_the_lenses_to_sweep(self):
        # T-2004: "review what shipped" alone shrank rounds to 1-3 follow-ups and the user asked for breadth again
        from unittest import mock
        import fmloop
        self.fm("loop", "on")
        with mock.patch("fmbudget.degrade", return_value="weekly usage 80%"):
            brief = fmloop.round_brief(c.find_project(self.repo))
        self.assertIn("one grounded idea per lens", brief)
        for lens in fmloop.MAIN_LENSES:
            self.assertIn(lens, brief)

    def test_a_round_lists_what_recent_work_left_behind_learned_from_history(self):
        # T-2073: the user had to ask for the site, skills and playbooks to catch up; no folder list, the repo's own
        # history says what usually moves with what
        import subprocess
        import fmloop

        def commit(files, msg):
            for path, text in files.items():
                os.makedirs(os.path.dirname(os.path.join(self.repo, path)) or self.repo, exist_ok=True)
                with open(os.path.join(self.repo, path), "a", encoding="utf-8") as f:
                    f.write(text)
            subprocess.run(["git", "-C", self.repo, "add", *files], check=True)
            subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)
        hub = {"CHANGELOG.md": "- x\n"}  # in every commit: its weak links must never add up to "owed"
        for i in range(3):
            commit({**hub, "old.txt": f"{i}\n"}, f"old {i}")
        for i in range(4):
            commit({**hub, "lib.py": f"x{i} = 1\n", "site/page.html": f"<p>{i}</p>\n"}, f"both {i}")
        p = c.find_project(self.repo)
        self.assertEqual(fmloop.lag(p), [], "everything that moves together just moved")
        for i in range(4):  # the page now moves with the code half the time, and missed the last 4
            commit({**hub, "lib.py": f"y{i} = 1\n"}, f"code {i}")
        left = fmloop.lag(p)
        self.assertEqual(left, ["- site/page.html: owes ~2.0 updates (lib.py changed in 4 commits since it last did; "
                                "they move together 50% of the time)"])  # old.txt: 27% with the hub, 8 commits: noise
        self.fm("loop", "on")
        brief = fmloop.round_brief(p)
        self.assertIn("- site/page.html: owes", brief)
        self.assertIn("Surfaces: every area of this repo (CHANGELOG.md, README.md, lib.py, old.txt, site)", brief)
        os.rename(os.path.join(self.repo, ".git"), os.path.join(self.repo, "git-gone"))
        self.assertIsNone(fmloop.lag(p))  # no history is unknown, never "nothing owed"

    def test_a_round_lists_the_asks_no_brainstorm_predicted(self):
        # T-2076: the round brief carries the brainstorms' misses, so the main thread asks what would have caught them
        import re
        import fmloop
        p = c.find_project(self.repo)
        d = os.path.join(p.dir, "research", "brainstorm-20250101-000000")
        os.makedirs(d)
        with open(os.path.join(d, "ideas.json"), "w") as f:
            json.dump({"lenses": {"user value": ["Speed up the parser"]}, "created": "2025-01-01T00:00:00Z"}, f)
        out = self.fm("capture", "Add more playbooks for every stage", "--source", "user").stdout
        tid = re.search(r"T-\d+", out).group(0)
        self.fm("loop", "on")
        brief = fmloop.round_brief(p)
        self.assertIn("Asks no brainstorm predicted", brief)
        self.assertIn(f"- {tid}: Add more playbooks for every stage", brief)

    def test_a_budget_limited_round_leaves_the_dry_streak_alone(self):
        # T-1986: with optional work dropped there is no ideas fan-out; a spent budget ended the loop as "2 dry rounds"
        from unittest import mock
        import fmloop
        self.fm("loop", "on")
        p = c.find_project(self.repo)
        with mock.patch("fmbudget.degrade", return_value="today's risk budget is spent"):
            for _ in range(3):
                s, stop = fmloop.record_yield(p, 1)
        self.assertFalse(stop)
        self.assertEqual(s["dry"], 0)
        self.assertTrue(s["limited"])
        self.assertIn("on", self.fm("loop").stdout)

    def test_two_dry_rounds_end_the_loop_with_a_decision(self):
        self.fm("loop", "on")
        self.fm("loop", "round")
        self.fm("loop", "yield", "1")
        self.assertIn("on", self.fm("loop").stdout, "one dry round is not the end")
        self.fm("loop", "round")
        self.fm("loop", "yield", "6")  # a fruitful round resets the count
        self.fm("loop", "round")
        self.fm("loop", "yield", "0")
        self.fm("loop", "round")
        out = self.fm("loop", "yield", "2").stdout
        self.assertIn("off", out)
        self.assertIn("off", self.fm("loop").stdout)
        self.assertIn("forever loop", self.fm("decide", "--list").stdout)
        self.assertIn("queue is empty", self.fm("next").stdout)

    def test_the_loop_says_what_it_shipped(self):
        # T-2011: a loop that ran for days ended with only its round number; how much it got done went unsaid
        self.fm("loop", "on")
        p = c.find_project(self.repo)
        s = c.read_meta(p)["loop"]
        c.update_meta(p, loop=dict(s, started=c.iso(time.time() - 7200)))  # clear of the clock's second
        with open(os.path.join(p.dir, "ledger.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(time.time() - 3600), "event": "task_done", "task": "T-0001"}) + "\n")
        self.fm("loop", "round")
        self.fm("loop", "yield", "0")
        self.assertIn("1 round, 1 task closed since", self.fm("loop").stdout)
        self.fm("loop", "round")
        self.fm("loop", "yield", "1")
        self.assertIn("2 rounds, 1 task closed since", self.fm("decide", "--list").stdout)
        self.fm("loop", "on")
        self.assertIn("0 rounds, 0 tasks closed since", self.fm("loop", "off").stdout, "a new run counts afresh")

    def test_the_drive_continues_into_each_round(self):
        self.fm("autonomy", "full")
        self.assertNotIn("fm loop round", self.stop().get("reason", ""))
        self.fm("loop", "on")
        r = self.stop()
        self.assertEqual(r.get("decision"), "block")
        self.assertIn("fm loop round", r["reason"])
        self.assertEqual(self.stop().get("decision"), None, "a round not started yet is pushed once, not fifty times")
        self.fm("loop", "round")
        self.assertEqual(self.stop().get("decision"), "block", "the next round is pushed after this one ran")

    def test_fm_ui_carries_the_loop(self):
        self.fm("loop", "on")
        self.fm("loop", "round")
        v = self.fm_json("ui")
        self.assertEqual(v["loop"]["on"], True)
        self.assertEqual(v["loop"]["round"], 1)


if __name__ == "__main__":
    unittest.main()


class LagKept(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def test_a_decision_naming_a_lagging_file_mutes_it_until_the_file_changes(self):
        # T-2075: a file fm decide kept (why it stays) was listed again every round
        import subprocess
        from unittest import mock
        import fmloop

        def commit(path, date):
            with open(os.path.join(self.repo, path), "a", encoding="utf-8") as f:
                f.write(date + "\n")
            subprocess.run(["git", "-C", self.repo, "add", path], check=True)
            subprocess.run(["git", "-C", self.repo, "commit", "-qm", "c"], check=True,
                           env={**os.environ, "GIT_COMMITTER_DATE": date + "T12:00:00", "GIT_AUTHOR_DATE": date + "T12:00:00"})
        commit("page.html", "2026-01-01")
        commit("data.py", "2026-01-01")
        p = c.find_project(self.repo)
        drift = [("page.html", 2.0, "lib.py", 4, 0.5), ("data.py", 2.0, "lib.py", 4, 0.5)]
        with mock.patch("fmmap.drift", return_value=drift):
            self.assertEqual(len(fmloop.lag(p)), 2)
            with open(os.path.join(p.dir, "decisions.md"), "a", encoding="utf-8") as f:
                f.write("| 2026-01-02 | [x] page.html stays: nothing in it changes with lib.py | why |\n")
            left = fmloop.lag(p)  # "a.py" must not match inside "data.py", nor "page.html" inside "mypage.html"
            self.assertEqual([x.split(":")[0] for x in left], ["- data.py"])
            commit("page.html", "2026-02-01")  # changed after the decision: listed again
            self.assertEqual(len(fmloop.lag(p)), 2)


class LoopReview(ForemanTestCase):
    """T-1057 review: the dry stop is Foreman's, not the model's memory; a yield counts once; a new round is progress."""
    def setUp(self):
        super().setUp()
        self.fm("init")

    def test_a_round_left_without_a_yield_counts_the_tasks_it_queued(self):
        self.fm("loop", "on")
        self.fm("loop", "round")
        self.assertIn("fm loop round --next", self.fm("next").stdout, "a drained open round is ended with --next")
        self.fm("loop", "round", "--next")  # nothing queued in round 1 and no yield: dry, counted by Foreman
        self.assertIn("1 dry", self.fm("loop").stdout)
        self.fm("loop", "round", "--next")  # round 2: dry again, so the loop ends
        self.assertIn("off", self.fm("loop").stdout)

    def test_reading_the_open_round_again_does_not_advance_it(self):
        # T-1153: a second fm loop round mid-round (re-reading the brief) counted round 1 dry and started round 2
        self.fm("loop", "on")
        self.fm("loop", "round")
        again = self.fm("loop", "round").stdout
        self.assertIn("round 1", again)
        self.assertIn("fm loop yield", again)
        out = self.fm("loop").stdout
        self.assertIn("round 1", out)
        self.assertNotIn("dry", out)
        self.fm("loop", "yield", "5")
        self.fm("loop", "round")  # a recorded yield closes the round: the next call starts round 2
        self.assertIn("round 2", self.fm("loop").stdout)

    def test_tasks_captured_during_a_round_are_its_yield(self):
        self.fm("loop", "on")
        self.fm("loop", "round")
        for i in range(4):
            self.fm("capture", f"idea {i}", "--source", "self")
        self.fm("loop", "round", "--next")
        out = self.fm("loop").stdout
        self.assertNotIn("dry", out)
        self.assertIn("round 2", out)

    def test_a_round_takes_one_yield(self):
        self.fm("loop", "on")
        self.fm("loop", "round")
        self.fm("loop", "yield", "0")
        self.assertNotEqual(self.fm("loop", "yield", "0", check=False).returncode, 0, "a second yield for one round")
        self.assertIn("on", self.fm("loop").stdout)

    def test_yield_before_any_round_is_refused(self):
        self.fm("loop", "on")
        self.assertNotEqual(self.fm("loop", "yield", "4", check=False).returncode, 0)

    def test_a_new_round_resets_the_drive_cap(self):
        self.fm("autonomy", "full")
        self.fm("loop", "on")
        gate = os.path.join(c.find_project(self.repo).dir, "gate.json")
        parse(self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "x", "session_id": "sess-1"}))
        with open(gate) as f:
            g = json.load(f)
        g["drive"]["sess-1"]["count"] = 49
        with open(gate, "w") as f:
            json.dump(g, f)
        self.fm("loop", "round")
        r = parse(self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "x", "session_id": "sess-1"})) or {}
        self.assertEqual(r.get("decision"), "block")
        with open(gate) as f:
            self.assertLess(json.load(f)["drive"]["sess-1"]["count"], 5, "a round started is progress, not a spin")

    def test_round_brief_quotes_seen_paths_and_survives_a_missing_git(self):
        d = os.path.join(c.find_project(self.repo).dir, "research", "brainstorm-1 x")
        os.makedirs(d)
        with open(os.path.join(d, "ideas.md"), "w", encoding="utf-8") as f:
            f.write("- an idea\n")
        self.fm("loop", "on")
        self.fm("loop", "round")
        out = self.fm("loop", "round", env={"PATH": "/nonexistent"}).stdout
        self.assertIn("'", out.split("--seen", 1)[1].split("\n", 1)[0])  # the path with a space is quoted
