"""T-1611: the fm code app's settings scopes: everywhere (tui.toml), this project (kept with Foreman's state for the
project), this run (memory), and the repo's policy pins over all of them, which never touch keys or motion."""
import os

from helpers import ForemanTestCase, read_text

import fmcodetui as T


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class Layers(ForemanTestCase):
    def test_narrower_scopes_win_and_pins_win_over_them(self):
        write(T.project_settings_path(self.repo), 'border = "square"\npalette = "riso"\n')
        cfg, problems = T.layered(T.DEFAULTS, self.repo, {"palette": "cb"})
        self.assertEqual((cfg["border"], cfg["palette"]), ("square", "cb"), problems)
        self.assertEqual(cfg["scopes"], {"border": "project", "palette": "run"})
        write(T.policy_path(self.repo), '[pin]\nborder = "double"\nmotion = "full"\n[pin.keys]\nq = "help"\n'
                                        '[pin.colors]\nok = "#33dd66"\n')
        cfg, problems = T.layered(T.DEFAULTS, self.repo, {"border": "rounded"})
        self.assertEqual(cfg["border"], "double", "the pin wins over this run and this project")
        self.assertEqual(cfg["theme"]["ok"], {"fg": "#33dd66"})
        self.assertEqual((cfg["motion"], cfg["keys"]["q"]), (T.DEFAULTS["motion"], "quit"), "never pinned")
        self.assertEqual(sorted(p.split(": ")[1] for p in problems if "never pinned" in p), ["pin.keys", "pin.motion"])
        self.assertEqual((cfg["scopes"]["border"], cfg["scopes"]["colors.ok"]), ("pin", "pin"))

    def test_a_bad_layer_is_said_and_the_rest_apply(self):
        write(T.project_settings_path(self.repo), 'border = "zigzag"\npalette = "riso"\n[[rule]]\nwhen = "running"\n')
        write(T.policy_path(self.repo), 'pin = 3\n')
        cfg, problems = T.layered(T.DEFAULTS, self.repo)
        self.assertEqual((cfg["border"], cfg["palette"]), (T.DEFAULTS["border"], "riso"))
        said = " | ".join(problems)
        self.assertIn("zigzag", said)
        self.assertIn("only tui.toml has [rule] tables", said)
        self.assertIn("pin: a [pin] table", said)

    def test_the_project_file_lives_with_foremans_state_not_the_repo(self):
        path = T.project_settings_path(self.repo)
        self.assertFalse(os.path.realpath(path).startswith(os.path.realpath(self.repo) + os.sep))
        self.assertTrue(path.startswith(os.path.realpath(os.environ["FOREMAN_HOME"])) or
                        path.startswith(os.environ["FOREMAN_HOME"]))


class App(ForemanTestCase):
    def setUp(self):
        super().setUp()
        import fmsettings
        from unittest import mock
        guard = mock.patch.object(fmsettings, "in_claude_code", return_value=False)  # the app's own terminal
        guard.start()
        self.addCleanup(guard.stop)

    def app(self):
        app = T.App(T.DEFAULTS, spawn=lambda *a, **k: None, root=self.repo)
        app.show_settings()
        return app

    def test_s_picks_the_scope_and_a_run_set_writes_nothing(self):
        app = self.app()
        app.key("s")
        self.assertEqual(app.set_scope, "project")
        app.key("s")
        self.assertEqual(app.set_scope, "run")
        app._settings_set("set border double")
        self.assertEqual(app.cfg["border"], "double", app.set_note)
        self.assertFalse(os.path.exists(T.config_path()) and "double" in read_text(T.config_path()))
        self.assertFalse(os.path.exists(T.project_settings_path(self.repo)))
        self.assertIn("this run", app.set_note[0])

    def test_a_project_set_writes_its_own_file_and_a_pin_refuses(self):
        app = self.app()
        app._settings_set("set border square --scope project")
        self.assertIn('border = "square"', read_text(T.project_settings_path(self.repo)), app.set_note)
        self.assertEqual(app.cfg["border"], "square")
        self.assertEqual(next(r for r in app.set_rows if r["key"] == "border").get("scope"), "project")
        write(T.policy_path(self.repo), '[pin]\nborder = "double"\n')
        app._settings_reload()
        self.assertEqual(app.cfg["border"], "double")
        app._settings_set("set border rounded --scope run")
        self.assertEqual((app.cfg["border"], app.set_note[1]), ("double", "bad"))
        self.assertIn("pinned by", app.set_note[0])
        app._settings_set("set border rounded --scope nowhere")
        self.assertIn("--scope takes", app.set_note[0])


class Cli(ForemanTestCase):
    def term(self, *args):
        """fm as the user's own terminal runs it (a pty, the Claude Code variables blank): (exit code, what it said)."""
        import pty
        import subprocess
        import sys
        from helpers import FM, pty_reader
        env = dict(os.environ, FOREMAN_INHIBITED="1", CLAUDECODE="", CLAUDE_CODE_ENTRYPOINT="")
        env.pop("CLAUDE_CODE_SESSION_ID", None)
        main, sub = pty.openpty()
        reader = pty_reader(main)  # T-1902: read as it writes; macOS drops what's unread once fm exits
        try:
            p = subprocess.run([sys.executable, FM, *args], cwd=self.repo, env=env, stdin=sub, stdout=sub,
                               stderr=subprocess.PIPE, text=True, timeout=30)
        finally:
            os.close(sub)
        reader.join(10)
        os.close(main)
        return p.returncode, bytes(reader.out).decode(errors="replace") + p.stderr

    def test_fm_settings_set_scope_project(self):
        self.fm("init")
        code, out = self.term("settings", "set", "border", "square", "--scope", "project")
        self.assertEqual(code, 0, out)
        self.assertIn("this project's", out)
        self.assertIn('border = "square"', read_text(T.project_settings_path(self.repo)))
        self.assertFalse(os.path.exists(T.config_path()) and "square" in read_text(T.config_path()))
        p = self.fm("settings", "set", "border", "heavy", "--scope", "project", check=False)  # an agent's shell
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("guard", p.stderr)
        self.assertIn('border = "square"', read_text(T.project_settings_path(self.repo)), "the guard kept it")
        self.assertNotEqual(self.term("settings", "set", "mascot", "off", "--scope", "project")[0], 0)
