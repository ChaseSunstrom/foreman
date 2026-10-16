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
        # no real transcripts: plain `fm replay` would otherwise replay this machine's sessions (slow, machine-specific)
        self.env = {"FOREMAN_GUARD_CASES": self.cases, "CLAUDE_CONFIG_DIR": os.path.join(self.tmp, "claude")}

    def wrong(self, *a, check=True):
        return self.fm("guard", "wrong", *a, env=self.env, check=check)

    def test_the_repos_corpus_agrees_with_the_guard(self):
        # the committed file itself: FOREMAN_GUARD_CASES and a missing file can't make this pass vacuously
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "guard_cases.jsonl")
        cases, broken = fmreplay.load_cases(path)
        self.assertEqual(broken, 0, "a line of guard_cases.jsonl is not a case")
        self.assertGreaterEqual(len(cases), 6)
        self.assertEqual(fmreplay.drift(cases), [], "the guard disagrees with a labelled case")

    def test_a_test_without_the_env_never_writes_the_real_corpus(self):
        # T-1197: a temp repo has no plugin/, so the corpus fell back to the real checkout's and tests wrote junk to it
        real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "guard_cases.jsonl")
        with open(real, "rb") as f:
            before = f.read()
        try:
            self.fm("guard", "wrong", "echo t1197", "--should", "allow", "--why", "x")
            with open(real, "rb") as f:
                self.assertEqual(f.read(), before)
        finally:
            with open(real, "rb") as f:
                if f.read() != before:
                    with open(real, "wb") as g:
                        g.write(before)

    def test_a_broken_line_is_counted_not_fatal(self):
        with open(self.cases, "w") as f:
            f.write('<<<<<<< HEAD\n{"id": "x"}\n{"id": "y", "cmd": "ls", "should": "allow"\n')
        self.wrong("ls -la", "--should", "allow")  # still adds
        cases, broken = fmreplay.load_cases(self.cases)
        self.assertEqual((len(cases), broken), (1, 3))
        out = self.fm("replay", "--cases", "--json", env=self.env, check=False)
        self.assertEqual(out.returncode, 1)  # a broken corpus is seen
        self.assertEqual(json.loads(out.stdout)["broken"], 3)

    def test_cwd_inside_the_repo_is_stored_relative(self):
        repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.wrong("ls -la", "--should", "allow", "--cwd", os.path.join(repo, "plugin"))
        self.assertEqual(json.loads(open(self.cases).read())["cwd"], "plugin")
        self.assertEqual(fmreplay.resolve_cwd("plugin"), os.path.join(fmreplay.repo_root(), "plugin"))

    def test_a_second_checkout_gets_its_own_case(self):
        # T-1175: run inside another Foreman checkout, the case goes to that checkout's corpus, cwd relative to it
        co = os.path.join(self.tmp, "co")
        os.makedirs(os.path.join(co, "plugin", "lib"))
        os.makedirs(os.path.join(co, "sub"))
        open(os.path.join(co, "plugin", "lib", "fmguard.py"), "w").close()
        main = os.path.join(fmreplay.c.PLUGIN_ROOT, "tests", "fixtures", "guard_cases.jsonl")
        before = open(main).read()
        self.fm("guard", "wrong", "ls -la", "--should", "allow", cwd=os.path.join(co, "sub"),
                env={"FOREMAN_GUARD_CASES": ""})  # the fallback itself, not the test default
        mine = os.path.join(co, "plugin", "tests", "fixtures", "guard_cases.jsonl")
        self.assertEqual(json.loads(open(mine).read())["cwd"], "sub")
        self.assertEqual(open(main).read(), before)

    def test_the_night_job_is_for_foremans_own_repo_only(self):
        from unittest import mock
        import fmcore as c
        import fmnight
        self.fm("init")
        self.wrong("ls -la", "--should", "allow")
        p = c.find_project(self.repo)
        with mock.patch.dict(os.environ, self.env):
            self.assertNotIn("guard cases", [n for n, _, _ in fmnight.jobs(p)])
            with mock.patch.object(c, "PLUGIN_ROOT", os.path.join(self.repo, "plugin")):
                self.assertIn("guard cases", [n for n, _, _ in fmnight.jobs(p)])

    def test_an_allow_label_the_guard_blocks_warns_against_loosening(self):
        import fmcore as c
        self.fm("init")
        self.wrong("git push --force origin main", "--should", "allow")
        self.fm("replay", "--cases", "--capture", env=self.env, check=False)
        tdir = os.path.join(c.find_project(self.repo).dir, "tasks")
        text = "".join(open(os.path.join(tdir, f)).read() for f in os.listdir(tdir))
        self.assertIn("do not loosen the guard without the user's yes", text)

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

    def test_the_replay_gate_holds_the_labels_too(self):
        # T-1182: the gate is plain `fm replay`; a drifted label must fail it, not only `fm replay --cases`
        self.wrong("ls", "--should", "allow")
        self.assertEqual(self.fm("replay", env=self.env, check=False).returncode, 0)
        self.wrong("ls -la", "--should", "block")  # the guard allows ls -la: drifted
        out = self.fm("replay", env=self.env, check=False)
        self.assertEqual(out.returncode, 1)
        self.assertIn("ls -la", out.stdout)

    def test_a_key_shaped_literal_is_refused(self):
        r = self.wrong("curl -H 'Authorization: Bearer abcdef123456' x", "--should", "block", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(self.cases))

    def test_night_captures_one_fix_per_drift(self):
        self.fm("init")
        self.wrong("ls -la", "--should", "block")
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
