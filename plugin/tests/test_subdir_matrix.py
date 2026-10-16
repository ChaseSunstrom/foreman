"""T-1185: the path-taking verbs give the same result run from the repo root, from a subdirectory and through a symlink
to the checkout (path bugs kept shipping: T-1148 a lease path doubled from a subdirectory; T-1165 a --file read from
the root, not the cwd). Each verb runs in a fresh repo per place; the normalised output, exit code and repo files are
compared with the root's."""
import json
import os
import re
import subprocess

from helpers import ForemanTestCase, git_repo

PLACES = ("root", "subdir", "symlink")


class SubdirMatrix(ForemanTestCase):
    def place(self, where):
        """A fresh initialised repo (same name, own parent) and the folder to run from."""
        parent = os.path.join(self.tmp, where)
        os.makedirs(parent)
        repo = git_repo(parent)
        for rel, text in (("src/a.txt", "one\n"), ("tests/test_a.py", "def test_a(): pass\n"), ("sub/.keep", "")):
            os.makedirs(os.path.join(repo, os.path.dirname(rel)), exist_ok=True)
            with open(os.path.join(repo, rel), "w") as f:
                f.write(text)
        subprocess.run(["git", "-C", repo, "add", "."], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "files"], check=True)
        self.fm("init", cwd=repo)
        self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true", "--step", "s", cwd=repo)
        cwd = repo
        if where == "subdir":
            cwd = os.path.join(repo, "sub")
        elif where == "symlink":
            cwd = os.path.join(parent, "link")
            os.symlink(repo, cwd)
        return repo, cwd

    def snapshot(self, repo):
        out = {}
        for d, _, files in os.walk(repo):
            if {".git", "__pycache__"} & set(d.split(os.sep)):
                continue
            for n in files:
                p = os.path.join(d, n)
                with open(p, errors="replace") as f:
                    out[os.path.relpath(p, repo)] = f.read()
        return out

    def run_matrix(self, make_args, setup=None, files=None, after=None):
        """make_args(repo, cwd) -> argv; files: [(rel, text)] written first; after: extra fm argv to run and record."""
        results = {}
        for where in PLACES:
            repo, cwd = self.place(where)
            for rel, text in (files or {}).items():
                with open(os.path.join(repo, rel), "w") as f:
                    f.write(text)
            if setup:
                setup(repo, cwd)
            p = self.fm(*make_args(repo, cwd), cwd=cwd, check=False)
            extra = self.fm(*after, cwd=cwd, check=False).stdout if after else ""
            link = os.path.join(os.path.dirname(repo), "link")

            def norm(s):
                s = s.replace(link, "<R>").replace(repo, "<R>")
                s = re.sub(r"app-[0-9a-f]{6}|\b[0-9a-f]{20,40}\b", "<H>", s)
                return re.sub(r"\d{4}-\d\d-\d\dT[\d:.]+Z?|\b\d+(\.\d+)?m?s\b", "<T>", s)
            results[where] = (p.returncode, norm(p.stdout + p.stderr), norm(extra), self.snapshot(repo))
        for where in PLACES[1:]:
            self.assertEqual(results[where], results["root"], f"from {where} differs from the root")
        self.assertEqual(results["root"][0], 0, results["root"])
        return results["root"]

    def test_subdir_matrix_lease(self):
        res = self.run_matrix(lambda r, c: ["lease", "take", "src/a.txt"], after=["lease", "list"])
        self.assertIn("src/a.txt", res[2])
        self.assertNotIn("sub/src", res[2])

    def test_subdir_matrix_edit(self):
        def setup(repo, cwd):
            with open(os.path.join(repo, "batch.json"), "w") as f:
                json.dump([{"file": "src/a.txt", "old": "one", "new": "two"}], f)
            self.fm("focus", "T-0001", cwd=cwd)
        res = self.run_matrix(lambda r, c: ["edit", "--file", os.path.relpath(os.path.join(r, "batch.json"), c)], setup=setup)
        self.assertEqual(res[3]["src/a.txt"], "two\n")

    def test_subdir_matrix_evidence(self):
        res = self.run_matrix(lambda r, c: ["task", "evidence", "T-0001", "--step", "1", "--run",
                                            "python3 -m py_compile tests/test_a.py"])
        self.assertIn("T-0001", res[1] + res[1])

    def test_subdir_matrix_check_affected(self):
        def setup(repo, cwd):
            self.fm("check", "affected", "python3 -c 'print(1)' {tests}", cwd=cwd)
            self.fm("check", "add", "true", cwd=cwd)
        self.run_matrix(lambda r, c: ["check", "--affected"], setup=setup,
                        files={"tests/test_a.py": "def test_a(): assert 1\n"})

    def test_subdir_matrix_focus(self):
        self.run_matrix(lambda r, c: ["focus", "T-0001"], after=["task", "show", "T-0001"])

    def test_subdir_matrix_inbox_spec(self):
        def setup(repo, cwd):
            with open(os.path.join(repo, "spec.md"), "w") as f:
                f.write("- [ ] write the thing\n")
        self.run_matrix(lambda r, c: ["inbox", "spec", os.path.relpath(os.path.join(r, "spec.md"), c)], setup=setup, after=["inbox"])

    def test_subdir_matrix_guard_wrong(self):
        self.run_matrix(lambda r, c: ["guard", "wrong", "git status", "--should", "allow", "--why", "x"],
                        after=["guard", "try", "git status"])

    def test_subdir_matrix_intake_file(self):
        def setup(repo, cwd):
            with open(os.path.join(repo, "in.txt"), "w") as f:
                f.write("FIX: a thing\n")
        self.run_matrix(lambda r, c: ["intake", "--file", os.path.relpath(os.path.join(r, "in.txt"), c), "--json"], setup=setup)
