"""T-1283: Foreman Code's terminal UI. It reads fm code's --json event stream and nothing else, so the stream carries
everything a live view draws; the views are pure functions of the state those events build, tested without a terminal."""
import json
import os
import sys
import time
import unittest
import unittest.mock

from test_code import CodeCase, call, plan


class Events(CodeCase):
    def events(self, r):
        return [json.loads(line) for line in r.stdout.splitlines() if line.strip()]

    def test_the_event_stream_has_what_a_live_view_draws(self):
        self.serve("openai", plan(), {"text": "Reading it first.", "calls": [("read", {"path": "calc.py"})]},
                   call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds now"))
        ev = self.events(self.code("fix add", "--model", "fake", "--json", "--no-commit"))
        kinds = [e["event"] for e in ev]
        self.assertEqual((ev[0]["event"], ev[0]["schema"]), ("start", 1), kinds)
        self.assertEqual(ev[0]["model"], "fake")
        self.assertIn("tokens", kinds)
        tok = [e for e in ev if e["event"] == "tokens"][-1]
        self.assertGreater(tok["total_in"], 0)
        self.assertTrue(any("Reading it first." in e["text"] for e in ev if e["event"] == "say"), kinds)
        read = next(e for e in ev if e["event"] == "action" and e["action"] == "read")
        self.assertIn("return a - b", read["detail"], "the action's result, for an expandable log line")
        self.assertIn("calc.py", next(e for e in ev if e["event"] == "changed")["files"])
        failed = next(e for e in ev if e["event"] == "verify" and e["exit"])
        self.assertIn("AssertionError", failed["output"], "the baseline run's failure, to show under it")
        self.assertEqual(kinds[-1], "closed")

    def test_plain_output_is_unchanged_by_the_new_events(self):
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        out = self.code("fix add", "--model", "fake", "--no-commit").stdout
        for word in ("call_in", "schema", '"event"', "Reading"):
            self.assertNotIn(word, out)

    def test_an_error_is_an_event_too(self):
        r = self.code("fix add", "--model", "nosuch", "--json", check=False)
        self.assertEqual(r.returncode, 1)
        last = self.events(r)[-1]
        self.assertEqual(last["event"], "error")
        self.assertIn("nosuch", last["text"])


RUN = [  # what one fm code --json run streams, shortened
    {"event": "start", "text": "", "schema": 1, "request": "fix add", "model": "fake", "worker": None},
    {"event": "plan", "text": "plan", "plan": {"type": "FIX", "tier": "S", "title": "Make calc.add add",
                                               "criteria": [{"text": "calc.add adds", "verify": "python3 test_calc.py"}],
                                               "steps": ["write the failing test", "fix calc.add"]}},
    {"event": "task", "text": "task T-0001 created and focused", "task": "T-0001"},
    {"event": "verify", "text": "before 1", "criterion": 1, "label": "before", "exit": 1, "cmd": "python3 test_calc.py",
     "output": "AssertionError: -1"},
    {"event": "step", "text": "step 1/2", "step": 1},
    {"event": "say", "text": "Reading calc.py first."},
    {"event": "tokens", "text": "", "call_in": 1200, "call_out": 80, "total_in": 1200, "total_out": 80},
    {"event": "action", "text": "", "action": "read", "target": "calc.py", "result": "ok", "detail": "1 def add"},
    {"event": "action", "text": "", "action": "run", "target": "rm -rf ~", "result": "refused",
     "detail": "refused: Foreman guard: rm of your home"},
    {"event": "step", "text": "step 2/2", "step": 2},
    {"event": "action", "text": "", "action": "edit", "target": "calc.py", "result": "ok", "detail": "edited"},
    {"event": "changed", "text": "", "step": 2, "files": ["calc.py"]},
    {"event": "verify", "text": "verify 1", "criterion": 1, "label": "verify", "exit": 0, "cmd": "python3 test_calc.py"},
    {"event": "closed", "text": "T-0001 closed; committed abc1234", "task": "T-0001", "tokens": [1200, 80]},
]


def tui():
    import fmcodetui
    return fmcodetui


class Core(unittest.TestCase):
    def state(self, events=RUN):
        st = tui().State()
        for e in events:
            st.apply(e)
        return st

    def test_the_state_follows_the_run(self):
        st = self.state()
        self.assertEqual((st.task, st.status, st.step, st.tokens), ("T-0001", "closed", 2, [1200, 80]))
        self.assertEqual(st.criteria[0]["state"], "pass")
        self.assertEqual([a["result"] for a in st.actions], ["ok", "refused", "ok"])
        self.assertEqual(st.files, {2: ["calc.py"]})

    def test_the_main_view_draws_every_station(self):
        canvas = tui().render(self.state(), 110, 32, tui().DEFAULTS)
        text = canvas.text()
        for words in ("Make calc.add add", "FIX S", "calc.add adds", "write the failing test", "fix calc.add",
                      "Reading calc.py first.", "rm -rf ~", "calc.py", "T-0001", "closed", "1.2k"):
            self.assertIn(words, text)
        self.assertEqual(canvas.style_of("rm -rf ~"), "bad", "a guard refusal stands out")
        self.assertEqual(len(text.splitlines()), 32)
        self.assertTrue(all(len(line) <= 110 for line in text.splitlines()))

    def test_a_narrow_terminal_gets_one_column(self):
        text = tui().render(self.state(), 66, 24, tui().DEFAULTS).text()
        self.assertTrue(all(len(line) <= 66 for line in text.splitlines()))
        self.assertIn("rm -rf ~", text, "the activity log still shows")
        self.assertIn("calc.add adds", text, "and the checks above it")

    def test_the_run_reads_as_pictures(self):
        app = tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None)
        for e in RUN + [{"event": "changed", "text": "", "step": 2, "files": ["calc.py"], "stat": {"calc.py": [3, 1]}}]:
            app.feed(e)
        cv = tui().render(app.state, 110, 32, tui().DEFAULTS, app)
        self.assertEqual(cv.text().splitlines()[2].count("✓"), 5, "plan, both steps, the checks and the close: done")
        self.assertEqual(cv.style_of(" ✓ "), "chip_ok")
        self.assertEqual(cv.style_of("PASS"), "chip_ok")
        self.assertIn("▆▆", cv.text(), "the changed file's lines as a bar")
        self.assertNotIn("Reading calc.py first.", cv.text(), "the model's own words wait behind t")
        app.key("t")
        self.assertIn("Reading calc.py first.", tui().render(app.state, 110, 32, tui().DEFAULTS, app).text())

    def test_time_and_tokens_are_charts(self):
        st = self.state([dict(e, ts=1000 + 10 * i) for i, e in enumerate(RUN)])
        self.assertEqual([s[0] for s in tui().spans(st)], ["plan", "step 1", "step 2", "checks"])
        text = tui().render(st, 110, 32, tui().DEFAULTS).text()
        self.assertIn("2m10s", text, "the run's length on the Time panel")
        top, floor = tui().columns([1, 2, 4], 20, 2)
        self.assertEqual((top.split(), floor.split()), (["██████"], ["▄▄▄▄▄▄", "██████", "██████"]),
                         "each call a column, the biggest the chart's full height")

    def test_partial_runs_and_unknown_events_never_break_the_view(self):
        for n in range(len(RUN) + 1):
            tui().render(self.state(RUN[:n]), 80, 24, tui().DEFAULTS)
        st = self.state(RUN + [{"event": "from-the-future", "text": "?"}, {"no": "event"}])
        self.assertEqual(st.status, "closed")
        with self.assertRaises(ValueError):  # a newer stream than this reader knows
            tui().State().apply({"event": "start", "text": "", "schema": 99})

    def test_keys_run_commands(self):
        app = tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None)
        app.key("?")
        self.assertEqual(app.mode, "help")
        app.key("?")
        self.assertEqual(app.mode, "main")
        app.key("n")
        self.assertEqual(app.mode, "prompt")
        for ch in "fix add":
            app.key(ch)
        started = []
        app.spawn = lambda words, opts: started.append((words, opts))
        app.key("\n")
        self.assertEqual(started, [(["fix add"], {})])
        app.key("q")
        self.assertTrue(app.done)


