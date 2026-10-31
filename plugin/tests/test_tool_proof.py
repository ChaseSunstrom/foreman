"""T-2372 (Mission 6, #5): a task that built a tool (fm new tool, fm mcp new) closes only after four proofs, each
refused on its own and named in the refusal: a tool_search receipt for its need before the build, the tool's test run
by fm red and then green, that test failing on a stubbed copy of the tool, and the tool used (a Bash call in the
session's transcript, not through its own test) after the green run. A task that built nothing pays nothing."""
import json
import os
import time

from helpers import ForemanTestCase

import fmcore as c
import fmtoolproof

SID = "0a1b2c3d-0000-4000-8000-0123456789ab"
TOOL = ("#!/usr/bin/env python3\n# fm new tool\nimport sys\n\n\ndef run(text):\n    return text.upper()\n\n\n"
        "def main(argv=None):\n    a = sys.argv[1:] if argv is None else argv\n"
        "    if not a or not a[0]:\n        return 1\n    print(run(a[0]))\n    return 0\n\n\n"
        "if __name__ == '__main__':\n    sys.exit(main())\n")
TEST = ("import os, sys, unittest\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "
        "'..', 'tools'))\nimport shout\n\n\nclass T(unittest.TestCase):\n    def test_it(self):\n"
        "        self.assertEqual(shout.run('abc'), 'ABC')\n        self.assertEqual(shout.main(['']), 1)\n\n\n"
        "if __name__ == '__main__':\n    unittest.main()\n")
WEAK = TEST.replace("self.assertEqual(shout.run('abc'), 'ABC')", "pass").replace("self.assertEqual(shout.main(['']), 1)",
                                                                                   "pass")
RUN = "python3 tests/test_shout.py"
PHRASE = {"search": "no search receipt", "red": "no red then green", "stub": "stub check", "use": "never used"}


