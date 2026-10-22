"""T-1496: one settings schema for both surfaces: the fm code app's tui.toml and the foreman-ui mod's userConfig (kept
by Claude Code in settings.json pluginConfigs). Shared settings share one name and value set; fm settings reads both."""
import json
import os
import unittest

from helpers import ForemanTestCase, read_json, read_text

import fmsettings

MOD = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "foreman-ui", ".claude-plugin", "plugin.json")


class Schema(unittest.TestCase):
    def test_one_schema_covers_both_surfaces(self):
        rows = fmsettings.schema()
        self.assertEqual({e["surface"] for e in rows}, {"app", "plugin"})
        plugin = {e["key"] for e in rows if e["surface"] == "plugin"}
        self.assertEqual(plugin, set(read_json(MOD)["userConfig"]))
        for e in rows:
            self.assertTrue(e["help"] and e["type"] and "default" in e, e)

    def test_motion_and_palette_share_one_name_and_value_set(self):
        cfg = read_json(MOD)["userConfig"]
        for name, shared in fmsettings.SHARED.items():
            entries = [e for e in fmsettings.schema() if e["key"] == name]
            self.assertEqual({e["surface"] for e in entries}, {"app", "plugin"}, name)
            for e in entries:
                self.assertEqual(tuple(e["choices"]), shared["choices"], (name, e["surface"]))
            # the old words stay listed after them: Claude Code drops a stored value its options don't name
            self.assertEqual(tuple(cfg[name]["options"]), shared["choices"] + tuple(shared["aliases"]),
                             f"plugin.json {name} options")
            self.assertIn(cfg[name]["default"], shared["choices"])

    def test_old_values_are_still_accepted(self):
        import tempfile
        import fmcodetui
        self.assertEqual(fmsettings.canon("motion", "calm"), "reduced", "the mod's old word")
        path = os.path.join(tempfile.mkdtemp(), "tui.toml")
        for text, want in (('motion = "calm"\n', ("motion", "reduced")), ('theme = "signal"\n', ("preset", "signal")),
                           ('palette = "cb"\n', ("palette", "cb"))):
            with open(path, "w") as f:
                f.write(text)
            cfg, errors = fmcodetui.load_config(path)
            self.assertEqual((errors, cfg[want[0]]), ([], want[1]), text)
        with open(path, "w") as f:
            f.write('palette = "cb"\n')
        self.assertEqual(fmcodetui.load_config(path)[0]["theme"]["ok"], fmcodetui._theme(fmcodetui.PALETTES["signal"])["ok"],
                         "cb on night is the signal colours")
        with open(path, "w") as f:
            f.write('theme = "paper"\npalette = "cb"\n')
        cfg, errors = fmcodetui.load_config(path)
        ok, bad = (fmcodetui._rgb(cfg["theme"][n]["fg"]) for n in ("ok", "bad"))
        self.assertEqual(errors, [])
        self.assertGreater(ok[2], ok[0], "pass is blue on paper too")
        self.assertGreater(bad[0], bad[2], "fail is orange")
        for n in ("ok", "bad", "warn", "accent"):
            self.assertGreaterEqual(fmcodetui.contrast(cfg["theme"][n]["fg"], cfg["theme"]["screen"]["bg"]), 3, n)


class Guard(unittest.TestCase):
    def test_a_builder_lane_writes_nothing_outside_its_worktree(self):
        import tempfile
        import types
        import unittest.mock as mock
        import fmcore
        lane, out = tempfile.mkdtemp(), os.path.join(tempfile.mkdtemp(), "settings.json")
        p, b = types.SimpleNamespace(lane=lane), types.SimpleNamespace(id="T-1", meta={"builder": True})
        with mock.patch.object(fmcore, "load_briefs", return_value=[]), \
                mock.patch.object(fmcore, "active_brief", return_value=b), \
                mock.patch.object(fmcore, "read_meta", return_value={}), \
                mock.patch.object(fmcore, "main_worktree", return_value="/nonexistent-main"):
            self.assertIsNotNone(fmsettings._guard_block(out, p))
            self.assertIsNone(fmsettings._guard_block(os.path.join(lane, "settings.json"), p))
        self.assertIsNone(fmsettings._guard_block(out, None), "outside a lane the same write is ordinary")


