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


class QueueQuote(ForemanTestCase):
    def test_a_quote_from_finished_tasks_of_each_type_and_tier(self):  # T-1878
        import collections
        from unittest import mock
        import fmcore as c
        import fmcost
        self.fm("init")
        for n in range(2):  # history: two small fixes closed
            tid = first(self.fm("task", "new", f"done {n}", "--type", "FIX", "--tier", "S", "--ac", "ok :: true",
                                "--step", "a", "--focus", "--json").stdout)["id"]
            self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
            self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        self.fm("task", "new", "Next fix", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "a")
        self.fm("task", "new", "New kind", "--type", "PERF", "--tier", "M", "--ac", "ok :: true", "--step", "a")
        p = c.find_project(self.repo)
        order = c.order_queue(c.load_briefs(p))[0]
        week = collections.Counter({"T-0001": 100_000, "T-0002": 300_000})
        with mock.patch.object(fmcost, "task_costs", lambda p, days: week if days > 1 else collections.Counter(x=5000)):
            q = fmcost.queue_quote(p, order)
        self.assertEqual((q["tasks"], q["tokens"], q["no_history"], q["last_day"]), (2, 200_000, ["T-0004"], 5000))
        self.assertIn("Quote: 2 task(s) ≈ 200k tokens", fmcost.quote_line(q))
        self.assertIn("no history: T-0004", fmcost.quote_line(q))
        d = json.loads(self.fm("queue", "--cost", "--json").stdout)  # no transcripts here: nothing has history
        self.assertEqual((d["quote"]["tokens"], sorted(d["quote"]["no_history"])), (0, ["T-0003", "T-0004"]))
        self.assertNotIn("quote", json.loads(self.fm("queue", "--json").stdout))  # only when asked: it scans


if __name__ == "__main__":
    unittest.main()
