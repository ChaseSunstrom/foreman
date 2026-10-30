"""fm find (T-2121): deterministic, language-agnostic finders over a tree. Zero findings on every clean exam render,
every planted defect of a covered kind found, nothing found that the key doesn't hold."""
import errno
import json
import os

from helpers import ForemanTestCase

import fmexam
import fmfind

COVERED = {"vuln", "slow", "dep", "untested", "docs", "flaky"}


def write(root, files):
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)


class FindRenders(ForemanTestCase):
    def test_clean_renders_find_nothing_and_planted_ones_find_their_key(self):
        for lang in fmexam.LANGS:
            for kind in fmexam.KINDS:
                for i in range(2):
                    sid = f"{kind}-{lang}-{i:03d}"
                    base = os.path.join(self.tmp, sid)
                    fmexam.render(base, {"id": sid, "kind": kind, "lang": lang, "split": "train"})
                    with self.subTest(sid=sid):
                        self.assertEqual(fmfind.find(os.path.join(base, "hidden", "clean")), [])
                        with open(os.path.join(base, "key.json")) as f:
                            key = json.load(f)
                        found = fmfind.find(os.path.join(base, "repo"))
                        for f in found:
                            self.assertTrue(any(fmexam._matches(f, d) for d in key["defects"]), f)
                        for d in key["defects"]:
                            if d["kind"] in COVERED and not d.get("done"):  # a done item (resume) isn't planted
                                self.assertTrue(any(fmexam._matches(f, d) for f in found), (d, found))


class FindPrecision(ForemanTestCase):
    def test_lookalikes_are_not_findings(self):
        root = os.path.join(self.tmp, "look")
        write(root, {
            "requirements.txt": "requests==2.31\n",
            "package.json": json.dumps({"dependencies": {"left-pad": "1.3.0"}}),
            "app.py": ("import requests\ntry:\n    import ujson\nexcept ImportError:\n    ujson = None\n\n\n"
                       "def get(db, name):\n    out = []\n    for x in out:\n        print(x)\n"
                       "    return db.execute(\"SELECT * FROM users WHERE name = ?\", (name,))\n"),
            "app.js": "const leftPad = require(\"left-pad\");\nfunction pad(s) { return leftPad(s, 3); }\nmodule.exports = { pad };\n",
            "test_app.py": "import random\nfrom app import *\nrandom.seed(4)\n\n\ndef test_get():\n    assert get(random.choice([1]), 'a')\n",
            "test_app.js": "const { pad } = require(\"./app.js\");\nfunction test_pad() { pad(\"a\"); }\n",
            "node_modules/x/index.js": "function nope(q) { return \"SELECT * FROM t WHERE a = '\" + q + \"'\"; }\n",
            "vendor/y.py": "def nope(q):\n    return \"SELECT * FROM t WHERE a = '\" + q + \"'\"\n",
        })
        self.assertEqual(fmfind.find(root), [])

    def test_real_repo_shapes_are_not_findings(self):
        """Seen on Foreman's own tree: code reached through a CLI registration, a module named only in a lazy() string,
        imports inside a triple-quoted fixture, planted fixtures, a card about another library."""
        root = os.path.join(self.tmp, "real")
        write(root, {
            "cli.py": ("def main():\n    return build()\n\n\ndef build():\n    def add(name, fn):\n        return fn\n"
                       "    add('go', cmd_go)\n    add('x', lazy('extra', 'cmd_x'))\n\n\ndef cmd_go(args):\n    return 1\n"),
            "extra.py": "def cmd_x(args):\n    return 2\n",
            "tests/test_cli.py": ("import subprocess\n\n\ndef test_go():\n    subprocess.run(['fm', 'go'])\n\n\n"
                                  "def test_main():\n    assert main\n    code = '''\nimport numpy\n'''\n"),
            "tests/fixtures/bad.py": "def nope(q):\n    return \"SELECT * FROM t WHERE a = '\" + q + \"'\"\n",
            "docs/pandas.md": "Use `read_csv(path)`, `merge(a, b)` and `main()`; never `iterrows()`.\n",
        })
        self.assertEqual(fmfind.find(root), [])

    def test_untested_still_seen_through_reach(self):
        root = os.path.join(self.tmp, "reach")
        write(root, {"app.py": "def main():\n    return 1\n\n\ndef orphan(x):\n    return x\n",
                     "test_app.py": "from app import *\n\n\ndef test_main():\n    assert main()\n"})
        self.assertEqual([(f["kind"], f["symbol"]) for f in fmfind.find(root)], [("untested", "orphan")])


