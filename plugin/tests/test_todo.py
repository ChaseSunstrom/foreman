"""T-1157: fm todo lists what only the user can do, each with what to type, and drops what is resolved."""
import json
import re
import unittest

from helpers import ForemanTestCase

import fmcore as c


class Todo(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "One", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "x", "--focus")
        self.p = c.find_project(self.repo)

    def pend(self, items):
        meta = c.read_meta(self.p)
        meta["pending_approvals"] = items
        c.write_meta(self.p, meta)

    def test_empty_is_one_line(self):
        self.assertEqual(len(self.fm("todo").stdout.strip().splitlines()), 1)
        self.assertEqual(json.loads(self.fm("todo", "--json").stdout)["todo"], [])

    def test_pending_ask_and_user_block_listed_then_ask_gone_when_granted(self):
        self.pend([{"task": "T-0001", "allow": ["publish"], "why": "ship it", "session": "s", "at": c.now()}])
        self.fm("capture", "Two")
        self.fm("task", "block", "T-0002", "waiting on the user to log in")
        out = self.fm("todo").stdout
        self.assertIn("T-0001", out)
        self.assertIn("publish", out)
        self.assertIn("ship it", out)
        self.assertIn("yes", out)
        self.assertIn("T-0002", out)
        self.assertIn("log in", out)
        self.pend([])  # the user's yes: the hook consumes the request
        out = self.fm("todo").stdout
        self.assertNotIn("publish", out)
        self.assertIn("T-0002", out)

    def test_block_not_for_the_user_is_not_listed(self):
        self.fm("capture", "Two")
        self.fm("task", "block", "T-0002", "flaky network")
        self.assertNotIn("T-0002", self.fm("todo").stdout)

    def test_outward_decision_listed_and_json(self):
        self.fm("decide", "publish the beta", "--why", "w", "--kind", "outward")
        self.fm("decide", "rename a var", "--why", "w")
        out = json.loads(self.fm("todo", "--json").stdout)["todo"]
        self.assertEqual([e["kind"] for e in out], ["decision"])
        self.assertIn("publish the beta", out[0]["text"])
        self.assertIn("fm decide --review", out[0]["command"])

    def test_reversed_decision_not_listed(self):
        self.fm("decide", "publish the beta", "--why", "w", "--kind", "outward")
        self.fm("decide", "hold the beta", "--why", "w", "--reverses", "publish the beta")
        self.assertNotIn("publish the beta", self.fm("todo").stdout)

    def test_old_decisions_counted_not_listed(self):
        self.fm("decide", "publish the beta", "--why", "w", "--kind", "outward")
        path = c.os.path.join(self.p.dir, "decisions.md")
        s = open(path).read()
        open(path, "w").write(re.sub(r"\| \d{4}-\d\d-\d\d \|", "| 2000-01-01 |", s))
        out = self.fm("todo").stdout
        self.assertNotIn("publish the beta", out)
        self.assertIn("1 older: fm decide --review", out)

    def test_expired_ask_says_ask_again(self):
        self.pend([{"task": "T-0001", "allow": ["publish"], "why": "w", "session": "s", "at": "2000-01-01T00:00:00Z"}])
        out = self.fm("todo").stdout
        self.assertIn("expired: ask again", out)
        self.assertNotIn("reply", out)

    def test_user_words_and_no_false_matches(self):
        self.fm("capture", "Two")
        self.fm("capture", "Three")
        self.fm("task", "block", "T-0002", "needs credentials")
        self.fm("task", "block", "T-0003", "hit the token limit")
        out = self.fm("todo").stdout
        self.assertIn("T-0002", out)
        self.assertNotIn("T-0003", out)


if __name__ == "__main__":
    unittest.main()
