"""T-3185: an exported GIT_DIR must never steer the tests' git calls at a real repo.

At 02:54 on 2026-11-05 a test run inherited GIT_DIR and wrote core.bare=true and the fixture identity
t@example.com into the project's own .git/config; every merge into main then failed."""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LEAKY = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY")


class GitEnvIsolation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fm-gitenv-")
        self.real = os.path.join(self.tmp, "real")
        subprocess.run(["git", "init", "-q", self.real], check=True)

    def run_with(self, code):
        env = {**os.environ, "GIT_DIR": os.path.join(self.real, ".git"), "GIT_WORK_TREE": self.real,
               "PYTHONPATH": HERE}
        return subprocess.run([sys.executable, "-c", code], env=env, cwd=HERE, capture_output=True, text=True,
                              timeout=60)

    def real_config(self, key):
        return subprocess.run(["git", "-C", self.real, "config", "--local", "--get", key], capture_output=True,
                              text=True).stdout.strip()

    def test_importing_the_helpers_drops_every_variable_that_redirects_git(self):
        r = self.run_with("import os, helpers; print([k for k in %r if k in os.environ])" % (LEAKY,))
        self.assertEqual(r.stdout.strip(), "[]", r.stderr[-800:])

    def test_a_scratch_repo_made_under_an_exported_git_dir_leaves_the_real_repo_alone(self):
        r = self.run_with("import os, helpers; helpers.git_repo(%r)" % self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        self.assertEqual(self.real_config("user.email"), "")
        self.assertNotEqual(self.real_config("core.bare"), "true")


if __name__ == "__main__":
    unittest.main()
