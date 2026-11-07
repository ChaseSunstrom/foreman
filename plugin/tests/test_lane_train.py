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


class Lanes(ForemanTestCase):
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

    def train(self, *ids, check=True, env=None):
        return self.fm("lane", "train", ",".join(ids), check=check, env=env)

    def meta(self, tid):
        return json.loads(self.fm("task", "show", tid, "--json").stdout)["meta"]


class Train(Lanes):
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

    def test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does(self):
        """T-3531: up to 3 probes at once, each in its own scratch tree (a barrier only 3 concurrent runs pass); the
        left-out list stays in candidate order, as a serial run (a host over 2x its CPUs) gives it, though the first
        lane finishes last."""
        self.fm("check", "affected", "python3 -m unittest {tests}")
        arrive, log, wait = (os.path.join(self.tmp, n) for n in ("arrive", "probe-log", "barrier-wait"))
        os.makedirs(arrive)

        def red(n, name, after):  # touches arrive/<name>, waits for 3 there (or the barrier-wait file's seconds)
            src = ("import os, time, unittest\nclass {0}(unittest.TestCase):\n    def test_it(self):\n"
                   "        open(os.path.join({1!r}, {0!r}), 'w').close()\n        end = time.time() + float(open({2!r}).read())\n"
                   "        while len(os.listdir({1!r})) < 3 and time.time() < end:\n            time.sleep(0.02)\n"
                   "        with open({3!r}, 'a') as f:\n            f.write('%s %d\\n' % ({0!r}, len(os.listdir({1!r}))))\n"
                   "        time.sleep({4})\n        self.assertTrue(False)\n").format(name, arrive, wait, log, after)
            return self.lane(n, f"test_{name.lower()}.py", src)

        ids = [red(1, "One", 0.6), self.lane(2, "same.txt", "lane\n"), red(3, "Two", 0.3), red(4, "Three", 0)]
        with open(os.path.join(self.repo, "same.txt"), "w") as f:
            f.write("base\n")
        self.git("add", "same.txt")
        self.git("commit", "-qm", "base moves")

        def run(load, secs):  # (the left-out line, what each lane's first run saw at the barrier)
            for f in os.listdir(arrive):
                os.remove(os.path.join(arrive, f))
            open(log, "w").close()
            with open(wait, "w") as f:
                f.write(str(secs))
            r = self.train(*ids, check=False, env={"FOREMAN_HOST": f"load={load},cpus=4,mem_mb=8192",
                                                   "FOREMAN_LOAD_WAIT": "0"})
            seen = {}
            for line in open(log).read().split("\n"):
                if line:
                    seen.setdefault(*line.split())
            return next(l for l in (r.stdout + r.stderr).splitlines() if "nothing to merge" in l), seen

        serial, alone = run(99, 0.3)
        both, seen = run(0.1, 30)
        self.assertEqual(alone["One"], "1", "a host over 2x its CPUs probes one lane at a time")
        self.assertEqual(seen, {"One": "3", "Two": "3", "Three": "3"}, "three probes ran at once")
        self.assertEqual(both, serial)
        self.assertLess(both.index(ids[0]), both.index(ids[1]))
        self.assertLess(both.index(ids[2]), both.index(ids[3]))
        self.assertIn("conflicts with the base: same.txt", both)
        self.assertNotIn("probe", self.git("worktree", "list"), "every probe's scratch tree is gone")

    def _green_lane(self, base_change, links=""):
        """A lane adding test_x.py (counting its runs), its green run recorded as evidence in the lane, then the base
        moving `base_change`; (task id, the run count after the evidence, the train's result, the count file)."""
        self.fm("check", "affected", "python3 -m unittest {tests}")
        count = os.path.join(self.tmp, "x-runs")
        src = (f"{links}import unittest\nclass X(unittest.TestCase):\n    def test_it(self):\n"
               f"        open({count!r}, 'a').write('x')\n")
        a = self.lane(1, "test_x.py", src)
        self.fm("task", "evidence", a, "--step", "1", "--run", "python3 -m unittest test_x.py",
                cwd=os.path.join(self.tmp, "lane1"))
        ran = os.path.getsize(count)
        with open(os.path.join(self.repo, base_change), "a") as f:
            f.write("moved\n")
        self.git("add", base_change)
        self.git("commit", "-qm", "the base moves")
        return a, ran, self.train(a), count

    def test_a_lane_whose_own_green_run_still_holds_skips_its_probe(self):
        """T-3531: the lane's evidence ran its affected tests green on a tree whose diff to base+lane touches none of
        them nor the sources they cover: the probe's test run is skipped, one note line, and the lane lands."""
        a, ran, r, count = self._green_lane("other.txt")
        self.assertIn(f"note {a}: probe skipped", r.stdout)
        self.assertEqual(os.path.getsize(count), ran, "the probe ran no test")
        self.assertTrue(self.meta(a)["lane_stop"].startswith("merged"))

    def test_a_lane_whose_tested_source_moved_on_the_base_is_probed(self):
        """T-3531: the base changed a source the affected test covers (map-links): its green run no longer holds."""
        with open(os.path.join(self.repo, "lib.py"), "w") as f:
            f.write("X = 1\n")
        self.git("add", "lib.py")
        self.git("commit", "-qm", "a source")
        a, ran, r, count = self._green_lane("lib.py", "# map-links: lib.py\n")
        self.assertNotIn("probe skipped", r.stdout)
        self.assertGreater(os.path.getsize(count), ran, "the probe ran the test again")
        self.assertTrue(self.meta(a)["lane_stop"].startswith("merged"))

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


OK = "import unittest\nclass {0}(unittest.TestCase):\n    def test_it(self):\n        pass\n"


