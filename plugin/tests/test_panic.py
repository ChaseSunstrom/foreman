"""T-0436: fm pause, one flag that stops everything Foreman runs unattended; fm pause off lifts it."""
import json
import os
import sys

from helpers import FM
from test_serve import ServeCase

import fmcore as c
import fmhooks


class Panic(ServeCase):
    def setUp(self):
        super().setUp()
        self.fm("autonomy", "full")
        for title in ("one", "two"):
            self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s")

    def drive(self):
        out = self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Continuing.",
                                 "session_id": "s1"}).stdout.strip()
        return json.loads(out).get("decision") if out.startswith("{") else None

    def claude_runs(self):
        return sum(line.startswith("claude ") for line in self.called().splitlines())

    def test_panic_blocks_unattended(self):
        self.assertEqual(self.drive(), "block")
        self.fm("pause")
        self.assertTrue(c.panicked())
        self.assertIsNone(self.drive())
        self.assertEqual(c.state_dict(c.find_project(self.repo))["autonomy"], "standard")  # tightened, not rewritten
        self.assertEqual(self.meta()["autonomy"], "full")
        self.assertFalse(fmhooks.second_due({"source": "startup"}, {}, False))
        self.assertIn("PAUSED", self.fm("status").stdout)
        for args in (["run"], ["serve"], ["night"], ["lane", "new", "T-0001"]):
            r = self.fm(*args, check=False, env=self.env())
            self.assertNotEqual(r.returncode, 0, args)
            self.assertIn("fm pause off", r.stderr, args)
        self.assertEqual(self.called(), "")  # no claude, no systemctl
        self.assertFalse(os.path.exists(self.unit))
        self.serve("stop")  # stopping still works: pause only tightens

    def test_panic_blocks_unattended_in_a_running_loop(self):
        fm = f"{sys.executable} {FM}"  # the user pauses while the first session runs
        self.stub("claude", f'{fm} pause\n{fm} task block $FOREMAN_DRIVE_TASK "needs a key"\n')
        r = self.fm("run", check=False, env=self.env())
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.claude_runs(), 1, "the second task never starts")
        self.assertIn("fm pause off", r.stderr)

    def test_panic_resume(self):
        self.fm("pause")
        self.fm("pause", "off")
        self.assertFalse(c.panicked())
        self.assertEqual(self.drive(), "block")
        self.assertEqual(c.state_dict(c.find_project(self.repo))["autonomy"], "full")
        self.assertTrue(fmhooks.second_due({"source": "startup"}, {}, False))
        self.assertNotIn("PAUSED", self.fm("status").stdout)
        self.fm("night", "--dry-run")
        self.fm("pause", "off")  # already off: nothing to do, no error
