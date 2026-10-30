"""fm find (T-2121): deterministic, language-agnostic finders over a tree. Zero findings on every clean exam render,
every planted defect of a covered kind found, nothing found that the key doesn't hold."""
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
                            if d["kind"] in COVERED:
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
        os.mkfifo(os.path.join(root, "pipe.py"))
        with open(os.path.join(root, "caf\udce9.py".encode("utf-8", "surrogateescape").decode("utf-8", "surrogateescape")), "w") as f:
            f.write("x = 1\n")
        for git in (False, True):
            if git:
                subprocess.run(["git", "init", "-q", root], check=True)
                subprocess.run(["git", "-C", root, "add", "-A"], check=True)
            with self.subTest(git=git):
                r = self.fm("find", root, "--json", check=False)
                self.assertIn(r.returncode, (0, 1), r.stderr)
                found = json.loads(r.stdout)["findings"]
                self.assertFalse([f for f in found if f["file"] in ("leak.py", "zero.py", "pipe.py")
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
