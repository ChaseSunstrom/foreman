"""T-3502: run.py skips a class already green at the same code, reruns 1 in 10 of those anyway and drops the cache
when one fails; the full gate, -k runs, nested runs and FOREMAN_NO_TEST_CACHE=1 never skip. T-3593: "the same code" is
what the class read when it passed: runcover.py records every file its processes open or run, every folder they list,
and the whole tree when a child escapes it; a change outside those skips the class, a class with no record runs."""
import contextlib
import io
import json
import re
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))
import run  # noqa: E402
import runcover  # noqa: E402

NESTED = ("SAMPO_SLOT", "FOREMAN_SLOT", "SAMPO_SLOTS", "FOREMAN_SLOTS", "SAMPO_NO_TEST_CACHE", "FOREMAN_NO_TEST_CACHE",
          "SAMPO_CACHE_FULL", "FOREMAN_CACHE_FULL")  # T-3638: a verify's opt-in in the caller's env must not skip a plain run


def outer(**extra):
    """This environment as a run.py started from a shell sees it: not inside a class's CPU slot, cache not switched off."""
    return dict({k: v for k, v in os.environ.items() if k not in NESTED}, **extra)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout


def scratch(d, files):
    """A git repo in d holding files ({path: text}), all committed."""
    for path, text in files.items():
        os.makedirs(os.path.dirname(os.path.join(d, path)), exist_ok=True)
        with open(os.path.join(d, path), "w") as f:
            f.write(text)
    git(d, "init", "-q", "-b", "main")
    git(d, "-c", "user.email=t@example.com", "-c", "user.name=t", "add", ".")
    git(d, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qm", "init")
    return d


TEST = "import unittest\nclass C(unittest.TestCase):\n    def test_x(self):\n        pass\n"


class Coverage(unittest.TestCase):
    """T-3593: what a class's recorded lines count as, and which changes touch them."""

    def setUp(self):
        self.d = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)
        scratch(self.d, {
            ".gitignore": "state/\n",
            "plugin/tests/run.py": "# the runner\n",
            "plugin/tests/helpers.py": "X = 1\n",
            "plugin/tests/runcover.py": "# the recorder\n",
            "plugin/tests/test_a.py": TEST,
            "plugin/tests/fixtures/data.txt": "x\n",
            "plugin/lib/mod.py": "X = 1\n",
            "docs/guide.md": "words\n",
            ".sampo/tasks/T-1.md": "state\n",
        })
        os.makedirs(os.path.join(self.d, "state"))
        open(os.path.join(self.d, "state", "x.json"), "w").close()
        self.here = os.path.join(self.d, "plugin", "tests")

    def tree(self):
        with mock.patch.object(run, "HERE", self.here):
            got = run.tree()
        self.assertEqual(got[0], self.d)
        return got

    def edit(self, path, text="changed\n"):
        os.makedirs(os.path.dirname(os.path.join(self.d, path)), exist_ok=True)
        with open(os.path.join(self.d, path), "a") as f:
            f.write(text)

    def test_a_file_whose_name_is_not_utf8_is_hashed_and_saved(self):  # T-3651: the 05:20 ship crashed in digest()
        bad = os.fsdecode(b"bad\xff.txt")  # Python holds the stray byte as the surrogate '\udcff'
        with open(os.path.join(self.d, bad), "w") as f:
            f.write("x\n")
        blobs = self.tree()[1]
        self.assertIn(bad, blobs)
        paths = sorted([bad, "./", "*", "?" + bad])
        d = run.digest(paths, run.values(blobs))
        self.assertEqual(d, run.digest(paths, run.values(blobs)))
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "c.json")
            run.save_cache(p, {"m.C": [d, 1, paths]}, 0)
            self.assertEqual(run.load_cache(p), (0, {"m.C": [[d, 1, paths]]}))

    def changes(self, paths, edit):
        """Whether edit() changes the digest of what a class that read paths depends on."""
        before = run.digest(sorted(paths), run.values(self.tree()[1]))
        edit()
        return before != run.digest(sorted(paths), run.values(self.tree()[1]))

    def test_recorded_lines_name_files_modules_folders_and_the_whole_tree(self):
        d, tag = self.d, sys.implementation.cache_tag
        text = "\n".join([f"f {d}/plugin/lib/mod.py", f"f {d}/plugin/lib/__pycache__/mod.{tag}.pyc",
                          f"f {d}/plugin/tests/fixtures/data.txt", f"d {d}/plugin/tests/fixtures", f"d {d}", "*",
                          "f /usr/lib/python3/os.py",  # outside the repo
                          f"f {d}/.git/HEAD", f"f {d}/state/x.json",  # on disk, but git doesn't see them
                          f"f {d}/.sampo/tasks/T-1.md", f"d {d}/.sampo/tasks",  # Sampo's task state: no test reads it
                          f"f {d}/plugin/lib/gone.py"])  # missing: creating it reruns
        with mock.patch.object(run, "HERE", self.here):
            got = run.covered(text, d, self.tree()[1])
        self.assertEqual(got, {"plugin/lib/mod.py", "plugin/tests/fixtures/data.txt", "plugin/tests/fixtures/", "./",
                               "*", "plugin/lib/gone.py"})

    def test_a_change_touches_only_the_classes_that_read_it(self):
        reads = ["plugin/lib/mod.py", "plugin/tests/test_a.py"]
        self.assertFalse(self.changes(reads, lambda: self.edit("docs/guide.md")))
        self.assertFalse(self.changes(reads, lambda: self.edit("plugin/lib/new.py")), "a new file nobody read")
        self.assertTrue(self.changes(reads, lambda: self.edit("plugin/lib/mod.py")))
        self.assertTrue(self.changes(reads, lambda: self.edit("plugin/tests/test_a.py", "# note\n")))
        self.assertTrue(self.changes(reads, lambda: os.remove(os.path.join(self.d, "plugin", "lib", "mod.py"))))

    def test_a_listed_folder_changes_with_its_names_and_a_missing_file_once_it_exists(self):
        self.assertFalse(self.changes(["plugin/tests/fixtures/"], lambda: self.edit("plugin/tests/fixtures/data.txt")))
        self.assertTrue(self.changes(["plugin/tests/fixtures/"], lambda: self.edit("plugin/tests/fixtures/new.txt")))
        self.assertTrue(self.changes(["./"], lambda: self.edit("top.md")))
        self.assertTrue(self.changes(["plugin/lib/gone.py"], lambda: self.edit("plugin/lib/gone.py")))

    def test_the_whole_tree_changes_with_any_file_but_sampo_s_task_state(self):
        self.assertTrue(self.changes(["*"], lambda: self.edit("docs/guide.md")))
        self.assertFalse(self.changes(["*", "./"], lambda: self.edit(".sampo/tasks/T-1.md")))

    def test_a_file_s_mode_counts_committed_or_not(self):  # review: test_docs checks os.access(hook, X_OK)
        hook = os.path.join(self.d, "plugin", "tests", "run.py")
        self.assertTrue(self.changes(["plugin/tests/run.py"], lambda: os.chmod(hook, 0o755)))
        git(self.d, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qam", "x")
        self.assertTrue(self.changes(["plugin/tests/run.py"], lambda: os.chmod(hook, 0o644)))
        self.edit("plugin/lib/new.py")
        new = os.path.join(self.d, "plugin", "lib", "new.py")
        self.assertTrue(self.changes(["plugin/lib/new.py"], lambda: os.chmod(new, 0o755)), "an untracked file's mode too")

    def test_git_s_head_and_tags_count_only_for_a_class_that_ran_git_on_the_repo(self):  # review
        commit = ["-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "x"]
        self.assertTrue(self.changes([run.GIT_STATE], lambda: git(self.d, *commit)))
        self.assertTrue(self.changes([run.GIT_STATE], lambda: git(self.d, "tag", "v1")))
        self.assertTrue(self.changes([run.GIT_STATE], lambda: git(self.d, "checkout", "-q", "-b", "side")))
        self.assertFalse(self.changes([run.GIT_STATE], lambda: git(self.d, "branch", "lane")),
                         "another lane's branch moving: every lane commit would rerun it")
        self.assertFalse(self.changes(["*", "plugin/lib/mod.py", "./", "plugin/"], lambda: git(self.d, *commit)),
                         "a whole-tree record keys on the files alone")
        with mock.patch.object(run, "HERE", self.here):
            got = run.covered("g\n*\n", self.d, self.tree()[1])
        self.assertEqual(got, {run.GIT_STATE, "*"})

    def test_what_a_stat_saw_counts(self):  # review: os.path.exists(skills/x/references/y.md) fires no audit event
        d, tag = self.d, sys.implementation.cache_tag  # noqa: F841
        text = "\n".join([f"s {d}/plugin/lib/mod.py", f"s {d}/plugin/tests/fixtures", f"s {d}/plugin/lib/gone.py",
                          f"s {d}/state/x.json"])
        with mock.patch.object(run, "HERE", self.here):
            got = run.covered(text, d, self.tree()[1])
        self.assertEqual(got, {"plugin/lib/mod.py", "?plugin/tests/fixtures", "?plugin/lib/gone.py", "?state/x.json"})
        self.assertTrue(self.changes(["?plugin/lib/gone.py"], lambda: self.edit("plugin/lib/gone.py")), "appears")
        self.assertTrue(self.changes(["?docs/guide.md"], lambda: os.remove(os.path.join(d, "docs", "guide.md"))), "goes")
        self.assertFalse(self.changes(["?plugin/tests/fixtures"], lambda: self.edit("plugin/tests/fixtures/data.txt")),
                         "a folder that still exists")
        self.assertTrue(self.changes(["?plugin/tests/fixtures"],
                                     lambda: shutil.rmtree(os.path.join(d, "plugin", "tests", "fixtures"))))

    def test_run_py_and_the_helpers_beside_it_are_every_class_s(self):
        with mock.patch.object(run, "HERE", self.here):
            self.assertEqual(run.shared(*self.tree()[:2]),
                             {"plugin/tests/run.py", "plugin/tests/helpers.py", "plugin/tests/runcover.py"})

    def test_blobs_are_git_hashes_of_the_files_on_disk_untracked_ones_too(self):
        self.edit("plugin/lib/mod.py")
        self.edit("plugin/lib/new.py", "Y = 2\n")
        _, blobs, _ = self.tree()
        for path in ("plugin/lib/mod.py", "plugin/lib/new.py", "docs/guide.md"):
            self.assertEqual(blobs[path], "100644 " + git(self.d, "hash-object", path).strip(), path)
        os.remove(os.path.join(self.d, "docs", "guide.md"))
        self.assertNotIn("docs/guide.md", self.tree()[1], "a deleted file isn't hashed")

    def test_every_worktree_of_a_repo_shares_one_cache(self):
        wt = os.path.join(os.path.realpath(tempfile.mkdtemp()), "lane")
        self.addCleanup(shutil.rmtree, os.path.dirname(wt), True)
        git(self.d, "worktree", "add", "-q", "--detach", wt)
        with mock.patch.object(run, "HERE", os.path.join(wt, "plugin", "tests")):
            lane = run.tree()
        self.assertEqual(lane[0], wt)
        self.assertEqual(lane[2], self.tree()[2])

    def test_outside_git_there_is_no_tree(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(run, "HERE", d):
            self.assertIsNone(run.tree())


class Recorder(unittest.TestCase):
    """T-3593: runcover.py in cover_python's venv: what a process and its children record."""

    @classmethod
    def setUpClass(cls):
        cls.d = os.path.realpath(tempfile.mkdtemp())
        scratch(cls.d, {"lib/mod_a.py": "A = 1\n", "lib/mod_b.py": "B = 1\n", "data.txt": "x\n", "folder/f.txt": "y\n",
                        "bin/tool": "#!/bin/sh\ntrue\n", "bin/sleep": "#!/bin/sh\ntrue\n",
                        "bin/pytool": "#!/usr/bin/env python3\nimport sys\nsys.path.insert(0, '.')\nimport mod_b\n"})
        for name in ("tool", "pytool", "sleep"):
            os.chmod(os.path.join(cls.d, "bin", name), 0o755)
        cls.cache = os.path.realpath(tempfile.mkdtemp())
        with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": cls.cache}):
            cls.py = run.cover_python()
        cls.blobs = dict.fromkeys(git(cls.d, "ls-files").split(), "blob")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, True)
        shutil.rmtree(cls.cache, True)

    def record(self, code):
        """What a script in the repo running `code` (and its children) recorded, as covered() reads it."""
        out = os.path.join(tempfile.mkdtemp(), "cover")
        self.addCleanup(shutil.rmtree, os.path.dirname(out), True)
        with open(os.path.join(self.d, "probe.py"), "w") as f:
            f.write("import os, subprocess, sys, tempfile\nsys.path.insert(0, 'lib')\n" + code)
        subprocess.run([self.py, "probe.py"], cwd=self.d, check=True, timeout=120, capture_output=True,
                       env=dict(os.environ, RUNPY_COVER=out, RUNPY_COVER_ROOTS=os.pathsep.join(run._roots(self.d))))
        with open(out) as f:
            return run.covered(f.read(), self.d, self.blobs)

    def test_the_venv_python_is_this_python_with_the_recorder_outside_tmp_and_made_once(self):
        self.assertIsNotNone(self.py)
        r = subprocess.run([self.py, "-c", "import sys, runcover; print(sys.version, runcover.PY)"], capture_output=True,
                           text=True, check=True)
        self.assertEqual(r.stdout.split(), [*sys.version.split(), self.py])
        self.assertTrue(self.py.startswith(os.path.join(self.cache, "sampo", "run-py", "")), "a job sandbox hides /tmp")
        stale = os.path.join(self.cache, "sampo", "run-py", "0ld")
        os.makedirs(stale)
        os.utime(stale, (1, 1))
        with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": self.cache}):
            self.assertEqual(run.cover_python(), self.py)
        self.assertEqual(os.listdir(os.path.dirname(stale)), [os.path.basename(os.path.dirname(os.path.dirname(self.py)))],
                         "one venv, and one no run used for weeks is gone")

    def test_a_cleared_environment_or_closed_descriptors_lose_nothing_and_write_nowhere_else(self):
        got = self.record("os.environ.clear()\nimport mod_a\n")
        self.assertIn("lib/mod_a.py", got)
        mine = os.path.join(tempfile.mkdtemp(), "mine")
        self.addCleanup(shutil.rmtree, os.path.dirname(mine), True)
        got = self.record(f"open('data.txt').read()\nos.closerange(3, 4096)\nfd = os.open({mine!r}, os.O_CREAT | os.O_WRONLY)\n"
                          "import mod_b\nos.close(fd)\n")
        self.assertIn("lib/mod_b.py", got)
        with open(mine) as f:
            self.assertEqual(f.read(), "", "a reused descriptor number is never written to")

    def test_modules_files_folders_and_a_child_python_s_reads(self):
        got = self.record("import mod_a\nopen('data.txt').read()\nos.listdir('folder')\n"
                          "subprocess.run([sys.executable, '-c', 'import mod_b'], cwd='lib', check=True)\n")
        self.assertLessEqual({"lib/mod_a.py", "data.txt", "folder/", "lib/mod_b.py"}, got)
        self.assertNotIn("*", got)

    def test_what_it_only_stats_exists_or_accesses(self):
        got = self.record("os.path.exists('missing.txt')\nos.path.isdir('folder')\nos.access('data.txt', os.X_OK)\n"
                          "os.stat('lib/mod_a.py')\nos.lstat('lib/mod_b.py')\n")
        self.assertLessEqual({"?missing.txt", "?folder", "data.txt", "lib/mod_a.py", "lib/mod_b.py"}, got)
        r = subprocess.run([self.py, "-c", "import os, shutil; print(shutil._use_fd_functions, os.stat in os.supports_fd,"
                            " os.stat in os.supports_dir_fd, os.lstat in os.supports_dir_fd)"],
                           capture_output=True, text=True, check=True, env=dict(os.environ, RUNPY_COVER=os.devnull))
        self.assertEqual(r.stdout.split(), ["True"] * 4, "rmtree keeps its fd-based, symlink-safe walk")

    def test_a_forked_child_s_reads_and_one_that_execs_this_python(self):
        got = self.record("pid = os.fork()\nif pid == 0:\n    import mod_b\n    os._exit(0)\nos.waitpid(pid, 0)\n")
        self.assertIn("lib/mod_b.py", got)
        got = self.record("pid = os.fork()\nif pid == 0:\n    os.chdir('lib')\n"
                          "    os.execv(sys.executable, [sys.executable, '-c', 'import mod_b'])\nos.waitpid(pid, 0)\n")
        self.assertIn("lib/mod_b.py", got)
        self.assertNotIn("*", got)

    def test_a_child_it_cant_follow_is_the_whole_tree(self):
        for code in ("subprocess.run([os.path.realpath(sys.executable), '-c', 'pass'])",  # a python without the hook
                     "subprocess.run([sys.executable, '-S', '-c', 'pass'])",  # no site: no .pth
                     "subprocess.run([sys.executable, '-X', 'utf8', '-Sc', 'pass'])",
                     "subprocess.run([sys.executable, '-c', 'pass'], env={'PATH': os.environ['PATH']})",  # no file
                     "subprocess.run(['git', '-C', 'lib', 'log'], capture_output=True)",
                     "subprocess.run(['cat', 'data.txt'], capture_output=True)",  # a program given a repo path
                     "subprocess.run('cat data.txt', shell=True, capture_output=True)",
                     "subprocess.run('python3 -c pass', shell=True)",  # a python the shell finds
                     "subprocess.run(['tool'], env=dict(os.environ, PATH='bin' + os.pathsep + os.environ['PATH']))",
                     "subprocess.run(['ls'], capture_output=True)",  # works in the repo: reads it by its folder
                     "subprocess.run(['env', 'python3', '-c', 'pass'], cwd=tempfile.mkdtemp())",  # another python
                     "subprocess.run([sys.executable, '-c', 'pass'], env=dict(os.environ, RUNPY_COVER=os.devnull))",
                     "os.system('true')"):
            with self.subTest(code):
                self.assertIn("*", self.record(code + "\n"))

    def test_a_python_found_on_path_a_python_script_and_a_wrapper_of_this_python_are_followed(self):
        venv = "env=dict(os.environ, PATH=os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH'])"
        for code in (f"subprocess.run(['python3', '-c', 'import mod_b'], cwd='lib', check=True, {venv})",
                     "subprocess.run('python3 -c \"import mod_b\"', shell=True, cwd=tempfile.mkdtemp(), check=True, "
                     "env=dict(os.environ, PYTHONPATH=os.path.abspath('lib'),"  # a gate's command line, in a scratch project
                     " PATH=os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH']))",
                     f"subprocess.run([os.path.abspath('bin/pytool')], cwd='lib', check=True, {venv})",  # fm, the hook
                     "subprocess.run(['env', sys.executable, '-c', 'import mod_b'], cwd='lib', check=True)",
                     "t = tempfile.mkdtemp()\nos.symlink(sys.executable, os.path.join(t, 'claude'))\n"  # a stand-in
                     "subprocess.run([os.path.join(t, 'claude'), '-c', 'import subprocess, sys; subprocess.run(sys.argv[1:])',"
                     " sys.executable, '-c', 'import mod_b'], cwd='lib', check=True)"):
            with self.subTest(code):
                got = self.record(code + "\n")
                self.assertIn("lib/mod_b.py", got)
                self.assertNotIn("*", got)
        self.assertIn("*", self.record("subprocess.run([os.path.abspath('bin/pytool')], cwd='lib')\n"),
                      "its #! python, found on this PATH, isn't this venv's")
        self.assertIn("*", self.record("subprocess.run(['bwrap', '--ro-bind', '/', '/', sys.executable, '-c', 'pass'])\n"),
                      "a sandbox hides the record file")

    def test_git_on_the_repo_also_keys_on_head_and_tags_other_blind_children_on_files_alone(self):
        for code in ("subprocess.run(['git', 'status'], capture_output=True)",
                     "subprocess.run(['git', '-C', 'lib', 'log'], capture_output=True)"):
            with self.subTest(code):
                self.assertLessEqual({"*", run.GIT_STATE}, self.record(code + "\n"))
        got = self.record("subprocess.run(['cat', 'data.txt'], capture_output=True)\n")
        self.assertIn("*", got)
        self.assertNotIn(run.GIT_STATE, got)

    def test_children_that_read_nothing_of_the_repo_stay_followed(self):
        got = self.record("t = tempfile.mkdtemp()\nsubprocess.run(['git', 'init', '-q', t], check=True)\n"
                          "subprocess.run(['git', '-C', t, 'status'], capture_output=True)\n"
                          "subprocess.run(['true'], check=True, cwd=t)\nsubprocess.run([sys.executable, '-I', '-c', 'pass'])\n"
                          "subprocess.run('echo hi', shell=True, capture_output=True, cwd=t)\n")
        self.assertNotIn("*", got)

    def test_a_program_that_reads_no_files_stays_followed_in_the_repo_but_not_given_a_repo_path(self):
        """T-3623: sleep, nvidia-smi and a one-shot browser run from a test's working folder (the repo) without reading it."""
        for name in sorted(runcover.QUIET):
            with self.subTest(name):
                t = f"t = os.path.join(tempfile.mkdtemp(), {name!r})\nos.symlink('/bin/true', t)\n"
                self.assertNotIn("*", self.record(t + "subprocess.run([t], check=True)\n"))
        self.assertIn("*", self.record("subprocess.run(['./bin/sleep', '0'])\n"), "a program of the repo's own")
        b = "t = os.path.join(tempfile.mkdtemp(), 'chromium')\nos.symlink('/bin/true', t)\n"
        shot = "subprocess.run([t, '--headless', '--dump-dom', %s], check=True)\n"
        self.assertNotIn("*", self.record(b + shot % "'http://127.0.0.1:1/'"))
        for arg in ("'data.txt'", "'file://' + os.path.abspath('data.txt')", "'file://localhost' + os.path.abspath('data.txt')",
                    "'file://' + os.path.abspath('data.txt') + '?q=1#x'", "'--app=file://' + os.path.abspath('data.txt')",
                    "'--user-data-dir=' + os.path.abspath('folder')", "'file://' + os.path.abspath('d%61ta.txt')"):
            with self.subTest(arg):
                self.assertIn("*", self.record(b + shot % ("'http://127.0.0.1:1/', " + arg)))
        for args in ("'--headless', '--remote-debugging-pipe', 'about:blank'", "'--headless', 'http://127.0.0.1:1/'"):
            with self.subTest(args):  # pages loaded later by devtools, or none to judge
                self.assertIn("*", self.record(b + f"subprocess.run([t, {args}], check=True)\n"))


def fake_classes(cids, tests=1, matched=None):
    """run.classes for main(): each class has `tests` tests, of which `matched` (default all) match the names."""
    def classes(patterns, k, hit, names, ids, parts, whole):
        for cid in cids:
            for i in range(tests):
                ids.append(f"{cid}.test_{i}")
                if i < (tests if matched is None else matched):
                    parts.setdefault(cid, []).append(f"{cid}.test_{i}")
        hit.update(names)
        return list(cids)
    return classes


class Main(unittest.TestCase):
    """main() with the classes, the tree and runs faked: what it runs, skips, records and says. Class X reads x.py."""

    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        env = mock.patch.dict(os.environ, outer(XDG_CACHE_HOME=self.d, FM_TEST_TIMES=os.path.join(self.d, "t.json")),
                              clear=True)
        env.start()
        self.addCleanup(env.stop)
        cover = mock.patch.object(run, "cover_python", return_value=None)  # no venv; sys.executable stays
        cover.start()
        self.addCleanup(cover.stop)
        self.blobs, self.git_dir = {"a.py": "ka", "b.py": "kb", "c.py": "kc", "other.py": "ko"}, "/repo"
        self.fail_ids, self.late, self.skips, self.during, self.blind = set(), set(), set(), {}, set()

    def main(self, *argv, cids=("test_m.A", "test_m.B"), tests=1, matched=None, sample=0.5):
        ran, err = [], io.StringIO()

        def run_one(c, *a):  # a class job runs its matched tests, a split class's job one test
            ran.append(c)
            n = (tests if matched is None else matched) if c.count(".") == 1 else 1
            if c.split(".")[1] not in self.blind:
                run.COVERED[c] = f"f /repo/{c.split('.')[1].lower()}.py\n"
            self.blobs.update(self.during.pop(c, {}))  # a file edited while the class runs
            if c in self.late:
                return c, 1, run.NOT_STARTED, 0, 0.0
            if c in self.skips:
                return c, 0, f"\nRan {n} tests in 0.0s\n\nOK (skipped=1)\n", n, 0.0
            return c, int(c in self.fail_ids), "boom" if c in self.fail_ids else "", n, 0.0
        rnd = sample if callable(sample) else (lambda: sample)
        with mock.patch.object(run, "classes", fake_classes(list(cids), tests, matched)), \
                mock.patch.object(run, "run_one", run_one), \
                mock.patch.object(run, "tree", lambda: ("/repo", dict(self.blobs), self.git_dir)), \
                mock.patch.object(run.random, "random", rnd), \
                mock.patch.object(sys, "argv", ["run.py", *argv]), contextlib.redirect_stderr(err):
            code = run.main()
        return code, ran, err.getvalue()

    def cache(self):
        p = run.cache_path(self.git_dir)
        return run.load_cache(p)[1] if os.path.exists(p) else None

    def test_a_named_rerun_skips_the_classes_green_at_the_same_code(self):
        code, ran, _ = self.main("test_m")
        self.assertEqual((code, sorted(ran)), (0, ["test_m.A", "test_m.B"]))
        code, ran, err = self.main("test_m")
        self.assertEqual((code, ran), (0, []), err)
        self.assertIn("skipped 2 classes green at the same code; FOREMAN_NO_TEST_CACHE=1 runs them", err)
        self.assertRegex(err, r"\nRan 0 tests in [\d.]+s \(0 jobs, [^\n]*\); 2 more green in the cache\n")
        self.assertEqual(err.strip().splitlines()[-1], "OK")
        lib = os.path.join(os.path.dirname(run.HERE), "lib")
        if lib not in sys.path:
            sys.path.insert(0, lib)
        from sampo import core
        self.assertEqual(core.judged(0, err)[0], 0, "a fully cached run is evidence, not a run of no tests")
        self.assertTrue(core.passed_summary(err))
        self.assertEqual(core.judged(0, "Ran 0 tests in 0.000s\n\nOK\n")[0], 5, "a run of nothing still proves nothing")

    def test_a_partly_cached_run_counts_ran_and_cached_apart(self):
        self.main("test_m")
        draws = iter([0.05, 0.9])  # A drawn, B cached
        _, ran, err = self.main("test_m", sample=lambda: next(draws))
        self.assertEqual(ran, ["test_m.A"])
        self.assertRegex(err, r"\nRan 1 tests in [\d.]+s \(1 jobs, [^\n]*\); 1 more green in the cache\n")

    def test_a_change_to_a_file_a_class_read_reruns_only_that_class(self):
        self.main("test_m")
        self.blobs["b.py"] = "kb2"
        _, ran, err = self.main("test_m")
        self.assertEqual(ran, ["test_m.B"])
        self.assertIn("skipped 1 classes", err)

    def test_a_change_no_class_read_reruns_none(self):
        self.main("test_m")
        self.blobs.update({"other.py": "ko2", "new.py": "kn"})
        self.assertEqual(self.main("test_m")[1], [])

    def test_a_new_or_renamed_class_and_one_nothing_was_recorded_for_run(self):
        self.blind = {"B"}
        self.main("test_m")
        _, ran, _ = self.main("test_m", cids=("test_m.A", "test_m.B", "test_n.C"))
        self.assertEqual(sorted(ran), ["test_m.B", "test_n.C"])
        self.assertEqual(sorted(self.cache()), ["test_m.A", "test_n.C"])

    def test_the_switch_the_full_gate_k_and_a_nested_run_never_skip(self):
        self.main("test_m")
        for argv, env in ((["test_m"], {"FOREMAN_NO_TEST_CACHE": "1"}), (["test_m"], {"SAMPO_NO_TEST_CACHE": "1"}),
                          ([], {}), (["test_m", "-k", "test_0"], {}), (["test_m"], {"FOREMAN_SLOT": "3"})):
            with self.subTest(argv=argv, env=env), mock.patch.dict(os.environ, env):
                code, ran, err = self.main(*argv)
                self.assertEqual((code, sorted(ran)), (0, ["test_m.A", "test_m.B"]), err)
                self.assertNotIn("skipped", err)

    def test_the_post_merge_opt_in_lets_a_full_run_skip_and_reaches_no_child(self):  # T-3638
        self.main()  # a plain full run records
        code, ran, err = self.main()
        self.assertEqual((code, sorted(ran)), (0, ["test_m.A", "test_m.B"]), "a plain full run never skips")
        with mock.patch.dict(os.environ, {"SAMPO_CACHE_FULL": "1"}):
            code, ran, err = self.main()
            self.assertEqual((code, ran), (0, []), err)
            self.assertNotIn("SAMPO_CACHE_FULL", os.environ, "children must not inherit the opt-in")
            self.assertNotIn("FOREMAN_CACHE_FULL", os.environ)
        with mock.patch.dict(os.environ, {"SAMPO_CACHE_FULL": "0"}):  # review: "0" is off, as for NO_CACHE
            code, ran, err = self.main()
            self.assertEqual((code, sorted(ran)), (0, ["test_m.A", "test_m.B"]), err)

    def test_the_full_gate_records_for_the_next_named_run(self):
        self.main()
        self.assertEqual([r[1:] for r in self.cache()["test_m.A"]], [[1, ["a.py"]]])
        _, ran, _ = self.main("test_m")
        self.assertEqual(ran, [])

    def test_the_cache_is_the_shared_git_folder_s(self):
        self.git_dir = "/repo/.git"
        self.main("test_m")
        self.assertEqual(sorted(self.cache()), ["test_m.A", "test_m.B"])

    def test_each_class_keeps_its_last_three_codes(self):
        for v in ("1", "2", "3", "4"):
            self.blobs["a.py"] = v
            self.main("test_m")
        self.assertEqual(len(self.cache()["test_m.A"]), run.KEEP)
        self.blobs["a.py"] = "2"
        self.assertEqual(self.main("test_m")[1], [], "a lane's code beside main's: both still cached")
        self.blobs["a.py"] = "1"
        self.assertEqual(self.main("test_m")[1], ["test_m.A"], "the oldest was let go")

    def test_only_a_fully_run_green_class_is_recorded(self):
        self.fail_ids = {"test_m.B"}
        self.assertEqual(self.main("test_m")[0], 1)
        self.assertEqual(sorted(self.cache()), ["test_m.A"])
        shutil.rmtree(os.path.join(self.d, "sampo"))
        self.fail_ids = set()
        self.main("test_m", tests=3, matched=2)  # the names matched 2 of each class's 3 tests
        self.assertIsNone(self.cache())

    def test_a_class_whose_files_changed_during_the_run_is_not_recorded(self):
        self.during = {"test_m.A": {"a.py": "ka2"}}  # A's file edited while A ran: it ran the old or the new
        self.main("test_m")
        self.assertEqual(sorted(self.cache()), ["test_m.B"])

    def test_a_class_that_skipped_a_test_is_not_recorded(self):  # skipUnless(chrome): green here, maybe not elsewhere
        self.skips = {"test_m.A"}
        self.assertEqual(self.main("test_m")[0], 0)
        self.assertEqual(sorted(self.cache()), ["test_m.B"])

    def test_a_split_class_is_recorded_once_all_its_tests_passed(self):
        seed = {"test_m.A": 99}  # slow last time: one job per test
        with open(os.environ["FM_TEST_TIMES"], "w") as f:
            json.dump(seed, f)
        _, ran, _ = self.main("test_m", cids=("test_m.A",), tests=2)
        self.assertEqual(sorted(ran), ["test_m.A.test_0", "test_m.A.test_1"])
        self.assertEqual([r[1:] for r in self.cache()["test_m.A"]], [[2, ["a.py"]]])

    def test_a_sampled_class_reruns_and_its_failure_drops_the_cache_and_runs_the_rest(self):
        self.main("test_m")
        _, ran, _ = self.main("test_m", sample=0.0)  # every cached class drawn
        self.assertEqual(sorted(ran), ["test_m.A", "test_m.B"])
        draws = iter([0.05, 0.9])  # A drawn, B skipped
        self.fail_ids = {"test_m.A"}
        code, ran, err = self.main("test_m", sample=lambda: next(draws))
        self.assertEqual(code, 1)
        self.assertEqual(ran, ["test_m.A", "test_m.B"], "the cache is wrong: what it skipped runs too")
        self.assertIn("test_m.A failed though the cache had it green", err)
        self.assertEqual(self.cache(), {}, "dropped, and nothing recorded from this run")

    def test_a_sampled_class_the_deadline_stopped_keeps_the_cache(self):
        self.main("test_m")
        self.late = {"test_m.A"}
        code, _, err = self.main("test_m", sample=0.0)
        self.assertEqual(code, 124, err)
        self.assertNotIn("the cache is wrong", err)
        self.assertEqual(sorted(self.cache()), ["test_m.A", "test_m.B"])

    def test_a_corrupt_cache_is_ignored(self):
        p = run.cache_path("/repo")
        os.makedirs(os.path.dirname(p))
        with open(p, "w") as f:
            f.write("{not json")
        code, ran, _ = self.main("test_m")
        self.assertEqual((code, len(ran)), (0, 2))
        self.assertEqual(sorted(self.cache()), ["test_m.A", "test_m.B"])


def rec(key, n=1, paths=("x.py",)):
    return [key, n, list(paths)]


class Store(unittest.TestCase):
    def test_the_path_is_per_repo_under_xdg_cache_home(self):
        with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": "/c"}):
            a, b = run.cache_path("/r/one"), run.cache_path("/r/two")
        self.assertTrue(a.startswith("/c/sampo/run-cache/") and a.endswith(".json"), a)
        self.assertNotEqual(a, b)
        with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": ""}):
            self.assertTrue(run.cache_path("/r").startswith(os.path.expanduser("~/.cache/sampo/run-cache/")))

    def test_a_write_is_atomic_and_never_follows_a_planted_link(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "sub", "c.json")
            victim = os.path.join(d, "victim")
            with open(victim, "w") as f:
                f.write("mine")
            os.makedirs(os.path.dirname(p))
            os.symlink(victim, f"{p}.{os.getpid()}")
            old = os.path.join(d, "sub", "gone-lane.json")
            open(old, "w").close()
            os.utime(old, (1, 1))
            run.save_cache(p, {"m.C": rec("k")}, 0)
            with open(victim) as f:
                self.assertEqual(f.read(), "mine")
            self.assertEqual(run.load_cache(p), (0, {"m.C": [rec("k")]}))
            self.assertFalse(os.path.exists(old), "a repo's cache unused for weeks (a removed lane's) is pruned")

    def test_paths_are_stored_once_however_many_classes_read_them(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            run.save_cache(p, {"m.A": rec("ka", 1, ["a.py", "core.py"]), "m.B": rec("kb", 2, ["core.py"])}, 0)
            with open(p) as f:
                self.assertEqual(sorted(json.load(f)["paths"]), ["a.py", "core.py"])
            self.assertEqual(run.load_cache(p)[1], {"m.A": [rec("ka", 1, ["a.py", "core.py"])],
                                                    "m.B": [rec("kb", 2, ["core.py"])]})

    def test_saves_merge_and_a_drop_is_not_undone_by_a_save_that_read_before_it(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            gen, _ = run.load_cache(p)  # two runs read the cache
            run.save_cache(p, {"m.A": rec("ka")}, gen)
            run.save_cache(p, {"m.B": rec("kb")}, gen)
            self.assertEqual(run.load_cache(p), (gen, {"m.A": [rec("ka")], "m.B": [rec("kb")]}), "merged")
            run.save_cache(p, {"m.A": rec("ka2")}, gen)
            self.assertEqual(run.load_cache(p)[1]["m.A"], [rec("ka2"), rec("ka")], "the newest first")
            run.drop_cache(p)  # a third found it wrong
            run.save_cache(p, {"m.C": rec("kc")}, gen)  # a run that read it before the drop
            self.assertEqual(run.load_cache(p), (gen + 1, {}))
            run.save_cache(p, {"m.D": rec("kd")}, gen + 1)  # one that read it after
            self.assertEqual(run.load_cache(p)[1], {"m.D": [rec("kd")]})

    def test_t3502_keys_read_as_an_empty_cache(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            with open(p, "w") as f:
                json.dump({"gen": 2, "classes": {"m.A": ["k", 1]}}, f)
            self.assertEqual(run.load_cache(p), (0, {}))

    @unittest.skipUnless(run.fcntl, "no flock here")
    def test_a_save_waits_for_the_lock(self):
        import threading
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            fd = os.open(p + ".lock", os.O_RDWR | os.O_CREAT, 0o600)
            run.fcntl.flock(fd, run.fcntl.LOCK_EX)
            t = threading.Thread(target=run.save_cache, args=(p, {"m.A": rec("ka")}, 0))
            t.start()
            t.join(0.3)
            self.assertTrue(t.is_alive(), "blocked on the lock another run holds")
            self.assertFalse(os.path.exists(p))
            os.close(fd)
            t.join(10)
            self.assertEqual(run.load_cache(p)[1], {"m.A": [rec("ka")]})


ONE = ("import os, sys, unittest\nHERE = os.path.dirname(os.path.abspath(__file__))\n"
       "sys.path.insert(0, os.path.join(HERE, '..', 'lib'))\nimport mod_a\n"
       "class One(unittest.TestCase):\n    def test_a(self):\n"
       "        open(os.path.join(HERE, 'fixtures', 'data.txt')).read()\n")
TWO = ("import os, subprocess, sys, unittest\nLIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib')\n"
       "class Two(unittest.TestCase):\n    def test_a(self):\n"
       "        subprocess.run([sys.executable, os.path.join(LIB, 'tool.py')], cwd=LIB, check=True)\n"
       "    def test_b(self):\n        pass\n")


class EndToEnd(unittest.TestCase):
    """The real run.py and runcover.py in a scratch repo: a rerun skips; a change reruns the classes that read it,
    in a child process too; a helper beside run.py reruns all; a renamed test runs."""

    def test_a_change_reruns_the_classes_that_read_it(self):
        top = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, top, True)
        d = os.path.join(top, "repo")
        tests = os.path.join(d, "plugin", "tests")
        os.makedirs(tests)
        for name in ("run.py", "runcover.py"):
            shutil.copy(os.path.join(run.HERE, name), os.path.join(tests, name))
        scratch(d, {"plugin/tests/test_one.py": ONE, "plugin/tests/test_two.py": TWO, "plugin/tests/common.py": "",
                    "plugin/tests/fixtures/data.txt": "x\n", "plugin/lib/mod_a.py": "A = 1\n",
                    "plugin/lib/mod_b.py": "B = 1\n", "plugin/lib/tool.py": "import mod_b\n", "README.md": "hi\n"})
        env = outer(XDG_CACHE_HOME=os.path.join(top, "cache"), FOREMAN_SLOTS="0", FM_TEST_TIMES=os.path.join(top, "t.json"))

        def go(*names):
            r = subprocess.run([sys.executable, os.path.join(tests, "run.py"), *(names or ("test_one", "test_two"))],
                               capture_output=True, text=True, timeout=300, env=env, cwd=d)
            self.assertEqual(r.returncode, 0, r.stderr)
            return r.stderr

        def edit(path):
            with open(os.path.join(d, path), "a") as f:
                f.write("# edited\n")
        self.assertRegex(go(), r"Ran 3 tests")
        # test_one has 1 test, test_two 2; each cached class reruns 1 time in 10, so a skip shows within 3 runs (1e-6)
        self.assertTrue(any("classes green at the same code" in go() for _ in range(3)))
        edit("README.md")  # read by neither
        self.assertTrue(any("classes green at the same code" in go() for _ in range(3)))
        edit("plugin/lib/mod_b.py")  # only test_two's child imports it
        self.assertRegex(go(), r"Ran (2 tests .*; 1 more green|3 tests)")
        edit("plugin/tests/fixtures/data.txt")  # only test_one reads it
        self.assertRegex(go(), r"Ran (1 tests .*; 2 more green|3 tests)")
        edit("plugin/tests/common.py")  # a helper beside run.py: every class's
        self.assertRegex(go(), r"Ran 3 tests in [^\n]*\)\n")
        os.rename(os.path.join(tests, "test_one.py"), os.path.join(tests, "test_uno.py"))
        self.assertRegex(go("test_uno", "test_two"), r"Ran (1 tests .*; 2 more green|3 tests)")


if __name__ == "__main__":
    unittest.main()
