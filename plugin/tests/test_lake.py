"""T-2974: the training lake, `sampo exam models --export DIR`: one provenance-tagged table across every project on the
machine, outcome-labelled, names and paths stripped, sensitive and opted-out projects left out, Claude's text refused."""
import getpass
import json
import os
import subprocess

from helpers import SampoTestCase

from sampo import core as c
from sampo import lake

OLD = "2026-01-01T00:00:00Z"


class Lake(SampoTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.make(self.repo, [
            ("fix the parser crash in /home/zed/secretproj/src/a.py", "FIX", "held"),
            ("add a csv export, see fmcore and fm task", "FEATURE", "revert"),
            ("add a json export for the Hidden project", "FEATURE", "held"),  # another project's name is stripped too
            ("add a json export", "FEATURE", "held"),
            ("add a json export", "FEATURE", "held"),  # a duplicate request
            (f"ls says -rw-r--r-- 1 {getpass.getuser()} grp; pushed to git@github.com:SomeOwner/tool.git; see OwnerZed/app, ownerzed.github.io, by Zed Person", "FIX", "held")])
        subprocess.run(["git", "-C", self.repo, "remote", "add", "origin", "git@github.com:OwnerZed/app.git"], check=True)
        subprocess.run(["git", "-C", self.repo, "config", "user.name", "Zed Person"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-q", "--allow-empty", "-m", 'Revert "add csv (T-0002)"', "-m", "This reverts commit abc."], check=True)
        self.other = self.sub("other")
        self.make(self.other, [("rename the widget", "CLEAN", "held")])
        self.hidden = self.sub("hidden")
        self.make(self.hidden, [("hidden thing", "FIX", "held")])
        c.update_meta(c.find_project(self.hidden), sensitive=True)
        self.out = os.path.join(self.tmp, "lake")

    def sub(self, name):
        root = os.path.join(self.tmp, name)
        os.makedirs(root)
        subprocess.run(["git", "init", "-q", "-b", "main", root], check=True)
        subprocess.run(["git", "-C", root, "config", "user.email", "t@e.com"], check=True)
        subprocess.run(["git", "-C", root, "config", "user.name", "t"], check=True)
        subprocess.run(["git", "-C", root, "commit", "-q", "--allow-empty", "-m", "init"], check=True)
        self.fm("init", cwd=root)
        return root

    def make(self, root, specs):
        p = c.find_project(root)
        for text, typ, _ in specs:
            tid = json.loads(self.fm("capture", f"task number {len(c.load_briefs(p)) + 1}", "--json", cwd=root).stdout)["id"]
            b = c.find_brief(p, tid)
            b.set_section("Raw request", f"> {text}\n")
            b.meta.update(type=typ, status="done", updated=OLD)
            b.set_section("Interpretation", "Reading 1: the agent's own words about it\n")
            b.set_section("Log", f"- {OLD} done\n")
            c.save_brief(p, b)
        c.log_event(p, "evidence", "T-0001", {"step": 1, "cmd": "pytest", "result": "exit 0 · 3 passed in /home/zed/x"})

    def export(self, *flags):
        r = self.fm("exam", "models", "--export", self.out, "--json", *flags)
        with open(os.path.join(self.out, "rows.jsonl")) as f:
            return json.loads(r.stdout), [json.loads(x) for x in f]

    def test_rows_labels_exclusions_and_stripping(self):
        man, rows = self.export()
        real = [r for r in rows if not r.get("canary")]
        text = json.dumps(real)
        self.assertEqual(len(real), 6)  # 7 tasks in two projects, minus the duplicate request; the sensitive one is out
        self.assertNotIn("hidden thing", text)
        self.assertNotIn("Hidden", text)
        self.assertEqual(man["excluded"], {"sensitive": 1, "optout": 0})
        labels = sorted(r["label"] for r in real)
        self.assertEqual(labels.count("reverted"), 1)
        self.assertEqual(man["dupes"], 1)
        for needle in ("/home/zed", "secretproj", self.tmp, "fmcore", "fm task", getpass.getuser(), "SomeOwner", "OwnerZed", "ownerzed", "Zed Person"):
            self.assertNotIn(needle, text)
        self.assertIn("sampo.core", text)
        self.assertEqual(sum(man["rows_per_project"].values()), 6)
        for r in real:
            self.assertTrue(r["prov"]["project"] and r["prov"]["task"] and r["weight"] > 0)
            self.assertIn(r["split"], ("train", "test"))
            self.assertNotIn("task_id", r)

    def test_authors_agent_text_off_by_default_tool_text_quarantined(self):
        _, rows = self.export()
        r = next(x for x in rows if not x.get("canary") and x["fields"].get("request"))
        self.assertEqual(r["fields"]["request"]["author"], "user")
        self.assertNotIn("interpretation", r["fields"])
        self.assertNotIn("the agent's own words", json.dumps(rows))
        tools = [x["tool_text"] for x in rows if x.get("tool_text")]
        self.assertTrue(tools and all(t["author"] == "tool" for t in tools))
        _, rows = self.export("--with-agent")
        self.assertEqual(next(x for x in rows if x["fields"].get("interpretation"))["fields"]["interpretation"]["author"], "agent")

    def test_optout_and_a_symlink_to_a_sensitive_root_are_left_out(self):
        link = os.path.join(self.tmp, "alias")
        os.symlink(self.hidden, link)
        po = c.find_project(self.other)
        c.update_meta(po, path=link)  # not sensitive in its own meta: its real path is
        man, rows = self.export()
        self.assertNotIn("rename the widget", json.dumps(rows))
        self.assertEqual(man["excluded"], {"sensitive": 2, "optout": 0})
        c.update_meta(po, path=self.other, lake_optout=True)
        man, rows = self.export()
        self.assertNotIn("rename the widget", json.dumps(rows))
        self.assertEqual(man["excluded"], {"sensitive": 1, "optout": 1})

    def test_a_rerun_gives_the_same_hash_and_the_canary_is_in_the_manifest(self):
        a, rows = self.export()
        b, _ = self.export()
        self.assertEqual(a["hash"], b["hash"])
        self.assertTrue(a["canary"] and any(r.get("canary") == a["canary"] for r in rows))
        self.fm("capture", "a new thing")  # a fresh task changes nothing in the export of done tasks
        self.assertEqual(self.export()[0]["hash"], a["hash"])
        self.make(self.other, [("more work", "FIX", "held")])
        self.assertNotEqual(self.export()[0]["hash"], a["hash"])

    def test_manifest_lands_in_research_and_nulls_are_fine(self):
        p = c.find_project(self.repo)
        b = c.find_brief(p, "T-0004")
        b.set_section("Raw request", "")
        c.save_brief(p, b)
        man, rows = self.export()
        self.assertTrue(os.path.getsize(os.path.join(p.dir, "research", "models", "lake-manifest.json")) > 0)
        self.assertTrue(os.path.exists(os.path.join(self.out, "manifest.json")))
        self.assertEqual(man["rows"], len(rows) - 1)  # the canary is not a row of any project
