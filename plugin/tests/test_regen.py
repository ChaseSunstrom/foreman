"""T-2918: sampo regen PATH deletes one module in a throwaway worktree and regrows it from its intent alone. Every model
call is a fake; nothing here reaches a model."""
# map-links: plugin/lib/sampo/regen.py
import os
import subprocess
import unittest
from unittest import mock

from helpers import ForemanTestCase

SRC = '''"""Doubles."""
import os


def double(x):
    return x * 2  # SECRETBODY-7731
'''
TEST = '''import os
import sys
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from pkg import twice


class Twice(unittest.TestCase):
    def test_double(self):
        self.assertEqual(twice.double(3), 6)

    def test_zero(self):
        self.assertEqual(twice.double(0), 0)
'''
GOOD = "```python\nimport os\n\n\ndef double(x):\n    return x + x\n```"


def git(root, *a):
    subprocess.run(["git", "-C", root, "-c", "user.email=a@b", "-c", "user.name=t", *a], check=True,
                   capture_output=True)


class Regen(ForemanTestCase):
    def setUp(self):
        super().setUp()
        from sampo import regen
        self.r = regen
        self.root = os.path.join(self.tmp, "fix")
        for rel, text in (("lib/pkg/twice.py", SRC), ("lib/pkg/user.py", "from pkg import twice\nx = twice.double(1)\n"),
                          ("lib/pkg/__init__.py", ""), ("tests/test_twice.py", TEST), ("tests/helpers.py", "")):
            os.makedirs(os.path.dirname(os.path.join(self.root, rel)), exist_ok=True)
            with open(os.path.join(self.root, rel), "w") as f:
                f.write(text)
        git(self.root, "init", "-q")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "x")
        self.links = {"tests/test_twice.py": ["lib/pkg/twice.py"]}
        self.rel = "lib/pkg/twice.py"

    def run_regen(self, replies):
        prompts = []

        def ask(system, prompt):
            prompts.append(prompt)
            return replies[min(len(prompts) - 1, len(replies) - 1)]
        out = self.r.regen(self.root, self.rel, ask, self.r.intent(self.root, self.rel, [("T-1", "make doubling", "", "")], "twice: doubles", self.links), self.links)
        return out, prompts

    def test_the_verb_lives_on_moons(self):
        self.fm("init")
        for argv in (("moons", "regen", "--leaves"), ("genesis", "moonshot", "regen", "--leaves")):
            self.assertIn("0 leaf modules", self.fm(*argv).stdout)

    def test_leaves_pick_small_tested_modules_and_skip_aliases(self):
        with open(os.path.join(self.root, "lib/pkg/fmtwice.py"), "w") as f:
            f.write("x = 1\n")
        with open(os.path.join(self.root, "lib/pkg/big.py"), "w") as f:
            f.write("x = 1\n" * 300)
        links = dict(self.links, **{"tests/test_big.py": ["lib/pkg/big.py"], "tests/test_fmtwice.py": ["lib/pkg/fmtwice.py"]})
        self.assertEqual(self.r.leaves(self.root, links), ["lib/pkg/twice.py"])

    def test_prompt_holds_intent_and_never_the_code(self):
        out, prompts = self.run_regen([GOOD])
        self.assertTrue(out["round_trip"], out)
        self.assertIn("make doubling", prompts[0])
        self.assertIn("twice: doubles", prompts[0])
        self.assertIn("test_double", prompts[0])  # the tests are intent
        self.assertIn("double", prompts[0])  # the importer's name
        self.assertNotIn("SECRETBODY-7731", prompts[0])
        self.assertNotIn("x * 2", prompts[0])

    def test_each_tests_result_is_reported_and_the_main_checkout_is_untouched(self):
        out, _ = self.run_regen(["```python\ndef double(x):\n    return x + 1 if x else 0\n```"] * 2)
        self.assertFalse(out["round_trip"])
        self.assertEqual(out["tests"].get("test_double"), False)
        self.assertEqual(out["tests"].get("test_zero"), True)
        self.assertEqual(out["tries"], 2)
        with open(os.path.join(self.root, self.rel)) as f:
            self.assertEqual(f.read(), SRC)
        self.assertEqual(subprocess.run(["git", "-C", self.root, "status", "--porcelain"], capture_output=True,
                                        text=True).stdout, "")
        self.assertEqual(subprocess.run(["git", "-C", self.root, "worktree", "list"], capture_output=True,
                                        text=True).stdout.count("\n"), 1, "the throwaway worktree is gone")

    def test_a_bad_reply_is_refused_without_running_and_the_second_try_may_pass(self):
        for bad, why in (("```python\nimport subprocess\ndef double(x): return x*2\n```", "import"),
                         ("```python\ndef double(x:\n```", "compile"), ("no code here", "code")):
            code, reason = self.r.check_reply(bad, {"os"})
            self.assertIsNone(code, bad)
            self.assertIn(why, reason)
        out, prompts = self.run_regen(["```python\nimport socket\n```", GOOD])
        self.assertTrue(out["round_trip"])
        self.assertEqual(out["tries"], 2)
        self.assertIn("import", prompts[1], "the second try is told why the first was refused")

    def test_two_tries_at_most(self):
        out, prompts = self.run_regen(["nothing"] * 5)
        self.assertEqual(len(prompts), 2)
        self.assertFalse(out["round_trip"])

    def test_a_dynamic_import_is_refused(self):
        code, why = self.r.check_reply("```python\nx = __import__('os')\n```", {"os"})
        self.assertIsNone(code)

    def test_never_writes_outside_the_worktree(self):
        with self.assertRaises(ValueError):
            self.r.regen(self.root, "../outside.py", lambda s, p: GOOD, "", self.links)

    def test_sensitive_asks_loopback_only(self):
        far = {"name": "far", "kind": "openai", "base_url": "http://10.1.2.3:8000/v1", "model": "m"}
        with mock.patch("sampo.models.resolve", return_value=far):
            with self.assertRaises(ValueError):
                self.r.make_ask(mock.Mock(slug="x"), "far", sensitive=True)
            with self.assertRaises(ValueError):
                self.r.make_ask(mock.Mock(slug="x"), "haiku", sensitive=True)

    def test_make_ask_calls_complete_and_haiku_through_run_child(self):
        near = {"name": "near", "kind": "openai", "base_url": "http://127.0.0.1:8000/v1", "model": "m"}
        with mock.patch("sampo.models.resolve", return_value=near), \
                mock.patch("sampo.models.complete", return_value={"text": "hi"}) as comp:
            self.assertEqual(self.r.make_ask(mock.Mock(slug="x"), "near", sensitive=True)("s", "p"), "hi")
            self.assertIsNone(comp.call_args.kwargs.get("tools"))
        with mock.patch("sampo.ideas.run_child", return_value="yo") as rc:
            self.assertEqual(self.r.make_ask(mock.Mock(slug="x"), "haiku", sensitive=False)("s", "p"), "yo")
            self.assertEqual(rc.call_args.args[3], "haiku")

    def test_slice_files_the_sample_first_and_advances_at_two(self):
        import json
        out = os.path.join(self.tmp, "res.json")
        seen = []
        res = self.r.slice_run(self.root, ["a", "b", "c"], lambda m, prof: {"module": m, "round_trip": m != "c", "model": prof},
                               out, ["local", "haiku"], on_sample=seen.append)
        self.assertEqual(seen, [["a", "b", "c"]])
        self.assertEqual(res["advanced"], "M-02 slice")
        with open(out) as f:
            self.assertEqual(json.load(f)["sample"], ["a", "b", "c"])
        res = self.r.slice_run(self.root, ["a", "c"], lambda m, prof: {"module": m, "round_trip": m == "a", "model": prof},
                               out, ["local", "haiku"])
        self.assertEqual(res["advanced"], "not-yet")
        self.assertEqual([x["approaches"] for x in res["modules"] if x["module"] == "c"], [["local", "haiku"]])


if __name__ == "__main__":
    unittest.main()
