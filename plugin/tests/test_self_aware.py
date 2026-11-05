"""T-3126 (T-3123 part 1): a message that points something out is a miss, logged with its class; `sampo misses` counts
them by class and per day. Fixtures are the user's own words from the evening of 2026-11-05."""
import json

from helpers import ForemanTestCase

from sampo import core as c

MISSES = [
    ("stalled", "why is the graph look or whatever on the local live site not done yet"),
    ("unfiled", "are you also keeping track and fixing all of these slight bugs you come across while using sampo too?"),
    ("unmeasured", "how can we improve the speed/efficiency of the merge queue too?"),
    ("unused", "have you tried using the local models for tasks with you? like the qwen 3.8 27b model"),
    ("invisible", "how can I view all of the cards?"),
    ("other", "think about how to make yourself more self aware and capture things like that in the future so I "
              "don't need to point them out"),
]
NOT_MISSES = ["and also have UI examples of each of the UI cards used and such?", "thanks", "Thanks!",
              "add a dark theme to the settings page"]


class Classify(ForemanTestCase):
    def test_each_of_tonights_six_gets_its_class_and_requests_and_thanks_get_none(self):
        from sampo import selfaware
        for cls, text in MISSES:
            self.assertEqual(selfaware.classify(text), cls, text)
        for text in NOT_MISSES:
            self.assertIsNone(selfaware.classify(text), text)

    def test_a_model_is_asked_only_when_no_pattern_matches_and_its_label_must_be_a_class(self):
        from sampo import selfaware
        asked = []
        ask = lambda text: asked.append(text) or "unused"
        self.assertEqual(selfaware.classify(MISSES[0][1], ask), "stalled")
        self.assertEqual(asked, [])  # a pattern matched: no model
        self.assertEqual(selfaware.classify("did you look at the gpu box lately", ask), "unused")
        self.assertEqual(len(asked), 1)
        self.assertIsNone(selfaware.classify("did you look at it", lambda t: "a made-up label"))
        self.assertIsNone(selfaware.classify("thanks", ask))  # a thanks never reaches the model
        self.assertEqual(len(asked), 1)


class Ledger(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo, create=False)

    def test_note_logs_a_miss_with_its_class_and_misses_prints_counts_by_class_and_day(self):
        from sampo import selfaware
        for cls, text in MISSES:
            self.assertEqual(selfaware.note(self.p, text, session="s1"), cls)
        self.assertIsNone(selfaware.note(self.p, "thanks", session="s1"))
        rows = c.ledger_events(self.p, ["miss"])
        self.assertEqual([r["data"]["cls"] for r in rows], [m[0] for m in MISSES])
        out = self.fm("misses").stdout
        for cls, _ in MISSES:
            self.assertIn(cls, out)
        self.assertIn(rows[0]["ts"][:10], out)
        self.assertIn("6", out)
        data = json.loads(self.fm("misses", "--json").stdout)
        self.assertEqual(data["total"], 6)
        self.assertEqual(data["by_class"]["stalled"], 1)
        self.assertEqual(data["by_day"][rows[0]["ts"][:10]], 6)

    def test_the_prompt_hook_logs_a_miss_and_not_a_request(self):
        from sampo import hooks
        for text in (MISSES[4][1], NOT_MISSES[0]):
            hooks.user_prompt_submit({"session_id": "s2", "cwd": self.repo, "prompt": text})
        rows = c.ledger_events(self.p, ["miss"])
        self.assertEqual([r["data"]["cls"] for r in rows], ["invisible"])
