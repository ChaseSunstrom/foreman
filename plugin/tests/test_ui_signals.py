"""T-0681: UI and motion — the view model carries a close-out card's facts and the health signals the band shows,
and a guard refusal of a long command quotes the part that matched."""
import json

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def ui(self):
        return json.loads(self.fm("ui", "--json").stdout)


class CloseOut(Base):
    def test_a_closed_task_carries_its_title_grade_and_lenses(self):
        self.fm("task", "new", "Tidy the parser", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check")
        card = self.ui()["closed"][0]
        self.assertEqual((card["id"], card["title"]), ("T-0001", "Tidy the parser"))
        self.assertTrue(card["grade"])
        self.assertIn("self", card["lenses"])


class Signals(Base):
    def test_signals_name_a_failing_gate_and_blocked_tasks(self):
        self.assertEqual(self.ui()["signals"], [], "a calm project shows nothing")
        self.fm("task", "new", "Stuck", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.fm("task", "block", "T-0001", "needs a key")
        c.log_event(self.p, "check_run", data={"results": [{"cmd": "pytest -q", "exit": 1, "s": 3.0}]})
        sig = self.ui()["signals"]
        self.assertIn("red", [x["level"] for x in sig])
        self.assertTrue(any("pytest -q" in x["text"] for x in sig))
        self.assertTrue(any("1 blocked" in x["text"] for x in sig))


class BlockSegment(Base):
    def test_a_long_commands_refusal_quotes_the_part_that_matched(self):
        cmd = "echo " + "padding " * 40 + "&& rm -rf ~/Documents && echo done"
        out = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout
        reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("rm -rf ~/Documents", reason.split("\n")[-1] if "\n" in reason else reason)
        self.assertIn("in: ", reason)
