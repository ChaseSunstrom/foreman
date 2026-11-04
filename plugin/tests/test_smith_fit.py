"""T-2939: a local profile whose prompt is over its context (less an output reserve) is cut to fit (the project file
list first, then older tool results, never the instructions) and says what it left out; anything that fits, and any
profile that is not local, is sent unchanged; when only the instructions and request remain and still do not fit, the
run stops as before."""
import json
import os
import subprocess
import unittest

import helpers  # noqa: F401  (puts plugin/lib on sys.path)
from sampo import smith
from test_code import CodeCase, plan
from test_code_truncation import LONG

NAMES = 150


LOCAL = {"name": "x", "kind": "openai", "base_url": "http://127.0.0.1:1/v1", "context": 4000}


def sent_tokens(body):
    return sum(len(str(x.get("content") or "")) for x in body["messages"]) // 4


class Fit(CodeCase):
    def files(self):
        for i in range(NAMES):
            open(os.path.join(self.repo, f"module_with_a_long_name_{i:04d}_for_padding.txt"), "w").close()
        subprocess.run(["git", "-C", self.repo, "add", "."], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "many files"], check=True)

    def run_with(self, context, request="make calc.add add", name="fake", used=0):
        f = self.serve("openai", dict(plan(), **{"in": used}))  # used 0: a server that reports no usage
        path = os.path.join(self.home, "models.json")
        conf = json.load(open(path))
        conf["profiles"][name]["context"] = context
        json.dump(conf, open(path, "w"))
        r = self.code(request, "--model", name, "--dry-plan", "--json", check=False)
        return f, r, r.stdout + r.stderr

    def test_a_prompt_over_the_context_is_cut_and_says_what_was_left_out(self):
        self.files()
        f, r, out = self.run_with(2500)
        self.assertEqual(r.returncode, 0, out)
        self.assertRegex(out, r"left out \d+ files")
        self.assertLessEqual(sent_tokens(f.seen[0]), 2500 - 2500 // 4)

    def test_a_prompt_within_the_context_is_sent_whole_with_no_note(self):
        self.files()
        f, r, out = self.run_with(32768)
        self.assertEqual(r.returncode, 0, out)
        self.assertNotIn("left out", out)
        self.assertIn("module_with_a_long_name_0000", json.dumps(f.seen[0]))

    def test_only_the_instructions_and_request_left_still_stops(self):
        f, r, out = self.run_with(100, LONG, used=40)  # nothing left to cut: the server's cut shows in its usage
        self.assertEqual(r.returncode, 1, out)
        self.assertIn("truncated the prompt at 40 tokens", out)

    def test_older_results_are_cut_before_the_prompt_is_sent(self):
        msgs = [{"role": "system", "content": "rules"}, {"role": "user", "content": "go"}]
        for i in range(8):
            msgs += [{"role": "assistant", "content": "x"}, {"role": "tool", "content": f"result {i}\n" + "y" * 4000}]
        run = type("R", (), {"emit": lambda s, *a, **k: s.notes.append(a), "notes": [], "root": "/nonexistent", "fence": lambda s, t: t})()
        out = smith.fit(run, LOCAL, msgs)
        self.assertLessEqual(sum(len(x["content"]) for x in out) // 4, 3000)
        self.assertEqual(msgs[3]["content"][:8], "result 0")  # the stored conversation is untouched
        self.assertRegex(run.notes[0][1], r"left out 0 files, \d+ older results")

    def test_a_profile_that_is_not_local_is_never_cut(self):
        msgs = [{"role": "system", "content": "s" * 40000}, {"role": "user", "content": "go"}]
        self.assertIs(smith.fit(None, dict(LOCAL, base_url="https://api.example.com/v1"), msgs), msgs)


if __name__ == "__main__":
    unittest.main()
