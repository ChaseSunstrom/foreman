"""fm repeats: procedures and commands a project keeps repeating, and what to turn them into (T-0023)."""
import json
import os

from helpers import ForemanTestCase, git_repo

import fmcore as c


class Repeats(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        for i in range(1, 4):
            tid = self.fm_json("task", "new", f"Fix bug {i}", "--type", "FIX", "--tier", "S",
                               "--step", "Write a failing test", "--step", f"fix bug {i}",
                               "--step", "Update the CHANGELOG.")["id"]
            self.fm("task", "evidence", tid, "--step", "1", f"python3 -m unittest tests.test_bug{i} -q", "1 failed")
            self.fm("task", "evidence", tid, "--step", "2", "python3 -m unittest discover -s tests", f"Ran {40 + i} OK")
            self.fm("task", "evidence", tid, "--step", "2", "npm run build && npm run lint", "ok")
            self.fm("task", "evidence", tid, "--step", "3", f"fm task log {tid} 'done'", "logged")
        self.fm("task", "evidence", "T-0001", "--step", "2", "cargo fmt --check", "ok")  # once: not a repeat

    def report(self):
        return self.fm_json("repeats")

    def test_repeated_commands_and_procedures_with_what_to_make_of_them(self):
        r = self.report()
        cmds = {x["shape"]: x for x in r["commands"]}
        self.assertEqual(cmds["python3 -m unittest …"]["count"], 6)
        self.assertEqual(cmds["python3 -m unittest …"]["tasks"], 3)
        self.assertIn("fm check add", cmds["python3 -m unittest …"]["suggest"])
        self.assertIn("script", cmds["npm run build && npm run lint"]["suggest"])
        self.assertFalse(any(s.startswith(("fm ", "cargo")) for s in cmds), "Foreman's own commands and one-offs")
        steps = {x["step"]: x for x in r["steps"]}
        self.assertEqual(set(steps), {"write a failing test", "update the changelog"})
        self.assertIn(".claude/skills/", steps["write a failing test"]["suggest"])

    def test_interpreter_flags_do_not_split_a_habit_and_git_reads_are_not_habits(self):
        import fmrepeats
        self.assertEqual(fmrepeats.shape("python3 -W error::ResourceWarning -m unittest discover -s x"),
                         fmrepeats.shape("python3 -m unittest test_a"))
        for i in range(1, 4):
            self.fm("task", "evidence", f"T-000{i}", "--step", "2", "git log --oneline -1", "abc123 fix")
        self.assertFalse(any(x["shape"].startswith("git log") for x in self.report()["commands"]))

    def test_a_narrowed_test_run_is_never_offered_as_a_gate(self):
        # T-0857: this repo was told to make "unittest … -p test_diff_gates.py -k dirty" a gate for every task
        import fmrepeats
        for narrow in ("python3 -m unittest discover -s t -q -p test_diff_gates.py -k dirty",
                       "python3 plugin/tests/run.py test_bus", "pytest tests/test_a.py::test_b", "pytest -k slow"):
            self.assertNotIn("fm check add", fmrepeats.suggest("python3 -m unittest …", narrow), narrow)
        cmds = {x["shape"]: x for x in self.report()["commands"]}  # the habit holds both kinds: the whole-suite one
        self.assertIn('fm check add "python3 -m unittest discover -s tests"', cmds["python3 -m unittest …"]["suggest"])

    def test_gate_words_count_in_the_command_not_in_directory_names(self):
        import fmrepeats
        self.assertIn("fm check add", fmrepeats.suggest("python3 plugin/tests/bench_hooks.py --runs …", "x"))
        self.assertNotIn("fm check add", fmrepeats.suggest("cp dist/build/app.js …", "x"))
        self.assertNotIn("fm check add", fmrepeats.suggest("git checkout main", "x"))
        self.assertEqual(fmrepeats.shape("cd sub &&"), "")

    def test_handled_items_can_be_dismissed_and_bad_meta_is_ignored(self):
        # round-2 audits: a repeat turned into a script or skill stops being reported; a stray non-string gate is skipped
        self.fm("repeats", "dismiss", "npm run build && npm run lint")
        self.fm("repeats", "dismiss", "Write a failing test.")
        r = self.report()
        self.assertNotIn("npm run build && npm run lint", {x["shape"] for x in r["commands"]})
        self.assertEqual({x["step"] for x in r["steps"]}, {"update the changelog"})
        self.assertIn("2 dismissed", self.fm("repeats").stdout)
        p = c.find_project(self.repo)
        c.update_meta(p, checks=[None, 3, "python3 -m unittest discover -s tests"])
        self.assertTrue({x["shape"]: x for x in self.report()["commands"]}["python3 -m unittest …"]["covered"])
        self.assertEqual(self.fm("tidy", check=False).returncode, 0)

    def test_commands_fm_check_already_runs_are_marked_covered(self):
        self.fm("check", "add", "python3 -m unittest discover -s tests")
        cmds = {x["shape"]: x for x in self.report()["commands"]}
        self.assertTrue(cmds["python3 -m unittest …"]["covered"])
        self.assertFalse(cmds["npm run build && npm run lint"]["covered"])
        out = self.fm("repeats").stdout
        self.assertIn("covered by fm check", out)
        self.assertIn("npm run build && npm run lint", out)

    def test_tidy_counts_what_could_become_a_project_tool(self):
        found = [f for f in json.loads(self.fm("tidy", "--json").stdout)["findings"] if f["kind"] == "repeats"]
        self.assertEqual(len(found), 1)
        self.assertIn("fm repeats", found[0]["fix"])

    def test_nothing_repeated(self):
        fresh = git_repo(self.tmp, "fresh")
        self.fm("init", cwd=fresh)
        self.assertIn("Nothing repeated", self.fm("repeats", cwd=fresh).stdout)
        self.assertEqual(self.fm_json("repeats", cwd=fresh), {"commands": [], "steps": []})

    def test_forge_drafts_a_script_and_a_skill_and_files_one_task_each_once(self):
        # T-1070: nothing is adopted; the draft sits in research/ and a captured task carries its path
        paths = {d["path"]: d["task"] for d in self.fm_json("repeats", "--forge")["drafts"]}
        script = next(x for x in paths if x.endswith(".sh") and "npm" in open(x).read())
        self.assertIn("npm run build && npm run lint", open(script).read())
        skill = next(x for x in paths if x.endswith("SKILL.md") and "Write a failing test" in open(x).read())
        gate = next(x for x in paths if x.endswith(".sh") and "unittest" in open(x).read())
        self.assertIn("fm check add", open(gate).read())
        p = c.find_project(self.repo)
        rel = os.path.relpath(script, p.dir)
        self.assertEqual(len([b for b in c.load_briefs(p) if rel in b.section("Raw request")]), 1)
        self.assertEqual(self.fm_json("repeats", "--forge")["drafts"], [], "a second run files nothing new")
        self.assertEqual(len([b for b in c.load_briefs(p) if rel in b.section("Raw request")]), 1)

    def test_forge_repairs_a_missing_draft_without_a_new_task_and_files_a_real_task(self):
        import os
        d = self.fm_json("repeats", "--forge")["drafts"][0]
        self.assertEqual(os.stat(d["path"]).st_mode & 0o111, 0, "a draft is never executable")
        p = c.find_project(self.repo)
        n = len(c.load_briefs(p))
        b = c.find_brief(p, d["task"])
        self.assertTrue(b.title.startswith("Adopt forge draft: "))
        self.assertIn("Forge draft: research/forge-", b.section("Raw request"))
        self.assertEqual(len(b.steps()), 1)
        self.assertTrue(b.acceptance())
        os.remove(d["path"])
        again = self.fm_json("repeats", "--forge")["drafts"]
        self.assertEqual(again, [{"path": d["path"], "task": d["task"]}])
        self.assertTrue(os.path.exists(d["path"]))
        self.assertEqual(len(c.load_briefs(p)), n)

    def test_forge_keeps_long_shared_prefixes_apart_and_redacts_and_quotes(self):
        prefix = "./deploy-to-the-staging-cluster.sh --target"  # one 40+ character prefix, two shapes
        for i in range(1, 4):
            tid = self.fm_json("task", "new", f"Deploy {i}", "--type", "FIX", "--tier", "S", "--step", "s")["id"]
            for tail in ("alpha && ./a", "beta && ./b --token ghp_" + "a1B2" * 9):
                self.fm("task", "evidence", tid, "--step", "1", f"{prefix} {tail}", "ok")
        paths = [d["path"] for d in self.fm_json("repeats", "--forge")["drafts"] if "deploy" in d["path"]]
        self.assertEqual(len(paths), 2)
        self.assertEqual(len(set(paths)), 2)
        self.assertFalse(any("ghp_" in open(x).read() for x in paths))
        self.assertTrue(any("[REDACTED" in open(x).read() for x in paths))

    def test_forge_skips_dismissed_shapes(self):
        self.fm("repeats", "dismiss", "npm run build && npm run lint")
        self.fm("repeats", "dismiss", "Write a failing test.")
        for d in self.fm_json("repeats", "--forge")["drafts"]:
            self.assertNotIn("npm run", open(d["path"]).read())
            self.assertNotIn("Write a failing test", open(d["path"]).read())
