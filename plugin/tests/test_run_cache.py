"""T-3502: run.py skips a class already green at the same code (its test file, the test modules it imports, the sources
the map links to it, the plugin tree), reruns 1 in 10 of those anyway and drops the cache when one fails; the full gate,
-k runs, nested runs and FOREMAN_NO_TEST_CACHE=1 never skip."""
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

NESTED = ("SAMPO_SLOT", "FOREMAN_SLOT", "SAMPO_SLOTS", "FOREMAN_SLOTS", "SAMPO_NO_TEST_CACHE", "FOREMAN_NO_TEST_CACHE")


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


class Keys(unittest.TestCase):
    def setUp(self):
        self.d = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d, True)
        scratch(self.d, {
            "plugin/tests/run.py": "# the runner\n",
            "plugin/tests/helpers.py": "import sampo\n",
            "plugin/tests/test_a.py": "import helpers\nSITE = 'site'\n" + TEST,  # names a top folder: linked to site/
            "plugin/tests/test_b.py": "from test_a import C as Base\n" + TEST,
            "plugin/tests/test_c.py": TEST,
            "plugin/tests/test_walk.py": "import os\nos.listdir('.')\n" + TEST,
            "plugin/tests/fixtures/data.txt": "x\n",
            "plugin/tests/walker.py": "import glob\nFOUND = glob.glob('*')\n",
            "plugin/tests/test_d.py": "from walker import FOUND\n" + TEST,  # reads folders through a helper
            "plugin/lib/sampo/core.py": "X = 1\n",
            "site/index.html": "<p>hi</p>\n",
            "docs/guide.md": "words\n",
            "MASTER.md": "map\n",
            ".sampo/tasks/T-1.md": "state\n",
        })
        self.here = os.path.join(self.d, "plugin", "tests")
        self.cids = ["test_a.C", "test_b.C", "test_c.C", "test_d.C", "test_walk.C"]

    def keys(self):
        with mock.patch.object(run, "HERE", self.here):
            repo, blobs = run.tree()
            self.assertEqual(repo, self.d)
            return run.cache_keys(repo, blobs, self.cids)

    def edit(self, path, text="changed\n"):
        with open(os.path.join(self.d, path), "a") as f:
            f.write(text)

    def changed(self, before):
        after = self.keys()
        return sorted(c for c in self.cids if before[c] != after[c])

    def test_blobs_are_git_hashes_of_the_files_on_disk_untracked_ones_too(self):
        self.edit("plugin/lib/sampo/core.py")
        with open(os.path.join(self.d, "plugin", "lib", "new.py"), "w") as f:
            f.write("Y = 2\n")
        with mock.patch.object(run, "HERE", self.here):
            _, blobs = run.tree()
        for path in ("plugin/lib/sampo/core.py", "plugin/lib/new.py", "MASTER.md"):
            self.assertEqual(blobs[path], git(self.d, "hash-object", path).strip(), path)
        os.remove(os.path.join(self.d, "docs", "guide.md"))
        with mock.patch.object(run, "HERE", self.here):
            self.assertNotIn("docs/guide.md", run.tree()[1], "a deleted file isn't hashed")

    def test_an_unchanged_tree_keeps_every_key(self):
        self.assertEqual(self.keys(), self.keys())
        keys = self.keys()
        self.assertEqual(keys["test_d.C"], keys["test_walk.C"], "both read folders: the whole tree's key")
        self.assertEqual(len(set(keys.values())), len(self.cids) - 1)

    def test_a_plugin_source_or_root_file_changes_every_key(self):
        for path in ("plugin/lib/sampo/core.py", "MASTER.md", "plugin/tests/fixtures/data.txt", "plugin/tests/run.py"):
            before = self.keys()
            self.edit(path)
            self.assertEqual(self.changed(before), self.cids, path)

    def test_a_test_file_changes_its_own_key_its_importers_and_the_folder_walkers(self):
        before = self.keys()
        self.edit("plugin/tests/test_c.py", "# note\n")
        self.assertEqual(self.changed(before), ["test_c.C", "test_d.C", "test_walk.C"])
        before = self.keys()
        self.edit("plugin/tests/test_a.py", "# note\n")
        self.assertEqual(self.changed(before), ["test_a.C", "test_b.C", "test_d.C", "test_walk.C"], "test_b imports test_a")
        before = self.keys()
        self.edit("plugin/tests/helpers.py", "# note\n")
        self.assertEqual(self.changed(before), ["test_a.C", "test_b.C", "test_d.C", "test_walk.C"], "imported through test_a")

    def test_another_top_folder_changes_only_the_tests_the_map_links_to_it(self):
        before = self.keys()
        self.edit("site/index.html")
        self.assertEqual(self.changed(before), ["test_a.C", "test_b.C", "test_d.C", "test_walk.C"], "test_a names 'site'")
        before = self.keys()
        self.edit("docs/guide.md")
        self.assertEqual(self.changed(before), ["test_d.C", "test_walk.C"], "test_d walks folders through walker.py")

    def test_sampo_task_state_changes_no_key(self):
        before = self.keys()
        self.edit(".sampo/tasks/T-1.md")
        with open(os.path.join(self.d, ".sampo", "tasks", "T-2.md"), "w") as f:
            f.write("new\n")
        self.assertEqual(self.changed(before), [])

    def test_no_map_keys_each_class_on_the_whole_tree(self):
        with mock.patch.object(run, "_test_links", side_effect=ImportError("no sampo")):
            before = self.keys()
            self.edit("docs/guide.md")
            self.assertEqual(self.changed(before), self.cids)

    def test_outside_git_there_are_no_keys(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(run, "HERE", d):
            self.assertIsNone(run.tree())


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
    """main() with the classes, keys and runs faked: what it runs, skips, records and says."""

    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        env = mock.patch.dict(os.environ, outer(XDG_CACHE_HOME=self.d, FM_TEST_TIMES=os.path.join(self.d, "t.json")),
                              clear=True)
        env.start()
        self.addCleanup(env.stop)
        self.keys = {"test_m.A": "ka", "test_m.B": "kb"}
        self.fail_ids, self.late, self.skips, self.during = set(), set(), set(), {}

    def main(self, *argv, cids=("test_m.A", "test_m.B"), tests=1, matched=None, sample=0.5):
        ran, err = [], io.StringIO()

        def run_one(c, *a):  # a class job runs its matched tests, a split class's job one test
            ran.append(c)
            n = (tests if matched is None else matched) if c.count(".") == 1 else 1
            self.keys.update(self.during.pop(c, {}))  # a file edited while the class runs
            if c in self.late:
                return c, 1, run.NOT_STARTED, 0, 0.0
            if c in self.skips:
                return c, 0, f"\nRan {n} tests in 0.0s\n\nOK (skipped=1)\n", n, 0.0
            return c, int(c in self.fail_ids), "boom" if c in self.fail_ids else "", n, 0.0
        rnd = sample if callable(sample) else (lambda: sample)
        with mock.patch.object(run, "classes", fake_classes(list(cids), tests, matched)), \
                mock.patch.object(run, "run_one", run_one), \
                mock.patch.object(run, "tree", return_value=("/repo", {})), \
                mock.patch.object(run, "cache_keys", lambda repo, blobs, cs: {c: self.keys[c] for c in cs if c in self.keys}), \
                mock.patch.object(run.random, "random", rnd), \
                mock.patch.object(sys, "argv", ["run.py", *argv]), contextlib.redirect_stderr(err):
            code = run.main()
        return code, ran, err.getvalue()

    def cache(self):
        p = run.cache_path("/repo")
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

    def test_a_changed_key_reruns_only_its_class(self):
        self.main("test_m")
        self.keys["test_m.B"] = "kb2"
        _, ran, err = self.main("test_m")
        self.assertEqual(ran, ["test_m.B"])
        self.assertIn("skipped 1 classes", err)

    def test_the_switch_the_full_gate_k_and_a_nested_run_never_skip(self):
        self.main("test_m")
        for argv, env in ((["test_m"], {"FOREMAN_NO_TEST_CACHE": "1"}), (["test_m"], {"SAMPO_NO_TEST_CACHE": "1"}),
                          ([], {}), (["test_m", "-k", "test_0"], {}), (["test_m"], {"FOREMAN_SLOT": "3"})):
            with self.subTest(argv=argv, env=env), mock.patch.dict(os.environ, env):
                code, ran, err = self.main(*argv)
                self.assertEqual((code, sorted(ran)), (0, ["test_m.A", "test_m.B"]), err)
                self.assertNotIn("skipped", err)

    def test_the_full_gate_records_for_the_next_named_run(self):
        self.main()
        self.assertEqual(self.cache()["test_m.A"][0], "ka")
        _, ran, _ = self.main("test_m")
        self.assertEqual(ran, [])

    def test_only_a_fully_run_green_class_is_recorded(self):
        self.fail_ids = {"test_m.B"}
        self.assertEqual(self.main("test_m")[0], 1)
        self.assertEqual(sorted(self.cache()), ["test_m.A"])
        shutil.rmtree(os.path.join(self.d, "sampo"))
        self.fail_ids = set()
        self.main("test_m", tests=3, matched=2)  # the names matched 2 of each class's 3 tests
        self.assertIsNone(self.cache())

    def test_a_class_whose_files_changed_during_the_run_is_not_recorded(self):
        self.during = {"test_m.A": {"test_m.A": "ka2"}}  # A's test file edited while A ran: it ran the old or the new
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
        self.assertEqual(self.cache()["test_m.A"], ["ka", 2])

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
            run.save_cache(p, {"m.C": ["k", 1]}, 0)
            with open(victim) as f:
                self.assertEqual(f.read(), "mine")
            self.assertEqual(run.load_cache(p), (0, {"m.C": ["k", 1]}))
            self.assertFalse(os.path.exists(old), "a repo's cache unused for weeks (a removed lane's) is pruned")


    def test_saves_merge_and_a_drop_is_not_undone_by_a_save_that_read_before_it(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            gen, _ = run.load_cache(p)  # two runs read the cache
            run.save_cache(p, {"m.A": ["ka", 1]}, gen)
            run.save_cache(p, {"m.B": ["kb", 1]}, gen)
            self.assertEqual(run.load_cache(p), (gen, {"m.A": ["ka", 1], "m.B": ["kb", 1]}), "merged, not replaced")
            run.drop_cache(p)  # a third found it wrong
            run.save_cache(p, {"m.C": ["kc", 1]}, gen)  # a run that read it before the drop
            self.assertEqual(run.load_cache(p), (gen + 1, {}))
            run.save_cache(p, {"m.D": ["kd", 1]}, gen + 1)  # one that read it after
            self.assertEqual(run.load_cache(p)[1], {"m.D": ["kd", 1]})

    @unittest.skipUnless(run.fcntl, "no flock here")
    def test_a_save_waits_for_the_lock(self):
        import threading
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            fd = os.open(p + ".lock", os.O_RDWR | os.O_CREAT, 0o600)
            run.fcntl.flock(fd, run.fcntl.LOCK_EX)
            t = threading.Thread(target=run.save_cache, args=(p, {"m.A": ["ka", 1]}, 0))
            t.start()
            t.join(0.3)
            self.assertTrue(t.is_alive(), "blocked on the lock another run holds")
            self.assertFalse(os.path.exists(p))
            os.close(fd)
            t.join(10)
            self.assertEqual(run.load_cache(p)[1], {"m.A": ["ka", 1]})


class EndToEnd(unittest.TestCase):
    """The real run.py in a scratch repo: git hashes, the skip line, an edit that reruns."""

    def test_a_rerun_of_an_unchanged_tree_skips_and_an_edit_reruns(self):
        top = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, top, True)
        d = os.path.join(top, "repo")
        tests = os.path.join(d, "plugin", "tests")
        os.makedirs(tests)
        shutil.copy(os.path.join(run.HERE, "run.py"), os.path.join(tests, "run.py"))
        scratch(d, {"plugin/tests/test_one.py": TEST, "plugin/tests/test_two.py": TEST})
        env = outer(XDG_CACHE_HOME=os.path.join(top, "cache"), FOREMAN_SLOTS="0", FM_TEST_TIMES=os.path.join(top, "t.json"))

        def go(*names):
            r = subprocess.run([sys.executable, os.path.join(tests, "run.py"), *names], capture_output=True, text=True,
                               timeout=300, env=env, cwd=d)
            self.assertEqual(r.returncode, 0, r.stderr)
            return r.stderr
        self.assertNotIn("skipped", go("test_one", "test_two"))
        errs = [go("test_one", "test_two") for _ in range(3)]  # each class reruns 1 time in 10: all 3 times both, 1e-6
        self.assertTrue(any("classes green at the same code" in e for e in errs), errs)
        self.assertTrue(all(re.search(r"Ran (2 tests|1 tests .*1 more|0 tests .*2 more)", e) for e in errs), errs)
        with open(os.path.join(tests, "test_two.py"), "a") as f:
            f.write("# edited\n")
        err = go("test_one", "test_two")
        self.assertNotIn("skipped 2 classes", err)
        self.assertIn("Ran 2 tests", err)


if __name__ == "__main__":
    unittest.main()
