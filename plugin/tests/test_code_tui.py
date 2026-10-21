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


class Terminal(unittest.TestCase):
    """T-1300: Foreman's own ANSI renderer (no curses): 24-bit colour where the terminal has it, the nearest of 256
    or 8 elsewhere, none on NO_COLOR, and only the cells that changed are written again."""

    def canvas(self):
        return tui().render(Core.state(self), 80, 24, tui().DEFAULTS)

    def test_the_colour_depth_follows_the_terminal(self):
        depth = tui().colour_depth
        self.assertEqual(depth({"COLORTERM": "truecolor", "TERM": "xterm-256color"}), 24)
        self.assertEqual(depth({"COLORTERM": "24bit"}), 24)
        self.assertEqual(depth({"TERM": "xterm-256color"}), 256)
        self.assertEqual(depth({"TERM": "xterm"}), 8)
        self.assertEqual(depth({"NO_COLOR": "1", "COLORTERM": "truecolor"}), 0)

    def test_each_depth_writes_its_own_colour_codes(self):
        for d, has, hasnt in ((24, "38;2;", "38;5;"), (256, "38;5;", "38;2;"), (0, "\x1b[", "38;")):
            out = tui().Term(d).frame(self.canvas(), tui().DEFAULTS)
            self.assertIn(has, out, d)
            if d:
                self.assertNotIn(hasnt, out, d)
            else:
                self.assertNotIn(";2;", out)
                self.assertNotIn("38;", out)
        eight = tui().Term(8).frame(self.canvas(), tui().DEFAULTS)
        self.assertNotIn("38;2;", eight)
        self.assertNotIn("38;5;", eight)

    def test_a_repeated_frame_writes_almost_nothing_and_a_change_only_its_cells(self):
        term, cv = tui().Term(24), self.canvas()
        first = term.frame(cv, tui().DEFAULTS)
        self.assertGreater(len(first), 2000)
        self.assertLess(len(term.frame(cv, tui().DEFAULTS)), 16)
        cv.put(5, 5, "Z", "bad")
        self.assertLess(len(term.frame(cv, tui().DEFAULTS)), 80)

    def test_keys_arrive_with_the_names_the_app_binds(self):
        self.assertEqual(tui().parse_keys("\x1b[A\x1b[6~q\x12\r\x7f\x1b[B\t"),
                         ["KEY_UP", "KEY_NPAGE", "q", "^R", "\n", "KEY_BACKSPACE", "KEY_DOWN", "\t"])
        self.assertEqual(tui().parse_keys("\x1b"), ["\x1b"])

    def test_any_size_draws_and_under_60_columns_is_one_panel(self):
        st = Core.state(self)
        for w, h in ((1, 1), (10, 5), (30, 8), (59, 20), (79, 24), (200, 60)):
            text = tui().render(st, w, h, tui().DEFAULTS).text().splitlines()
            self.assertEqual(len(text), h, (w, h))
            self.assertTrue(all(len(line) <= w for line in text), (w, h))
        small = tui().render(st, 59, 20, tui().DEFAULTS).text()
        self.assertEqual(small.count("╭"), 1, "just the activity log")
        self.assertIn("rm -rf ~", small)

    def test_no_colour_reverses_chips_but_not_text_on_a_panel(self):
        cv, term = self.canvas(), tui().Term(0)
        rows, text = term.cells(cv, tui().DEFAULTS), cv.text().splitlines()
        y = next(i for i, line in enumerate(text) if "rm -rf ~" in line)
        self.assertNotIn(";7", rows[y][text[y].index("rm -rf ~")][1], "plain text inside a panel isn't inverted")
        self.assertIn(";7", rows[y][text[y].index("GUARD")][1], "a chip still is")

    def test_a_key_sequence_split_across_reads_waits_for_its_end(self):
        split = tui().split_tail
        self.assertEqual(split("ab\x1b["), ("ab", "\x1b["))
        self.assertEqual(split("q\x1b[1;5"), ("q", "\x1b[1;5"))
        self.assertEqual(split("q\x1b"), ("q", "\x1b"))
        self.assertEqual(split("q\x1b[A"), ("q\x1b[A", ""))

    def test_wide_and_combining_characters_keep_the_columns(self):
        cv = tui().Canvas(10, 1)
        cv.put(0, 0, "日本x")
        self.assertEqual([ch for ch, _ in cv.cells[0][:5]], ["日", "", "本", "", "x"])
        cv.put(0, 0, "éxy")
        self.assertEqual([ch for ch, _ in cv.cells[0][:3]], ["é", "x", "y"])
        self.assertEqual(len(cv.cells[0]), 10)

    def test_a_closed_terminal_doesnt_hide_why_the_screen_ended(self):
        import pty
        master, slave = pty.openpty()

        def gone(io):
            os.close(master)
            raise SystemExit(129)
        with self.assertRaises(SystemExit):
            tui().session(gone, slave, slave)
        os.close(slave)

    def test_wrap_is_off_so_the_last_cell_cant_scroll_the_screen(self):
        import fmcodeterm
        self.assertIn("\x1b[?7l", fmcodeterm.ENTER)
        self.assertIn("\x1b[?7h", fmcodeterm.LEAVE)


RUNNING = RUN[:10]  # step 2 just started, the checks not yet run


def lum(spec):
    import fmcodetui
    r, g, b = fmcodetui._rgb(spec)
    return r + g + b


