#!/usr/bin/env python3
"""T-1537: the taste ledger for looks: a kept look, a reverted one and 'not like that' move its rank; a 12-pair
calibration picker records twelve answers; learning reads only the local files the user names."""
import builtins
import io
import json
import os
import socket
import unittest
from unittest import mock

from helpers import PLUGIN, ForemanTestCase, read_text  # puts plugin/lib on sys.path
import fmcore as c
import fmtaste

LOOKS = os.path.join(PLUGIN, "skills", "library", "cards", "looks")


class Opens:
    """Every path builtins.open and os.open are asked for while it's active."""

    def __init__(self):
        self.paths, self._open, self._os_open = [], builtins.open, os.open

    def __enter__(self):
        def op(f, *a, **kw):
            if isinstance(f, (str, bytes, os.PathLike)):
                self.paths.append(os.path.realpath(f))
            return self._open(f, *a, **kw)

        def os_op(f, *a, **kw):
            self.paths.append(os.path.realpath(f))
            return self._os_open(f, *a, **kw)
        self._patches = [mock.patch.object(builtins, "open", op), mock.patch.object(os, "open", os_op),
                         mock.patch.object(socket, "socket", side_effect=AssertionError("no network"))]
        for p in self._patches:
            p.start()
        return self

    def __exit__(self, *exc):
        for p in self._patches:
            p.stop()

    def outside(self, *allowed):
        allowed = [os.path.realpath(a) for a in allowed]
        return [x for x in self.paths if not any(x == a or x.startswith(a + os.sep) for a in allowed)]


class Ledger(ForemanTestCase):
    def test_a_kept_and_a_reverted_look_update_the_ledger(self):
        self.fm("looks", "keep", "look-lido")
        self.fm("looks", "keep", "Night market")  # a title works as well as the card's name
        ledger = os.path.join(c.state_dir(), "taste", "looks.json")
        events = json.loads(read_text(ledger))["events"]
        self.assertEqual([(e["signal"], e["look"]) for e in events],
                         [("kept", "look-lido"), ("kept", "look-night-market")])
        top = self.fm_json("looks")["looks"]
        self.assertEqual(len(top), 12, "every look is ranked, the unseen ones at 0")
        self.assertEqual({top[0]["look"], top[1]["look"]}, {"look-lido", "look-night-market"})
        self.fm("looks", "revert", "lido", "--why", "too cheerful for a bank")
        self.fm("looks", "not", "look-lido", "--why", "not like that")
        rank = {r["look"]: r for r in self.fm_json("looks")["looks"]}
        self.assertLess(rank["look-lido"]["score"], 0)
        self.assertEqual(rank["look-lido"]["kept"], 1)
        self.assertEqual(rank["look-lido"]["reverted"], 1)
        self.assertEqual(self.fm_json("looks")["looks"][0]["look"], "look-night-market")
        self.assertEqual(self.fm_json("looks")["looks"][-1]["look"], "look-lido")
        last = json.loads(read_text(ledger))["events"][-1]
        self.assertEqual((last["signal"], last["why"]), ("not", "not like that"))

    def test_an_unknown_look_or_signal_writes_nothing(self):
        p = self.fm("looks", "keep", "look-nope", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("look-lido", p.stderr, "names the looks there are")
        p = self.fm("looks", "keep", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(c.state_dir(), "taste", "looks.json")))
        with self.assertRaises(ValueError):
            fmtaste.record("loved", "look-lido")

    def test_the_ledger_stays_bounded_and_survives_a_corrupt_file(self):
        path = fmtaste.ledger_path()
        os.makedirs(os.path.dirname(path))
        with open(path, "w") as f:
            f.write("{not json")
        fmtaste.record("kept", "look-lido")  # a broken ledger starts over rather than failing every call
        self.assertEqual(len(fmtaste.load()["events"]), 1)
        odd = [{"signal": "kept", "look": ["x"]}, {"signal": "calibration", "pairs": [[1, {}]], "answers": "a"},
               {"signal": "calibration", "pairs": "ab"}, "junk", None]
        self.assertEqual(fmtaste.scores(odd), {}, "a hand-edited ledger's odd rows are skipped, not a crash")
        with mock.patch.object(fmtaste, "EVENTS_KEEP", 5):
            for _ in range(9):
                fmtaste.record("not", "look-lab-notebook", why="x" * 5000)
            events = fmtaste.load()["events"]
        self.assertEqual(len(events), 5)
        self.assertLessEqual(max(len(e.get("why", "")) for e in events), fmtaste.WHY_CAP)