AWS = "AKIA" + "Q7ZT4M2XK9" + "PL3VBN"


class FindHostile(ForemanTestCase):
    """fm find reads repos it doesn't trust: it never hangs, never reads outside the tree, never crashes on odd input."""

    def test_symlinks_fifos_and_odd_names_neither_hang_nor_leak(self):
        import subprocess
        root, outside = os.path.join(self.tmp, "hostile"), os.path.join(self.tmp, "outside")
        write(outside, {"creds.py": f'KEY = "{AWS}"\n'})
        write(root, {"app.py": "def run():\n    return 1\n", "big.py": "x = 1  # " + "*" * 60 + "\n",
                     "c.c": "*" * 60 + "\nint main(void) { return 0; }\n",
                     "q.py": "def q(a):\n    return 'select " + "select " * 50000 + "' + a\n",
                     "pyproject.toml": "project = 'x'\n", "package.json": "[1]",
                     "Cargo.toml": b"name = '\xff'\n".decode("latin-1"),
                     "venv/lib/x.py": "def nope(q):\n    return \"SELECT * FROM t WHERE a = '\" + q + \"'\"\n"})
        os.symlink("/dev/zero", os.path.join(root, "zero.py"))
        os.symlink(os.path.join(outside, "creds.py"), os.path.join(root, "leak.py"))
        write(outside, {"notes.md": "See `./nowhere/setup.md` and `ghost()`.\n"})  # flagged if the link were followed
        os.symlink(os.path.join(outside, "notes.md"), os.path.join(root, "leak.md"))  # T-2124: fmdocs too
        os.symlink("/dev/zero", os.path.join(root, "zero.md"))
        os.mkfifo(os.path.join(root, "pipe.py"))
        try:
            with open(os.path.join(root, "caf\udce9.py"), "w") as f:
                f.write("x = 1\n")
        except OSError as e:  # T-2152: APFS refuses a name that isn't UTF-8 (EILSEQ); the rest of the repo still runs
            if e.errno != errno.EILSEQ:
                raise
        for git in (False, True):
            if git:
                subprocess.run(["git", "init", "-q", root], check=True)
                subprocess.run(["git", "-C", root, "add", "-A"], check=True)
            with self.subTest(git=git):
                r = self.fm("find", root, "--json", check=False)
                self.assertIn(r.returncode, (0, 1), r.stderr)
                found = json.loads(r.stdout)["findings"]
                self.assertFalse([f for f in found if f["file"] in ("leak.py", "zero.py", "pipe.py", "leak.md", "zero.md")
                                  or f["file"].startswith("venv/")], found)

    def test_secret_in_a_generated_file_is_still_found(self):
        root = os.path.join(self.tmp, "gen")
        write(root, {"api_pb2.py": f'# Generated by the protocol buffer compiler.  DO NOT EDIT!\nKEY = "{AWS}"\n'})
        self.assertEqual([f["kind"] for f in fmfind.find(root)], ["secret"])

    def test_a_tree_git_ignores_is_walked_not_called_clean(self):
        import subprocess
        repo = os.path.join(self.tmp, "parent")
        write(repo, {".gitignore": "sub/\n", "sub/q.py": "def q(a):\n    return \"SELECT * FROM t WHERE a = '\" + a + \"'\"\n"})
        subprocess.run(["git", "init", "-q", repo], check=True)
        self.assertEqual([f["kind"] for f in fmfind.find(os.path.join(repo, "sub"))], ["vuln"])
        empty = os.path.join(self.tmp, "none")
        os.makedirs(empty)
        r = self.fm("find", empty, check=False)
        self.assertEqual(r.returncode, 0)
        self.assertIn("No files", r.stdout)


