"""T-3185: an exported GIT_DIR must never steer the tests' git calls at a real repo.

At 02:54 on 2026-11-05 a test run inherited GIT_DIR and wrote core.bare=true and the fixture identity
t@example.com into the project's own .git/config; every merge into main then failed."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

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


class ScratchRepoCost(unittest.TestCase):
    """T-3581: every test's scratch repo cost 5 git processes (init, 2x config, add, commit), ~35,000 a suite."""

    def setUp(self):
        sys.path.insert(0, HERE)
        import helpers
        self.helpers, self.tmp = helpers, tempfile.mkdtemp(prefix="fm-repocost-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def git(self, root, *a):
        return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)

    def test_a_repo_after_the_processes_first_costs_one_git_process(self):
        self.helpers.git_repo(self.tmp, "warm")
        with mock.patch.object(subprocess, "run", wraps=subprocess.run) as run:
            self.helpers.git_repo(self.tmp, "app")
        self.assertEqual(run.call_count, 1, run.call_args_list)

    def test_each_repo_reads_clean_and_makes_its_own_init_commit_when_called(self):
        self.helpers.git_repo(self.tmp, "warm")
        with mock.patch.dict(os.environ, {"GIT_COMMITTER_DATE": "@1000000000 +0000"}):
            root = self.helpers.git_repo(self.tmp, "app")
        self.assertEqual(self.git(root, "log", "--format=%ct %ae %an %s").stdout.split("\n")[0],
                         "1000000000 t@example.com t init")
        self.assertEqual(self.git(root, "rev-list", "--count", "HEAD").stdout.strip(), "1")
        self.assertEqual(self.git(root, "branch", "--show-current").stdout.strip(), "main")
        self.assertEqual(self.git(root, "config", "user.email").stdout.strip(), "t@example.com")
        self.assertEqual(self.git(root, "diff-files", "--quiet").returncode, 0, "a copied index reads dirty")
        self.assertEqual(self.git(root, "diff-index", "--quiet", "HEAD").returncode, 0)
        self.assertEqual(self.git(root, "status", "--porcelain").stdout, "")
        with open(os.path.join(root, "README.md"), "w") as f:
            f.write("# APP\n")  # same size, same second: still seen
        self.assertEqual(self.git(root, "diff-files", "--name-only").stdout.strip(), "README.md")
        with open(os.path.join(self.tmp, "warm", "README.md")) as f:
            self.assertEqual(f.read(), "# app\n", "an edit in one repo reached another")


class GateKeyIsolation(unittest.TestCase):
    def test_an_in_process_gate_signs_with_the_tests_own_key_not_the_users(self):
        # T-3195: test_lanes.SelfChangeGate read the real ~/.config/sampo/selfgate.key
        sys.path.insert(0, HERE)
        from helpers import SampoTestCase
        from sampo import selfgate

        class T(SampoTestCase):
            def runTest(self):
                pass
        t = T()
        t.setUp()
        try:
            self.assertTrue(selfgate._keyfile().startswith(t.tmp + os.sep), selfgate._keyfile())
        finally:
            t.doCleanups()
            t.tearDown()


if __name__ == "__main__":
    unittest.main()
