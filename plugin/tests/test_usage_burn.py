"""T-1800: Foreman tells why usage burns, from the transcripts and the usage reading, before anyone asks."""
import datetime
import json
import os
import time
import unittest

from helpers import ForemanTestCase
import fmcost


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
        found = fmcost.burn_findings(os.path.join(self.tmp, "projects"),
                                     forecast={"seven_day": {"full_at": now + 3600, "resets_at": now + 4 * 3600}})
        text = "\n".join(f"{a} → {b}" for a, b in found)
        for words in ("context per reply averages 300k", "3 sessions", "Opus subagents", "run out 3 h before"):
            self.assertIn(words, text)
        self.assertEqual(len(found), 4)

    def test_a_lean_week_says_nothing(self):
        self._write("-p/a.jsonl", [_msg(i, "a", "claude-sonnet-5-5", 60_000, self._now()) for i in range(30)])
        self.assertEqual(fmcost.burn_findings(os.path.join(self.tmp, "projects"), forecast={}), [])

    def test_doctor_warns_and_session_start_reads_the_cached_scan(self):
        self.fm("init")
        fmcost.write_burn([("context per reply averages 300k", "sessions compact late")])
        import fmdoctor
        self.assertEqual(fmdoctor.check_usage_burn([("x", "y")]).status, "WARN")
        self.assertEqual(fmdoctor.check_usage_burn([]).status, "PASS")
        self.assertIn("averages 300k", fmcost.burn_line())


if __name__ == "__main__":
    unittest.main()
