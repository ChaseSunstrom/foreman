"""T-0071 round B: how strongly work is verified — prove against the start tree, PERF numbers, CLEAN behaviour
locks, a verification grade, the sentinel, slow gates, the environment in cached passes, process-group kills."""
import json
import os
import subprocess
import time

from helpers import ForemanTestCase

import fmcore as c


class VerifyStrength(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def commit(self):
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "x"], check=True)

    def new(self, type_="FIX", *extra):
        self.fm("task", "new", "t", "--type", type_, "--tier", "S", "--step", "do it", "--ac", "works", *extra, "--focus")

    def test_prove_fails_on_the_start_tree_and_passes_now(self):
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        self.commit()
        self.new()
        self.write("calc.py", "def add(a, b):\n    return a + b\n")
        self.write("tests/test_calc.py", "import calc\nassert calc.add(2, 2) == 4\n")
        run = "PYTHONPATH=. python3 tests/test_calc.py"
        p = self.fm("task", "prove", "T-0001", "--run", run, "--step", "1")
        self.assertIn("proved", p.stdout)
        b = c.find_brief(self.p, "T-0001")
        self.assertTrue(b.red_green(), "both runs are recorded as fm runs of the same command")
        self.assertEqual(subprocess.run(["git", "-C", self.repo, "worktree", "list"], capture_output=True,
                                        text=True).stdout.count("\n"), 1, "the temporary worktree is removed")

    def test_prove_says_when_the_test_doesnt_test_the_change(self):
        self.write("calc.py", "X = 1\n")
        self.commit()
        self.new()
        self.write("tests/test_x.py", "assert True\n")
        p = self.fm("task", "prove", "T-0001", "--run", "python3 tests/test_x.py", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("passes without the change too", p.stdout)

    def test_prove_needs_a_changed_test(self):
        self.new()
        p = self.fm("task", "prove", "T-0001", "--run", "true", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("changed no test files", p.stderr)

    def finish_s(self):
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "true")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "audit", "T-0001", "self", "checked", "ok")
        return self.fm("task", "done", "T-0001", check=False)

    def test_perf_task_needs_before_after_numbers(self):
        self.new("PERFORMANCE")
        p = self.finish_s()
        self.assertIn("no before/after numbers", p.stderr)
        self.fm("task", "set", "T-0001", "--section", "Measurements", "--text", "p50: 120 ms → 40 ms (bench.py)")
        self.assertEqual(self.fm("task", "done", "T-0001", check=False).returncode, 0)

    def test_clean_task_needs_tests_run_before_its_first_edit(self):
        self.new("CLEAN")
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            f.write(json.dumps({"ts": "2000-01-01T00:00:00Z", "task": "T-0001", "event": "touched",
                                "data": {"file": os.path.join(self.repo, "a.py"), "tool": "Edit"}}) + "\n")
        p = self.finish_s()
        self.assertIn("no behaviour lock", p.stderr)
        self.fm("task", "set", "T-0001", "--section", "Behaviour lock", "--text", "none: docs-only rename")
        self.assertEqual(self.fm("task", "done", "T-0001", check=False).returncode, 0)

    def test_done_reports_a_verification_grade_and_records_files(self):
        self.new("FEATURE")
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            f.write(json.dumps({"ts": c.now(), "task": "T-0001", "event": "touched",
                                "data": {"file": os.path.join(self.repo, "a.py"), "tool": "Edit"}}) + "\n")
        p = self.finish_s()
        self.assertIn("verification: ok — 2 ran, 0 typed", p.stdout, "no independent lens or red→green: ok, not strong")
        b = c.find_brief(self.p, "T-0001")
        self.assertEqual(b.meta["verified"], "ok")
        self.assertIn("a.py", b.section("Files touched"))
        self.assertEqual(b.grade()[0], "ok")

    def test_sentinel_reruns_past_passing_checks(self):
        self.new("FEATURE")
        self.write("flag", "1")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "test -f flag")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "git push --dry-run || true")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "audit", "T-0001", "self", "checked", "ok")
        self.fm("task", "done", "T-0001")
        self.assertEqual(self.fm("sentinel").returncode, 0)
        os.remove(os.path.join(self.repo, "flag"))
        p = self.fm("sentinel", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("✗ T-0001: test -f flag", p.stdout)
        self.assertIn("1 with side effects skipped", p.stdout)

    def test_a_timed_out_check_kills_its_whole_process_group(self):
        marker = os.path.join(self.tmp, "orphan")
        start = time.time()
        code, out = c.run_command(self.repo, f"(sleep 3; touch {marker}) & sleep 30", timeout=1)
        self.assertEqual(code, 124)
        self.assertLess(time.time() - start, 8)
        time.sleep(3.5)
        self.assertFalse(os.path.exists(marker), "the background child was killed with the group")

    def test_cached_pass_depends_on_the_environment_and_slow_gates_are_named(self):
        self.fm("check", "add", "true")
        self.fm("check")
        self.assertIn("cached", self.fm("check").stdout)
        self.assertNotIn("cached", self.fm("check", env={"VIRTUAL_ENV": "/other"}).stdout)
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:
            for _ in range(3):
                f.write(json.dumps({"ts": c.now(), "event": "check_run", "data": {
                    "tree": "x", "results": [{"cmd": "sleep 3", "exit": 0, "s": 0.2}]}}) + "\n")
        self.fm("check", "rm", "1")
        self.fm("check", "add", "sleep 3")
        self.assertIn("slower: 3.", self.fm("check").stdout)
