"""T-1145: a verify that names a test module, script file or npm script that doesn't exist is refused when the
criterion is added or edited, with what is missing, instead of failing at evidence or finish time."""
import os
from helpers import ForemanTestCase


class VerifyCheck(ForemanTestCase):
    def put(self, rel, text=""):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def add(self, verify):
        self.fm("init", check=False)
        self.fm("task", "new", "x", "--type", "FIX", "--tier", "S", "--step", "s", "--focus", check=False)
        return self.fm("task", "ac", "T-0001", "add", "works", "--verify", verify, check=False)

    def test_missing_things_are_refused_naming_them(self):
        for verify, named in (("python3 tests/run.py test_nowhere_x", "test_nowhere_x"),
                              ("python3 -m unittest test_nowhere_x", "test_nowhere_x"),
                              ("python3 tools/nope.py", "tools/nope.py"),
                              ("bash scripts/nope.sh", "scripts/nope.sh"),
                              ("cd web && npm run lint", "lint")):
            with self.subTest(verify=verify):
                self.setUp()
                self.put("tests/run.py")
                self.put("web/package.json", '{"scripts": {"test": "x"}}')
                r = self.add(verify)
                self.assertNotEqual(r.returncode, 0)
                self.assertIn(named, r.stderr)

    def test_real_cd_and_unknown_pass(self):
        for verify in ("python3 tests/run.py test_real", "python3 -m unittest tests.test_real", "python3 tools/ok.py",
                       "cd web && npm test", "cd web && npm run lint", "cargo test nothing_x", "python3 -c 'pass'"):
            with self.subTest(verify=verify):
                self.setUp()
                self.put("tests/run.py")
                self.put("tests/test_real.py")
                self.put("tools/ok.py")
                self.put("web/package.json", '{"scripts": {"test": "x", "lint": "y"}}')
                r = self.add(verify)
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_task_new_ac_is_checked_too(self):
        self.fm("init")
        r = self.fm("task", "new", "x", "--type", "FIX", "--tier", "S", "--ac", "w :: python3 tools/nope.py",
                    "--step", "s", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("tools/nope.py", r.stderr)
