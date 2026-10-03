"""T-0125: the self-improvement loop. fm friction digests Foreman's own friction since the last pass; fm next calls for a
pass every N closed tasks; a marked pass starts the next digest after it, which then reports what became of its items."""
import json
import os
import unittest

from helpers import ForemanTestCase

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # --focus prints its own lines after the JSON


class Friction(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def close_one(self, n):
        tid = first(self.fm("task", "new", f"tidy {n}", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus",
                                 "--json").stdout)["id"]
        self.fm("task", "finish", tid, "--run", "true", "--audit", "self check")
        return tid

    def test_the_digest_names_each_kind_of_friction_and_a_pass_starts_the_next_after_it(self):
        self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "npm publish"}})  # a guard block
        tid = first(self.fm("task", "new", "Fix", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus",
                                 "--json").stdout)["id"]
        self.fm("task", "log", tid, "steer: make it faster")
        self.fm("capture", "Gates by path", "--source", "self")
        out = self.fm("friction").stdout
        for needle in ("publish", "steer: make it faster", "Gates by path"):
            self.assertIn(needle, out)
        path = self.fm("friction", "--brief").stdout.strip().split()[-1]
        with open(path, encoding="utf-8") as f:
            brief = f.read()
        self.assertIn("publish", brief)  # self-contained: the digest is in it
        self.assertIn("at most 5", brief)
        self.fm("friction", "--mark")
        out = self.fm("friction").stdout
        self.assertNotIn("steer: make it faster", out)  # the next pass starts after this one
        self.assertIn("Gates by path", out)  # and reports what became of the last pass's self items (open)

    def test_fm_next_calls_for_a_pass_every_n_closed_tasks_at_a_task_boundary(self):
        nxt = lambda: self.fm("next").stdout
        self.close_one(1)
        self.close_one(2)
        self.assertNotIn("self-improvement pass", nxt(), "off unless the project asks for it")
        self.fm("friction", "--every", "2")
        self.assertIn("self-improvement pass", nxt())
        first(self.fm("task", "new", "Busy", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus",
                           "--json").stdout)
        self.assertNotIn("self-improvement pass", nxt(), "never in the middle of a task")

    def test_a_pass_waits_two_hours_after_the_last_so_it_has_friction_to_read(self):
        # T-0154: pass 2 came due 13 minutes after pass 1 with one new friction line
        import fmcore as c
        nxt = lambda: self.fm("next").stdout
        self.fm("friction", "--every", "1")
        self.fm("friction", "--mark")
        self.close_one(1)
        self.assertNotIn("self-improvement pass", nxt())
        p = c.find_project(self.repo)
        meta = c.read_meta(p)
        meta["rsi_at"] = c.iso(c.time.time() - 3 * 3600)
        c.write_meta(p, meta)
        self.assertIn("self-improvement pass", nxt())


if __name__ == "__main__":
    unittest.main()
