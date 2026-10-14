"""T-0783: big Bash outputs reach the model as head, failure lines and tail, with the full text one Read away."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "hooks", "compact")


def run(stdout, stderr="", state=None, **extra):
    with tempfile.TemporaryDirectory() as home:
        pl = dict({"session_id": "s-1", "tool_name": "Bash", "tool_input": {"command": "pytest"}, "cwd": home,
                   "hook_event_name": "PostToolUse", "tool_response": {"stdout": stdout, "stderr": stderr,
                                                                      "interrupted": False, "isImage": False}}, **extra)
        env = {k: v for k, v in os.environ.items() if k != "FOREMAN_STATE"}
        env.update(FOREMAN_HOME=home, **({"FOREMAN_STATE": state} if state else {}))
        p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(pl), capture_output=True, text=True, timeout=30,
                           env=env)
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

    def test_state_dir_write_errors_and_no_false_footer(self):
        # T-0821 (round-1 review): FOREMAN_STATE moves Foreman's state, so the full text goes there; a folder it can't
        # write leaves the output untouched instead of crashing the hook; nothing cut claims no cut
        big = "\n".join(f"line {i}" for i in range(3000))
        with tempfile.TemporaryDirectory() as state:
            code, out, full = run(big, state=state)
            self.assertEqual(full, big)
            self.assertIn(os.path.join(os.path.realpath(state), "outputs", "s-1"),
                          os.path.realpath(re.search(r"full output: ([^\s\]]+)", out["stdout"]).group(1)))
            blocker = os.path.join(state, "file")
            open(blocker, "w").close()
            p = run(big, state=os.path.join(blocker, "state"))
            self.assertEqual((p[0], p[1]), (0, None), "can't write: the output passes through")
        wide = "\n".join("w" * 300 for _ in range(50))  # over the limit in few lines, none past WIDE
        code, out, _ = run(wide)
        self.assertNotIn("cut", out["stdout"])
        self.assertTrue(out["stdout"].startswith(wide))

    def test_a_lone_surrogate_doesnt_crash_the_hook(self):
        # T-0839 (round-2 review): json accepts \ud800; writing it as utf-8 raised, past the OSError pass-through
        code, out, full = run("line\n" * 2000 + "bad \ud800 char\n")
        self.assertEqual(code, 0)
        self.assertIn("bad", full)

    def test_a_runaway_output_is_saved_as_its_head_and_tail(self):
        # T-0824 (round 2): the full text had no size cap, so one runaway command could fill the disk
        huge = "first line\n" + "x" * 99 + "\n" + ("y" * 99 + "\n") * 30000 + "last line\n"
        code, out, full = run(huge)
        self.assertLess(len(full), len(huge))
        self.assertLessEqual(len(full), 2_100_000)
        self.assertTrue(full.startswith("first line") and full.endswith("last line\n"))
        self.assertIn("characters cut", full)


if __name__ == "__main__":
    unittest.main()
