"""fm exam long (T-2258): goals replayed from a local repo's task changes, hidden checks from what shipped."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmprove

TEST = ("import unittest\nimport app\n\n\nclass T(unittest.TestCase):\n"
        "    def test_old(self):\n        self.assertEqual(app.old(), 0)\n{extra}")
APP = "def old():\n    return 0\n"


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


class Long(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.src = os.path.join(self.tmp, "src")
        subprocess.run(["git", "init", "-q", "-b", "main", self.src], check=True)
        for k, v in (("user.email", "t@example.com"), ("user.name", "t")):
            subprocess.run(["git", "-C", self.src, "config", k, v], check=True)
        write(self.src, "app.py", APP)
        write(self.src, "tests/test_app.py", TEST.format(extra=""))
        self.commit("init")
        app, tests = APP, TEST.format(extra="")
        for n, passes_at_base in ((1, False), (2, True), (3, False)):
            app += f"\n\ndef f{n}():\n    return {n}\n"
            body = f"    def test_f{n}(self):\n        self.assertEqual(app.f{n}(), {n})\n"
            if passes_at_base:  # a check that already passes at the base: the window must be dropped
                body = f"    def test_f{n}(self):\n        self.assertEqual(app.old(), 0)\n"
            tests += "\n" + body
            write(self.src, "app.py", app)
            write(self.src, "tests/test_app.py", tests)
            self.commit(f"Add f{n} (T-100{n})")

    def commit(self, msg):
        subprocess.run(["git", "-C", self.src, "add", "."], check=True)
        subprocess.run(["git", "-C", self.src, "commit", "-qm", msg], check=True)

    def gen(self, trust=True):
        if trust:
            fmprove.remember(self.src)
        return self.fm("exam", "long", "gen", "--from", self.src, "--json", check=trust)

    def test_gen_keeps_only_red_at_base_green_at_target_with_no_future_history(self):
        r = json.loads(self.gen().stdout)
        self.assertEqual(sorted(s["id"] for s in r["scenarios"]), ["T-1001", "T-1003"])  # T-1002's check passes at base
        for s in r["scenarios"]:
            repo = s["repo"]
            self.assertEqual(subprocess.run(["git", "-C", repo, "rev-list", "--count", "HEAD"], capture_output=True,
                                            text=True).stdout.strip(), "1")
            key = json.load(open(os.path.join(os.path.dirname(repo), "key.json")))
            self.assertFalse(os.path.exists(os.path.join(repo, "key.json")))
            self.assertEqual(len(key["checks"]), 1)
            self.assertIn("test_app.T.test_f" + s["id"][-1], key["checks"][0])
            self.assertNotIn("def f1", open(os.path.join(repo, "app.py")).read()) if s["id"] == "T-1001" else None
        later = [s for s in r["scenarios"] if s["id"] == "T-1003"][0]["repo"]
        self.assertIn("def f2", open(os.path.join(later, "app.py")).read())  # base of T-1003 holds the earlier work
        self.assertNotIn("def f3", open(os.path.join(later, "app.py")).read())  # but never its own or later work

    def test_oracle_scores_true_done_and_empty_does_not_and_the_line_is_tier_long(self):
        run = json.loads(self.gen().stdout)["run"]
        for agent, done in (("oracle", 2), ("empty", 0)):
            self.fm("exam", "long", "run", run, "--agent", agent)
            g = json.loads(self.fm("exam", "long", "grade", run, "--agent", agent, "--json").stdout)
            self.assertEqual(g["true_done"], done, g)
            self.assertEqual(g["regressions"], 0, g)
        long = [x for x in self.lines() if x.get("tier") == "long"]
        self.assertEqual([(x["agent"], x["true_done"], x["model"]) for x in long], [("oracle", 2, None), ("empty", 0, None)])  # zero-token arms: no model

    def lines(self):
        import fmcore as c
        import fmgenesis
        p = c.find_project(self.repo)
        with open(os.path.join(fmgenesis.home(p), "exam.jsonl")) as f:
            return [json.loads(x) for x in f.read().splitlines()]

    def test_an_untrusted_source_runs_none_of_its_code(self):
        ran = os.path.join(self.tmp, "ran")
        write(self.src, "tests/test_evil.py", f"open({ran!r}, 'w').write('x')\n")
        self.commit("evil")
        r = self.gen(trust=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fm prove", r.stderr)
        self.assertFalse(os.path.exists(ran))

    def work(self, run, agent, sid="T-1001"):
        import fmcore as c
        import fmlong
        return os.path.join(fmlong._root(c.find_project(self.repo)), run, "work", agent, sid)

    def grade(self, run, agent):
        return json.loads(self.fm("exam", "long", "grade", run, "--agent", agent, "--json").stdout)

    def test_an_answer_cannot_shadow_the_stdlib_or_stand_in_for_a_hidden_test(self):
        run = json.loads(self.gen().stdout)["run"]
        self.fm("exam", "long", "run", run, "--agent", "empty")
        w = self.work(run, "empty")
        write(w, "unittest.py", "raise SystemExit(0)\n")  # would end any run that imports it first
        write(w, "test_app.py", "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_f1(self):\n        pass\n")
        self.assertEqual(self.grade(run, "empty")["true_done"], 0)

    def test_a_break_is_a_regression_and_every_goal_counts_in_the_total(self):
        run = json.loads(self.gen().stdout)["run"]
        self.fm("exam", "long", "run", run, "--agent", "oracle")
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.work(run, "oracle")))), "T-1003", "key.json")) as f:
            self.assertTrue(json.load(f)["sample"])
        self.assertEqual(self.grade(run, "oracle")["regressions"], 0)  # by construction
        f = os.path.join(self.work(run, "oracle"), "app.py")
        text = open(f).read()
        with open(f, "w") as fh:
            fh.write(text.replace("return 0", "return 9"))
        g = self.grade(run, "oracle")
        self.assertTrue(g["regressions"] >= 1 and g["true_done"] == 2, g)
        os.rename(self.work(run, "oracle", "T-1003"),os.path.join(self.tmp, "gone"))  # one unanswered
        g = self.grade(run, "oracle")
        self.assertEqual((g["scenarios"], g["true_done"]), (2, 1), g)  # the unanswered goal is in the 2, not in the 1

    def test_grade_rechecks_trust(self):
        import fmcore as c
        run = json.loads(self.gen().stdout)["run"]
        self.fm("exam", "long", "run", run, "--agent", "oracle")
        os.remove(os.path.join(c.state_dir(), "prove-trusted.json"))
        r = self.fm("exam", "long", "grade", run, "--agent", "oracle", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fm prove", r.stderr)

    def test_a_runner_timeout_is_none_not_all_red_and_a_forged_key_is_refused(self):
        import fmlong
        t = os.path.join(self.tmp, "slow")
        write(t, "tests/test_s.py", "import time, unittest\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        time.sleep(30)\n")
        old, fmlong.RUN_T = fmlong.RUN_T, 1
        try:
            self.assertIsNone(fmlong._passed(t, ["tests/test_s.py::test_s.T.test_a"], ["tests"]))
        finally:
            fmlong.RUN_T = old
        key = {"id": "x", "checks": ["../x.py::a.B.c"], "sample": [], "files": [], "test_files": [], "pypath": [],
               "base": "0" * 40, "target": "0" * 40}
        with self.assertRaises(ValueError):
            fmlong._check_key(key)
        with self.assertRaises(ValueError):
            fmlong._check_key(dict(key, checks=[], target="--output=x"))

    def test_n_zero_and_a_gen_that_keeps_nothing_fail_without_a_run(self):
        fmprove.remember(self.src)
        self.assertNotEqual(self.fm("exam", "long", "gen", "--from", self.src, "--n", "0", check=False).returncode, 0)
        empty = os.path.join(self.tmp, "empty")
        subprocess.run(["git", "init", "-q", "-b", "main", empty], check=True)
        fmprove.remember(empty)
        r = self.fm("exam", "long", "gen", "--from", empty, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.gen().returncode, 0)
        import fmcore as c
        import fmlong
        self.assertEqual(os.listdir(fmlong._root(c.find_project(self.repo))), ["l001"])
