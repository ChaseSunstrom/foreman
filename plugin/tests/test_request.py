"""T-0696 (Intelligence — understanding the request and the user): every clause of a message accounted for, standing
steers turned into rule candidates, corrections as a task's fate, misreadings from the oracle, and asks left
unanswered."""
import os
import re
import time

from helpers import ForemanTestCase

import fmcore as c

ORACLE_STUB = r'''#!/usr/bin/env python3
import sys
sys.stdin.read()
print("## Examples\n- GIVEN a report WHEN exported THEN a CSV downloads")
print("## Ambiguities\n- none")
print("## Misreadings\n- exporting every report instead of the one on screen — ask which reports before building")
'''


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def done(self, title):
        self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        tid = c.load_briefs(self.p)[-1].id
        return tid


class Clauses(Base):
    def test_each_clause_maps_to_a_task_or_is_named_until_noted(self):
        self.fm("capture", "Add a CSV export to the reports page", "--type", "FEATURE", "--tier", "S")
        out = self.fm("clauses", "Add a CSV export to the reports page. Also fix the login timeout on mobile.").stdout
        self.assertRegex(out, r"CSV export.*→ T-0001")
        self.assertRegex(out, r"login timeout.*unaccounted")
        self.assertIn("1 clause(s) of the last request unaccounted", self.fm("next").stdout)
        self.fm("clauses", "--note", "1", "answered in chat: it's a server setting")
        self.assertNotIn("unaccounted", self.fm("next").stdout)


class Steers(Base):
    def test_a_standing_steer_is_a_rule_candidate_at_close_and_a_veto_proposal_at_once(self):
        tid = self.done("Build the release")
        self.fm("task", "log", tid, "steer: never commit generated files, from now on")
        self.fm("task", "log", tid, "steer: use the smaller icon here")
        r = self.fm("task", "finish", tid, "--audit", "self", "--run", "true")
        self.assertIn("Standing steer", r.stdout + r.stderr)
        self.assertNotIn("smaller icon", r.stdout + r.stderr)
        self.assertRegex(self.fm("taste").stdout, r"commit.*generated")


class Reactions(Base):
    def test_a_correction_logged_against_a_closed_task_makes_it_corrected(self):
        tid = self.done("Rename the module")
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true")
        time.sleep(1)
        c.log_event(self.p, "correction", task=tid, data={"text": "no, keep the old name for the CLI"})
        self.assertRegex(self.fm("outcomes").stdout, rf"{tid} corrected")


class Misreading(Base):
    def test_the_oracle_keeps_the_worst_misreading_and_its_probe(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(ORACLE_STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.fm("task", "new", "Export reports", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("oracle", "T-0001", env={"PATH": bindir + os.pathsep + os.environ["PATH"]})
        self.assertRegex(c.find_brief(self.p, "T-0001").section("Oracle"),
                         r"Misreadings.*\n- exporting every report instead of the one on screen — ask which")


class Asks(Base):
    def test_unanswered_asks_from_the_last_session_show_in_next_and_expire_to_deferred(self):
        self.fm("capture", "Make the dashboard dark", "--type", "FEATURE", "--tier", "S", "--source", "self")
        self.fm("task", "set", "T-0001", "explore=true")
        b = c.find_brief(self.p, "T-0001")
        with open(b.path) as f:  # as fm second session files it: the user confirms a child's reading (T-0289)
            text = f.read().replace("explore: true", "explore: true\nconfirm: true", 1)
        with open(b.path, "w") as f:
            f.write(text)
        c.log_event(self.p, "capture", task="T-0001", data={"source": "self", "via": "second session"})
        nxt = self.fm("next").stdout
        self.assertIn("1 unanswered ask(s) from your last session wait for the user's yes", nxt)
        self.assertNotIn("T-0001", nxt)  # a child's reading is the user's to confirm, not Claude's to act on
        self.assertRegex(self.fm("state").stdout, r"T-0001 .*✋ waits for your yes")
        with open(b.path, "w") as f:
            f.write(re.sub(r"(?m)^created: .*$", f"created: {c.iso(time.time() - 8 * 86400)}", text))
        self.fm("tidy", "--apply")
        self.assertEqual(c.find_brief(self.p, "T-0001").status, "deferred")
