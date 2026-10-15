"""Knowledge out (T-0958): lessons as a Claude Code rule file scoped to their files, decisions as ADRs, and a deferral
that comes back in fm next when a file changes."""
import glob
import os

from helpers import ForemanTestCase, read_text

import fmcore as c


class BoardExport(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def test_lessons_export_as_a_rule_file_scoped_to_their_files(self):
        self.fm("task", "new", "Quote shell paths", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "s", "--focus")
        tid = c.load_briefs(self.p)[-1].id
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true", "--lesson", "quote every path")
        b = c.load_briefs(self.p, include_archive=True)[-1]
        b.set_section("Files touched", "- src/run.sh\n")
        c.save_brief(self.p, b)
        self.fm("recall", "--export-rules")
        text = read_text(os.path.join(self.repo, ".claude", "rules", "foreman-lessons.md"))
        head = text.split("---")[1]
        self.assertIn("paths:", head)
        self.assertIn('"src/run.sh"', head)
        self.assertIn("quote every path", text)
        self.assertIn(tid, text)

    def test_decisions_export_as_one_adr_per_decision(self):
        self.fm("decide", "use sqlite", "--why", "one file, no server", "--rejected", "postgres")
        self.fm("decide", "keep the 60s TTL", "--why", "rate limits")
        self.fm("decide", "--export-adr", "docs/adr")
        files = sorted(glob.glob(os.path.join(self.repo, "docs", "adr", "*.md")))
        self.assertEqual(len(files), 2, files)
        first = read_text(files[0])
        self.assertIn("use sqlite", first)
        self.assertIn("## Decision", first)
        self.assertIn("one file, no server", first)
        self.assertIn("postgres", first)

    def test_a_deferral_wakes_when_its_file_changes_and_not_before(self):
        with open(os.path.join(self.repo, "auth.py"), "w") as f:
            f.write("TTL = 60\n")
        self.fm("task", "new", "Rework token refresh", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "s")
        tid = c.load_briefs(self.p)[-1].id
        self.fm("task", "defer", tid, "waits on the auth rewrite", "--until", "when auth.py changes")
        self.assertNotIn("is due back", self.fm("next").stdout)
        with open(os.path.join(self.repo, "auth.py"), "w") as f:
            f.write("TTL = 300\n")
        out = self.fm("next").stdout
        self.assertIn(f"deferred {tid} is due back", out)
        self.assertIn("auth.py", out)

    def test_a_deferral_trigger_outside_the_project_is_refused(self):
        self.fm("task", "new", "x", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        tid = c.load_briefs(self.p)[-1].id
        r = self.fm("task", "defer", tid, "--until", "when ../../etc/passwd changes", check=False)
        self.assertNotEqual(r.returncode, 0)
