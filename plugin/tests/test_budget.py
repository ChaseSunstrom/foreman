"""fm budget (T-0227): every child run and subagent records what it cost, and caps refuse what would overspend —
bounded use, not avoidance."""
import json
import os
import time

from helpers import ForemanTestCase, read_text

import fmbudget as bud
import fmcore as c

STUB = r'''#!/usr/bin/env python3
import json, os, sys
sys.stdin.read()
print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.07,
                  "result": "## Examples\n- GIVEN a WHEN b THEN c\n## Ambiguities\n- none"}))
'''


class Budget(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"]}
        self.fm("init")

    def spend(self):
        path = os.path.join(c.state_dir(), "spend.jsonl")
        return [json.loads(l) for l in read_text(path).splitlines()] if os.path.exists(path) else []

    def test_a_child_run_records_its_cost(self):
        tid = json.loads(self.fm("task", "new", "Export CSV", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                                 "--step", "do", "--json").stdout)["id"]
        self.fm("oracle", tid, env=self.env)
        rec = self.spend()[-1]
        self.assertEqual((rec["feature"], rec["usd"], rec["runs"]), ("oracle", 0.07, 1))
        self.assertIn("oracle", self.fm("budget").stdout)
        self.assertIn("GIVEN a WHEN b THEN c", self.fm("task", "show", tid).stdout, "the JSON result's text is used")

    def test_caps_refuse_what_would_overspend(self):
        bud.set_caps(day=10, run=4)
        bud.record("bench", 9.5, runs=3)
        bud.check("oracle", 0.3)  # fits
        with self.assertRaises(bud.BudgetError) as e:
            bud.check("bench", 1.0)
        self.assertIn("today", str(e.exception))
        with self.assertRaises(bud.BudgetError) as e:
            bud.check("evolve", 5.0)
        self.assertIn("per command", str(e.exception))

    def test_estimates_come_from_recent_runs(self):
        for usd in (0.2, 0.4):
            bud.record("research", usd, runs=1)
        self.assertAlmostEqual(bud.estimate("research", 3, fallback=9), 0.9)
        self.assertEqual(bud.estimate("never-ran", 2, fallback=0.5), 1.0)

    def test_caps_halve_when_weekly_usage_is_high(self):
        bud.set_caps(day=10, run=8)
        folder = os.path.join(c.state_dir(), "sessions")
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "s1.json"), "w") as f:
            json.dump({"rate_limits": {"seven_day": {"used_percentage": 85}}}, f)
        with self.assertRaises(bud.BudgetError) as e:
            bud.check("bench", 6.0)
        self.assertIn("usage", str(e.exception))

    def test_raising_a_cap_is_recorded_as_a_costly_decision(self):
        self.fm("budget", "set", "--day", "5")
        self.fm("budget", "set", "--day", "20", "--because", "night bench")
        decisions = read_text(os.path.join(c.find_project(self.repo).dir, "decisions.md"))
        self.assertIn("night bench", decisions)
        self.assertEqual(decisions.count("budget"), 1, "lowering needs no decision")
        self.assertNotEqual(self.fm("budget", "set", "--day", "30", check=False).returncode, 0, "raising says why")

    def test_bad_caps_never_switch_the_budget_off(self):
        # T-0227 review: --day nan made every comparison false; a corrupt file crashed every command
        for bad in ("nan", "-1", "inf"):
            with self.subTest(bad=bad):
                self.assertNotEqual(self.fm("budget", "set", "--day", bad, "--because", "x", check=False).returncode, 0)
        with open(os.path.join(c.state_dir(), "budget.json"), "w") as f:
            f.write('{"day": null, "run": [1]}')
        self.assertEqual(bud.caps(), bud.DEFAULTS)
        with open(os.path.join(c.state_dir(), "budget.json"), "w") as f:
            f.write("[1, 2]")
        self.assertEqual(bud.caps(), bud.DEFAULTS)
        self.assertIn("today", self.fm("budget").stdout)

    def test_subagents_are_counted_and_capped(self):
        transcript = os.path.join(self.tmp, "agent.jsonl")
        with open(transcript, "w") as f:
            for i in range(2):
                f.write(json.dumps({"type": "assistant", "timestamp": c.now(), "message": {
                    "id": f"m{i}", "usage": {"input_tokens": 1000, "output_tokens": 100}}}) + "\n")
        self.hook("SubagentStop", {"agent_id": "a1", "agent_type": "foreman:fm-recon",
                                   "agent_transcript_path": transcript})
        rec = self.spend()[-1]
        self.assertEqual((rec["feature"], rec["tokens"]), ("subagent:foreman:fm-recon", 3000))
        bud.set_caps(subagent_tokens=2500)
        out = self.hook("PreToolUse", {"tool_name": "Agent", "tool_input": {"subagent_type": "foreman:fm-recon",
                                                                           "prompt": "x"}})
        self.assertEqual(out.returncode, 2)
        self.assertIn("budget", out.stderr)
        bud.set_caps(subagent_tokens=10_000)
        self.assertEqual(self.hook("PreToolUse", {"tool_name": "Agent", "tool_input": {"prompt": "x"}}).returncode, 0)
