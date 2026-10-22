"""T-1543: settings safety. A tui.toml the fm code app can't draw with boots the last one it could (said on the screen,
the file left as the user wrote it); an edit made to tui.toml while the app runs is merged into it, and a key changed
there is never overwritten unseen; fm settings bisect names the setting that breaks the screen, trying halves of the
changed keys against the renderer on temporary copies (tui.toml is never written)."""
import contextlib
import io
import os
import random
import types
import unittest.mock as mock

from helpers import ForemanTestCase, read_text

import fmcodetui as T
import fmsettings

REAL = T.render


def picky(st, w, h, cfg, *a, **k):
    """The renderer, failing on one value: no setting the schema takes breaks the real one, so a test makes one."""
    if cfg["layout"].get("narrow_below") == 7:
        raise ZeroDivisionError("a layout it can't draw")
    return REAL(st, w, h, cfg, *a, **k)


class Case(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.toml = os.path.join(self.home, "tui.toml")
        uhome = os.path.join(self.tmp, "uhome")  # a shared key (motion) writes the pane's option there, not the user's
        os.makedirs(os.path.join(uhome, ".claude"))
        self.patches = [mock.patch.object(T, "render", side_effect=picky),
                        mock.patch.object(fmsettings, "in_claude_code", return_value=False),
                        mock.patch.dict(os.environ, {"HOME": uhome})]
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


class LastKnownGood(Case):
    def test_a_config_that_fails_to_render_boots_the_last_good_one_and_says_so(self):
        self.write('border = "heavy"\n')
        cfg, errors, note, _ = fmsettings.boot()
        self.assertEqual((cfg["border"], errors, note), ("heavy", [], None))
        self.assertEqual(read_text(fmsettings.good_path()), 'border = "heavy"\n', "a good start keeps its file")
        bad = 'border = "double"\n[layout]\nnarrow_below = 7\n'
        self.write(bad)
        cfg, errors, note, _ = fmsettings.boot()
        self.assertEqual(cfg["border"], "heavy", "the last good one")
        for word in ("can't draw", "ZeroDivisionError", "last good", "fm settings bisect"):
            self.assertIn(word, note)
        self.assertEqual(read_text(self.toml), bad, "tui.toml as the user left it")
        self.assertEqual(read_text(fmsettings.good_path()), 'border = "heavy"\n', "a bad start keeps the good copy")

    def test_the_good_copy_never_brings_back_a_value_the_app_refuses(self):
        self.write('border = "nope"\n')
        cfg, errors, note, _ = fmsettings.boot()
        self.assertEqual((cfg["border"], note), (T.DEFAULTS["border"], None))
        self.assertIn("border", errors[0])
        self.write('[layout]\nnarrow_below = 7\n')
        cfg, errors, note, _ = fmsettings.boot()
        self.assertIn("last good", note)
        self.assertEqual(cfg["border"], T.DEFAULTS["border"], "the copy is loaded as tui.toml is: skipped there too")
        self.assertIn("border", errors[0])

    def test_with_no_good_copy_it_boots_the_defaults(self):
        self.write('[layout]\nnarrow_below = 7\n')
        cfg, _, note, _ = fmsettings.boot()
        self.assertEqual(cfg["layout"]["narrow_below"], T.DEFAULTS["layout"]["narrow_below"])
        self.assertIn("defaults", note)

    def test_the_app_says_so_on_its_screen(self):
        import fmcli
        self.write('border = "heavy"\n')
        fmsettings.boot()
        self.write('[layout]\nnarrow_below = 7\n')
        got = {}
        with mock.patch.object(T, "run_screen", side_effect=lambda app, *a: got.setdefault("app", app)), \
                mock.patch.object(T, "fm_projects", return_value=[]), \
                mock.patch.object(fmcli, "resolve", side_effect=fmcli.UsageError("not in a project")):
            T.main(types.SimpleNamespace(), [], home=True)
        app = got["app"]
        self.assertEqual(app.cfg["border"], "heavy")
        self.assertIn("last good", T.render(app.state, 200, 30, app.cfg, app).text())


class ExternalEdit(Case):
    def app(self, text='border = "heavy"\n'):
        self.write(text)
        cfg, _, _, seen = fmsettings.boot()
        app = T.App(cfg, spawn=lambda *a, **k: None)
        app.tui, self.t = seen, [100.0]
        app.clock = lambda: self.t[0]
        return app

    def tick(self, app):
        self.t[0] += 2
        app.poll()

    def test_an_edit_made_while_the_app_runs_is_merged_and_said(self):
        app = self.app()
        self.write('border = "double"\n[layout]\nnarrow_below = 60\n')
        self.tick(app)
        self.assertEqual((app.cfg["border"], app.cfg["layout"]["narrow_below"]), ("double", 60))
        for word in ("tui.toml changed", "border", "layout.narrow_below"):
            self.assertIn(word, app.message)
        app.message = ""
        self.tick(app)
        self.assertEqual(app.message, "", "said once")

    def test_an_edit_it_cant_draw_with_keeps_the_running_look(self):
        app = self.app()
        bad = 'border = "double"\n[layout]\nnarrow_below = 7\n'
        self.write(bad)
        self.tick(app)
        self.assertEqual(app.cfg["border"], "heavy")
        self.assertIn("can't draw", app.message)
        self.assertEqual(read_text(self.toml), bad, "never written back")
        self.write('border = "double"\n[layout\n')  # an editor half-way through a save
        self.tick(app)
        self.assertEqual(app.cfg["border"], "heavy")
        self.assertIn("isn't valid TOML", app.message)
        self.write('border = "double"\n[layout]\nnarrow_below = 7\nwidths = [50, 50]\n')
        self.tick(app)
        self.assertIn("(layout.widths)", app.message, "listed against the last file that parsed")

    def tick_bounded(self, app):
        """A tick that must come back: a read that blocks (a FIFO with no writer) fails the test, never hangs it."""
        import threading
        t = threading.Thread(target=self.tick, args=(app,), daemon=True)
        t.start()
        t.join(10)
        self.assertFalse(t.is_alive(), "the watch blocked on tui.toml")

    def test_a_fifo_a_device_or_a_huge_file_never_freezes_the_watch(self):
        app = self.app()
        app.show_settings()  # its list is read again on an outside edit: that read is bounded too
        os.unlink(self.toml)
        os.mkfifo(self.toml)
        self.tick_bounded(app)
        self.assertIn("not a regular file", app.message)
        self.assertEqual(app.cfg["border"], "heavy", "the running look kept")
        os.unlink(self.toml)
        if os.path.exists("/dev/zero"):
            os.symlink("/dev/zero", self.toml)
            self.tick_bounded(app)
            self.assertIn("not a regular file", app.message)
            os.unlink(self.toml)
        self.write('border = "double"\n' + "# padding\n" * 120_000)  # past the 1 MB a settings file gets
        self.tick_bounded(app)
        self.assertIn("over 1 MB", app.message)
        self.assertEqual(app.cfg["border"], "heavy")
        app.message = ""
        self.tick_bounded(app)
        self.assertEqual(app.message, "", "said once")

    def test_an_unreadable_file_is_said_once(self):
        app = self.app()
        with open(self.toml, "wb") as f:
            f.write(b'border = "\xff"\n')
        self.tick(app)
        self.assertIn("can't read", app.message)
        app.message = ""
        self.tick(app)
        self.assertEqual(app.message, "", "said once")

    def test_the_hush_key_takes_an_outside_edit_made_just_before(self):
        app = self.app()
        self.write('border = "double"\n')  # within the second before the watch reads it again
        app.key("z")
        self.assertEqual((app.cfg["border"], app.cfg["motion"]), ("double", "reduced"))
        self.assertIn('border = "double"', read_text(self.toml))

    def test_a_file_left_invalid_outside_says_so_not_unset(self):
        base = 'border = "heavy"\n'
        self.write('border = "double"\n[layout\n')
        done, refused = fmsettings.set_key("border", "rounded", base=base)
        self.assertEqual(done, [])
        self.assertIn("isn't valid TOML", refused[0])
        self.assertNotIn("unset", refused[0])

    def test_its_own_writes_are_not_outside_edits(self):
        app = self.app()
        app.show_settings()
        app._settings_set("set border double")
        app.message = ""
        self.tick(app)
        self.assertEqual((app.cfg["border"], app.message), ("double", ""))

    def test_a_key_changed_outside_is_never_overwritten_unseen(self):
        base = 'border = "heavy"\n'
        self.write(base)
        self.write('border = "double"\n')  # another program, after the app read it
        done, refused = fmsettings.set_key("border", "rounded", base=base)
        self.assertEqual(done, [])
        self.assertIn("changed", refused[0])
        self.assertEqual(read_text(self.toml), 'border = "double"\n')
        done, refused = fmsettings.set_key("layout.narrow_below", 60, base=base)
        self.assertEqual(refused, [])
        self.assertEqual(read_text(self.toml), 'border = "double"\n\n[layout]\nnarrow_below = 60\n', "merged")

    def test_a_preview_kept_after_an_outside_change_to_its_key_is_refused(self):
        app = self.app('theme = "night"\n')
        app.show_settings()
        app._settings_set("set theme riso")
        self.assertIsNotNone(app.set_pending)
        self.write('theme = "signal"\n')
        self.tick(app)
        app.key("x")  # keeps the preview: written only if the file still says what the app showed
        self.assertEqual(read_text(self.toml), 'theme = "signal"\n')
        self.assertIn("changed", app.set_note[0])
        self.assertEqual(app.cfg["preset"], "signal", "the screen as the file is")


class Bisect(Case):
    BAD = ('# mine\nborder = "double"\ntheme = "riso"\n[keys]\n' + "".join(f'{c} = "quit"\n' for c in "abcefgiopu")
           + '[layout]\nnarrow = ["log"]\nnarrow_below = 7\n')  # the bad one last: one key at a time takes 14 tries

    def test_it_names_the_key_that_breaks_rendering_and_writes_nothing(self):
        self.write('border = "heavy"\n')
        fmsettings.boot()
        self.write(self.BAD)
        got = fmsettings.bisect()
        self.assertEqual((got["key"], got["alone"], got["base"]), ("layout.narrow_below", True, "the last good copy"))
        self.assertEqual(got["changed"], 14)
        self.assertLessEqual(got["tries"], 9, "halves (4 tries), and the ends and the key alone checked")
        self.assertEqual(read_text(self.toml), self.BAD)
        self.assertEqual(read_text(fmsettings.good_path()), 'border = "heavy"\n')

    def test_a_key_that_breaks_it_only_with_another_says_so(self):
        def pair(st, w, h, cfg, *a, **k):
            if cfg["border"] == "double" and cfg["layout"].get("narrow_below") == 7:
                raise ZeroDivisionError("these two together")
            return REAL(st, w, h, cfg, *a, **k)
        self.write(self.BAD)
        with mock.patch.object(T, "render", side_effect=pair):
            got = fmsettings.bisect()
        self.assertEqual((got["key"], got["alone"], got["base"]), ("layout.narrow_below", False, "the defaults"))

    def test_the_command_from_fm_and_claude_code(self):
        self.write(self.BAD)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            fmsettings.cmd_settings(types.SimpleNamespace(action="bisect", key=None, value=None, surface=None,
                                                          json=False))
        self.assertIn("layout.narrow_below = 7", out.getvalue())
        self.assertEqual(read_text(self.toml), self.BAD)
        self.write('border = "double"\n')
        self.assertIn("draws", self.fm("settings", "bisect").stdout)
        body = read_text(os.path.join(os.path.dirname(__file__), "..", "commands", "settings.md"))
        self.assertIn("`fm settings bisect`", body)


class Monkey(Case):
    def test_random_keys_on_the_settings_screen_never_break_it_or_the_file(self):
        self.write('border = "heavy"\n')
        app = T.App(fmsettings.boot()[0], spawn=lambda *a, **k: None)
        app.show_settings()
        rnd = random.Random(1543)
        # never r: the runners list's Enter starts a real coding CLI
        keys = list("/:mbql jkJKHL\n\x1b\x7f") + ["KEY_UP", "KEY_DOWN", "KEY_NPAGE", "\t", "1", "a", '"', "["]
        real, sets = fmsettings.set_key, []
        with mock.patch.object(fmsettings, "set_key", side_effect=lambda *a, **k: sets.append(a) or real(*a, **k)):
            for k in [":", *"set border double", "\n"] + [rnd.choice(keys) for _ in range(400)]:
                app.key(k)
                if app.mode not in ("settings", "layout", "runners", "settings_loading"):
                    app.show_settings()
                REAL(app.state, 100, 30, app.cfg, app)
        self.assertIn(("border", "double", None), sets, "the :set line was reached")
        self.assertIsNotNone(fmsettings._parses(read_text(self.toml)), "tui.toml still parses")
        self.assertIsNone(fmsettings.render_error(T.load_config()[0]), "and the app can draw with it")
