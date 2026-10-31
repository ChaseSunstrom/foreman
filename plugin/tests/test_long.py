"""fm exam long (T-2258): goals replayed from a local repo's task changes, hidden checks from what shipped."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmprove

TEST = ("import unittest\nimport app\n\n\nclass T(unittest.TestCase):\n"
        "    def test_old(self):\n        self.assertEqual(app.old(), 0)\n{extra}")
APP = "def old():\n    return 0\n"


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


class Long(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.src = os.path.join(self.tmp, "src")
        subprocess.run(["git", "init", "-q", "-b", "main", self.src], check=True)
        for k, v in (("user.email", "t@example.com"), ("user.name", "t")):
            subprocess.run(["git", "-C", self.src, "config", k, v], check=True)
        write(self.src, "app.py", APP)
        write(self.src, "tests/test_app.py", TEST.format(extra=""))
        self.commit("init")
        app, tests = APP, TEST.format(extra="")
        for n, passes_at_base in ((1, False), (2, True), (3, False)):
            app += f"\n\ndef f{n}():\n    return {n}\n"
            body = f"    def test_f{n}(self):\n        self.assertEqual(app.f{n}(), {n})\n"
            if passes_at_base:  # a check that already passes at the base: the window must be dropped
                body = f"    def test_f{n}(self):\n        self.assertEqual(app.old(), 0)\n"
            tests += "\n" + body
            write(self.src, "app.py", app)
            write(self.src, "tests/test_app.py", tests)
            self.commit(f"Add f{n} (T-100{n})")

    def commit(self, msg):
        subprocess.run(["git", "-C", self.src, "add", "."], check=True)
        subprocess.run(["git", "-C", self.src, "commit", "-qm", msg], check=True)

    def gen(self, trust=True):
        if trust:
            fmprove.remember(self.src)
        return self.fm("exam", "long", "gen", "--from", self.src, "--json", check=trust)

    def test_gen_keeps_only_red_at_base_green_at_target_with_no_future_history(self):
        r = json.loads(self.gen().stdout)
        self.assertEqual(sorted(s["id"] for s in r["scenarios"]), ["T-1001", "T-1003"])  # T-1002's check passes at base
        for s in r["scenarios"]:
            repo = s["repo"]
            self.assertEqual(subprocess.run(["git", "-C", repo, "rev-list", "--count", "HEAD"], capture_output=True,
                                            text=True).stdout.strip(), "1")
            key = json.load(open(os.path.join(os.path.dirname(repo), "key.json")))
            self.assertFalse(os.path.exists(os.path.join(repo, "key.json")))
            self.assertEqual(len(key["checks"]), 1)
            self.assertIn("test_app.T.test_f" + s["id"][-1], key["checks"][0])
            self.assertNotIn("def f1", open(os.path.join(repo, "app.py")).read()) if s["id"] == "T-1001" else None
        later = [s for s in r["scenarios"] if s["id"] == "T-1003"][0]["repo"]
        self.assertIn("def f2", open(os.path.join(later, "app.py")).read())  # base of T-1003 holds the earlier work
        self.assertNotIn("def f3", open(os.path.join(later, "app.py")).read())  # but never its own or later work

    def test_oracle_scores_true_done_and_empty_does_not_and_the_line_is_tier_long(self):
        run = json.loads(self.gen().stdout)["run"]
        for agent, done in (("oracle", 2), ("empty", 0)):
            self.fm("exam", "long", "run", run, "--agent", agent)
            g = json.loads(self.fm("exam", "long", "grade", run, "--agent", agent, "--json").stdout)
            self.assertEqual(g["true_done"], done, g)
            self.assertEqual(g["regressions"], 0, g)
        long = [x for x in self.lines() if x.get("tier") == "long"]
        self.assertEqual([(x["agent"], x["true_done"], x["model"]) for x in long], [("oracle", 2, None), ("empty", 0, None)])  # zero-token arms: no model

    def lines(self):
        import fmcore as c
        import fmgenesis
        p = c.find_project(self.repo)
        with open(os.path.join(fmgenesis.home(p), "exam.jsonl")) as f:
            return [json.loads(x) for x in f.read().splitlines()]

    def test_an_untrusted_source_runs_none_of_its_code(self):
        ran = os.path.join(self.tmp, "ran")
        write(self.src, "tests/test_evil.py", f"open({ran!r}, 'w').write('x')\n")
        self.commit("evil")
        r = self.gen(trust=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fm prove", r.stderr)
        self.assertFalse(os.path.exists(ran))

    def work(self, run, agent, sid="T-1001"):
        import fmcore as c
        import fmlong
        return os.path.join(fmlong._root(c.find_project(self.repo)), run, "work", agent, sid)

    def grade(self, run, agent):
        return json.loads(self.fm("exam", "long", "grade", run, "--agent", agent, "--json").stdout)

    def test_an_answer_cannot_shadow_the_stdlib_or_stand_in_for_a_hidden_test(self):
        run = json.loads(self.gen().stdout)["run"]
        self.fm("exam", "long", "run", run, "--agent", "empty")
        w = self.work(run, "empty")
        write(w, "unittest.py", "raise SystemExit(0)\n")  # would end any run that imports it first
        write(w, "test_app.py", "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_f1(self):\n        pass\n")
        self.assertEqual(self.grade(run, "empty")["true_done"], 0)

    def test_a_break_is_a_regression_and_every_goal_counts_in_the_total(self):
        run = json.loads(self.gen().stdout)["run"]
        self.fm("exam", "long", "run", run, "--agent", "oracle")
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.work(run, "oracle")))), "T-1003", "key.json")) as f:
            self.assertTrue(json.load(f)["sample"])
        self.assertEqual(self.grade(run, "oracle")["regressions"], 0)  # by construction
        f = os.path.join(self.work(run, "oracle"), "app.py")
        text = open(f).read()
        with open(f, "w") as fh:
            fh.write(text.replace("return 0", "return 9"))
        g = self.grade(run, "oracle")
        self.assertTrue(g["regressions"] >= 1 and g["true_done"] == 2, g)
        os.rename(self.work(run, "oracle", "T-1003"),os.path.join(self.tmp, "gone"))  # one unanswered
        g = self.grade(run, "oracle")
        self.assertEqual((g["scenarios"], g["true_done"]), (2, 1), g)  # the unanswered goal is in the 2, not in the 1

    def test_grade_rechecks_trust(self):
        import fmcore as c
        run = json.loads(self.gen().stdout)["run"]
        self.fm("exam", "long", "run", run, "--agent", "oracle")
        os.remove(os.path.join(c.state_dir(), "prove-trusted.json"))
        r = self.fm("exam", "long", "grade", run, "--agent", "oracle", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fm prove", r.stderr)

    def test_a_runner_timeout_is_none_not_all_red_and_a_forged_key_is_refused(self):
        import fmlong
        t = os.path.join(self.tmp, "slow")
        write(t, "tests/test_s.py", "import time, unittest\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        time.sleep(30)\n")
        old, fmlong.RUN_T = fmlong.RUN_T, 1
        try:
            self.assertIsNone(fmlong._passed(t, ["tests/test_s.py::test_s.T.test_a"], ["tests"]))
        finally:
            fmlong.RUN_T = old
        key = {"id": "x", "checks": ["../x.py::a.B.c"], "sample": [], "files": [], "test_files": [], "pypath": [],
               "base": "0" * 40, "target": "0" * 40}
        with self.assertRaises(ValueError):
            fmlong._check_key(key)
        with self.assertRaises(ValueError):
            fmlong._check_key(dict(key, checks=[], target="--output=x"))

    def test_n_zero_and_a_gen_that_keeps_nothing_fail_without_a_run(self):
        fmprove.remember(self.src)
        self.assertNotEqual(self.fm("exam", "long", "gen", "--from", self.src, "--n", "0", check=False).returncode, 0)
        empty = os.path.join(self.tmp, "empty")
        subprocess.run(["git", "init", "-q", "-b", "main", empty], check=True)
        fmprove.remember(empty)
        r = self.fm("exam", "long", "gen", "--from", empty, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.gen().returncode, 0)
        import fmcore as c
        import fmlong
        self.assertEqual(os.listdir(fmlong._root(c.find_project(self.repo))), ["l001"])

    # T-2262: the foreman and plain session arms and the faults planted in a long run, against a stub claude
    def stub(self):
        import fmcore as c
        import fmlong
        from unittest import mock
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        write(bindir, "claude", STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.cfg = os.path.join(self.tmp, "cfg")  # claude's config dir: a test never touches the real ~/.claude
        patch = mock.patch.dict(os.environ, {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log,
                                             "CLAUDE_CONFIG_DIR": self.cfg})
        patch.start()
        self.addCleanup(patch.stop)
        for k, v in (("KILL_T", 0.02), ("PAUSE_GAP", 0)):
            old = getattr(fmlong, k)
            setattr(fmlong, k, v)
            self.addCleanup(setattr, fmlong, k, old)
        self.p, self.fmlong = c.find_project(self.repo), fmlong
        self.run_id = json.loads(self.gen().stdout)["run"]

    def calls(self):
        with open(self.log) as f:
            return [json.loads(x) for x in f]

    def go(self, agent, faults=(), **kw):
        return self.fmlong.run(self.p, self.run_id, agent, faults=faults, **kw)

    def faults(self, agent, sid="T-1001"):
        with open(os.path.join(self.fmlong._root(self.p), self.run_id, "faults", agent, sid + ".json")) as f:
            return json.load(f)

    def test_plain_gets_no_plugin_and_foreman_gets_it_and_both_get_the_goal_and_model(self):
        self.stub()
        for agent, plugin in (("plain", False), ("foreman", True)):
            open(self.log, "w").close()
            r = self.go(agent, model="sonnet")
            self.assertEqual(sorted(r["answered"]), ["T-1001", "T-1003"])
            calls = self.calls()
            self.assertEqual([x["plugin"] for x in calls], [plugin] * 2, agent)
            self.assertTrue(all(x["model"] == "sonnet" and "Add f" in x["prompt"] for x in calls))
            self.assertEqual(self.faults(agent), [])
            self.assertTrue(os.path.isdir(self.fmlong._work(self.p, self.run_id, agent, "T-1001")))
        self.assertIsNone(calls[0]["quiet"])  # foreman's session keeps Foreman's brief rule
        g = self.fmlong.grade(self.p, self.run_id, "plain")  # a stub changes nothing: graded, none done, stamped with its model
        self.assertEqual((g["true_done"], g["model"]), (0, "sonnet"))

    def test_kill_stops_the_session_midway_then_resumes_it_and_logs_both(self):
        import time
        self.stub()
        os.environ["STUB_HANG"] = "1"
        self.addCleanup(os.environ.pop, "STUB_HANG", None)
        t = time.time()
        self.go("plain", ("kill",))
        self.assertLess(time.time() - t, 20)  # the hung first turn was killed, not waited out
        a, b = self.calls()[:2]
        self.assertEqual((a["resume"], b["resume"]), (None, a["sid"]))
        (k,) = self.faults("plain")
        self.assertEqual((k["kind"], k["fired"], k["resumed"], k["resume_ok"]), ("kill", True, True, True))
        self.assertIn("at", k)

    def test_a_kill_that_never_fires_is_logged_unfired_with_no_resume(self):
        self.stub()
        self.go("plain", ("kill",))
        self.assertEqual(len(self.calls()), 2)  # one turn a goal
        self.assertEqual([(k["kind"], k["fired"], k["resumed"]) for k in self.faults("plain")], [("kill", False, False)])

    def test_pause_waits_a_logged_gap_then_resumes_after_a_stop_at_a_checkpoint(self):
        self.stub()
        self.fmlong.PAUSE_GAP = 0.2
        self.go("foreman", ("pause",))
        a, b = self.calls()[:2]
        self.assertIn("stop", a["prompt"].lower())
        self.assertEqual(b["resume"], a["sid"])
        (k,) = self.faults("foreman")
        self.assertEqual((k["kind"], k["gap_s"], k["resumed"], k["resume_ok"]), ("pause", 0.2, True, True))

    def test_compaction_forces_a_small_window_and_logs_how_many_happened(self):
        self.stub()
        self.go("plain", ("compaction",))
        self.assertEqual(self.calls()[0]["window"], str(self.fmlong.COMPACT_AT))
        (k,) = self.faults("plain")
        self.assertEqual((k["kind"], k["compactions"], k["ok"]), ("compaction", 0, False))  # the stub never compacts

    def test_misleading_plants_a_wrong_test_the_session_sees_and_the_key_never_names(self):
        self.stub()
        self.go("plain", ("misleading",))
        self.assertTrue(all(x["planted"] == ["test_planted_old_behaviour.py"] for x in self.calls()))
        (k,) = self.faults("plain")
        self.assertEqual((k["kind"], k["file"]), ("misleading", "tests/test_planted_old_behaviour.py"))
        self.assertTrue(k["kept"])
        base = os.path.join(self.fmlong._root(self.p), self.run_id, "T-1001")
        with open(os.path.join(base, "key.json")) as f:
            self.assertNotIn("planted", f.read())
        self.assertFalse(os.path.exists(os.path.join(base, "repo", k["file"])))  # the base repo stays clean
        g = self.fmlong.grade(self.p, self.run_id, "plain")  # the plant is never one of the checks
        self.assertEqual(g["regressions"], 0)

    def test_all_faults_together_and_a_rerun_starts_clean(self):
        self.stub()
        self.go("plain", ("kill", "pause", "compaction", "misleading"))
        self.assertEqual(sorted(k["kind"] for k in self.faults("plain")), ["compaction", "kill", "misleading", "pause"])
        self.go("plain", ("pause",))
        self.assertEqual([k["kind"] for k in self.faults("plain")], ["pause"])

    def test_grade_reports_false_done_cost_interventions_and_never_records_unknown_as_zero(self):  # T-2263
        self.stub()
        os.environ["STUB_HANG"] = "1"
        self.addCleanup(os.environ.pop, "STUB_HANG", None)
        self.go("plain", ("kill",), limit=2)  # the stub says "done" but writes nothing: hidden checks stay red
        g = self.grade(self.run_id, "plain")
        self.assertEqual((g["true_done"], g["false_done"], g["resumes_needed"], g["unfinished"]), (0, 2, 0, 0), g)
        self.assertEqual(g["cost_unknown"], 2, g)  # a killed turn reports no cost
        self.assertEqual(g["cost"], 0.2)  # only the resumed turns' cost: 2 x 0.1
        self.assertIsNone(g["hours_to_done"])
        self.assertIsNone(g["guard_blocks"])  # the stub leaves no guard events: unknown, not 0
        self.assertTrue(all(x["false_done"] is True and x["cost_unknown"] for x in g["goals"]), g)
        o = self.fmlong.run(self.p, self.run_id, "oracle")
        g = self.grade(self.run_id, "oracle")  # no session ran: nothing to read the claim or cost from
        self.assertEqual(o["agent"], "oracle")
        self.assertEqual((g["true_done"], g["false_done"], g["cost"], g["resumes_needed"], g["unfinished"]), (2, None, None, None, None), g)
        self.assertEqual(g["unknown"]["false_done"], 2, g)

    def test_grade_reads_seeded_metrics_hours_guard_blocks_and_a_false_done(self):  # T-2263
        self.stub()
        self.go("plain", limit=0)  # a stamp only
        self.fmlong.run(self.p, self.run_id, "oracle")
        root = self.fmlong._root(self.p)
        os.makedirs(os.path.join(root, self.run_id, "faults", "oracle"))
        for sid, said, secs in (("T-1001", True, 5400), ("T-1003", True, 60)):
            with open(os.path.join(root, self.run_id, "faults", "oracle", sid + ".run.json"), "w") as f:
                json.dump({"cost": 0.25, "cost_unknown": False, "said_done": said, "secs": secs, "guard_blocks": 2, "ended_ok": True}, f)
        g = self.grade(self.run_id, "oracle")
        self.assertEqual((g["false_done"], g["guard_blocks"], g["cost"], g["hours_to_done"]), (0, 4, 0.5, 0.017), g)
        os.remove(os.path.join(self.work(self.run_id, "oracle", "T-1003"), "app.py"))  # now the second goal fails
        g = self.grade(self.run_id, "oracle")
        self.assertEqual((g["true_done"], g["false_done"], g["hours_to_done"]), (1, 1, 1.5), g)  # the first true-done left standing

    def test_a_session_that_stopped_short_is_unfinished_not_a_human_intervention(self):  # T-2263
        self.stub()
        self.go("plain", limit=0)
        self.fmlong.run(self.p, self.run_id, "oracle")
        root = self.fmlong._root(self.p)
        os.makedirs(os.path.join(root, self.run_id, "faults", "oracle"))
        put = lambda sid, info: json.dump(info, open(os.path.join(root, self.run_id, "faults", "oracle", sid + ".run.json"), "w"))
        put("T-1001", {"said_done": False, "ended_ok": True})  # stopped short: no error, no claim
        put("T-1003", {"said_done": False, "ended_ok": False, "resume_failed": 1})  # an error and a failed resume
        r = self.grade(self.run_id, "oracle")
        g = {x["id"]: x for x in r["goals"]}
        self.assertEqual((g["T-1001"]["resumes_needed"], g["T-1001"]["unfinished"]), (0, 1))
        self.assertEqual((g["T-1003"]["resumes_needed"], g["T-1003"]["unfinished"]), (2, 0))
        self.assertEqual((r["resumes_needed"], r["unfinished"]), (2, 1))
        put("T-1001", {"ended_ok": True})  # no claim recorded: can't tell
        g = {x["id"]: x for x in self.grade(self.run_id, "oracle")["goals"]}["T-1001"]
        self.assertEqual((g["resumes_needed"], g["unfinished"], g["false_done"]), (0, None, None))

    def test_a_tampered_run_json_id_is_refused_and_nothing_outside_the_run_is_touched(self):
        self.stub()
        outside = os.path.join(self.tmp, "x")
        write(outside, "keep", "1")
        path = os.path.join(self.fmlong._root(self.p), self.run_id, "run.json")
        meta = json.load(open(path))
        meta["scenarios"][0]["id"] = "../../x"
        write(os.path.dirname(path), "run.json", json.dumps(meta))
        for agent in ("plain", "empty"):
            with self.assertRaises(ValueError):
                self.go(agent)
        self.assertEqual(os.listdir(outside), ["keep"])
        self.assertFalse(os.path.exists(self.log))

    def test_session_arms_default_to_three_goals_and_limit_raises_it(self):
        self.stub()
        self.assertEqual(len(self.go("plain", limit=1)["answered"]), 1)
        self.assertEqual(len(self.calls()), 1)

    def test_spend_is_checked_before_each_goal_and_doubles_for_a_resuming_fault(self):
        import fmbudget
        self.stub()
        seen = []
        from unittest import mock
        flat = lambda f, n, fb=0.5: n * fb  # no measured spend: the first run records some
        with mock.patch.object(fmbudget, "check", lambda f, est, hint="": seen.append(est)), \
                mock.patch.object(fmbudget, "estimate", flat):
            self.go("plain")
            plain = list(seen)
            del seen[:]
            self.go("plain", ("pause",))
        self.assertEqual(len(plain), 3)  # up front, then a goal each
        self.assertEqual(seen[0], 2 * plain[0])

    def test_a_pause_whose_reply_has_no_marker_is_unfired_and_not_resumed(self):
        self.stub()
        os.environ["STUB_NOPAUSE"] = "1"
        self.addCleanup(os.environ.pop, "STUB_NOPAUSE", None)
        self.go("plain", ("pause",))
        self.assertEqual(len(self.calls()), 2)
        (k,) = self.faults("plain")
        self.assertEqual((k["fired"], k["resumed"]), (False, False))

    def test_the_first_turn_cap_never_exceeds_the_session_timeout(self):
        import time
        self.stub()
        self.fmlong.KILL_T = 60
        os.environ["STUB_HANG"] = "1"
        self.addCleanup(os.environ.pop, "STUB_HANG", None)
        t = time.time()
        self.go("plain", ("kill",), timeout=0.02, limit=1)
        self.assertLess(time.time() - t, 20)

    def test_a_resume_that_fails_after_a_kill_gets_one_fresh_turn_and_the_kill_cost_is_unknown(self):
        self.stub()
        for k in ("STUB_HANG", "STUB_NORESUME"):
            os.environ[k] = "1"
            self.addCleanup(os.environ.pop, k, None)
        (gid,) = self.go("plain", ("kill",), limit=1)["answered"]
        a, b, c3 = self.calls()
        self.assertEqual((b["resume"], c3["resume"]), (a["sid"], None))
        self.assertIn("Add f", c3["prompt"])
        self.assertNotEqual(c3["sid"], a["sid"])
        (k,) = self.faults("plain", gid)
        self.assertEqual((k["resume_ok"], k["fresh"], k["cost_unknown"]), (False, True, True))

    def test_the_sessions_transcripts_are_removed_with_or_without_the_compaction_fault(self):
        self.stub()
        self.go("plain")
        left = [n for r, _, fs in os.walk(self.cfg) for n in fs]
        self.assertEqual(left, [])

    def test_unknown_faults_and_faults_on_a_zero_token_arm_are_refused_before_any_session(self):
        self.stub()
        for agent, faults in (("plain", ("nope",)), ("oracle", ("kill",))):
            with self.assertRaises(ValueError):
                self.go(agent, faults)
        self.assertFalse(os.path.exists(self.log))
        r = self.fm("exam", "long", "run", self.run_id, "--agent", "plain", "--faults", "compaction,misleading", "--json")
        self.assertEqual(json.loads(r.stdout)["agent"], "plain")


STUB = r'''#!/usr/bin/env python3
import json, os, sys, time
argv = sys.argv[1:]
arg = lambda k: argv[argv.index(k) + 1] if k in argv else None
sid = arg("--resume") or arg("--session-id") or "s-1"
planted = sorted(n for r, _, fs in os.walk(".") if ".git" not in r for n in fs if n.startswith("test_planted"))
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"plugin": "--plugin-dir" in argv, "model": arg("--model"), "prompt": arg("-p"), "resume": arg("--resume"),
                        "sid": sid, "window": os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW"), "planted": planted,
                        "quiet": os.environ.get("FOREMAN_QUIET")}) + "\n")
hung = os.path.join(os.environ["CLAUDE_CONFIG_DIR"], "hung" + os.getcwd().replace("/", "_"))
if os.environ.get("STUB_HANG") and not arg("--resume") and not os.path.exists(hung):
    os.makedirs(os.path.dirname(hung), exist_ok=True)
    open(hung, "w").close()  # hang once per goal: a fresh turn after the failed resume must not hang too
    time.sleep(30)
if os.environ.get("STUB_NORESUME") and arg("--resume"):  # the killed turn never wrote its session
    print("No conversation found", file=sys.stderr)
    sys.exit(1)
d = os.path.join(os.environ["CLAUDE_CONFIG_DIR"], "projects", "p")
os.makedirs(d, exist_ok=True)
open(os.path.join(d, sid + ".jsonl"), "w").write("{}\n")
said = "PAUSED" if "say PAUSED" in arg("-p") and not os.environ.get("STUB_NOPAUSE") else "done"
print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.1, "result": said, "session_id": sid}))
'''
