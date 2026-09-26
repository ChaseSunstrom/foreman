"""fm repeats: procedures and commands a project keeps repeating, and what to turn them into (T-0023)."""
import json

from helpers import ForemanTestCase, git_repo


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