DIFF = """diff --git a/deploy.py b/deploy.py
--- a/deploy.py
+++ b/deploy.py
@@ -21,6 +21,9 @@ def main(argv=None):
     args = parse(argv)
+    if args.dry_run:
+        print("\\n".join(args.files))
+        return 0
     upload(args.files, args.bucket)
-    return upload_done()
"""


class Views(unittest.TestCase):
    def app(self, **kw):
        return tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None, **kw)

    def test_d_shows_the_runs_diff_coloured_and_q_closes_only_the_view(self):
        app = self.app(diff=lambda: DIFF)
        for e in RUN:
            app.feed(e)
        app.key("d")
        self.assertEqual(app.mode, "diff")
        cv = tui().render(app.state, 100, 30, tui().DEFAULTS, app)
        self.assertEqual(cv.style_of("+    if args.dry_run:"), "ok")
        self.assertEqual(cv.style_of("-    return upload_done()"), "bad")
        self.assertEqual(cv.style_of("@@ -21,6"), "accent")
        app.key("q")
        self.assertEqual((app.mode, app.done), ("main", False))

    def test_h_lists_past_runs_and_enter_replays_one(self):
        import tempfile
        folder = tempfile.mkdtemp()
        for tid, req, end in (("T-0001", "fix add", "closed"), ("T-0002", "add a --dry-run flag", "blocked")):
            with open(os.path.join(folder, f"{tid}.events.jsonl"), "w") as f:
                for e in ({"event": "start", "text": "", "schema": 1, "request": req, "ts": 1760000000},
                          {"event": "task", "text": "", "task": tid}, {"event": end, "text": end, "task": tid}):
                    f.write(json.dumps(e) + "\n")
        app = self.app(history=folder)
        app.key("h")
        self.assertEqual(app.mode, "history")
        text = tui().render(app.state, 100, 30, tui().DEFAULTS, app).text()
        self.assertIn("add a --dry-run flag", text)
        self.assertIn("fix add", text)
        app.key("j")
        app.key("\n")
        self.assertEqual(app.mode, "main")
        self.assertIn(app.state.task, ("T-0001", "T-0002"))
        self.assertIn(app.state.status, ("closed", "blocked"))

    def test_m_picks_the_model_or_worker_the_next_run_uses(self):
        app = self.app(choices=lambda: [("model", "qwen2.5-coder:32b"), ("worker", "claude"), ("worker", "codex")])
        app.key("m")
        self.assertEqual(app.mode, "picker")
        self.assertIn("codex", tui().render(app.state, 100, 30, tui().DEFAULTS, app).text())
        app.key("j")
        app.key("\n")
        self.assertEqual((app.mode, app.opts.get("worker"), app.opts.get("model")), ("main", "claude", None))
        started = []
        app.spawn = lambda words, opts: started.append(opts)
        app.start(["fix add"])
        self.assertEqual(started[0]["worker"], "claude")


