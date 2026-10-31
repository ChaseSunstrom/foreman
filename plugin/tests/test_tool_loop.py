"""T-2369 (Mission 6, #5): a capability miss during an active task is that task's to find-build-test-use, and
fm task finish refuses the task while the miss is unresolved. Resolved only by run evidence, never by a typed line."""
import json
import os
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c


class MissLoop(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Use gizmo", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.p = c.find_project(self.repo)
        self.tid = c.load_briefs(self.p)[-1].id

    def miss(self, cmd="true gizmo", err="bash: gizmo: command not found", sid="s1"):
        self.hook("PostToolUseFailure", {"tool_name": "Bash", "tool_input": {"command": cmd}, "error": err,
                                         "session_id": sid})
        time.sleep(1.05)  # timestamps are whole seconds and a run counts only when strictly later than the miss

    def passed(self, cmd, sid="s1"):
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}, "session_id": sid,
                                  "tool_response": {"stdout": "ok", "stderr": "", "interrupted": False}})

    def finish(self):
        return self.fm("task", "finish", self.tid, "--audit", "self", "--run", "true", check=False)

    def refused(self, why=""):
        r = self.finish()
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("capability miss", r.stderr + r.stdout, why)
        self.assertEqual(c.find_brief(self.p, self.tid).status, "active")

    def closes(self):
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def test_a_miss_is_logged_with_the_task_and_the_command_and_fm_next_names_it(self):
        self.miss("FOO=1 true gizmo --x")
        (e,) = [e for e in c.ledger_events(self.p, ["capability_miss"])]
        self.assertEqual((e["task"], e["data"]["name"], e["data"]["kind"]), (self.tid, "gizmo", "command"))
        self.assertIn("true gizmo --x", e["data"]["cmd"])
        nxt = self.fm("next").stdout
        self.assertIn("open miss `gizmo`", nxt)
        self.assertIn("fm which", nxt)

    def test_a_task_with_no_miss_pays_nothing_and_finishes(self):
        self.assertNotIn("open miss", self.fm("next").stdout)
        self.closes()

    def test_finish_refuses_on_every_try_and_a_later_green_run_of_the_same_command_closes_it(self):
        self.miss()
        for _ in range(3):
            self.refused()
        self.hook("PostToolUseFailure", {"tool_name": "Bash", "tool_input": {"command": "true gizmo"},
                                         "error": "Exit code 1\nboom"})
        self.refused("a red run resolves nothing")
        self.passed("cd sub && true  gizmo")  # where it ran and spacing are not what it was
        self.closes()

    def test_a_run_before_the_miss_does_not_count_and_a_second_miss_reopens_it(self):
        self.passed("true gizmo")
        self.miss()
        self.refused()
        self.passed("true gizmo")
        self.miss()
        self.refused("the newest miss is the open one")

    def test_an_fm_run_closes_it_but_a_red_as_expected_or_typed_run_does_not(self):
        self.miss("false gizmo")
        self.fm("task", "evidence", self.tid, "--step", "1", "--expect-fail", "--run", "false gizmo")
        self.refused("an expect-fail run")
        self.fm("task", "evidence", self.tid, "--step", "1", "false gizmo", "exit 0 · 3 passed [ran]")
        self.refused("a typed line, whatever it says")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true gizmo", check=False)
        self.refused("another command")
        self.miss("true gizmo")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true gizmo")
        self.refused("the false one is still open")
        self.miss("false gizmo")
        self.passed("false gizmo")
        self.closes()

    def test_the_command_fmfixes_pairs_with_the_failure_closes_it(self):
        self.miss("gizmo --x")
        self.refused()
        self.passed("python3 tools/gizmo.py --x")
        (e,) = c.ledger_events(self.p, ["fix_paired"])
        self.assertEqual(e["task"], self.tid)
        self.closes()

    def test_a_tool_proved_event_naming_it_closes_it_but_another_name_does_not(self):
        self.miss()
        c.log_event(self.p, "tool_proved", task=self.tid, data={"name": "other"})
        self.refused()
        c.log_event(self.p, "tool_proved", task=self.tid, data={"name": "gizmo"})
        self.closes()

    def test_a_queued_grant_closes_it_only_with_a_green_run_of_the_fallback_step(self):
        self.miss()
        c.log_event(self.p, "grant_queued", task=self.tid, data={"name": "gizmo", "step": 1})
        self.refused("the grant alone")
        time.sleep(1.05)
        self.fm("task", "evidence", self.tid, "--step", "1", "--expect-fail", "--run", "false")
        self.refused("a red fallback run")
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true")
        self.closes()

    def test_a_missing_module_the_task_then_writes_is_not_a_miss_but_a_missing_command_is(self):
        self.miss("python3 app.py", "ModuleNotFoundError: No module named 'gizmolib'")
        self.refused("not written yet")
        with open(os.path.join(self.repo, "gizmolib.py"), "w") as f:
            f.write("X = 1\n")
        self.assertNotIn("open miss", self.fm("next").stdout)
        self.closes()

    def test_a_command_not_found_is_not_cleared_by_a_file_of_that_name(self):
        self.miss()
        with open(os.path.join(self.repo, "gizmo.py"), "w") as f:
            f.write("X = 1\n")
        self.refused()

    def test_a_miss_logged_on_another_task_or_none_does_not_block_this_one(self):
        c.log_event(self.p, "capability_miss", task="T-9999", data={"name": "gizmo", "cmd": "gizmo", "kind": "command"})
        c.log_event(self.p, "capability_miss", task=None, data={"name": "gizmo", "cmd": "gizmo", "kind": "command"})
        self.closes()

    def test_done_refuses_too_so_it_is_not_a_way_round(self):
        self.miss()
        self.fm("task", "evidence", self.tid, "--step", "1", "--run", "true")
        r = self.fm("task", "done", self.tid, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("capability miss", r.stderr + r.stdout)

    def test_block_is_the_way_out_without_closing(self):
        self.miss()
        self.fm("task", "block", self.tid, "gizmo cannot be installed here")
        self.assertEqual(c.find_brief(self.p, self.tid).status, "blocked")


if __name__ == "__main__":
    unittest.main()