class Motion(unittest.TestCase):
    """T-1300: motion is a pure function of state and time. Each test renders at two times and compares."""

    def app(self, events, motion="full"):
        cfg = dict(tui().DEFAULTS, motion=motion)
        app = tui().App(cfg, spawn=lambda *a, **k: None)
        for e in events:
            app.feed(e)
        return app, cfg

    def frame(self, app, cfg, t, w=110, h=32):
        return tui().render(app.state, w, h, cfg, app, t=t)

    def cell(self, cv, needle, cfg, offset=0):
        for y, row in enumerate(cv.cells):
            i = "".join(ch for ch, _ in row).find(needle)
            if i >= 0:
                return tui().resolve(row[i + offset][1], cfg, cv.bg[y][i + offset])
        self.fail(f"{needle!r} not drawn")

    def test_the_station_being_worked_pulses_and_its_spinner_turns(self):
        app, cfg = self.app(RUNNING)
        a, b = self.frame(app, cfg, 100.0), self.frame(app, cfg, 100.8)
        track_a, track_b = a.text().splitlines()[2], b.text().splitlines()[2]
        self.assertNotEqual(track_a, track_b, "the spinner moved")
        chip = lambda cv: next(tui().resolve(st, cfg)["bg"] for ch, st in cv.cells[2] if tui().resolve(st, cfg).get("bg")
                               and isinstance(st, tuple))
        self.assertNotEqual(chip(a), chip(b), "the pulse changed the chip's colour")

    def test_a_light_travels_along_the_link_into_the_current_station(self):
        app, cfg = self.app(RUNNING)
        a, b = self.frame(app, cfg, 100.0), self.frame(app, cfg, 100.35)
        link = lambda cv: [tui().resolve(st, cfg).get("fg") for ch, st in cv.cells[2] if ch == "━"]
        self.assertNotEqual(link(a), link(b))

    def test_counters_roll_up_to_new_values(self):
        app, cfg = self.app(RUN[:6])
        self.frame(app, cfg, 100.0)
        app.feed({"event": "tokens", "text": "", "call_in": 9000, "call_out": 900, "total_in": 10200, "total_out": 980})
        early, late = self.frame(app, cfg, 100.05).text(), self.frame(app, cfg, 103.0).text()
        self.assertNotIn("10.2k in", early, "still rolling")
        self.assertIn("10.2k in", late)

    def test_a_check_that_flips_flashes_then_settles(self):
        app, cfg = self.app(RUN[:12])
        self.frame(app, cfg, 100.0)
        app.feed(RUN[12])  # the check passes
        hot, cool = self.frame(app, cfg, 100.05), self.frame(app, cfg, 104.0)
        self.assertGreater(lum(self.cell(hot, "PASS", cfg)["bg"]), lum(self.cell(cool, "PASS", cfg)["bg"]))
        self.assertEqual(self.cell(cool, "PASS", cfg)["bg"], tui().resolve("chip_ok", cfg)["bg"])

    def test_a_new_activity_line_fades_in(self):
        app, cfg = self.app(RUN[:7])
        self.frame(app, cfg, 100.0)
        app.feed(RUN[7])  # read calc.py
        dim, full = self.frame(app, cfg, 100.03), self.frame(app, cfg, 103.0)
        self.assertLess(lum(self.cell(dim, "read", cfg)["fg"]), lum(self.cell(full, "read", cfg)["fg"]))

    def test_closing_sends_a_wave_along_the_track(self):
        app, cfg = self.app(RUN[:-1])
        self.frame(app, cfg, 100.0)
        app.feed(RUN[-1])
        self.frame(app, cfg, 100.05)  # the frame that sees it close
        during, after = self.frame(app, cfg, 100.45), self.frame(app, cfg, 105.0)
        bright = lambda cv: max(lum(tui().resolve(st, cfg, cv.bg[2][x]).get("fg") or "#000000")
                                for x, (ch, st) in enumerate(cv.cells[2]) if ch == "━")
        self.assertGreater(bright(during), bright(after))

    def test_a_guard_refusal_lands_with_a_flash(self):
        app, cfg = self.app(RUN[:8])
        self.frame(app, cfg, 100.0)
        app.feed(RUN[8])  # rm -rf ~ refused
        self.frame(app, cfg, 100.02)
        hot, cool = self.frame(app, cfg, 100.3), self.frame(app, cfg, 104.0)
        self.assertGreater(lum(self.cell(hot, "GUARD", cfg, -1)["bg"]), lum(self.cell(cool, "GUARD", cfg, -1)["bg"]))
        self.assertEqual(self.cell(cool, "GUARD", cfg, -1)["bg"], tui().resolve("chip_bad", cfg)["bg"])

    def test_the_idle_screen_is_a_welcome_not_a_blank(self):
        app, cfg = self.app([])
        a, b = self.frame(app, cfg, 100.0), self.frame(app, cfg, 100.9)
        text = a.text()
        for words in ("Foreman Code", "new request", "past runs"):
            self.assertIn(words, text)
        self.assertNotEqual([r for r in a.cells], [r for r in b.cells], "its mark breathes")

    def test_motion_off_draws_the_same_at_any_time(self):
        app, cfg = self.app(RUNNING, motion="off")
        a, b = self.frame(app, cfg, 100.0), self.frame(app, cfg, 101.37)
        self.assertEqual(a.cells, b.cells)

    def test_reduced_motion_keeps_colour_changes_but_nothing_moves(self):
        app, cfg = self.app(RUN[:12], motion="reduced")
        self.frame(app, cfg, 100.0)
        app.feed(RUN[12])
        a, b = self.frame(app, cfg, 100.05), self.frame(app, cfg, 100.55)
        self.assertEqual(a.text(), b.text(), "no spinner, no rolling numbers")
        self.assertGreater(lum(self.cell(a, "PASS", cfg)["bg"]), lum(tui().resolve("chip_ok", cfg)["bg"]))

    def test_the_frame_rate_follows_what_moves(self):
        app, cfg = self.app(RUNNING)
        self.frame(app, cfg, 100.0)
        self.assertLessEqual(app.fps(100.0), 30)
        self.assertGreaterEqual(app.fps(100.0), 8, "live work animates")
        done, cfg2 = self.app(RUN)
        self.frame(done, cfg2, 100.0)
        self.assertLessEqual(done.fps(110.0), 4, "a settled screen barely redraws")
        off, cfg3 = self.app(RUNNING, motion="off")
        self.assertLessEqual(off.fps(100.0), 4)

    def test_gradients_colour_the_header_and_the_chart(self):
        app, cfg = self.app(RUN)
        cv = self.frame(app, cfg, 100.0)
        brand = [tui().resolve(st, cfg).get("bg") for ch, st in cv.cells[0][:16]]
        self.assertGreater(len(set(brand)), 3, "the brand chip is a ramp, not one colour")
        rows = [y for y, row in enumerate(cv.cells) if "Tokens" in "".join(ch for ch, _ in row)]
        cols = [tui().resolve(st, cfg).get("fg") for y in range(rows[0] + 1, cv.h - 3)
                for ch, st in cv.cells[y] if ch in tui().BLOCKS]
        self.assertGreater(len(set(cols)), 1, "the token columns are shaded")

    def test_panels_sit_on_their_own_background(self):
        cv = self.frame(*self.app(RUN), 100.0)
        inside = cv.bg[5][3]
        self.assertIsNotNone(inside, "a panel's inside has its own tint")
        self.assertNotEqual(inside, tui().resolve("screen", tui().DEFAULTS)["bg"])

    def test_the_svg_draws_bars_without_seams(self):
        """Backgrounds first, then glyphs that overlap their neighbours: no hairline between a bar's cells."""
        T, rgb = tui(), tui().rgb
        cv = T.Canvas(4, 2)
        cv.tint(0, 0, 2, 4, "#111B2B")
        cv.put(0, 0, "▆", rgb(fg="#3366FF"))
        cv.put(0, 1, "▆", rgb(fg="#4477FF"))
        cv.put(1, 0, "█", rgb(fg="#5588FF"))
        svg = T.to_svg(cv, T.DEFAULTS).splitlines()
        rects = [s for s in svg if s.startswith("<rect x=")]
        backs = [k for k, s in enumerate(rects) if 'fill="#111b2b"' in s.lower()]
        bars = [k for k, s in enumerate(rects) if "#3366" in s.upper() or "#4477" in s.upper() or "#5588" in s.upper()]
        self.assertEqual((len(bars), len(backs) > 0), (3, True), rects)
        self.assertLess(max(backs), min(bars), "every background comes before every bar")
        a, b = (float(rects[k].split('x="')[1].split('"')[0]) for k in bars[:2])
        w = float(rects[bars[0]].split('width="')[1].split('"')[0])
        self.assertGreater(a + w, b, "a bar cell overlaps the next one")

    def row_of(self, cv, needle):
        return next((y, "".join(ch for ch, _ in row).find(needle)) for y, row in enumerate(cv.cells)
                    if needle in "".join(ch for ch, _ in row))

    def test_the_newest_line_is_the_focal_line_while_running(self):
        app, cfg = self.app(RUNNING)
        cv = self.frame(app, cfg, 100.0)
        y, x = self.row_of(cv, "2  fix calc.add")  # step 2 has just started: its header is the newest line
        panel = tui().col(cfg, "panel", "bg")
        self.assertNotEqual(tui().resolve(cv.cells[y][x + 4][1], cfg, cv.bg[y][x + 4]).get("bg"), panel, "the now line")
        y2, x2 = self.row_of(cv, "rm -rf ~")
        self.assertEqual(tui().resolve(cv.cells[y2][x2][1], cfg, cv.bg[y2][x2]).get("bg"), panel, "older lines")
        app, cfg = self.app(RUN)
        cv = self.frame(app, cfg, 100.0)
        y, x = self.row_of(cv, "T-0001 closed")
        self.assertEqual(tui().resolve(cv.cells[y][x][1], cfg, cv.bg[y][x]).get("bg"), panel, "a closed run has none")

    def test_a_file_that_just_changed_glows_then_cools(self):
        app, cfg = self.app(RUN[:11])
        self.frame(app, cfg, 100.0)
        app.feed(RUN[11])  # calc.py changed
        self.frame(app, cfg, 100.05)
        def name(t):  # the Changed panel's calc.py (the Activity panel names it too, further left)
            cv = self.frame(app, cfg, t)
            y = next(y for y, row in enumerate(cv.cells) if " +0" in "".join(ch for ch, _ in row))
            x = "".join(ch for ch, _ in cv.cells[y]).rfind("calc.py")
            return tui().resolve(cv.cells[y][x][1], cfg, cv.bg[y][x])
        hot, cold = name(100.3), name(105.0)
        ink = tui().col(cfg, "screen")
        self.assertGreater(lum(hot["fg"]), lum(cold.get("fg") or ink) + 20, "just changed: bright")
        self.assertEqual(cold.get("fg") or ink, ink, "then plain text again")

    def test_rolling_totals_hold_their_place(self):
        app, cfg = self.app(RUN[:6])
        self.frame(app, cfg, 100.0)
        app.feed(RUN[6])
        self.frame(app, cfg, 100.02)
        places = {self.row_of(self.frame(app, cfg, t), " in ")[1] for t in (100.05, 100.4, 105.0)}
        self.assertEqual(len(places), 1, "the labels don't slide while the numbers roll")

    def test_an_empty_panel_shimmers_while_the_run_starts(self):
        app, cfg = self.app(RUN[:1])
        looks = {tuple(lum(self.cell(self.frame(app, cfg, t), "nothing changed yet", cfg, k)["fg"])
                       for k in range(0, 18, 3))
                 for t in (100.0, 100.5, 101.0)}
        self.assertGreater(len(looks), 1, "a light passes over the words")
        self.row_of(self.frame(app, cfg, 101.0), "planning the work")  # not the idle welcome
        app, cfg = self.app(RUN[:1], motion="off")
        self.assertEqual(self.cell(self.frame(app, cfg, 100.0), "nothing changed yet", cfg).get("fg"),
                         tui().col(cfg, "dim"))

    def test_a_theme_without_colours_keeps_its_chips_reversed_while_moving(self):
        cfg = dict(tui().DEFAULTS, theme=tui().PRESETS["mono"](), preset="mono")
        app = tui().App(cfg, spawn=lambda *a, **k: None)
        for e in RUN[:8]:
            app.feed(e)
        self.frame(app, cfg, 100.0)
        app.feed(RUN[8])  # the guard refuses
        for t in (100.05, 100.3):
            cv = self.frame(app, cfg, t)
            self.assertTrue(self.cell(cv, "GUARD", cfg).get("reverse"), t)
            self.assertTrue(self.cell(cv, "RUNNING", cfg).get("reverse"), t)

    def test_a_note_names_the_runner_in_activity(self):
        # T-1328: with nothing configured fm code picks a runner and says which; the screen shows it
        app, cfg = self.app(RUN[:1] + [{"event": "note", "text": "runner: claude (no model is set up)", "ts": 1.0}])
        self.assertIn("runner: claude", self.frame(app, cfg, 100.0, w=110, h=32).text())

    def test_tool_uses_show_and_a_heartbeat_ticks_until_the_next_line(self):
        # T-1329: a CLI's tool use is an Activity line; "still working" ticks in one line, gone at the next real one
        beat = {"event": "working", "worker": "claude", "secs": 10, "text": "claude working (10 s)", "ts": 2.0}
        app, cfg = self.app(RUN[:1] + [{"event": "tool", "action": "edit", "target": "calc.py", "ts": 1.0}, beat,
                                       dict(beat, secs=20, text="claude working (20 s)")])
        text = self.frame(app, cfg, 100.0, w=110, h=32).text()
        self.assertIn("edit", text)
        self.assertIn("calc.py", text)
        self.assertIn("working (20 s)", text)
        self.assertNotIn("working (10 s)", text, "one ticking line, not one per beat")
        app.feed({"event": "tool", "action": "run", "target": "python3 test_calc.py", "ts": 3.0})
        self.assertNotIn("working (20 s)", self.frame(app, cfg, 101.0, w=110, h=32).text())

    def test_a_stall_is_a_warning_line_and_the_status_bar_says_when_the_cli_was_last_heard(self):
        # T-1336: a CLI silent past FM_STALL gets a stalled line in Activity; the bar says how long it has been quiet
        beat = {"event": "working", "worker": "claude", "secs": 130, "silent": 125, "text": "claude working (130 s)",
                "ts": 2.0}
        stall = {"event": "stalled", "worker": "claude", "secs": 125, "cause": "prompt", "last": "Overwrite? (y/n)",
                 "text": "claude stalled: waiting at a prompt: Overwrite? (y/n)", "ts": 2.5}
        app, cfg = self.app(RUN[:1] + [beat, stall], motion="off")
        cv = self.frame(app, cfg, 100.0, w=110, h=32)
        self.assertIn("Overwrite? (y/n)", cv.text().splitlines()[self.row_of(cv, "waiting at a prompt")[0]])
        self.assertEqual(self.cell(cv, "waiting at a prompt", cfg).get("fg"), tui().col(cfg, "warn"))
        bar = cv.text().splitlines()[-1]
        self.assertIn("last heard 2m05s ago", bar)
        app.feed({"event": "tool", "action": "run", "target": "pytest", "ts": 3.0})
        self.assertNotIn("last heard", self.frame(app, cfg, 101.0, w=110, h=32).text().splitlines()[-1],
                         "heard again: nothing to say")
        self.assertIn("waiting at a prompt", self.frame(app, cfg, 101.0, w=110, h=32).text(), "the warning stays")

    def test_an_answer_wraps_and_the_run_reads_as_finished(self):
        # T-1320: a question's answer is one long line; it wraps in Activity, and nothing reads as still running
        long = "parse_dates treats a date with no timezone as UTC " * 6
        app, cfg = self.app(RUN[:1] + [{"event": "answer", "text": long.strip(), "ts": 5.0}])
        cv = self.frame(app, cfg, 100.0, w=110, h=32)
        text = cv.text()
        self.assertGreaterEqual(text.count("treats a date"), 4, "every part of the answer is on screen")
        self.assertIn("ANSWERED", text)
        self.assertNotIn("…", "".join(line for line in text.splitlines() if "treats a date" in line))

    def test_no_state_is_shown_by_colour_alone(self):
        """Mono theme: every verdict still reads as a word or a mark."""
        cfg = dict(tui().DEFAULTS, theme=tui().PRESETS["mono"](), preset="mono")
        for events, words in ((RUNNING, ("RED", "GUARD", "✓")), (RUN, ("PASS", "DONE", "GUARD"))):
            app = tui().App(cfg, spawn=lambda *a, **k: None)
            for e in events:
                app.feed(e)
            text = "\n".join("".join(ch for ch, _ in row) for row in self.frame(app, cfg, 100.0).cells)
            for word in words:
                self.assertIn(word, text)


