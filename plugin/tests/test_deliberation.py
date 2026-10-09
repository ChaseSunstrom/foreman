"""T-0687 (Intelligence — deliberation): objections that outlive the review, and panels sized by stakes."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c

STUB = r'''#!/usr/bin/env python3
import sys
sys.stdin.read()
print("## Objections\n- the cache is never invalidated\n- there is no rollback path\nVerdict: revise — fix the cache first")
'''


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"]}
        self.fm("init")
        self.p = c.find_project(self.repo)


class Dissent(Base):
    def test_objections_stay_open_until_answered_and_the_close_lists_them(self):
        self.fm("task", "new", "Cache the report", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true",
                "--step", "s")
        for sec in ("Interpretation", "Approach (options → choice → why)"):
            self.fm("task", "set", "T-0001", "--section", sec, "--text", "planned")
        self.fm("second", "plan", "T-0001", env=self.env)
        dissent = c.find_brief(self.p, "T-0001").section("Dissent")
        self.assertIn("- [ ] the cache is never invalidated", dissent)
        self.fm("task", "dissent", "T-0001", "resolve", "1", "invalidated on every write")
        self.assertIn("[x] the cache is never invalidated", c.find_brief(self.p, "T-0001").section("Dissent"))
        self.fm("focus", "T-0001")
        out = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--lens", "intent: ok",
                      "--lens", "edge: ok", "--docs", "none: internal", "--lesson", "none: test")
        text = out.stdout + out.stderr
        self.assertIn("open dissent", text)
        self.assertIn("no rollback", text)
        self.assertNotIn("never invalidated", text.split("open dissent")[1])


class Panel(Base):
    def test_small_tasks_skip_panels_and_large_plans_get_a_second_read(self):
        with open(os.path.join(c.PLUGIN_ROOT, "protocols.json")) as f:
            rules = json.load(f)
        self.assertEqual(rules["S"]["panel"], "none")
        self.fm("task", "new", "Tiny", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        out = self.fm("second", "plan", "T-0001", env=self.env).stdout
        self.assertIn("skipped", out)
        self.assertFalse(c.find_brief(self.p, "T-0001").section("Plan review").strip())
        self.fm("task", "new", "Big change", "--type", "FEATURE", "--tier", "L", "--ac", "ok :: true", "--step", "s")
        for sec in ("Interpretation", "Approach (options → choice → why)", "Build vs reuse"):
            self.fm("task", "set", "T-0002", "--section", sec, "--text", "planned")
        self.fm("task", "drop", "T-0001", "not needed")
        self.assertIn("fm second plan T-0002", self.fm("next").stdout)
