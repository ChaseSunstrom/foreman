"""T-1661: the Control Room's extras. fm settings serve draws the layout as a grid of panels with ← ↑ ↓ → buttons
(columns and heights in one write, one undo, as the app's layout editor); numbers turn by detents (a range dial with
ticks for a closed range, a stepped number for an open one, [ and ] in the app's settings screen); fm settings newcomer
plays a first-time user through the settings screen with only what it shows, writes nothing and names where it got
stuck."""
import contextlib
import io
import json
import os
import threading
import unittest.mock as mock

import test_settings_serve as serve
from helpers import ForemanTestCase, read_text

import fmcli
import fmcodetui as T
import fmideas
import fmsettings
import fmsettingsserve

COLS = [["log", "files"], ["checks", "time", "tokens"]]  # files moved to the left column from the defaults
HTS = [[1, "auto"], ["auto", "auto", 1]]


def entry(key, surface=None):
    return fmsettings.find(key, surface)[0]


class _Room(ForemanTestCase):
    """A home with no tui.toml, outside Claude Code; the page served on demand."""
    req, login, post = serve.Serve.req, serve.Serve.login, serve.Serve.post

    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")
        os.makedirs(os.path.join(self.uhome, ".claude"))
        self.toml = os.path.join(self.home, "tui.toml")
        self.settings = os.path.join(self.uhome, ".claude", "settings.json")
        for x in (mock.patch.dict(os.environ, {"HOME": self.uhome}),
                  mock.patch.object(fmsettings, "in_claude_code", return_value=False)):
            x.start()
            self.addCleanup(x.stop)
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
        self.cookie = None

    def serve(self):
        self.server, self.token = fmsettingsserve.make()
        self.port, stop = self.server.server_address[1], threading.Event()
        t = threading.Thread(target=fmsettingsserve.serve, args=(self.server, 30, stop), daemon=True)
        t.start()
        self.addCleanup(lambda: (stop.set(), t.join(5)))


class Pure(_Room):
    def test_layout_moved_moves_refuses_an_only_panel_and_stops_at_the_edge(self):
        lay = T.DEFAULTS["layout"]
        self.assertEqual(fmsettings.layout_moved(lay, 1, 1, -1, 0), (COLS, HTS, "files", 0, 1))
        self.assertIsNone(fmsettings.layout_moved(lay, 1, 0, 0, -1), "the top: nowhere to go")
        self.assertIsNone(fmsettings.layout_moved(lay, 1, 0, 1, 0), "the right edge")
        with self.assertRaisesRegex(fmsettings.SettingError, "only panel"):
            fmsettings.layout_moved(lay, 0, 0, 1, 0)
        self.assertEqual(lay["columns"][0], ["log"], "the defaults untouched")

    def test_a_closed_range_turns_on_a_1_2_5_grid_and_an_open_one_climbs_a_ladder(self):
        fresh, tokens, narrow = entry("freshAt", "plugin"), entry("freshTokens", "plugin"), entry("layout.narrow_below")
        self.assertEqual([fmsettings.detent(fresh, v, n) for v, n in ((60, 1), (63, 1), (63, -1), (100, 1), (0, -1))],
                         [65, 65, 60, 100, 0])
        self.assertEqual([fmsettings.detent(tokens, v, n) for v, n in ((150000, 1), (150000, -1), (0, 1), (0, -1))],
                         [200000, 100000, 1, 0])
        self.assertEqual((fmsettings.detent(narrow, 80, 1), fmsettings.detent(narrow, 80, -1)), (100, 50))
        with self.assertRaises(fmsettings.SettingError):
            fmsettings.detent(entry("border"), "rounded", 1)

    def test_a_fractional_dial_turns_off_a_value_float_division_lands_under(self):
        e = dict(entry("freshAt", "plugin"), type="number", range=(0, 1), key="x")
        self.assertEqual((fmsettings.detent(e, 0.3, 1), fmsettings.detent(e, 0.3, -1)), (0.35, 0.25))


