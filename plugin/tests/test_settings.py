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
        self.env = {"HOME": self.uhome}

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
        self.fm("settings", "set", "theme", "paper", env=self.env)
        self.assertEqual(read_text(os.path.join(self.home, "tui.toml")), '# mine\nborder = "heavy"\ntheme = "paper"\n')

    def test_a_plugin_set_the_guard_protects_prints_the_change_and_writes_nothing(self):
        p = self.fm("settings", "set", "mascot", "orange", env=self.env, check=False)
        self.assertNotEqual(p.returncode, 0)
        said = p.stdout + p.stderr
        for words in (self.settings, "pluginConfigs", "foreman-ui@foreman", '"mascot": "orange"'):
            self.assertIn(words, said)
        self.assertEqual(read_text(self.settings), self.before)

    def test_a_plugin_set_the_guard_allows_keeps_the_rest_of_settings(self):
        other = os.path.join(self.tmp, "cc")
        os.makedirs(other)
        with open(os.path.join(other, "settings.json"), "w") as f:
            f.write(self.before)
        self.fm("settings", "set", "palette", "cb", "--surface", "plugin", env=dict(self.env, CLAUDE_CONFIG_DIR=other))
        got = read_json(os.path.join(other, "settings.json"))
        self.assertEqual(got["pluginConfigs"]["foreman-ui@foreman"]["options"], {"motion": "calm", "palette": "cb"})
        self.assertEqual((got["model"], got["pluginConfigs"]["other@m"]), ("x", {"options": {"a": 1}}))

    def test_a_shared_set_writes_the_app_and_says_what_the_plugin_needs(self):
        p = self.fm("settings", "set", "motion", "off", env=self.env, check=False)
        self.assertNotEqual(p.returncode, 0, "the plugin half was refused")
        self.assertIn('motion = "off"', read_text(os.path.join(self.home, "tui.toml")))
        self.assertIn('"motion": "off"', p.stdout + p.stderr)
        self.assertEqual(read_text(self.settings), self.before)

    def test_a_bad_plugin_value_is_refused(self):
        for key, value in (("freshAt", "500"), ("freshAt", "lots"), ("mascot", "pink"), ("motion", "wobbly")):
            p = self.fm("settings", "set", key, value, "--surface", "plugin", env=self.env, check=False)
            self.assertNotEqual(p.returncode, 0, (key, value))
        self.assertEqual(read_text(self.settings), self.before)


if __name__ == "__main__":
    unittest.main()
