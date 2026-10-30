"""fm exam (T-2079): a generated exam of throwaway repos in six languages with planted defects and request shapes,
answer keys kept outside each repo, a held-out third per kind, agents graded against the keys, scores to the Genesis
tower's exam.jsonl."""
import json
import os
import subprocess

from helpers import ForemanTestCase, read_text


class ExamGen(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def gen(self, *args):
        return self.fm_json("exam", "gen", *args)

    def test_per_kind_quotas_hold_out_a_third_without_leaking(self):
        res = self.gen("--seed", "3", "--per-kind", "9", "--lang", "python", "--kind", "bug,vuln")
        for kind in ("bug", "vuln"):
            mine = [s for s in res["scenarios"] if s["kind"] == kind]
            self.assertEqual(len(mine), 9, kind)
            self.assertEqual(sum(s["split"] == "holdout" for s in mine), 3, kind)
        ids = [s["id"] for s in res["scenarios"]]
        self.assertEqual(len(ids), len(set(ids)))
        train = self.gen("--seed", "3", "--per-kind", "9", "--lang", "python", "--kind", "bug,vuln", "--split", "train")
        want = {s["id"] for s in res["scenarios"] if s["split"] == "train"}
        self.assertEqual({s["id"] for s in train["scenarios"]}, want)  # same ids, no held-out one among them
        self.assertTrue(all(s["split"] == "train" for s in train["scenarios"]))
        self.assertTrue(all(os.path.isdir(s["repo"]) for s in train["scenarios"]))

    def test_key_and_hidden_checks_sit_outside_a_one_commit_repo(self):
        res = self.gen("--seed", "1", "--per-kind", "1", "--lang", "python", "--kind", "bug,docs")
        for s in res["scenarios"]:
            base = os.path.dirname(s["repo"])
            key = json.loads(read_text(os.path.join(base, "key.json")))
            self.assertEqual(key["kind"], s["kind"])
            self.assertTrue(key["defects"])
            self.assertTrue(os.path.isdir(os.path.join(base, "hidden")))
            self.assertFalse({"key.json", "hidden"} & set(os.listdir(s["repo"])))
            log = subprocess.run(["git", "log", "--oneline"], cwd=s["repo"], capture_output=True, text=True).stdout
            self.assertEqual(len(log.splitlines()), 1)
            body = "".join(read_text(os.path.join(s["repo"], f)) for f in os.listdir(s["repo"])
                           if os.path.isfile(os.path.join(s["repo"], f)))
            for d in key["defects"]:  # the key's wording never shows up in what the agent sees
                self.assertNotIn(d["text"], body)

    def test_oracle_scores_full_and_empty_scores_zero(self):
        run = self.gen("--seed", "2", "--per-kind", "1", "--lang", "python")["run"]
        o = self.fm_json("exam", "run", run, "--agent", "oracle")
        self.assertGreater(o["keyed"], 0)
        self.assertEqual((o["found"], o["false_alarms"]), (o["keyed"], 0))
        self.assertGreater(o["fixable"], 0)
        self.assertEqual(o["fixed"], o["fixable"])
        self.assertGreater(o["tf_keyed"], 0)
        self.assertEqual(o["tf_first"], o["tf_keyed"])
        self.assertGreater(o["readings_keyed"], 0)
        self.assertEqual(o["readings_hit"], o["readings_keyed"])
        self.assertEqual(o["missing_hit"], o["missing_keyed"])
        self.assertGreater(o["missing_keyed"], 0)
        e = self.fm_json("exam", "run", run, "--agent", "empty")
        self.assertEqual((e["found"], e["fixed"], e["readings_hit"], e["missing_hit"]), (0, 0, 0, 0))
        regrade = self.fm_json("exam", "grade", run, "--agent", "oracle")
        self.assertEqual(regrade["found"], o["found"])
        lines = read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()
        self.assertEqual([json.loads(x)["agent"] for x in lines], ["oracle", "empty", "oracle"])
        self.assertIn("holdout", json.loads(lines[0]))
        self.assertIn("oracle", self.fm("genesis").stdout)  # the tower's status shows the last score
        self.assertIn("oracle", self.fm("exam").stdout)

    def test_finders_arm_runs_without_a_session_and_fixes_nothing(self):
        run = self.gen("--seed", "4", "--per-kind", "1", "--lang", "python", "--kind", "docs,vuln,bug")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "finders")
        self.assertEqual((r["agent"], r["keyed"], r["fixed"], r["tf_first"]), ("finders", 3, 0, 0))
        self.assertLessEqual(r["found"], r["keyed"])

    def test_unknown_language_or_kind_is_refused(self):
        for args in (("--lang", "cobol"), ("--kind", "nonsense"), ("--per-kind", "0")):
            r = self.fm("exam", "gen", *args, check=False)
            self.assertNotEqual(r.returncode, 0, args)
        r = self.fm("exam", "run", "no-such-run", "--agent", "oracle", check=False)
        self.assertNotEqual(r.returncode, 0)