class AffectedGate(Lanes):
    """T-3544: the train's full-suite gate (the affected template's runner with no names) runs only the tests the
    batch's merged changes reach plus the rule tests; the full suite moves to the post-merge verify."""
    def setUp(self):
        super().setUp()
        self.suite = os.path.join(self.tmp, "suite-runs")  # one line per suite run: its folder and its arguments
        os.makedirs(os.path.join(self.repo, "plugin", "tests"))
        files = {"suite.sh": f'echo "${{PWD##*/}} $*" >> {self.suite}\nPYTHONPATH=plugin/tests exec python3 -m unittest "$@"\n',
                 "plugin/tests/test_doctor.py": OK.format("Doctor"),  # rule tests (cli.RULE_TESTS)
                 "plugin/tests/test_rename_aliases.py": OK.format("Aliases"), "test_other.py": OK.format("Other")}
        for rel, text in files.items():
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write(text)
        self.git("add", "-A")
        self.git("commit", "-qm", "a suite")
        self.fm("check", "add", "sh suite.sh")
        self.fm("check", "affected", "sh suite.sh {names}")
        from sampo import core as c
        self.p = c.find_project(self.repo)

    def gate_args(self):
        """The suite's arguments on each run in the train's scratch tree (the probes run in their own)."""
        with open(self.suite) as f:
            return [ln.split(" ", 1)[1].strip() for ln in f if ln.startswith("sampo-train-")]

    def test_the_gate_names_only_the_affected_modules_and_the_rule_tests(self):
        """A lane adding a module gets test_rename_aliases though no map link names it (T-3316's miss); the other
        gates run as configured, the pass records its modules, and each landed merge awaits the full suite."""
        from sampo import core as c, lanes
        a, b = self.lane(1, "test_a.py", OK.format("A")), self.lane(2, "plugin/newmod.py", "X = 1\n")
        r = self.train(a, b, env={"FM_POSTMERGE_CMD": "sh suite.sh"})
        self.assertEqual(self.gate_args(), ["test_doctor test_rename_aliases test_a"], r.stdout)
        self.assertEqual(self.gate_runs(), 1, "the other gate ran once, as configured")
        row = [e for e in c.ledger_events(self.p, ("check_run",)) if e["data"].get("train")][-1]["data"]["results"][1]
        self.assertEqual((row["cmd"], row["affected"]), ("sh suite.sh", ["test_doctor", "test_rename_aliases", "test_a"]))
        self.assertEqual(sorted(x["task"] for x in lanes.pm_records(self.p).values()), sorted([a, b]))
        self.assertIn("3 affected test module(s)", r.stdout)

    def test_a_red_gate_names_the_failing_class_on_the_left_out_lane(self):
        """Each lane is green alone (its probe passes); together they fail: the culprit's reason and brief name the
        failing class and the gate's last lines, so nobody reruns a full suite to learn them."""
        pair = "import os, unittest\nclass Pair(unittest.TestCase):\n    def test_it(self):\n        self.assertFalse(os.path.exists('b.txt'))\n"
        a, b = self.lane(1, "test_pair.py", pair), self.lane(2, "b.txt")
        r = self.train(a, b)
        self.assertIn(f"left out {b}: its merge turns the gates red: sh suite.sh on 3 affected test module(s), "
                      "failing test_pair.Pair", r.stdout)
        self.assertIn("FAILED (failures=1)", r.stdout, "the gate's last lines")
        log = self.fm("task", "show", b).stdout
        self.assertIn("test_pair.Pair", log)
        self.assertIn("FAILED (failures=1)", log)
        self.assertTrue(os.path.exists(os.path.join(self.repo, "test_pair.py")))
        self.assertFalse(os.path.exists(os.path.join(self.repo, "b.txt")))

    def test_full_gate_runs_the_bare_full_suite(self):
        from sampo import lanes
        self.train(self.lane(1, "test_a.py", OK.format("A")), env={"FOREMAN_FULL_GATE": "1", "FM_POSTMERGE_CMD": "sh suite.sh"})
        self.assertEqual(self.gate_args(), [""])
        self.assertEqual(lanes.pm_records(self.p), {}, "the full suite already ran: no post-merge verify")

    def test_a_close_after_the_train_reuses_its_affected_pass(self):
        """T-3526's close skips its linked tests when the train's pass ran every one of them."""
        a = self.lane(1, "test_a.py", OK.format("A"))
        self.train(a)
        with open(self.suite) as f:
            before = f.read()
        r = self.fm("task", "finish", a, "--audit", "self", "--run", "true", check=False, env={"FOREMAN_SENTINEL": "off"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("covered by the gates' pass", r.stdout)
        with open(self.suite) as f:
            self.assertEqual(f.read(), before, "the linked tests ran again")


class SlotPriority(Lanes):
    def test_the_train_and_the_main_checks_runs_take_slots_first_and_a_lanes_do_not(self):
        """T-3614: tests/run.py gives freed CPU slots to a waiting run with SAMPO_SLOT_PRIORITY=1 first."""
        seen = os.path.join(self.tmp, "priority")
        self.fm("check", "add", f'echo "${{FOREMAN_SLOT_PRIORITY:-low}}" >> {seen}')
        unset = {"FOREMAN_SLOT_PRIORITY": ""}  # this test's own runner may run with it
        tid = self.lane(1, "a.txt")
        self.fm("check", "--fresh", cwd=os.path.join(self.tmp, "lane1"), env=unset)
        self.fm("check", "--fresh", env=unset)
        self.fm("check", "--fresh", env={"FOREMAN_SLOT_PRIORITY": "0"})  # an opt-out stays low
        self.train(tid, env=unset)
        self.assertEqual(open(seen).read().split(), ["low", "1", "0", "1"])


if __name__ == "__main__":
    unittest.main()
