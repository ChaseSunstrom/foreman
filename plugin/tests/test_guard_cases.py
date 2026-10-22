"""T-1162: fm guard wrong stores a labelled guard case (plugin/tests/fixtures/guard_cases.jsonl); the guard is held to
every label here, fm replay --cases reports them, and fm night captures one FIX per drifted case."""
import json
import os
import tempfile
from unittest import mock

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
        # T-1284: a case in /tmp means "where Foreman's temp fallback lives" (tempfile's folder: /tmp on Linux, a
        # /var/folders/… one on macOS), so the corpus runs with the temp folder pinned to /tmp on every platform
        # T-1291: drift itself pins it, so a different TMPDIR (macOS, /var/tmp) can't make the /tmp case drift
        with mock.patch.object(tempfile, "tempdir", "/var/tmp"):
            self.assertEqual(fmreplay.drift(cases), [], "the guard disagrees with a labelled case")
            self.assertEqual(tempfile.tempdir, "/var/tmp", "verdicts must restore tempfile's folder")

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


ALLOW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "guard_allow.jsonl")


class AllowCorpus(ForemanTestCase):
    """T-1517: the safety ratchet. Everyday commands the guard must pass (a false block is a cost too), the guard's own
    files locked against fm evolve, and a check that couldn't run is reported unable, never a pass."""

    def test_every_everyday_command_passes(self):
        cases, broken = fmreplay.load_cases(ALLOW)
        self.assertEqual(broken, 0, "a line of guard_allow.jsonl is not a case")
        self.assertGreaterEqual(len(cases), 40)
        self.assertEqual({k["should"] for k in cases}, {"allow"}, "the allow corpus holds allow labels only")
        self.assertEqual(len({k["id"] for k in cases}), len(cases), "an id twice")
        # a temp Foreman home, then this checkout as Foreman's own (the main checkout is protected core): a case whose
        # verdict depends on the tree would turn the real replay red there while passing in a lane
        import fmguard
        for home in (self.home, fmreplay._corpus_root()):
            env = {"FOREMAN_HOME": home, "FOREMAN_STATE": os.path.join(self.tmp, "state")}
            with self.subTest(home=home), mock.patch.dict(os.environ, env), \
                    mock.patch.object(tempfile, "tempdir", "/var/tmp"):
                for v in fmguard._PY_PATH_VARS:  # an inherited PYTHONPATH rightly makes every python3 -c suspect
                    os.environ.pop(v, None)
                self.assertEqual([(k["cmd"], k["got"]) for k in fmreplay.drift(cases)], [])

    def test_the_replay_holds_both_corpora(self):
        with mock.patch.dict(os.environ):
            os.environ.pop("FOREMAN_GUARD_CASES", None)  # the committed files, as fm replay --cases reads them
            cases, broken = fmreplay.load_cases()
        self.assertEqual(broken, 0)
        where = [fmreplay._where(k) for k in cases]
        self.assertEqual(len(where), len(set(where)), "a command and folder both files hold is replayed once")
        for path in (ALLOW, fmreplay.cases_path()):
            self.assertLessEqual({fmreplay._where(k) for k in fmreplay.load_cases(path)[0]}, set(where), path)

    def _default(self, cases_lines, allow_lines):
        """load_cases() in its default mode over two temp files (None: that file is missing)."""
        paths = []
        for name, lines in (("cases.jsonl", cases_lines), ("allow.jsonl", allow_lines)):
            paths.append(os.path.join(self.tmp, name))
            if lines is None and os.path.exists(paths[-1]):
                os.remove(paths[-1])
            elif lines is not None:
                with open(paths[-1], "w") as f:
                    f.write("".join(json.dumps(x) + "\n" for x in lines))
        with mock.patch.dict(os.environ), mock.patch.object(fmreplay, "cases_path", return_value=paths[0]), \
                mock.patch.object(fmreplay, "allow_path", return_value=paths[1]):
            os.environ.pop("FOREMAN_GUARD_CASES", None)
            return fmreplay.load_cases()

    def _allow(self, n, cwd="."):
        return [{"id": f"a{i}", "cmd": f"echo {i}", "cwd": cwd, "should": "allow"} for i in range(n)]

    def test_a_missing_or_cut_down_allow_corpus_is_broken_not_skipped(self):
        floor = self._allow(fmreplay.ALLOW_MIN)
        self.assertEqual(self._default([], floor)[1], 0)
        self.assertEqual(self._default([], None)[1], 1, "a missing allow-corpus")
        self.assertEqual(self._default([], [])[1], 1, "an emptied allow-corpus")
        self.assertEqual(self._default([], floor[:-1])[1], 1, "one under the floor")

    def test_both_files_meet_on_command_and_folder_not_id(self):
        floor = self._allow(fmreplay.ALLOW_MIN)
        same = {"id": "other-id", "cmd": "echo 0", "cwd": ".", "should": "allow"}
        cases, broken = self._default([same], floor)
        self.assertEqual((len(cases), broken), (fmreplay.ALLOW_MIN, 0), "one command and folder, one case")
        cases, broken = self._default([dict(same, should="block")], floor)
        self.assertEqual(broken, 1, "opposite labels for one command and folder are refused, not settled by order")
        self.assertEqual(sorted(k["should"] for k in cases if k["cmd"] == "echo 0"), ["allow", "block"])

    def test_a_label_contradicting_the_allow_corpus_is_refused_and_names_it(self):
        import fmcli
        mine, allow = os.path.join(self.tmp, "mine.jsonl"), os.path.join(self.tmp, "allow.jsonl")
        with open(allow, "w") as f:  # an id that isn't _key's: the command and folder decide
            f.write(json.dumps({"id": "hand-written", "cmd": "ls -la", "cwd": self.repo, "should": "allow"}) + "\n")
        with mock.patch.dict(os.environ), mock.patch.object(fmreplay, "allow_path", return_value=allow), \
                mock.patch.object(fmreplay, "cases_path", return_value=mine):
            os.environ.pop("FOREMAN_GUARD_CASES", None)
            with self.assertRaises(fmcli.UsageError) as e:
                fmreplay.add_case("ls -la", "block", cwd=self.repo)
            self.assertEqual(fmreplay.add_case("ls -la", "allow", cwd=self.repo)["id"], "hand-written")
        self.assertIn(allow, str(e.exception))
        self.assertFalse(os.path.exists(mine), "the refused label was stored")

    def test_evolve_never_revises_the_guards_own_files(self):
        import fmbudget
        import fmevolve
        targets = [("plugin/lib/fmguard.py", "plugin"), ("plugin/lib/fmhooks.py", "plugin"),
                   ("plugin/lib/fmreplay.py", "plugin"), ("plugin/lib/fmevolve.py", "plugin"),  # its replay, this lock
                   ("plugin/lib/fmmutate.py", "plugin"), ("plugin/lib/fmbench.py", "plugin"),  # mutants, the bench gate
                   ("plugin/hooks/hook", "plugin"), ("plugin/hooks/hooks.json", "plugin"),
                   ("plugin/tests/test_guard_cases.py", "plugin"), ("plugin/tests/test_guard.py", "plugin"),
                   ("plugin/tests/fixtures/guard_allow.jsonl", "plugin"),
                   ("plugin/tests/fixtures/gen_evasions.py", "plugin"),
                   ("plugin/skills/../lib/fmguard.py", "plugin"),  # a dot-dot walk to it
                   ("plugin/hooks/rules/x.md", "plugin/hooks")]  # an instruction-shaped name under the hooks
        with mock.patch.object(fmevolve, "mutate", side_effect=AssertionError("the child ran")), \
                mock.patch.object(fmbudget, "check"):
            for target, plugin_dir in targets:
                with self.subTest(target=target), self.assertRaises(ValueError) as e:
                    fmevolve.generation(None, self.repo, target, plugin_dir, cases=[])
                self.assertIn("the guard's own", str(e.exception))

    def test_evolve_refuses_a_link_or_a_folder_in_place_of_an_instruction_file(self):
        # written through in the candidate's worktree, a symlinked SKILL.md would put the child's text into the guard
        import subprocess
        import fmbench
        import fmbudget
        import fmevolve
        plugin = os.path.join(self.repo, "plugin")
        for d in ("lib", "skills/x", "skills/d.md"):
            os.makedirs(os.path.join(plugin, d))
        for name in ("lib/fmguard.py", "lib/notes.md", "skills/d.md/inner.md"):
            with open(os.path.join(plugin, name), "w") as f:
                f.write("GUARD = 1\n")
        os.symlink("../../lib/fmguard.py", os.path.join(plugin, "skills", "x", "SKILL.md"))  # a linked file
        os.symlink("../lib", os.path.join(plugin, "skills", "y"))  # a linked parent folder
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "links"], check=True)
        calls, real = [], fmbench._safe_git

        def spy(repo, *a, **k):
            calls.append(a)
            return real(repo, *a, **k)
        with mock.patch.object(fmevolve, "mutate", side_effect=AssertionError("the child ran")), \
                mock.patch.object(fmbudget, "check"), mock.patch.object(fmbench, "_safe_git", spy):
            for target, why in (("plugin/skills/x/SKILL.md", "not a plain file"),
                                ("plugin/skills/y/notes.md", "isn't committed"),  # git never walks a linked folder
                                ("plugin/skills/d.md", "not a plain file")):
                with self.subTest(target=target), self.assertRaises(ValueError) as e:
                    fmevolve.generation(None, self.repo, target, cases=[])
                self.assertIn(why, str(e.exception))
        head = subprocess.run(["git", "-C", self.repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout
        reads = [a for a in calls if a[0] in ("show", "ls-tree")]
        self.assertTrue(reads)
        self.assertTrue(all(head.strip() in " ".join(a) for a in reads), f"read at symbolic HEAD, not the pinned "
                                                                         f"commit: {reads}")

    def test_an_unrunnable_check_reports_unable(self):
        # the guard crashing on a should-block case was counted a pass: a refusal is what the label wanted
        import fmguard
        cases = [{"id": "a", "cmd": "rm -rf ~", "cwd": "", "should": "block"},
                 {"id": "b", "cmd": "ls", "cwd": "", "should": "allow"}]
        with mock.patch.object(fmguard, "check", side_effect=RuntimeError("the parser broke")):
            got = fmreplay.drift(cases)
        self.assertEqual(sorted((k["id"], k["got"]) for k in got), [("a", "unable"), ("b", "unable")])

    def test_the_replay_reports_unable_and_fails(self):
        import types
        import fmcli
        import fmguard
        path = os.path.join(self.tmp, "unable.jsonl")
        with open(path, "w") as f:
            f.write(json.dumps({"id": "a", "cmd": "rm -rf ~", "cwd": "", "should": "block"}) + "\n")
        args = types.SimpleNamespace(json=True, capture=False)
        with mock.patch.dict(os.environ, {"FOREMAN_GUARD_CASES": path}), \
                mock.patch.object(fmguard, "check", side_effect=RuntimeError("the parser broke")), \
                mock.patch("builtins.print") as out, self.assertRaises(SystemExit) as e:
            fmreplay.report_cases(args, fmcli)
        self.assertEqual(e.exception.code, 1)
        res = json.loads("".join(str(x.args[0]) for x in out.call_args_list if x.args))
        self.assertEqual((res["drifted"], res["unable"]), (1, 1))

    def _run_json(self, fn, *a):
        """(exit code, the JSON fn printed)."""
        with mock.patch("builtins.print") as out:
            try:
                fn(*a)
                code = 0
            except SystemExit as e:
                code = e.code
        return code, json.loads("".join(str(x.args[0]) for x in out.call_args_list if x.args))

    def test_a_candidate_that_cannot_judge_never_scores_clean(self):
        # fm replay --candidate: a check() that always raises tightened every allow and recategorised every block
        import types
        import fmcli
        import fmguard

        def broken(*a, **k):
            raise RuntimeError("the candidate broke")
        cand = types.SimpleNamespace(Ctx=fmguard.Ctx, project_root_for=fmguard.project_root_for, check=broken)
        cmds = [("ls", self.repo), ("rm -rf ~", "")]
        with mock.patch.object(fmreplay, "candidate", return_value=cand), \
                mock.patch.object(fmreplay, "corpus", return_value=cmds):
            code, res = self._run_json(fmreplay.score, types.SimpleNamespace(candidate="x", days=7, json=True), fmcli)
        self.assertEqual(code, 1)
        self.assertEqual((res["unable"], res["loosened"], res["tightened"], res["recategorised"]), (2, 0, 0, 0))

    def test_the_plain_replay_reports_unable_and_never_accepts_it(self):
        import types
        import fmcli
        import fmguard
        args = types.SimpleNamespace(cases=False, candidate=None, cwd=None, cmd=None, days=7, accept=True, json=True)
        with mock.patch.object(fmreplay, "corpus", return_value=[("ls", self.repo)]), \
                mock.patch.object(fmguard, "check", side_effect=RuntimeError("the parser broke")):
            code, res = self._run_json(fmreplay.cmd_replay, args)
        self.assertEqual((code, res["unable"], res["newly_blocked"]), (1, 1, 0))
        with open(fmreplay._baseline_path()) as f:
            self.assertEqual(json.load(f)["verdicts"], {}, "an error taken as the baseline would pass from then on")

    def test_friction_says_unable_not_still_blocks(self):
        import fmfriction
        import fmguard
        events = [{"tool": "Bash", "cmd": "ls", "session_id": "s1"}]
        with mock.patch.object(fmfriction, "_transcript_commands", return_value={("s1", "ls"): ("ls", self.repo)}), \
                mock.patch.object(fmguard, "check", side_effect=RuntimeError("the parser broke")):
            self.assertIn("unable", fmfriction._recheck(events)[0])