STUB = r'''#!/usr/bin/env python3
import json, os, re, sys
argv = sys.argv[1:]
if "--permission-mode" in argv:  # a session arm: it answers in its reply and changes nothing
    with open(os.environ["STUB_LOG"], "a") as f:
        f.write(("plugin" if "--plugin-dir" in argv else "bare") + "\n")
    with open(os.environ["STUB_LOG"] + ".cwd", "a") as f:
        f.write(os.getcwd() + "\n")
    reply = 'Looked.\n{"findings": [{"file": "app.py", "symbol": "nothing", "says": "a guess"}], "notes": [], "done": true}'
    if os.environ.get("STUB_MODE") == "error":  # rate-limited mid-run: an error result, no answer
        print(json.dumps({"type": "result", "is_error": True, "total_cost_usd": 0.05, "result": "rate limited"}))
        sys.exit(0)
    print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.25, "result": reply}))
    sys.exit(0)
prompt = sys.stdin.read()  # the tool-less author: plants an off-by-one in clamp, and its test
name = re.search(r"def (\w+)\(x, lo, hi\)", prompt).group(1)
want = 4 if os.environ.get("STUB_MODE") == "weak" else 3  # weak: a test that fails on the clean module too
plant = {"function": name, "source": f"def {name}(x, lo, hi):\n    return lo if x < lo else hi if x > hi + 1 else x\n",
         "test": f"assert {name}(4, 0, 3) == {want}", "says": f"{name}() lets hi + 1 through",  # unindented, as models send
         "request": "Some values come back out of range; find and fix it."}
print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.01, "result": json.dumps(plant)}))
'''


