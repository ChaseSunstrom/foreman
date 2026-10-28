"""The backlog, further (T-1856, T-1857, T-1860, T-1861): fm inbox swipe in a terminal asks one item at a time
(r revive · k keep · d drop · s skip · q stop), each verdict applied as it is said; the fm code app has the same
pile as its backlog view; fm inbox pick skips items waiting on an open one and now and then pairs an item with a far
one of its kind (--epsilon); fm inbox prefer --reset forgets the learned title-word weights."""
import contextlib
import io
import json
import os
from unittest import mock

from helpers import ForemanTestCase

import fmcodetui as T
import fmcore as c
import fmeco


class _Inbox(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def deferred(self, *titles):
        for t in titles:
            self.fm("capture", t)
        for b in c.load_briefs(self.p):
            self.fm("task", "defer", b.id, "later")

    def status(self):
        return {b.id: b.status for b in c.load_briefs(self.p, include_archive=True)}

    def capture(self, *titles):
        for t in titles:
            self.fm("capture", t, "--tier", "M", "--type", "FEATURE", "--anyway")


class Swipe(_Inbox):
    def loop(self, *keys):
        keys, out = iter(keys), io.StringIO()

        def ask(prompt=""):
            try:
                return next(keys)
            except StopIteration:
                raise EOFError from None
        with mock.patch("builtins.input", ask), contextlib.redirect_stdout(out):
            return fmeco.swipe_loop(self.p), out.getvalue()

    def test_the_terminal_loop_applies_each_verdict_as_it_is_said(self):
        self.deferred("Port the CLI to Windows", "Add a plugin marketplace page", "Support YAML config files",
                      "Ship a Homebrew formula")
        said, out = self.loop("r", "maybe", "dunno", "drop", "s", "k")
        self.assertEqual(said, ["T-0001 revived", "T-0002 dropped", "T-0004 kept"])
        self.assertIn("T-0002 dropped\n", out, "each verdict said as it lands")
        self.assertIn("r revive · k keep · d drop · s skip · q stop", out)
        self.assertIn("later", out, "each item shows why it was deferred")
        self.assertEqual([self.status()[t] for t in ("T-0001", "T-0002", "T-0003", "T-0004")],
                         ["captured", "dropped", "deferred", "deferred"])

    def test_q_or_the_end_of_input_stops_with_what_was_said_kept(self):
        self.deferred("Port the CLI to Windows", "Add a plugin marketplace page")
        self.assertEqual(self.loop("d", "q")[0], ["T-0001 dropped"])
        self.assertEqual(self.status()["T-0002"], "deferred")
        self.assertEqual(self.loop()[0], [], "no input: nothing applied")

    def test_an_item_changed_elsewhere_is_said_and_the_sweep_goes_on(self):
        self.deferred("Port the CLI to Windows", "Add a plugin marketplace page")
        items = fmeco.swipe_list(self.p)
        fmeco.swipe_apply(self.p, "T-0001:revive")  # another session, after the list was read
        with mock.patch.object(fmeco, "swipe_list", return_value=items):
            said, out = self.loop("k", "d")
        self.assertEqual(said, ["T-0002 dropped"])
        self.assertIn("T-0001 is not deferred", out)

    def test_a_terminal_gets_the_loop_and_a_pipe_or_json_the_list(self):
        self.deferred("Port the CLI to Windows")
        import fmcli
        parse = fmcli.build_parser().parse_args
        with mock.patch.object(fmeco, "_tty", return_value=True), mock.patch.object(fmcli, "resolve", return_value=self.p), \
                mock.patch.object(fmeco, "swipe_loop", return_value=[]) as loop, contextlib.redirect_stdout(io.StringIO()):
            fmeco.cmd_inbox(parse(["inbox", "swipe"]))
            fmeco.cmd_inbox(parse(["inbox", "swipe", "--json"]))
        self.assertEqual(loop.call_count, 1)
        self.assertIn("T-0001", self.fm("inbox", "swipe").stdout, "piped: the list, as before")


class Pick(_Inbox):
    def test_an_item_waiting_on_an_open_one_is_not_offered(self):
        self.capture("Speed up the search index", "#T-0001 Cache the search results", "Polish the onboarding screens")
        d = json.loads(self.fm("inbox", "pick", "--epsilon", "0", "--json").stdout)
        self.assertEqual([[x["a"]["id"], x["b"]["id"]] for x in d["pairs"]], [["T-0001", "T-0003"]])

    def test_epsilon_pairs_an_item_with_a_far_one_of_its_kind(self):
        self.capture("Speed up the search index", "Polish the onboarding screens", "Cache the search results",
                     "Animate the onboarding banner", "Trim the release notes", "Rename the export flag")

        class Far:  # always explores, always the farthest
            random = staticmethod(lambda: 0.0)
            choice = staticmethod(lambda xs: xs[-1])
        ids = lambda got: [[x["a"]["id"], x["b"]["id"]] for x in got]  # noqa: E731
        self.assertEqual(ids(fmeco.inbox_pick(self.p, epsilon=1.0, rng=Far)),
                         [["T-0001", "T-0006"], ["T-0002", "T-0005"], ["T-0003", "T-0004"]])
        self.assertEqual(ids(fmeco.inbox_pick(self.p, epsilon=0.0, rng=Far)),
                         [["T-0001", "T-0002"], ["T-0003", "T-0004"], ["T-0005", "T-0006"]])
        for bad in ("1.5", "-0.1", "x", "nan"):
            self.assertEqual(self.fm("inbox", "pick", "--epsilon", bad, check=False).returncode, 1, bad)
        self.assertEqual(self.fm("inbox", "first", "--epsilon", "0", check=False).returncode, 1, "pick only")


class Prefer(_Inbox):
    def test_reset_forgets_the_learned_weights(self):
        self.capture("Speed up the search index", "Polish the onboarding screens")
        rank = lambda: [b.id for b in c.rank_inbox(c.load_briefs(self.p))]  # noqa: E731
        self.fm("inbox", "prefer", "T-0002", "T-0001")
        self.assertEqual(rank(), ["T-0002", "T-0001"])
        self.assertIn("Forgot", self.fm("inbox", "prefer", "--reset").stdout)
        self.assertEqual(rank(), ["T-0001", "T-0002"])
        self.assertFalse(os.path.exists(os.path.join(self.p.dir, "prefer.json")))
        self.assertIn("nothing learned", self.fm("inbox", "prefer", "--reset").stdout)
        self.assertEqual(self.fm("inbox", "prefer", "T-0002", "T-0001", "--reset", check=False).returncode, 1)
        self.assertEqual(self.fm("inbox", "pick", "--reset", check=False).returncode, 1, "prefer only")
        with open(os.path.join(self.p.dir, "prefer.json"), "w") as f:
            f.write("{not json")
        self.assertIn("unreadable", self.fm("inbox", "prefer", "--reset").stdout)


class App(_Inbox):
    def app(self, root):
        return T.App(T.load_config()[0], spawn=lambda *a, **k: None, root=root)

    def test_the_app_backlog_view_revives_keeps_and_drops_at_once(self):
        self.deferred("Port the CLI to Windows", "Add a plugin marketplace page", "Support YAML config files")
        app = self.app(self.repo)
        app.key("I")
        self.assertEqual(app.mode, "backlog")
        text = T.render(app.state, 120, 40, app.cfg, app).text()
        self.assertIn("Add a plugin marketplace page", text)
        self.assertIn("r revive", text)
        for k in ("r", " ", "d"):
            app.key(k)
        self.assertEqual([self.status()[t] for t in ("T-0001", "T-0002", "T-0003")], ["captured", "deferred", "dropped"])
        self.assertIn("T-0003 dropped", app.message)
        self.assertEqual(app.items, [])
        app.key("\x1b")
        self.assertEqual(app.mode, "main")

    def test_a_row_changed_elsewhere_goes_with_its_error_said(self):
        self.deferred("Port the CLI to Windows", "Add a plugin marketplace page")
        app = self.app(self.repo)
        app.key("I")
        fmeco.swipe_apply(self.p, "T-0001:revive")
        app.key("d")
        self.assertIn("not deferred", app.message)
        self.assertEqual([x["id"] for x in app.items], ["T-0002"])
        self.assertEqual(self.status()["T-0002"], "deferred")

    def test_outside_a_project_the_view_says_so_and_stays_shut(self):
        app = self.app(self.tmp)
        app.key("I")
        self.assertEqual(app.mode, "main")
        self.assertIn("not a Foreman project", app.message)

    def test_claude_code_has_the_reset(self):
        with open(os.path.join(os.path.dirname(fmeco.__file__), "..", "commands", "backlog.md")) as f:
            self.assertIn("fm inbox prefer --reset", f.read())
