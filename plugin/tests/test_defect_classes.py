"""T-1164: fm lane brief lists the defect classes reviewers confirmed in the last 30 days (a class once, with its count and
an example); rejected and older findings are ignored; with none there is no section."""
import json
import os
import unittest

from helpers import ForemanTestCase

import fmcore as c


class DefectClasses(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def finding(self, text, verdict="confirmed"):
        c.log_event(self.p, "finding", task="T-9000", data={"lens": "edge", "verdict": verdict, "text": text})

    def brief(self):
        tid = json.loads(self.fm("task", "new", "X", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true",
                                 "--step", "s", "--interpretation", "x", "--approach", "x", "--json").stdout)["id"]
        path = json.loads(self.fm("lane", "brief", tid, "--json").stdout)["path"]
        with open(path) as f:
            return f.read()

    def test_two_confirmed_of_one_class_print_once_with_count(self):
        self.finding("The new check runs on every hook call: hot path cost")
        self.finding("Another hot path scan of the whole ledger per prompt")
        self.finding("hot path read, but rejected", "rejected")
        text = self.brief()
        self.assertIn("Defects this project keeps shipping", text)
        lines = [ln for ln in text.splitlines() if "hot path" in ln.lower() and "2" in ln]
        self.assertEqual(len(lines), 1, text)
        self.assertIn("Another hot path scan", lines[0])  # the newest as the example

    def test_rejected_and_old_findings_make_no_section(self):
        self.finding("hot path cost", "rejected")
        old = {"ts": "2020-01-01T00:00:00+00:00", "task": "T-9001", "event": "finding",
               "data": {"lens": "edge", "verdict": "confirmed", "text": "hot path cost"}}
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            f.write(json.dumps(old) + "\n")
        self.assertNotIn("keeps shipping", self.brief())

    def test_no_findings_no_section(self):
        self.assertNotIn("keeps shipping", self.brief())


if __name__ == "__main__":
    unittest.main()
