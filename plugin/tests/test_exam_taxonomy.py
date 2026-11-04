"""T-2926: the exam taxonomy names each scenario's one end. Fixtures are the real last events of s0-001's Smith runs
and the end texts of the 32k / nothink exam logs (copied, shortened where long)."""
import json
import os
import tempfile
import unittest

from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)

from sampo import louhi

E = lambda kind, text, **kw: {"event": kind, "text": text, **kw}
ENDS = {
    "budget": [E("error", "fm code: model: gpu-qwen4-nothink: reasoning used the whole budget: no text in 8192 tokens (think: false,")],
    "plan_refused": [E("error", "fm code: fm focus refused the plan: fm: refused: T-0001 isn't planned enough to start: missing a criterion")],
    "plan_refused_new": [E("error", "fm code: fm task new refused the plan: fm: refused: x")],
    "no_plan": [E("error", "fm code: the model gave no valid plan after 2 repairs, nor field by field: type must be one of FIX, not None")],
    "loop": [E("error", "fm code: stopped: the model used all 40 turns (--max-steps) before step:2 was done; fm code --resume T-0001")],
    "finish_refused": [E("verify", "verify 1 pass", label="verify", exit=0),
                       E("blocked", "T-0001 blocked: fm code: fm task finish refused: fm: refused: T-0001 can't be marked done: - no Decision: research")],
    "finish_refused_proof": [E("blocked", "T-0001 blocked: fm code: fm task finish refused: fm: T-0001 not finished, nothing ran: - no red→green proof")],
    "finish_refused_set": [E("blocked", "T-0001 blocked: fm code: fm task set Regression test refused: fm: bad")],  # T-2948
    "timeout": [E("timeout", "no end after 900 s")],
    "closed": [E("action", "edit ok", action="edit", target="a", result="ok"), E("closed", "T-0001 closed")],
    "other": [E("answer", "I could not do it")],
}


class Taxonomy(unittest.TestCase):
    def test_each_end_is_one_named_class(self):
        for name, evs in ENDS.items():
            want = name.split("_new")[0].replace("_proof", "").replace("_set", "")
            self.assertEqual(louhi.end_class(evs), want, name)
            if want in louhi.FAILURE_CLASSES and want != "loop":
                self.assertGreaterEqual(louhi.failure_classes(evs).get(want, 0), 1, name)

    def test_no_plan_is_not_malformed(self):
        got = louhi.failure_classes(ENDS["no_plan"])
        self.assertEqual(got, {"no_plan": 1})

    def test_ends_sum_to_the_scenarios(self):
        from sampo import core as c
        with tempfile.TemporaryDirectory() as d:
            ans = os.path.join(d, "answers", "smith")
            os.makedirs(ans)
            for i, evs in enumerate(ENDS.values()):
                with open(os.path.join(ans, f"s{i}.events.jsonl"), "w") as f:
                    f.write("".join(json.dumps(e) + "\n" for e in evs))
            orig = (louhi.load, louhi._answers)
            louhi.load, louhi._answers = (lambda p, run: None), (lambda p, run, agent: ans)
            try:
                tax = louhi.taxonomy(None, "r")
            finally:
                louhi.load, louhi._answers = orig
        self.assertEqual(tax["scenarios"], len(ENDS))
        self.assertEqual(sum(tax["ends"].values()), tax["scenarios"])
        self.assertEqual(tax["ends"]["budget"], 1)
        self.assertEqual(tax["ends"]["other"], 1)
        self.assertEqual(tax["ends"]["closed"], 1)
        self.assertEqual(tax["ends"]["plan_refused"], 2)


if __name__ == "__main__":
    unittest.main()