class FindCli(ForemanTestCase):
    def test_verb_exits_one_on_findings_and_zero_on_clean(self):
        base = os.path.join(self.tmp, "r")
        fmexam.render(base, {"id": "vuln-python-000", "kind": "vuln", "lang": "python", "split": "train"})
        r = self.fm("find", os.path.join(base, "repo"), "--json", check=False)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertTrue(any(f["kind"] == "vuln" for f in json.loads(r.stdout)["findings"]))
        r = self.fm("find", os.path.join(base, "hidden", "clean"), check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_a_crash_exits_two_not_one(self):
        """1 means findings; a scan that dies must not read as 'found something' to a CI script."""
        import argparse
        from unittest import mock
        with mock.patch.object(fmfind, "scan", side_effect=RecursionError("deep")):
            self.assertEqual(fmfind.cmd_find(argparse.Namespace(path=self.tmp, json=False)), 2)

    def test_exam_finders_arm_runs_fm_find(self):
        self.fm("init")
        run = self.fm_json("exam", "gen", "--seed", "1", "--per-kind", "1", "--lang", "python",
                           "--kind", "slow,vuln,untested")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "finders")
        self.assertEqual((r["keyed"], r["found"], r["false_alarms"]), (3, 3, 0))

    def test_exam_finders_arm_names_the_worst_first(self):
        """T-2125: the arm lists fm find's ranked leads, so a rank scenario (a vuln beside a missing test and a docs
        slip) closes on order, not only on what was found."""
        self.fm("init")
        run = self.fm_json("exam", "gen", "--seed", "3", "--per-kind", "2", "--lang", "python", "--kind", "rank")["run"]
        r = self.fm_json("exam", "run", run, "--agent", "finders")
        self.assertEqual((r["rank_keyed"], r["rank_hit"]), (2, 2), r)


class FindRank(ForemanTestCase):
    """T-2125: --rank puts the worst first (severity x reach x the finder's precision); a finder under the floor is muted."""

    def lead(self, finder, kind, file="app.py", symbol="x"):
        return {"finder": finder, "kind": kind, "file": file, "line": 1, "symbol": symbol, "says": kind}

    def test_vuln_and_bug_outrank_slow_and_docs_even_with_reach(self):
        found = [self.lead("docs", "docs", "README.md", "go"), self.lead("slow", "slow", "a.py", "go"),
                 self.lead("sql", "vuln", "b.py", "q"), self.lead("probe", "bug", "c.py", "p"),
                 self.lead("untested", "untested", "d.py", "u")]
        texts = {f"m{i}.py": "go()\n" for i in range(20)}  # go is named everywhere: reach can't lift slow past a vuln
        got = fmfind.rank(found, texts, {})
        self.assertEqual([f["kind"] for f in got[:2]], ["vuln", "bug"])
        self.assertEqual({f["kind"] for f in got[2:]}, {"slow", "docs", "untested"})
        self.assertTrue(all(f["score"] >= g["score"] for f, g in zip(got, got[1:])))
        self.assertGreater(next(f for f in got if f["kind"] == "slow")["reach"], 1)

    def test_a_finder_under_the_floor_is_muted_not_dropped(self):
        found = [self.lead("slow", "slow"), self.lead("sql", "vuln")]
        got = fmfind.rank(found, {}, {"slow": 0.2})
        self.assertEqual([(f["finder"], f.get("held")) for f in got], [("sql", None), ("slow", "muted")])

    def test_rank_flag_prints_scores_best_first(self):
        root = os.path.join(self.tmp, "r")
        write(root, {"app.py": ("def q(db, a):\n    return db.execute(\"SELECT * FROM t WHERE a = '\" + a + \"'\")\n\n\n"
                                "def orphan(x):\n    return x\n"),
                     "test_app.py": "from app import *\n\n\ndef test_q():\n    assert q\n"})
        r = self.fm("find", root, "--rank", "--json", check=False)
        self.assertEqual(r.returncode, 1, r.stderr)
        got = json.loads(r.stdout)["findings"]
        self.assertEqual([f["kind"] for f in got], ["vuln", "untested"])
        self.assertIn("score", got[0])


