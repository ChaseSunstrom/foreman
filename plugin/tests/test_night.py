"""Unattended checks (T-0298): fm bench stranger — a newcomer session from the README alone, its stumbles captured as
self items (T-0244); fm night — budgeted background work while the user is away, refused at high usage (T-0236)."""
import json
import os

from helpers import ForemanTestCase, read_text

import fmcore as c

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "cwd": os.getcwd(), "state": os.environ.get("FOREMAN_STATE")}) + "\n")
events = os.path.join(os.environ["FOREMAN_STATE"], "events.jsonl")
os.makedirs(os.path.dirname(events), exist_ok=True)
with open(events, "a") as f:  # what a newcomer's session leaves: a guard block, a mistyped fm call
    f.write(json.dumps({"kind": "guard_block", "category": "rm-outside", "tool": "Bash"}) + "\n")
    f.write(json.dumps({"kind": "tool_fail", "tool": "Bash", "target": "fm tsk new 'fix calc'",
                        "error": "fm: argument cmd: invalid choice: 'tsk'"}) + "\n")
    f.write(json.dumps({"kind": "tool_fail", "tool": "Bash", "target": "pytest -q", "error": "exit 1"}) + "\n")
print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.3, "num_turns": 4, "result": "done"}))
'''


class Stranger(ForemanTestCase):
    def test_a_newcomers_stumbles_become_self_items(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        log = os.path.join(self.tmp, "log")
        env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": log}
        self.fm("init")
        res = json.loads(self.fm("bench", "stranger", "--json", env=env).stdout)
        call = json.loads(read_text(log).splitlines()[0])
        self.assertIn("README", " ".join(call["args"]))  # the README is all it gets
        self.assertNotEqual(os.path.realpath(call["cwd"]), os.path.realpath(self.repo))  # a toy repo, not this one
        self.assertFalse(call["state"].startswith(c.state_dir()))  # a fresh Foreman state, not this one
        kinds = " | ".join(res["findings"])
        self.assertIn("rm-outside", kinds)
        self.assertIn("fm tsk new", kinds)  # a failed fm call
        self.assertNotIn("pytest", kinds)  # other failures aren't Foreman's
        self.assertIn("not finished", kinds)  # the stub fixed nothing: the toy test still fails
        selfp = c.find_project(c.foreman_home())
        titles = [b.title for b in c.load_briefs(selfp) if b.meta.get("source") == "self"]
        self.assertEqual(len(titles), len(res["captured"]))
        self.assertTrue(1 <= len(titles) <= 5)
        again = json.loads(self.fm("bench", "stranger", "--plugin", c.PLUGIN_ROOT, "--json", env=env).stdout)
        self.assertEqual(again["captured"], [])  # the same stumbles aren't captured twice


class Night(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        d = os.path.join(c.state_dir(), "sessions")  # usage known and low (unknown usage halves the limit)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "s.json"), "w") as f:
            json.dump({"rate_limits": {"seven_day": {"used_percentage": 10}}}, f)

    def test_dry_run_lists_what_fits(self):
        out = json.loads(self.fm("night", "--dry-run", "--json").stdout)
        names = [j["name"] for j in out["jobs"]]
        self.assertIn("landscape", names)  # never scanned: due
        self.assertIn("second session", names)
        self.assertLessEqual(sum(j["usd"] for j in out["jobs"]), out["limit"])
        tight = json.loads(self.fm("night", "--dry-run", "--max-usd", "0.001", "--json").stdout)
        self.assertEqual([j["name"] for j in tight["jobs"]], ["scout", "dream", "cold files", "compost", "consolidate"])  # T-1071, T-0950, T-0665, T-0660: only free jobs fit
        self.assertTrue(tight["skipped"])  # what didn't fit is named
        tid = json.loads(self.fm("task", "new", "x", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                                 "--json").stdout)["id"]
        self.fm("focus", tid)
        self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        tight = json.loads(self.fm("night", "--dry-run", "--max-usd", "0.001", "--json").stdout)
        self.assertIn(("sentinel", ["sentinel", "--bisect"], 0.0),  # T-0888: closed tasks' checks against HEAD, free
                      [(j["name"], j["argv"], j["usd"]) for j in tight["jobs"]])

    def test_gardening_jobs_are_listed_and_accepted(self):  # T-1071
        out = json.loads(self.fm("night", "--dry-run", "--only", "compost", "--json").stdout)
        self.assertEqual([j["name"] for j in out["jobs"]], ["compost"])
        names = [j["name"] for j in json.loads(self.fm("night", "--dry-run", "--json").stdout)["jobs"]]
        self.assertIn("compost", names)
        self.assertIn("consolidate", names)

    def test_night_compost_touches_only_lanes(self):  # T-1071 review
        import fmnight
        p = c.find_project(self.repo)
        argv = dict((n, a) for n, a, _ in fmnight.jobs(p))
        self.assertEqual(argv["compost"], ["tidy", "--apply", "--lanes-only"])
        self.assertIn("--capture", argv["consolidate"])
        self.fm("task", "new", "Stuck", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        tid = c.load_briefs(p)[-1].id
        self.fm("task", "block", tid, "waiting")
        out = self.fm("tidy", "--apply", "--lanes-only", "--json").stdout
        self.assertEqual(json.loads(out)["findings"], [])
        self.assertEqual(c.find_brief(p, tid).status, "blocked")

    def _queue_job(self, *extra):
        out = json.loads(self.fm("night", "--dry-run", "--only", "queue", "--json", *extra).stdout)
        return next((j for j in out["jobs"] if j["name"] == "queue"), None), out

    def test_queue_job_only_with_an_unblocked_small_task(self):  # T-1046
        self.assertIsNone(self._queue_job()[0])  # empty queue
        self.fm("task", "new", "Stuck", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "block", "T-0001", "waiting")
        self.assertIsNone(self._queue_job()[0])  # only a blocked task
        self.fm("task", "new", "Big", "--type", "FEATURE", "--tier", "L", "--ac", "ok :: true", "--step", "s")
        self.assertIsNone(self._queue_job()[0])  # L is never run overnight
        self.fm("task", "new", "Small", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        job, _ = self._queue_job()
        self.assertEqual(job["argv"][0], "run")
        job, out = self._queue_job("--max-usd", "0.01")
        self.assertIsNone(job)
        self.assertIn("queue", [s["name"] for s in out["skipped"]])  # too small a budget for it

    def test_a_night_records_the_tasks_the_queue_closed_and_the_digest_says_so(self):  # T-1046
        import argparse
        from unittest import mock
        import fmnight
        self.fm("task", "new", "Small", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        p = c.find_project(self.repo)

        seen = []

        def fake(argv, **kw):  # fm run closing T-0001
            seen.append(argv)
            c.log_event(p, "task_done", task="T-0001", data={})
            return mock.Mock(returncode=0, stdout="finished 1", stderr="")
        args = argparse.Namespace(only=["queue"], max_usd=5.0, dry_run=False, json=True, print_timer=False, project=None)
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            with mock.patch.object(fmnight.subprocess, "run", fake):
                fmnight.cmd_night(args)
        finally:
            os.chdir(cwd)
        self.assertEqual(seen[0][seen[0].index("--max-usd") + 1], "5.0000")  # the night's remaining budget
        night = [e for e in c.ledger_tail(p, 50) if e.get("event") == "night"][-1]
        self.assertEqual(night["data"]["closed"], ["T-0001"])
        self.assertIn("closed T-0001", self.fm("digest").stdout)

    def test_high_usage_runs_nothing(self):
        sessions = os.path.join(c.state_dir(), "sessions")
        os.makedirs(sessions, exist_ok=True)
        with open(os.path.join(sessions, "s.json"), "w") as f:
            json.dump({"rate_limits": {"seven_day": {"used_percentage": 85}}}, f)
        p = self.fm("night", "--dry-run", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("usage", p.stderr)

    def test_a_night_runs_its_jobs_and_the_digest_says_so(self):
        res = json.loads(self.fm("night", "--max-usd", "0.05", "--only", "second session", "--json",
                                 env={"PATH": "/nonexistent:" + os.environ["PATH"]}).stdout)
        self.assertEqual([j["name"] for j in res["ran"]], ["second session"])
        self.assertIn("Night", self.fm("digest").stdout)


SECOND = r'''#!/usr/bin/env python3
import json, os, sys
sys.stdin.read()
if os.environ.get("STUB_HIGH"):  # usage climbs during the night
    d = os.path.join(os.environ["FOREMAN_HOME"], "state", "sessions")
    os.makedirs(d, exist_ok=True)
    json.dump({"rate_limits": {"seven_day": {"used_percentage": 90}}}, open(os.path.join(d, "late.json"), "w"))
