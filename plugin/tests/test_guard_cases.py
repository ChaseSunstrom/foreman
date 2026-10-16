"""T-1162: fm guard wrong stores a labelled guard case (plugin/tests/fixtures/guard_cases.jsonl); the guard is held to
every label here, fm replay --cases reports them, and fm night captures one FIX per drifted case."""
import json
import os

from helpers import ForemanTestCase

import fmreplay


class GuardCases(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.cases = os.path.join(self.tmp, "cases.jsonl")
        self.env = {"FOREMAN_GUARD_CASES": self.cases}

    def wrong(self, *a, check=True):
        return self.fm("guard", "wrong", *a, env=self.env, check=check)

    def test_the_repos_corpus_agrees_with_the_guard(self):
        cases = fmreplay.load_cases()
        self.assertEqual(fmreplay.drift(cases), [], "the guard disagrees with a labelled case")

    def test_a_case_is_stored_once_and_replay_reports_it(self):
        self.wrong("ls -la", "--should", "allow", "--why", "was refused")
        self.wrong("ls -la", "--should", "allow")  # again: no second row
        self.assertEqual(len(open(self.cases).read().splitlines()), 1)
        out = self.fm("replay", "--cases", "--json", env=self.env, check=False)
        self.assertEqual(out.returncode, 0)
        self.assertEqual(json.loads(out.stdout)["drifted"], 0)
        self.wrong("ls -la", "--should", "block", check=False)  # contradicts the stored label: refused
        self.assertEqual(len(open(self.cases).read().splitlines()), 1)

    def test_replay_fails_while_the_guard_disagrees(self):
        self.wrong("ls -la", "--should", "block")  # the guard allows ls
        out = self.fm("replay", "--cases", "--json", env=self.env, check=False)
        self.assertEqual(out.returncode, 1)
        res = json.loads(out.stdout)
        self.assertEqual((res["cases"], res["drifted"]), (1, 1))

    def test_a_key_shaped_literal_is_refused(self):
        r = self.wrong("curl -H 'Authorization: Bearer abcdef123456' x", "--should", "block", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(self.cases))

    def test_night_captures_one_fix_per_drift(self):
        self.fm("init")
        self.wrong("ls -la", "--should", "block")
        names = lambda: [j["name"] for j in json.loads(
            self.fm("night", "--dry-run", "--json", env=self.env).stdout)["jobs"]]
        self.assertIn("guard cases", names())
        for _ in range(2):
            self.fm("replay", "--cases", "--capture", env=self.env, check=False)
        import fmcore as c
        def fixes():  # read the files: this process's brief memo can't see another process's writes
            tdir = os.path.join(c.find_project(self.repo).dir, "tasks")
            return [t for t in (open(os.path.join(tdir, f)).read() for f in os.listdir(tdir)) if "Guard verdict drifted" in t]
        self.assertEqual(len(fixes()), 1)
        self.assertIn("FIX", fixes()[0])
        self.wrong("pwd", "--should", "block")  # a second drifted case: one more, not two
        r = self.fm("replay", "--cases", "--capture", env=self.env)
        self.assertEqual(len(fixes()), 2, r.stdout + r.stderr)
