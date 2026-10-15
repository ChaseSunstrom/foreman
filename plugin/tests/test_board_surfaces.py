"""T-0962: small surfaces from the board: NO_COLOR, step N/M in the statusline, fm ui --demo, fm page --picks, the
sync join line, and the tmux and LSP notes."""
import json
import os
import subprocess

from helpers import ForemanTestCase, read_text

import fmcore as c

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATUSLINE = os.path.join(ROOT, "plugin", "hooks", "statusline")
CATALOGUE = [{"id": "step-truth", "capability": "Step pointer", "mark": "build", "value": 5, "effort": "S"},
             {"id": "artifact-cockpit", "capability": "Cockpit", "mark": "later", "value": 4, "effort": "M"}]


class BoardSurfaces(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def _focus(self):
        self.fm("task", "new", "Fix login", "--type", "FIX", "--tier", "S", "--ac", "works :: true", "--step",
                "reproduce", "--step", "fix", "--focus")

    def _statusline(self, **env):
        uhome = os.path.join(self.tmp, "uhome")
        os.makedirs(os.path.join(uhome, ".claude"), exist_ok=True)
        c.write_atomic(os.path.join(self.home, "state", "install-manifest.json"), json.dumps({"statusline_hud": False}))
        payload = {"session_id": "s-b", "cwd": self.repo, "model": {"display_name": "Opus"},
                   "context_window": {"used_percentage": 31}}
        e = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CONFIG_DIR", "NO_COLOR")}
        e.update(FOREMAN_HOME=self.home, HOME=uhome, COLUMNS="200", **env)
        p = subprocess.run([STATUSLINE], input=json.dumps(payload), capture_output=True, text=True, env=e,
                           timeout=15, cwd=self.repo)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_no_color_drops_every_ansi_colour(self):
        self._focus()
        self.assertIn("\x1b[", self._statusline())
        self.assertNotIn("\x1b[", self._statusline(NO_COLOR="1"))

    def test_the_statusline_shows_step_n_of_m(self):
        self._focus()
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "repro.sh", "fails as reported")
        self.assertIn("step 1/2", self._statusline(NO_COLOR="1"))

    def test_ui_demo_has_every_key_a_real_view_has(self):
        self._focus()
        real = json.loads(self.fm("ui", "--json").stdout)
        demo = json.loads(self.fm("ui", "--demo").stdout)
        self.assertEqual(set(real) - set(demo), set())
        self.assertEqual(set(real["active"]) - set(demo["active"]), set())
        self.assertEqual(set(real["mode"]) - set(demo["mode"]), set())

    def test_page_picks_are_stored_checked_and_summarised(self):
        os.makedirs(os.path.join(self.p.dir, "research"), exist_ok=True)
        with open(os.path.join(self.p.dir, "research", "cat.json"), "w") as f:
            json.dump(CATALOGUE, f)
        bad = self.fm("page", "--catalogue", "cat", "--picks", "-", input='{"nope": "add"}', check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("nope", bad.stderr + bad.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.p.dir, "picks.json")))
        r = self.fm("page", "--catalogue", "cat", "--picks", "-",
                    input='{"step-truth": "add", "artifact-cockpit": "veto"}')
        self.assertIn("1 add", r.stdout)
        self.assertIn("1 veto", r.stdout)
        saved = json.loads(read_text(os.path.join(self.p.dir, "picks.json")))
        self.assertEqual(saved["picks"], {"step-truth": "add", "artifact-cockpit": "veto"})
        self.assertEqual(saved["catalogue"], "cat")

    def test_sync_status_prints_the_join_line(self):
        self.fm("sync", "on")
        out = self.fm("sync", "status").stdout
        self.assertIn("teammate", out)
        self.assertIn("fm sync on", out)

    def test_docs_name_the_tmux_line_and_lsp_diagnostics(self):
        self.assertIn("#(fm state --line)", read_text(os.path.join(ROOT, "README.md")))
        ref = read_text(os.path.join(ROOT, "plugin", "skills", "intake", "references", "execute.md"))
        self.assertIn("LSP", ref)
        self.assertIn("diagnostics", ref)