print(json.dumps({"result": "## Missed\n- none", "total_cost_usd": float(os.environ.get("STUB_COST", "0.5"))}))
'''


class PrePlan(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        d = os.path.join(c.state_dir(), "sessions")  # usage known and low
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "s.json"), "w") as f:
            json.dump({"rate_limits": {"seven_day": {"used_percentage": 10}}}, f)

    def test_pre_plan_reads_a_queued_l_tasks_plan_once(self):
        # T-0730: idle time reads the plan of a big queued task before anyone starts it
        self.fm("task", "new", "Big", "--type", "FEATURE", "--tier", "L", "--ac", "ok :: true", "--step", "s")
        out = json.loads(self.fm("night", "--dry-run", "--only", "pre-plan", "--json").stdout)
        self.assertEqual([j["argv"] for j in out["jobs"]], [["second", "plan", "T-0001"]])
        self.fm("task", "set", "T-0001", "--section", "Plan review", "--text", "read")
        out = json.loads(self.fm("night", "--dry-run", "--only", "pre-plan", "--json").stdout)
        self.assertEqual(out["jobs"], [])


class NightGuards(ForemanTestCase):
    """T-0298 review: the limit is a cap on spend, usage is re-read, sensitive projects and odd names are refused."""

    def setUp(self):
        super().setUp()
        self.fm("init")
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(SECOND)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        cc = os.path.join(self.tmp, "cc")
        import fmcost
        d = os.path.join(cc, "projects", os.path.basename(fmcost.transcripts_dir(self.repo)))
        os.makedirs(d)
        with open(os.path.join(d, "old.jsonl"), "w") as f:
            f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "export the report"}}))
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "CLAUDE_CONFIG_DIR": cc,
                    "FOREMAN_SESSION_ID": "now"}
        import fmbudget
        fmbudget.record("research", 0.0001, runs=10)  # landscape looks nearly free: it fits the plan
        self.fresh_snapshot(10)

    def fresh_snapshot(self, pct):
        d = os.path.join(c.state_dir(), "sessions")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "s.json"), "w") as f:
            json.dump({"rate_limits": {"seven_day": {"used_percentage": pct}}}, f)

    def test_spend_past_the_limit_stops_the_night(self):
        res = json.loads(self.fm("night", "--max-usd", "0.1", "--only", "second session", "--only", "landscape",
                                 "--json", env=self.env).stdout)
        self.assertEqual([j["name"] for j in res["ran"]], ["second session"])  # it cost 0.5: nothing after it
        self.assertIn("limit", res["stopped"])

    def test_usage_climbing_mid_night_stops_it(self):
        res = json.loads(self.fm("night", "--max-usd", "1", "--only", "second session", "--only", "landscape",
                                 "--json", env=dict(self.env, STUB_COST="0.0", STUB_HIGH="1")).stdout)
        self.assertEqual([j["name"] for j in res["ran"]], ["second session"])
        self.assertIn("usage", res["stopped"])

    def test_night_breaker_stops_after_two_failed_jobs(self):
        # T-0434: two failed jobs in a row stop the night (never a retry); each job beats into the state dir first
        self.fm("capture", "RESEARCH: which TOML parser handles comments", "--type", "RESEARCH")
        beat = os.path.join(c.find_project(self.repo).dir, "heartbeat-night.json")
        seen = os.path.join(self.tmp, "seen")
        with open(os.path.join(self.tmp, "bin", "claude"), "w") as f:
            f.write(f"#!/usr/bin/env bash\ncat {beat} >> {seen}; echo >> {seen}\necho 'Error: boom' >&2\nexit 1\n")
        res = json.loads(self.fm("night", "--max-usd", "50", "--only", "second session", "--only", "landscape",
                                 "--only", "research debt", "--json", env=self.env).stdout)
        self.assertEqual([j["name"] for j in res["ran"]], ["second session", "landscape"])
        self.assertTrue(all(j["exit"] for j in res["ran"]))
        self.assertIn("in a row", res["stopped"])
        self.assertIn("second session", read_text(seen))
        self.assertFalse(os.path.exists(beat))  # the night ended: no heartbeat left to go stale

    def test_unknown_usage_halves_the_limit(self):
        os.remove(os.path.join(c.state_dir(), "sessions", "s.json"))
        res = json.loads(self.fm("night", "--dry-run", "--max-usd", "1", "--json").stdout)
        self.assertEqual(res["limit"], 0.5)
        self.assertIn("unknown", res["note"])

    def test_sensitive_projects_and_unknown_jobs(self):
        p = self.fm("night", "--dry-run", "--only", "landscpe", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("landscpe", p.stderr)
        self.fm("sensitive", "on")
        res = json.loads(self.fm("night", "--dry-run", "--json").stdout)
        self.assertEqual(res["jobs"], [])
        self.assertIn("sensitive", res["note"])

    def test_research_debt_and_evolve_candidates_are_jobs(self):
        rid = json.loads(self.fm("capture", "RESEARCH: which TOML parser handles comments", "--type", "RESEARCH",
                                 "--json").stdout)["id"]
        self.fm("log", "evolve", json.dumps({"kept": True, "branch": "evolve/20261004-0100", "target": "x.md"}))
        jobs = {j["name"]: j for j in json.loads(self.fm("night", "--dry-run", "--max-usd", "50", "--json").stdout)["jobs"]
                + json.loads(self.fm("night", "--dry-run", "--max-usd", "50", "--json").stdout)["skipped"]}
        self.assertIn(rid, " ".join(jobs["research debt"].get("argv") or [rid]))
        self.assertIn("evolve candidate", " ".join(jobs))


class StrangerGuards(ForemanTestCase):
    def test_captures_wait_for_the_user_and_quote_the_replay(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": os.path.join(self.tmp, "log")}
        self.fm("init")
        res = json.loads(self.fm("bench", "stranger", "--json", env=env).stdout)
        selfp = c.find_project(c.foreman_home())
        b = c.find_brief(selfp, res["captured"][0])
        self.assertTrue(c.needs_approval(b, "full"))  # text from a replay waits for the user's yes
        self.assertIn("quoted from", b.section("Raw request"))
        sessions = os.path.join(c.state_dir(), "sessions")
        os.makedirs(sessions, exist_ok=True)
        with open(os.path.join(sessions, "s.json"), "w") as f:
            json.dump({"rate_limits": {"five_hour": {"used_percentage": 95}}}, f)
        self.assertNotEqual(self.fm("bench", "stranger", env=env, check=False).returncode, 0)


class NightLease(ForemanTestCase):
    # T-0921: two nights at once (a cron firing while a manual one runs) would run every job twice
    def test_a_second_night_while_one_runs_stops_at_once(self):
        import fcntl
        self.fm("init")
        p = c.find_project(self.repo)
        with open(os.path.join(p.dir, "night.lock"), "w") as held:
            fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
            r = self.fm("night", "--max-usd", "0.1", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already running", r.stderr)
