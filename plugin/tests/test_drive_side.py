"""T-1176: the drive's side-task offer never hands a builder lane work a builder can't do (a brainstorm, a release),
and a task whose gates run in the background (meta gates_running with a live pid) is in progress, not a side task."""
import os
import subprocess

from test_hooks import HookCase

import fmcore as c


class DriveSide(HookCase):
    def stop(self, msg):
        return self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": msg, "session_id": "sess-1"})

    def reasons(self, n=3):
        self.hook("SubagentStart", {"agent_id": "a1", "agent_type": "foreman:fm-reviewer"})
        return [self.stop("Waiting for the review.").stdout for _ in range(n)]

    def offered(self, n=3):
        return " ".join(self.reasons(n))

    def test_research_and_release_get_no_lane(self):
        self.fm("init")
        research = self.task("Brainstorm ideas", type_="RESEARCH", focus=False)
        release = self.task("Release v2.0", focus=False)
        self.task("Current work")
        text = self.offered()
        self.assertIn(research, text)
        self.assertIn(release, text)
        self.assertNotIn("fm lane brief", text)

    def test_live_gate_run_is_not_offered_but_a_dead_one_is(self):
        self.fm("init")
        busy = self.task("Gates running", focus=False)
        self.task("Current work")
        p = self.project()
        c.update_meta(p, gates_running={"task": busy, "pid": os.getpid(), "at": c.now()})
        self.assertNotIn(f"Start {busy}", self.offered())
        done = subprocess.Popen(["true"])
        done.wait()
        c.update_meta(p, gates_running={"task": busy, "pid": done.pid, "at": c.now()})
        self.assertIn(f"Start {busy}", self.offered())
