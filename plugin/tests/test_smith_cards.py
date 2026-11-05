"""T-3160: fm code offers its task the calling cards that fit it, as a native tool and as a JSON action; a card call
runs through the card runner (schema, confinement, checker) and fm code's own guard, and the model reads its result."""
import json
import os
import subprocess
import sys
import unittest

from test_callcards import confined
from test_code import CLOSE, CodeCase, call, plan, text_action

GUARD = {"path": "calc.py", "function": "add", "param": "a", "value": "0"}


def card(name, inputs):  # test_code's call() takes the action's name as its own first argument
    return {"calls": [("card", {"name": name, "inputs": inputs})]}


def card_text(name, inputs):
    return {"text": "I'll do this:\n" + json.dumps({"action": "card", "name": name, "inputs": inputs})}


@confined
class Cards(CodeCase):
    def test_a_native_card_call_changes_the_file_and_the_model_reads_its_diff(self):
        f = self.serve("openai", plan(), card("py-none-guard", GUARD),
                       call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds"), CLOSE)
        r = self.code("make calc.add add, and return early if the parameter a is None", "--model", "fake",
                      check=False)
        self.assertIn("    if a is None:\n        return 0\n    return a + b", self.calc(), r.stdout + r.stderr)
        tools = [t["function"]["name"] for t in f.seen[1]["tools"]]
        self.assertIn("card", tools)
        self.assertIn("py-none-guard", f.said(1), "the card is offered by name")
        self.assertIn("card py-none-guard: applied", f.said(2))
        self.assertIn("+    if a is None:", f.said(2), "the model reads the diff")
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)

    def test_the_json_action_path_calls_a_read_card(self):
        f = self.serve("openai", plan(), card_text("py-outline", {"path": "calc.py"}),
                       text_action("edit", file="calc.py", old="a - b", new="a + b"),
                       text_action("done", summary="adds"), CLOSE, tools=False)
        r = self.code("outline calc.py, then make calc.add add instead of subtract", "--model", "fake", check=False)
        self.assertIn('\\"action\\": \\"card\\"', f.said(1), "the text form is taught")
        self.assertIn("py-outline", f.said(1))
        self.assertIn("card py-outline: facts", f.said(2))
        self.assertIn("return a + b", self.calc(), r.stdout + r.stderr)

    def test_a_card_not_offered_or_misspelt_is_named(self):
        f = self.serve("openai", plan(), card("py-none-gaurd", GUARD),
                       call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds"), CLOSE)
        self.code("make calc.add add, and return early if the parameter a is None", "--model", "fake", check=False)
        self.assertIn("did you mean 'py-none-guard'", f.said(2))
        self.assertNotIn("if a is None", self.calc())

    def test_an_unknown_action_lists_card_among_the_actions(self):
        f = self.serve("openai", plan(), call("call_card", card="py-none-guard"),
                       call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds"), CLOSE)
        self.code("make calc.add add, and return early if the parameter a is None", "--model", "fake", check=False)
        self.assertIn("no action 'call_card'; the actions are read, search, edit, write, run, done and card",
                      f.said(2))

    def test_cards_off_offers_none(self):
        f = self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"),
                       call("done", summary="adds"), CLOSE)
        self.code("make calc.add add, and return early if the parameter a is None", "--model", "fake",
                  env={"SAMPO_CARDS": "off"}, check=False)
        self.assertNotIn("card", [t["function"]["name"] for t in f.seen[1]["tools"]])
        self.assertNotIn("py-none-guard", f.said(1))

    def test_a_question_runs_read_cards_only(self):
        f = self.serve("openai", {"text": json.dumps({"answer": "it subtracts"})},
                       card("py-outline", {"path": "calc.py"}), card("py-none-guard", GUARD),
                       call("done", summary="calc.add (calc.py line 1) subtracts"))
        r = self.code("outline calc.py: what does calc.add do?", "--model", "fake", "--json")
        self.assertIn("card py-outline: facts", f.said(2), r.stdout)
        notes = [json.loads(ln) for ln in r.stdout.splitlines() if '"cards"' in ln and ln.startswith("{")]
        self.assertIn("py-outline", notes[0]["cards"], "the run says what it was offered (the card bench reads it)")
        self.assertIn("refused", f.said(3))
        self.assertNotIn("py-none-guard", json.dumps(f.seen[1]["tools"]), "a write card isn't offered to a question")
        self.assertEqual(self.calc(), "def add(a, b):\n    return a - b\n")


class Portable(unittest.TestCase):
    """T-3238: on macOS (no Landlock) every test that runs a card for real must skip, not fail: CI was red on main."""

    def test_card_tests_skip_where_calls_cannot_be_confined(self):
        here = os.path.dirname(os.path.abspath(__file__))
        boot = ("import sys\nsys.path[:0] = [sys.argv[1], sys.argv[2]]\nfrom sampo import landlock\n"
                "landlock.available = lambda: (False, 'Landlock is Linux only (this is Darwin)')\nimport unittest\n"
                "unittest.main(module=None, argv=['unittest', 'test_callcards', 'test_smith_cards.Cards'])\n")
        r = subprocess.run([sys.executable, "-c", boot, os.path.join(here, "..", "lib"), here], cwd=here,
                           capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0, r.stderr[-3000:])
        self.assertIn("skipped=", r.stderr)
