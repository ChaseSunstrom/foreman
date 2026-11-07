"""T-2878: Smith for small local models. An action's arguments under another unambiguous name, or nested one level, are
read (mimo-v2.6:9b lost 7.8% of its turns to `write needs file as str`); a missing one is sent back as one line naming
what was sent and the shape wanted. --small (small-model mode) adds the controls for the hollow close, 36% of the local
models' exam failures: a change plan's check must fail before the work, a change request isn't planned as research or
answered, and a change plan's last step can't end with nothing changed."""
import json
import os
import tempfile
import unittest
from unittest import mock

from test_code import CLOSE, PLAN, CodeCase, call, journal_text, plan

from sampo import louhi, models, smith, smithbench

DONE = call("done", summary="fixed")


class ArgAliases(CodeCase):
    def calc(self):
        with open(os.path.join(self.repo, "calc.py"), encoding="utf-8") as f:
            return f.read()

    def test_an_edit_with_path_for_file_lands(self):
        self.serve("openai", plan(PLAN), call("edit", path="calc.py", old="a - b", new="a + b"), DONE)
        r = self.code("fix add", "--model", "fake")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("a + b", self.calc())
        self.assertEqual(self.task()["status"], "done")

    def test_arguments_nested_one_level_are_read(self):
        self.serve("openai", plan(PLAN), call("edit", arguments={"file_path": "calc.py", "old_string": "a - b",
                                                                   "new_string": "a + b"}), DONE)
        r = self.code("fix add", "--model", "fake")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("a + b", self.calc())

    def test_a_missing_argument_comes_back_as_one_line_naming_what_was_sent(self):
        f = self.serve("openai", plan(PLAN), call("write", content="x\n"),
                       call("edit", file="calc.py", old="a - b", new="a + b"), DONE)
        self.code("fix add", "--model", "fake")
        back = f.said(2)
        self.assertIn("write needs file as str (you sent: content)", back)
        self.assertIn('{\\"action\\": \\"write\\", \\"file\\"', back)  # the shape wanted, in the tool result

    def test_two_aliases_are_ambiguous_and_neither_is_guessed(self):
        f = self.serve("openai", plan(PLAN), call("edit", path="calc.py", filename="other.py", old="a - b", new="a + b"),
                       call("edit", file="calc.py", old="a - b", new="a + b"), DONE)
        self.code("fix add", "--model", "fake")
        self.assertIn("you sent: filename, new, old, path", f.said(2))
        self.assertFalse(os.path.exists(os.path.join(self.repo, "other.py")))

    def test_two_aliases_with_one_value_are_one_argument(self):
        self.assertEqual(smith.canon_args("edit", {"path": "x.py", "file_path": "x.py", "old": "a", "new": "b"})["file"],
                         "x.py")
        self.assertNotIn("file", smith.canon_args("edit", {"path": "x.py", "file_path": "y.py", "old": "a", "new": "b"}))


class AsksChange(unittest.TestCase):
    def test_a_question_asks_for_no_change(self):
        for q in ("Why does the cache update twice?", "Explain how handle works", "what does calc.add do",
                  "Can you add a test?", "is the fix in?"):
            with self.subTest(q=q):
                self.assertIsNone(smith.asks_change(q))

    def test_an_imperative_does(self):
        for r, word in (("fix add", "fix"), ("Something is off in the paging; find and fix it.", "fix"),
                        ("make this faster", "make"), ("The tests won't run; fix it.", "fix")):
            with self.subTest(r=r):
                self.assertEqual(smith.asks_change(r), word)
        self.assertIsNone(smith.asks_change("Check the docs are right."))


GREEN ="python3 -c 'import calc'"  # passes before any work
FIX_EDIT = call("edit", file="calc.py", old="a - b", new="a + b")


class SmallMode(CodeCase):
    def run_small(self, small, *script, request="fix add"):
        f = self.serve("openai", *script)
        r = self.code(request, "--model", "fake", *(["--small"] if small else []), check=False)
        return f, r

    def test_a_perf_plan_whose_check_already_passes_goes_back_once(self):
        perf = dict(PLAN, type="PERFORMANCE", criteria=[{"text": "calc imports", "verify": GREEN}])
        for small in (True, False):
            with self.subTest(small=small):
                f, r = self.run_small(small, plan(perf), plan(PLAN), FIX_EDIT, call("done", summary="fixed"), CLOSE)
                sent_back = "already passes before any work" in f.said(1)
                self.assertEqual(sent_back, small, r.stdout + r.stderr)
                self.tearDown()
                self.setUp()

    def test_a_change_request_planned_as_research_goes_back_to_be_typed(self):
        research = dict(PLAN, type="RESEARCH")
        f, r = self.run_small(True, plan(research), plan(PLAN), FIX_EDIT, call("done", summary="fixed"), CLOSE)
        self.assertIn("asks for a change", f.said(1))
        self.assertIn("RESEARCH", f.said(1))
        self.assertEqual(self.task()["type"], "FIX")

    def test_a_change_request_answered_goes_back_for_a_plan(self):
        answer = {"text": json.dumps({"answer": "calc.add subtracts; change - to +"})}
        f, r = self.run_small(True, answer, plan(PLAN), FIX_EDIT, call("done", summary="fixed"), CLOSE)
        self.assertIn("asks for a change", f.said(1))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.task()["status"], "done")

    def test_a_question_is_still_answered(self):
        answer = {"text": json.dumps({"answer": "calc.add subtracts"})}
        f, r = self.run_small(True, answer, call("done", summary="calc.add subtracts (calc.py:2)"),
                              request="what does calc.add do?")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("asks for a change", json.dumps(f.seen))

    def test_the_last_step_of_a_change_plan_cant_end_with_nothing_changed(self):
        green = dict(PLAN, criteria=[{"text": "calc imports", "verify": GREEN}])
        close = {"text": json.dumps(dict(json.loads(CLOSE["text"]), regression="none: the check was green before"))}
        f, r = self.run_small(True, plan(green), plan(green), call("done", summary="nothing to do"), FIX_EDIT,
                              call("done", summary="fixed"), close)  # a green-before check: the close asks why
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        refused = [json.loads(ln) for ln in journal_text(self).splitlines() if '"early_done"' in ln]
        self.assertEqual(len(refused), 1)
        self.assertIn("no file has changed", f.said(3))

    def test_the_exam_arm_passes_small_and_records_it(self):
        script = "import json,sys\nprint(json.dumps({'event':'answer','text':' '.join(sys.argv)}))\n"
        with tempfile.TemporaryDirectory() as tmp:
            base, work = os.path.join(tmp, "base"), os.path.join(tmp, "work")
            os.makedirs(os.path.join(base, "repo"))
            fm = os.path.join(tmp, "fm.py")
            with open(fm, "w") as h:
                h.write(script)
            with mock.patch.object(smithbench, "FM", fm), mock.patch.object(models, "resolve", lambda m: {"name": m}), \
                    mock.patch.object(models, "complete", lambda *a, **k: {"text": "{}", "tool_calls": [], "usage": {}}):
                ans = louhi._smith_arm(base, {"request": "x", "kind": "vuln"}, work, "fake", None,
                                       os.path.join(tmp, "e.jsonl"), small=True)
            self.assertIn("--small", ans["notes"][0])
            self.assertTrue(ans["small"])