class ToolProof(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Shout", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.p = c.find_project(self.repo)
        self.tid = c.load_briefs(self.p)[-1].id
        self.cc = os.path.join(self.tmp, "cc")
        self.env = {"CLAUDE_CODE_SESSION_ID": SID, "CLAUDE_CONFIG_DIR": self.cc}
        self.tool, self.test = (os.path.join(self.repo, d) for d in ("tools/shout.py", "tests/test_shout.py"))

    def f(self, *a, **kw):
        return self.fm(*a, env=self.env, check=kw.pop("check", True), **kw)

    def write(self, path, text):
        with open(path, "w") as fh:
            fh.write(text)

    def search(self):
        self.f("which", "shout", check=False)

    def build(self, searched=True):
        if searched:
            self.search()
        self.f("new", "tool", "shout")

    def run_test(self):
        return self.f("task", "evidence", self.tid, "--step", "1", "--run", RUN, check=False)

    def red_green(self, body=TEST):
        self.run_test()  # the scaffold's own test fails until the tool works
        self.write(self.tool, TOOL)
        self.write(self.test, body)
        self.run_test()

    def transcript(self, *commands, when="2999-01-01T00:00:00.000Z"):
        d = os.path.join(self.cc, "projects", "x")
        os.makedirs(d, exist_ok=True)
        rows = []
        for i, cmd in enumerate(commands):
            rows.append({"type": "assistant", "timestamp": when, "message": {"content": [
                {"type": "tool_use", "id": f"t{i}", "name": "Bash", "input": {"command": cmd}}]}})
            rows.append({"type": "user", "timestamp": when, "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"t{i}", "is_error": False, "content": "ok"}]}})
        self.write(os.path.join(d, SID + ".jsonl"), "".join(json.dumps(r) + "\n" for r in rows))

    def finish(self):
        return self.f("task", "finish", self.tid, "--audit", "self", "--run", "true", check=False)

    def refused(self, *words):
        r = self.finish()
        out = r.stderr + r.stdout
        self.assertNotEqual(r.returncode, 0, out)
        for w in words:
            self.assertIn(PHRASE[w], out)
        self.assertEqual(c.find_brief(self.p, self.tid).status, "active")
        return out

    def proved(self):
        return c.ledger_events(self.p, ["tool_proved"])

    def test_all_four_close_it_and_log_tool_proved(self):
        self.build()
        self.red_green()
        self.transcript("python3 tools/shout.py hello")
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        (e,) = self.proved()
        self.assertEqual((e["task"], e["data"]["name"], e["data"]["path"]), (self.tid, "shout", self.tool))

    def test_a_task_that_built_nothing_gets_no_check(self):
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertEqual(self.proved(), [])

    def test_the_build_is_logged_with_the_task_the_files_and_the_need(self):
        self.build()
        (e,) = c.ledger_events(self.p, ["tool_built"])
        self.assertEqual((e["task"], e["data"]["path"], e["data"]["test"], e["data"]["name"]),
                         (self.tid, self.tool, self.test, "shout"))

    def test_no_search_receipt_before_the_build_is_refused_alone(self):
        self.build(searched=False)
        self.red_green()
        self.transcript("python3 tools/shout.py hello")
        out = self.refused("search")
        for other in ("stub", "red", "use"):
            self.assertNotIn(PHRASE[other], out)
        self.search()  # a search after the build is no receipt for it
        self.refused("search")
        self.assertEqual(self.proved(), [])

    def test_a_search_for_something_else_is_no_receipt(self):
        self.f("which", "zorblat frobnicate", check=False)
        self.build(searched=False)
        self.red_green()
        self.transcript("python3 tools/shout.py hello")
        self.refused("search")

    def test_a_test_never_seen_red_is_refused_alone(self):
        self.build()
        self.write(self.tool, TOOL)
        self.write(self.test, TEST)
        self.run_test()  # green the first time: nothing says it could fail
        self.transcript("python3 tools/shout.py hello")
        out = self.refused("red")
        for other in ("search", "stub", "use"):
            self.assertNotIn(PHRASE[other], out)

    def test_a_test_left_red_is_refused(self):
        self.build()
        self.run_test()
        self.transcript("python3 tools/shout.py hello")
        self.refused("red")

    def test_a_test_that_cannot_fail_on_a_stub_is_refused_alone(self):
        self.build()
        self.red_green(WEAK)
        self.transcript("python3 tools/shout.py hello")
        out = self.refused("stub")
        for other in ("search", "red", "use"):
            self.assertNotIn(PHRASE[other], out)

    def test_no_use_is_refused_alone_and_a_run_of_its_own_test_or_before_green_or_help_is_no_use(self):
        self.build()
        self.red_green()
        self.transcript()  # the session has a transcript and nothing in it ran the tool
        out = self.refused("use")
        self.transcript("python3 tests/test_shout.py", "python3 tools/shout.py --help", "echo shout.pyx")
        self.refused("use")
        self.transcript("python3 tools/shout.py hello", when="2000-01-01T00:00:00.000Z")
        self.refused("use")
        for other in ("search", "red", "stub"):
            self.assertNotIn(PHRASE[other], out)
        self.assertEqual(self.proved(), [])

    def test_every_missing_piece_is_named_in_one_refusal_and_no_typed_reason_replaces_one(self):
        self.build(searched=False)
        out = self.refused("search", "red")  # the use is judged only once a green run says when to look
        r = self.f("task", "evidence", self.tid, "--step", "1", "tool proved, trust me", "exit 0", check=False)
        self.assertEqual(r.returncode, 0, r.stderr)  # a typed line is evidence of the step, not of the tool
        self.refused("search", "red")
        self.assertIn("shout", out)

    def test_without_any_transcript_the_use_is_unproven_not_refused_and_not_marked_proved(self):
        self.build()
        self.red_green()
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertEqual(self.proved(), [])
        (e,) = c.ledger_events(self.p, ["tool_unproven"])
        self.assertEqual(e["data"]["path"], self.tool)

    def test_proving_resolves_a_miss_of_the_same_name(self):
        c.log_event(self.p, "capability_miss", task=self.tid, data={"name": "shout", "kind": "command",
                                                                    "cmd": "shout hi"})
        time.sleep(1.05)
        self.build()
        self.red_green()
        self.transcript("python3 tools/shout.py hello")
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def test_the_scaffolds_tests_fail_on_a_stub_and_pass_on_the_real_tool(self):
        self.build()
        self.write(self.tool, TOOL)
        self.write(self.test, TEST)
        self.assertIsNone(fmtoolproof.stub_problem(self.tool, self.test))
        self.write(self.test, WEAK)
        self.assertIn("stub", fmtoolproof.stub_problem(self.tool, self.test))
        self.write(self.test, "import sys\nsys.exit(3)\n")  # fails on the real one too: nothing to tell
        self.assertIn("real", fmtoolproof.stub_problem(self.tool, self.test))

    def test_a_generated_mcp_server_is_logged_and_its_test_fails_on_a_stub(self):
        d = os.path.join(self.tmp, "srv")
        self.f("mcp", "new", "gizmo", "--wrap", "echo", "--dir", d)
        (e,) = c.ledger_events(self.p, ["tool_built"])
        self.assertEqual((e["task"], e["data"]["name"], e["data"]["path"], e["data"]["test"]),
                         (self.tid, "gizmo", os.path.join(d, "server.py"), os.path.join(d, "test_server.py")))
        self.assertIsNone(fmtoolproof.stub_problem(e["data"]["path"], e["data"]["test"]))

    def test_a_stub_run_that_hangs_is_bounded(self):
        self.build()
        self.write(self.tool, TOOL)
        self.write(self.test, "import time\ntime.sleep(60)\n" + TEST)  # the real run hangs too: killed, no verdict
        t0 = time.monotonic()
        why = fmtoolproof.stub_problem(self.tool, self.test, seconds=1)
        self.assertLess(time.monotonic() - t0, 20)
        self.assertIn("timed out", why)