class Record(unittest.TestCase):
    def test_a_run_records_to_a_video(self):
        import shutil
        import tempfile
        if not (shutil.which("ffmpeg") and shutil.which("rsvg-convert")):
            self.skipTest("needs ffmpeg and rsvg-convert")
        out = os.path.join(tempfile.mkdtemp(), "run.mp4")
        tui().record(RUN, out, size=(60, 20), fps=4, seconds=2)
        self.assertGreater(os.path.getsize(out), 1000)

    def test_without_ffmpeg_it_says_so(self):
        with unittest.mock.patch("shutil.which", lambda name: None):
            with self.assertRaises(RuntimeError) as e:
                tui().record(RUN, "x.mp4")
        self.assertIn("ffmpeg", str(e.exception))


class Config(unittest.TestCase):
    def write(self, text):
        import tempfile
        path = os.path.join(tempfile.mkdtemp(), "tui.toml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_a_users_file_sets_theme_colours_layout_and_keys(self):
        cfg, errors = tui().load_config(self.write(
            'theme = "paper"\nborder = "heavy"\n[colors]\nok = "#007A00"\naccent = { fg = 33, bold = false }\n'
            '[layout]\ncolumns = [["log", "files"]]\nwidths = [100]\n[keys]\nx = "stop"\nq = "none"\n"ctrl+r" = "resume"\n'))
        self.assertEqual(errors, [])
        self.assertEqual(cfg["theme"]["ok"], {"fg": "#007A00"})
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

    def test_signal_is_a_colour_blind_safe_theme(self):
        import fmcodetui
        cfg, errors = tui().load_config(self.write('theme = "signal"\n'))
        self.assertEqual(errors, [])
        ok, bad = (fmcodetui._rgb(cfg["theme"][n]["fg"]) for n in ("ok", "bad"))
        self.assertGreater(ok[2], ok[0], "pass is blue, not green")
        self.assertGreater(bad[0], bad[2], "fail is orange-red")
        self.assertGreater(abs(ok[2] - bad[2]) + abs(ok[0] - bad[0]), 250, "far apart for red-green blindness")

    def test_a_colour_too_faint_to_read_is_named_and_skipped(self):
        cfg, errors = tui().load_config(self.write('[colors]\ndim = "#18202C"\nok = "#7CFC8A"\n'))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("colors.dim", errors[0])
        self.assertIn(":1", errors[0], "it says the contrast")
        self.assertNotEqual(cfg["theme"]["dim"].get("fg"), "#18202C", "the theme's own dim stays")
        self.assertEqual(cfg["theme"]["ok"]["fg"], "#7CFC8A", "a readable one applies")

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

    def budgets(self, **values):
        """T-1315: tiny budgets so a short sleep is over them."""
        for name, value in values.items():
            p = unittest.mock.patch.object(tui(), name, value)
            p.start()
            self.addCleanup(p.stop)

    def app(self, panel="slow"):
        cfg, errors = tui().load_config(Config.write(self, f'[layout]\ncolumns = [["log"], ["{panel}"]]\nwidths = [60, 40]\n'))
        self.assertEqual(errors, [])
        return tui().App(cfg, spawn=lambda *a, **k: None), cfg

    def notes(self, app):
        return [str(n.get("text")) for n in app.state.log if n.get("kind") == "error"]

    def test_a_command_that_raises_is_said_in_activity_and_switched_off(self):
        calls = []

        def bad(app):
            calls.append(1)
            raise RuntimeError("kaboom")
        tui().API().command("bad_cmd", bad, key="b")
        app, _ = self.app("checks")
        app.key("b")
        app.key("b")
        self.assertEqual(len(calls), 1, "switched off after the first failure")
        self.assertEqual(len(self.notes(app)), 1, self.notes(app))
        self.assertIn("command bad_cmd failed: RuntimeError: kaboom; switched off", self.notes(app)[0])
        app.key("?")  # the screen keeps running: a built-in still works
        self.assertEqual(app.mode, "help")

    def test_a_slow_command_is_switched_off_with_how_long_it_took(self):
        self.budgets(COMMAND_BUDGET=0.001)
        calls = []
        tui().API().command("slow_cmd", lambda app: (calls.append(1), time.sleep(0.01)), key="b")
        app, _ = self.app("checks")
        app.key("b")
        app.key("b")
        self.assertEqual(len(calls), 1)
        note = self.notes(app)[0]
        self.assertIn("command slow_cmd took", note)
        self.assertIn("ms; switched off", note)

    def test_a_slow_handler_is_switched_off_once(self):
        self.budgets(HANDLER_BUDGET=0.001)
        calls = []
        tui().API().on("*", lambda st, e: (calls.append(1), time.sleep(0.01)))
        st = tui().State()
        for e in RUN:
            st.apply(e)
        self.assertEqual(len(calls), 1)
        self.assertEqual(st.status, "closed")
        notes = [str(n.get("text")) for n in st.log if n.get("kind") == "error"]
        self.assertEqual(len(notes), 1, notes)
        self.assertIn("ms; switched off", notes[0])

    def test_a_slow_panel_is_switched_off_after_three_frames_running(self):
        self.budgets(PANEL_BUDGET=0.001)
        calls, slow = [], [True]

        def panel(st, w, h, app):
            calls.append(1)
            if slow[0]:
                time.sleep(0.01)
            return [[("tick", "ok")]]
        tui().API().panel("slow", "Slow", panel)
        app, cfg = self.app()
        tui().render(app.state, 110, 32, cfg, app)
        tui().render(app.state, 110, 32, cfg, app)
        slow[0] = False
        tui().render(app.state, 110, 32, cfg, app)  # a fast frame resets the count
        slow[0] = True
        for _ in range(2):
            tui().render(app.state, 110, 32, cfg, app)
        self.assertEqual(self.notes(app), [], "not three frames running yet")
        tui().render(app.state, 110, 32, cfg, app)
        self.assertEqual(len(calls), 6)
        text = tui().render(app.state, 110, 32, cfg, app).text()
        self.assertEqual(len(calls), 6, "switched off: not called again")
        self.assertIn("switched off", text)
        self.assertEqual(len(self.notes(app)), 1)
        self.assertIn("panel slow took", self.notes(app)[0])

    def test_a_slow_built_in_panel_is_never_switched_off(self):
        self.budgets(PANEL_BUDGET=-1.0)  # every frame is over it
        app, cfg = self.app("checks")
        for e in RUN:
            app.feed(e)
        for _ in range(5):
            text = tui().render(app.state, 110, 32, cfg, app).text()
        self.assertNotIn("switched off", text)
        self.assertEqual(self.notes(app), [])

    def test_a_file_others_can_change_is_skipped(self):
        d = self.folder(**{"open.py": "def setup(api):\n    api.panel('open', 'Open', lambda st, w, h, app: [])\n"})
        os.chmod(os.path.join(d, "open.py"), 0o666)
        errors = tui().load_extensions(d)
        self.assertIn("another user can change it", errors[0])
        self.assertNotIn("open", tui().PANELS)


GOLDEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "golden")
GOLDEN_AT = (0.0, 3.4, 9.1, 30.0)  # seconds into the demo's 30 s playback, from planning to closed


