"""T-0114: fm queue --preview shows each queued and inbox item with the usual time for its type and size here, and what
will need the user under the current autonomy, gathered so they can be answered together before a long run."""
import json
import unittest

from helpers import ForemanTestCase

first = lambda text: json.JSONDecoder().raw_decode(text)[0]


class QueuePreview(ForemanTestCase):
    def test_usual_times_and_what_needs_the_user(self):
        self.fm("init")
        for n in range(3):  # history: three small features closed
            tid = first(self.fm("task", "new", f"done {n}", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                                "--step", "a", "--focus", "--json").stdout)["id"]
            self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        self.fm("task", "new", "Big one", "--type", "FEATURE", "--tier", "L", "--interpretation", "x", "--approach", "y",
                "--ac", "ok :: true", "--step", "a")                              # T-0004: an L plan
        self.fm("task", "new", "Small one", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a")
        self.fm("capture", "Later idea", "--type", "FEATURE", "--tier", "S")      # T-0006, inbox
        data = json.loads(self.fm("queue", "--preview", "--json").stdout)
        rows = {r["id"]: r for r in data["items"]}
        self.assertEqual(set(rows), {"T-0004", "T-0005", "T-0006"})
        self.assertEqual(rows["T-0004"]["needs"], ["plan approval"])
        self.assertEqual(rows["T-0005"]["needs"], [])
        self.assertIsInstance(rows["T-0005"]["minutes"], int)  # FEATURE/S has history here
        self.assertIsNone(rows["T-0004"]["minutes"])  # FEATURE/L has none
        out = self.fm("queue", "--preview").stdout
        self.assertIn("1 need you", out)
        self.assertIn("T-0004", out.split("\n")[1])  # the asks come first, together
        self.fm("autonomy", "full")
        self.assertEqual({r["id"]: r for r in json.loads(self.fm("queue", "--preview", "--json").stdout)["items"]}
                         ["T-0004"]["needs"], [], "full autonomy approves its own plans")


if __name__ == "__main__":
    unittest.main()
