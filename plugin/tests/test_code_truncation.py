"""T-1404: a server that silently drops the start of a long prompt (llama.cpp, Ollama, vLLM with a small context) still
answers; fm code reads the reply's own prompt-token count and, far under what it sent, stops naming the truncation
instead of acting on an answer that never saw its instructions."""
from test_code import CodeCase, call, plan

LONG = "make calc.add add instead of subtract. Background: " + "the adder keeps a running total of numbers. " * 300
FULL = 5000  # what a server that read the whole prompt reports for it (about 3,400 by fm code's estimate)


def big(step, n=FULL):
    return dict(step, **{"in": n})


class Truncation(CodeCase):
    def failed(self, r):
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        return r.stdout + r.stderr

    def test_a_plan_whose_prompt_was_cut_fails_naming_it(self):
        for kind in ("openai", "anthropic"):
            with self.subTest(kind=kind):
                self.serve(kind, big(plan(), 40))
                out = self.failed(self.code(LONG, "--model", "fake", check=False))
                self.assertIn("truncated the prompt at 40 tokens", out)
                self.assertIn("longer context", out)
                self.assertEqual(self.status(), "")  # no task, no edit

    def test_a_step_whose_prompt_was_cut_fails_before_running_its_action(self):
        self.serve("openai", big(plan()), big(call("edit", file="calc.py", old="a - b", new="a + b"), 200))
        out = self.failed(self.code(LONG, "--model", "fake", "--no-commit", check=False))
        self.assertIn("truncated the prompt at 200 tokens", out)
        self.assertIn("return a - b", self.calc())  # the confused answer's edit never ran

    def passes(self, request, n):
        steps = (plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="adds"))
        self.serve("openai", *(big(s, n) for s in steps))
        self.code(request, "--model", "fake", "--no-commit")
        self.assertIn("return a + b", self.calc())

    def test_a_reply_that_read_the_whole_prompt_passes(self):
        self.passes(LONG, FULL)

    def test_a_server_that_reports_no_usage_passes(self):
        self.passes(LONG, 0)

    def test_a_short_prompt_never_trips_it(self):  # under the floor, tokenizer variance is no signal
        self.passes("make calc.add add", 5)
