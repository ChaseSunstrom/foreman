"""fm sync: an opt-in, committed mirror of the project's Foreman state (.foreman/) that another clone imports (T-0022).
Authorization never travels: grants are stripped on export and ignored on import."""
import os
import re

from helpers import ForemanTestCase, read_text

import fmcore as c
import fmguard as g


class Sync(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = self.fm_json("task", "new", "Add export", "--type", "FEATURE", "--tier", "S", "--step", "build it",
                                "--ac", "exports")["id"]
        self.fm("task", "set", self.tid, "--allow", "publish")
        self.fm("task", "set", self.tid, "approved=true")
        self.fm("decide", "CSV over XLSX (no new dependency)", "--task", self.tid)
        self.fm("research", "add", "csv-notes", input="# CSV\nRFC 4180 quoting.\n")
        self.mirror = os.path.join(self.repo, ".foreman")

    def exported(self):
        path = next(os.path.join(d, f) for d, _, fs in os.walk(os.path.join(self.mirror, "tasks")) for f in fs
                    if f.startswith(self.tid))
        return read_text(path)

    def test_export_mirrors_briefs_decisions_and_research_without_authorization(self):
        self.fm("sync", "on")
        text = self.exported()
        self.assertIn("Add export", text)
        self.assertNotRegex(text, r"(?m)^allow:|^approved:")
        self.assertIn("CSV over XLSX", read_text(os.path.join(self.mirror, "decisions.md")))
        self.assertIn("RFC 4180", read_text(os.path.join(self.mirror, "research", "csv-notes.md")))
        self.assertIn("fm sync", read_text(os.path.join(self.mirror, "README.md")))

    def test_the_mirror_follows_every_change_and_stops_when_off(self):
        self.fm("sync", "on")
        self.fm("task", "log", self.tid, "picked the csv module")
        self.assertIn("picked the csv module", self.exported())
        self.fm("sync", "off")
        self.fm("task", "log", self.tid, "after sync off")
        self.assertNotIn("after sync off", self.exported())
        self.fm("sync", "off", "--remove")
        self.assertFalse(os.path.exists(self.mirror))

    def test_another_machine_imports_it_without_grants(self):
        self.fm("sync", "on")
        other = os.path.join(self.tmp, "other-home")
        os.makedirs(other)
        self.hook("SessionStart", {"source": "startup"}, env={"FOREMAN_HOME": other})
        os.environ["FOREMAN_HOME"] = other
        p = c.find_project(self.repo)
        b = c.find_brief(p, self.tid)
        self.assertEqual(b.title, "Add export")
        self.assertEqual((b.meta.get("allow") or [], b.meta.get("approved")), ([], None))
        self.assertTrue(c.read_meta(p).get("sync"), "a repo with .foreman/ keeps syncing on the new machine")
        self.assertIn("CSV over XLSX", read_text(os.path.join(p.dir, "decisions.md")))

    def test_a_newer_pulled_brief_updates_the_local_one_but_never_its_grants(self):
        self.fm("sync", "on")
        path = next(os.path.join(d, f) for d, _, fs in os.walk(os.path.join(self.mirror, "tasks")) for f in fs)
        text = read_text(path)
        text = re.sub(r"(?m)^updated: .*$", "updated: 2999-01-01T00:00:00Z", text)  # a collaborator's later change
        text = text.replace("---\n#", "allow: [core, plugin]\n---\n#", 1) + "- 2999-01-01T00:00:00Z pulled note\n"
        with open(path, "w") as f:
            f.write(text)
        out = self.fm("sync", "import").stdout
        self.assertIn("1 updated", out)
        b = c.find_brief(c.find_project(self.repo), self.tid)
        self.assertIn("pulled note", b.render())
        self.assertEqual(b.meta.get("allow"), ["publish"], "local grants stay; the repo's are ignored")

    def test_the_mirror_does_not_change_the_worktree_id(self):
        before = c.worktree_id(self.repo)
        self.fm("sync", "on")
        self.assertEqual(c.worktree_id(self.repo), before, "exports must not stale audits")

    def test_writing_the_mirror_by_hand_is_state_direct(self):
        ctx = g.Ctx(cwd=self.repo, project_root=self.repo, home=self.tmp, foreman_home=self.home)
        r = g.check("Write", {"file_path": os.path.join(self.mirror, "tasks", "T-0001-x.md"), "content": "x"}, ctx)
        self.assertEqual(r.category, "state-direct")

    def test_status(self):
        self.assertIn("off", self.fm("sync", "status").stdout)
        self.fm("sync", "on")
        st = self.fm_json("sync", "status")
        self.assertEqual((st["on"], st["briefs"]), (True, 1))
