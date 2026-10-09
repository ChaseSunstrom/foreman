"""T-0676 (performance and cost): gate order by failure odds per second (T-0467), a hook latency SLO by revision
(T-0486), degrading optional work while usage runs ahead of pace (T-0449), the model behind each finished task (T-0487)
and compacting at an M/L step boundary (T-0448)."""
import json
import os
import shlex
import time

from helpers import read_text
from test_hooks import HookCase, parse
import test_ideas

import fmcore as c
import fmdoctor
import fmeco


def usage(**windows):
    """A statusline snapshot: window=(used %, seconds until it resets)."""
    folder = os.path.join(c.state_dir(), "sessions")
    os.makedirs(folder, exist_ok=True)
    rl = {k: {"used_percentage": u, "resets_at": int(time.time() + s)} for k, (u, s) in windows.items()}
    with open(os.path.join(folder, "s.json"), "w") as f:
        json.dump({"rate_limits": rl}, f)


AHEAD = {"seven_day": (78, 6 * 86400)}  # 78% used with a seventh of the week gone: ahead of pace, under 90%


class GateOrder(HookCase):
    def gate(self, name):
        return f"echo {name} >> {shlex.quote(self.log)}; test ! -e {shlex.quote(self.flag)}-{name}"

    def ran(self):
        out = read_text(self.log).split() if os.path.exists(self.log) else []
        if os.path.exists(self.log):
            os.remove(self.log)
        return out

    def test_gates_run_by_failure_odds_per_second_and_list_in_configured_order(self):
        self.log, self.flag = os.path.join(self.tmp, "order.log"), os.path.join(self.tmp, "fail")
        self.fm("init")
        gates = [self.gate(x) for x in "abc"]
        for g in gates:
            self.fm("check", "add", g)
        res = self.fm_json("check", "--fresh")
        self.assertEqual(self.ran(), ["a", "b", "c"], "no history: the configured order")
        p = self.project()
        for i in range(5):  # a: slow, never fails · b: fast, never fails · c: fails often, 2 s
            c.log_event(p, "check_run", data={"results": [{"cmd": gates[0], "exit": 0, "s": 9.0},
                                                          {"cmd": gates[1], "exit": 0, "s": 1.0},
                                                          {"cmd": gates[2], "exit": int(i < 2), "s": 2.0}]})
        res = self.fm_json("check", "--fresh")
        self.assertEqual(self.ran(), ["c", "b", "a"], "most failure odds per second of runtime first")
        self.assertEqual([r["cmd"] for r in res["results"]], gates, "results still listed in configured order")
        run = [e for e in c.ledger_tail(p, 50) if e.get("event") == "check_run"][-1]
        self.assertEqual([r["cmd"] for r in run["data"]["results"]], gates, "the ledger too (fm check's cache reads it)")
        open(self.flag + "-c", "w").close()
        r = self.fm("check", "--fresh", "--fail-fast", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(set(self.ran()), {"c"}, "fail-fast: the likeliest failure ran first and ended the run")
        self.assertIn("2 later gate(s) not run", r.stdout)


class HookSlo(HookCase):
    def write_events(self, rows):
        path = os.path.join(c.state_dir(), "events.jsonl")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            for rev, ms in rows:
                f.write(json.dumps({"ts": c.now(), "kind": "hook_ms", "event": "PreToolUse", "ms": ms, "rev": rev}) + "\n")

    def test_each_hook_ms_event_carries_the_revision(self):
        self.fm("init")
        self.hook("PreToolUse", {"tool_name": "Read", "tool_input": {"file_path": os.path.join(self.repo, "README.md")}})
        ms = [e for e in self.events() if e.get("kind") == "hook_ms"]
        self.assertTrue(ms)
        self.assertEqual(ms[-1].get("rev"), fmeco.version())

    def test_doctor_warns_past_the_slo_and_names_the_revision_where_it_rose(self):
        self.assertEqual(fmdoctor.check_hook_slo().status, "PASS", "no runs recorded: nothing to judge")
        self.write_events([("1.2.15", 40)] * 150 + [("1.2.16", 60)] * 100)
        r = fmdoctor.check_hook_slo()
        self.assertEqual(r.status, "PASS", r.detail)
        self.write_events([("1.2.15", 40)] * 150 + [("1.2.16", 60)] * 100 + [("1.2.17", 400)] * 100)
        r = fmdoctor.check_hook_slo()
        self.assertEqual(r.status, "WARN", r.detail)
        self.assertIn("1.2.17", r.detail)
        self.assertIn("1.2.16", r.detail, "the revision before it, for the range")
        self.assertIn("150", r.detail, "bench_hooks' budget is the SLO")
        self.assertNotIn("1.2.15", r.detail, "only the last 200 runs count")


class DegradeOnPace(HookCase):
    def test_fm_next_drops_the_friction_pass_while_ahead_of_pace(self):
        self.fm("init")
        self.fm("friction", "--every", "1")
        p = self.project()
        c.log_event(p, "task_done", task="T-0099")
        self.assertIn("self-improvement pass due", self.fm("next").stdout)
        usage(**AHEAD)
        out = self.fm("next").stdout
        self.assertNotIn("self-improvement pass due", out)
        self.assertIn("ahead of pace", out)
        self.assertIn("required gates still run", out)

    def test_the_drive_offers_no_side_work_while_ahead_of_pace(self):
        self.fm("init")
        queued = self.task("Second fix", focus=False)
        self.task("Current work")
        usage(**AHEAD)
        self.hook("SubagentStart", {"agent_id": "a1", "agent_type": "foreman:fm-reviewer"})
        p = self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Waiting for the review.",
                               "session_id": "sess-1"})
        reason = (parse(p) or {}).get("reason", "")
        self.assertNotIn(f"lane brief {queued}", reason, "no side task while usage runs ahead of pace")
        self.assertNotIn(f"second plan {queued}", reason)
        self.assertIn("ahead of pace", reason)
        self.assertIn(queued, reason, "the queue is the user's work: it's still named as what comes next")

    def test_ideas_deepen_runs_no_rounds_and_over_the_cap_still_blocks(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(test_ideas.STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        log = os.path.join(self.tmp, "stub.log")
        env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": log}
        pack = os.path.join(self.tmp, "pack.md")
        with open(pack, "w") as f:
            f.write("Project: a tiny calculator app.\n")
        self.fm("init")
        usage(**AHEAD)
        r = self.fm("ideas", "--pack", pack, "--lens", "user value", "--deepen", "2", env=env)
        calls = [json.loads(l) for l in read_text(log).splitlines()]
        self.assertEqual(len(calls), 1, "the lens ran; no deepen round")
        self.assertFalse(any("deepen:" in x["stdin"] for x in calls))
        self.assertIn("ahead of pace", r.stdout + r.stderr)
        self.fm("check", "add", "true")
        self.assertEqual(self.fm("check", "--fresh", check=False).returncode, 0, "required gates still run")
        self.fm("budget", "set", "--day", "0")
        r = self.fm("ideas", "--pack", pack, "--lens", "user value", env=env, check=False)
        self.assertNotEqual(r.returncode, 0, "over the cap still blocks")
        self.assertIn("budget:", r.stderr)


class ModelLog(HookCase):
    def test_finish_logs_the_model_and_cost_shows_passes_by_model(self):
        self.fm("init")
        sessions = os.path.join(c.state_dir(), "sessions")
        os.makedirs(sessions, exist_ok=True)
        with open(os.path.join(sessions, "sess-m.json"), "w") as f:
            json.dump({"model": "Opus 5.5"}, f)
        env = {"FOREMAN_SESSION_ID": "sess-m"}
        self.fm("task", "new", "Add a", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                "--focus", env=env)
        self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check", env=env)
        done = [e for e in c.ledger_tail(self.project(), 200) if e.get("event") == "task_done"][-1]["data"]
        self.assertEqual({k: done.get(k) for k in ("model", "type", "tier")}, {"model": "Opus 5.5", "type": "FEATURE",
                                                                                "tier": "S"})
        self.assertIn(done.get("verified"), ("weak", "ok", "strong"))
        out = self.fm("cost", "--by-model").stdout
        self.assertIn("Opus 5.5", out)
        self.assertIn("FEATURE S", out)
        self.assertIn("1 passed", out)
        data = self.fm_json("cost", "--by-model")
        self.assertEqual(data["by_model"]["Opus 5.5"]["FEATURE S"]["passed"], 1)


class StepCompact(HookCase):
    def context(self, pct):
        sessions = os.path.join(c.state_dir(), "sessions")
        os.makedirs(sessions, exist_ok=True)
        with open(os.path.join(sessions, "sess-1.json"), "w") as f:
            json.dump({"context_pct": pct}, f)

    def stop(self):
        p = self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Working on it.",
                               "session_id": "sess-1"})
        return (parse(p) or {}).get("reason", "")

    def test_a_full_context_at_an_ml_step_boundary_says_checkpoint_and_compact(self):
        self.fm("init")
        tid = self.task("Big change", type_="FEATURE", tier="M")
        self.context(72)
        self.assertNotIn("step boundary", self.stop(), "mid-step: no note")
        self.fm("task", "evidence", tid, "--step", "1", "pytest", "red as expected")
        reason = self.stop()
        self.assertIn("step boundary", reason)
        self.assertIn("fm checkpoint", reason)
        self.assertIn("Resume here", reason)
        self.assertIn("/compact", reason)
        self.assertNotIn("step boundary", self.stop(), "said once per step boundary")

    def test_no_note_for_s_tasks_low_context_or_once_work_resumed(self):
        self.fm("init")
        small = self.task("Small fix")
        self.context(72)
        self.fm("task", "evidence", small, "--step", "1", "pytest", "red")
        self.assertNotIn("step boundary", self.stop(), "S: compaction overhead isn't worth it")
        tid = self.task("Big change", type_="FEATURE", tier="M")  # pauses the S task
        self.context(30)
        self.fm("task", "evidence", tid, "--step", "1", "pytest", "red")
        self.assertNotIn("step boundary", self.stop(), "context is fine")
        self.context(72)
        self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(self.repo, "README.md")}})
        self.assertNotIn("step boundary", self.stop(), "the next step is under way: not a boundary")
