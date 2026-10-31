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
        self.assertEqual([(x["agent"], x["true_done"], x["model"]) for x in long], [("oracle", 2, "default"), ("empty", 0, "default")])

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
