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

    def test_its_review_every_claude_launcher_waits_and_only_the_user_lifts_it(self):
        # T-0591 (T-0436 review): fm session start, fm ideas, fm research ask, fm bench and fm relate still launched
        # claude children while paused; and Claude could run fm pause off itself
        from unittest import mock
        import fmrelate
        pack = os.path.join(self.tmp, "pack.md")
        with open(pack, "w") as f:
            f.write("a pack\n")
        self.fm("pause")
        for args in (["session", "start", "do x"], ["ideas", "--pack", pack], ["research", "ask", "what is x?"],
                     ["bench", "run"], ["relate"], ["oracle", "will it work?"]):
            r = self.fm(*args, check=False, env=self.env())
            self.assertNotEqual(r.returncode, 0, args)
            self.assertIn("fm pause off", r.stderr, args)
        self.assertEqual(self.called(), "")
        with mock.patch.dict(os.environ, {"FOREMAN_NO_BACKGROUND": ""}), mock.patch("subprocess.Popen") as popen:
            fmrelate.spawn(c.find_project(self.repo))  # the SessionStart path: skipped, never raised
        popen.assert_not_called()
        out = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "fm pause off"}}).stdout
        self.assertIn('"deny"', out)
        self.assertTrue(c.panicked())

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