SQL = "def q(db, a):\n    return db.execute(\"SELECT * FROM t WHERE a = '\" + a + \"'\")\n"


class FindLearns(ForemanTestCase):
    """T-2125: --capture files the top findings as tasks tagged with their finder; what became of those tasks is the
    finder's precision (prior 0.5 over 10): a dropped one counts against it, and under the floor it is muted."""

    def test_capture_tags_the_finder_and_dropped_tasks_mute_it(self):
        import fmcli
        import fmcore as c
        self.fm("init")
        write(os.path.join(self.repo, "app"), {"app.py": SQL + "\n\ndef orphan(x):\n    return x\n",
                                               "test_app.py": "from app import *\n\n\ndef test_q():\n    assert q\n"})
        ids = json.loads(self.fm("find", "app", "--rank", "--capture", "5", "--json", check=False).stdout)["captured"]
        p = c.find_project(self.repo)
        briefs = {b.id: b for b in c.load_briefs(p)}
        self.assertEqual([briefs[i].meta.get("finder") for i in ids], ["sql", "untested"])
        self.assertEqual(briefs[ids[0]].type, "SECURITY")
        self.assertFalse(briefs[ids[0]].meta.get("confirm"))  # this project's own tree: no outside text
        again = self.fm("find", "app", "--capture", "5", "--json", check=False)
        self.assertEqual(json.loads(again.stdout)["captured"], [])  # the same finding is never filed twice
        self.assertEqual(fmfind.precision(p), {})  # open tasks say nothing yet
        for i in range(7):
            b = fmcli._create(p, f"untested lead {i}", "FIX", "S", "dropped", source="discovered")
            b.meta["finder"] = "untested"
            c.save_brief(p, b, touch=False)
        self.assertLess(fmfind.precision(p)["untested"], fmfind.FLOOR)
        got = json.loads(self.fm("find", "app", "--rank", "--json", check=False).stdout)["findings"]
        self.assertEqual([(f["finder"], f.get("held")) for f in got], [("sql", None), ("untested", "muted")])
        # a muted finder's lead is never filed
        briefs[ids[1]].meta["status"] = "dropped"
        c.save_brief(p, briefs[ids[1]], touch=False)
        self.assertEqual(json.loads(self.fm("find", "app", "--capture", "5", "--json", check=False).stdout)["captured"], [])

    def test_done_tasks_that_held_raise_precision(self):
        import fmcli
        import fmcore as c
        self.fm("init")
        p = c.find_project(self.repo)
        for status in ("done",) * 6 + ("dropped",):
            b = fmcli._create(p, "sql lead", "SECURITY", "S", status, source="discovered")
            b.meta["finder"] = "sql"
            c.save_brief(p, b, touch=False)
        self.assertEqual(fmfind.precision(p), {"sql": round(11 / 17, 3)})

    def test_twin_leads_both_file_a_drop_is_never_refiled_a_fixed_one_that_returns_is(self):
        import fmcore as c
        self.fm("init")
        write(os.path.join(self.repo, "app"), {"keys.py": f'A = "{AWS}"\nB = "{AWS[:-1]}Q"\n'})
        ids = json.loads(self.fm("find", "app", "--capture", "5", "--json", check=False).stdout)["captured"]
        self.assertEqual(len(ids), 2)  # two leaks in one file are two tasks, not one key
        p = c.find_project(self.repo)
        briefs = {b.id: b for b in c.load_briefs(p)}
        briefs[ids[0]].meta["status"] = "dropped"
        briefs[ids[1]].meta["status"] = "done"
        for i in ids:
            c.save_brief(p, briefs[i], touch=False)
        again = json.loads(self.fm("find", "app", "--capture", "5", "--json", check=False).stdout)["captured"]
        self.assertEqual(len(again), 1)  # the dismissed one stays refuted; the done one came back: a regression
        self.assertEqual(c.load_briefs(p)[-1].meta["find_key"], briefs[ids[1]].meta["find_key"])

    def test_held_leads_leave_the_exit_clean_and_old_drops_fade(self):
        import fmcli
        import fmcore as c
        from unittest import mock
        import fmoutcomes
        self.fm("init")
        write(os.path.join(self.repo, "app"), {"app.py": "def main():\n    return 1\n\n\ndef orphan(x):\n    return x\n",
                                               "test_app.py": "from app import *\n\n\ndef test_main():\n    assert main()\n"})
        p = c.find_project(self.repo)
        made = []
        for i in range(7):
            b = fmcli._create(p, f"untested lead {i}", "FIX", "S", "dropped", source="discovered")
            b.meta["finder"] = "untested"
            c.save_brief(p, b, touch=False)
            made.append(b)
        r = self.fm("find", "app", "--rank", check=False)
        self.assertEqual(r.returncode, 0, r.stdout)  # the only lead is muted: nothing to act on
        self.assertIn("held back", r.stdout)
        for b in made:  # a year on, the drops weigh little: the finder is heard again
            b.meta["updated"] = "2025-01-01T00:00:00Z"
            c.save_brief(p, b, touch=False)
        self.assertGreaterEqual(fmfind.precision(p)["untested"], fmfind.FLOOR)
        b = fmcli._create(p, "sql lead", "SECURITY", "S", "done", source="discovered")
        b.meta["finder"] = "sql"
        c.save_brief(p, b, touch=False)
        with mock.patch.object(fmoutcomes, "outcomes", return_value={b.id: {"fate": "reverted"}}):
            self.assertEqual(fmfind.precision(p)["sql"], round(5 / 11, 3))  # a reverted fix was no real find

    def test_capture_needs_a_count_and_a_project(self):
        self.fm("init")
        write(os.path.join(self.repo, "app"), {"q.py": SQL})
        for n in ("0", "-1"):
            self.assertEqual(self.fm("find", "app", "--capture", n, check=False).returncode, 2)
        out = os.path.join(self.tmp, "bare")
        write(out, {"q.py": SQL})
        r = self.fm("find", ".", "--capture", "1", cwd=out, check=False)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("inside a Foreman project", r.stderr + r.stdout)
        self.assertEqual(self.fm("find", "nope", check=False).returncode, 2)

    def test_a_tree_outside_the_project_waits_for_a_yes(self):
        import fmcore as c
        self.fm("init")
        out = os.path.join(self.tmp, "elsewhere")
        write(out, {"q.py": SQL})
        ids = json.loads(self.fm("find", out, "--capture", "1", "--json", check=False).stdout)["captured"]
        b = next(b for b in c.load_briefs(c.find_project(self.repo)) if b.id == ids[0])
        self.assertTrue(b.meta.get("confirm"))
        self.assertEqual(b.meta.get("finder"), "sql")


