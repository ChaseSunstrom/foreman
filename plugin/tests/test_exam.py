"""fm exam (T-2079): a generated exam of throwaway repos in six languages with planted defects and request shapes,
answer keys kept outside each repo, a held-out third per kind, agents graded against the keys, scores to the Genesis
tower's exam.jsonl."""
import json
import os
import re
import shutil
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
        self.fm("genesis", "put", "gen-1/seed.md", "--file", "-", input="# Seed\n")  # a newer seed after the answers
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

    def test_a_proven_unkeyed_finding_is_an_exam_defect_not_a_false_alarm(self):
        s = self.gen("--seed", "1", "--per-kind", "1", "--lang", "python", "--kind", "bug")["scenarios"][0]
        run_dir = os.path.dirname(os.path.dirname(s["repo"]))
        run, sid = os.path.basename(run_dir), s["id"]
        o = self.fm_json("exam", "run", run, "--agent", "oracle")
        self.assertEqual((o["false_alarms"], o["exam_defects"]), (0, 0))
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
        self.assertEqual((g["exam_defects"], g["false_alarms"]), (1, 6))
        self.assertIn("backslashes", " ".join(g["exam_defect_findings"]))
        self.assertIn("1 exam defect", self.fm("exam").stdout)

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
    with open(os.environ["STUB_LOG"] + ".prompt", "a") as f:
        f.write(argv[argv.index("-p") + 1] + "\n---\n")
    reply = 'Looked.\n{"findings": [{"file": "app.py", "symbol": "nothing", "says": "a guess"}], "notes": [], "done": true}'
    if os.environ.get("STUB_MODE") == "error":  # rate-limited mid-run: an error result, no answer
        print(json.dumps({"type": "result", "is_error": True, "total_cost_usd": 0.05, "result": "rate limited"}))
        sys.exit(0)
    print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.25, "result": reply}))
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

    def test_initiative_kinds_none_rank_clean(self):
        """#1's exam (T-2126): none and rank are child-authored with no request, clean is the app as is; the oracle
        closes all, empty closes only clean, and rank closes only when the vuln is named before the low ones."""
        import fmexam
        r = self.fm_json("exam", "gen", "--seed", "3", "--per-kind", "3", "--lang", "python", "--kind", "none,rank,clean",
                         "--author", "child", env=self.env)
        self.assertEqual(r["dropped"], [])
        by = {k: [s for s in r["scenarios"] if s["kind"] == k] for k in ("none", "rank", "clean")}
        self.assertEqual({k: {s["author"] for s in v} for k, v in by.items()},
                         {"none": {"child"}, "rank": {"child"}, "clean": {"self"}})
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
