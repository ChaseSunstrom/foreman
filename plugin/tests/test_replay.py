"""T-0189: fm replay runs the real shell commands of recent Claude Code sessions through the current guard and reports
what a guard change now blocks (a likely false positive) or now lets through (a possible bypass), against the verdicts
last accepted. The baseline holds hashes and verdicts, never a command."""
import json
import os
import unittest

from helpers import ForemanTestCase


class Replay(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")
        log = os.path.join(self.uhome, ".claude", "projects", "-work-app", "s1.jsonl")
        os.makedirs(os.path.dirname(log))
        calls = [("ls -la", self.repo), ("git push --force origin main", self.repo), ("echo hi > notes.txt", self.repo),
                 ("ls -la", self.repo)]  # the same command in the same folder counts once
        with open(log, "w") as f:
            for cmd, cwd in calls:
                f.write(json.dumps({"type": "assistant", "cwd": cwd, "message": {"content": [
                    {"type": "tool_use", "name": "Bash", "input": {"command": cmd}}]}}) + "\n")
            f.write("not json\n")  # a torn line is skipped

    def replay(self, *args, check=False):
        return self.fm("replay", *args, env={"HOME": self.uhome}, check=check)

    def test_replay_reports_changed_verdicts_until_accepted(self):
        first = self.replay()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)  # nothing to compare with yet
        self.assertIn("3 real commands", first.stdout)
        self.assertEqual(self.replay("--accept").returncode, 0)
        base = os.path.join(self.home, "state", "guard-replay.json")
        if not os.path.exists(base):
            base = next(os.path.join(r, f) for r, _, fs in os.walk(self.tmp) for f in fs if f == "guard-replay.json")
        text = open(base).read()
        self.assertNotIn("git push", text)  # hashes and verdicts only
        data = json.loads(text)
        self.assertEqual(sorted(data["verdicts"].values()), ["allow", "allow", "git-destructive"])
        # a guard that used to let the push through, and used to block the listing: both changes are reported
        flip = {k: ("allow" if v == "git-destructive" else "core" if v == "allow" else v) for k, v in data["verdicts"].items()}
        with open(base, "w") as f:
            json.dump({**data, "verdicts": flip}, f)
        out = self.replay()
        self.assertEqual(out.returncode, 1, out.stdout)
        self.assertIn("newly blocked", out.stdout)
        self.assertIn("git push --force origin main", out.stdout)
        self.assertIn("newly allowed", out.stdout)
        self.assertEqual(self.replay("--accept").returncode, 0)
        self.assertEqual(self.replay().returncode, 0)

    def test_bench_guard_coverage_names_untested_rules(self):
        cmds = os.path.join(self.tmp, "cmds.txt")
        with open(cmds, "w") as f:
            f.write("rm -rf /\n")
        out = self.fm("bench", "guard", "--coverage", "--cmds", cmds, "--json", env={"HOME": self.uhome}, check=False)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)  # some rule is untested
        data = json.loads(out.stdout)
        self.assertEqual(data["caught"], ["rm-outside"])
        self.assertNotIn("rm-outside", data["untested"])
        self.assertIn("git-destructive", data["untested"])
        self.assertEqual(len(data["caught"]) + len(data["untested"]), 14)

    def test_mutation_names_the_rule_no_test_catches(self):
        import fmmutate
        d = os.path.join(self.tmp, "fixture")
        os.makedirs(d)
        with open(os.path.join(d, "rules.py"), "w") as f:
            f.write("def check(x):\n    out = []\n    if x == 1:\n        out.append(('red', 'one'))\n"
                    "    if x == 2:\n        out.append(('blue', 'two'))\n    return out\n")
        with open(os.path.join(d, "t.py"), "w") as f:  # tests the red rule only
            f.write("import rules\nassert rules.check(1) == [('red', 'one')]\n")
        import sys
        kw = dict(tree_root=d, dest="fixture", cmd=[sys.executable, "fixture/t.py"], cats=["red", "blue"],
                  module=os.path.join(d, "rules.py"), rel="fixture/rules.py")
        res = fmmutate.run(**kw)
        self.assertEqual(res["killed"], 1, res)
        self.assertEqual([(m["line"], m["category"]) for m in res["survived"]], [(6, "blue")], res)
        # negating blue's guard changes what check(1) returns, which the red test notices: both weakened mutants die
        res = fmmutate.run(weaken=True, **kw)
        self.assertEqual((res["killed"], res["survived"]), (2, []), res)


if __name__ == "__main__":
    unittest.main()
