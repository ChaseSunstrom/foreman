"""T-1554: fm new web in a new folder makes a project born proven (its own check is its gate, and passes); fm codemod
previews a rewrite as a diff and writes it only with --apply; fm dev --once runs the affected tests."""
import json
import os
import subprocess
import sys

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


class BuildWhatIsMissing(ForemanTestCase):
    """T-2278: fm new tool NAME (a stdlib script and the test that fails until it works) and fm new skill NAME."""
    def new(self, *a, check=True):
        return self.fm("new", *a, "--json", env={"PATH": os.path.join(PLUGIN, "bin") + os.pathsep + os.environ["PATH"]},
                       cwd=self.tmp, check=check)

    def test_a_tool_lands_with_a_test_that_fails_and_passes_its_check(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        got = json.loads(self.new("tool", "shout", d).stdout)
        tool, test = os.path.join(d, "tools", "shout.py"), os.path.join(d, "tests", "test_shout.py")
        self.assertEqual(sorted(got["wrote"]), sorted([tool, test]))
        self.assertIn("argparse", read_text(tool))
        self.assertNotIn("__NAME__", read_text(tool) + read_text(test))
        h = subprocess.run([sys.executable, tool, "--help"], capture_output=True, text=True)
        self.assertEqual((h.returncode, "usage:" in h.stdout), (0, True))
        self.assertEqual(subprocess.run([sys.executable, tool], capture_output=True).returncode, 2)  # bad usage
        red = subprocess.run([sys.executable, test], capture_output=True, text=True)
        self.assertNotEqual(red.returncode, 0, "the test fails until the tool does its job")
        ok = self.new("check", tool, "--run", check=False)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)

    def test_a_tool_that_ignores_help_fails_its_check(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        self.new("tool", "shout", d)
        tool = os.path.join(d, "tools", "shout.py")
        with open(tool, "w") as f:
            f.write("# fm new tool\nprint('hi')\n")
        p = self.new("check", tool, "--run", check=False)
        self.assertEqual(p.returncode, 1, p.stdout)

    def test_the_checked_tool_runs_sandboxed_without_our_secrets(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        self.new("tool", "shout", d)
        tool = os.path.join(d, "tools", "shout.py")
        with open(tool, "w") as f:
            f.write("# fm new tool\nimport argparse, os, sys\n"
                    "if os.environ.get('T2278_SECRET') or os.path.expanduser('~') != os.getcwd():\n    sys.exit(7)\n"
                    "argparse.ArgumentParser(prog='x').parse_args()\n")
        env = {"PATH": os.path.join(PLUGIN, "bin") + os.pathsep + os.environ["PATH"], "T2278_SECRET": "hunter2"}
        p = self.fm("new", "check", tool, "--run", "--json", env=env, cwd=self.tmp, check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_a_half_written_tool_is_undone_whole(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        with open(os.path.join(d, "tests"), "w") as f:  # a file where the test's folder should be
            f.write("x")
        p = self.new("tool", "foo", d, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(d, "tools", "foo.py")), "nothing of ours is left")

    def test_a_symlinked_folder_and_a_stdlib_name_are_refused(self):
        d, out = os.path.join(self.tmp, "proj"), os.path.join(self.tmp, "outside")
        os.makedirs(d)
        os.makedirs(out)
        os.symlink(out, os.path.join(d, "tools"))
        self.assertNotEqual(self.new("tool", "foo", d, check=False).returncode, 0)
        os.symlink(out, os.path.join(d, ".claude"))
        self.assertNotEqual(self.new("skill", "foo", d, check=False).returncode, 0)
        self.assertEqual(os.listdir(out), [], "nothing written through a link")
        for bad in ("json", "os", "sys"):
            self.assertNotEqual(self.new("tool", bad, self.tmp, check=False).returncode, 0, bad)

    def test_the_hint_says_run_and_the_description_is_quoted(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        p = self.fm("new", "tool", "shout", d, env={"PATH": os.path.join(PLUGIN, "bin") + os.pathsep + os.environ["PATH"]},
                    cwd=self.tmp)
        self.assertIn("fm new check --run ", p.stdout)
        self.new("skill", "tidy", d)
        text = read_text(os.path.join(d, ".claude", "skills", "tidy", "SKILL.md"))
        self.assertIn('description: "Use whenever ', text)

    def test_a_skill_lands_in_the_listing_format_and_passes_its_check(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        got = json.loads(self.new("skill", "tidy-logs", d).stdout)
        path = os.path.join(d, ".claude", "skills", "tidy-logs", "SKILL.md")
        self.assertEqual(got["wrote"], [path])
        text = read_text(path)
        desc = json.loads(next(x for x in text.splitlines() if x.startswith("description: "))[len("description: "):])
        self.assertTrue(desc.startswith("Use whenever "))
        self.assertLessEqual(len(desc), 125)
        self.assertEqual(self.new("check", path, check=False).returncode, 0)
        with open(path, "w") as f:
            f.write("---\nname: tidy-logs\ndescription: Tidies logs.\n---\nbody\n")
        self.assertEqual(self.new("check", path, check=False).returncode, 1)

    def test_neither_overwrites_and_a_bad_name_is_refused(self):
        d = os.path.join(self.tmp, "proj")
        os.makedirs(d)
        for kind in ("tool", "skill"):
            self.new(kind, "demo", d)
            again = self.new(kind, "demo", d, check=False)
            self.assertNotEqual(again.returncode, 0)
            self.assertIn("exists", again.stdout + again.stderr)
        os.unlink(os.path.join(d, "tests", "test_demo.py"))  # half there: the other file is still not overwritten
        with open(os.path.join(d, "tools", "demo.py"), "w") as f:
            f.write("mine\n")
        self.assertNotEqual(self.new("tool", "demo", d, check=False).returncode, 0)
        self.assertEqual(read_text(os.path.join(d, "tools", "demo.py")), "mine\n")
        self.assertFalse(os.path.exists(os.path.join(d, "tests", "test_demo.py")), "nothing written on a refusal")
        for kind, bad in (("tool", "../x"), ("tool", "Bad Name"), ("tool", "a-b"), ("tool", "1x"), ("tool", ""),
                          ("skill", "../x"), ("skill", "A"), ("skill", "a_b"), ("skill", "-x"), ("skill", "x" * 40)):
            with self.subTest(kind=kind, name=bad):
                self.assertNotEqual(self.new(kind, bad, d, check=False).returncode, 0)
        self.assertEqual(sorted(os.listdir(os.path.join(d, "tools"))), ["demo.py"])


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
