"""The line under the prompt (T-0092): one clean Foreman layout by default — a session line (model, folder, branch,
context, rate limits, cost) and a Foreman line, or a chip on the session line when the foreman-ui mod draws the band;
the old stack (your original command, claude-hud, two Foreman lines) only when opted in."""
import json
import os
import re
import subprocess

from helpers import ForemanTestCase

import fmcore as c

STATUSLINE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks", "statusline")
ANSI = re.compile(r"\x1b\[[0-9;]*m")


class StatuslineUi(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Fix login", "--type", "FIX", "--tier", "S", "--ac", "works :: true", "--step", "reproduce",
                "--step", "fix", "--focus")
        self.uhome = os.path.join(self.tmp, "uhome")
        os.makedirs(os.path.join(self.uhome, ".claude"))
        self.manifest(statusLine_original={"type": "command", "command": "echo OLD-LINE"}, statusline_hud=False)

    def manifest(self, **kw):
        c.write_atomic(os.path.join(self.home, "state", "install-manifest.json"), json.dumps(kw))

    def settings(self, **kw):
        with open(os.path.join(self.uhome, ".claude", "settings.json"), "w") as f:
            json.dump(kw, f)

    def run_line(self, columns="160"):
        payload = {"session_id": "s-ui", "cwd": self.repo, "model": {"display_name": "Opus 5.5"},
                   "workspace": {"current_dir": self.repo, "project_dir": self.repo},
                   "cost": {"total_cost_usd": 12.89, "total_lines_added": 737, "total_lines_removed": 31},
                   "context_window": {"used_percentage": 31, "context_window_size": 1000000},
                   "rate_limits": {"five_hour": {"used_percentage": 5, "resets_at": 4102444800},
                                   "seven_day": {"used_percentage": 25, "resets_at": 4102444800}}}
        env = dict(os.environ, FOREMAN_HOME=self.home, HOME=self.uhome, COLUMNS=columns)
        env.pop("CLAUDE_CONFIG_DIR", None)
        p = subprocess.run([STATUSLINE], input=json.dumps(payload), capture_output=True, text=True, env=env,
                           timeout=15, cwd=self.repo)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout.rstrip("\n").split("\n")

    def test_default_is_one_session_line_and_one_foreman_line_in_true_color(self):
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "repro.sh", "fails as reported")
        raw = self.run_line()
        lines = [ANSI.sub("", l) for l in raw]
        self.assertEqual(len(lines), 2, lines)
        self.assertNotIn("OLD-LINE", "\n".join(lines), "the old stack is opt-in now")
        for needle in ("Opus 5.5", os.path.basename(self.repo), "ctx", "31%", "5h", "5%", "7d", "25%", "$12.89",
                       "+737", "−31"):
            self.assertIn(needle, lines[0])
        for needle in ("▌T-0001", "FIX S", "executing", "━━━━━─────", "1/2", "fix", "audits 0/1", "q0 in0", "standard",
                       "guard on"):
            self.assertIn(needle, lines[1])
        self.assertIn("\x1b[38;2;", raw[0], "true color, not the old plain text")

    def test_the_old_stack_comes_back_when_opted_in(self):
        self.manifest(statusLine_original={"type": "command", "command": "echo OLD-LINE"}, statusline_hud=False,
                      statusline_layout="stack")
        lines = self.run_line()
        self.assertEqual(lines[0], "OLD-LINE")

    def test_with_the_mod_on_foreman_is_a_chip_on_the_session_line(self):
        self.settings(enabledPlugins={"foreman-ui@foreman": True})
        lines = [ANSI.sub("", l) for l in self.run_line()]
        self.assertEqual(len(lines), 1, lines)
        self.assertIn("▌T-0001 0/2", lines[0])

    def test_narrow_terminals_get_a_cut_line_not_a_wrapped_one(self):
        for line in self.run_line(columns="40"):
            self.assertLessEqual(len(ANSI.sub("", line)), 40)

    def test_regen_views_writes_the_structured_status(self):
        st = json.loads(open(os.path.join(c.find_project(self.repo).dir, "status.json")).read())
        self.assertEqual(st["active"]["id"], "T-0001")
        self.assertEqual((st["active"]["done"], st["active"]["total"], st["active"]["step"]), (0, 2, "reproduce"))
        self.assertEqual((st["queue"], st["inbox"], st["autonomy"]), (0, 0, "standard"))

    def test_a_failing_snapshot_or_odd_columns_never_costs_the_lines(self):
        sessions = os.path.join(self.home, "state", "sessions")
        os.makedirs(os.path.dirname(sessions), exist_ok=True)
        if os.path.isdir(sessions):
            os.rename(sessions, sessions + ".bak")
        with open(sessions, "w") as f:  # a file where the snapshot dir should be: every snapshot write fails
            f.write("x")
        lines = [ANSI.sub("", l) for l in self.run_line(columns="abc")]
        self.assertEqual(len(lines), 2, lines)
        self.assertIn("▌T-0001", lines[1])