class FakeCurses:
    A_BOLD, A_REVERSE, A_ITALIC, COLORS, COLOR_PAIRS = 1, 2, 4, 256, 256

    def __init__(self, colors=256):
        self.COLORS, self.pairs = colors, []

    def has_colors(self):
        return True

    def use_default_colors(self):
        pass

    def init_pair(self, n, fg, bg):
        self.pairs.append((fg, bg))

    def color_pair(self, n):
        return n << 8


class Terminal(unittest.TestCase):
    def test_no_color_draws_with_weight_and_reverse_only(self):
        fake = FakeCurses()
        with unittest.mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
            attrs = tui()._attrs(fake, tui().DEFAULTS)
        self.assertEqual(fake.pairs, [])
        self.assertTrue(attrs["chip_ok"] & fake.A_REVERSE and attrs["select"] & fake.A_REVERSE)
        self.assertTrue(attrs["strong"] & fake.A_BOLD)

    def test_an_8_colour_terminal_gets_the_nearest_of_8(self):
        fake = FakeCurses(colors=8)
        with unittest.mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("NO_COLOR", None)
            tui()._attrs(fake, tui().DEFAULTS)
        self.assertTrue(fake.pairs)
        self.assertTrue(all(-1 <= c < 8 for pair in fake.pairs for c in pair), fake.pairs)

    def test_any_size_draws_and_under_60_columns_is_one_panel(self):
        st = Core.state(self)
        for w, h in ((1, 1), (10, 5), (30, 8), (59, 20), (79, 24), (200, 60)):
            text = tui().render(st, w, h, tui().DEFAULTS).text().splitlines()
            self.assertEqual(len(text), h, (w, h))
            self.assertTrue(all(len(line) <= w for line in text), (w, h))
        small = tui().render(st, 59, 20, tui().DEFAULTS).text()
        self.assertEqual(small.count("╭"), 1, "just the activity log")
        self.assertIn("rm -rf ~", small)


