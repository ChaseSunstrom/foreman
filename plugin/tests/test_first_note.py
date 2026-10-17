"""T-0969: test-first at edit time. The first Edit/Write of a non-test source file in a FIX/FEATURE task that has
changed no test file and recorded no failing run gets one note to write and run the failing test first; once per task,
zero tokens, never a block."""
import os

from test_hooks import HookCase

HEAD = "Foreman: test first"


class TestFirstNote(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def edit(self, rel, tool="Edit"):
        ti = {"file_path": os.path.join(self.repo, rel), "old_string": "x", "new_string": "y"} if tool == "Edit" \
            else {"file_path": os.path.join(self.repo, rel), "content": "y\n"}
        proc = self.hook("PreToolUse", {"tool_name": tool, "tool_input": ti})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn('"deny"', proc.stdout)
        ctx = self.ctx_of(proc)
        return ctx[ctx.index(HEAD):] if HEAD in ctx else ""

    def write(self, rel):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("def test_x():\n    assert False\n")

    def test_the_first_source_edit_of_a_fix_task_gets_one_note(self):
        tid = self.task()
        self.assertEqual(self.edit("README.md"), "", "docs get none")
        self.assertEqual(self.edit("config.json", tool="Write"), "", "config gets none")
        self.assertEqual(self.edit("tests/test_app.py"), "", "a test-file edit gets none")
        note = self.edit("app.py")
        self.assertIn("failing test", note)
        self.assertIn(f"fm task evidence {tid}", note)
        self.assertLessEqual(len(note), 300)
        self.assertEqual(self.edit("other.py"), "", "a second edit in the same task gets none")
        self.assertEqual(self.edit("app.py", tool="Write"), "")

    def test_an_unattended_feature_task_is_told_to_run_the_test_not_record_it(self):
        # T-1231: in the long duel every request's note became an fm task evidence call (up to 12 a session); a
        # FEATURE needs no recorded red run, a FIX still does (its red-to-green proof)
        headless = {"CLAUDE_CODE_ENTRYPOINT": "sdk-cli", "FOREMAN_BENCH": "1"}
        for type_, recorded in (("FEATURE", False), ("FIX", True)):
            tid = self.task(title=type_, type_=type_)
            proc = self.hook("PreToolUse", {"tool_name": "Edit", "tool_input": {
                "file_path": os.path.join(self.repo, f"{type_.lower()}.py"), "old_string": "x", "new_string": "y"}},
                env=headless)
            note = self.ctx_of(proc)
            self.assertIn("failing test", note, type_)
            self.assertEqual(f"fm task evidence {tid}" in note, recorded, type_)

    def test_a_feature_task_gets_it_and_a_new_task_gets_it_again(self):
        self.task(type_="FEATURE")
        self.assertIn("failing test", self.edit("lib/core.ts"))
        self.task(title="Second", type_="FIX")
        self.assertIn("failing test", self.edit("lib/core.ts"))

    def test_clean_and_research_tasks_get_none(self):
        for type_ in ("CLEAN", "RESEARCH", "PERF"):
            self.task(title=type_, type_=type_)
            self.assertEqual(self.edit("app.py"), "", type_)

    def test_a_failing_run_on_record_means_none(self):
        tid = self.task()
        self.fm("task", "evidence", tid, "--step", "1", "--run", "false", check=False)
        self.assertEqual(self.edit("app.py"), "")

    def test_a_changed_test_file_means_none(self):
        self.task()
        self.write("tests/test_app.py")
        self.assertEqual(self.edit("app.py"), "")
