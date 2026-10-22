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
