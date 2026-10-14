"""T-0783: big Bash outputs reach the model as head, failure lines and tail, with the full text one Read away."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "hooks", "compact")


def run(stdout, stderr="", **extra):
    with tempfile.TemporaryDirectory() as home:
        pl = dict({"session_id": "s-1", "tool_name": "Bash", "tool_input": {"command": "pytest"}, "cwd": home,
                   "hook_event_name": "PostToolUse", "tool_response": {"stdout": stdout, "stderr": stderr,
                                                                      "interrupted": False, "isImage": False}}, **extra)
        p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(pl), capture_output=True, text=True, timeout=30,
                           env=dict(os.environ, FOREMAN_HOME=home))
        out = json.loads(p.stdout)["hookSpecificOutput"]["updatedToolOutput"] if p.stdout.strip() else None
        full = None
        if out:
            m = re.search(r"full output: ([^\s\]]+)", out["stdout"] + out["stderr"])
            full = open(m.group(1)).read() if m else None
        return p.returncode, out, full


class Compact(unittest.TestCase):
    def test_a_big_failing_run_keeps_every_failure_line(self):
        lines = [f"tests/test_mod.py::test_{i} PASSED" for i in range(600)]
        lines[300] = "tests/test_mod.py::test_300 FAILED - AssertionError: 2 != 3"
        lines[450] = "E   Traceback (most recent call last):"
        lines.append("==== 1 failed, 599 passed in 3.2s ====")
        text = "\n".join(lines) + "\n"
        code, out, full = run(text)
        self.assertEqual(code, 0)
        self.assertLess(len(out["stdout"]), 8000)
        for must in ("test_300 FAILED", "Traceback", "1 failed, 599 passed", "test_0 PASSED"):
            self.assertIn(must, out["stdout"])
        self.assertEqual(full, text, "the full text is one Read away")
        self.assertEqual((out["interrupted"], out["isImage"]), (False, False))

    def test_small_interrupted_and_image_outputs_are_left_alone(self):
        self.assertIsNone(run("ok\n")[1])
        self.assertIsNone(run("x\n" * 20000, tool_response={"stdout": "x\n" * 20000, "stderr": "", "interrupted": True,
                                                           "isImage": False})[1])
        self.assertIsNone(run("", tool_name="Read")[1])

    def test_a_failure_deep_in_a_long_line_survives(self):
        # measured on 30 days of real outputs: minified bundles and wide tables put the failure word past the cut
        line = "x" * 9000 + " TypeError: cannot read properties of undefined " + "y" * 9000
        code, out, full = run(line + "\nok\n")
        self.assertIn("TypeError: cannot read properties", out["stdout"])
        self.assertLess(len(out["stdout"]), 2000)
        self.assertEqual(full, line + "\nok\n")

    def test_stderr_failures_survive_too(self):
        code, out, _ = run("\n".join(f"line {i}" for i in range(3000)), stderr="fatal: not a git repository\n")
        self.assertIn("fatal: not a git repository", out["stdout"] + out["stderr"])


if __name__ == "__main__":
    unittest.main()
