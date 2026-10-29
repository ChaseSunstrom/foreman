"""T-1267: Foreman's ticks follow the working files. Claude Code raises no rewind event, so a /rewind (or a revert) that
takes back a step's files shows as a tree recorded before that step's proof: the step reopens and its proof stops
counting."""
import json
import os
import unittest

from helpers import ForemanTestCase


class Rewind(ForemanTestCase):
    def write(self, name, text="x = 1\n"):
        with open(os.path.join(self.repo, name), "w") as f:
            f.write(text)

    def two_steps_done(self):
        tid = self.fm_json("task", "new", "Two steps", "--type", "FIX", "--tier", "S", "--ac", "it works :: true",
                           "--step", "one", "--step", "two")["id"]
        self.fm("focus", tid)
        for n, name in ((1, "a.py"), (2, "b.py")):
            self.write(name)
            self.fm("task", "evidence", tid, "--step", str(n), "--run", "true")
            self.fm("task", "step", tid, "done", str(n))
        return tid

    def context(self, event, **payload):
        out = self.hook(event, payload)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout)["hookSpecificOutput"]["additionalContext"] if out.stdout.strip() else ""

    def test_files_taken_back_to_before_step_one_reopen_both_steps_at_the_next_session(self):
        tid = self.two_steps_done()
        for name in ("a.py", "b.py"):  # what /rewind to before step 1 does to the files
            os.remove(os.path.join(self.repo, name))
        ctx = self.context("SessionStart", source="resume")
        self.assertIn(f"{tid} step(s) 1, 2", ctx)
        self.assertIn("/rewind", ctx)
        brief = self.fm("task", "show", tid).stdout
        self.assertIn("1. [ ] one", brief)
        self.assertIn("2. [ ] two", brief)
        self.assertEqual(brief.count("[rewound]"), 2, "both proofs kept, marked")
        self.assertIn("rewind: the working files", brief)
        self.assertIn(f"{tid} step 1/2", self.fm("next").stdout, "the proofs are queued again")
        self.assertNotIn("/rewind", self.context("SessionStart", source="resume"), "flagged once")

    def test_files_taken_back_to_between_the_steps_reopen_only_the_later_one_on_the_next_prompt(self):
        tid = self.two_steps_done()
        os.remove(os.path.join(self.repo, "b.py"))
        ctx = self.context("UserPromptSubmit", prompt="carry on")
        self.assertIn(f"{tid} step(s) 2 ", ctx)
        brief = self.fm("task", "show", tid).stdout
        self.assertIn("1. [x] one", brief)
        self.assertIn("2. [ ] two", brief)
        self.assertIn(f"{tid} step 2/2", self.fm("next").stdout)

    def test_later_work_moving_on_or_undoing_a_step_with_its_own_proof_reopens_nothing(self):
        tid = self.two_steps_done()
        self.write("c.py")  # new work after the proofs
        self.assertNotIn("/rewind", self.context("UserPromptSubmit", prompt="carry on"))
        os.remove(os.path.join(self.repo, "c.py"))
        os.remove(os.path.join(self.repo, "a.py"))  # a third step undoes step 1's file, and proves it
        self.fm("task", "step", tid, "add", "three")
        self.fm("task", "evidence", tid, "--step", "3", "--run", "true")
        self.assertNotIn("/rewind", self.context("UserPromptSubmit", prompt="carry on"))
        self.assertNotIn("[rewound]", self.fm("task", "show", tid).stdout)

    def test_fm_state_reconciles_too_and_a_typed_mark_cant_forge_one(self):
        tid = self.two_steps_done()
        os.remove(os.path.join(self.repo, "b.py"))
        out = self.fm("state").stdout
        self.assertIn(f"{tid} step(s) 2 ", out)
        self.assertIn("2. [ ] two", self.fm("task", "show", tid).stdout)
        self.fm("task", "evidence", tid, "true", "ok [rewound]", "--step", "2")
        self.assertNotIn("ok [rewound]", self.fm("task", "show", tid).stdout)

    def test_no_git_before_a_passing_proof_and_the_callers_briefs_are_used(self):
        # T-2029: every prompt ran three git commands and a second brief scan, though only a proved step can rewind
        from unittest import mock

        import fmcore as c
        tid = self.fm_json("task", "new", "Unproved", "--type", "FIX", "--tier", "S", "--ac", "it works :: true",
                           "--step", "one")["id"]
        self.fm("focus", tid)
        self.fm("task", "evidence", tid, "--step", "1", "--run", "false", check=False)  # a failed run proves nothing
        p = c.find_project(self.repo)
        with mock.patch.object(c, "worktree_tree", side_effect=AssertionError("ran git")):
            self.assertIsNone(c.reconcile_rewind(p))
        self.fm("task", "drop", tid, "test")
        tid = self.two_steps_done()
        os.remove(os.path.join(self.repo, "b.py"))
        briefs = c.load_briefs(p)
        with mock.patch.object(c, "active_brief_fast", side_effect=AssertionError("scanned the briefs again")):
            self.assertEqual(c.reconcile_rewind(p, briefs=briefs), (tid, [2]))
        self.assertIn("2. [ ] two", self.fm("task", "show", tid).stdout)


if __name__ == "__main__":
    unittest.main()
