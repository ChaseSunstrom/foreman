"""fm task prove --hunks (T-0271): each code hunk of a task's diff is reverted alone and the check run; a hunk whose
removal still passes is unproven — the check doesn't test it."""
import json
import os
import subprocess

from helpers import ForemanTestCase

BEFORE = "def f():\n    return 1\n\n\nX = 0\n\n\ndef g():\n    return 1\n"
AFTER = "def f():\n    return 2\n\n\nX = 0\n\n\ndef g():\n    return 2\n"
CHECK = "python3 -c 'import calc; assert calc.f() == 2'"  # tests f only


class _Case(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.write("calc.py", BEFORE)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "calc"], check=True)
        self.tid = json.loads(self.fm("task", "new", "Return 2", "--type", "FIX", "--tier", "S", "--ac", "x :: true",
                                      "--step", "change it", "--json").stdout)["id"]
        self.fm("focus", self.tid)

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)


class Hunks(_Case):
    def test_the_untested_hunk_is_named(self):
        self.write("calc.py", AFTER)
        self.write("test_calc.py", "import calc\nassert calc.f() == 2\n")  # tests aren't mutated
        p = self.fm("task", "prove", self.tid, "--hunks", "--run", CHECK, "--json", check=False)
        res = json.loads(p.stdout)
        self.assertEqual((res["total"], res["proven"]), (2, 1))
        self.assertEqual([h["file"] for h in res["unproven"]], ["calc.py"])
        self.assertIn("return 2", res["unproven"][0]["text"])
        self.assertIn("def g", open(os.path.join(self.repo, "calc.py")).read())  # the working tree is untouched
        self.assertEqual(open(os.path.join(self.repo, "calc.py")).read(), AFTER)
        self.assertNotEqual(p.returncode, 0)

    def test_a_check_failing_anyway_proves_nothing(self):
        self.write("calc.py", AFTER)
        p = self.fm("task", "prove", self.tid, "--hunks", "--run", "false", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("unchanged tree", p.stderr)

    def test_spaces_and_deleted_files(self):
        self.write("my calc.py", "def h():\n    return 3\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "more"], check=True)
        self.fm("task", "drop", self.tid, "restart")
        tid = json.loads(self.fm("task", "new", "Again", "--type", "FIX", "--tier", "S", "--ac", "x :: true",
                                 "--step", "x", "--json").stdout)["id"]
        self.fm("focus", tid)
        self.write("my calc.py", "def h():\n    return 4\n")
        os.remove(os.path.join(self.repo, "calc.py"))
        res = json.loads(self.fm("task", "prove", tid, "--hunks", "--run",
                                 "python3 -c 'import importlib.util as u, sys; sys.exit(0)'", "--json", check=False).stdout)
        self.assertEqual(sorted(h["file"] for h in res["unproven"]), ["calc.py", "my calc.py"])
        self.assertEqual(res["skipped"], [])

    def test_nothing_to_prove(self):
        p = self.fm("task", "prove", self.tid, "--hunks", "--run", CHECK, check=False)
        self.assertIn("no code hunks", p.stdout + p.stderr)


class Evidence(_Case):
    def test_all_proven_passes_and_unproven_is_inconclusive(self):
        self.write("calc.py", BEFORE.replace("return 1\n\n\nX", "return 2\n\n\nX"))  # only f changes
        self.fm("task", "prove", self.tid, "--hunks", "--run", CHECK, "--step", "1")
        brief = self.fm("task", "show", self.tid).stdout
        self.assertIn("1/1 hunks proven", brief)
        self.write("calc.py", AFTER)
        self.fm("task", "prove", self.tid, "--hunks", "--run", CHECK, "--step", "1", check=False)
        brief = self.fm("task", "show", self.tid).stdout
        self.assertIn("1/2 hunks proven", brief)
        self.assertIn("[inconclusive]", brief)
        self.fm("task", "prove", self.tid, "--hunks", "--run", CHECK, "--step", "1", "--max", "1", check=False)
        last = [x for x in self.fm("task", "show", self.tid).stdout.splitlines() if "--max" in x][-1]
        self.assertIn("[inconclusive]", last)  # a cut-short run is never a pass


class Fallback(ForemanTestCase):
    """T-0297: in Foreman's own checkout, a mutation that crashes the hook falls back to HEAD's code — which in the
    proof worktree must be the task's base, not the unmutated tree, or the crash is masked."""

    def test_head_is_the_tasks_base_while_checks_run(self):
        self.fm("init")
        os.makedirs(os.path.join(self.repo, "plugin", "hooks"))
        with open(os.path.join(self.repo, "plugin", "hooks", "hook"), "w") as f:
            f.write("# Foreman's hook: def committed_library(): ...\n")
        with open(os.path.join(self.repo, "calc.py"), "w") as f:
            f.write(BEFORE)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "calc"], check=True)
        tid = json.loads(self.fm("task", "new", "Return 2", "--type", "FIX", "--tier", "S", "--ac", "x :: true",
                                 "--step", "change it", "--json").stdout)["id"]
        self.fm("focus", tid)
        with open(os.path.join(self.repo, "calc.py"), "w") as f:
            f.write(AFTER)
        log = os.path.join(self.tmp, "heads.log")
        check = (f"git rev-parse 'HEAD^{{tree}}' >> {log} && python3 -c 'import calc; "
                 f"assert calc.f() == 2 and calc.g() == 2'")
        res = json.loads(self.fm("task", "prove", tid, "--hunks", "--run", check, "--json", check=False).stdout)
        self.assertEqual((res["total"], res["proven"]), (2, 2))  # restores between hunks still work
        meta = json.loads(self.fm("task", "show", tid, "--json").stdout)["meta"]
        base_tree = subprocess.run(["git", "-C", self.repo, "rev-parse", f"{meta.get('base_tree') or meta['base']}^{{tree}}"],
                                   capture_output=True, text=True, check=True).stdout.strip()
        heads = set(open(log).read().split())
        self.assertEqual(heads, {base_tree})  # every check, baseline included, ran with HEAD at the base
