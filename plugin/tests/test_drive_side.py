"""T-1176: the drive's side-task offer never hands a builder lane work a builder can't do (a brainstorm, a release),
and a task whose gates run in the background (meta gates_running with a live pid) is in progress, not a side task."""
import os
import subprocess

from test_hooks import HookCase

import fmcore as c


class LaneHeld(HookCase):
    """T-1469: with every queued task held by a builder lane, the drive said 'fm focus T-x' each Stop, which fm focus
    refuses ('held by lane'); a lane's task is running work, said once."""

    def stop(self):
        return self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Waiting on the builders.",
                                  "session_id": "sess-1"}).stdout

    def test_a_task_a_lane_holds_is_not_offered_to_focus(self):
        self.fm("init")
        self.fm("autonomy", "full")
        tid = self.task("Lane work", focus=False)
        import fmcli
        fmcli.mutate(self.project(), tid, lambda x: x.meta.__setitem__("builder", c.now()), "lane_builder", {})
        first = self.stop()
        self.assertNotIn(f"fm focus {tid}", first)
        self.assertIn(tid, first)
        self.assertNotIn(tid, self.stop(), "said once, not on every Stop")

    def test_fm_next_skips_a_task_a_lane_holds(self):
        # T-1478: the Stop note's trailing "Next: T-x: fm focus T-x" (fm next) still named a lane's task
        self.fm("init")
        held = self.task("Lane work", focus=False)
        free = self.task("Free work", focus=False)
        import fmcli
        fmcli.mutate(self.project(), held, lambda x: x.meta.__setitem__("builder", c.now()), "lane_builder", {})
        out = self.fm("next").stdout
        self.assertNotIn(f"fm focus {held}", out)
        self.assertIn(free, out)


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
