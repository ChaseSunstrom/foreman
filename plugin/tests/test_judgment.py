"""T-0688 (Intelligence — judgment, taste and decisions): doors, implicit decisions, the cheapest version, follow-ups
answered ahead, precedent, taste from overwrites, and how often decisions get reversed."""
import os
import subprocess

from helpers import ForemanTestCase, read_text

import fmcore as c

REFS = os.path.join(c.PLUGIN_ROOT, "skills", "intake", "references")
STUB = r'''#!/usr/bin/env python3
import sys
sys.stdin.read()
print("The cheapest version that meets it: a plain CSV export from the existing table, no new UI.")
'''


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)


class Doors(Base):
    def test_execution_classifies_forks_as_one_or_two_way_doors(self):
        text = read_text(os.path.join(REFS, "execute.md")).lower()
        self.assertIn("one-way door", text)
        self.assertIn("two-way door", text)


class Implicit(Base):
    def test_reviews_ask_for_the_decisions_taken_by_default(self):
        self.assertIn("implicit decisions", read_text(os.path.join(REFS, "audit.md")).lower())
        self.assertIn("implicit decisions", read_text(os.path.join(c.PLUGIN_ROOT, "agents", "fm-reviewer.md")).lower())


class Cheapest(Base):
    def test_a_child_argues_the_cheapest_version_into_the_brief(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.fm("task", "new", "Export reports", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true", "--step", "s")
        self.fm("second", "cheapest", "T-0001", env={"PATH": bindir + os.pathsep + os.environ["PATH"]})
        self.assertIn("plain CSV export", c.find_brief(self.p, "T-0001").section("Cheapest version"))


class Followups(Base):
    def test_finish_keeps_the_answers_to_likely_followups_and_the_insight(self):
        self.fm("task", "new", "Tidy", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true",
                "--followups", "Does it handle empty input? => yes, it returns an empty list",
                "--insight", "the parser was already lenient; only the caller assumed otherwise")
        b = c.find_brief(self.p, "T-0001")
        self.assertIn("empty input", b.section("Follow-up answers"))
        self.assertIn("already lenient", b.section("Insight"))
        self.assertIn("already lenient", self.fm("digest").stdout)


class Precedent(Base):
    def test_a_decision_cites_what_it_rests_on_and_the_order_is_written(self):
        self.fm("decide", "Keep exports local", "--why", "privacy", "--cites", "user 2026-10-09: everything local")
        self.assertIn("[cites: user 2026-10-09: everything local]", read_text(os.path.join(self.p.dir, "decisions.md")))
        self.assertRegex(read_text(os.path.join(REFS, "execute.md")).lower(), r"user's words.*vetoes.*decisions.*lessons")


class Overwrites(Base):
    def test_user_commits_that_rework_an_agents_file_are_listed(self):
        def commit(msg, text):
            with open(os.path.join(self.repo, "x.py"), "w") as f:
                f.write(text)
            subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
            subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)
        commit("Add x\n\nForeman-Task: T-0001", "A = 1\n")
        commit("Rename A to LIMIT, I prefer it", "LIMIT = 1\n")
        out = self.fm("taste", "--overwrites").stdout
        self.assertIn("x.py", out)
        self.assertIn("I prefer it", out)


class Reversals(Base):
    def test_the_digest_reports_reversals_per_kind(self):
        self.fm("decide", "Use sqlite for the cache", "--kind", "costly")
        self.fm("decide", "Name it cache.db")
        self.fm("decide", "Use a JSON file for the cache", "--kind", "costly", "--reverses", "sqlite for the cache")
        out = self.fm("digest").stdout
        self.assertRegex(out, r"costly: 1 of 2 reversed")
