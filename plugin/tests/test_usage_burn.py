"""T-1800: Foreman tells why usage burns, from the transcripts and the usage reading, before anyone asks."""
import datetime
import json
import os
import time
import unittest

from helpers import ForemanTestCase
from sampo import cost


def _msg(i, sid, model, ctx, ts):
    return json.dumps({"type": "assistant", "sessionId": sid, "timestamp": ts, "message": {
        "id": f"{sid}-{model}-{i}", "model": model, "usage": {"input_tokens": 10, "cache_read_input_tokens": ctx}}})


class UsageBurn(ForemanTestCase):
    def _write(self, rel, lines):
        path = os.path.join(self.tmp, "projects", rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")

    def _now(self):
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def test_each_cause_is_named_with_its_fix(self):
        ts = self._now()
        for sid in ("a", "b", "c"):  # three sessions in one hour, each replying with ~300k of context
            self._write(f"-p/{sid}.jsonl", [_msg(i, sid, "claude-sonnet-5-5", 300_000, ts) for i in range(10)])
        self._write("-p/a/subagents/agent-1.jsonl", [_msg(i, "a", "claude-opus-5-5", 900_000, ts) for i in range(10)])
        now = time.time()
        found = cost.burn_findings(os.path.join(self.tmp, "projects"),
                                     forecast={"seven_day": {"full_at": now + 3600, "resets_at": now + 4 * 3600}})
        text = "\n".join(f"{a} → {b}" for a, b in found)
        for words in ("context per reply averages 300k", "3 sessions", "Opus subagents", "run out 3 h before"):
            self.assertIn(words, text)
        self.assertEqual(len(found), 4)

    def test_a_window_the_user_set_above_foremans_is_named_not_install_user(self):  # T-2537
        from unittest import mock
        ts = self._now()
        self._write("-p/a.jsonl", [_msg(i, "a", "claude-sonnet-5-5", 300_000, ts) for i in range(30)])
        folder = os.path.join(self.tmp, "projects")
        with mock.patch.dict(os.environ, {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000"}):
            text = "\n".join(f"{a} → {b}" for a, b in cost.burn_findings(folder, forecast={}))
        self.assertIn("1.0M", text, "the user's own window, named")
        self.assertNotIn("fm install-user", text, "install-user leaves a set window alone: a no-op fix")
        self.assertIn("/compact", text)
        with mock.patch.dict(os.environ, {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": "200k"}):
            text = "\n".join(f"{a} → {b}" for a, b in cost.burn_findings(folder, forecast={}))
        self.assertNotIn("fm install-user", text, "Foreman's window is already set: the advice is /compact")

    def test_only_lines_carrying_usage_are_parsed(self):
        # T-3193: a month of transcripts is ~1.3M lines; parsing each one made fm digest take 24-33 s
        from unittest import mock
        ts = self._now()
        tool = json.dumps({"type": "user", "timestamp": ts, "message": {"content": [{"type": "tool_result", "content": "x"}]}})
        self._write("-p/a.jsonl", [_msg(i, "a", "claude-sonnet-5-5", 300_000, ts) for i in range(30)] + [tool] * 50)
        real = json.loads
        with mock.patch.object(cost.json, "loads", side_effect=real) as loads:
            found = cost.burn_findings(os.path.join(self.tmp, "projects"), forecast={})
        self.assertEqual([c for c in loads.call_args_list if "tool_result" in str(c.args[:1])], [])
        self.assertIn("context per reply averages 300k", "\n".join(a for a, _ in found))

    def test_a_lean_week_says_nothing(self):
        self._write("-p/a.jsonl", [_msg(i, "a", "claude-sonnet-5-5", 60_000, self._now()) for i in range(30)])
        self.assertEqual(cost.burn_findings(os.path.join(self.tmp, "projects"), forecast={}), [])

    def test_doctor_warns_and_session_start_reads_the_cached_scan(self):
        self.fm("init")
        cost.write_burn([("context per reply averages 300k", "sessions compact late")])
        from sampo import doctor
        self.assertEqual(doctor.check_usage_burn([("x", "y")]).status, "WARN")
        self.assertIn("/usage", doctor.check_usage_burn([("x", "y")]).detail)  # T-1797: CC 2.1.311 f applies fixes
        self.assertEqual(doctor.check_usage_burn([]).status, "PASS")
        self.assertIn("averages 300k", cost.burn_line())


if __name__ == "__main__":
    unittest.main()