class Calibration(ForemanTestCase):
    def test_the_calibration_picker_records_twelve_answers(self):
        shown = self.fm_json("looks", "calibrate")
        pairs = shown["pairs"]
        self.assertEqual(len(pairs), 12)
        names = {os.path.splitext(n)[0] for n in os.listdir(LOOKS) if n.startswith("look-")}
        seen = [x for a, b in pairs for x in (a["look"], b["look"])]
        self.assertTrue(all(a["look"] != b["look"] for a, b in pairs))
        self.assertEqual(set(seen), names, "every look is shown")
        self.assertEqual(len({frozenset((a["look"], b["look"])) for a, b in pairs}), 12, "no pair twice")
        for few in ("a,b", "a," * 12 + "a", "a,b,x,a,b,a,b,a,b,a,b,a"):
            p = self.fm("looks", "calibrate", "--answers", few, check=False)
            self.assertNotEqual(p.returncode, 0, few)
        self.assertEqual(fmtaste.load()["events"], [])
        answers = "a,b,n,a,b,a,b,a,b,a,b,a"
        got = self.fm_json("looks", "calibrate", "--round", str(shown["round"]), "--answers", answers)
        self.assertEqual(got["answered"], 12)
        cal = fmtaste.load()["events"][-1]
        self.assertEqual(cal["signal"], "calibration")
        self.assertEqual(cal["answers"], answers.replace(",", ""))
        self.assertEqual([list(x) for x in cal["pairs"]], [[a["look"], b["look"]] for a, b in pairs])
        rank = {r["look"]: r["score"] for r in self.fm_json("looks")["looks"]}
        self.assertEqual(rank[pairs[0][0]["look"]] - rank[pairs[0][1]["look"]] != 0, True)
        again = self.fm_json("looks", "calibrate")
        self.assertNotEqual(again["round"], shown["round"], "the next calibration pairs them differently")

    def test_the_keyboard_picker_takes_one_key_a_pair_and_stops_on_q(self):
        pairs = fmtaste.pairs(fmtaste.looks())
        keys = iter("x1" + "2" * 10 + "n")  # x isn't an answer: asked again
        out = io.StringIO()
        self.assertEqual(fmtaste.pick(pairs, lambda: next(keys), out.write), list("a" + "b" * 10 + "n"))
        self.assertIn("12/12", out.getvalue())
        keys = iter("12q")
        self.assertIsNone(fmtaste.pick(pairs, lambda: next(keys), io.StringIO().write))
        self.assertIsNone(fmtaste.pick(pairs, lambda: "", io.StringIO().write), "end of input stops it too")

    def test_ranking_orders_looks_by_what_was_kept(self):
        fmtaste.record("kept", "look-observatory")
        fmtaste.record("kept", "look-observatory")
        fmtaste.record("kept", "look-lido")
        fmtaste.record("not", "look-cartographer", why="too busy")
        order = [r["look"] for r in fmtaste.rank()]
        self.assertEqual(order[:2], ["look-observatory", "look-lido"])
        self.assertEqual(order[-1], "look-cartographer")
        self.assertIn("look-observatory", self.fm("looks").stdout.splitlines()[1])


