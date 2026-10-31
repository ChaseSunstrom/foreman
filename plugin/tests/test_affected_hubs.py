"""T-1467: a file that co-changes with many tests (CHANGELOG.md, edited by every task) carries no signal: its co-change
pairs ran ~28 test files on every close. A narrow pair (hooks.json and its wiring test) still runs."""
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


class AffectedHubs(ForemanTestCase):
    def commit(self, files, msg):
        for rel, body in files.items():
            os.makedirs(os.path.dirname(os.path.join(self.repo, rel)) or self.repo, exist_ok=True)
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write(body)
        for args in (["add", "-A"], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", msg]):
            subprocess.run(["git", "-C", self.repo, *args], check=True)

    def test_a_hub_file_brings_no_paired_tests_and_a_narrow_pair_still_does(self):
        import fmcli
        self.fm("init")
        self.fm("check", "affected", "python3 -m pytest -q {tests}")
        for i in range(3):  # every change also touched the changelog, as every task here does
            for n in range(12):
                self.commit({f"tests/test_part{n}.py": f"N = {i}\n", f"src/part{n}.py": f"N = {i}\n",
                             "CHANGELOG.md": f"# {i} {n}\n"}, f"part {n} round {i}")
            self.commit({"hooks/hooks.json": f'{{"n": {i}}}\n', "tests/test_wiring.py": f"N = {i}\n"}, f"wire {i}")
        self.fm("task", "new", "note it", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        with open(os.path.join(self.repo, "CHANGELOG.md"), "a") as f:
            f.write("- a line\n")
        p = c.find_project(self.repo, create=False)
        _, tests, _ = fmcli.affected(p)
        self.assertFalse([t for t in tests if "test_part" in t], tests)
        with open(os.path.join(self.repo, "hooks", "hooks.json"), "w") as f:
            f.write('{"n": 9}\n')
        _, tests, _ = fmcli.affected(p)
        self.assertIn("tests/test_wiring.py", tests)

    def test_a_hook_path_module_brings_test_core_for_its_import_budget(self):
        # T-2307: a new top-level import in fmhooks.py passed the lane and failed only at ship (T-2305)
        import fmcli
        self.fm("init")
        self.fm("check", "affected", "python3 -m pytest -q {tests}")
        self.commit({"plugin/lib/fmhooks.py": "N = 1\n", "plugin/lib/fmother.py": "N = 1\n",
                     "plugin/tests/test_core.py": "N = 1\n"}, "seed")
        self.fm("task", "new", "note it", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        p = c.find_project(self.repo, create=False)
        for rel, want in (("plugin/lib/fmother.py", False), ("plugin/lib/fmhooks.py", True), ("plugin/lib/fmcore.py", True)):
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write("N = 2\n")
            _, tests, _ = fmcli.affected(p)
            self.assertEqual("plugin/tests/test_core.py" in tests, want, (rel, tests))

    def test_a_hub_file_that_once_turned_the_gates_red_brings_the_test_it_broke(self):
        # T-2148: MASTER.md co-changes with every task, so no pair links it, yet an edit to it broke test_docs (T-2147)
        import fmcli
        self.fm("init")
        self.fm("check", "affected", "python3 -m pytest -q {tests}")
        for n in range(12):
            self.commit({f"tests/test_part{n}.py": "N = 1\n", f"src/part{n}.py": "N = 1\n", "MASTER.md": f"# {n}\n"},
                        f"part {n}")
        self.commit({"tests/test_docs.py": "def test_count():\n    open('MASTER.md')\n"}, "docs test")
        p = c.find_project(self.repo, create=False)
        fmcli._baseline(p, [("python3 -m pytest -q", 1, "FAILED tests/test_docs.py::test_count - AssertionError\n"
                             "==== 1 failed in 0.1s ====\n", None)])
        bid = next(b.id for b in c.load_briefs(p) if b.meta.get("baseline"))
        self.commit({"MASTER.md": "# fixed\n", "CHANGELOG.md": "- count\n"}, f"MASTER map table count ({bid})")
        self.commit({"src/count.py": "N = 3\n", "CHANGELOG.md": "- count fixed\n"}, f"count fix ({bid})")
        self.fm("task", "new", "note it", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        with open(os.path.join(self.repo, "MASTER.md"), "a") as f:
            f.write("- a line\n")
        _, tests, _ = fmcli.affected(p)
        self.assertNotIn("tests/test_docs.py", tests)  # the baseline task is still open: nothing learned yet
        fmcli.mutate(p, bid, lambda x: x.meta.update(status="done"), "test_done")  # its fix shipped
        self.commit({"src/other.py": "N = 2\n"}, "other")  # HEAD moves, so the map is rebuilt
        _, tests, _ = fmcli.affected(p)
        self.assertIn("tests/test_docs.py", tests)
        self.assertFalse([t for t in tests if "test_part" in t], tests)
        import fmmap
        broke = fmmap.load(p)["broke"]  # the code fix links; its changelog line, a record, doesn't
        self.assertEqual(broke.get("src/count.py"), ["tests/test_docs.py"], broke)
        self.assertNotIn("CHANGELOG.md", broke)