class Command(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")
        os.makedirs(os.path.join(self.uhome, ".claude"))
        self.settings = os.path.join(self.uhome, ".claude", "settings.json")
        self.before = json.dumps({"model": "x", "pluginConfigs": {"foreman-ui@foreman": {"options": {"motion": "calm"}},
                                                                   "other@m": {"options": {"a": 1}}}}, indent=2)
        with open(self.settings, "w") as f:
            f.write(self.before)
        with open(os.path.join(self.home, "tui.toml"), "w") as f:
            f.write('# mine\nborder = "heavy"\n')
        self.env = {"HOME": self.uhome, "CLAUDECODE": "", "CLAUDE_CODE_ENTRYPOINT": ""}  # the user's own terminal
        self.claude = dict(self.env, CLAUDECODE="1")  # inside a Claude Code session: the guard decides

    def term(self, *args):
        """fm run as the user's own terminal runs it: stdin and stdout a pty, the Claude Code variables blank (T-1572:
        with no terminal the guard decides, whatever the variables say)."""
        import pty
        import subprocess
        import sys
        from helpers import FM
        env = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1", **self.env)
        env.pop("CLAUDE_CODE_SESSION_ID", None)
        main, sub = pty.openpty()
        try:
            p = subprocess.run([sys.executable, FM, *args], cwd=self.repo, env=env, stdin=sub, stdout=sub,
                               stderr=subprocess.PIPE, text=True, timeout=30)
        finally:
            os.close(sub)
        out = b""
        while True:  # what it printed waits in the pty; EIO once it's read
            try:
                chunk = os.read(main, 65536)
            except OSError:
                break
            if not chunk:
                break
            out += chunk
        os.close(main)
        self.assertEqual(p.returncode, 0, f"fm {' '.join(args)}\n{out.decode(errors='replace')}{p.stderr}")
        return out.decode(errors="replace")

    def test_blank_claude_variables_with_no_terminal_still_go_through_the_guard(self):
        p = self.fm("settings", "set", "mascot", "orange", env=self.env, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("guard", p.stdout + p.stderr)
        self.assertEqual(read_text(self.settings), self.before, "settings.json untouched")

    def test_list_shows_user_bindings_and_what_the_app_cant_read(self):
        with open(os.path.join(self.home, "tui.toml"), "w") as f:
            f.write('theme = ["x"]\n[keys]\nz = "stop"\n')
        by = {(r["surface"], r["key"]): r for r in json.loads(self.fm("settings", "list", "--json", env=self.env).stdout)}
        self.assertEqual((by["app", "keys.z"]["value"], by["app", "keys.z"]["default"]), ("stop", "none"))
        text = self.fm("settings", "list", env=self.env).stdout
        self.assertIn("keys.z", text)
        self.assertIn("theme = ['x']", text, "the bad setting is named, not hidden behind the default")
        self.assertIn("stop", self.fm("settings", "get", "keys.z", env=self.env).stdout)
        self.term("settings", "set", "theme", "paper")  # repairs a file the app chokes on
        self.assertIn('theme = "paper"', read_text(os.path.join(self.home, "tui.toml")))

    def test_inside_claude_code_tui_toml_needs_the_guard(self):
        path = os.path.join(self.home, "tui.toml")
        p = self.fm("settings", "set", "theme", "paper", env=self.claude, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn(path, p.stdout + p.stderr)
        self.assertIn('theme = "paper"', p.stdout + p.stderr, "the exact change to make")
        self.assertEqual(read_text(path), '# mine\nborder = "heavy"\n')

    def test_a_config_dir_outside_home_is_refused(self):
        other = os.path.join(self.tmp, "cc")
        os.makedirs(other)
        with open(os.path.join(other, "settings.json"), "w") as f:
            f.write(self.before)
        p = self.fm("settings", "set", "palette", "cb", "--surface", "plugin", env=dict(self.env, CLAUDE_CONFIG_DIR=other),
                    check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(read_text(os.path.join(other, "settings.json")), self.before)

    def test_list_shows_both_surfaces_with_value_default_and_where(self):
        rows = json.loads(self.fm("settings", "list", "--json", env=self.env).stdout)
        by = {(r["surface"], r["key"]): r for r in rows}
        self.assertEqual((by["app", "border"]["value"], by["app", "border"]["default"]), ("heavy", "rounded"))
        self.assertEqual(by["app", "border"]["where"], os.path.join(self.home, "tui.toml"))
        self.assertEqual((by["plugin", "motion"]["value"], by["plugin", "motion"]["default"]), ("reduced", "full"))
        self.assertIn(self.settings, by["plugin", "motion"]["where"])
        self.assertIn("foreman-ui@foreman", by["plugin", "motion"]["where"])
        self.assertEqual(by["plugin", "mascot"]["value"], "blue", "unset: the default")
        text = self.fm("settings", "list", env=self.env).stdout
        self.assertIn("app", text)
        self.assertIn("plugin", text)
        self.assertIn("heavy", text)

    def test_get_shows_each_surface(self):
        out = self.fm("settings", "get", "motion", env=self.env).stdout
        self.assertIn("app", out)
        self.assertIn("plugin", out)
        self.assertIn("reduced", out)
        self.assertNotEqual(self.fm("settings", "get", "nosuch", env=self.env, check=False).returncode, 0)

    def test_an_app_set_writes_tui_toml_in_place(self):
        self.term("settings", "set", "theme", "paper")
        self.assertEqual(read_text(os.path.join(self.home, "tui.toml")), '# mine\nborder = "heavy"\ntheme = "paper"\n')

    def test_a_plugin_set_the_guard_protects_prints_the_change_and_writes_nothing(self):
        p = self.fm("settings", "set", "mascot", "orange", env=self.claude, check=False)
        self.assertEqual(p.returncode, 2)
        said = p.stdout + p.stderr
        for words in (self.settings, "pluginConfigs", "foreman-ui@foreman", '"mascot": "orange"'):
            self.assertIn(words, said)
        self.assertEqual(read_text(self.settings), self.before)

    def test_in_the_users_terminal_settings_json_is_written(self):
        self.term("settings", "set", "mascot", "orange")
        got = read_json(self.settings)
        self.assertEqual(got["pluginConfigs"]["foreman-ui@foreman"]["options"], {"motion": "calm", "mascot": "orange"})
        self.assertEqual((got["model"], got["pluginConfigs"]["other@m"]), ("x", {"options": {"a": 1}}))

    def test_a_plugin_set_the_guard_allows_keeps_the_rest_of_settings(self):
        other = os.path.join(self.uhome, "cc")  # a config folder of the user's the guard doesn't protect
        os.makedirs(other)
        with open(os.path.join(other, "settings.json"), "w") as f:
            f.write(self.before)
        self.fm("settings", "set", "palette", "cb", "--surface", "plugin", env=dict(self.claude, CLAUDE_CONFIG_DIR=other))
        got = read_json(os.path.join(other, "settings.json"))
        self.assertEqual(got["pluginConfigs"]["foreman-ui@foreman"]["options"], {"motion": "calm", "palette": "cb"})
        self.assertEqual((got["model"], got["pluginConfigs"]["other@m"]), ("x", {"options": {"a": 1}}))

    def test_a_shared_set_writes_what_it_may_and_says_what_the_rest_needs(self):
        other = os.path.join(self.uhome, "cc")
        os.makedirs(other)
        p = self.fm("settings", "set", "motion", "off", env=dict(self.claude, CLAUDE_CONFIG_DIR=other), check=False)
        self.assertEqual(p.returncode, 2, "the app half was refused")
        self.assertIn('motion = "off"', p.stdout + p.stderr)
        self.assertEqual(read_text(os.path.join(self.home, "tui.toml")), '# mine\nborder = "heavy"\n')
        self.assertEqual(read_json(os.path.join(other, "settings.json"))["pluginConfigs"]["foreman-ui@foreman"],
                         {"options": {"motion": "off"}})
        self.term("settings", "set", "motion", "off")  # the terminal: both
        self.assertIn('motion = "off"', read_text(os.path.join(self.home, "tui.toml")))
        self.assertEqual(read_json(self.settings)["pluginConfigs"]["foreman-ui@foreman"]["options"]["motion"], "off")

    def test_a_bad_plugin_value_is_refused(self):
        for key, value in (("freshAt", "500"), ("freshAt", "lots"), ("mascot", "pink"), ("motion", "wobbly")):
            p = self.fm("settings", "set", key, value, "--surface", "plugin", env=self.env, check=False)
            self.assertNotEqual(p.returncode, 0, (key, value))
        self.assertEqual(read_text(self.settings), self.before)


class PreviewApp(unittest.TestCase):
    """T-1573: the fm code app's preview refuses what set_app refuses, the guard's refusal too, and writes nothing."""
    def test_it_refuses_what_set_app_refuses_and_writes_nothing(self):
        import tempfile
        import unittest.mock as mock
        path, mine = os.path.join(tempfile.mkdtemp(), "tui.toml"), '# mine\ntheme = "night"\n'
        with open(path, "w", encoding="utf-8") as f:
            f.write(mine)
        bad = (("theme", "nope"), ("colors.ok", '"\udcff"'), ("colors.ok", {"fg": "\udcff"}), ("nope", "x"))
        with mock.patch.object(fmsettings, "in_claude_code", return_value=False):
            for key, value in bad:
                for fn in (fmsettings.set_app, fmsettings.preview_app):
                    with self.subTest(fn=fn.__name__, key=key, value=value), self.assertRaises(fmsettings.SettingError):
                        fn(key, value, path)
            value, cfg = fmsettings.preview_app("motion", "calm", path)
            self.assertEqual((value, cfg["motion"], cfg["preset"]), ("reduced", "reduced", "night"))
        with mock.patch.object(fmsettings, "in_claude_code", return_value=True), \
                mock.patch.object(fmsettings, "_guard_block", return_value="a protected file"):
            for fn in (fmsettings.set_app, fmsettings.preview_app):
                with self.subTest(fn=fn.__name__), self.assertRaises(fmsettings.SettingError) as e:
                    fn("theme", "paper", path)
                self.assertIn("guard", str(e.exception))
        self.assertEqual(read_text(path), mine, "nothing written")


class PluginSurface(unittest.TestCase):
    """T-1574: /foreman:settings runs fm settings (one implementation); the pane re-reads its options on each poll."""
    ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

    def test_the_command_lists_and_sets_through_fm_settings(self):
        text = read_text(os.path.join(self.ROOT, "plugin", "commands", "settings.md"))
        head, _, body = text.partition("\n---\n")
        self.assertTrue(head.startswith("---\n") and "\ndescription: " in head, "frontmatter with a description")
        self.assertIn("disable-model-invocation: true", head, "the person's command: no share of the skill listing")
        for cmd in ("fm settings list", "fm settings get", "fm settings set"):
            self.assertIn(f"`{cmd}", body, cmd)
        self.assertIn("$ARGUMENTS", body)

    def test_the_pane_applies_changed_options_on_its_poll(self):
        mod = os.path.join(self.ROOT, "mods", "foreman-ui")
        src = read_text(os.path.join(mod, "hooks", "register.tsx"))
        # a wiring check only: the behaviour's proof is the mod's own test, run by claude plugin test mods/foreman-ui
        poll = src[src.index("async function pollOptions("):src.index("async function tick(")]
        tick = src[src.index("async function tick("):src.index("async function gauge(")]
        self.assertIn("$.config.list()", poll, "the engine's current option values")
        self.assertIn("applyOptions(", poll)
        self.assertIn("pollOptions($)", tick, "read on every 2 s poll")
        tests = read_text(os.path.join(mod, "tests", "foreman-ui.test.tsx"))
        self.assertIn("applies on the next poll, no restart (T-1574)", tests, "claude plugin test runs the behaviour")


if __name__ == "__main__":
    unittest.main()
