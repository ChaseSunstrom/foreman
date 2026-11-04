"""T-2936: a model that never writes plan JSON still gets an M plan through the field-by-field ladder (fakes only)."""
import json
import unittest

from test_code import CodeCase

OPTIONS = ("build | add the check to calc.add and its test | the test cannot reach calc.add\n"
           "exists | reuse the existing add helper in calc.py | the helper is not what the tests import\n"
           "less | leave calc.add alone and document it | the bug stays")
M_ANSWERS = ("FIX", "M", "Make calc.add add",
             "calc.add adds two numbers :: python3 test_calc.py\ncalc.add keeps its signature :: python3 test_calc.py",
             "1. edit calc.py\n2. run the test",
             "- the request means calc.add returns a sum\n- the request means every operator in calc.py is checked",
             OPTIONS, "1", "70", "it is the smallest change that makes the test pass")


class Ladder(CodeCase):
    def run_ladder(self, answers):
        return self.serve("openai", *[{"text": "nope"}] * 3, *[{"text": a} for a in answers])

    def test_an_m_plan_comes_field_by_field_and_passes_check_plan(self):
        from sampo import smith
        f = self.run_ladder(M_ANSWERS)
        r = self.code("fix add", "--model", "fake", "--dry-plan")
        self.assertIn("field by field", r.stdout)
        self.assertEqual(len(f.seen), 3 + len(M_ANSWERS))
        v = {"type": "FIX", "tier": "M", "title": "Make calc.add add", "steps": ["edit calc.py", "run the test"],
             "criteria": smith._criteria("a :: b"),
             "readings": smith._items("- one\n- two"), "options": smith._options(OPTIONS), "choice": 1,
             "confidence": 70, "why": "the smallest change that makes the test pass"}
        self.assertIsNone(smith.check_plan(v))
        self.assertEqual([o["kind"] for o in v["options"]], ["build", "exists", "less"])

    def test_every_question_has_a_worked_example_and_type_lists_the_six(self):
        from sampo import smith
        for key, q, *_ in smith.PLAN_FIELDS:
            self.assertIn("for example", q, key)
        self.assertTrue(all(t in smith.PLAN_FIELDS[0][1] for t in smith.TYPES))

    def test_an_s_answer_asks_no_m_fields(self):
        f = self.run_ladder(("FIX", "S", "Make calc.add add", "calc.add adds :: python3 test_calc.py", "1. edit"))
        r = self.code("fix add", "--model", "fake", "--dry-plan")
        self.assertIn("field by field", r.stdout)
        self.assertEqual(len(f.seen), 3 + 5)


if __name__ == "__main__":
    unittest.main()
