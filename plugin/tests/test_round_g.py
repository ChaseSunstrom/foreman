"""T-0071 round G (super brainstorm 3): runs that prove nothing, weakened tests, dangling names, companion edits,
notes that re-arm after compaction, syntax notes, non-interactive git, gate hints and --fail-fast, fm pr, the CI
commands in the map, the starting context in fm cost."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c
import fmmap


class RoundG(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path) or self.repo, exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        return path

    def commit(self, msg="x"):
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)

    def test_a_green_run_of_zero_tests_counts_as_a_failure(self):
        code, out = c.run_command(self.repo, "echo 'Ran 0 tests in 0.000s'; echo OK")
        self.assertEqual(code, 5)
        self.assertIn("proves nothing", out)
        self.assertEqual(c.run_command(self.repo, "echo 'Ran 12 tests in 0.1s'")[0], 0)
        self.assertEqual(c.run_command(self.repo, "echo '=== no tests ran in 0.01s ==='")[0], 5)
        self.assertEqual(c.run_command(self.repo, "echo 'collected 0 items'; echo '=== 7 passed in 0.2s ==='")[0], 0,
                         "a multi-suite run where other tests ran is a real pass")

    def test_pre_audit_flags_weakened_tests_and_dangling_names(self):
        diff = ("diff --git a/tests/test_x.py b/tests/test_x.py\n--- a/tests/test_x.py\n+++ b/tests/test_x.py\n"
                "-    assert total([]) == 0\n-    assert total([1]) == 1\n+@unittest.skip('flaky')\n"
                "diff --git a/cart.py b/cart.py\n--- a/cart.py\n+++ b/cart.py\n-def compute_total(items):\n"
                "+def total(items):\n")
        self.write("api.py", "from cart import compute_total\n")
        found = "\n".join(fmmap.pre_audit(self.repo, diff, ["tests/test_x.py", "cart.py"]))
        self.assertIn("2 assertion(s) removed from tests/test_x.py", found)
        self.assertIn("test skipped or narrowed in tests/test_x.py", found)
        self.assertIn("removed compute_total is still named in api.py", found)

    def test_companion_edits_come_from_history(self):
        for i in range(3):
            self.write("schema.sql", f"-- v{i}\n")
            self.write("models.py", f"V = {i}\n")
            self.commit(f"v{i}")
        m = fmmap.load(self.p, rebuild=True)
        self.assertEqual(m["pairs"].get("schema.sql"), ["models.py"])
        found = "\n".join(fmmap.pre_audit(self.repo, "", ["schema.sql"], m))
        self.assertIn("schema.sql usually changes with models.py", found)

    def test_one_shot_notes_rearm_after_a_new_context(self):
        big = self.write("big.py", "x = 1\n" * 700)

        def read():
            return self.hook("PostToolUse", {"tool_name": "Read", "tool_input": {"file_path": big}}).stdout
        self.assertIn("fm outline", read())
        self.assertEqual(read(), "")
        self.hook("SessionStart", {"source": "compact"})
        self.assertIn("fm outline", read())

    def test_an_edit_that_breaks_syntax_is_said_at_once(self):
        path = self.write("broken.py", "def f(:\n    pass\n")
        out = self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path}}).stdout
        self.assertIn("broken.py:1: SyntaxError", out)
        path = self.write("conf.json", '{"a": 1,}')
        self.assertIn("not valid JSON", self.hook("PostToolUse", {"tool_name": "Write",
                                                                  "tool_input": {"file_path": path}}).stdout)
        jsonc = self.write("tsconfig.json", '{"compilerOptions": {}, // comments are fine here\n}')
        self.assertEqual(self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": jsonc}}).stdout, "")
        ok = self.write("fine.py", "x = 1\n")
        self.assertEqual(self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": ok}}).stdout, "")

    def test_check_suggests_gates_and_stops_early_when_asked(self):
        self.write("package.json", json.dumps({"scripts": {"test": "jest"}}))
        self.commit()
        self.assertIn("found in the project: npm run test", self.fm("check", check=False).stderr)
        self.fm("check", "add", "false")
        self.fm("check", "add", "true")
        data = self.fm_json("check", "--fail-fast", check=False)
        self.assertEqual([r["cmd"] for r in data["results"]], ["false"])

    def test_pr_description_from_the_brief(self):
        self.fm("task", "new", "empty carts total zero", "--type", "FIX", "--tier", "S", "--step", "s",
                "--ac", "total([]) is 0 :: true", "--focus")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "true")
        self.fm("task", "ac", "T-0001", "check", "1")
        out = self.fm("pr", "T-0001").stdout
        self.assertIn("## empty carts total zero", out)
        self.assertIn("- [x] total([]) is 0 — `true → exit 0", out)
        self.assertIn("Foreman task T-0001 (FIX S)", out)

    def test_map_lists_ci_commands(self):
        self.write(".github/workflows/ci.yml", "jobs:\n  t:\n    steps:\n      - uses: actions/checkout@v4\n"
                                               "      - run: python -m pytest -q\n      - run: ruff check .\n"
                                               "      - run: echo hi\n")
        self.commit()
        m = fmmap.load(self.p, rebuild=True)
        self.assertEqual(m["ci"], ["python -m pytest -q", "ruff check ."])
        self.assertIn("CI runs: python -m pytest -q", fmmap.render(m))

    def test_environment_failures_are_labelled(self):
        self.fm("check", "add", "python3 -c 'import no_such_module_xyz'")
        out = self.fm("check", check=False).stdout
        self.assertIn("environment: a module or tool is missing", out)

    def test_generated_files_are_flagged_on_edit_and_in_the_pre_audit(self):
        gen = self.write("api_pb2.py", "x = 1\n")
        hand = self.write("gen/models.py", "# Code generated by protoc. DO NOT EDIT.\nx = 1\n")
        out = self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": hand}}).stdout
        self.assertIn("looks generated or vendored", out)
        self.assertNotIn("generated", self.hook("PostToolUse", {"tool_name": "Edit",
                                                                "tool_input": {"file_path": hand}}).stdout)
        found = "\n".join(fmmap.pre_audit(self.repo, "", ["api_pb2.py", "README.md"]))
        self.assertIn("generated or vendored file edited: api_pb2.py", found)
        self.assertNotIn("README.md", found)
        self.assertTrue(os.path.exists(gen))

    def test_audit_scan_checks_any_branch_diff(self):
        self.write("app.py", "x = 1\n")
        self.commit("base")
        subprocess.run(["git", "-C", self.repo, "checkout", "-qb", "feature"], check=True)
        self.write("app.py", "x = 2\nbreakpoint()\n")
        self.commit("wip")
        p = self.fm("audit", "scan", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("debug leftover in app.py", p.stdout)
        self.assertEqual(self.fm("audit", "prep", check=False).returncode, 1)

    def test_git_never_prompts(self):
        env = subprocess.run(["bash", "-c", "true"], capture_output=True)  # the helper runs git with no terminal
        self.assertEqual(env.returncode, 0)
        self.assertEqual(c._git(self.repo, "config", "--get", "core.askpass"), "")
