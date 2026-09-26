"""Visibility layer: statusline wrapper, subagent statusline, fm watch."""
import json
import os
import subprocess
import time
import unittest

from helpers import PLUGIN, ForemanTestCase

import fmcore as c

STATUSLINE = os.path.join(PLUGIN, "hooks", "statusline")
SUBAGENT_LINE = os.path.join(PLUGIN, "hooks", "subagent-statusline")


class VisibilityCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Fix login", "--type", "FIX", "--tier", "S")
        self.fm("task", "step", "T-0001", "add", "reproduce")
        self.fm("task", "step", "T-0001", "add", "fix")
        self.fm("focus", "T-0001")

    def manifest(self, **kw):
        c.write_atomic(os.path.join(self.home, "state", "install-manifest.json"), json.dumps(kw))

    def status_payload(self):
        return {"session_id": "sess-9", "cwd": self.repo, "model": {"id": "claude-x", "display_name": "X"},
                "workspace": {"current_dir": self.repo, "project_dir": self.repo},
                "cost": {"total_cost_usd": 1.23},
                "context_window": {"used_percentage": 41.5, "context_window_size": 200000},
                "rate_limits": {"five_hour": {"used_percentage": 12, "resets_at": 1}},
                "prompt_cache": {"hit_ratio": 0.8}}

    def statusline(self, payload=None, env=None):
        e = dict(os.environ, FOREMAN_HOME=self.home, COLUMNS="120")
        e.update(env or {})
        return subprocess.run([STATUSLINE], input=json.dumps(payload or self.status_payload()), capture_output=True,
                              text=True, env=e, timeout=15, cwd=self.repo)


class Statusline(VisibilityCase):
    def test_composes_original_then_foreman_line(self):
        self.manifest(statusLine_original={"type": "command", "command": "echo ORIGINAL-LINE"}, statusline_hud=False)
        lines = self.statusline().stdout.rstrip("\n").split("\n")
        self.assertEqual(lines[0], "ORIGINAL-LINE")
        self.assertIn("T-0001 FIX 1/2", lines[-1])
        self.assertIn("foreman", lines[-1])

    def test_blank_or_failing_original_still_prints_foreman_line(self):
        self.manifest(statusLine_original={"type": "command", "command": "echo; exit 3"}, statusline_hud=False)
        p = self.statusline()
        self.assertEqual(p.returncode, 0)
        lines = [l for l in p.stdout.split("\n") if l.strip()]
        self.assertEqual(len(lines), 1)
        self.assertIn("T-0001", lines[0])

    def test_original_receives_the_same_json(self):
        cmd = "python3 -c 'import json,sys;print(json.load(sys.stdin)[\"model\"][\"display_name\"])'"
        self.manifest(statusLine_original={"type": "command", "command": cmd}, statusline_hud=False)
        self.assertEqual(self.statusline().stdout.split("\n")[0], "X")

    def test_writes_session_snapshot(self):
        self.manifest(statusline_hud=False)
        self.statusline()
        snap = json.load(open(os.path.join(self.home, "state", "sessions", "sess-9.json")))
        self.assertEqual((snap["context_pct"], snap["cost_usd"], snap["cache_hit_ratio"]), (41.5, 1.23, 0.8))
        self.assertEqual(snap["project"], c.slug_for(self.repo))

    def test_without_manifest_or_project_prints_something_useful(self):
        elsewhere = os.path.join(self.tmp, "nowhere")
        os.makedirs(elsewhere)
        payload = dict(self.status_payload(), cwd=elsewhere)
        p = self.statusline(payload, env={"FOREMAN_HOME": os.path.join(self.tmp, "empty-home")})
        self.assertEqual(p.returncode, 0)
        self.assertIn("foreman", p.stdout)


class SubagentStatusline(VisibilityCase):
    def test_rows_show_task_tokens_and_elapsed(self):
        payload = {"session_id": "s", "cwd": self.repo, "columns": 100,
                   "tasks": [{"id": "a1", "name": "fm-recon", "type": "subagent", "status": "running",
                              "description": "map auth module", "label": "fm-recon",
                              "startTime": int((time.time() - 65) * 1000), "model": "claude-sonnet",
                              "contextWindowSize": 200000, "tokenCount": 12345, "cwd": self.repo}]}
        p = subprocess.run([SUBAGENT_LINE], input=json.dumps(payload), capture_output=True, text=True, timeout=10,
                           env=dict(os.environ, FOREMAN_HOME=self.home))
        rows = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
        self.assertEqual(rows[0]["id"], "a1")
        for part in ("T-0001", "map auth module", "12.3k/200k", "6%", "1m0"):
            self.assertIn(part, rows[0]["content"])

    def test_garbage_input_prints_nothing(self):
        p = subprocess.run([SUBAGENT_LINE], input="not json", capture_output=True, text=True, timeout=10)
        self.assertEqual((p.returncode, p.stdout), (0, ""))


class Watch(VisibilityCase):
    def test_once_renders_sections_and_new_tool_event_within_two_seconds(self):
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "duration_ms": 321})
        t0 = time.monotonic()
        out = self.fm("watch", "--once").stdout
        self.assertLess(time.monotonic() - t0, 2.0)
        for section in ("Active", "Queue", "Inbox", "Tool timeline", "Subagents", "Files touched", "Guard blocks",
                        "Hook latency", "Session"):
            self.assertIn(section, out)
        self.assertIn("T-0001", out)
        self.assertIn("pytest -q", out)
        self.assertIn("321", out)

    def test_once_shows_guard_blocks_and_latency(self):
        self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "npm publish"}})
        self.hook("SessionStart", {"source": "startup"})
        out = self.fm("watch", "--once").stdout
        self.assertIn("publish", out)
        self.assertRegex(out, r"SessionStart\s+p50")


if __name__ == "__main__":
    unittest.main()
