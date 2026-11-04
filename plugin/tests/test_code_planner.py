"""T-2945: fm code --planner P --model A asks the plan and the close notes of P and runs every step on A."""
import json
import os
import tempfile
import unittest
from unittest import mock

from test_code import CLOSE, FIX, M_PLAN, CodeCase, journal_text, plan

from sampo import louhi, models, smithbench  # noqa: E402  (test_code puts plugin/lib on the path)


class CodePlanner(CodeCase):
    def split(self, *flags):
        big = self.serve("anthropic", plan(M_PLAN), CLOSE, name="big")
        small = self.serve("anthropic", *FIX, name="small")
        return self.code("fix add", "--model", "small", *flags, check=False), big, small

    def test_the_plan_and_close_notes_go_to_the_planner_and_the_steps_to_the_model(self):
        r, big, small = self.split("--planner", "big")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(len(big.seen), 2, "the plan and the close notes")
        self.assertEqual(len(small.seen), 2, "the two step turns")
        self.assertIn("Make calc.add add", big.said(1) + small.said(0))
        start = json.loads(next(l for l in journal_text(self, "T-0001").splitlines() if '"kind": "start"' in l))
        self.assertEqual((start["model"], start["planner"]), ("small", "big"))

    def test_without_planner_every_slot_goes_to_the_model(self):
        small = self.serve("anthropic", plan(M_PLAN), *FIX, CLOSE, name="small")
        r = self.code("fix add", "--model", "small")
        self.assertEqual(len(small.seen), 4, r.stdout)

    def test_a_bad_planner_fails_before_the_first_call(self):
        small = self.serve("anthropic", plan(M_PLAN), *FIX, CLOSE, name="small")
        r = self.code("fix add", "--model", "small", "--planner", "nope", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nope", r.stdout + r.stderr)
        self.assertEqual(small.seen, [])


class ExamArm(unittest.TestCase):
    def test_the_smith_arm_passes_planner_through_and_records_it(self):
        fake = "import json,sys\nprint(json.dumps({'event': 'closed', 'text': ' '.join(sys.argv)}))\n"
        done = {"text": '{"findings": []}', "tool_calls": [], "usage": {"in": 1, "out": 1}}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(models, "resolve", lambda m: {"name": m}), \
                mock.patch.object(models, "complete", lambda *a, **k: done):
            os.makedirs(os.path.join(tmp, "base", "repo"))
            fm = os.path.join(tmp, "fm.py")
            with open(fm, "w") as h:
                h.write(fake)
            for planner in ("big", None):
                with mock.patch.object(smithbench, "FM", fm):
                    ans = louhi._smith_arm(os.path.join(tmp, "base"), {"request": "r", "kind": "bug"},
                                           os.path.join(tmp, f"w{planner}"), "small", None,
                                           os.path.join(tmp, "e.jsonl"), planner)
                self.assertEqual(ans["planner"], planner)
                with open(os.path.join(tmp, "e.jsonl")) as h:
                    self.assertEqual("--planner big" in h.read(), planner == "big")
