"""T-0707 (Frontier 07, first slice): one local graph of code, tasks and commits with time on its edges, queried for a
change's blast radius and a task's ranked read-set, as of any moment."""
import json
import os
import subprocess

from helpers import ForemanTestCase

FILES = {"app/auth.py": "def check_token(t):\n    return bool(t)\n",
         "app/session.py": "import auth\n\n\ndef open_session(t):\n    return auth.check_token(t)\n",
         "app/billing.py": "def invoice(total):\n    return round(total, 2)\n",
         "tests/test_auth.py": "import auth\n"}


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Fix login token expiry", "--type", "FIX", "--tier", "S")
        self.fm("task", "new", "Add invoices", "--type", "FEATURE", "--tier", "S")
        for rel, text in FILES.items():
            self.write(rel, text)
        self.commit("base", "2026-01-01T10:00:00Z")
        self.write("app/auth.py", FILES["app/auth.py"] + "\n\nTTL = 60\n")
        self.write("app/session.py", FILES["app/session.py"] + "\n\nREFRESH = True\n")
        self.commit("Fix login token expiry\n\nForeman-Task: T-0001", "2026-02-01T10:00:00Z")
        self.write("app/billing.py", FILES["app/billing.py"] + "\n\nCURRENCY = 'EUR'\n")
        self.commit("Add invoices\n\nForeman-Task: T-0002", "2026-03-01T10:00:00Z")

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def commit(self, msg, when):
        env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True, env=env)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True, env=env)


class Blast(Base):
    def test_dependents_co_change_tests_and_past_fixes_as_of_a_moment(self):
        out = self.fm("graph", "blast", "app/auth.py").stdout
        self.assertIn("app/session.py", out)
        self.assertIn("tests/test_auth.py", out)
        self.assertIn("T-0001", out)
        self.assertIn("co-change", out)
        before = self.fm("graph", "blast", "app/auth.py", "--as-of", "2026-01-15T00:00:00Z").stdout
        self.assertNotIn("T-0001", before)
        self.assertNotIn("co-change: app/session.py", before)


class Pack(Base):
    def test_a_tasks_words_reach_files_through_past_tasks(self):
        data = json.loads(self.fm("graph", "pack", "login token refresh is broken", "--json").stdout)
        files = [f["path"] for f in data["files"]]
        self.assertEqual(set(files[:2]), {"app/auth.py", "app/session.py"}, files)
        self.assertTrue("app/billing.py" not in files or files.index("app/billing.py") > 1)


class Graphify(Base):
    def test_graphify_edges_become_file_edges(self):
        self.write("graphify-out/graph.json", json.dumps({
            "nodes": [{"id": "inv", "source_file": os.path.join(self.repo, "app/billing.py")},
                      {"id": "sess", "source_file": "app/session.py"}],
            "links": [{"source": "inv", "target": "sess", "relation": "calls"}]}))
        out = self.fm("graph", "blast", "app/session.py").stdout
        self.assertIn("app/billing.py", out.split("co-change")[0])
