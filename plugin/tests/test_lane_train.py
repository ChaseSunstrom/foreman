"""T-3380: sampo lane train merges N reviewed lanes in a scratch integration worktree, gates once, bisects a red set to
the culprit lanes, fast-forwards the main checkout's branch, and records a gate pass `sampo check` reuses while the code
tree (minus CHANGELOG.md and the sync mirror) is the same."""
# map-links: plugin/lib/sampo/train.py
import json
import math
import os
import subprocess
import unittest

from helpers import ForemanTestCase

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # noqa: E731


class Train(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.runs = os.path.join(self.tmp, "gate-runs")
        self.fm("check", "add", f"echo x >> {self.runs}; test ! -e BREAK")

    def git(self, *args, cwd=None):
        return subprocess.run(["git", "-C", cwd or self.repo, *args], capture_output=True, text=True).stdout.strip()

    def gate_runs(self):
        return len(open(self.runs).read().split()) if os.path.exists(self.runs) else 0

    def lane(self, n, name, text=None, ac="true"):
        """A lane worktree with a task and one commit writing `name`; its task id."""
        path = os.path.join(self.tmp, f"lane{n}")
        subprocess.run(["git", "-C", self.repo, "worktree", "add", "-q", "-b", f"foreman/lane{n}", path], check=True)
        tid = first(self.fm("task", "new", f"Lane {n}", "--type", "FEATURE", "--tier", "S", "--ac", f"ok :: {ac}",
                            "--step", "s", "--json", "--focus", cwd=path).stdout)["id"]
        with open(os.path.join(path, name), "w") as f:
            f.write(text or f"{n}\n")
        self.git("add", name, cwd=path)
        self.git("commit", "-qm", f"lane {n}", cwd=path)
        return tid

    def train(self, *ids, check=True):
        return self.fm("lane", "train", ",".join(ids), check=check)

    def meta(self, tid):
        return json.loads(self.fm("task", "show", tid, "--json").stdout)["meta"]

    def test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget(self):
        ids = [self.lane(1, "a.txt"), self.lane(2, "b.txt"), self.lane(3, "c.txt"), self.lane(4, "BREAK")]
        r = self.train(*ids)
        self.assertIn(ids[3], r.stdout)
        self.assertLessEqual(self.gate_runs(), 1 + math.ceil(math.log2(4)), r.stdout)
        for name in ("a.txt", "b.txt", "c.txt"):
            self.assertTrue(os.path.exists(os.path.join(self.repo, name)), name)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "BREAK")))
        for tid in ids[:3]:
            self.assertTrue(self.meta(tid)["lane_stop"].startswith("merged"), self.meta(tid))
        self.assertFalse(self.meta(ids[3]).get("lane_stop", "").startswith("merged"))
        self.assertNotIn("train", self.git("worktree", "list"), "the scratch worktree is gone")

    def test_a_middle_culprit_costs_one_regate_more(self):
        ids = [self.lane(1, "a.txt"), self.lane(2, "BREAK"), self.lane(3, "c.txt"), self.lane(4, "d.txt")]
        r = self.train(*ids)
        self.assertLessEqual(self.gate_runs(), 2 + math.ceil(math.log2(4)), r.stdout)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "d.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.repo, "BREAK")))

    def test_check_reuses_the_train_pass_when_only_changelog_and_mirror_changed(self):
        self.train(self.lane(1, "a.txt"), self.lane(2, "b.txt"))
        self.assertEqual(self.gate_runs(), 1)
        with open(os.path.join(self.repo, "CHANGELOG.md"), "w") as f:
            f.write("- a line the close adds\n")
        os.makedirs(os.path.join(self.repo, ".sampo"), exist_ok=True)
        with open(os.path.join(self.repo, ".sampo", "STATE.md"), "w") as f:
            f.write("mirror\n")
        self.assertIn("cached", self.fm("check").stdout)
        self.assertEqual(self.gate_runs(), 1, "no gate ran")
        with open(os.path.join(self.repo, "a.txt"), "w") as f:
            f.write("changed code\n")
        self.fm("check")
        self.assertEqual(self.gate_runs(), 2, "a code change reruns the gates")

    def test_a_conflicting_lane_is_skipped_with_its_files_and_main_only_fast_forwards(self):
        a, b, d = self.lane(1, "same.txt", "one\n"), self.lane(2, "same.txt", "two\n"), self.lane(3, "d.txt")
        r = self.train(a, b, d)
        self.assertIn(b, r.stdout)
        self.assertIn("same.txt", r.stdout)
        self.assertEqual(open(os.path.join(self.repo, "same.txt")).read(), "one\n")
        self.assertTrue(os.path.exists(os.path.join(self.repo, "d.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.repo, ".git", "MERGE_HEAD")))
        self.assertEqual(self.git("reflog", "-n", "1", "--format=%gs").split()[0], "merge", "one fast-forward")
        self.assertFalse(self.meta(b).get("lane_stop", "").startswith("merged"))

    def test_a_lane_conflicting_with_the_base_is_left_out_before_any_gate_run(self):
        """T-3474: git merge-tree names a conflict with the base in milliseconds, not as 'an earlier lane'."""
        a = self.lane(1, "same.txt", "lane\n")
        with open(os.path.join(self.repo, "same.txt"), "w") as f:
            f.write("base\n")
        self.git("add", "same.txt")
        self.git("commit", "-qm", "base moves")
        r = self.train(a, check=False)
        self.assertIn("conflicts with the base: same.txt", r.stdout + r.stderr)
        self.assertEqual(self.gate_runs(), 0, "no gate run on a lane merge-tree rules out")

    def test_a_lane_whose_affected_test_fails_is_left_out_before_the_gate_run(self):
        """T-3474: each lane's affected tests run on base+lane first; a red one is named by class, a green one lands
        through one gate run (the gate itself never runs these tests)."""
        self.fm("check", "affected", "python3 -m unittest {tests}")
        test = "import unittest\nclass {0}(unittest.TestCase):\n    def test_it(self):\n        self.assertTrue({1})\n"
        good = self.lane(1, "test_good.py", test.format("Good", "True"))
        bad = self.lane(2, "test_bad.py", test.format("Bad", "False"))
        r = self.train(good, bad)
        self.assertIn(f"left out {bad}: its affected tests fail on the base: test_bad.Bad", r.stdout)
        self.assertEqual(self.gate_runs(), 1, r.stdout)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "test_good.py")))
        self.assertFalse(os.path.exists(os.path.join(self.repo, "test_bad.py")))
        self.assertNotIn("probe", self.git("worktree", "list"), "the probe worktrees are gone")

    def test_an_affected_test_red_on_the_base_itself_is_left_to_the_gates(self):
        """T-3474 review: a class red on the bare base too isn't the lane's fault: an info line, and the lane goes on."""
        self.fm("check", "affected", "python3 -m unittest {tests}")
        red = "import unittest\nclass Old(unittest.TestCase):\n    def test_it(self):\n        self.assertTrue(False)\n"
        with open(os.path.join(self.repo, "test_old.py"), "w") as f:
            f.write(red)
        self.git("add", "test_old.py")
        self.git("commit", "-qm", "a red test on the base")
        a = self.lane(1, "test_old.py", red + "# touched\n")
        r = self.train(a)
        self.assertIn("its affected tests are red on the base itself: test_old.Old; left to the gates", r.stdout)
        self.assertNotIn(f"left out {a}", r.stdout)
        self.assertEqual(self.gate_runs(), 1, r.stdout)
        self.assertTrue(self.meta(a)["lane_stop"].startswith("merged"))

    def test_a_flaky_affected_test_is_rerun_once_and_the_lane_goes_on(self):
        """T-3474 review: red once, green on the rerun of its class: named as flaky, never blamed on the lane."""
        self.fm("check", "affected", "python3 -m unittest {tests}")
        count = os.path.join(self.tmp, "flaky-runs")
        flaky = ("import os, unittest\nclass Flaky(unittest.TestCase):\n    def test_it(self):\n"
                 f"        with open({count!r}, 'a') as f:\n            f.write('x')\n"
                 f"        self.assertGreater(os.path.getsize({count!r}), 1)\n")
        a = self.lane(1, "test_flaky.py", flaky)
        r = self.train(a)
        self.assertIn("flaky", r.stdout)
        self.assertIn("test_flaky.Flaky", r.stdout)
        self.assertNotIn(f"left out {a}", r.stdout)
        self.assertEqual(self.gate_runs(), 1, r.stdout)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "test_flaky.py")))

    def test_a_lane_whose_own_criterion_is_red_is_left_out_named(self):
        a, b = self.lane(1, "a.txt"), self.lane(2, "b.txt", ac="false")
        r = self.train(a, b)
        self.assertIn(b, r.stdout)
        self.assertIn("criterion", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "b.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.repo, "a.txt")))

    def test_a_bare_train_names_no_lane_and_lands_nothing(self):
        self.lane(1, "a.txt")
        r = self.fm("lane", "train", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "a.txt")))

    def test_a_repeated_id_merges_once(self):
        a = self.lane(1, "a.txt")
        self.train(a, a)
        self.assertEqual(self.gate_runs(), 1)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "a.txt")))

    def test_a_red_base_stops_the_train_instead_of_blaming_a_lane(self):
        with open(os.path.join(self.repo, "BREAK"), "w") as f:
            f.write("x\n")
        self.git("add", "BREAK")
        self.git("commit", "-qm", "red base")
        a = self.lane(1, "a.txt")
        r = self.train(a, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("base", r.stderr + r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "a.txt")))
        self.assertFalse(self.meta(a).get("lane_stop", "").startswith("merged"))


if __name__ == "__main__":
    unittest.main()
