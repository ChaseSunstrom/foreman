"""T-0071 round B: how strongly work is verified — prove against the start tree, PERF numbers, CLEAN behaviour
locks, a verification grade, the sentinel, slow gates, the environment in cached passes, process-group kills.
T-1518 (Repeat): repeated timed runs as evidence, the release canary's load flaps, a task receipt's reading order."""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from unittest import mock

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
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "do it", "--ac", "flag",
                "--ac", "pushed", "--focus")
        self.write("flag", "1")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "test -f flag")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "evidence", "T-0001", "--ac", "2", "--run", "git push --dry-run || true")
        self.fm("task", "ac", "T-0001", "check", "2")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "test -d .")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "audit", "T-0001", "self", "checked", "ok")
        self.fm("task", "done", "T-0001")
        self.assertEqual(self.fm("sentinel").returncode, 0)
        os.remove(os.path.join(self.repo, "flag"))
        p = self.fm("sentinel", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("✗ T-0001: test -f flag", p.stdout)
        self.assertIn("1 with side effects skipped", p.stdout)
        self.assertNotIn("test -d", p.stdout, "step evidence is work, not a declared check")

    def test_point_in_time_skipped_and_flake_rerun(self):
        # T-1380: release canaries failed on a release task's `git log origin/main …` check (true only until the next
        # release) and on suites that flaked under the canaries' side-by-side load, then passed
        self.write("flake.sh", "if [ -f once ]; then exit 0; fi\n: > once\nexit 1\n")
        self.write("once", "")
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--step", "do it", "--ac", "flaky",
                "--ac", "released", "--focus")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "sh flake.sh")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "evidence", "T-0001", "--ac", "2", "--run", "git rev-parse --verify -q origin/main || true")
        self.fm("task", "ac", "T-0001", "check", "2")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "test -d .")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "audit", "T-0001", "self", "checked", "ok")
        self.fm("task", "done", "T-0001")
        os.remove(os.path.join(self.repo, "once"))  # the next run fails once, then passes: a flake
        p = self.fm("sentinel", check=False)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("1 flaky", p.stdout)
        self.assertIn("1 point-in-time skipped", p.stdout)
        self.assertNotIn("origin/main", p.stdout)

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


# a stub fm for the canary: `projects` lists STUB_PROJECTS; `sentinel` fails in "broken" always, in "flappy" once
# (its marks in STUB_DIR)
CANARY_STUB = '''import json, os, sys
roots = json.loads(os.environ["STUB_PROJECTS"])
if sys.argv[1] == "projects":
    print(json.dumps({"projects": [{"project": k, "root": v, "exists": True} for k, v in roots.items()]}))
    sys.exit(0)
name = next(k for k, v in roots.items() if os.path.realpath(v) == os.path.realpath(os.getcwd()))
seen = os.path.join(os.environ["STUB_DIR"], name)
first = not os.path.exists(seen)
open(seen, "a").close()
if name == "broken" or (name == "flappy" and first):
    print("Sentinel: 1 past check(s); 1 failing now")
    sys.exit(1)
print("Sentinel: 1 past check(s); 0 failing now")
'''


