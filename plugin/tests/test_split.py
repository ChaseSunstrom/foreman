"""T-0709 (Frontier 09, first slice): a big task splits along the code's seams into child tasks, and only a capsule
comes back up."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c

CLUSTERS = {"a": ["alpha_core.py", "alpha_view.py", "alpha_store.py"],
            "b": ["beta_core.py", "beta_view.py", "beta_store.py"]}


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        for k, files in CLUSTERS.items():
            for f in files:  # each file names the others in its cluster: the code graph's 'uses' edges
                others = " ".join(os.path.splitext(o)[0] for o in files if o != f)
                self.write(f, f"# uses {others}\nX = 1\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        for k, files in CLUSTERS.items():  # and they change together
            for f in files:
                self.write(f, open(os.path.join(self.repo, f)).read() + f"# {k}\n")
            self.git("commit", "-qam", f"cluster {k}")
        self.fm("task", "new", "Rework everything", "--type", "FEATURE", "--tier", "L", "--scope", "*.py",
                "--ac", "all fine :: true")

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as f:
            f.write(text)

    def git(self, *a):
        subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True)


class Split(Base):
    def test_coupled_files_stay_together_and_the_parent_waits_for_its_children(self):
        data = json.loads(self.fm("task", "split", "T-0001", "--parts", "2", "--json").stdout)
        parts = [set(x["files"]) for x in data["children"]]
        self.assertIn(set(CLUSTERS["a"]), parts)
        self.assertIn(set(CLUSTERS["b"]), parts)
        p = c.find_project(self.repo)
        kids = [b for b in c.load_briefs(p) if b.meta.get("parent") == "T-0001"]
        self.assertEqual(len(kids), 2)
        self.assertTrue(all(set(k.meta.get("scope") or []) in parts for k in kids))
        r = self.fm("task", "done", "T-0001", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(kids[0].id, r.stdout + r.stderr)


class Capsule(Base):
    def test_a_finished_child_returns_a_bounded_capsule(self):
        self.fm("task", "split", "T-0001", "--parts", "2")
        kid = next(b for b in c.load_briefs(c.find_project(self.repo)) if b.meta.get("parent") == "T-0001")
        f = sorted(kid.meta["scope"])[0]
        self.fm("focus", kid.id)
        self.write(f, "X = 2\n")
        self.fm("task", "finish", kid.id, "--audit", "self", "--run", "true", "--commit", "Part one")
        out = self.fm("task", "capsule", kid.id).stdout
        self.assertLessEqual(len(out.strip().splitlines()), 15)
        self.assertIn(f, out)
        self.assertIn("done", out)
        self.assertIn("verif", out.lower())