class Page(_Room):
    def setUp(self):
        super().setUp()
        self.serve()

    def move(self, **fields):
        self.cookie or self.login()
        h = {"Content-Type": "application/x-www-form-urlencoded", "Origin": f"http://127.0.0.1:{self.port}"}
        return self.req("POST", "/move", "&".join(f"{k}={v}" for k, v in fields.items()), h)

    def test_the_layout_is_a_grid_of_panels_with_the_moves_each_can_make(self):
        page = fmsettingsserve.page("n", "")
        self.assertIn('class="grid"', page)
        for name in ("log", "checks", "files", "time", "tokens"):
            self.assertIn(f"<b>{name}</b>", page)
        self.assertEqual(page.count('action="/move"'), 5 * 4, "four buttons a panel")
        log = page[page.index("<b>log</b>"):page.index("<b>checks</b>")]
        self.assertEqual(log.count("disabled"), 4, "log is its column's only panel at both edges: no move")
        self.assertNotIn("<script", page)

    def test_a_move_writes_columns_and_heights_as_one_undo(self):
        status, body, _ = self.move(c=1, i=1, dc=-1, di=0)
        self.assertEqual(status, 200, body)
        self.assertIn("files moved", body)
        lay = T.load_config(self.toml)[0]["layout"]
        self.assertEqual((lay["columns"], lay["heights"]), (COLS, HTS))
        fmsettings.undo()
        self.assertEqual(T.load_config(self.toml)[0]["layout"]["columns"], T.DEFAULTS["layout"]["columns"])

    def test_a_bad_move_is_refused_and_writes_nothing(self):
        for fields, word in (({"c": 0, "i": 0, "dc": 1, "di": 0}, "only panel"), ({"c": 9, "i": 0, "dc": 0, "di": 1},
                             "nowhere"), ({"c": "x", "i": 0, "dc": 0, "di": 1}, "whole numbers"),
                             ({"c": 0, "i": 0, "dc": 2, "di": 0}, "one step")):
            status, body, _ = self.move(**fields)
            self.assertEqual(status, 422, fields)
            self.assertIn(word, body)
        self.assertFalse(os.path.exists(self.toml))

    def test_a_move_from_a_stale_page_moves_nothing(self):
        status, body, _ = self.move(c=1, i=1, dc=-1, di=0, name="time")
        self.assertEqual(status, 422)
        self.assertIn("changed", body)
        self.assertFalse(os.path.exists(self.toml))
        self.assertEqual(self.move(c=1, i=1, dc=-1, di=0, name="files")[0], 200)

    def test_enter_in_a_number_sets_what_was_typed(self):
        page = fmsettingsserve.page("n", "")
        form = page[page.rindex("<form", 0, page.index(">layout.narrow_below<")):]
        form = form[:form.index("</form>")]
        self.assertTrue(form[form.index("<button"):].startswith("<button>set</button>"),
                        "the form's first button is the one Enter presses")
        self.assertIn('aria-label="layout.narrow_below up one detent"', form)

    def test_closed_ranges_are_dials_with_ticks_and_open_ones_stepped_numbers(self):
        page = fmsettingsserve.page("n", "")
        fresh = page[page.index(">freshAt<"):][:900]
        self.assertIn('type="range" min="0" max="100" step="any"', fresh)
        self.assertIn('<datalist id="ticks-plugin-freshAt"><option value="0"><option value="5">', fresh)
        narrow = page[page.index(">layout.narrow_below<"):][:600]
        self.assertIn('type="number" min="0" step="1"', narrow)
        self.assertEqual(narrow.count('name="turn"'), 2, "a turn down and up: one detent each")

    def test_a_turn_posted_moves_one_detent_from_the_value_shown(self):
        self.assertEqual(self.post({"key": "layout.narrow_below", "surface": "app", "value": "80", "turn": "1"})[0],
                         200)
        self.assertEqual(T.load_config(self.toml)[0]["layout"]["narrow_below"], 100)
        self.assertEqual(self.post({"key": "layout.narrow_below", "surface": "app", "value": "100", "turn": "-1"})[0],
                         200)
        self.assertEqual(T.load_config(self.toml)[0]["layout"]["narrow_below"], 50, "the 1-2-5 ladder down")
        status, body, _ = self.post({"key": "border", "surface": "app", "value": "rounded", "turn": "1"})
        self.assertEqual(status, 422)
        self.assertIn("a number", body)
        self.assertEqual(self.post({"key": "layout.narrow_below", "surface": "app", "value": "80", "turn": "5"})[0],
                         422)


