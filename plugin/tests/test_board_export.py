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

    def lesson(self, title, lesson, files):
        self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        tid = c.load_briefs(self.p)[-1].id
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true", "--lesson", lesson)
        b = next(x for x in c.load_briefs(self.p, include_archive=True) if x.id == tid)
        b.set_section("Files touched", "".join(f"- {f}\n" for f in files))
        c.save_brief(self.p, b)
        return tid

    def test_lessons_export_one_rule_file_per_task_scoped_to_its_files(self):
        secret = "ghp_" + "a1B2" * 9
        tid = self.lesson("Quote shell paths", f"quote every path; the token {secret} was in a log", ["src/run.sh"])
        none = self.lesson("No files", "a lesson with nothing touched", [])
        hot = [self.lesson(f"Hot {i}", f"lesson {i}", ["CHANGELOG.md", f"src/m{i}.py"]) for i in range(6)]
        self.fm("recall", "--export-rules")
        folder = os.path.join(self.repo, ".claude", "rules", "foreman-lessons")
        text = read_text(os.path.join(folder, f"{tid}.md"))
        head = text.split("---")[1]
        self.assertIn('"src/run.sh"', head)
        self.assertIn("quote every path", text)
        self.assertNotIn(secret, text)  # lessons are redacted before they land in the work tree
        self.assertFalse(os.path.exists(os.path.join(folder, f"{none}.md")))  # unscoped: never loaded every session
        hot0 = read_text(os.path.join(folder, f"{hot[0]}.md"))
        self.assertIn('"src/m0.py"', hot0)
        self.assertNotIn("CHANGELOG.md", hot0)  # a file most tasks touch scopes nothing
        self.fm("recall", "--lessons", "--retire", f"{tid}.1", "--why", "wrong")
        self.assertFalse(os.path.exists(os.path.join(folder, f"{tid}.md")))  # a retired lesson leaves the export

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
        self.fm("decide", "ship on fridays", "--why", "x", "--kind", "costly")
        self.fm("decide", "--review", "--export-adr", "docs/review")
        self.assertEqual([os.path.basename(f)[:4] for f in glob.glob(os.path.join(self.repo, "docs", "review", "*.md"))],
                         ["0003"])  # numbered as in the full list, so exports never collide
        self.assertNotEqual(self.fm("decide", "x", "--export-adr", "d", check=False).returncode, 0)

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
