"""T-0690 (Intelligence — metacognition and calibration): stated confidence scored against what happened, a competence
atlas of where work tends not to hold, and close-outs that flag rewritten criteria and suspiciously smooth runs."""
import os

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def done(self, title, *extra, files=(), conf=None):
        self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")
        tid = c.load_briefs(self.p)[-1].id
        if conf is not None:
            self.fm("task", "set", tid, f"confidence={conf}")
        if files:
            self.fm("task", "set", tid, "--section", "Files touched", "--text", "".join(f"- {f}\n" for f in files))
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true", *extra)
        return tid

    def fix_of(self, tid):
        self.fm("capture", f"Crash in what {tid} added", "--type", "FIX", "--tier", "S")


class Calibrate(Base):
    def test_stated_confidence_is_scored_against_outcomes_in_the_digest(self):
        a = self.done("One", conf=90)
        self.done("Two", conf=90)
        self.fix_of(a)
        self.assertNotEqual(self.fm("task", "set", "T-0002", "confidence=150", check=False).returncode, 0)
        out = self.fm("digest").stdout
        self.assertRegex(out, r"Calibration.*80–94%: 2 task\(s\), 1 held on the first finish \(50%\)")


class Atlas(Base):
    def test_atlas_groups_outcomes_by_file_and_focus_cautions_on_a_weak_one(self):
        ids = [self.done(f"Task {i}", files=["lib/a.py", f"lib/ok{i}.py"]) for i in range(3)]
        self.fix_of(ids[0])
        self.fix_of(ids[1])
        out = self.fm("outcomes", "--atlas").stdout
        self.assertRegex(out, r"lib/a\.py: 2 of 3 needed a later fix or revert")
        self.fm("task", "new", "Touch a again", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "s", "--scope", "lib/a.py")
        tid = c.load_briefs(self.p)[-1].id
        self.assertRegex(self.fm("focus", tid).stdout, r"Caution: lib/a\.py: 2 of 3 tasks that touched it needed")


class Honest(Base):
    def test_finish_flags_criteria_edited_after_focus_and_smooth_runs(self):
        with open(os.path.join(self.repo, "p.txt"), "w") as f:
            f.write("ok\n")
        self.fm("task", "new", "Parser", "--type", "FEATURE", "--tier", "M", "--interpretation", "x", "--approach",
                "a vs b: a", "--ac", "parses every input :: grep -q ok p.txt",
                "--step", "s", "--focus")
        self.fm("task", "ac", "T-0001", "edit", "1", "--text", "parses the common inputs")
        r = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "grep -q ok p.txt", "--lens", "intent: ok",
                    "--lens", "edge: ok", "--docs", "none: a test", "--lesson", "l", check=False)
        err = r.stdout + r.stderr
        self.assertIn("criteria edited after work started", err)
        self.assertIn("parses every input → parses the common inputs", err)
        self.assertIn("suspiciously smooth", err)
        flags = [e for e in c.ledger_tail(self.p, 200) if e.get("event") == "closeout_flags"]
        self.assertEqual(sorted(flags[-1]["data"]["kinds"]), ["criteria_edited", "smooth"])
