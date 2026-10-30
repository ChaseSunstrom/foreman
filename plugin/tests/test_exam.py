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

    def test_unknown_language_or_kind_is_refused(self):
        for args in (("--lang", "cobol"), ("--kind", "nonsense"), ("--per-kind", "0")):
            r = self.fm("exam", "gen", *args, check=False)
            self.assertNotEqual(r.returncode, 0, args)
        r = self.fm("exam", "run", "no-such-run", "--agent", "oracle", check=False)
        self.assertNotEqual(r.returncode, 0)


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