class Config(unittest.TestCase):
    def write(self, text):
        import tempfile
        path = os.path.join(tempfile.mkdtemp(), "tui.toml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_a_users_file_sets_theme_colours_layout_and_keys(self):
        cfg, errors = tui().load_config(self.write(
            'theme = "paper"\nborder = "heavy"\n[colors]\nok = "#00FF00"\naccent = { fg = 33, bold = false }\n'
            '[layout]\ncolumns = [["log", "files"]]\nwidths = [100]\n[keys]\nx = "stop"\nq = "none"\n"ctrl+r" = "resume"\n'))
        self.assertEqual(errors, [])
        self.assertEqual(cfg["theme"]["ok"], {"fg": "#00FF00"})
        self.assertEqual(cfg["theme"]["accent"], {"fg": 33, "bold": False})
        self.assertEqual(cfg["theme"]["screen"]["bg"], tui().PALETTES["paper"]["bg"])
        self.assertEqual((cfg["keys"]["x"], cfg["keys"]["^R"]), ("stop", "resume"))
        self.assertNotIn("q", cfg["keys"])
        text = tui().render(tui().State(), 100, 30, cfg).text()
        self.assertIn("┏", text)
        self.assertEqual(tui().DEFAULTS["keys"]["q"], "quit", "the defaults stay as they were")

    def test_each_bad_setting_is_one_line_and_the_rest_still_apply(self):
        cfg, errors = tui().load_config(self.write(
            'theme = "neon"\nborders = 1\n[colors]\nok = "green"\nnosuch = "#000000"\n'
            '[layout]\ncolumns = [["log", "nosuch"]]\nwidths = [0]\n[keys]\nx = "explode"\n"ctrl+" = "stop"\ny = "stop"\n'))
        self.assertEqual(len(errors), 8, "\n".join(errors))
        self.assertTrue(all("\n" not in e for e in errors))
        for words in ("neon", "borders", "green", "nosuch", "widths", "explode", "ctrl+"):
            self.assertTrue(any(words in e for e in errors), words)
        self.assertEqual(cfg["keys"]["y"], "stop")

    def test_print_config_prints_a_file_that_loads_back_the_same(self):
        cfg, errors = tui().load_config(self.write(tui().print_config(tui().DEFAULTS)))
        self.assertEqual(errors, [])
        self.assertEqual(cfg, tui().DEFAULTS)
        paper, _ = tui().load_config(self.write('theme = "paper"\n'))
        again, _ = tui().load_config(self.write(tui().print_config(paper)))
        self.assertEqual(again, paper)

    def test_an_unreadable_file_names_itself(self):
        path = self.write("theme = \n")
        cfg, errors = tui().load_config(path)
        self.assertEqual(len(errors), 1)
        self.assertIn(path, errors[0])
        self.assertEqual(cfg, tui().DEFAULTS)

    def test_mono_has_no_colours(self):
        cfg, _ = tui().load_config(self.write('theme = "mono"\n'))
        self.assertFalse([n for n, spec in cfg["theme"].items() if n != "screen" and ("fg" in spec or "bg" in spec)])


def git_repo():
    import subprocess
    import tempfile
    root = tempfile.mkdtemp()
    git = lambda *a: subprocess.run(["git", "-C", root, *a], check=True, capture_output=True)
    git("init", "-q")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    with open(os.path.join(root, "a.py"), "w") as f:
        f.write("x = 1\n")
    git("add", ".")
    git("commit", "-qm", "base")
    return root, git


class Review(unittest.TestCase):
    """T-1283's review: each finding as a test."""

    def test_the_diff_view_runs_git_without_a_planted_fsmonitor(self):
        root, git = git_repo()
        marker = os.path.join(root, "ran")
        git("config", "core.fsmonitor", f"touch {marker}; false")
        with open(os.path.join(root, "a.py"), "w") as f:
            f.write("x = 2\n")
        app = tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None, root=root)
        app.key("d")
        self.assertFalse(os.path.exists(marker), "a worker's git config ran when d was pressed")
        self.assertIn("+x = 2", app.view_lines)

    def test_the_diff_view_goes_step_by_step_and_shows_new_files(self):
        root, _ = git_repo()
        with open(os.path.join(root, "a.py"), "w") as f:
            f.write("x = 2\n")
        with open(os.path.join(root, "b.py"), "w") as f:
            f.write("y = 1\n")
        app = tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None, root=root)
        for e in RUN[:2] + [{"event": "changed", "text": "", "step": 1, "files": ["a.py"]},
                            {"event": "changed", "text": "", "step": 2, "files": ["a.py", "b.py"]}]:
            app.feed(e)
        app.key("d")
        lines = app.view_lines
        first, second = (next(i for i, x in enumerate(lines) if x.startswith(f"── step {n}")) for n in (1, 2))
        self.assertLess(first, lines.index("+x = 2"))
        self.assertLess(second, lines.index("+y = 1"), "the new file, under the step that made it")
        self.assertLess(lines.index("+x = 2"), second)

    def test_plain_text_carries_no_control_characters(self):
        e = {"kind": "action", "action": "write", "target": "a\x1b]52;c;aGk=\x07.py", "result": "ok"}
        self.assertNotIn("\x1b", tui().entry_text(e))
        self.assertNotIn("\x07", tui().entry_text({"kind": "say", "text": "hi\x07\x1b[2J"}))

    def test_a_resumed_run_keeps_its_plan_on_screen(self):
        st = Core.state(self, RUN[:6] + [{"event": "start", "text": "", "schema": 1, "request": "fix add",
                                          "task": "T-0001", "resume": True}, RUN[9]])
        self.assertEqual(st.plan.get("title"), "Make calc.add add")
        self.assertEqual([s["state"] for s in st.steps], ["done", "now"])
        self.assertEqual(st.criteria[0]["text"], "calc.add adds")

    def test_control_keys_reach_their_ctrl_bindings(self):
        self.assertEqual(tui().key_of("\x12"), "^R")
        self.assertEqual([tui().key_of(k) for k in ("\t", "\n", "\r", "\x1b", "q", "KEY_UP")],
                         ["\t", "\n", "\n", "\x1b", "q", "KEY_UP"])

    def test_the_run_is_stopped_when_the_screen_dies(self):
        app = tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None)
        stopped = []
        app.stop = lambda: stopped.append(1)

        def wrapper(fn):
            raise KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            tui().run_screen(app, wrapper)
        self.assertEqual(stopped, [1])

    def test_plain_prints_the_plan_the_task_the_red_runs_and_why_a_command_was_refused(self):
        import io
        app = tui().App(tui().DEFAULTS, spawn=lambda *a, **k: None)
        for e in RUN + [{"event": "exit", "code": 0}]:
            app.events.put(e)
        out = io.StringIO()
        self.assertEqual(tui().run_plain(app, out), 0)
        text = out.getvalue()
        for words in ("Make calc.add add", "T-0001", "RED", "rm of your home", "closed"):
            self.assertIn(words, text)

    def test_a_panel_that_returns_bad_lines_says_so_and_the_screen_stays(self):
        tui().PANELS["broken"] = ("Broken", lambda st, w, h, app: ["not a line"])
        try:
            cfg = dict(tui().DEFAULTS, layout=dict(tui().DEFAULTS["layout"], columns=[["log"], ["broken"]]))
            text = tui().render(Core.state(self), 110, 30, cfg).text()
        finally:
            del tui().PANELS["broken"]
        self.assertIn("panel broken failed", text)

    def test_line_counts_name_a_non_ascii_file_once_and_stop_reading_a_big_one(self):
        import fmcode
        root, git = git_repo()
        with open(os.path.join(root, "café.py"), "w") as f:
            f.write("a = 1\n")
        git("add", ".")
        git("commit", "-qm", "café")
        with open(os.path.join(root, "café.py"), "w") as f:
            f.write("a = 2\nb = 3\n")
        with open(os.path.join(root, "big.txt"), "w") as f:
            f.write("x\n" * 100)
        with unittest.mock.patch.object(fmcode, "NUMSTAT_CAP", 10):
            stat = fmcode._numstat(root, ["café.py", "big.txt"])
        self.assertEqual(stat, {"café.py": [2, 1], "big.txt": [5, 0]})

    def test_s_stops_the_run_and_r_resumes_its_task(self):
        class Child:
            pid, code = 999999, None

            def poll(self):
                return self.code
        spawned, child = [], Child()
        app = tui().App(tui().DEFAULTS, spawn=lambda words, opts: spawned.append((words, opts)) or child)
        app.start(["fix add"])
        for e in RUN[:5]:
            app.feed(e)
        killed = []
        with unittest.mock.patch.object(os, "killpg", lambda pid, sig: killed.append(pid)):
            app.key("s")
        self.assertEqual(killed, [999999])
        child.code = -15
        app.key("r")
        self.assertEqual(spawned[-1], ([], {"resume": "T-0001"}))


SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "tui", "cost_meter.py")


class Extensions(unittest.TestCase):
    def setUp(self):
        t = tui()
        self.live = (t.PANELS, t.COMMANDS, t.HANDLERS, t.EXT_COMMANDS, t.EXT_LABELS, t.DEFAULTS["keys"])
        self.saved = [type(x)(x) for x in self.live]
        self.saved[2] = {k: list(v) for k, v in t.HANDLERS.items()}

    def tearDown(self):
        for live, saved in zip(self.live, self.saved):
            live.clear()
            live.update(saved) if isinstance(live, dict) else live.extend(saved)

    def folder(self, **files):
        import tempfile
        d = tempfile.mkdtemp()
        for name, body in files.items():
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(body)
        return d

    def test_the_sample_adds_a_panel_a_command_and_an_event_handler(self):
        import shutil
        d = self.folder()
        shutil.copy(SAMPLE, d)
        self.assertEqual(tui().load_extensions(d), [])
        cfg, errors = tui().load_config(Config.write(self, '[layout]\ncolumns = [["log"], ["cost"]]\nwidths = [60, 40]\n'))
        self.assertEqual(errors, [], "the layout can name the extension's panel")
        app = tui().App(cfg, spawn=lambda *a, **k: None)
        for e in RUN:
            app.feed(e)
        text = tui().render(app.state, 110, 32, cfg, app).text()
        self.assertIn("$0.0016", text)
        self.assertIn("1 model call", text, "its handler counted the tokens events")
        app.key("c")
        self.assertIn("$0.0048", tui().render(app.state, 110, 32, cfg, app).text())
        app.key("?")
        self.assertIn("the cost panel's next price", tui().render(app.state, 110, 32, cfg, app).text())

    def test_a_failing_extension_says_why_and_the_others_still_load(self):
        d = self.folder(**{"a_bad.py": "def setup(api):\n    raise RuntimeError('boom')\n",
                           "b_good.py": "def setup(api):\n    api.panel('hello', 'Hello', lambda st, w, h, app: [[('hi', 'ok')]])\n"
                                        "    api.on('*', lambda st, e: 1 / 0)\n"})
        errors = tui().load_extensions(d)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("a_bad.py", errors[0])
        self.assertIn("boom", errors[0])
        self.assertIn("hello", tui().PANELS)
        st = tui().State()
        for e in RUN:
            st.apply(e)
        self.assertEqual(st.status, "closed", "a handler that throws doesn't stop the run's view")
        self.assertEqual(sum("ZeroDivisionError" in str(n.get("text")) for n in st.log), 1, "said once, then dropped")

    def test_a_file_others_can_change_is_skipped(self):
        d = self.folder(**{"open.py": "def setup(api):\n    api.panel('open', 'Open', lambda st, w, h, app: [])\n"})
        os.chmod(os.path.join(d, "open.py"), 0o666)
        errors = tui().load_extensions(d)
        self.assertIn("another user can change it", errors[0])
        self.assertNotIn("open", tui().PANELS)


