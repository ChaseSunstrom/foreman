"""T-1656: settings profiles. tui.toml's [profile.NAME] tables each hold a when clause on terminal facts (an ssh
session, inside tmux, TERM, the width, the colour depth) and settings; the fm code app applies the first one it meets
over the file's own settings, each value through the same checks, read through the same bounded reader. fm settings
profile lists them and names the one that applies here."""
import json
import os
import unittest.mock as mock

from helpers import ForemanTestCase, read_text

import fmcodetui as T
import fmsettings

PROFILES = '''motion = "full"
border = "heavy"

[profile.phone]
when = { ssh = true, width_below = 100 }
motion = "off"
[profile.phone.layout]
narrow_below = 200

[profile.tmux]
when = { tmux = true }
border = "double"

[profile.kitty]
when = { term = "xterm-kit*", colors = 24 }
motion = "reduced"
'''
# a terminal with none of the facts: what the test runner's own (tmux, ssh) can't leak into
BARE = {"TERM": "xterm", "COLUMNS": "120", "TMUX": "", "SSH_CONNECTION": "", "SSH_CLIENT": "", "SSH_TTY": "",
        "COLORTERM": "", "NO_COLOR": ""}


class Profile(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.toml = os.path.join(self.home, "tui.toml")
        uhome = os.path.join(self.tmp, "uhome")
        os.makedirs(os.path.join(uhome, ".claude"))
        self.env = dict(BARE, HOME=uhome, CLAUDECODE="", CLAUDE_CODE_ENTRYPOINT="")
        self.patches = [mock.patch.dict(os.environ, self.env),
                        mock.patch.object(fmsettings, "in_claude_code", return_value=False)]
        for x in self.patches:
            x.start()
        os.environ.pop("CLAUDE_CONFIG_DIR", None)

    def tearDown(self):
        for x in reversed(self.patches):
            x.stop()
        super().tearDown()

    def write(self, text):
        with open(self.toml, "w", encoding="utf-8") as f:
            f.write(text)

    def load(self, **env):
        return T.load_config(self.toml, env=dict(BARE, **env))

    def test_the_first_profile_the_terminal_meets_applies_over_the_file(self):
        self.write(PROFILES)
        cfg, errors = self.load()
        self.assertEqual((cfg["motion"], cfg["border"], cfg.get("profile"), errors), ("full", "heavy", None, []))
        ssh = {"SSH_CONNECTION": "10.0.0.2 5000 10.0.0.1 22", "TMUX": "/tmp/tmux-1/default,1,0"}
        cfg, errors = self.load(COLUMNS="80", **ssh)
        self.assertEqual((cfg["motion"], cfg["border"], cfg["layout"]["narrow_below"]), ("off", "heavy", 200),
                         "phone, first in the file, wins over tmux")
        self.assertEqual((cfg["profile"]["name"], errors), ("phone", []))
        self.assertEqual(set(cfg["profile"]["sets"]), {"motion", "layout.narrow_below"})
        cfg, _ = self.load(**ssh)  # 120 columns: not narrow enough for phone
        self.assertEqual((cfg["profile"]["name"], cfg["border"], cfg["motion"]), ("tmux", "double", "full"))
        self.assertEqual(self.load(TERM="xterm-kitty", COLORTERM="truecolor")[0]["motion"], "reduced")
        self.assertIsNone(self.load(TERM="xterm-kitty")[0].get("profile"), "8 colours: kitty wants 24")

    def test_a_profile_goes_through_the_schema_and_a_bad_one_is_said(self):
        self.write('border = "heavy"\n[profile.a]\nwhen = { tmux = true, shell = "zsh" }\nborder = "double"\n'
                   '[profile.b]\nborder = "double"\n'
                   '[profile.c]\nwhen = { tmux = true }\nmotion = "fast"\nborder = "rounded"\n[profile.c.colors]\n'
                   'nope = "#ffffff"\n')
        cfg, errors = self.load(TMUX="/tmp/t")
        self.assertEqual((cfg["profile"]["name"], cfg["border"], cfg["motion"]), ("c", "rounded", "full"),
                         "a and b passed over; c's good value applies, its bad ones are skipped")
        said = "\n".join(errors)
        for word in ("profile.a.when.shell", "profile.b: no when", "profile.c.motion = 'fast'",
                     "profile.c.colors.nope"):
            self.assertIn(word, said)
        self.assertTrue(all(e.startswith(f"{self.toml}: profile.") for e in errors), errors)
        self.write('[profile]\nphone = 3\n')
        self.assertIn("profile.phone: a table", self.load()[1][0])
        self.write('profile = 3\n')
        self.assertIn("profile: a [profile.NAME] table", self.load()[1][0])
        self.write('[profile.x]\nwhen = { term = "' + "*a" * 200 + '" }\n')
        self.assertIn("profile.x.when.term", self.load()[1][0])

    def test_a_bad_profile_value_never_refuses_the_files_own_setting(self):
        self.write('[profile.c]\nwhen = { tmux = true }\nmotion = "fast"\n')
        with mock.patch.dict(os.environ, {"TMUX": "/tmp/t"}):
            self.assertEqual(fmsettings.set_app("motion", "off")[0], "off")
            self.assertNotIn(("app", "profile"), fmsettings.written(), "not a dead setting")
            self.assertEqual(fmsettings.diff(), [{"surface": "app", "key": "motion", "value": "off",
                                                  "default": T.DEFAULTS["motion"]}])

    def test_a_profile_the_app_cant_draw_with_starts_the_last_good_settings(self):
        real = T.render

        def picky(st, w, h, cfg, *a, **k):
            if cfg["layout"].get("narrow_below") == 7:
                raise ZeroDivisionError("a layout it can't draw")
            return real(st, w, h, cfg, *a, **k)
        self.write('border = "heavy"\n')
        fmsettings.boot()
        self.write('border = "heavy"\n[profile.t]\nwhen = { tmux = true }\n[profile.t.layout]\nnarrow_below = 7\n')
        with mock.patch.object(T, "render", side_effect=picky), mock.patch.dict(os.environ, {"TMUX": "/tmp/t"}):
            cfg, _, note, _ = fmsettings.boot()
        self.assertIn("last good", note)
        self.assertEqual((cfg["layout"]["narrow_below"], cfg["border"], cfg.get("profile")),
                         (T.DEFAULTS["layout"]["narrow_below"], "heavy", None), "the good copy has no profile")

    def test_profiles_are_read_through_the_bounded_reader(self):
        os.mkfifo(self.toml)  # a FIFO would block a plain open
        got = fmsettings.profiles(env=BARE)
        self.assertEqual(got["profiles"], [])
        self.assertIn("not a regular file", got["problems"][0])
        os.unlink(self.toml)
        self.write("#" * (fmsettings.APP_MAX + 10))
        self.assertIn("over 1 MB", fmsettings.profiles(env=BARE)["problems"][0])

    def test_fm_settings_profile_lists_them_and_names_the_one_that_applies(self):
        self.write(PROFILES)
        here = dict(self.env, SSH_CONNECTION="10.0.0.2 5000 10.0.0.1 22", COLUMNS="80")
        got = json.loads(self.fm("settings", "profile", "--json", env=here).stdout)
        self.assertEqual(got["active"], "phone")
        self.assertEqual([p["name"] for p in got["profiles"]], ["phone", "tmux", "kitty"])
        self.assertEqual([p["matches"] for p in got["profiles"]], [True, False, False])
        self.assertEqual((got["facts"]["ssh"], got["facts"]["width"], got["facts"]["tmux"]), (True, 80, False))
        text = self.fm("settings", "profile", env=dict(here, CLAUDECODE="1")).stdout  # from Claude Code too
        self.assertIn("phone", text)
        self.assertIn("applies", text)
        self.assertIn("ssh = true", text)
        self.assertIn("none applies", self.fm("settings", "profile", env=self.env).stdout)
        self.assertIn("profile phone", self.fm("settings", "list", env=here).stdout)
        body = read_text(os.path.join(os.path.dirname(__file__), "..", "commands", "settings.md"))
        self.assertIn("`fm settings profile`", body)

    def test_the_settings_screen_names_the_profile(self):
        self.write(PROFILES)
        with mock.patch.dict(os.environ, {"TMUX": "/tmp/t"}):
            cfg, _, _, _ = fmsettings.boot()
            app = T.App(cfg, spawn=lambda *a, **k: None)
            app.show_settings()
            self.assertIn("profile tmux", T._settings_note(app))
            row = next(r for r in app.set_rows if r["key"] == "border")
            self.assertEqual((row["value"], row.get("profile")), ("double", "tmux"))