class Sources(ForemanTestCase):
    def _page(self):
        site = os.path.join(self.tmp, "site")
        os.makedirs(site)
        with open(os.path.join(site, "style.css"), "w") as f:
            f.write("body { color: #262D2E }\n")
        page = os.path.join(site, "page.html")
        with open(page, "w") as f:  # Lido's accent and ground, a linked sheet and a remote image it must not follow
            f.write('<link rel="stylesheet" href="style.css"><img src="https://example.com/x.png">'
                    '<p style="color:#076E87;background:#F0F9FA">Book a lane at the pool: timetable</p>')
        return site, page

    def test_nothing_reads_a_file_the_user_didnt_name(self):
        site, page = self._page()
        before = os.stat(page).st_mtime_ns
        with Opens() as seen:
            got = fmtaste.learn([page])
            fmtaste.rank()
            fmtaste.record("kept", "look-lido")
            fmtaste.pairs(fmtaste.looks())
        self.assertEqual(got["learned"][0]["look"], "look-lido")
        self.assertEqual(seen.outside(LOOKS, c.state_dir()), [os.path.realpath(page)])
        self.assertNotIn(os.path.join(site, "style.css"), seen.paths)
        self.assertEqual(os.stat(page).st_mtime_ns, before, "the named file is only read")
        event = [e for e in fmtaste.load()["events"] if e["signal"] == "learned"][0]
        self.assertEqual(event["source"], "page.html", "the ledger keeps the file's name, never its text or path")

    def test_only_local_regular_files_and_only_so_much_of_them(self):
        site, page = self._page()
        for bad in ("https://example.com/page.html", "file:///etc/passwd", site, os.path.join(site, "missing")):
            with self.subTest(bad=bad):
                got = fmtaste.learn([bad])
                self.assertEqual(got["learned"], [])
                self.assertEqual(len(got["skipped"]), 1)
        big = os.path.join(self.tmp, "big.css")
        with open(big, "w") as f:
            f.write("a" * (fmtaste.SOURCE_CAP + 10) + " #076E87 #F0F9FA")
        self.assertEqual(len(fmtaste.read_named(big)), fmtaste.SOURCE_CAP)
        self.assertEqual(fmtaste.learn([big])["learned"], [], "nothing past the cap is read")
        fifo = os.path.join(self.tmp, "pipe")
        os.mkfifo(fifo)
        self.assertEqual(len(fmtaste.learn([fifo])["skipped"]), 1, "a pipe is refused, not waited on")
        heic = os.path.join(self.tmp, "x.heic")
        with open(heic, "wb") as f:
            f.write(b"\0\0\0\x18ftypheic #076E87 #076E87")
        self.assertEqual(fmtaste.learn([heic])["learned"], [], "an unknown binary is noise, not colours")
        with mock.patch.object(fmtaste, "LEARN_MAX", 1):
            got = fmtaste.learn([page, page])
        self.assertEqual((len(got["learned"]), len(got["skipped"])), (1, 1), "a run reads LEARN_MAX files at most")
        p = self.fm("looks", "learn", check=False)
        self.assertNotEqual(p.returncode, 0, "learn needs a path the user names")

    def test_a_photo_needs_an_installed_reader_and_says_so(self):
        photo = os.path.join(self.tmp, "shot.png")
        with open(photo, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\0" * 64)
        with mock.patch.dict("sys.modules", {"PIL": None, "PIL.Image": None}):
            got = fmtaste.learn([photo])
        self.assertEqual(got["learned"], [])
        self.assertIn("Pillow", got["skipped"][0]["why"])
        self.assertNotIn("install", got["skipped"][0]["why"].split("Pillow")[0], "detected, never installed")


class CodeApp(ForemanTestCase):
    def test_fm_code_has_a_keyboard_picker_that_records_twelve_answers(self):
        import fmcodetui as tui
        app = tui.App(tui.load_config()[0], spawn=lambda *a, **k: None)
        app.key("L")
        self.assertEqual(app.mode, "looks")
        text = tui.render(app.state, 120, 40, app.cfg, app).text()
        self.assertIn("1/12", text)
        first = fmtaste.looks()[fmtaste.pairs(fmtaste.looks())[0][0]]["title"]
        self.assertIn(first, text)
        for k in "1" * 11:
            app.key(k)
        app.key("\x1b")  # stopped before twelve: nothing recorded
        self.assertEqual(app.mode, "main")
        self.assertEqual(fmtaste.load()["events"], [])
        app.key("L")
        app.key("KEY_DOWN")
        app.key("\n")  # Enter takes the highlighted one: the second look
        for k in "x" + "12n" * 3 + "1":  # x answers nothing
            app.key(k)
        self.assertEqual(app.mode, "looks")
        app.key("n")
        self.assertEqual(app.mode, "main")
        self.assertEqual(fmtaste.load()["events"][-1]["answers"], "b" + "abn" * 3 + "an")
        self.assertIn("12 answers", app.message)


class Surfaces(unittest.TestCase):
    def test_claude_code_has_a_user_only_command_and_the_directions_skill_ranks_by_it(self):
        cmd = read_text(os.path.join(PLUGIN, "commands", "looks.md"))
        self.assertIn("disable-model-invocation: true", cmd)
        for word in ("AskUserQuestion", "fm looks calibrate", "--answers", "--round", "fm looks learn"):
            self.assertIn(word, cmd)
        skill = read_text(os.path.join(PLUGIN, "skills", "directions", "SKILL.md"))
        for word in ("fm looks", "fm looks keep", "fm looks not", "fm looks revert"):
            self.assertIn(word, skill)


if __name__ == "__main__":
    unittest.main()