class Repeat(ForemanTestCase):
    """T-1518: repeated timed runs as evidence (median and spread), the canary's load flaps, a receipt's reading order."""

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.fm("task", "new", "t", "--type", "PERFORMANCE", "--tier", "S", "--step", "do it", "--ac", "works", "--focus")

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def evidence(self):
        return c.find_brief(self.p, "T-0001").evidence()

    def test_repeat_records_median_and_spread(self):
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "sleep 0.2", "--repeat", "5")
        line = self.evidence()[-1]
        self.assertIn("` → exit 0 · ×5 runs: median ", line)
        m = re.search(r"median ([\d.]+)s, spread ±([\d.]+)s \(\d+%\), min ([\d.]+)s, max ([\d.]+)s", line)
        self.assertTrue(m, line)
        med, spread, lo, hi = map(float, m.groups())
        self.assertGreaterEqual(lo, 0.2, "each run sleeps 0.2 s: none is faster, however loaded the machine")
        self.assertTrue(lo <= med <= hi and spread <= hi - lo + 0.002, line)
        self.assertIn("median", p.stdout)

    def test_a_failing_run_among_the_repeats_fails_it_with_its_count(self):
        self.write("third.sh", 'n=$(cat n 2>/dev/null || echo 0); n=$((n+1)); echo $n > n; [ "$n" -ne 3 ]\n')
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "sh third.sh", "--repeat", "5", check=False)
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("` → ✗ exit 1 · ×5 runs, 1 failed: median ", self.evidence()[-1])
        with open(os.path.join(self.repo, "n")) as f:
            self.assertEqual(f.read().strip(), "5", "every run ran after the failure: the count is out of 5")

    def test_repeat_is_capped_and_bounded_in_time(self):
        for n in ("0", "51"):
            p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true", "--repeat", n, check=False)
            self.assertNotEqual(p.returncode, 0, p.stderr)
            self.assertIn("--repeat", p.stderr)
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "false", "--repeat", "3", "--expect-fail",
                    check=False)
        self.assertIn("--repeat", p.stderr)
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "true", "ok", "--repeat", "3", check=False)
        self.assertIn("--repeat", p.stderr)
        self.assertEqual(self.evidence(), [], "a refused --repeat records nothing")
        p = self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "sleep 5", "--repeat", "5", "--timeout", "1",
                    check=False)
        self.assertNotEqual(p.returncode, 0)
        line = self.evidence()[-1]
        self.assertIn("✗ exit 124", line)
        self.assertIn("×1 of 5 runs (--timeout reached), 1 failed: no run finished in time", line,
                      "--timeout bounds all the runs together; a timed-out run isn't a time")
        self.assertIn("timed out after 1s", line, "the user's --timeout, not what was left of it")

    def test_timed_out_runs_stay_out_of_the_numbers(self):
        import fmcli
        self.assertEqual(fmcli._repeat_runs(self.repo, "true", 3, 0)[:2], (124, "timed out before the first run"))
        self.write("slow.sh", "if [ -f once ]; then sleep 5; fi; : > once\n")
        code, output, timing = fmcli._repeat_runs(self.repo, "sh slow.sh", 3, 3)
        self.assertEqual(code, 124, output)
        self.assertIn("timed out after 3s", output, "the user's --timeout, not what was left of it")
        self.assertIn("×2 of 3 runs (--timeout reached), 1 failed: median ", timing)
        self.assertIn("spread n/a", timing, "one finished run has no spread")

    def canary(self, load, **patches):
        """The canary's report over four projects: flappy (this repo) fails once, broken always, gone can't run, fine
        passes; the host's load stands at `load` on 8 CPUs."""
        import fmrelease
        stub = os.path.join(self.tmp, "fmstub.py")
        with open(stub, "w") as f:
            f.write(CANARY_STUB)
        roots = {"flappy": self.repo, **{k: os.path.join(self.tmp, k) for k in ("broken", "gone", "fine")}}
        for k in ("broken", "fine"):
            os.makedirs(roots[k], exist_ok=True)
        env = {"STUB_PROJECTS": json.dumps(roots), "STUB_DIR": tempfile.mkdtemp(dir=self.tmp),
               "FOREMAN_HOST": f"load={load},cpus=8"}
        out = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.multiple(fmrelease, FM=[sys.executable, stub], **patches))
            stack.enter_context(mock.patch.dict(os.environ, env))
            stack.enter_context(contextlib.redirect_stdout(out))
            fmrelease._canary_worker("9.9.9", self.repo)
        return out.getvalue()

    def test_the_canary_calls_a_failure_under_load_that_passes_alone_a_load_flap(self):
        report = self.canary(40)
        flap = next((x for x in report.splitlines() if x.strip().startswith("~ flappy")), "")
        self.assertIn("load flap", flap, report)
        self.assertIn("1 failing now", flap, "the failing result is kept beside the passing one")
        self.assertIn("0 failing now", flap)
        self.assertIn("load 40.0 on 8 CPUs", flap, "each result with the load it ran under")
        self.assertRegex(report, r"✗ broken: .*alone", "a failure that fails alone too stays a failure")
        self.assertNotRegex(report, r"gone: .*alone", "a sentinel that couldn't run isn't rerun")
        self.assertIn("✓ fine", report)
        self.assertIn("canary done: 2 of 4 project(s) failing, 1 load flap(s): flappy", report)
        titles = [b.title for b in c.load_briefs(self.p)]
        self.assertTrue(any("load flap" in t and "flappy" in t for t in titles), titles)  # an intermittent regression

    def test_a_failure_on_a_quiet_host_stays_a_failure_and_reruns_have_a_time_budget(self):
        report = self.canary(0.5)
        self.assertNotIn("~ flappy", report, "a quiet host: no load flap, and no rerun to call one")
        self.assertNotIn("alone", report)
        self.assertIn("canary done: 3 of 4 project(s) failing\n", report)
        titles = [b.title for b in c.load_briefs(self.p)]
        self.assertTrue(any(t.startswith("Canary after Foreman 9.9.9") and "flappy" in t for t in titles), titles)
        report = self.canary(40, RERUN_S=0)
        self.assertIn("no rerun for flappy, broken", report)
        self.assertIn("canary done: 3 of 4 project(s) failing\n", report)

    def test_a_ui_tasks_receipt_lists_files_in_reading_order(self):
        files = {"README.md": "# app\n\nA button.\n", "tests/test_button.py": "import Button\n",
                 "src/App.tsx": "import Button from './Button'\n", "src/Button.tsx": "import {get} from './client'\n",
                 "src/theme.css": "a { color: red }\n", "src/client.ts": "export const get = 1\n"}
        for rel, text in files.items():
            self.write(rel, text)
        self.fm("task", "set", "T-0001", "--section", "Measurements", "--text", "p50: 120 ms → 40 ms (bench.py)")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true", "--repeat", "2")
        d = self.fm_json("task", "receipt", "T-0001")
        order = ["src/client.ts", "src/theme.css", "src/Button.tsx", "src/App.tsx", "tests/test_button.py", "README.md"]
        self.assertEqual([f["path"] for f in d["files"]], order, "what it builds on, styles, components, the entry "
                                                                 "point, tests, docs")
        self.assertEqual([f["path"] for f in d["files"] if f["ui"]], order[1:4])
        text = self.fm("task", "receipt", "T-0001").stdout
        self.assertLess(text.index("src/theme.css"), text.index("tests/test_button.py"))
        self.assertIn("src/Button.tsx  +1 −0  [UI]", text)
        self.assertIn("120 ms → 40 ms", text, "the before/after numbers")
        self.assertRegex(text, r"`true`: ×2 runs: median [\d.]+s", "and the --repeat medians")
        self.assertIn("×2 runs: median", d["before_after"])