FAKE_TOKEN = "ghp_" + "x1Y2" * 9  # a GitHub token shape, never real
APP = ("def used():\n    return 1\n\n\ndef unused():\n    return 2\n\n\ndef by_name():\n    return 3\n\n\n"
       "def one(): return 4\n")
SUITE = ("import unittest\nimport app\n\n\nclass T(unittest.TestCase):\n    def test_used(self):\n"
         "        self.assertEqual(app.used(), 1)\n\n    def test_by_name(self):\n"
         "        self.assertEqual(getattr(app, 'by_' + 'name')(), 3)\n")


class FindProve(ForemanTestCase):
    """T-2122: fm prove turns fm find's candidates into proof tickets a person can rerun, or leads."""

    def proj(self, files=None):
        root = os.path.join(self.tmp, "proj")
        write(root, files or {"app.py": APP, "tests/test_app.py": SUITE})
        return root

    def test_a_stub_the_suite_never_notices_is_proven_and_one_it_notices_is_a_lead(self):
        root = self.proj()
        r = self.fm("prove", root, "--yes-run", "--json", check=False)
        self.assertEqual(r.returncode, 1, r.stderr)  # something proven: findings
        res = json.loads(r.stdout)
        by = {t["symbol"]: t for t in res["tickets"]}
        self.assertEqual(by["unused"]["verdict"], "proven", by)
        self.assertIn("stayed green", by["unused"]["evidence"])
        self.assertIn("python3 -m unittest", by["unused"]["evidence"])  # the command a person reruns
        self.assertEqual(by["by_name"]["verdict"], "lead")  # fm find's guess was wrong: a test reaches it by name
        self.assertIn('a test runs "by_name"', by["by_name"]["evidence"])
        self.assertEqual(by["one"]["verdict"], "lead")  # a one-line def can't be instrumented safely
        self.assertIn("couldn't instrument", by["one"]["evidence"])
        self.assertNotIn("used", by)
        with open(os.path.join(root, "app.py")) as f:
            self.assertEqual(f.read(), APP)  # the tree itself is never touched
        swallow = SUITE + ("\n    def test_swallows(self):  # reaches it by name and swallows whatever it raises\n"
                           "        try:\n            getattr(app, 'un' + 'used')()\n        except Exception:\n"
                           "            pass\n")
        root2 = os.path.join(self.tmp, "swallow")
        write(root2, {"app.py": APP, "tests/test_app.py": swallow})
        r = json.loads(self.fm("prove", root2, "--yes-run", "--json", check=False).stdout)
        t = next(t for t in r["tickets"] if t["symbol"] == "unused")
        self.assertEqual(t["verdict"], "lead", t)  # a marker, not a raise: a swallowed error can't fake a proof
        self.assertIn('a test runs "unused"', t["evidence"])

    def test_a_red_suite_or_none_proves_nothing(self):
        root = self.proj({"app.py": APP, "tests/test_app.py": SUITE.replace("app.used(), 1", "app.used(), 9")})
        r = json.loads(self.fm("prove", root, "--yes-run", "--json", check=False).stdout)
        self.assertTrue(r["tickets"] and all(t["verdict"] == "lead" for t in r["tickets"]))
        self.assertIn("isn't green untouched", r["tickets"][0]["evidence"])
        bare = os.path.join(self.tmp, "bare")
        write(bare, {"app.py": APP, "README.md": "Call `used()` and `unused()`, then `missing_fn()`.\n"})
        r = json.loads(self.fm("prove", bare, "--yes-run", "--json", check=False).stdout)
        docs = [t for t in r["tickets"] if t["kind"] == "docs"]
        self.assertEqual(docs[0]["verdict"], "proven")  # its finder's own check, re-run cold on a fresh copy
        self.assertIn("re-found", docs[0]["evidence"])

    def test_a_planted_untested_function_is_proven_where_the_tests_run_themselves(self):
        tc = fmexam.toolchains()
        for lang, tool in (("python", "python"), ("js", "js"), ("ruby", "ruby")):
            if not tc[tool]:
                continue
            base = os.path.join(self.tmp, lang)
            fmexam.render(base, {"id": f"untested-{lang}-000", "kind": "untested", "lang": lang, "split": "train"})
            r = json.loads(self.fm("prove", os.path.join(base, "repo"), "--yes-run", "--json", check=False).stdout)
            with self.subTest(lang=lang):
                self.assertEqual([t["verdict"] for t in r["tickets"]], ["proven"], r)

    def test_a_suite_that_cannot_fail_proves_nothing(self):
        # mutate to confirm: a function the tests name is stubbed first; a suite that stays green can't show an absence
        root = self.proj({"app.py": APP, "tests/test_app.py": "import unittest\n\n\nclass T(unittest.TestCase):\n"
                          "    def test_nothing(self):  # used\n        pass\n"})
        r = json.loads(self.fm("prove", root, "--yes-run", "--json", check=False).stdout)
        self.assertTrue(r["tickets"] and all(t["verdict"] == "lead" for t in r["tickets"]), r)
        self.assertIn("can't show a function goes unrun", r["tickets"][0]["evidence"])

    def test_the_suite_runs_without_credentials_or_the_users_home(self):
        seen = os.path.join(self.tmp, "seen.json")
        suite = SUITE + ("\n\nclass E(unittest.TestCase):\n    def test_env(self):\n        import json, os\n"
                         f"        json.dump({{k: os.environ.get(k) for k in ('HOME', 'GITHUB_TOKEN', 'FOREMAN_HOME')}}, "
                         f"open({seen!r}, 'w'))\n")
        root = self.proj({"app.py": APP, "tests/test_app.py": suite})
        self.fm("prove", root, "--yes-run", check=False, env={"GITHUB_TOKEN": FAKE_TOKEN})
        with open(seen) as f:
            env = json.load(f)
        self.assertIsNone(env["GITHUB_TOKEN"])
        self.assertIsNone(env["FOREMAN_HOME"])  # nothing of Foreman's state reaches repo code
        self.assertNotIn(env["HOME"], (os.path.expanduser("~"), self.home))
        self.assertIn("fm-prove-", env["HOME"])

    def test_a_tree_whose_head_is_yours_runs_and_a_local_email_cant_forge_it(self):
        import subprocess
        root, home = self.proj(), os.path.join(self.tmp, "githome")
        write(home, {".gitconfig": "[user]\n\temail = me@example.com\n\tname = Me\n"})
        genv = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} | {"HOME": home, "GIT_CONFIG_NOSYSTEM": "1"}
        git = lambda *a: subprocess.run(["git", "-C", root, *a], env=genv, check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        git("commit", "-qm", "mine")
        self.assertEqual(self.fm("prove", root, check=False, env={"HOME": home}).returncode, 1)  # proven, no --yes-run
        git("config", "user.email", "other@example.com")  # the repo's own config names someone else ...
        git("commit", "-q", "--allow-empty", "-m", "theirs")
        r = self.fm("prove", root, check=False, env={"HOME": home})
        self.assertEqual(r.returncode, 2)  # ... and HEAD is theirs: the global email decides, so nothing ran
        self.assertIn("HEAD's author is other@example.com", r.stderr)

    def test_repo_code_runs_only_in_a_tree_that_is_yours_or_with_yes_run(self):
        root = self.proj()
        r = self.fm("prove", root, check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("--yes-run", r.stderr)  # not provably the user's tree: nothing ran
        self.assertNotIn("fm prove stub", open(os.path.join(root, "app.py")).read())

    def test_the_copy_drops_links_credentials_and_home(self):
        import fmprove
        root = self.proj({"app.py": APP, "tests/test_app.py": SUITE})
        os.symlink(os.path.expanduser("~"), os.path.join(root, "home-link"))
        os.mkfifo(os.path.join(root, "pipe"))  # copytree would block or fail on it
        tmp, dst = fmprove._copy(root)
        try:
            self.assertFalse(os.path.lexists(os.path.join(dst, "home-link")))  # a link could reach outside the copy
            self.assertFalse(os.path.lexists(os.path.join(dst, "pipe")))
            env = fmprove._env(tmp)
            self.assertEqual(env["HOME"], tmp)
            self.assertFalse([k for k in env if k.startswith(("FOREMAN_", "CLAUDE_")) or k.endswith("_TOKEN")])
        finally:
            import shutil
            shutil.rmtree(tmp)
