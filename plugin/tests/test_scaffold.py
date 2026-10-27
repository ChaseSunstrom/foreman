"""T-1554: fm new web in a new folder makes a project born proven (its own check is its gate, and passes); fm codemod
previews a rewrite as a diff and writes it only with --apply; fm dev --once runs the affected tests."""
import json
import os
import subprocess

from helpers import PLUGIN, ForemanTestCase, read_text


class Born(ForemanTestCase):
    def env(self):
        return {"PATH": os.path.join(PLUGIN, "bin") + os.pathsep + os.environ["PATH"]}  # this checkout's fm

    def test_fm_new_web_in_a_new_folder_is_born_proven(self):
        demo = os.path.join(self.tmp, "demo")
        got = json.loads(self.fm("new", "web", demo, "--json", env=self.env(), cwd=self.tmp).stdout)
        self.assertTrue(got["green"], got["born"])
        self.assertEqual([s["step"] for s in got["born"]], ["git init", "fm init", "its check as the gate",
                                                            "first commit", "fm check"])
        self.assertIn("Born from fm new web", subprocess.run(["git", "-C", demo, "log", "--format=%s"],
                                                             capture_output=True, text=True).stdout)
        p = self.fm("check", cwd=demo, env=self.env(), check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_an_existing_folder_only_gets_the_file(self):
        here = os.path.join(self.tmp, "here")
        os.makedirs(here)
        got = json.loads(self.fm("new", "web", here, "--json", env=self.env(), cwd=self.tmp).stdout)
        self.assertEqual(got["born"], [])
        self.assertFalse(os.path.exists(os.path.join(here, ".git")))


class Codemod(ForemanTestCase):
    def setUp(self):
        super().setUp()
        for rel, text in (("a.py", "def old_name():\n    pass\n\n\nold_name()\nnot_old_name_x = 1\n"),
                          ("docs/b.txt", "old_name in the docs\n")):
            os.makedirs(os.path.dirname(os.path.join(self.repo, rel)), exist_ok=True)
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write(text)
        with open(os.path.join(self.repo, "blob.dat"), "wb") as f:
            f.write(b"old_name\0binary")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "files"], check=True)

    def test_rename_previews_a_diff_then_applies_it(self):
        before = read_text(os.path.join(self.repo, "a.py"))
        out = self.fm("codemod", "rename", "old_name", "new_name", cwd=self.repo).stdout
        self.assertIn("-def old_name():", out)
        self.assertIn("+def new_name():", out)
        self.assertIn("3 replacement(s) in 2 file(s): nothing written", out)
        self.assertEqual(read_text(os.path.join(self.repo, "a.py")), before, "a preview writes nothing")
        got = json.loads(self.fm("codemod", "rename", "old_name", "new_name", "--apply", "--json", cwd=self.repo).stdout)
        self.assertEqual((got["replacements"], got["applied"]), (3, True))
        a = read_text(os.path.join(self.repo, "a.py"))
        self.assertIn("new_name()\n", a)
        self.assertIn("not_old_name_x = 1", a, "a whole word only")
        with open(os.path.join(self.repo, "blob.dat"), "rb") as f:
            self.assertEqual(f.read(), b"old_name\0binary", "a binary file is never rewritten")

    def test_sub_takes_a_regex_and_paths_narrow_it(self):
        self.fm("codemod", "sub", r"old_(\w+)", r"new_\1", "a.py", "--apply", cwd=self.repo)
        self.assertIn("not_new_name_x", read_text(os.path.join(self.repo, "a.py")))
        self.assertEqual(read_text(os.path.join(self.repo, "docs", "b.txt")), "old_name in the docs\n")
        for bad in (["sub", "(", "x"], ["rename", "a.b", "c"], ["rename", "x"]):
            p = self.fm("codemod", *bad, cwd=self.repo, check=False)
            self.assertNotEqual(p.returncode, 0, bad)


class Dev(ForemanTestCase):
    def test_once_runs_the_affected_check_and_returns_its_code(self):
        self.fm("init")
        want = self.fm("check", "--affected", check=False).returncode
        self.assertEqual(self.fm("dev", "--once", check=False).returncode, want)