class ExamAuthors(ForemanTestCase):
    """Step 6: a tool-less child authors the bug and vuln scenarios (kept only when fm exam check passes them), and
    the foreman and plain session arms answer held-out scenarios with their cost recorded."""

    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.fm("init")

    def test_child_authored_scenarios_are_kept_only_when_sound(self):
        r = self.fm_json("exam", "gen", "--seed", "1", "--per-kind", "3", "--lang", "python", "--kind", "bug,docs",
                         "--author", "child", env=self.env)
        bugs = [s for s in r["scenarios"] if s["kind"] == "bug"]
        self.assertEqual((len(bugs), r["dropped"]), (3, []))
        self.assertTrue(all(s["author"] == "child" for s in bugs))
        self.assertTrue(all(s["author"] == "self" for s in r["scenarios"] if s["kind"] == "docs"))
        key = json.loads(read_text(os.path.join(os.path.dirname(bugs[0]["repo"]), "key.json")))
        self.assertIn("lets hi + 1 through", key["defects"][0]["text"])
        self.assertEqual(key["request"], "Some values come back out of range; find and fix it.")
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual((o["found"], o["fixed"], o["tf_first"]), (o["keyed"], o["fixable"], o["tf_keyed"]))
        lines = read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()
        self.assertEqual(json.loads(lines[-1])["author"], "child+self")

    def test_a_child_scenario_that_fails_check_is_dropped(self):
        r = self.fm_json("exam", "gen", "--seed", "1", "--per-kind", "2", "--lang", "python", "--kind", "bug",
                         "--author", "child", env=dict(self.env, STUB_MODE="weak"))
        self.assertEqual((r["scenarios"], len(r["dropped"])), ([], 2))
        self.assertIn("clean render", r["dropped"][0]["why"])

    def test_session_arms_answer_held_out_scenarios_with_their_cost(self):
        run = self.fm_json("exam", "gen", "--seed", "2", "--per-kind", "3", "--lang", "python", "--kind", "bug")["run"]
        for agent in ("foreman", "plain"):
            r = self.fm_json("exam", "run", run, "--agent", agent, "--split", "holdout", "--limit", "1", env=self.env)
            self.assertEqual((r["scenarios"], r["holdout"]["scenarios"], r["false_alarms"]), (1, 1, 1))
            self.assertAlmostEqual(r["cost"], 0.25)
        self.assertEqual(read_text(self.log).split(), ["plugin", "bare"])
        state = os.path.dirname(os.path.dirname(self.fm_json("genesis")["dir"]))  # the guard blocks edits in p.dir
        for cwd in read_text(self.log + ".cwd").split():
            self.assertFalse(os.path.realpath(cwd).startswith(os.path.realpath(state)), cwd)
        spend = read_text(os.path.join(self.home, "state", "spend.jsonl"))
        self.assertEqual(spend.count('"exam-arm"'), 2)  # each session's cost lands in fm cost / fm budget

    def test_errored_sessions_are_counted_and_the_sample_spans_kinds(self):
        run = self.fm_json("exam", "gen", "--seed", "2", "--per-kind", "3", "--lang", "python", "--kind", "bug,docs")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "plain", "--limit", "2", env=dict(self.env, STUB_MODE="error"))
        self.assertEqual((r["scenarios"], r["errors"]), (2, 2))
        self.assertIn("2 errored", self.fm("exam").stdout)
        row = json.loads(read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()[-1])
        self.assertEqual((row["kinds"], row["split"]), (["bug", "docs"], "all"))
        bad = self.fm("exam", "grade", run, "--agent", "../..", check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("unknown agent", bad.stderr + bad.stdout)

    def test_reply_parsing_takes_the_last_findings_object_and_survives_junk(self):
        import fmexam
        got = fmexam._reply('x {"a": 1} {"findings": [{"file": "a"}, 3], "notes": "no", "done": "yes"} tail')
        self.assertEqual(got, {"findings": [{"file": "a"}], "notes": [], "done": False})
        self.assertEqual(fmexam._reply('{"findings": ' + "[" * 20000)["findings"], [])  # past the recursion limit


class LangCheck:
    """Every kind rendered in one language: the planted suite runs, each hidden check fails on the planted repo and
    passes on the clean render, and the clean suite passes (fm exam check, the exam of the exam)."""
    LANG = ""

    def test_planted_fails_hidden_checks_and_clean_passes(self):
        self.fm("init")
        if not self.fm_json("exam")["toolchains"].get(self.LANG):
            self.skipTest(f"no {self.LANG} toolchain here")
        run = self.fm_json("exam", "gen", "--seed", "5", "--per-kind", "1", "--lang", self.LANG)["run"]
        chk = self.fm_json("exam", "check", run, check=False)
        self.assertTrue(chk["ok"], chk["problems"])
        self.assertGreaterEqual(chk["checked"], 11)


class ExamPython(LangCheck, ForemanTestCase):
    LANG = "python"


class ExamJs(LangCheck, ForemanTestCase):
    LANG = "js"


class ExamTs(LangCheck, ForemanTestCase):
    LANG = "ts"


class ExamRust(LangCheck, ForemanTestCase):
    LANG = "rust"


class ExamRuby(LangCheck, ForemanTestCase):
    LANG = "ruby"


class ExamC(LangCheck, ForemanTestCase):
    LANG = "c"
