#!/usr/bin/env python3
"""T-1672: the taste ledger's follow-ups: a look of the day rolled with the ledger's lean (and the pane's idle line),
where taste turned (bisect), a style séance for the departed looks, and kept/reverted read from DESIGN.md's git
history, each stint recorded once."""
import os
import subprocess
import unittest.mock as mock

from helpers import ForemanTestCase
import fmtaste


def events(*rows):
    """(signal, look[, why]) rows as ledger events a minute apart, oldest first."""
    return [dict({"ts": f"2026-10-01T00:{i:02}:00Z", "signal": s, "look": f"look-{look}"}, **({"why": w[0]} if w else {}))
            for i, (s, look, *w) in enumerate(rows)]


class Roll(ForemanTestCase):
    def test_the_same_all_day_and_leaning_to_what_was_kept(self):
        self.assertEqual({fmtaste.roll("2026-10-01") for _ in range(5)}, {fmtaste.roll("2026-10-01")})
        days = [f"2026-11-{d:02}" for d in range(1, 31)]
        self.assertGreater(len({fmtaste.roll(d, events=[]) for d in days}), 3, "with no taste: a fair draw")
        lean = events(*[("kept", "lido")] * 5)
        self.assertGreater(sum(fmtaste.roll(d, events=lean) == "look-lido" for d in days), 20, "kept five times")

    def test_the_pane_line_waits_for_taste_then_names_the_keep(self):
        self.fm("init")
        self.assertIsNone(fmtaste.roll_line())
        self.assertIsNone(self.fm_json("ui").get("look"))
        self.fm("looks", "keep", "lido")
        line = fmtaste.roll_line()
        self.assertTrue(line.startswith("Look of the day: "), line)
        self.assertIn("· fm looks keep ", line)
        self.assertEqual(self.fm_json("ui")["look"], line)
        self.assertIn("Look of the day", self.fm("looks", "roll").stdout)


class Bisect(ForemanTestCase):
    def test_the_turn_is_where_the_lean_moved_most(self):
        got = fmtaste.bisect(events(*[("kept", "lido")] * 4, ("reverted", "lido"), *[("kept", "night-market")] * 3))
        self.assertEqual((got["event"], got["before"], got["after"], got["at"]),
                         (4, "look-lido", "look-night-market", "2026-10-01T00:04:00Z"))

    def test_a_taste_that_held_and_too_few_to_split(self):
        self.assertIsNone(fmtaste.bisect(events(*[("kept", "lido")] * 4))["at"])
        with self.assertRaisesRegex(ValueError, "too few"):
            fmtaste.bisect(events(("kept", "lido")))
        r = self.fm("looks", "bisect", check=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)


class Seance(ForemanTestCase):
    def test_the_departed_with_their_last_words_and_where_they_live_on(self):
        rows = fmtaste.seance(events(("kept", "observatory"), ("reverted", "lido", "too loud"), ("not", "cartographer")))
        self.assertEqual([(r["look"], r["said"], r["lives_on"]) for r in rows],
                         [("look-lido", "too loud", "look-observatory"), ("look-cartographer", None, "look-observatory")])
        self.assertIn("No departed looks", self.fm("looks", "seance").stdout)
        self.fm("looks", "revert", "lido", "--why", "too loud")
        self.assertIn('"too loud"', self.fm("looks", "seance").stdout)


class History(ForemanTestCase):
    def commit(self, direction, day):
        with open(os.path.join(self.repo, "DESIGN.md"), "w", encoding="utf-8") as f:
            f.write(f"# Design\n\n## Point of view\n\nx\n\n## Direction\n\n{direction}\n\n## Knobs\n\nlook-lido (a knob)\n")
        when = f"2026-09-{day:02}T12:00:00+00:00"
        subprocess.run(["git", "-C", self.repo, "add", "DESIGN.md"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", f"design {day}"], check=True,
                       env=dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when))

    def test_a_look_replaced_within_a_week_is_reverted_one_that_stayed_kept_once(self):
        self.commit("look-lido, audacity bold. Runner-up: look-observatory.", 1)
        self.commit("look-night-market, audacity safe.", 3)
        self.commit("look-night-market, audacity bold.", 5)
        self.commit("own: Harbour, audacity wild.", 15)
        got = fmtaste.history(os.path.join(self.repo, "DESIGN.md"), now="2026-09-30T00:00:00Z")
        self.assertEqual([(e["signal"], e["look"]) for e in got["recorded"]],
                         [("reverted", "look-lido"), ("kept", "look-night-market")])
        self.assertEqual([s["look"] for s in got["stints"]], ["look-lido", "look-night-market", None])
        self.assertEqual(fmtaste.scores()["look-night-market"]["score"], 3)
        again = self.fm_json("looks", "history", os.path.join(self.repo, "DESIGN.md"))
        self.assertEqual(again["recorded"], [], "each stint once")
        self.assertEqual(len(fmtaste.load()["events"]), 2)

    def test_a_slow_git_is_refused_and_a_cut_window_drops_its_first_stint(self):  # T-1672 review
        self.commit("look-lido, audacity bold.", 1)
        self.commit("look-night-market, audacity safe.", 3)
        self.commit("look-observatory, audacity safe.", 20)
        path, real = os.path.join(self.repo, "DESIGN.md"), subprocess.run

        def slow(cmd, *a, **k):
            if "show" in cmd:
                raise subprocess.TimeoutExpired(cmd, 1)
            return real(cmd, *a, **k)
        with mock.patch.object(fmtaste.subprocess, "run", side_effect=slow), \
                self.assertRaisesRegex(ValueError, "git failed"):
            fmtaste.history(path)
        with mock.patch.object(fmtaste, "HISTORY_MAX", 2):
            got = fmtaste.history(path, now="2026-09-30T00:00:00Z")
        self.assertEqual([s["look"] for s in got["stints"]], ["look-observatory"], "night-market's start was cut")
        self.assertEqual([(e["signal"], e["look"]) for e in got["recorded"]], [("kept", "look-observatory")])

    def test_a_keep_said_by_hand_during_the_stint_counts_once(self):  # T-1672 review
        self.commit("look-lido, audacity bold.", 1)
        self.commit("look-night-market, audacity safe.", 15)
        fmtaste._append({"ts": "2026-09-05T00:00:00Z", "signal": "kept", "look": "look-lido"})
        got = fmtaste.history(os.path.join(self.repo, "DESIGN.md"), now="2026-09-30T00:00:00Z")
        self.assertEqual([(e["signal"], e["look"]) for e in got["recorded"]], [("kept", "look-night-market")])

    def test_a_file_with_no_history_is_refused(self):
        with self.assertRaisesRegex(ValueError, "no git history"):
            fmtaste.history(os.path.join(self.repo, "DESIGN.md"))
