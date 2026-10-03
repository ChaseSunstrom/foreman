"""T-0086: a file a Bash command changed (sed -i, a generator) counts as the active task's touch like an Edit's, and one
outside the task's scope gets the same live note; a file changed before the call isn't counted."""
import json
import os
import time
import unittest

from helpers import ForemanTestCase


class BashTouches(ForemanTestCase):
    def test_files_a_command_changed_are_the_tasks_touches(self):
        import fmcore as c
        self.fm("init")
        self.fm("task", "new", "A", "--type", "FEATURE", "--tier", "S", "--scope", "a.py", "--ac", "ok :: true",
                "--step", "s", "--focus")
        for rel in ("a.py", "b.py", "old.py"):
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write("x = 1\n")
        past = time.time() - 600
        os.utime(os.path.join(self.repo, "old.py"), (past, past))  # changed before the call
        p = self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": "sed -i s/0/1/ a.py b.py"},
                                      "tool_response": {"stdout": "", "stderr": ""}, "duration_ms": 300})
        note = json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("changed b.py, outside T-0001 scope", note)  # only b.py: a.py is in scope, old.py is older
        touched = c.task_touches(c.find_project(self.repo), "T-0001")
        self.assertEqual(sorted(touched), ["a.py", "b.py"])
        again = self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": "true"}, "duration_ms": 10})
        self.assertNotIn("b.py", again.stdout, "one note per file")


if __name__ == "__main__":
    unittest.main()
