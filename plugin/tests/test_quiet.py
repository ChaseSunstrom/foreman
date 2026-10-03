"""T-0077: FOREMAN_QUIET=1 marks a session another tool drives (an orchestrator): Foreman adds no context, nudges or
brief requirement there, and the guard still blocks what it always blocks."""
import os
import unittest

from helpers import ForemanTestCase

QUIET = {"FOREMAN_QUIET": "1"}


class Quiet(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def test_no_context_nudges_or_brief_requirement(self):
        for event, payload in (("SessionStart", {"source": "startup"}), ("UserPromptSubmit", {"prompt": "fix the bug"}),
                               ("Stop", {})):
            p = self.hook(event, payload, env=QUIET)
            self.assertEqual((p.returncode, p.stdout.strip()), (0, ""), event)
        edit = {"tool_name": "Write", "tool_input": {"file_path": os.path.join(self.repo, "app.py"), "content": "x"}}
        self.assertEqual(self.hook("PreToolUse", edit, env=QUIET).returncode, 0)
        self.assertEqual(self.hook("PreToolUse", edit).returncode, 2, "without it the brief requirement holds")

    def test_the_guard_still_blocks(self):
        p = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "rm -rf ~"}}, env=QUIET)
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
