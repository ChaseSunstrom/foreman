"""T-0189: fm replay runs the real shell commands of recent Claude Code sessions through the current guard and reports
what a guard change now blocks (a likely false positive) or now lets through (a possible bypass), against the verdicts
last accepted. The baseline holds hashes and verdicts, never a command."""
import json
import os
import subprocess
import unittest

from helpers import FM, ForemanTestCase

import fmguard as g


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
        self.assertEqual(len(data["caught"]) + len(data["untested"]), len(g.CATEGORIES))

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

    def test_mutation_uses_the_checkout_it_runs_in(self):
        # T-1121: run from a builder's worktree, it mutated the main checkout's guard (the fm on PATH), not the lane's
        lane = os.path.join(self.tmp, "lane")
        os.makedirs(os.path.join(lane, "plugin", "lib"))
        with open(os.path.join(lane, "plugin", "lib", "fmguard.py"), "w") as f:
            f.write("def check(x):\n    out = []\n    out.append(('core', 'one'))\n    return out\n")
        r = subprocess.run([FM, "bench", "guard", "--mutate", "--tests", "true", "--json"], cwd=lane, capture_output=True,
                           text=True, env=dict(os.environ, FOREMAN_HOME=self.home))
        self.assertEqual(json.loads(r.stdout)["total"], 1, r.stdout + r.stderr)

    def test_flip_mode_flips_operators_inside_check_functions(self):
        # T-1121: the old mutate_guard.py's operator flips, folded into fm bench guard --mutate --flip
        import sys
        import fmmutate
        d = os.path.join(self.tmp, "flipfix")
        os.makedirs(d)
        with open(os.path.join(d, "rules.py"), "w") as f:
            f.write("def check(x):\n    return x == 1\n\n\ndef check_big(y):\n    return y > 5\n\n\n"
                    "def helper(z):\n    return z == 0\n")
        with open(os.path.join(d, "t.py"), "w") as f:  # tests check only; helper isn't a check function
            f.write("import rules\nassert rules.check(1) and not rules.check(2)\n")
        res = fmmutate.run(os.path.join(d, "rules.py"), "flipfix/rules.py", d, "flipfix", [sys.executable, "flipfix/t.py"],
                           [], flip=True)
        self.assertEqual(res["tried"], 2, res)  # check's == and check_big's >, never helper's
        self.assertEqual([(m["line"], m["category"]) for m in res["survived"]], [(6, "flip")], res)
        self.assertIn("> → <=", res["survived"][0]["stmt"])

    def test_mutation_sees_every_rule_shape_and_reports_the_unmutated(self):
        import fmmutate
        src = (
            "def f(x, found, cats):\n"
            "    found.append(('a', 'x'))\n"            # 2
            "    cats.append('b')\n"                    # 3
            "    found += [('c', 'x')]\n"               # 4
            "    found += [(cat, 'x') for cat in x]\n"  # 5
            "    found.extend([('d', 'x')])\n"          # 6
            "    if x:\n"
            "        return [('e', 'x')]\n"             # 8
            "    if x > 1:\n"
            "        return 'f'\n"                      # 10
            "    return Block('g', 'x')\n")             # 11
        ms = fmmutate.mutants(src, list("abcdefgz"))
        self.assertEqual([(m["line"], m["category"]) for m in ms],
                         [(2, "a"), (3, "b"), (4, "c"), (5, "*"), (6, "d"), (8, "e"), (10, "f"), (11, "g")])
        self.assertIn("return []", ms[5]["src"])  # a dropped list return stays a list
        d = os.path.join(self.tmp, "shapes")
        os.makedirs(d)
        with open(os.path.join(d, "m.py"), "w") as f:
            f.write(src)
        res = fmmutate.run(os.path.join(d, "m.py"), "s/m.py", d, "s", ["true"], list("abcdefgz"))
        self.assertEqual(res["not_mutated"], ["z"])

    def test_mutation_kills_a_hung_suite_and_refuses_a_failing_baseline(self):
        import fmmutate
        d = os.path.join(self.tmp, "hang")
        os.makedirs(d)
        with open(os.path.join(d, "m.py"), "w") as f:
            f.write("def f(found):\n    found.append(('a', 'x'))\n")
        with open(os.path.join(d, "t.py"), "w") as f:  # passes on the intact module, hangs once the rule is gone
            f.write("import time, m\nl = []\nm.f(l)\nif not l:\n    time.sleep(60)\n")
        t0 = __import__("time").monotonic()
        res = fmmutate.run(os.path.join(d, "m.py"), "h/m.py", d, "h", [__import__("sys").executable, "h/t.py"], ["a"],
                           timeout=2)
        self.assertEqual((res["killed"], res["survived"]), (1, []))
        self.assertLess(__import__("time").monotonic() - t0, 30)  # wall clock: the timeout=2 kill deadline
        with self.assertRaisesRegex(ValueError, "boom"):
            fmmutate.run(os.path.join(d, "m.py"), "h/m.py", d, "h", ["sh", "-c", "echo boom; exit 1"], ["a"])


    def test_mutation_copies_the_extra_files_the_tests_import(self):
        # T-1605: the guard's evasion tests import site/bench_safety.py, outside the plugin tree a mutant copy holds
        import fmmutate
        import fmreplay
        d = os.path.join(self.tmp, "extra")
        os.makedirs(os.path.join(d, "x"))
        with open(os.path.join(d, "x", "m.py"), "w") as f:
            f.write("def f(found):\n    found.append(('a', 'x'))\n")
        with open(os.path.join(d, "helper.py"), "w") as f:
            f.write("OK = 1\n")
        with open(os.path.join(d, "x", "t.py"), "w") as f:
            f.write("import os, sys\nsys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'side'))\n"
                    "import helper, m\nl = []\nm.f(l)\nassert l\n")
        res = fmmutate.run(os.path.join(d, "x", "m.py"), "x/m.py", os.path.join(d, "x"), "x",
                           [__import__("sys").executable, "x/t.py"], ["a"],
                           extra=[(os.path.join(d, "helper.py"), "side/helper.py")])
        self.assertEqual(res["killed"], 1)
        here = os.path.dirname(os.path.abspath(__file__))
        self.assertIn(os.path.join("site", "bench_safety.py"),
                      [rel for _, rel in fmreplay.mutate_extras(os.path.join(here, ".."))])

if __name__ == "__main__":
    unittest.main()
