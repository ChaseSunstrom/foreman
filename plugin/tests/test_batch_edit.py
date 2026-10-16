"""T-1089: change many files in one call. fm edit applies a batch of exact replacements atomically (each old text unique
unless --all, every file inside the active task's scope); fm sub runs a regex codemod with a preview; fm lane max sets
how many builders may be out at once."""
import json
import os
import unittest

from helpers import ForemanTestCase


class _Files(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        for name, text in (("a.py", "x = 1\ny = 2\n"), ("b.py", "x = 1\nx = 1\n"), ("c.py", "z = 3\n")):
            with open(os.path.join(self.repo, name), "w") as f:
                f.write(text)
        tid = self.fm_json("task", "new", "Rename", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                           "--scope", "a.py", "--scope", "b.py")["id"]
        self.fm("focus", tid)

    def read(self, name):
        with open(os.path.join(self.repo, name)) as f:
            return f.read()

    def edit(self, spec, *args, check=True):
        return self.fm("edit", *args, input=json.dumps(spec), check=check)


class BatchEdit(_Files):
    def test_a_batch_applies_every_replacement(self):
        out = self.edit([{"file": "a.py", "old": "x = 1", "new": "x = 10"}, {"file": "a.py", "old": "y = 2", "new": "y = 20"},
                         {"file": "b.py", "old": "x = 1", "new": "x = 5", "all": True}]).stdout
        self.assertEqual(self.read("a.py"), "x = 10\ny = 20\n")
        self.assertEqual(self.read("b.py"), "x = 5\nx = 5\n")
        self.assertIn("a.py", out)
        self.assertIn("2 replacements", out)

    def test_all_or_nothing(self):
        p = self.edit([{"file": "a.py", "old": "x = 1", "new": "x = 10"}, {"file": "a.py", "old": "nope", "new": "q"}], check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("not found", p.stdout + p.stderr)
        self.assertEqual(self.read("a.py"), "x = 1\ny = 2\n", "nothing written when one entry fails")

    def test_an_ambiguous_old_text_is_refused_without_all(self):
        p = self.edit([{"file": "b.py", "old": "x = 1", "new": "x = 5"}], check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("2 times", p.stdout + p.stderr)

    def test_dry_run_writes_nothing(self):
        out = self.edit([{"file": "a.py", "old": "x = 1", "new": "x = 10"}], "--dry-run").stdout
        self.assertIn("a.py", out)
        self.assertEqual(self.read("a.py"), "x = 1\ny = 2\n")

    def test_a_file_outside_the_task_scope_is_refused(self):
        p = self.edit([{"file": "c.py", "old": "z = 3", "new": "z = 4"}], check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("scope", p.stdout + p.stderr)
        self.assertEqual(self.read("c.py"), "z = 3\n")

    def test_the_guard_decides_as_it_would_for_an_edit(self):
        # a settings file in scope is still the guard's: Claude Code's settings never change behind its back
        os.makedirs(os.path.join(self.repo, ".claude"))
        with open(os.path.join(self.repo, ".claude", "settings.json"), "w") as f:
            f.write('{"a": 1}\n')
        tid = self.fm_json("task", "new", "Settings", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                           "--scope", ".claude")["id"]
        self.fm("focus", tid)
        p = self.edit([{"file": ".claude/settings.json", "old": '"a": 1', "new": '"a": 2'}], check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("settings.json", p.stdout + p.stderr)
        with open(os.path.join(self.repo, ".claude", "settings.json")) as f:
            self.assertEqual(f.read(), '{"a": 1}\n')

    def test_a_path_outside_the_project_is_refused(self):
        p = self.edit([{"file": "../outside.py", "old": "a", "new": "b"}], check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("outside the project", p.stdout + p.stderr)

    def test_review_crlf_is_kept(self):
        with open(os.path.join(self.repo, "a.py"), "w", newline="") as f:
            f.write("x = 1\r\ny = 2\r\n")
        self.edit([{"file": "a.py", "old": "x = 1", "new": "x = 9"}])
        with open(os.path.join(self.repo, "a.py"), newline="") as f:
            self.assertEqual(f.read(), "x = 9\r\ny = 2\r\n")

    def test_review_glob_scope_matches(self):
        os.makedirs(os.path.join(self.repo, "lib"))
        with open(os.path.join(self.repo, "lib", "m.py"), "w") as f:
            f.write("q = 1\n")
        tid = self.fm_json("task", "new", "Glob", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                           "--scope", "lib/*.py")["id"]
        self.fm("focus", tid)
        self.edit([{"file": "lib/m.py", "old": "q = 1", "new": "q = 2"}])
        self.assertEqual(self.read("lib/m.py"), "q = 2\n")

    def test_review_a_malformed_block_refuses_the_batch(self):
        spec = "@@ a.py\n<<<\nx = 1\n===\nx = 7\n>>>\n@@ b.py\n<<<\nx = 1\n===\nx = 3\n"  # the second never closes
        p = self.fm("edit", input=spec, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("block", p.stdout + p.stderr)
        self.assertEqual(self.read("a.py"), "x = 1\ny = 2\n")

    def test_review_a_path_rule_blocks_as_for_an_edit(self):
        self.fm("rule", "add", "b\\.py$", "--on", "path", "--why", "frozen")
        p = self.edit([{"file": "b.py", "old": "x = 1", "new": "x = 5", "all": True}], check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("frozen", p.stdout + p.stderr)

    def test_review_a_failed_write_leaves_every_file_as_it_was(self):
        os.makedirs(os.path.join(self.repo, "ro"))
        with open(os.path.join(self.repo, "ro", "c.py"), "w") as f:
            f.write("k = 1\n")
        tid = self.fm_json("task", "new", "Ro", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                           "--scope", "a.py", "--scope", "ro")["id"]
        self.fm("focus", tid)
        os.chmod(os.path.join(self.repo, "ro"), 0o555)
        try:
            if os.access(os.path.join(self.repo, "ro"), os.W_OK):
                self.skipTest("running as root: a read-only folder is still writable")
            p = self.edit([{"file": "a.py", "old": "x = 1", "new": "x = 10"}, {"file": "ro/c.py", "old": "k = 1", "new": "k = 2"}],
                          check=False)
            self.assertNotEqual(p.returncode, 0)
            self.assertEqual(self.read("a.py"), "x = 1\ny = 2\n", "nothing written when one file can't be")
        finally:
            os.chmod(os.path.join(self.repo, "ro"), 0o755)

    def test_a_spec_file_for_builders(self):
        spec = os.path.join(self.tmp, "batch.json")
        with open(spec, "w") as f:
            json.dump([{"file": "a.py", "old": "y = 2", "new": "y = 3"}], f)
        self.fm("edit", "--file", spec)
        self.assertEqual(self.read("a.py"), "x = 1\ny = 3\n")

    def test_block_format(self):
        spec = "@@ a.py\n<<<\nx = 1\n===\nx = 7\n>>>\n"
        self.fm("edit", input=spec)
        self.assertEqual(self.read("a.py"), "x = 7\ny = 2\n")

    def test_no_active_task_refuses(self):
        self.fm("checkpoint", "--note", "pause")
        st = self.fm_json("state")
        if st.get("active"):
            self.fm("task", "drop", st["active"]["id"], "test")
        p = self.edit([{"file": "a.py", "old": "x = 1", "new": "x = 9"}], check=False)
        self.assertNotEqual(p.returncode, 0)


class Sub(_Files):
    def test_preview_counts_then_apply(self):
        out = self.fm("sub", r"x = (\d)", r"x = \g<1>0", "--glob", "*.py").stdout
        self.assertIn("a.py: 1", out)
        self.assertIn("b.py: 2", out)
        self.assertEqual(self.read("a.py"), "x = 1\ny = 2\n", "preview writes nothing")
        self.fm("sub", r"x = (\d)", r"x = \g<1>0", "--glob", "*.py", "--apply")
        self.assertEqual(self.read("b.py"), "x = 10\nx = 10\n")

    def test_review_sub_stays_inside_the_project(self):
        out = self.fm("sub", "x", "y", "--glob", "../**/*.py", check=False)
        self.assertNotIn("..", out.stdout)

    def test_review_a_bad_replacement_is_a_usage_error(self):
        p = self.fm("sub", "x", r"\9", "--glob", "*.py", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertNotIn("Traceback", p.stderr)

    def test_max_caps_the_files(self):
        p = self.fm("sub", "x", "y", "--glob", "*.py", "--apply", "--max", "1", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--max", p.stdout + p.stderr)


class LaneMax(ForemanTestCase):
    def test_the_builder_cap_is_a_setting(self):
        self.fm("init")
        self.assertIn("2", self.fm("lane", "max").stdout)
        self.fm("lane", "max", "4")
        self.assertIn("4", self.fm("lane", "max").stdout)
        self.assertNotEqual(self.fm("lane", "max", "50", check=False).returncode, 0)
        p = self.fm("lane", "max", "²", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertNotIn("Traceback", p.stderr)


class Hint(ForemanTestCase):
    def test_the_third_edit_of_one_file_points_at_fm_edit_once(self):
        self.fm("init")
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a", "--focus")
        path = os.path.join(self.repo, "a.py")
        notes = [self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path}}).stdout for _ in range(5)]
        self.assertEqual(sum("fm edit" in n for n in notes), 1, notes)
        self.assertIn("fm edit", notes[2])

    def test_a_subagents_edits_get_no_batch_hint(self):
        # T-1104: a builder's edits raised the hint in the main thread's context
        self.fm("init")
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a", "--focus")
        path = os.path.join(self.repo, "b.py")
        notes = [self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path}, "agent_id": "a1"}).stdout
                 for _ in range(7)]
        self.assertFalse(any("fm edit" in n for n in notes), notes)
        self.assertFalse(any("without a check" in n for n in notes), notes)  # T-1110: nor the thrash note

    def test_a_subagents_failed_run_gives_this_thread_no_note(self):
        # T-1110: a builder's red run put "Suspects: …" and its failure (against this thread's task) into this context
        self.fm("init")
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "s", "--ac", "a", "--focus")
        err = "Traceback (most recent call last):\n  File \"x.py\", line 3\nKeyError: 'col'\nFAIL: test_x"
        pl = {"tool_name": "Bash", "tool_input": {"command": "python3 x.py"}, "error": err}
        with open(os.path.join(self.repo, "x.py"), "w") as f:  # changed and on the stack: a suspect
            f.write("a = 1\nb = 2\nc = {}['col']\n")
        self.assertEqual(self.hook("PostToolUseFailure", dict(pl, agent_id="a1")).stdout.strip(), "")
        self.assertIn("Suspects", self.hook("PostToolUseFailure", pl).stdout)  # this thread's own failure still notes


if __name__ == "__main__":
    unittest.main()
