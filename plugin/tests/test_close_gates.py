"""T-1117: Foreman keeps the suite green itself. A close runs the tests linked to what it changed and refuses a new
failure; a red full-gate run becomes one urgent baseline task; full runs start in the background after closes."""
import json
import os
import shutil
import subprocess
import unittest

from helpers import ForemanTestCase

import fmcore as c

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "def add(a, b):\n    return a + b\n"
TEST = ("import unittest\nimport sys, os\nsys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))\nimport calc\n\n\n"
        "class Calc(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(calc.add(1, 2), 3)\n")
OTHER = "import unittest\n\n\nclass Other(unittest.TestCase):\n    def test_other(self):\n        pass\n"


class CloseGates(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        os.makedirs(os.path.join(self.repo, "tests"))
        shutil.copy(os.path.join(HERE, "run.py"), os.path.join(self.repo, "tests", "run.py"))
        self.write("calc.py", SRC)
        self.write("tests/test_calc.py", TEST)
        self.write("tests/test_other.py", OTHER)
        self.write(".gitignore", "__pycache__/\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "suite"], check=True)
        self.fm("check", "add", "python3 tests/run.py")
        self.fm("check", "affected", "python3 tests/run.py {names}")
        self.p = c.find_project(self.repo)

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def task(self, title="Change add"):
        tid = self.fm_json("task", "new", title, "--type", "FEATURE", "--tier", "S", "--ac", "works :: true", "--step",
                           "s", "--scope", "calc.py")["id"]
        self.fm("focus", tid)
        return tid

    def finish(self, tid, *extra):
        return self.fm("task", "finish", tid, "--audit", "self", "--run", "true", *extra, check=False,
                       env={"FOREMAN_SENTINEL": "off"})

    def events(self, kind):
        return [e for e in c.ledger_events(self.p, (kind,))]

    def test_a_close_that_breaks_a_linked_test_is_refused(self):
        tid = self.task()
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        r = self.finish(tid)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("test_calc", r.stdout + r.stderr)
        self.assertNotEqual(c.find_brief(self.p, tid).status, "done")
        self.write("calc.py", SRC + "\n")
        r = self.finish(tid)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_a_failure_already_red_in_the_last_full_run_is_noted_not_refused(self):
        self.write("calc.py", "def add(a, b):\n    return a - b\n")  # broken before the task
        self.fm("check", check=False, env={"FOREMAN_SENTINEL": "off"})
        tid = self.task()
        self.write("calc.py", "def add(a, b):\n    return a - b  # still\n")
        r = self.finish(tid)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("already red", r.stdout + r.stderr)

    def test_a_red_full_run_captures_one_urgent_baseline_task(self):
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        out = self.fm("check", check=False).stdout
        base = [b for b in c.load_briefs(self.p) if b.meta.get("baseline")]
        self.assertEqual(len(base), 1, out)
        self.assertEqual(base[0].type, "FIX")
        self.assertEqual(base[0].priority, "urgent")
        self.assertIn("test_calc", base[0].title + base[0].section("Raw request"))
        self.assertIn(base[0].id, out)
        self.fm("check", check=False)
        self.assertEqual(len([b for b in c.load_briefs(self.p) if b.meta.get("baseline")]), 1, "once per failing set")
        self.write("calc.py", SRC)
        self.assertIn(f"baseline is green again: {base[0].id}", self.fm("check").stdout)

    def test_a_known_flake_is_not_a_baseline(self):
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        out = self.fm("check", check=False).stdout
        names = [n for r in self.events("check_run")[-1]["data"]["results"] for n in r.get("failing") or []]
        for b in c.load_briefs(self.p):
            if b.meta.get("baseline"):
                self.fm("task", "drop", b.id, "reset for the flake case")
        with open(os.path.join(self.p.dir, "flakes.json"), "w") as f:
            json.dump({"pending": {}, "flaky": {n: {"seen": 2} for n in names}}, f)
        self.fm("check", check=False)
        self.assertEqual([b for b in c.load_briefs(self.p) if b.meta.get("baseline") and b.status != "dropped"], [], out)

    def test_a_tasks_own_red_mid_work_is_not_a_baseline(self):
        # a task writing its failing test first runs fm check red: that's its work, not a broken baseline
        self.task()
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        self.fm("check", check=False)
        self.assertEqual([b for b in c.load_briefs(self.p) if b.meta.get("baseline")], [])

    def test_a_gate_that_names_no_failing_test_is_left_to_say_so_itself(self):
        self.fm("check", "add", "false")
        self.fm("check", check=False)
        self.assertEqual([b for b in c.load_briefs(self.p) if b.meta.get("baseline")], [])

    def test_a_close_is_not_judged_by_its_own_earlier_red_run(self):
        # review: the task's own red fm check was read as "the last full run", so its own break closed with a note
        tid = self.task()
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        self.fm("check", check=False, env={"FOREMAN_SENTINEL": "off"})
        r = self.finish(tid)
        self.assertNotEqual(r.returncode, 0, r.stdout)

    def test_a_flaky_linked_test_gets_one_rerun(self):
        tid = self.task()
        flag = os.path.join(self.repo, "once")
        self.write("tests/test_flaky.py", "import os, unittest\n\n\nclass F(unittest.TestCase):\n    def test_f(self):\n"
                   f"        if not os.path.exists({flag!r}):\n            open({flag!r}, 'w').close()\n"
                   "            self.fail('first run')\n")
        self.write("calc.py", SRC + "# touch\n")
        self.write(".gitignore", "__pycache__/\nonce\n")
        self.fm("task", "set", tid, "scope=calc.py,tests/test_flaky.py,.gitignore")
        r = self.finish(tid)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_json_output_stays_json(self):
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        self.fm("check", check=False, env={"FOREMAN_SENTINEL": "off"})
        tid = self.task()
        self.write("calc.py", "def add(a, b):\n    return a - b  # still\n")
        r = self.fm("task", "finish", tid, "--audit", "self", "--run", "true", "--json", check=False,
                    env={"FOREMAN_SENTINEL": "off"})
        json.loads(r.stdout)

    def test_a_sentinel_run_on_a_tree_edited_since_the_close_captures_nothing(self):
        tid = self.task()
        self.write("calc.py", SRC + "# tidy\n")
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true", env={"FOREMAN_SENTINEL": "off"})
        self.task("Next")
        self.write("calc.py", "def add(a, b):\n    return a - b\n")  # the next task's red-first edit
        self.fm("check", check=False, env={"FOREMAN_SENTINEL_RUN": "1", "FOREMAN_SENTINEL_TREE": "0" * 12})
        self.assertEqual([b for b in c.load_briefs(self.p) if b.meta.get("baseline")], [])

    def test_the_background_sentinel_runs_at_low_priority(self):
        # T-1463: started at full priority, it competed for CPU with the next task's foreground finish and tests
        import fmcli
        from unittest import mock
        started, real = [], fmcli.subprocess.Popen
        env = {k: v for k, v in os.environ.items() if k not in ("FOREMAN_SENTINEL", "FOREMAN_NO_BACKGROUND")}
        # subprocess is shared: only the sentinel's own start is faked, git and the rest run for real
        fake = lambda argv, **kw: (started.append(argv) or mock.Mock(pid=1)) if "sentinel" in argv else real(argv, **kw)
        with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(c, "host_strain", lambda: False), \
                mock.patch.object(fmcli.subprocess, "Popen", fake):
            self.assertEqual(fmcli._sentinel(self.p), "started")
        self.assertEqual(started[0][:3], ["nice", "-n", "10"])

    def test_only_one_sentinel_runs_at_a_time(self):
        import fmcli
        with open(os.path.join(self.p.dir, "sentinel.pid"), "w") as f:
            f.write(str(os.getpid()))  # a live run
        os.environ["FOREMAN_SENTINEL"] = "sync"
        try:
            self.assertIsNone(fmcli._sentinel(self.p))
        finally:
            del os.environ["FOREMAN_SENTINEL"]

    def test_a_file_its_scope_log_names_is_committed_with_it(self):
        # T-1122: a doc edited in the same command as the finish has no touched record yet; another task touched it
        # since this one's first focus, so the commit left it out though the task's own scope reason named it
        self.write("CHANGELOG.md", "# Changelog\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "changelog"], check=True)
        a = self.task()
        self.fm("checkpoint")
        b = self.task("Other")
        self.hook("PostToolUse", {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(self.repo, "CHANGELOG.md")},
                                  "tool_response": {}})
        self.fm("checkpoint")
        self.fm("focus", a)
        self.write("calc.py", SRC + "# a\n")
        self.write("CHANGELOG.md", "# Changelog\n- a\n")
        self.fm("task", "log", a, "scope: CHANGELOG.md — its release note")
        r = self.fm("task", "finish", a, "--audit", "self", "--run", "true", "--commit", "A", check=False,
                    env={"FOREMAN_SENTINEL": "off"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        shown = subprocess.run(["git", "-C", self.repo, "show", "--name-only", "--format=", "HEAD"], capture_output=True,
                               text=True).stdout.split()
        self.assertIn("CHANGELOG.md", shown, r.stdout)
        self.assertIn("calc.py", shown)

    def test_a_close_starts_a_full_run_when_the_last_one_is_old(self):
        tid = self.task()
        self.write("calc.py", SRC + "# tidy\n")
        before = len(self.events("check_run"))
        r = self.fm("task", "finish", tid, "--audit", "self", "--run", "true", check=False,
                    env={"FOREMAN_SENTINEL": "sync"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        runs = self.events("check_run")
        self.assertEqual(len(runs), before + 1, "no full run yet: one starts after the close")
        self.assertEqual({x["cmd"] for x in runs[-1]["data"]["results"]}, {"python3 tests/run.py"})
        tid = self.task("Again")
        self.write("calc.py", SRC + "# again\n")
        self.fm("task", "finish", tid, "--audit", "self", "--run", "true", env={"FOREMAN_SENTINEL": "sync"})
        self.assertEqual(len(self.events("check_run")), before + 1, "a fresh full run: none started")


if __name__ == "__main__":
    unittest.main()