class Command(CodeCase):
    def test_fm_code_tui_draws_a_recorded_run(self):
        svg = os.path.join(self.home, "shot.svg")
        fixture = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "demo",
                               "code-tui.jsonl")
        self.code("tui", "--snapshot", svg, "--events", fixture, "--size", "100x30")
        with open(svg, encoding="utf-8") as f:
            body = f.read()
        self.assertTrue(body.startswith("<svg"), body[:80])
        self.assertIn("4e1b9c2", body)

    def test_print_config_and_a_bad_file(self):
        out = self.code("tui", "--print-config").stdout
        self.assertIn('theme = "night"', out)
        with open(os.path.join(self.home, "tui.toml"), "w", encoding="utf-8") as f:
            f.write('theme = "neon"\n')
        r = self.code("tui", "--snapshot", os.path.join(self.home, "x.svg"), "--events", os.devnull, check=False)
        self.assertEqual(r.returncode, 0, "a bad setting is said and skipped; the screen still runs")
        self.assertIn("neon", r.stderr)
        r = self.code("tui", "--print-config", check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("neon", r.stderr)

    def test_resume_reaches_fm_code(self):
        r = self.code("tui", "--plain", "--resume", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("STOP", r.stdout, "fm code --resume's own error, as a line")

    def test_extensions_load_from_foremans_home_and_never_from_the_project(self):
        panel = "def setup(api):\n    api.panel('{0}', '{0}', lambda st, w, h, app: [])\n"
        for folder, name in ((os.path.join(self.home, "tui"), "fromhome"), (os.path.join(self.repo, "tui"), "fromrepo"),
                             (os.path.join(self.repo, ".foreman", "tui"), "fromrepo2")):
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, f"{name}.py"), "w", encoding="utf-8") as f:
                f.write(panel.format(name))
        out = self.code("tui", "--print-config").stdout
        self.assertIn("fromhome", out)
        self.assertNotIn("fromrepo", out)

    def test_the_screen_runs_a_request_in_a_terminal(self):
        import fcntl
        import pty
        import select
        import struct
        import termios
        from test_code import FM
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        env = dict(self.env(), TERM="xterm-256color")
        env.pop("NO_COLOR", None)
        pid, fd = pty.fork()
        if pid == 0:  # the child: a 100x30 terminal running fm code tui
            try:
                fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))
                os.chdir(self.repo)
                os.execve(sys.executable, [sys.executable, FM, "code", "tui", "fix add", "--model", "fake",
                                           "--no-commit"], env)
            finally:
                os._exit(127)
        seen, deadline = b"", time.time() + 40
        try:
            while b"CLOSED" not in seen and time.time() < deadline:
                if select.select([fd], [], [], 0.5)[0]:
                    try:
                        seen += os.read(fd, 65536)
                    except OSError:
                        break
            self.assertIn(b"CLOSED", seen, seen[-2000:])
            self.assertIn(b"\x1b[", seen, "drawn with curses, not printed")
            os.write(fd, b"q")
            while time.time() < deadline:
                done, status = os.waitpid(pid, os.WNOHANG)
                if done:
                    self.assertEqual(os.waitstatus_to_exitcode(status), 0)
                    break
                if select.select([fd], [], [], 0.2)[0]:
                    try:
                        os.read(fd, 65536)
                    except OSError:
                        pass
            else:
                self.fail("q didn't quit")
        finally:
            try:
                os.kill(pid, 9)
                os.waitpid(pid, 0)
            except (OSError, ChildProcessError):
                pass
            os.close(fd)

    def test_fm_code_tui_plain_runs_a_request_line_by_line(self):
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        r = self.code("tui", "--plain", "fix add", "--model", "fake", "--no-commit")
        self.assertIn("edit   calc.py", r.stdout)
        self.assertIn("closed", r.stdout.splitlines()[-1])
        self.assertNotIn('"event"', r.stdout)


class RunHistory(CodeCase):
    def test_fm_code_keeps_each_runs_events_for_the_history(self):
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        self.code("fix add", "--model", "fake", "--no-commit")
        path = os.path.join(os.path.dirname(os.path.dirname(self.task()["path"])), "code", "T-0001.events.jsonl")
        kinds = [json.loads(line)["event"] for line in open(path)]
        self.assertEqual((kinds[0], kinds[-1]), ("start", "closed"))
        self.assertIn("plan", kinds)


if __name__ == "__main__":
    import unittest
    unittest.main()
