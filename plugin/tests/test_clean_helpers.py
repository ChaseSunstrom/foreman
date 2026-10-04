"""One definition each (T-0295): the test-file pattern is c.TESTISH everywhere; every tool-less child — fm ideas, fm
research ask, fm oracle, fm second — runs through fmideas' runners, with FOREMAN_NO_BACKGROUND=1."""
import json
import os

from helpers import ForemanTestCase, read_text

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"no_background": os.environ.get("FOREMAN_NO_BACKGROUND"), "args": args[:4]}) + "\n")
if any("Split the question" in a for a in args):
    print(json.dumps({"result": "- Is the sky blue?", "total_cost_usd": 0.01}))
    sys.exit(0)
text = ("- **Paint it** — because — category: look\n"
        "## Examples\n- GIVEN a WHEN b THEN c\n## Ambiguities\n- none\n"
        "## Objections\n- LOW: fine\nVerdict: proceed\n"
        '- CLAIM: the sky is blue | SOURCE: https://a.dev/1 | QUOTE: "blue" | TIER: primary | DATE: 2026-01-01\n')
print(json.dumps({"result": text, "total_cost_usd": 0.01}))
'''


class Pattern(ForemanTestCase):
    def test_one_test_file_pattern(self):
        import fmbench
        import fmcore as c
        import fmmap
        self.assertIs(fmbench.TEST_FILE, c.TESTISH)
        self.assertIs(fmmap._TEST, c.TESTISH)
        for path in ("web/__tests__/calc.js", "spec/calc_spec.rb", "tests/test_calc.py", "test_util.js"):
            self.assertTrue(c.TESTISH.search(path), path)


class Children(ForemanTestCase):
    def test_every_child_runs_through_one_runner_without_background_work(self):
        import fmideas
        self.assertTrue(callable(fmideas.run_child) and callable(fmideas.run_children))
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        log = os.path.join(self.tmp, "log")
        env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": log, "FOREMAN_NO_BACKGROUND": ""}
        self.fm("init")
        pack = os.path.join(self.tmp, "pack.md")
        with open(pack, "w") as f:
            f.write("A small project.\n")
        self.fm("ideas", "--pack", pack, "--lens", "delight", env=env)
        self.fm("research", "ask", "Is the sky blue?", "--no-verify", env=env)
        tid = json.loads(self.fm("task", "new", "Paint the sky", "--type", "FEATURE", "--tier", "M", "--ac", "x :: true",
                                 "--step", "x", "--interpretation", "x", "--approach", "x", "--json").stdout)["id"]
        self.fm("oracle", tid, env=env)
        self.fm("second", "plan", tid, env=env)
        calls = [json.loads(x) for x in read_text(log).splitlines()]
        self.assertGreaterEqual(len(calls), 5)  # a lens, a planner, a researcher, the oracle, the plan review
        self.assertEqual({x["no_background"] for x in calls}, {"1"})


FAILING = r'''#!/usr/bin/env python3
import json, os, sys, time
sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"no_background": os.environ.get("FOREMAN_NO_BACKGROUND")}) + "\n")
mode = os.environ["STUB_MODE"]
if mode == "fail":
    sys.stderr.write("x" * 400 + "\nREAL ERROR: not logged in\n")
    sys.exit(1)
if mode == "sleep":
    time.sleep(5)
print(json.dumps({"result": "I'd rather not revise it.", "total_cost_usd": 0.01}))
'''


class Failures(ForemanTestCase):
    """T-0295 review: the runners' failure paths — the end of stderr (where claude puts the error) on one line, no
    doubled prefixes, the ledger rows, and fm evolve's mutation child."""

    def stub(self, mode):
        from unittest import mock
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir, exist_ok=True)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(FAILING)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "log")
        patch = mock.patch.dict(os.environ, {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log,
                                             "STUB_MODE": mode, "FOREMAN_NO_BACKGROUND": ""})
        patch.start()
        self.addCleanup(patch.stop)

    def rows(self, feature):
        import fmbudget
        return [e for e in fmbudget.ledger() if e.get("feature") == feature]

    def test_errors_keep_the_end_of_stderr_on_one_line(self):
        import fmideas
        self.stub("fail")
        with self.assertRaises(ValueError) as e:
            fmideas.run_child("oracle", "sys", "prompt", "sonnet", 30, project="x", detail="T-0001")
        self.assertIn("REAL ERROR: not logged in", str(e.exception))
        self.assertNotIn("\n", str(e.exception))
        [(text, err)] = fmideas.run_children([(fmideas.child_cmd("sonnet", "s"), "p", "delight")], 30, "ideas")
        self.assertIsNone(text)
        self.assertIn("REAL ERROR: not logged in", err)
        self.assertNotIn("\n", err)
        self.assertEqual([(r["project"], r["detail"]) for r in self.rows("oracle")], [("x", "T-0001")])
        self.assertEqual([r["detail"] for r in self.rows("ideas")], ["delight"])

    def test_a_timeout_is_recorded_like_before(self):
        import fmideas
        self.stub("sleep")
        out = fmideas.run_children([(fmideas.child_cmd("sonnet", "s"), "p", ""), (fmideas.child_cmd("sonnet", "s"), "p",
                                    "delight")], 1, "research")
        self.assertEqual([e for _, e in out], ["timed out after 1s"] * 2)
        self.assertEqual([r["detail"] for r in self.rows("research")],
                         ["timed out: cost unknown", "delight (timed out: cost unknown)"])
        with self.assertRaises(ValueError) as e:
            fmideas.run_child("oracle", "sys", "prompt", "sonnet", 1)
        self.assertEqual(str(e.exception).count("oracle"), 1)

    def test_the_oracle_error_isnt_prefixed_twice(self):
        self.stub("fail")
        self.fm("init")
        tid = json.loads(self.fm("task", "new", "Paint the sky", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true",
                                 "--step", "x", "--json").stdout)["id"]
        r = self.fm("oracle", tid, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("the oracle: ", r.stderr + r.stdout)
        self.assertIn("REAL ERROR", r.stderr + r.stdout)

    def test_evolves_mutation_child(self):
        import fmcore as c
        import fmevolve
        self.fm("init")
        p = c.find_project(self.repo)
        self.stub("fail")
        with self.assertRaises(ValueError) as e:
            fmevolve.mutate(p, "plugin/rules/foreman.md", "# rules\n", [], "sonnet", timeout=30)
        self.assertIn("REAL ERROR", str(e.exception))
        self.stub("plain")
        with self.assertRaises(ValueError) as e:
            fmevolve.mutate(p, "plugin/rules/foreman.md", "# rules\n", [], "sonnet", timeout=30)
        self.assertIn("no revised file came back", str(e.exception))
        self.assertEqual({json.loads(x)["no_background"] for x in read_text(self.log).splitlines()}, {"1"})
        self.assertEqual([r["detail"] for r in self.rows("evolve")], ["plugin/rules/foreman.md"] * 2)