class Turn(_Room):
    """The app's settings screen: [ and ] turn the selected number."""
    def app(self):
        app = T.App(T.load_config(self.toml)[0], spawn=lambda *a, **k: None)
        app.show_settings()
        return app

    def pick(self, app, key):
        app.item_index = next(i for i, r in enumerate(app.items) if r.get("key") == key)

    def test_brackets_turn_the_selected_number_and_say_so_elsewhere(self):
        app = self.app()
        self.assertIn("[ ]  turn", T.render(app.state, 120, 40, app.cfg, app).text())
        self.pick(app, "layout.narrow_below")
        app.key("]")
        self.assertEqual(T.load_config(self.toml)[0]["layout"]["narrow_below"], 100)
        self.pick(app, "layout.narrow_below")
        app.key("[")
        app.key("[")
        self.assertEqual(T.load_config(self.toml)[0]["layout"]["narrow_below"], 20, "100, 50, 20: each from the last")
        before = read_text(self.toml)
        self.pick(app, "border")
        app.key("]")
        self.assertEqual(app.set_note[1], "bad")
        self.assertIn("a number", app.set_note[0])
        self.assertEqual(read_text(self.toml), before)

    def test_on_a_narrow_screen_the_hints_wrap_onto_the_spare_note_line(self):
        app = self.app()
        for w in (120, 100, 80):
            screen = T.render(app.state, w, 30, app.cfg, app).text()
            for hint in ("[ ]  turn", "l  layout", "r  runners", "Esc  close"):
                self.assertIn(hint, screen, w)


class Newcomer(_Room):
    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fmcli.main(["settings", "newcomer", *args])
        return rc, out.getvalue()

    def test_the_scripted_newcomer_reaches_each_goal_and_writes_nothing(self):
        got = fmsettings.newcomer()
        self.assertTrue(got and all(g["done"] for g in got), got)
        self.assertFalse(os.path.exists(self.toml))
        self.assertFalse(os.path.exists(self.settings))
        rc, out = self.run_cli()
        self.assertEqual(rc, 0, out)
        self.assertIn("✓", out)
        self.assertIn("nothing written", out)

    def test_where_it_got_stuck_names_the_step_and_the_hint_missing(self):
        hints = tuple(h for h in T._SET_HINTS if h[0] != "[ ]")
        with mock.patch.object(T, "_SET_HINTS", hints):
            got = fmsettings.newcomer()
        stuck = [g for g in got if not g["done"]]
        self.assertEqual(len(stuck), 1, got)
        self.assertEqual((stuck[0]["step"], stuck[0]["missing"]), (2, "[ ]  turn"))
        goals = os.path.join(self.tmp, "goals.json")
        with open(goals, "w", encoding="utf-8") as f:
            json.dump([{"goal": "find the hidden switch", "steps": [{"see": "flip the hidden switch", "keys": "x"}],
                        "done": {"border": "square"}}], f)
        rc, out = self.run_cli("--goals", goals)
        self.assertEqual(rc, 1, out)
        self.assertIn("find the hidden switch: stuck at step 1", out)
        self.assertIn("flip the hidden switch", out)

    def test_real_asks_a_model_for_the_keys_with_only_the_screen(self):
        asked = []

        homes = []

        def child(feature, system, prompt, *a, **k):
            asked.append(prompt)
            homes.append(os.environ.get("FOREMAN_HOME"))
            return json.dumps({"keys": ":border square\n"})
        with mock.patch.object(fmideas, "run_child", side_effect=child):
            got = fmsettings.newcomer(goals=[{"goal": "square borders", "steps": [], "done": {"border": "square"}}],
                                      real=True)
        self.assertTrue(got[0]["done"], got)
        self.assertEqual(len(asked), 1)
        self.assertEqual(homes, [self.home], "the model's call is spent against the real budget, not the sandbox's")
        self.assertIn("square borders", asked[0])
        self.assertIn("Settings", asked[0], "the screen as text")
        self.assertFalse(os.path.exists(self.toml))

    def test_a_model_that_fails_stops_its_goal_not_the_run(self):
        goals = [{"goal": "square borders", "steps": [], "done": {"border": "square"}}] * 2
        with mock.patch.object(fmideas, "run_child", side_effect=ValueError("the daily budget is spent")):
            got = fmsettings.newcomer(goals=goals, real=True)
            with mock.patch("shutil.which", return_value="/usr/bin/claude"):
                rc, out = self.run_cli("--real")
        self.assertEqual([(g["done"], g["step"]) for g in got], [(False, 1)] * 2)
        self.assertIn("budget is spent", got[0]["missing"])
        self.assertEqual(rc, 1, out)
        self.assertIn("the model failed", out)

    def test_a_goals_file_of_the_wrong_shape_is_refused(self):
        goals = os.path.join(self.tmp, "goals.json")
        with open(goals, "w", encoding="utf-8") as f:
            json.dump([{"goal": "x", "steps": [{"see": 1}], "done": {}}], f)
        rc, out = self.run_cli("--goals", goals)
        self.assertEqual(rc, 2, out)
