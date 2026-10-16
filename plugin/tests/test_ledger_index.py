"""T-1082: fm ui runs on every state change, and one run read the same briefs four times and the same ledger five
times. A process re-uses what it already read from an unchanged file, hands out fresh copies, and reads again when the
file changes."""
import json
import os
from unittest import mock

from helpers import ForemanTestCase

import fmcore as c


class Memo(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.tid = self.fm_json("task", "new", "Memo me", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                                "--step", "s")["id"]

    def settle(self):
        """Briefs written over 2 s ago: a file still that fresh isn't memoized (a same-tick rewrite could pass for it)."""
        for path in c.brief_paths(self.p):
            os.utime(path, (os.path.getmtime(path) - 10, os.path.getmtime(path) - 10))

    def test_an_unchanged_brief_parses_once_and_each_load_is_its_own_copy(self):
        self.settle()
        c.load_briefs(self.p)
        with mock.patch.object(c.Brief, "parse", wraps=c.Brief.parse) as parse:
            a = c.load_briefs(self.p)
            b = c.load_briefs(self.p)
            self.assertEqual(parse.call_count, 0, "unchanged files: no parse")
        a[0].meta["title_extra"] = "x"
        a[0].sections[0][1] = "changed"
        self.assertNotIn("title_extra", b[0].meta)
        self.assertNotEqual(b[0].sections[0][1], "changed")
        self.assertNotIn("title_extra", c.load_briefs(self.p)[0].meta, "a caller's change never reaches the memo")
        self.assertEqual(c.find_brief(self.p, self.tid).render(), b[0].render())

    def test_a_list_edited_in_place_still_renders(self):
        # review: _orig shared meta's lists, so an in-place append compared equal and render dropped it
        self.fm("task", "set", self.tid, "scope=a.py")
        b = c.find_brief(self.p, self.tid)
        b.meta["scope"].append("y.py")
        self.assertIn("y.py", b.render())

    def test_the_memo_forgets_a_vanished_file_and_stays_small(self):
        self.settle()
        c.load_briefs(self.p)
        self.assertTrue(any(k.endswith(".md") for k in c._BRIEF_MEMO))
        path = c.find_brief(self.p, self.tid).path
        os.unlink(path)
        self.assertIsNone(c.find_brief(self.p, self.tid))
        self.assertEqual(c.load_briefs(self.p), [])
        self.assertNotIn(path, c._BRIEF_MEMO)
        self.assertLessEqual(c.TAIL_MEMO_MAX, 20000)

    def test_an_edited_brief_is_read_again(self):
        self.settle()
        c.load_briefs(self.p)
        self.fm("task", "set", self.tid, "--section", "Interpretation", "--text", "new words")
        self.assertIn("new words", c.load_briefs(self.p)[0].section("Interpretation"))
        self.assertIn("new words", c.find_brief(self.p, self.tid).section("Interpretation"))

    def test_a_smaller_tail_after_a_larger_one_reads_nothing_new(self):
        for i in range(30):
            c.log_event(self.p, "probe", data={"i": i})
        big = c.ledger_tail(self.p, 25)
        with mock.patch("builtins.open", side_effect=AssertionError("read again")):
            small = c.ledger_tail(self.p, 10)
        self.assertEqual(small, big[-10:])
        small[0]["event"] = "mutated"
        self.assertNotEqual(c.ledger_tail(self.p, 10)[0]["event"], "mutated")

    def test_an_appended_ledger_is_read_again(self):
        c.ledger_tail(self.p, 50)
        c.log_event(self.p, "probe", data={"i": "last"})
        self.assertEqual((c.ledger_tail(self.p, 5)[-1].get("data") or {}).get("i"), "last")

    def test_the_same_events_as_a_plain_read(self):
        for i in range(12):
            c.log_event(self.p, "probe", data={"i": i})
        with open(os.path.join(self.p.dir, "ledger.jsonl"), encoding="utf-8") as f:
            plain = [json.loads(x) for x in f.read().splitlines()][-7:]
        c.ledger_tail(self.p, 20)
        self.assertEqual(c.ledger_tail(self.p, 7), plain)
