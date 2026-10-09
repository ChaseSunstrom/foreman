"""T-0686 (Intelligence — debugging and diagnosis): prove the diagnosis, say why it wasn't caught, escalate when stuck,
bisect history, and fingerprint failures."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def commit(self, msg):
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)
        return subprocess.run(["git", "-C", self.repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


class Prove(Base):
    def test_the_fix_removed_is_red_and_the_fix_is_green(self):
        self.write("calc.py", "def add(a, b):\n    return a - b\n")
        self.commit("bug")
        self.fm("task", "new", "Fix add", "--type", "FIX", "--tier", "S", "--ac", "adds :: python3 test_calc.py",
                "--step", "fix", "--focus")
        self.write("test_calc.py", "import calc\nassert calc.add(1, 2) == 3\n")
        self.write("calc.py", "def add(a, b):\n    return a + b\n")
        out = self.fm("task", "prove", "T-0001", "--run", "python3 test_calc.py").stdout
        self.assertRegex(out.lower(), r"red|fail")
        self.assertTrue(c.find_brief(self.p, "T-0001").red_green())


class WhyNotCaught(Base):
    def test_a_fix_says_why_it_was_not_caught_and_the_answer_becomes_a_followup(self):
        self.fm("task", "new", "Fix it", "--type", "FIX", "--tier", "M", "--ac", "ok :: true", "--step", "s")
        for sec in ("Interpretation", "Approach (options → choice → why)"):
            self.fm("task", "set", "T-0001", "--section", sec, "--text", "planned")
        self.fm("focus", "T-0001")
        self.fm("task", "set", "T-0001", "--section", "Regression test", "--text", "none: a typo")
        close = ["task", "finish", "T-0001", "--audit", "self", "--run", "true", "--lens", "intent: ok",
                 "--lens", "edge: ok", "--docs", "none: internal", "--lesson", "none: trivial"]
        r = self.fm(*close, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("why-not-caught", r.stdout + r.stderr)
        self.fm(*close, "--why-not-caught", "no test feeds an empty CSV to the exporter")
        kids = [b for b in c.load_briefs(self.p) if b.meta.get("source") == "followup"]
        self.assertTrue(any("empty CSV" in b.title for b in kids), [b.title for b in kids])


class Ladder(Base):
    def test_the_next_rung_follows_failed_runs_and_open_hypotheses(self):
        self.fm("task", "new", "Fix flake", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        for _ in range(2):
            self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "false", check=False)
        self.assertIn("fm-debugger", self.fm("next").stdout)
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "false", check=False)
        self.fm("task", "hypo", "T-0001", "add", "the cache is stale", "--probe", "ls")
        self.fm("task", "hypo", "T-0001", "add", "the clock skews", "--probe", "date")
        self.assertIn("differential", self.fm("next").stdout)


class Bisect(Base):
    def test_the_first_bad_commit_is_named(self):
        self.write("ok.txt", "ok\n")
        good = self.commit("good")
        self.write("n.txt", "1\n")
        self.commit("unrelated")
        self.write("ok.txt", "broken\n")
        self.commit("break the ok file")
        self.write("m.txt", "2\n")
        self.commit("later")
        out = self.fm("bisect", "--run", "grep -qx ok ok.txt", "--good", good, check=False).stdout
        self.assertIn("break the ok file", out)
        self.assertIn("ok.txt", out)


class Fingerprint(Base):
    def test_failing_gates_are_fingerprinted_and_fix_magnets_ranked(self):
        self.fm("check", "add", "python3 -c 'raise SystemExit(\"boom: config missing\")'")
        self.fm("check", check=False)
        recs = c.tail_jsonl(os.path.join(self.p.dir, "failures.jsonl"), 50)
        self.assertTrue(any("config missing" in str(r.get("sig")) for r in recs), recs)
        for title in ("Fix parser crash", "Fix parser BOM"):
            tid = json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--json").stdout)["id"]
            c.log_event(self.p, "touched", task=tid, data={"file": os.path.join(self.repo, "parse.py")})
        c.log_event(self.p, "touched", task="T-0099", data={"file": os.path.join(self.repo, "ui.py")})
        out = self.fm("recall", "--magnets").stdout
        self.assertRegex(out, r"parse\.py.*2 fix")
