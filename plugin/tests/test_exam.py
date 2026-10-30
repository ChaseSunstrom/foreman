"""fm exam (T-2079): a generated exam of throwaway repos in six languages with planted defects and request shapes,
answer keys kept outside each repo, a held-out third per kind, agents graded against the keys, scores to the Genesis
tower's exam.jsonl."""
import difflib
import json
import os
import re
import shutil
import sys
import subprocess

from helpers import CLEAN_READER, ForemanTestCase, read_text

CLEAN = {"PATH": CLEAN_READER + os.pathsep + os.environ["PATH"]}  # T-2166: the put's cold read passes


class ExamGen(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def gen(self, *args):
        return self.fm_json("exam", "gen", *args)

    def test_exists_parts_and_trigger_scenarios_render_check_and_grade(self):
        # T-2216: #2 exists (the module already does what's asked: name it, add nothing), #9 parts (three defects in
        # one request), #11 trigger (the tests must run on a schedule); the oracle closes each and empty closes none
        r = self.gen("--seed", "8", "--per-kind", "1", "--lang", "python", "--kind", "exists,parts,trigger")
        by = {s["kind"]: s for s in r["scenarios"]}
        keys = {k: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for k, s in by.items()}
        self.assertEqual(keys["exists"]["defects"], [])
        self.assertIn(rf"\b{re.escape(keys['exists']['names']['clamp'])}\b", keys["exists"]["readings"])
        self.assertNotIn(keys["exists"]["names"]["clamp"], keys["exists"]["request"])  # it asks, never names
        self.assertEqual([d["kind"] for d in keys["parts"]["defects"]], ["bug", "vuln", "slow"])
        self.assertEqual([d["kind"] for d in keys["trigger"]["defects"]], ["trigger"])
        clean = os.path.join(os.path.dirname(by["trigger"]["repo"]), "hidden", "clean")
        self.assertIn("cron:", read_text(os.path.join(clean, ".github", "workflows", "nightly.yml")))
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual(sorted(o["closed"]["train"] + o["closed"]["holdout"]), sorted(s["id"] for s in by.values()))
        e = self.fm_json("exam", "run", r["run"], "--agent", "empty")
        self.assertEqual(e["closed"]["train"] + e["closed"]["holdout"], [])
        # T-2216 review: naming what exists while adding a copy of it doesn't close exists, and a README line that
        # says 'schedule:' and 'cron: x' isn't a trigger
        run_dir = os.path.dirname(os.path.dirname(by["exists"]["repo"]))
        work = os.path.join(run_dir, "work", "oracle")
        with open(os.path.join(work, by["exists"]["id"], "app.py"), "a") as f:
            f.write("\n\ndef keep_in_range(x, lo, hi):\n    return max(lo, min(x, hi))\n")
        with open(os.path.join(work, by["trigger"]["id"], "README.md"), "a") as f:
            f.write("\nschedule:\n  - cron: 0 3 * * * run the tests\n")
        os.remove(os.path.join(work, by["trigger"]["id"], ".github", "workflows", "nightly.yml"))
        ans = os.path.join(run_dir, "answers", "oracle", by["exists"]["id"] + ".json")
        a = json.loads(read_text(ans))
        a["findings"] = [{"file": "app.py", "symbol": keys["exists"]["names"]["clamp"], "says": "it already exists"}]
        with open(ans, "w") as f:
            json.dump(a, f)  # a finding on exists is no false alarm: it has nothing keyed to find
        g = self.fm_json("exam", "grade", r["run"], "--agent", "oracle")
        closed = g["closed"]["train"] + g["closed"]["holdout"]
        self.assertNotIn(by["exists"]["id"], closed)  # the copy broke it
        self.assertNotIn(by["trigger"]["id"], closed)  # a README isn't a schedule
        self.assertIn(by["parts"]["id"], closed)
        a["findings"], a["notes"] = [], a["notes"]
        with open(os.path.join(work, by["exists"]["id"], "app.py")) as f:
            body = f.read().split("\n\ndef keep_in_range")[0] + "\n"
        with open(os.path.join(work, by["exists"]["id"], "app.py"), "w") as f:
            f.write(body)
        g = self.fm_json("exam", "grade", r["run"], "--agent", "oracle")
        self.assertIn(by["exists"]["id"], g["closed"]["train"] + g["closed"]["holdout"])  # the finding alone: still closed

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

    def test_an_unreadable_answer_is_an_error_not_a_quiet_close(self):
        """T-2103: a corrupt or non-object answer file grades as an errored session, never as an empty answer that
        closes a scenario whose right move is to find nothing."""
        res = self.gen("--seed", "4", "--per-kind", "3", "--lang", "python", "--kind", "clean")
        run, s0 = res["run"], res["scenarios"][0]
        e = self.fm_json("exam", "run", run, "--agent", "empty")
        ids = sorted(e["closed"]["train"] + e["closed"]["holdout"])
        self.assertEqual(len(ids), 3)
        answers = os.path.join(os.path.dirname(os.path.dirname(s0["repo"])), "answers", "empty")
        for sid, body in zip(ids, ("{", "[]")):
            with open(os.path.join(answers, f"{sid}.json"), "w") as f:
                f.write(body)
        g = self.fm_json("exam", "grade", run, "--agent", "empty")
        self.assertEqual(sorted(g["closed"]["train"] + g["closed"]["holdout"]), ids[2:])
        self.assertEqual(g["errors"], 2)

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
        g = self.gen("--seed", "2", "--per-kind", "1", "--lang", "python")
        run = g["run"]
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
        self.fm("genesis", "init", "--file", "-", input="Ship it.\nMUST: tests pass.\n")  # T-2166: a put is read against gen-0
        self.fm("genesis", "put", "gen-1/seed.md", "--file", "-", input="# Seed\n", env=CLEAN)  # a newer seed after the answers
        regrade = self.fm_json("exam", "grade", run, "--agent", "oracle")
        self.assertEqual(regrade["found"], o["found"])
        lines = read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()
        self.assertEqual([json.loads(x)["agent"] for x in lines], ["oracle", "empty", "oracle"])
        first = json.loads(lines[0])
        self.assertIn("holdout", first)
        want = {sp: sorted(s["id"] for s in g["scenarios"] if s["split"] == sp) for sp in ("train", "holdout")}
        self.assertEqual(first["closed"], want)  # every scenario closed, filed under the run's own split
        self.assertEqual(first["gen"], 0)  # no seed yet: the generation the line grades
        self.assertEqual(json.loads(lines[2])["gen"], 0)  # the generation that answered, stamped at run, not at regrade
        self.assertIn("oracle", self.fm("genesis").stdout)  # the tower's status shows the last score
        self.assertIn("oracle", self.fm("exam").stdout)

    def test_a_graded_held_out_run_lands_on_the_capability_scorecard(self):
        # T-2097: grade files the ids it graded, so a capability scores on its held-out scenarios
        self.fm("genesis", "init", "--file", "-", input="go\n\n## 2. The capability spec\n\n"
                "1. **Correctness.** Fixes what's broken. Exam: bug.\n\n## 3. The tower\n")
        g = self.gen("--seed", "4", "--per-kind", "9", "--lang", "python", "--kind", "bug")
        self.assertNotEqual(self.fm("exam", "scorecard", check=False).returncode, 0, "nothing graded yet")
        self.fm_json("exam", "run", g["run"], "--agent", "oracle", "--split", "holdout")
        line = json.loads(read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()[-1])
        held = sorted(s["id"] for s in g["scenarios"] if s["split"] == "holdout")
        self.assertEqual(line["answered"], {"holdout": held, "child": []})
        r = json.loads(self.fm("exam", "scorecard", "--agent", "oracle", "--json", check=False).stdout)  # T-2204: the template decides nothing
        self.assertEqual([(x["state"], x["closed"], x["graded"], x["selfmade"]) for x in r["rows"]], [("too few", 0, 0, 3)])
        self.assertIn("3 self-authored held-out results not counted", self.fm("exam", "scorecard", "--agent", "oracle",
                                                                             check=False).stdout)

    def test_the_clean_app_keeps_the_edge_contract_and_its_suite_proves_it(self):
        import fmexam  # T-2120: page n or size < 1 is empty, lo wins in clamp, label keeps a long s, total of none is 0
        s = self.gen("--seed", "1", "--per-kind", "1", "--lang", "python", "--kind", "bug")["scenarios"][0]
        base = os.path.dirname(s["repo"])
        key, clean = json.loads(read_text(os.path.join(base, "key.json"))), os.path.join(base, "hidden", "clean")
        readme = read_text(os.path.join(clean, "README.md"))
        for clause in ("below 1 gives an empty page", "lo wins when lo > hi", "s itself when", "0 for none", "standard SQL"):
            self.assertIn(clause, readme)
        self.assertTrue(fmexam.suite(key, clean)[0])
        n = key["names"]
        for fn, old in (("page", f"def {n['page']}(xs, n, size):\n    return xs[(n - 1) * size:n * size]\n"),
                        ("clamp", f"def {n['clamp']}(x, lo, hi):\n    return lo if x < lo else hi if x > hi else x\n"),
                        ("label", f"def {n['label']}(s, width):\n    return s.rjust(width)[-width:]\n"),
                        ("total", f"def {n['total']}(xs):\n    return sum(xs) if xs else None\n"),
                        ("dedupe", f"def {n['dedupe']}(xs):\n    return list(dict.fromkeys(x for x in xs if x >= 0))\n")):
            mutant = os.path.join(self.tmp, "mut-" + fn)
            shutil.copytree(clean, mutant)
            with open(os.path.join(mutant, "app.py"), "a") as f:
                f.write("\n\n" + old)  # the later def wins: one clause broken, the rest as clean
            self.assertFalse(fmexam.suite(key, mutant)[0], f"the clean suite misses a broken {fn} clause")

    def test_test_first_puts_back_only_the_defects_lines(self):
        # T-2203: an arm that also edited other code in the file keeps that edit; a defect region it rewrote credits nothing
        import fmexam
        s = self.gen("--seed", "1", "--per-kind", "1", "--lang", "python", "--kind", "bug")["scenarios"][0]
        base = os.path.dirname(s["repo"])
        key = json.loads(read_text(os.path.join(base, "key.json")))
        clean, kind = os.path.join(base, "hidden", "clean"), next(x for x in key["defects"] if x["tf"])["kind"]  # a code defect
        planted = os.path.join(base, "hidden", "planted", kind)
        arm = os.path.join(self.tmp, "arm")
        shutil.copytree(clean, arm)
        with open(os.path.join(arm, "app.py"), "a") as f:
            f.write("\n\ndef extra_helper():\n    return 1\n")
        tmp, dst = fmexam.putback(base, kind, arm)
        try:
            body = read_text(os.path.join(dst, "app.py"))
            self.assertIn("extra_helper", body)  # the arm's other edit survives
            self.assertEqual(body.replace("\n\ndef extra_helper():\n    return 1\n", ""), read_text(os.path.join(planted, "app.py")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertTrue(fmexam.suite(key, clean)[0])
        self.assertIsNone(fmexam.putback(base, kind, os.path.join(self.tmp, "nowhere")))
        # the arm fixed the defect in other words but kept the lines around it: the region is replaced by the planted one
        c, p = read_text(os.path.join(clean, "app.py")).splitlines(True), read_text(os.path.join(planted, "app.py")).splitlines(True)
        op, i1, i2, j1, j2 = next(o for o in difflib.SequenceMatcher(None, c, p, autojunk=False).get_opcodes() if o[0] != "equal")
        helper = "\n\ndef extra_helper():\n    return 1\n"
        for name, lines, ok in (("reworded", c[:i1] + ["# reworded\n"] + [x.rstrip("\n") + "  # reworded\n" for x in c[i1:i2]] + c[i2:], True),
                                ("anchors", c[:i1 - 1] + [c[i1 - 1].rstrip("\n") + "  # moved\n"] + c[i1:i2] + c[i2:], False)):
            arm = os.path.join(self.tmp, name)
            shutil.copytree(clean, arm)
            with open(os.path.join(arm, "app.py"), "w") as f:
                f.write("".join(lines) + helper)
            got = fmexam.putback(base, kind, arm)
            if not ok:
                self.assertIsNone(got, name)
                continue
            try:
                self.assertEqual(read_text(os.path.join(got[1], "app.py")), "".join(p) + helper)
            finally:
                shutil.rmtree(got[0], ignore_errors=True)

    def test_putback_replaces_each_reworded_region_between_its_anchors(self):
        # T-2203: two replaced regions in one file, an anchor widened past a line the clean file repeats, one at the end
        import fmexam
        base = os.path.join(self.tmp, "synthetic")
        g = "def g(y):\n    if y is None:\n        return 0\n    return 1\n"
        tail = "\n\ndef z():\n    return 0\n"
        clean = "def f(x):\n    return x + 1\n\n\n" + g + "\n\ndef h(y):\n    if y is None:\n        return 0\n    return y * 2\n" + tail
        planted = clean.replace("x + 1", "x").replace("y * 2", "y")
        doc = g.replace("def g(y):\n", "def g(y):\n    \"\"\"doc\"\"\"\n")
        arm = os.path.join(self.tmp, "armwork")
        for path, text in ((os.path.join(base, "hidden", "clean"), clean), (os.path.join(base, "hidden", "planted", "k"), planted),
                           (arm, clean.replace("    return x + 1\n", "    return 1 + x\n").replace(g, doc)
                            .replace("    return y * 2\n", "    result = y * 2\n    return result\n"))):
            os.makedirs(path)
            with open(os.path.join(path, "app.py"), "w") as f:
                f.write(text)
        os.chmod(os.path.join(arm, "app.py"), 0o444)  # a read-only file is replaced in the copy, not written through
        tmp, dst = fmexam.putback(base, "k", arm)
        try:
            self.assertEqual(read_text(os.path.join(dst, "app.py")), planted.replace(g, doc))  # both defects back, the doc kept
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        # a region on the file's last line anchors on the file's end: what the arm added past it goes too (a test
        # that imports it then fails to load, which _caught never credits)
        for path, text in ((os.path.join(base, "hidden", "clean"), clean + "    # end\n"),
                           (os.path.join(base, "hidden", "planted", "k"), planted + "    # END\n")):
            with open(os.path.join(path, "app.py"), "w") as f:
                f.write(text)
        os.chmod(os.path.join(arm, "app.py"), 0o644)
        with open(os.path.join(arm, "app.py"), "a") as f:
            f.write("    # end\n\n\ndef helper():\n    return 1\n")
        tmp, dst = fmexam.putback(base, "k", arm)
        try:
            self.assertEqual(read_text(os.path.join(dst, "app.py")), planted.replace(g, doc) + "    # END\n")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_a_red_from_a_name_the_putback_removed_is_not_the_arms_test_catching_the_defect(self):
        # T-2203: a suite that fails only because it can't load (the region held a name it imports) caught nothing
        import fmexam
        key = {"commands": {"suite": "t.py", "exec": sys.executable + " -I @F@"}}
        for name, body, caught in (("assert", "assert 1 == 2\n", True), ("load", "from app import gone\n", False),
                                   ("green", "assert 1 == 1\n", False)):
            target = os.path.join(self.tmp, "caught-" + name)
            os.makedirs(target)
            for fname, text in (("t.py", body), ("app.py", "x = 1\n")):
                with open(os.path.join(target, fname), "w") as f:
                    f.write(text)
            self.assertEqual(fmexam._caught(key, target), caught, name)

    def test_an_unkeyed_finding_proved_only_by_the_arms_own_test_stays_a_false_alarm(self):
        # T-2170: the arm wrote the change and the test, so its proof is the arm grading itself; with no outside check
        # agreeing, the finding stays a false alarm, counted apart (proved_by_arm) and listed so a real one gets read
        s = self.gen("--seed", "1", "--per-kind", "1", "--lang", "python", "--kind", "bug")["scenarios"][0]
        run_dir = os.path.dirname(os.path.dirname(s["repo"]))
        run, sid = os.path.basename(run_dir), s["id"]
        o = self.fm_json("exam", "run", run, "--agent", "oracle")
        self.assertEqual((o["false_alarms"], o["exam_defects"], o["proved_by_arm"]), (0, 0, 0))
        work, ans_path = os.path.join(run_dir, "work", "oracle", sid), os.path.join(run_dir, "answers", "oracle", sid + ".json")
        q, bs = json.loads(read_text(os.path.join(run_dir, sid, "key.json")))["names"]["query"], chr(92)
        with open(os.path.join(work, "app.py"), "a") as f:  # the arm also escapes backslashes, a dialect the base ignores
            f.write(f"\n\n_q = {q}\n\n\ndef {q}(name):\n    return _q(name.replace(chr(92), chr(92) * 2))\n")
            f.write("\n\ndef extra():\n    return 1\n")  # code the arm added: its test fails on the base for a missing name
        for name, body in {"test_bs.py": f"from app import {q}\nassert {q}('a' + chr(92) + 'b').count(chr(92)) == 2\n",
                           "test_same.py": f"from app import {q}\nassert {q}('bob').endswith(\"'bob'\")\n",
                           "test_x.py": "from app import extra\nassert extra() == 1\n"}.items():
            with open(os.path.join(work, name), "w") as f:  # test_bs: red on the clean base, green here; test_same: green on both
                f.write(body)
        ans = json.loads(read_text(ans_path))
        ans["findings"] += [{"file": "app.py", "symbol": q, "says": "backslashes" + bs, "test": "test_bs.py"},
                            {"file": "app.py", "symbol": q, "says": "a guess", "test": "test_same.py"},
                            {"file": "app.py", "symbol": q, "says": "no proof"},
                            {"file": "app.py", "symbol": q, "says": "outside", "test": "../../" + sid + "/key.json"},
                            {"file": "app.py", "symbol": q, "says": "absolute", "test": os.path.join(work, "test_bs.py")},
                            {"file": "app.py", "symbol": q, "says": "new code", "test": "test_x.py"},
                            {"file": "app.py", "symbol": q, "says": "nul", "test": "test_bs.py\x00"}]
        with open(ans_path, "w") as f:
            json.dump(ans, f)
        g = self.fm_json("exam", "grade", run, "--agent", "oracle")
        self.assertEqual((g["exam_defects"], g["false_alarms"], g["proved_by_arm"]), (0, 7, 1))
        self.assertIn("backslashes", " ".join(g["proved_by_arm_findings"]))  # listed, to read and fix the generator by
        self.assertNotIn("exam_defect_findings", g)  # old lines' key meant a defect; this one lists false alarms
        import fmcore as c
        import fmgenesis
        tail = fmgenesis._exam_tail(fmgenesis.home(c.find_project(self.repo)))
        self.assertIn("7 false alarms (1 with the arm's own proof)", tail)  # what a genesis cold read sees, too
        line = self.fm("exam").stdout
        self.assertIn("7 false alarms (1 with the arm's own proof)", line)
        self.assertNotIn("exam defect", line)

    def test_finders_arm_runs_without_a_session_and_fixes_nothing(self):
        run = self.gen("--seed", "4", "--per-kind", "1", "--lang", "python", "--kind", "docs,vuln,bug")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "finders")
        self.assertEqual((r["agent"], r["keyed"], r["fixed"], r["tf_first"]), ("finders", 3, 0, 0))
        self.assertLessEqual(r["found"], r["keyed"])

    def test_recall_is_reported_per_language_and_per_defect_kind(self):
        # T-2233 (steer: detection ladder): #1's recall was one total, so a finder blind in one language hid in it
        run = self.gen("--seed", "4", "--per-kind", "3", "--lang", "python,js", "--kind", "docs,vuln")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "finders")
        by = r["recall"]
        self.assertEqual(sorted(by["lang"]), ["js", "python"])
        self.assertEqual(sorted(by["kind"]), ["docs", "vuln"])
        for axis in ("lang", "kind"):  # each axis splits the same totals
            self.assertEqual([sum(v[i] for v in by[axis].values()) for i in (0, 1)], [r["found"], r["keyed"]])
        h = r["holdout"]["recall"]
        self.assertEqual((sum(v[1] for v in h["lang"].values()) > 0, sum(v[1] for v in h["lang"].values())),
                         (True, r["holdout"]["keyed"]))
        text = self.fm("exam", "run", run, "--agent", "finders").stdout
        self.assertRegex(text, r"by language: js \d+/\d+ · python \d+/\d+")
        self.assertRegex(text, r"by kind: docs \d+/\d+ · vuln \d+/\d+")

    def test_unknown_language_or_kind_is_refused(self):
        for args in (("--lang", "cobol"), ("--kind", "nonsense"), ("--per-kind", "0")):
            r = self.fm("exam", "gen", *args, check=False)
            self.assertNotEqual(r.returncode, 0, args)
        r = self.fm("exam", "run", "no-such-run", "--agent", "oracle", check=False)
        self.assertNotEqual(r.returncode, 0)
        r = self.fm("exam", "run", "no-such-run", "--agent", "oracle", "--request", "x", check=False)
        self.assertIn("--request goes with a session agent", r.stderr)


STUB = r'''#!/usr/bin/env python3
import json, os, re, sys
argv = sys.argv[1:]
if "--permission-mode" in argv:  # a session arm: it answers in its reply and changes nothing
    with open(os.environ["STUB_LOG"], "a") as f:
        f.write(("plugin" if "--plugin-dir" in argv else "bare") + "\n")
    with open(os.environ["STUB_LOG"] + ".cwd", "a") as f:
        f.write(os.getcwd() + "\n")
    with open(os.environ["STUB_LOG"] + ".budget", "a") as f:
        f.write((argv[argv.index("--max-budget-usd") + 1] if "--max-budget-usd" in argv else "none") + "\n")
    with open(os.environ["STUB_LOG"] + ".prompt", "a") as f:
        f.write(argv[argv.index("-p") + 1] + "\n---\n")
    reply = 'Looked.\n{"findings": [{"file": "app.py", "symbol": "nothing", "says": "a guess"}], "notes": [], "done": true}'
    if os.environ.get("STUB_MODE") == "nojson" and "--resume" not in argv:  # fixed things, then forgot the JSON
        reply = 'Fixed the SQL splice and the README\'s wrong name. {"findings": [{"says": "it said "x""}]}'  # broken JSON
    if os.environ.get("STUB_MODE") == "error":  # rate-limited mid-run: an error result, no answer
        print(json.dumps({"type": "result", "is_error": True, "total_cost_usd": 0.05, "result": "rate limited"}))
        sys.exit(0)
    print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.25, "result": reply, "session_id": "s-1"}))
    sys.exit(0)
prompt = sys.stdin.read()  # the tool-less author: plants an off-by-one in clamp, and its test
name = re.search(r"def (\w+)\(x, lo, hi\)", prompt).group(1)
if any("4 to 6 items" in a for a in argv):  # T-2149: a goal or resume key, 5 items (or a broken one per STUB_MODE)
    tot, lab = re.search(r"def (\w+)\(xs\):\n    return sum", prompt).group(1), re.search(r"def (\w+)\(s, width\)", prompt).group(1)
    items = [{"kind": "code", "function": name, "source": f"def {name}(x, lo, hi):\n    return max(lo, x if x == hi + 1 else min(x, hi))\n",
              "test": f"assert {name}(4, 0, 3) == 3", "says": f"{name}() lets hi + 1 through"},
             {"kind": "code", "function": tot, "source": f"def {tot}(xs):\n    return sum(xs) if len(xs) != 1 else 0\n",
              "test": f"assert {tot}([7]) == 7", "says": f"{tot}() drops a lone item"},
             {"kind": "test", "function": lab, "says": f"nothing tests {lab}()"},
             {"kind": "readme", "line": "Every helper raises nothing on empty input.", "pattern": "raises nothing", "says": "the README skips empty input"},
             {"kind": "readme", "line": "Needs no packages beyond the standard library.", "pattern": "(?i)needs no packages", "says": "the README skips setup"}]
    mode = os.environ.get("STUB_MODE")
    if mode == "few":
        items = items[:3]
    elif mode == "samefn":
        items[1] = dict(items[0], says="again")
    elif mode == "badre":
        items[3]["pattern"] = "("
    elif mode == "readmematch":
        items[3]["pattern"] = "Helpers|raises nothing"
    elif mode == "many":
        items += items[3:5]
    elif mode == "nokind":
        del items[2]
    elif mode == "badkind":
        items[2]["kind"] = "docs"
    elif mode == "dupreadme":
        items[4] = dict(items[3])
    elif mode == "nested":
        items[3]["pattern"] = "(r+)+aises nothing"
    print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.01, "result": json.dumps({"items": items})}))
    sys.exit(0)
want = 4 if os.environ.get("STUB_MODE") == "weak" else 3  # weak: a test that fails on the clean module too
plant = {"function": name, "source": f"def {name}(x, lo, hi):\n    return max(lo, x if x == hi + 1 else min(x, hi))\n",
         "test": f"assert {name}(4, 0, 3) == {want}\n    assert {name}(2, 0, 3) == 2",  # only line 1 trimmed, as models send
         "says": f"{name}() lets hi + 1 through",
         "request": "Some values come back out of range; find and fix it."}
mode = os.environ.get("STUB_MODE")
if any("already does" in a for a in argv):  # T-2216: exists, a request for what a function already does
    plant = {"function": name, "request": f"Could you add {name}?" if mode == "named" else
             "I need something that keeps a value inside a range.", "example": f"{name}() already does that; reuse it."}
elif any("on a schedule by themselves" in a for a in argv):  # T-2216: trigger, in the user's words
    plant = {"request": "Add a cron job for the tests." if mode == "giveaway" else "Have the checks run by themselves each morning."}
elif any("three different defects" in a for a in argv):  # T-2216: parts, three plants in three functions
    tot, lab = re.search(r"def (\w+)\(xs\):\n    return sum", prompt).group(1), re.search(r"def (\w+)\(s, width\)", prompt).group(1)
    items = [{"function": name, "source": f"def {name}(x, lo, hi):\n    return max(lo, x if x == hi + 1 else min(x, hi))\n",
              "test": f"assert {name}(4, 0, 3) == 3", "says": f"{name}() lets hi + 1 through"},
             {"function": tot, "source": f"def {tot}(xs):\n    return sum(xs) if len(xs) != 1 else 0\n",
              "test": f"assert {tot}([7]) == 7", "says": f"{tot}() drops a lone item"},
             {"function": lab, "source": f"def {lab}(s, width):\n    return s if len(s) == 1 else s.rjust(width)\n",
              "test": f"assert {lab}('a', 3) == '  a'", "says": f"{lab}() doesn't pad a one-letter label"}]
    if mode == "samefn":
        items[2] = dict(items[0], says="again")
    plant = {"request": "Three problems: ranges leak past the top, a one-item total is zero, and one-letter labels "
                        "don't pad. Fix all three.", "items": items}
elif any("vague request" in a for a in argv):  # T-2217: the request-shape kinds, written by the child
    plant = {"request": "make it nicer", "example": "Did you mean faster on big lists, or clearer to read?",
             "readings": {"echo": ["nicer", "faster"], "empty": ["x?", "clearer"], "group": ["(ab)+c", "clearer"],
                          "one": ["faster"], "dup": ["faster", "faster"], "broad": ["\\.", "clearer"]}.get(
                 mode, ["\\bfast(er)?\\b|speed", "clear(er)?|readab"])}  # \b and a group: no oracle split survives them
    if mode == "noexample":
        del plant["example"]
elif any("two sensible readings" in a for a in argv):
    tot = re.search(r"def (\w+)\(xs\):\n    return sum", prompt).group(1)
    plant = {"request": f"make {tot}() skip bad values", "readings": ["negative (amounts?|totals?)|refund", "null|missing values?"],
             "example": "Skip negative amounts, or skip missing values?"}
elif any("can't reach" in a for a in argv):
    plant = {"request": "Match the labels to the brand guide in our Notion page",
             "missing": {"echo": ["trello"], "broad": ["o"]}.get(mode, ["notion"]),
             "example": "I can't open the Notion page from here; paste the guide or export it."}
elif any("new helper" in a for a in argv):  # T-2211: untested and clean, a function the module didn't have
    plant = {"name": name if mode == "collide" else "middle", "source": "def middle(xs):\n    return sorted(xs)[len(xs) // 2]\n",
             "test": "assert middle([3, 1, 2]) == 2", "says": "middle() gives the middle value",
             "request": "Look over the tests."}
elif any("false sentence" in a for a in argv):  # T-2211: docs, a README line the code contradicts
    pg = re.search(r"def (\w+)\(xs, n, size\)", prompt).group(1)
    plant = {"function": pg, "wrong": "Pages are numbered from zero.", "right": "Pages are numbered from one.",
             "never": {"bothmatch": "numbered from", "badre": "(zero", "greedy": "n.*u.*m.*zero"}.get(mode, "numbered from zero"),
             "must": "numbered from one",
             "says": f"the README says {pg}() numbers pages from zero", "request": "The docs seem off about paging."}
elif any("flaky test" in a for a in argv):  # T-2211: flaky, a test that sums random numbers
    tot = re.search(r"def (\w+)\(xs\):\n    return sum", prompt).group(1)
    plant = {"function": tot, "test": f"import random\n    xs = [random.randint(0, 9) for _ in range(3)]\n    assert {tot}(xs) < 20",
             "fixed": f"assert {tot}([9, 9, 1]) == 19", "never": "random",
             "says": f"test_{tot} sums random numbers and fails when they reach 20", "request": "CI fails now and then."}
    if mode == "nofixed":
        del plant["fixed"]
elif any("big input" in a for a in argv):  # T-2204: slow, shown by a big input timing out
    d = re.search(r"def (\w+)\(xs\):\n    seen", prompt).group(1)
    plant = {"function": d, "source": f"def {d}(xs):\n    out = []\n    for x in xs:\n        if x not in out:\n"
                                      f"            out.append(x)\n    return out\n",
             "test": f"assert {d}(list(range(60000))) == list(range(60000))",
             "says": f"{d}() scans its output list for each item, quadratic on big inputs",
             "request": "Deduping a big list hangs."}
elif any("isn't installed" in a for a in argv):  # T-2204: dep, an import that isn't there
    lab = re.search(r"def (\w+)\(s, width\)", prompt).group(1)
    plant = {"function": lab, "source": f"def {lab}(s, width):\n    from strpad import pad_left\n    return pad_left(s, width)\n",
             "test": f"assert {lab}('ab', 4) == '  ab'", "says": f"{lab}() imports strpad, which isn't installed",
             "request": "Labels crash."}
if os.environ.get("STUB_MODE") == "norequest":
    del plant["request"]
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
        r = self.fm_json("exam", "gen", "--seed", "1", "--per-kind", "3", "--lang", "python", "--kind", "bug",
                         "--author", "child", env=self.env)
        bugs = [s for s in r["scenarios"] if s["kind"] == "bug"]
        self.assertEqual((len(bugs), r["dropped"]), (3, []))
        self.assertTrue(all(s["author"] == "child" for s in bugs))  # T-2217: every kind has a child shape now
        key = json.loads(read_text(os.path.join(os.path.dirname(bugs[0]["repo"]), "key.json")))
        self.assertIn("lets hi + 1 through", key["defects"][0]["text"])
        self.assertEqual(key["request"], "Some values come back out of range; find and fix it.")
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual((o["found"], o["fixed"], o["tf_first"]), (o["keyed"], o["fixable"], o["tf_keyed"]))
        lines = read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()
        self.assertEqual(json.loads(lines[-1])["author"], "child")

    def test_children_author_slow_and_dep_scenarios_too(self):
        # T-2204: a slow plant shows by its big-input test timing out, a dep plant by an import that isn't installed;
        # the exam line names them as an outside author's, so the scorecard counts them
        r = self.fm_json("exam", "gen", "--seed", "2", "--per-kind", "1", "--lang", "python", "--kind", "slow,dep",
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        self.assertEqual({s["kind"]: s["author"] for s in r["scenarios"]}, {"slow": "child", "dep": "child"})
        keys = {s["kind"]: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for s in r["scenarios"]}
        self.assertTrue(keys["slow"]["defects"][0]["check"]["slow"])
        self.assertIn("quadratic", keys["slow"]["defects"][0]["text"])
        self.assertIn("strpad", keys["dep"]["defects"][0]["text"])
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual((o["found"], o["fixed"], o["tf_first"]), (o["keyed"], o["fixable"], o["tf_keyed"]))
        line = json.loads(read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()[-1])
        self.assertEqual(line["answered"]["child"], sorted(s["id"] for s in r["scenarios"] if s["split"] == "holdout"))

    def test_children_author_untested_docs_flaky_and_clean_scenarios(self):
        # T-2211: each kind's own reply shape, rendered and gated by fm exam check; a malformed reply drops its scenario
        kinds = ("untested", "docs", "flaky", "clean")
        r = self.fm_json("exam", "gen", "--seed", "5", "--per-kind", "1", "--lang", "python", "--kind", ",".join(kinds),
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        by = {s["kind"]: s for s in r["scenarios"]}
        self.assertEqual({k: s["author"] for k, s in by.items()}, dict.fromkeys(kinds, "child"))
        keys = {k: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for k, s in by.items()}
        self.assertEqual(keys["untested"]["defects"][0]["symbols"], ["middle"])
        self.assertNotIn("middle", read_text(os.path.join(by["untested"]["repo"], "test_app.py")))
        self.assertIn("def middle", read_text(os.path.join(by["clean"]["repo"], "app.py")))  # novel code, still clean
        self.assertEqual(keys["clean"]["defects"], [])
        self.assertIn("numbered from zero", read_text(os.path.join(by["docs"]["repo"], "README.md")))
        self.assertIn("random", read_text(os.path.join(by["flaky"]["repo"], "test_app.py")))
        self.assertEqual(keys["docs"]["request"], "The docs seem off about paging.")
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual(sorted(o["closed"]["train"] + o["closed"]["holdout"]), sorted(s["id"] for s in r["scenarios"]))
        e = self.fm_json("exam", "run", r["run"], "--agent", "empty")
        self.assertEqual(e["closed"]["train"] + e["closed"]["holdout"], [by["clean"]["id"]])
        for mode, kind, why in (("collide", "untested", "isn't a plain name"), ("bothmatch", "docs", "tell its two lines apart"),
                                ("badre", "docs", "bad never regex"), ("greedy", "docs", "open-ended repeats"),
                                ("nofixed", "flaky", "fixed")):
            d = self.fm_json("exam", "gen", "--seed", "5", "--per-kind", "1", "--lang", "python", "--kind", kind,
                             "--author", "child", env=dict(self.env, STUB_MODE=mode))
            self.assertEqual(d["scenarios"], [], mode)
            self.assertIn(why, d["dropped"][0]["why"], mode)

    def test_children_author_exists_trigger_and_parts_scenarios(self):
        # T-2216: #2, #9 and #11's kinds have an outside author too; a giveaway or a malformed reply is dropped
        kinds = ("exists", "trigger", "parts")
        r = self.fm_json("exam", "gen", "--seed", "9", "--per-kind", "1", "--lang", "python", "--kind", ",".join(kinds),
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        by = {s["kind"]: s for s in r["scenarios"]}
        self.assertEqual({k: s["author"] for k, s in by.items()}, dict.fromkeys(kinds, "child"))
        keys = {k: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for k, s in by.items()}
        self.assertEqual(keys["exists"]["request"], "I need something that keeps a value inside a range.")
        self.assertEqual(keys["trigger"]["request"], "Have the checks run by themselves each morning.")
        self.assertEqual(len(keys["parts"]["defects"]), 3)
        self.assertTrue(all(d["tf"] for d in keys["parts"]["defects"]))
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual(sorted(o["closed"]["train"] + o["closed"]["holdout"]), sorted(s["id"] for s in r["scenarios"]))
        for kind, mode, why in (("exists", "named", "names the function"), ("trigger", "giveaway", "gives the fix away"),
                                ("parts", "samefn", "two plants on one function")):
            d = self.fm_json("exam", "gen", "--seed", "9", "--per-kind", "1", "--lang", "python", "--kind", kind,
                             "--author", "child", env=dict(self.env, STUB_MODE=mode))
            self.assertEqual(d["scenarios"], [], (kind, mode))
            self.assertIn(why, d["dropped"][0]["why"], (kind, mode))

    def test_children_write_the_vague_ambiguous_and_missing_tool_requests(self):
        # T-2217: the child writes the ask and what a good answer names; repeating the request names none of it
        kinds = ("vague", "ambiguous", "missing-tool")
        r = self.fm_json("exam", "gen", "--seed", "6", "--per-kind", "1", "--lang", "python", "--kind", ",".join(kinds),
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        by = {s["kind"]: s for s in r["scenarios"]}
        self.assertEqual({k: s["author"] for k, s in by.items()}, dict.fromkeys(kinds, "child"))
        keys = {k: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for k, s in by.items()}
        self.assertEqual((keys["vague"]["request"], keys["vague"]["readings"]),
                         ("make it nicer", ["\\bfast(er)?\\b|speed", "clear(er)?|readab"]))
        self.assertEqual([d["kind"] for d in keys["vague"]["defects"]], ["slow"])  # the template's code stays
        self.assertEqual((keys["missing-tool"]["missing"], keys["missing-tool"]["done_ok"]), (["notion"], False))
        for k in ("vague", "ambiguous"):
            self.assertFalse(any(re.search(x, keys[k]["request"], re.I) for x in keys[k]["readings"]), k)
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual(sorted(o["closed"]["train"] + o["closed"]["holdout"]), sorted(s["id"] for s in r["scenarios"]))
        for kind, mode, why in (("vague", "echo", "matches the request"), ("missing-tool", "echo", "misses the request"),
                                ("vague", "empty", "matches anything"), ("vague", "group", "repeats a group"),
                                ("vague", "one", "isn't 2 different"), ("vague", "dup", "isn't 2 different"),
                                ("vague", "broad", "a filler answer"), ("missing-tool", "broad", "a filler answer"),
                                ("vague", "noexample", "example")):
            d = self.fm_json("exam", "gen", "--seed", "6", "--per-kind", "1", "--lang", "python", "--kind", kind,
                             "--author", "child", env=dict(self.env, STUB_MODE=mode))
            self.assertEqual(d["scenarios"], [], (kind, mode))
            self.assertIn(why, d["dropped"][0]["why"], (kind, mode))

    def test_a_new_function_is_exported_and_declared_where_the_language_needs_it(self):
        import fmexam  # T-2211: JS exports and imports it, TS exports it, Rust makes it pub, C declares it in app.h
        for lang, src, test in (("js", "function middle(xs) {\n  return xs[0];\n}\n", "  assert.strictEqual(middle([1]), 1);\n"),
                                ("ts", "function middle(xs: number[]): number {\n  return xs[0];\n}\n",
                                 "  assert.strictEqual(middle([1]), 1);\n"),
                                ("c", "long middle(const long *xs, int n) {\n    return n ? xs[0] : 0;\n}\n",
                                 "    long xs[] = {1};\n    assert(middle(xs, 1) == 1);\n"),
                                ("rust", "fn middle(xs: &[i64]) -> i64 {\n    xs[0]\n}\n", "    assert_eq!(middle(&[1]), 1);\n")):
            base = os.path.join(self.tmp, "shaped-" + lang)
            s = {"id": f"clean-{lang}-000001", "kind": "clean", "lang": lang, "split": "train", "author": "child"}
            fmexam.render(base, s, {"shape": "clean", "says": "x", "request": "", "name": "middle", "source": src, "test": test})
            repo = os.path.join(base, "repo")
            app = read_text(os.path.join(repo, fmexam.SPEC[lang]["files"][0]))
            if lang == "js":
                self.assertRegex(app, r"module\.exports = \{[^}]*\bmiddle\b")
                self.assertRegex(read_text(os.path.join(repo, "test_app.js")), r"const \{[^}]*\bmiddle\b[^}]*\} = require")
            elif lang == "ts":
                self.assertIn("export function middle", app)
                self.assertRegex(read_text(os.path.join(repo, "test_app.ts")), r"import \{[^}]*\bmiddle\b")
            elif lang == "rust":
                self.assertIn("pub fn middle", app)
            else:
                self.assertIn("long middle(const long *xs, int n);", read_text(os.path.join(repo, "app.h")))
        bad = {"shape": "clean", "says": "x", "request": "", "name": "middle", "test": "    assert(middle(0) == 0);\n",
               "source": "typedef struct { long a; } S; long middle(S s) { return s.a; }\n"}  # a brace before it: refused
        with self.assertRaises(ValueError):
            fmexam.render(os.path.join(self.tmp, "shaped-bad"), {"id": "clean-c-000002", "kind": "clean", "lang": "c",
                                                                  "split": "train", "author": "child"}, bad)

    def test_initiative_kinds_none_rank_clean(self):
        """#1's exam (T-2126): none and rank are child-authored with no request, clean is the app as is; the oracle
        closes all, empty closes only clean, and rank closes only when the vuln is named before the low ones."""
        import fmexam
        r = self.fm_json("exam", "gen", "--seed", "3", "--per-kind", "3", "--lang", "python", "--kind", "none,rank,clean",
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        by = {k: [s for s in r["scenarios"] if s["kind"] == k] for k in ("none", "rank", "clean")}
        self.assertEqual({k: {s["author"] for s in v} for k, v in by.items()},
                         {"none": {"child"}, "rank": {"child"}, "clean": {"child"}})  # T-2211: clean too
        keys = {s["id"]: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for s in r["scenarios"]}
        none, rank = keys[by["none"][0]["id"]], keys[by["rank"][0]["id"]]
        self.assertEqual(([d["kind"] for d in none["defects"]], none["request"]), (["bug", "untested", "docs"], ""))
        self.assertNotEqual(none["defects"][0]["symbols"], none["defects"][1]["symbols"])  # the stub plants clamp
        self.assertEqual(rank["rank"], [["vuln"], ["untested", "docs"]])
        self.assertEqual(keys[by["clean"][0]["id"]]["defects"], [])
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual(sorted(o["closed"]["train"] + o["closed"]["holdout"]), sorted(keys))
        e = self.fm_json("exam", "run", r["run"], "--agent", "empty")
        self.assertEqual(sorted(e["closed"]["train"] + e["closed"]["holdout"]), sorted(s["id"] for s in by["clean"]))
        fs = [{"file": d["files"][0], "symbol": d["symbols"][0]} for d in rank["defects"]]  # vuln, untested, docs
        self.assertTrue(fmexam._in_order(fs, rank))
        self.assertFalse(fmexam._in_order(fs[1:] + fs[:1], rank))  # the vuln named last
        self.assertFalse(fmexam._in_order(fs[:2], rank))  # one missed
        self.assertIn("0/1 ranked", fmexam.summary({"found": 3, "keyed": 3, "rank_keyed": 1, "rank_hit": 0}))

    def test_finish_kinds_goal_and_resume(self):
        """#4's exam (T-2140): goal gets only a vague goal, resume a half-done PLAN.md and "continue"; the key is what a
        finished version holds. The oracle closes all and empty none; saying done with an item unmet is a false done,
        extra work is never a false alarm, and a done item that breaks is broken."""
        import fmexam
        r = self.fm_json("exam", "gen", "--seed", "3", "--per-kind", "3", "--lang", "python", "--kind", "goal,resume",
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        self.assertEqual({s["author"] for s in r["scenarios"]}, {"child"})
        keys = {s["id"]: json.loads(read_text(os.path.join(os.path.dirname(s["repo"]), "key.json"))) for s in r["scenarios"]}
        goal = next(k for k in keys.values() if k["kind"] == "goal")
        res = next(s for s in r["scenarios"] if s["kind"] == "resume")
        resume = keys[res["id"]]
        self.assertEqual([d["kind"] for d in goal["defects"]], ["code1", "code2", "test3", "readme4", "readme5"])
        self.assertIn("lets hi + 1 through", goal["defects"][0]["text"])  # the child's key, no template item (T-2149)
        self.assertEqual([d["tf"] for d in goal["defects"]], [True, True, False, False, False])
        self.assertEqual(goal["request"], fmexam.REQUESTS["goal"])  # the template goal, never the child's report
        self.assertEqual(resume["request"], "continue")
        self.assertEqual([d.get("done", False) for d in resume["defects"]], [False, False, True, False, False])
        plan = read_text(os.path.join(res["repo"], "PLAN.md"))
        self.assertIn("Goal: " + fmexam.REQUESTS["goal"], plan)
        self.assertEqual((plan.count("- [x] "), plan.count("- [ ] ")), (1, 4))
        self.assertTrue(self.fm_json("exam", "check", r["run"])["ok"])
        o = self.fm_json("exam", "run", r["run"], "--agent", "oracle")
        self.assertEqual(sorted(o["closed"]["train"] + o["closed"]["holdout"]), sorted(keys))
        self.assertEqual((o["keyed"], o["false_done"], o["broken"]), (0, 0, 0))
        e = self.fm_json("exam", "run", r["run"], "--agent", "empty")
        self.assertEqual((e["closed"], e["fixed"], e["broken"], e["false_done"]), ({"train": [], "holdout": []}, 0, 0, 0))
        pl = self.fm_json("exam", "run", r["run"], "--agent", "plain", "--limit", "2", env=self.env)  # done, changed nothing
        self.assertEqual((pl["false_done"], pl["false_alarms"], pl["closed"]), (2, 0, {"train": [], "holdout": []}))
        self.assertIn("2 false done", fmexam.summary(pl))
        self.assertIn("\ncontinue\n\n(Unattended", "\n" + read_text(self.log + ".prompt"))
        work = os.path.join(os.path.dirname(os.path.dirname(res["repo"])), "work", "oracle", res["id"], "test_app.py")
        names = resume["names"]
        txt = read_text(work)
        with open(work, "w") as f:  # the oracle's resume undoes the done test item; the suite still passes
            f.write(txt.replace(f"{names['label']}(", f"{names['label']} ("))
        g = self.fm_json("exam", "grade", r["run"], "--agent", "oracle")
        self.assertEqual((g["broken"], g["false_done"]), (1, 1))
        self.assertNotIn(res["id"], g["closed"]["train"] + g["closed"]["holdout"])
        self.assertIn("1 broken", fmexam.summary(g))
        t = self.fm_json("exam", "gen", "--seed", "3", "--per-kind", "1", "--lang", "python", "--kind", "resume")
        tk = json.loads(read_text(os.path.join(os.path.dirname(t["scenarios"][0]["repo"]), "key.json")))
        self.assertEqual([(d["kind"], d.get("done", False)) for d in tk["defects"]],
                         [("bug", False), ("vuln", True), ("untested", False), ("docs", True)])
        self.assertTrue(self.fm_json("exam", "check", t["run"])["ok"])
        nr = self.fm_json("exam", "gen", "--seed", "4", "--per-kind", "1", "--lang", "python", "--kind", "goal,bug",
                          "--author", "child", env=dict(self.env, STUB_MODE="norequest"))
        self.assertEqual(([s["kind"] for s in nr["scenarios"]], len(nr["dropped"])), (["goal"], 1))  # a bug needs its report
        for mode, why in (("few", "3 items, not 4 to 6"), ("samefn", "two code items on one function"),
                          ("badre", "bad README regex"), ("readmematch", "readme4 check passes on the planted repo"),
                          ("many", "7 items, not 4 to 6"), ("nokind", "one code, one test and one README item"),
                          ("badkind", "no code, test or README item"), ("dupreadme", "two README items close with one line"),
                          ("nested", "repeats a group")):
            d = self.fm_json("exam", "gen", "--seed", "4", "--per-kind", "1", "--lang", "python", "--kind", "goal",
                             "--author", "child", env=dict(self.env, STUB_MODE=mode))
            self.assertEqual(d["scenarios"], [], mode)
            self.assertIn(why, d["dropped"][0]["why"], mode)

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
        self.assertEqual(read_text(self.log + ".budget").split(), ["none", "none"])  # T-2179: no dollar cap on proving
        self.fm_json("exam", "run", run, "--agent", "plain", "--split", "holdout", "--limit", "1", "--budget", "1",
                     env=self.env)
        self.assertEqual(read_text(self.log + ".budget").split()[-1], "1")  # a cap the run names still holds

    def test_a_reply_with_no_findings_object_gets_one_more_turn_for_it(self):
        run = self.fm_json("exam", "gen", "--seed", "2", "--per-kind", "3", "--lang", "python", "--kind", "bug")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "foreman", "--split", "holdout", "--limit", "1",
                         env=dict(self.env, STUB_MODE="nojson"))
        self.assertEqual((r["scenarios"], r["false_alarms"]), (1, 1))  # the resumed turn's answer is graded
        self.assertAlmostEqual(r["cost"], 0.5)  # both turns
        prompts = read_text(self.log + ".prompt").split("\n---\n")
        self.assertIn("only the JSON object", prompts[1])
        answers = os.path.join(os.path.dirname(os.path.dirname(self.fm_json("genesis")["dir"])), "exam", run, "answers", "foreman")
        a = json.loads(read_text(os.path.join(answers, next(f for f in os.listdir(answers) if f.endswith(".json")))))
        self.assertTrue(a["reasked"])
        self.assertIn("Fixed the SQL splice", a["said"])  # the first reply's tail, so a lost answer can be read back
        self.assertIn("1 re-asked", self.fm("exam").stdout)  # the lost-answer rate shows on the exam line
        r = self.fm_json("exam", "run", run, "--agent", "plain", "--split", "holdout", "--limit", "1", "--model", "haiku",
                         env=self.env)
        self.assertEqual(len(read_text(self.log + ".prompt").split("\n---\n")), 4)  # an answered reply isn't re-asked
        self.assertEqual(r["model"], "haiku")  # T-2158: the line says which model answered, so smoke never decides
        self.assertIsNone(self.fm_json("exam", "run", run, "--agent", "oracle").get("model"))  # no session, no model
        self.assertEqual(read_text(os.path.join(answers, "model")), "default")  # no --model: the configured one
        self.assertEqual(self.fm_json("exam", "grade", run, "--agent", "foreman", "--model", "haiku")["model"], "haiku")
        os.remove(os.path.join(answers, "model"))  # answers from before the stamp name their model at the regrade
        self.assertEqual(self.fm_json("exam", "grade", run, "--agent", "foreman", "--model", "haiku")["model"], "haiku")
        self.assertIn("model haiku", self.fm("exam").stdout)  # the exam line says it too
        self.assertNotEqual(self.fm("exam", "grade", run, "--agent", "foreman", "--model", "opus", check=False).returncode,
                            0)  # a named stamp is a fact: a regrade never rewrites it
        self.assertIn("session arm", self.fm("exam", "grade", run, "--agent", "oracle", "--model", "haiku",
                                             check=False).stderr)  # no session, nothing to stamp

    def test_the_genesis_arm_runs_one_generation_on_the_given_request(self):
        run = self.fm_json("exam", "gen", "--seed", "2", "--per-kind", "3", "--lang", "python", "--kind", "bug")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "genesis", "--split", "holdout", "--limit", "1", env=self.env)
        self.assertEqual((r["scenarios"], r["request"]), (1, "make this great"))  # the default request is recorded
        self.assertEqual(read_text(self.log).split(), ["plugin"])
        prompt = read_text(self.log + ".prompt")
        self.assertTrue(prompt.startswith("make this great"), prompt[:80])
        self.assertIn("fm genesis draft", prompt)
        self.assertIn("fm genesis step", prompt)
        row = json.loads(read_text(os.path.join(self.fm_json("genesis")["dir"], "exam.jsonl")).splitlines()[-1])
        self.assertEqual((row["agent"], row["request"]), ("genesis", "make this great"))
        p = self.fm_json("exam", "run", run, "--agent", "plain", "--split", "holdout", "--limit", "1",
                         "--request", "make this great", env=self.env)
        self.assertEqual(p["request"], "make this great")
        self.assertTrue(read_text(self.log + ".prompt").split("---\n")[1].startswith("make this great"))

    def test_errored_sessions_are_counted_and_the_sample_spans_kinds(self):
        run = self.fm_json("exam", "gen", "--seed", "2", "--per-kind", "3", "--lang", "python", "--kind", "bug,docs")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "plain", "--limit", "2", env=dict(self.env, STUB_MODE="error"))
        self.assertEqual((r["scenarios"], r["errors"], r["reasked"]), (2, 2, 0))  # an errored turn isn't re-asked
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
        chk = self.fm_json("exam", "check", run, check=False, timeout=300)  # T-2152: builds and runs every suite
        self.assertTrue(chk["ok"], chk["problems"])
        self.assertGreaterEqual(chk["checked"], 11)
        s = self.fm_json("exam", "gen", "--seed", "5", "--per-kind", "1", "--lang", self.LANG, "--kind", "bug")["scenarios"][0]
        clean = os.path.join(os.path.dirname(s["repo"]), "hidden", "clean")
        cmd = re.search(r"Run the tests: `(.+)`", read_text(os.path.join(clean, "README.md"))).group(1)
        r = subprocess.run(cmd, shell=True, cwd=clean, capture_output=True, text=True, timeout=300)  # T-2120: as shown
        self.assertEqual(r.returncode, 0, (cmd, r.stderr[-300:]))


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
