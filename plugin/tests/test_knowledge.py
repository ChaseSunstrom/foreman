"""T-0694 (Intelligence — research and knowledge): dependency call sites read locally, research that ends in a
decision, a Chesterton check on deletions, prior art from other opted-in projects, cited explanations, and the hot
files no session has read."""
import json
import os
import subprocess

from helpers import ForemanTestCase, git_repo
from test_research import STUB

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def write(self, rel, text, root=None):
        path = os.path.join(root or self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def commit(self, msg, root=None):
        subprocess.run(["git", "-C", root or self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", root or self.repo, "commit", "-qm", msg], check=True)


class Deps(Base):
    def test_calls_lists_import_sites_and_the_names_used_without_the_network(self):
        self.write("requirements.txt", "requests>=2.0,<3\nleftpad>=1\n")
        self.write("app/net.py", "from requests import Session, get\n")
        self.write("app/other.py", "import requests\nrequests.post('x')\n")
        self.commit("deps")
        out = self.fm("deps", "--calls", env={"FOREMAN_OFFLINE": "1", "https_proxy": "http://127.0.0.1:9"}).stdout
        self.assertRegex(out, r"requests .*2 file\(s\)")
        self.assertIn("app/net.py:1", out)
        self.assertRegex(out, r"names used: .*Session")
        self.assertRegex(out, r"leftpad .*no import site")


class Decision(Base):
    def test_a_research_note_ends_in_a_decision_prompt_and_a_research_close_without_one_warns(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": os.path.join(self.tmp, "log")}
        self.fm("task", "new", "Which parser", "--type", "RESEARCH", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        res = json.loads(self.fm("research", "ask", "How fast is the json parser?", "--no-verify", "--task", "T-0001",
                                 "--json", env=env).stdout)
        with open(res["path"]) as f:
            note = f.read()
        self.assertIn("## Decision", note)
        self.assertIn("fm task set T-0001 --section Decision", note)
        import fmcli
        warns = fmcli._close_warnings(self.p, c.find_brief(self.p, "T-0001"), [])
        self.assertTrue(any("no Decision" in w for w in warns), warns)


class Chesterton(Base):
    def test_closing_a_task_that_deleted_a_file_warns_until_origins_say_why(self):
        self.write("legacy/shim.py", "X = 1\n")
        self.commit("shim")
        self.fm("task", "new", "Drop the shim", "--type", "CLEAN", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        os.remove(os.path.join(self.repo, "legacy", "shim.py"))
        import fmcli
        b = c.find_brief(self.p, "T-0001")
        self.assertTrue(any("legacy/shim.py" in w and "Origins" in w for w in fmcli._close_warnings(self.p, b, [])))
        self.fm("task", "set", "T-0001", "--section", "Origins", "--text", "- legacy/shim.py: py2 compat, gone since 2024")
        b = c.find_brief(self.p, "T-0001")
        self.assertFalse(any("Origins" in w for w in fmcli._close_warnings(self.p, b, [])))


class PriorArt(Base):
    def test_recall_repos_cites_other_opted_in_projects_and_skips_the_rest(self):
        shared, private = git_repo(self.tmp, "billing"), git_repo(self.tmp, "vault")
        for root in (shared, private):
            self.write("lib/invoice.py", "def parse_invoice(text):\n    return text\n", root=root)
            self.commit("invoice", root=root)
            self.fm("init", cwd=root)
        self.fm("share", "on", cwd=shared)
        out = self.fm("recall", "--repos", "parse_invoice").stdout
        self.assertRegex(out, r"billing.*lib/invoice\.py:1")
        self.assertNotIn("vault", out)


class Explain(Base):
    def test_explain_cites_where_the_named_identifiers_are_defined(self):
        self.write("lib/cache.py", "class SessionCache:\n    pass\n\n\ndef warm_cache(c):\n    return c\n")
        self.commit("cache")
        out = self.fm("recall", "--explain", "how does warm_cache fill the SessionCache?").stdout
        self.assertIn("lib/cache.py:5", out)
        self.assertIn("lib/cache.py:1", out)


class Cold(Base):
    def test_map_cold_lists_hot_files_no_session_read_and_capture_files_one_item(self):
        for i in range(3):
            self.write("hot.py", f"X = {i}\n")
            self.write("warm.py", f"Y = {i}\n")
            self.commit(f"edit {i}")
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a") as f:
            f.write(json.dumps({"ts": c.now(), "kind": "tool", "tool": "Read", "project": self.p.slug,
                                "target": os.path.join(self.repo, "warm.py")}) + "\n")
        out = self.fm("map", "--cold").stdout
        self.assertIn("hot.py", out)
        self.assertNotIn("warm.py", out)
        self.fm("map", "--cold", "--capture")
        self.fm("map", "--cold", "--capture")
        cold = [b for b in c.load_briefs(self.p) if b.meta.get("source") == "cold"]
        self.assertEqual(len(cold), 1)
        import fmnight
        self.assertIn("cold files", [n for n, _, _ in fmnight.jobs(self.p)])