def golden_frame(at, size=(120, 34)):
    """The demo run played to `at` seconds: each row's text plus a digest of every cell's resolved look, so a change
    to any panel's words or colours shows as a diff."""
    import hashlib
    T = tui()
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(root, "demo", "code-tui.jsonl"), encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]
    app = T.App(T.DEFAULTS, spawn=lambda *a, **k: None)
    gap = 30.0 / max(1, len(events))
    fed, out = 0, []
    for k in range(int(at * 10) + 1):  # ten frames a second, so motion has the same history at every instant
        t = k / 10
        while fed < len(events) and fed * gap <= t:
            app.feed(events[fed])
            fed += 1
        cv = T.render(app.state, size[0], size[1], T.DEFAULTS, app, t=1000.0 + t)
    for y, row in enumerate(cv.cells):
        looks = "|".join(repr(sorted(T.resolve(s, T.DEFAULTS, cv.bg[y][x]).items())) for x, (_, s) in enumerate(row))
        out.append("".join(ch for ch, _ in row).rstrip() + "  ⟨" + hashlib.sha1(looks.encode()).hexdigest()[:10] + "⟩")
    return "\n".join(out) + "\n"


class Golden(unittest.TestCase):
    """T-1306: the demo run at fixed instants, compared with plugin/tests/fixtures/golden. A deliberate change to the
    screen rewrites them: FM_GOLDEN=regen python3 plugin/tests/run.py test_code_tui."""

    def test_the_demo_run_draws_as_recorded(self):
        for at in GOLDEN_AT:
            path = os.path.join(GOLDEN, f"demo-{at:04.1f}s.txt")
            got = golden_frame(at)
            if os.environ.get("FM_GOLDEN") == "regen":
                os.makedirs(GOLDEN, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(got)
            with self.subTest(at=at):
                with open(path, encoding="utf-8") as f:
                    want = f.read()
                self.assertEqual(got, want, f"the screen at {at}s changed: if that's meant, FM_GOLDEN=regen")


class Fuzz(unittest.TestCase):
    """T-1306: a newer fm code, a hand-edited events file or a bug can send any event; the screen never falls over."""
    KINDS = ["start", "plan", "task", "step", "say", "tokens", "action", "worker", "revert", "fix", "verify", "changed",
             "closed", "blocked", "error", "answer", "resume", "exit", "nonsense", "__init__", None, 5]
    VALUES = [None, "", "x", "日本語テキスト", "é", "\x1b[31mred\x07", "a" * 3000, 0, -1, 10 ** 12, 3.5, [], {},
              [1, 2], {"a": 1}, True, "\n\n\t", " \n ", float("nan"), float("inf"), float("-inf"), 1e300]
    FIELDS = ["text", "plan", "step", "criterion", "label", "exit", "cmd", "output", "files", "stat", "total_in",
              "total_out", "call_in", "call_out", "action", "target", "result", "detail", "tokens", "task", "worker",
              "ts", "request", "model", "reason", "file", "round", "schema", "verify", "resume", "code", "stderr"]
    SIZES = ((1, 1), (10, 5), (40, 12), (80, 24), (132, 34), (200, 60))

    def event(self, r):
        e = {"event": r.choice(self.KINDS)}
        for k in r.sample(self.FIELDS, r.randint(0, 8)):
            e[k] = r.choice(self.VALUES)
        if r.random() < .3:
            e["plan"] = {"type": r.choice(["FIX", None, 3]), "tier": r.choice(["S", "M", None]),
                         "title": r.choice(self.VALUES), "steps": r.choice([[], ["a", "b"], None, [1, None], "s"]),
                         "criteria": r.choice([[], [{"text": r.choice(self.VALUES), "verify": r.choice(self.VALUES)}],
                                               "x", None, [None]])}
        if r.random() < .3:
            e["stat"] = r.choice([{"a.py": [1, 2]}, {"b": "x"}, {"c": [None, "x"]}, [], {1: [1, 1]}])
        if r.random() < .5:  # mostly sane times, sometimes out of order
            e["ts"] = 1000 + r.uniform(-50, 300)
        return e

    def test_any_event_stream_draws_at_any_size(self):
        import random
        T = tui()
        for seed in range(300):
            r = random.Random(seed)  # a failure names its seed; Random(seed) replays it
            events = [self.event(r) for _ in range(r.randint(0, 40))]
            app = T.App(T.DEFAULTS, spawn=lambda *a, **k: None)
            for e in events:
                app.feed(e)
            for w, h in self.SIZES:
                with self.subTest(seed=seed, size=(w, h)):
                    for t in (100.0, 100.3, 101.7):
                        cv = T.render(app.state, w, h, T.DEFAULTS, app, t=t)
                    self.assertTrue(T.to_svg(cv, T.DEFAULTS).startswith("<svg"))
                    self.assertEqual(len(cv.cells), h)

    def test_a_malformed_event_changes_nothing(self):
        T = tui()
        st = Core.state(self)
        before = repr(vars(st))
        for e in ({"event": "tokens", "total_in": "lots"}, {"event": "step", "step": "two"},
                  {"event": "verify", "criterion": [1]}, {"event": "changed", "files": 5},
                  {"event": "closed", "tokens": ["a", 1]}, {"event": "exit", "code": 1, "stderr": " \n "}):
            st.apply(e)
            self.assertEqual(repr(vars(st)), before, e)
        with self.assertRaises(ValueError, msg="a newer stream is still said, not skipped"):
            st.apply({"event": "start", "schema": T.SCHEMA + 1})
        self.assertEqual(repr(vars(st)), before)

    def test_odd_values_that_are_kept_still_draw(self):
        T = tui()
        st = T.State()
        for e in ({"event": "start", "request": ["a", 1], "model": 5, "worker": {"x": 1}, "task": 7, "ts": float("nan")},
                  {"event": "say", "text": 3, "ts": float("inf")}, {"event": "step", "step": 1, "ts": float("-inf")}):
            st.apply(e)
        self.assertIsNone(st.first_ts, "a time that isn't a finite number isn't a time")
        T.render(st, 80, 24, T.DEFAULTS, None, t=5.0)


class Home(unittest.TestCase):
    """T-1330: fm code opens the app: home lists every Foreman project, a project's view its work and past runs, and a
    run starts in that project's folder."""
    PROJECTS = [
        {"project": "old", "root": "/w/old", "exists": True, "active": None, "queue": 0, "inbox": 1, "blocked": 0,
         "updated": 100.0},
        {"project": "new", "root": "/w/new", "exists": True, "active": {"id": "T-0002", "title": "fix login"},
         "queue": 1, "inbox": 1, "blocked": 1, "updated": 200.0},
        {"project": "gone", "root": "/w/gone", "exists": False, "updated": 150.0},
    ]
    STATE = {"active": {"id": "T-0002", "type": "FIX", "tier": "S", "title": "fix login"},
             "queue": [{"id": "T-0003", "type": "FEATURE", "tier": "S", "title": "add export"}],
             "inbox": [{"id": "T-0004", "type": "FIX", "tier": "S", "title": "typo in help"}],
             "blocked": [{"id": "T-0005", "type": "FIX", "tier": "M", "title": "flaky upload",
                          "reason": "needs a device"}]}

    def app(self, state=None):
        T = tui()
        self.spawned = []
        app = T.App(T.DEFAULTS, spawn=lambda words, opts: self.spawned.append((words, app.root)),
                    projects=lambda: [dict(p) for p in self.PROJECTS],
                    project_state=state or (lambda p: dict(self.STATE, code_dir=None)))
        return T, app

    def text(self, T, app):
        return T.render(app.state, 120, 34, T.DEFAULTS, app, t=100.0).text()

    def test_home_lists_every_project_newest_first_and_a_missing_one_last_saying_why(self):
        T, app = self.app()
        app.show_home()
        self.assertEqual([p["project"] for p in app.items], ["new", "old", "gone"], "a missing folder last")
        text = self.text(T, app)
        for want in ("new", "fix login", "gone", "folder missing", "old"):
            self.assertIn(want, text)

    def test_a_project_view_lists_its_work_and_runs_a_queued_task_there(self):
        T, app = self.app()
        app.show_home()
        app.key("\n")  # opens "new"
        text = self.text(T, app)
        for want in ("fix login", "add export", "typo in help", "flaky upload", "needs a device"):
            self.assertIn(want, text)
        app.item_index = next(i for i, it in enumerate(app.items) if (it.get("task") or {}).get("id") == "T-0003")
        app.key("r")
        self.assertEqual(self.spawned, [(["--task", "T-0003"], "/w/new")])

    def test_n_in_a_project_starts_a_new_request_in_its_folder(self):
        T, app = self.app()
        app.show_home()
        app.key("\n")
        app.key("n")
        for ch in "add a flag":
            app.key(ch)
        app.key("\n")
        self.assertEqual(self.spawned, [(["add a flag"], "/w/new")])

    def test_a_project_whose_state_cant_be_read_says_why_and_home_still_draws(self):
        def broken(p):
            raise RuntimeError("state looks corrupt")
        T, app = self.app(state=broken)
        app.show_home()
        app.key("\n")
        self.assertIn("state looks corrupt", self.text(T, app))
        app.key("\x1b")
        self.assertIn("old", self.text(T, app))

    def test_a_missing_folder_never_starts_a_run(self):
        T, app = self.app()
        app.show_home()
        app.item_index = [p["project"] for p in app.items].index("gone")
        app.key("\n")
        self.assertIn("folder missing", self.text(T, app))
        app.key("n")
        app.key("r")
        self.assertEqual(self.spawned, [])
        self.assertIn("folder", app.message)

    def test_browsing_never_moves_the_runs_folder(self):
        # a resume (r) or diff (d) on the run screen stays with the run's own project
        T, app = self.app()
        app.root = "/w/run"
        app.key("p")
        app.key("\n")
        app.key("\x1b")
        app.key("\x1b")
        self.assertEqual((app.mode, app.root), ("main", "/w/run"))

    def test_esc_in_the_request_box_goes_back_to_the_project(self):
        T, app = self.app()
        app.show_home()
        app.key("\n")
        app.key("n")
        app.key("\x1b")
        self.assertEqual(app.mode, "project")
        self.assertEqual(self.spawned, [])

    def test_p_opens_home_from_a_run(self):
        T, app = self.app()
        app.key("p")
        self.assertEqual(app.mode, "home")


class Command(CodeCase):
    def test_fm_code_with_no_request_and_no_terminal_says_what_to_give(self):
        # T-1330: piped or without a terminal, fm code alone is the usage error it always was (exit 1)
        r = self.code(check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("needs a request", r.stderr)

    def test_fm_code_alone_on_a_terminal_opens_the_app(self):
        # T-1330: like claude, fm code with nothing after it opens the app: this project's view, Esc for every project
        import fcntl
        import pty
        import select
        import struct
        import termios
        from test_code import FM
        self.fm("task", "new", "add export", "--type", "FEATURE", "--tier", "S", "--ac", "done :: true")
        slug = self.fm_json("state")["project"].encode()
        env = dict(self.env(), TERM="xterm-256color")
        pid, fd = pty.fork()
        if pid == 0:
            try:
                fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack("HHHH", 34, 120, 0, 0))
                os.chdir(self.repo)
                os.execve(sys.executable, [sys.executable, FM, "code"], env)
            finally:
                os._exit(127)
        deadline = time.time() + 60  # two fm subprocesses (projects, state) before the first frame, on a busy machine

        def until(want):
            seen = b""
            while want not in seen and time.time() < deadline:
                if select.select([fd], [], [], 0.3)[0]:
                    try:
                        seen += os.read(fd, 65536)
                    except OSError:
                        break
            return seen
        try:
            seen = until(b"add export")
            self.assertIn(b"add export", seen, seen[-1500:])
            self.assertIn(slug, seen, "the project's own view")
            os.write(fd, b"\x1b")
            self.assertIn(b"Foreman projects", until(b"Foreman projects"))
            os.write(fd, b"q")
            while time.time() < deadline:
                done, status = os.waitpid(pid, os.WNOHANG)
                if done:
                    self.assertEqual(os.waitstatus_to_exitcode(status), 0)
                    break
                until(b"\x00")
            else:
                self.fail("q didn't quit")
        finally:
            try:
                os.kill(pid, 9)
            except OSError:
                pass
            os.close(fd)

    def test_fm_code_tui_draws_a_recorded_run(self):
        svg = os.path.join(self.home, "shot.svg")
        fixture = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "demo",
                               "code-tui.jsonl")
        self.code("tui", "--snapshot", svg, "--events", fixture, "--size", "100x30")
        with open(svg, encoding="utf-8") as f:
            body = f.read()
        self.assertTrue(body.startswith("<svg"), body[:80])
        self.assertIn("4e1b9c2", body)

    def test_events_alone_replays_the_run_as_plain_lines(self):
        # T-1363: --events FILE without --snapshot or --record replays it; with no terminal, as Activity lines
        fixture = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "demo",
                               "code-tui.jsonl")
        for extra in ([], ["--plain"]):
            r = self.code("tui", "--events", fixture, *extra, check=False)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("DONE", r.stdout)
            self.assertIn("edit   deploy.py", r.stdout)
        r = self.code("tui", "--events", os.path.join(self.tmp, "missing.jsonl"), check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("missing.jsonl", r.stderr)

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
            fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 24, 80, 0, 0))  # T-1306: the child gets SIGWINCH
            seen = b""
            while b"\x1b[2J" not in seen and time.time() < deadline:
                if select.select([fd], [], [], 0.5)[0]:
                    seen += os.read(fd, 65536)
            self.assertIn(b"\x1b[2J", seen, "a resize clears and draws again")
            os.write(fd, b"q")
            after = b""
            while time.time() < deadline:
                done, status = os.waitpid(pid, os.WNOHANG)
                if done:
                    self.assertEqual(os.waitstatus_to_exitcode(status), 0)
                    break
                if select.select([fd], [], [], 0.2)[0]:
                    try:
                        after += os.read(fd, 65536)
                    except OSError:
                        pass
            else:
                self.fail("q didn't quit")
            while select.select([fd], [], [], 0.2)[0]:  # what it wrote just before it exited
                try:
                    after += os.read(fd, 65536)
                except OSError:
                    break
            for mode, why in ((b"\x1b[?1049l", "the alternate screen is left"), (b"\x1b[?25h", "the cursor shown"),
                              (b"\x1b[?7h", "wrap back on")):
                self.assertIn(mode, after, why)
        finally:
            try:
                os.kill(pid, 9)
                os.waitpid(pid, 0)
            except (OSError, ChildProcessError):
                pass
            os.close(fd)

    def _in_terminal(self, *argv, want):
        """T-1343: fm code ARGV in a 100x30 pseudo-terminal: (what it wrote by `want`, its exit code or None)."""
        import fcntl
        import pty
        import select
        import struct
        import termios
        from test_code import FM
        env = dict(self.env(), TERM="xterm-256color")
        env.pop("NO_COLOR", None)
        pid, fd = pty.fork()
        if pid == 0:
            try:
                fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))
                os.chdir(self.repo)
                os.execve(sys.executable, [sys.executable, FM, "code", *argv], env)
            finally:
                os._exit(127)
        seen, code, deadline = b"", None, time.time() + 40
        try:
            while want not in seen and time.time() < deadline:
                if select.select([fd], [], [], 0.5)[0]:
                    try:
                        seen += os.read(fd, 65536)
                    except OSError:
                        break
            if b"\x1b[?1049h" in seen:  # the app: q quits it
                os.write(fd, b"q")
            while time.time() < deadline:
                done, status = os.waitpid(pid, os.WNOHANG)
                if done:
                    code = os.waitstatus_to_exitcode(status)
                    break
                if select.select([fd], [], [], 0.2)[0]:
                    try:
                        seen += os.read(fd, 65536)
                    except OSError:
                        pass
            return seen, code
        finally:
            try:
                os.kill(pid, 9)
                os.waitpid(pid, 0)
            except (OSError, ChildProcessError):
                pass
            os.close(fd)

    def test_fm_code_with_a_request_on_a_terminal_runs_it_in_the_app(self):
        # T-1343: like claude "<prompt>", fm code "<request>" on a terminal opens the app with that run going
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        seen, code = self._in_terminal("fix add", "--model", "fake", "--no-commit", want=b"CLOSED")
        self.assertIn(b"CLOSED", seen, seen[-2000:])
        self.assertIn(b"\x1b[?1049h", seen, "the app's screen, not printed lines")
        self.assertEqual(code, 0, "q quits")
        self.assertIn("a + b", self.calc())

    def test_plain_on_a_terminal_prints_fm_codes_own_lines(self):
        # T-1343: --plain keeps today's output on a terminal: fm code's own lines, no screen
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="x"))
        seen, code = self._in_terminal("fix add", "--model", "fake", "--no-commit", "--plain", want=b"closed (tokens")
        self.assertIn(b"T-0001 closed (tokens", seen, seen[-2000:])
        self.assertNotIn(b"\x1b[?1049h", seen, "no screen")
        self.assertNotIn(b"DONE", seen, "fm code's lines, not the app's Activity lines")
        self.assertEqual(code, 0)

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
