"""T-1656: settings profiles. tui.toml's [profile.NAME] tables each hold a when clause on terminal facts (an ssh
session, inside tmux, TERM, the width, the colour depth) and settings; the fm code app applies the first one it meets
over the file's own settings, each value through the same checks, read through the same bounded reader. fm settings
profile lists them and names the one that applies here.

T-1657: rules. tui.toml's [[rule]] tables each hold a when clause on the run's events (verify, failing, running,
closed) and a layout or panel swap the app draws while it holds; an extension declares its settings (api.setting) and
they list, check and set as the app's own, under [ext.NAME]."""
import contextlib
import io
import json
import os
import types
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


class _Tui(ForemanTestCase):
    """A tui.toml in a fresh Foreman home, on a bare terminal, outside Claude Code."""
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

    def set(self, key, value):
        """fm settings set KEY VALUE --surface app in this process (a subprocess has no terminal: the guard decides)."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            fmsettings.cmd_settings(types.SimpleNamespace(action="set", key=key, value=value, surface="app",
                                                          json=False, project=None))
        return out.getvalue()


class Profile(_Tui):
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
            self.assertEqual(T._setting_row(row, 100)[0][0], "◆ ", "a glyph in the first column")
            app.item_index = app.items.index(row)
            about = "".join(t for t, _ in T._settings_foot(app, 100)[1])
            self.assertIn("set by profile tmux here", about)

    def test_a_name_from_the_file_never_forges_a_line(self):
        name = "x\\n  evil \\u202e ← applies"  # TOML escapes: a line break and a right-to-left override
        self.write(f'[profile."{name}"]\nwhen = {{ tmux = true }}\nmotion = "off"\n')
        here = dict(self.env, TMUX="/tmp/t")
        outs = [self.fm("settings", *a, env=here).stdout for a in (("profile",), ("list", "look"), ("get", "motion"))]
        with mock.patch.dict(os.environ, {"TMUX": "/tmp/t"}):
            outs.append(self.set("motion", "reduced"))
        for out in outs:
            self.assertNotIn("‮", out)
            self.assertFalse([x for x in out.splitlines() if x.startswith("  evil")], out)
            self.assertIn("\\n", out)

    def test_with_no_terminal_and_no_columns_the_width_is_unknown(self):
        self.write(PROFILES)
        here = dict(self.env, SSH_CONNECTION="10.0.0.2 5000 10.0.0.1 22", COLUMNS="0")  # 0: not a width
        got = json.loads(self.fm("settings", "profile", "--json", env=here).stdout)
        self.assertEqual((got["facts"]["width"], got["active"]), (None, None), "width_below never meets no width")
        self.assertIn("columns unknown (no terminal)", self.fm("settings", "profile", env=here).stdout)

    def test_a_set_names_each_profile_that_overrides_the_key(self):
        self.write(PROFILES)
        out = self.set("motion", "reduced")
        self.assertIn("profile phone also sets motion: it overrides on terminals where "
                      "{ ssh = true, width_below = 100 } holds", out)
        self.assertIn("profile kitty also sets motion", out)
        self.assertNotIn("also sets", self.set("palette", "cb"))
        app = T.App(T.load_config(self.toml, env=BARE)[0], spawn=lambda *a, **k: None)
        app.show_settings()
        app._settings_set("set layout.narrow_below 90")
        self.assertIn("profile phone also sets layout.narrow_below", app.set_note[0])

    def test_an_empty_when_is_refused(self):
        self.write('[profile.e]\nwhen = {}\nmotion = "off"\n')
        cfg, errors = self.load()
        self.assertEqual((cfg["motion"], cfg.get("profile")), (T.DEFAULTS["motion"], None))
        self.assertIn("profile.e.when: empty", errors[0])

    def test_the_profile_sets_only_what_landed_by_the_key_it_means(self):
        self.write('[profile.t]\nwhen = { tmux = true }\n[profile.t.keys]\nENTER = "nope"\nq = "none"\n')
        self.assertEqual(self.load(TMUX="/tmp/t")[0]["profile"]["sets"], ["keys.q"])

    def test_print_config_prints_the_profile_tables_not_their_values_baked_in(self):
        import tomllib
        self.write(PROFILES)
        here = dict(self.env, TMUX="/tmp/t")
        out = self.fm("code", "tui", "--print-config", env=here).stdout
        self.assertIn('border = "heavy"', out, "the file's own value, not tmux's")
        self.assertIn("[profile.phone]", out)
        got = tomllib.loads(out)
        self.assertEqual(got["profile"]["phone"]["when"], {"ssh": True, "width_below": 100})
        self.assertEqual(got["profile"]["phone"]["layout"], {"narrow_below": 200})
        with open(self.toml, "w", encoding="utf-8") as f:
            f.write(out)
        self.assertEqual(self.load(TMUX="/tmp/t")[0]["border"], "double", "it loads back with its profiles")

    def test_a_profile_problem_isnt_said_as_the_default_showing(self):
        self.write('[profile.c]\nwhen = { tmux = true }\nmotion = "fast"\n[profile.d]\nmotion = "off"\n')
        out = self.fm("settings", "list", "look", env=dict(self.env, TMUX="/tmp/t")).stdout
        lines = [x for x in out.splitlines() if "profile." in x]
        self.assertEqual(len(lines), 2, out)
        self.assertFalse([x for x in lines if "the default shows" in x], lines)
        self.assertEqual(sorted("passed over" in x for x in lines), [False, True], lines)

    def test_export_says_profiles_arent_carried(self):
        self.assertIn("[profile] tables aren't in it", " ".join(self.fm("settings", "--help").stdout.split()))


RUN = [{"event": "start", "schema": 1, "request": "fix it", "task": "T-1"},
       {"event": "plan", "plan": {"title": "fix it", "criteria": [{"text": "tests pass", "verify": "make test"}],
                                  "steps": ["edit"]}},
       {"event": "task", "task": "T-1"}, {"event": "step", "step": 1}]
PASSED = {"event": "verify", "criterion": 1, "label": "verify", "cmd": "make test", "exit": 0}
FAILED = dict(PASSED, exit=1, output="1 failed")
CLOSED = {"event": "closed", "task": "T-1", "text": "closed T-1 abc1234"}
RULES = '''[[rule]]
when = { verify = true }
layout = { columns = [["verify"], ["checks"]], widths = [60, 40] }
'''
DEMO = '''def setup(api):
    api.setting("refresh", "int", 5, "seconds between polls", range=(1, 60))
    api.setting("mode", "choice", "fast", "how it polls", choices=("fast", "slow"))
'''


class Rules(_Tui):
    def setUp(self):
        super().setUp()
        saved = (dict(T.EXT_SETTINGS), dict(T.DEFAULTS["ext"]), set(T.EXT_LOADED))

        def put_back():
            for live, was in zip((T.EXT_SETTINGS, T.DEFAULTS["ext"], T.EXT_LOADED), saved):
                live.clear()
                live.update(was)
        self.addCleanup(put_back)

    def app(self, cfg):
        app = T.App(cfg, spawn=lambda *a, **k: None)
        for e in RUN:
            app.feed(e)
        return app

    def shown(self, app):
        return T.render(app.state, 120, 34, app.cfg, app).text()

    def demo(self):
        api = T.API("demo")
        api.setting("refresh", "int", 5, "seconds between polls", range=(1, 60))
        api.setting("mode", "choice", "fast", "how it polls", choices=("fast", "slow"))
        api.setting("loud", "bool", False, "a bell when a check fails")

    def test_a_rule_switches_the_layout_while_verify_runs_and_back_after(self):
        self.write(RULES)
        cfg, errors = self.load()
        self.assertEqual(errors, [])
        app = self.app(cfg)
        self.assertNotIn("Check output", self.shown(app), "no check yet: the file's own layout")
        app.feed(PASSED)
        self.assertIn("Check output", self.shown(app), "the checks running: the rule's layout")
        self.assertNotIn("Activity", self.shown(app))
        app.feed(CLOSED)
        self.assertNotIn("Check output", self.shown(app), "the run closed: back to the file's layout")
        self.assertEqual(T.rule_layout(cfg, app.state), cfg["layout"])

    def test_a_rule_swaps_a_panel_while_a_check_fails(self):
        self.write('[[rule]]\nwhen = { failing = true }\npanels = { log = "verify" }\n')
        app = self.app(self.load()[0])
        app.feed(FAILED)
        self.assertIn("Check output", self.shown(app))
        self.assertNotIn("Activity", self.shown(app))
        app.feed(PASSED)
        self.assertIn("Activity", self.shown(app), "the check passes again: the log is back")

    def test_the_layout_editor_shows_the_files_layout_not_a_rules(self):
        self.write(RULES)
        app = self.app(self.load()[0])
        app.feed(PASSED)
        app.mode = "layout"
        self.assertIn("Activity", self.shown(app))

    def test_an_unknown_event_or_key_is_said_once_and_skipped(self):
        self.write('[[rule]]\nwhen = { lane = true }\nlayout = { top = [] }\n'
                   '[[rule]]\nlayout = { top = [] }\n'
                   '[[rule]]\nwhen = { verify = "yes" }\n'
                   '[[rule]]\nwhen = { verify = true }\ncolour = "red"\nlayout = { columns = [["nope"]] }\n'
                   'panels = { log = "nope" }\n')
        cfg, errors = self.load()
        said = "\n".join(errors)
        for word in ("rule.1.when.lane: not an event", "rule.2.when: a table of events", "rule.3.when.verify = 'yes'",
                     "rule.4.colour: not a rule setting", "rule.4.layout.columns: no panel 'nope'", "rule.4.panels.log"):
            self.assertIn(word, said)
        self.assertEqual(len(errors), 6, "each said once")
        self.assertEqual(cfg["rules"], [{"when": {"verify": True}, "layout": {}, "panels": {}}])
        app = self.app(cfg)
        app.feed(FAILED)
        self.assertIn("Activity", self.shown(app), "nothing left to switch: the file's layout")
        self.write("rule = 3\n")
        self.assertIn("rule: a [[rule]] table per rule", self.load()[1][0])
        out = self.fm("settings", "list", "layout", env=self.env).stdout
        self.assertIn("rule: a [[rule]] table per rule: passed over", out)
        self.assertNotIn("the default shows", out)
        self.write('[[rule]]\nwhen = { closed = true }\npanels = { log = "verify" }\n' * (T.RULES_MAX + 1))
        cfg, errors = self.load()
        self.assertEqual((len(cfg["rules"]), errors), (T.RULES_MAX, [f"{self.toml}: rule.{T.RULES_MAX + 1} on: "
                                                                       f"{T.RULES_MAX} rules at most: passed over"]))

    def test_a_rule_the_app_cant_draw_with_starts_the_last_good_settings(self):
        real = T.render

        def picky(st, w, h, cfg, *a, **k):
            if cfg["layout"].get("narrow_below") == 7:
                raise ZeroDivisionError("a layout it can't draw")
            return real(st, w, h, cfg, *a, **k)
        self.write('border = "heavy"\n')
        fmsettings.boot()
        self.write('border = "heavy"\n[[rule]]\nwhen = { verify = true }\nlayout = { narrow_below = 7 }\n')
        with mock.patch.object(T, "render", side_effect=picky):
            cfg, _, note, _ = fmsettings.boot()
        self.assertIn("last good", note)
        self.assertIsNone(cfg.get("rules"))

    def test_print_config_prints_the_rules_and_they_load_back(self):
        import tomllib
        self.write(RULES + '[[rule]]\nwhen = { failing = true, running = true }\npanels = { log = "verify" }\n')
        out = self.fm("code", "tui", "--print-config", env=self.env).stdout
        self.assertEqual(out.count("[[rule]]"), 2, out)
        self.assertEqual(tomllib.loads(out)["rule"], tomllib.loads(RULES + '[[rule]]\nwhen = { failing = true, '
                                                                          'running = true }\npanels = { log = '
                                                                          '"verify" }\n')["rule"])
        self.assertNotIn("dead", self.fm("settings", "diff", env=self.env).stdout, "a rule isn't a dead setting")

    def test_an_extensions_settings_load_check_and_set_as_the_apps_own(self):
        self.demo()
        self.write('[ext.demo]\nrefresh = 99\nmode = "slow"\nnope = 1\n[ext.ghost]\nx = 1\n')
        cfg, errors = self.load()
        self.assertEqual(cfg["ext"]["demo"], {"refresh": 5, "mode": "slow", "loud": False})
        said = "\n".join(errors)
        for word in ("ext.demo.refresh = 99: from 1 to 60", "ext.demo.nope: not a setting of demo",
                     "ext.ghost: no extension"):
            self.assertIn(word, said)
        self.write("")
        self.assertEqual(fmsettings.set_app("ext.demo.refresh", "10")[0], 10)
        self.assertEqual(fmsettings.set_app("ext.demo.loud", "true")[0], True)
        self.assertIn("[ext.demo]", read_text(self.toml))
        self.assertEqual(self.load()[0]["ext"]["demo"], {"refresh": 10, "mode": "fast", "loud": True})
        for key, value in (("ext.demo.refresh", "0"), ("ext.demo.loud", "maybe"), ("ext.demo.mode", "slower"),
                           ("ext.demo.nope", "1")):
            with self.assertRaises(fmsettings.SettingError, msg=key):
                fmsettings.set_app(key, value)
        self.assertEqual(fmsettings.diff(), [
            {"surface": "app", "key": "ext.demo.refresh", "value": 10, "default": 5},
            {"surface": "app", "key": "ext.demo.loud", "value": True, "default": False}])
        self.write('[ext.demo]\nrefresh = 10\n')
        fmsettings.set_app("ext.demo.refresh", None)
        self.assertNotIn("refresh", read_text(self.toml), "an undo removes it")

    def test_the_settings_screen_lists_an_extensions_keys_under_its_own_group(self):
        self.demo()
        self.write('[ext.demo]\nmode = "slow"\n')
        cfg, _, _, _ = fmsettings.boot()
        app = T.App(cfg, spawn=lambda *a, **k: None)
        app.show_settings()
        row = next(r for r in app.set_rows if r["key"] == "ext.demo.mode")
        self.assertEqual((row["group"], row["value"], row["default"], row["choices"]),
                         ("ext.demo", "slow", "fast", ["fast", "slow"]))
        head = next(r for r in app.items if r.get("head") == "ext.demo")
        self.assertIn("DEMO", T._setting_row(head, 100)[0][0])
        app._settings_set("set ext.demo.refresh 30")
        self.assertEqual(app.cfg["ext"]["demo"]["refresh"], 30)

    def test_a_bad_declaration_is_refused_when_the_extension_loads(self):
        for args, kw in ((("Bad key", "int", 1, "h"), {}), (("n", "colour", 1, "h"), {}),
                         (("n", "int", 0, "h"), {"range": (1, 9)}), (("n", "choice", "x", "h"), {"choices": ("a",)}),
                         (("n", "choice", "a", "h"), {}), (("n", "bool", "yes", "h"), {})):
            with self.assertRaises(ValueError, msg=args):
                T.API("demo").setting(*args, **kw)
        with self.assertRaises(ValueError):
            T.API("we.ird").setting("n", "int", 1, "h")
        with self.assertRaises(ValueError):
            T.API().setting("n", "int", 1, "h")
        self.assertNotIn("demo", T.EXT_SETTINGS)

    def test_fm_settings_lists_and_sets_an_extensions_keys(self):
        folder = os.path.join(self.home, "tui")
        os.makedirs(folder)
        path = os.path.join(folder, "demo.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(DEMO)
        os.chmod(path, 0o644)
        out = self.fm("settings", "list", "ext.demo", env=self.env).stdout
        self.assertIn("ext.demo.refresh", out)
        self.assertIn("ext.demo.mode", out)
        no = self.fm("settings", "set", "ext.demo.refresh", "0", env=self.env, check=False)
        self.assertNotEqual(no.returncode, 0)
        self.assertIn("ext.demo.refresh = 0: from 1 to 60", no.stdout)
        # a subprocess has no terminal: the guard decides, and says the change as the [ext.demo] line it needs
        said = self.fm("settings", "set", "ext.demo.refresh", "12", env=self.env, check=False).stdout
        self.assertIn("under [ext.demo], refresh = 12", said)
        self.assertIn("ext.demo.refresh 5", " ".join(self.fm("settings", "get", "ext.demo.refresh",
                                                            env=self.env).stdout.split()))

    def test_the_command_says_how_rules_and_extension_settings_are_set(self):
        body = read_text(os.path.join(os.path.dirname(__file__), "..", "commands", "settings.md"))
        self.assertIn("[[rule]]", body)
        self.assertIn("ext.NAME", body)
