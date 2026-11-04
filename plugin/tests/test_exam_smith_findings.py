"""T-2931: the smith arm asks the local profile once for findings from fm code's end text. Fakes only; the end text is
gemma4:12b's real vuln-js answer, the untested-rust file and symbol are the real ones."""
import json
import os
import tempfile
import unittest
from unittest import mock

from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)

from sampo import louhi, models, smithbench

END = "SQL Injection: File app.js, Line 23, the find_user_sql function concatenates name"
FAKE_FM = "import json,sys\nfor e in json.loads(%r): print(json.dumps(e))\n"


class SmithFindings(unittest.TestCase):
    def arm(self, events, reply, files=("app.js",)):
        calls = []
        def complete(profile, messages, **kw):
            calls.append(messages)
            return {"text": reply, "tool_calls": [], "usage": {"in": 1, "out": 1}}
        with tempfile.TemporaryDirectory() as tmp:
            base, work = os.path.join(tmp, "base"), os.path.join(tmp, "work")
            os.makedirs(os.path.join(base, "repo"))
            for f in files:
                with open(os.path.join(base, "repo", f), "w") as h:
                    h.write("x = 1\n")
            fm = os.path.join(tmp, "fm.py")
            with open(fm, "w") as h:
                h.write(FAKE_FM % json.dumps(events))
            log = os.path.join(tmp, "e.jsonl")
            with mock.patch.object(smithbench, "FM", fm), mock.patch.object(models, "resolve", lambda m: {"name": m}), \
                    mock.patch.object(models, "complete", complete):
                ans = louhi._smith_arm(base, {"request": "audit", "kind": "vuln"}, work, "fake", None, log)
            with open(log) as h:
                logged = h.read()
        return ans, calls, logged

    def test_the_end_text_becomes_findings_the_grade_can_credit(self):
        reply = 'Here: {"findings": [{"file": "app.js", "symbol": "find_user_sql", "says": "SQL injection"}]}'
        ans, calls, logged = self.arm([{"event": "answer", "text": END}], reply)
        self.assertEqual(len(calls), 1)
        self.assertIn(END, json.dumps(calls[0]))
        self.assertIn("app.js", json.dumps(calls[0]), "the file list goes with the text")
        self.assertEqual(ans["findings"], [{"file": "app.js", "symbol": "find_user_sql", "says": "SQL injection"}])
        self.assertIn("findings", logged, "the call is in the events log")
        key = {"defects": [{"files": ["app.js"], "symbols": ["find_user_sql"]}]}
        self.assertEqual(louhi._matches(ans["findings"][0], key["defects"][0]), True)

    def test_a_file_not_in_the_repo_is_dropped(self):
        reply = json.dumps({"findings": [{"file": "ghost.js", "symbol": "clamp", "says": "x"},
                                         {"file": "app.rs", "symbol": "clamp", "says": "uncovered"}]})
        ans, _, _ = self.arm([{"event": "answer", "text": "clamp in app.rs is uncovered"}], reply, files=("app.rs",))
        self.assertEqual([f["file"] for f in ans["findings"]], ["app.rs"])

    def test_no_end_text_makes_no_call(self):
        ans, calls, _ = self.arm([{"event": "error", "text": ""}], "{}")
        self.assertEqual((calls, ans["findings"]), ([], []))

    def test_a_failing_model_leaves_findings_empty(self):
        ans, calls, _ = self.arm([{"event": "answer", "text": END}], "no json at all")
        self.assertEqual((len(calls), ans["findings"]), (1, []))


if __name__ == "__main__":
    unittest.main()
