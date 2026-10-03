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
        text = text.replace("---\n#", "allow: [core, plugin]\nplugin_pin: [evil@m, 0000, 9999999999]\n---\n#", 1) \
            + "- 2999-01-01T00:00:00Z pulled note\n"
        with open(path, "w") as f:
            f.write(text)
        out = self.fm("sync", "import").stdout
        self.assertIn("1 updated", out)
        b = c.find_brief(c.find_project(self.repo), self.tid)
        self.assertIn("pulled note", b.render())
        self.assertEqual(b.meta.get("allow"), ["publish"], "local grants stay; the repo's are ignored")
        self.assertNotIn("plugin_pin", b.meta, "a pinned plugin yes (T-0036) never comes from the repo either")

    def pulled(self, text_fn, rel=None):
        """Change the mirror the way a git pull would."""
        path = rel and os.path.join(self.mirror, rel) or next(
            os.path.join(d, f) for d, _, fs in os.walk(os.path.join(self.mirror, "tasks")) for f in fs)
        text = text_fn(read_text(path) if os.path.exists(path) else "")
        with open(path, "w") as f:
            f.write(text)
        return path

    def test_marks_audits_and_focus_from_elsewhere_do_not_count_here(self):
        # round-3 adversary audit: a pulled brief can't satisfy this machine's run, audit or plan gates
        self.fm("sync", "on")
        self.pulled(lambda t: t.replace("status: planned", "status: active") + "\n- (step 1) `pytest` → exit 0 · ok"
                    " [ran] [tree deadbeef0000] (2999-01-01T00:00:00Z)\n- (audit intent) `x` → ok [tree deadbeef0000]"
                    " (2999-01-01T00:00:00Z)\n")
        self.fm("sync", "import")
        b = c.find_brief(c.find_project(self.repo), self.tid)
        self.assertIn("exit 0 · ok", b.render(), "the pulled evidence arrived")
        self.assertIn("(audit intent, imported)", b.render())
        self.assertEqual(b.audits(), [])
        self.assertNotIn("[ran]", b.render())
        self.assertNotIn("[tree", b.render())
        self.assertEqual(b.status, "planned", "focus is per machine")

    def test_a_pull_is_never_overwritten_by_the_next_export(self):
        # round-3 edge audit: exports run on every fm change; a pulled change must wait for the import, not be lost
        self.fm("sync", "on")
        self.pulled(lambda t: t + "- 2026-09-26T00:00:00Z from the other machine\n")
        self.fm("task", "log", self.tid, "local note")  # the next fm command takes the pull in first, then works on it
        here = c.find_brief(c.find_project(self.repo), self.tid).render()
        self.assertIn("from the other machine", here)
        self.assertIn("local note", here)
        self.assertIn("from the other machine", self.exported())
        self.assertIn("local note", self.exported())

    def test_both_sides_changed_keeps_local_and_saves_theirs(self):
        self.fm("sync", "on")
        self.fm("sync", "off")
        self.fm("task", "log", self.tid, "local only change")
        self.pulled(lambda t: t + "- 2026-09-26T00:00:00Z their change\n")
        out = self.fm("sync", "import").stdout
        self.assertIn("conflict", out)
        p = c.find_project(self.repo)
        self.assertIn("local only change", c.find_brief(p, self.tid).render())
        saved = os.path.join(p.dir, "sync-conflicts")
        self.assertTrue(any("their change" in read_text(os.path.join(saved, f)) for f in os.listdir(saved)))

    def test_unresolved_merges_symlinks_and_odd_names_are_refused(self):
        self.fm("sync", "on")
        self.pulled(lambda t: t + "<<<<<<< HEAD\nmine\n=======\ntheirs\n>>>>>>> branch\n")
        secret = os.path.join(self.tmp, "secret.txt")
        with open(secret, "w") as f:
            f.write("TOP SECRET\n")
        os.symlink(secret, os.path.join(self.mirror, "research", "leak.md"))
        out = self.fm("sync", "import").stdout
        self.assertIn("merge conflict", out)
        p = c.find_project(self.repo)
        self.assertFalse(os.path.exists(os.path.join(p.dir, "research", "leak.md")))
        with open(os.path.join(p.dir, "tasks", "notes.md"), "w") as f:
            f.write("not a brief\n")
        self.fm("task", "log", self.tid, "still works")  # export skips names that aren't briefs
        os.mkfifo(os.path.join(self.mirror, "research", "pipe.md"))  # a reader would block on it forever
        self.fm("sync", "import")
        self.fm("task", "log", self.tid, "no hang")

    def test_code_in_the_mirror_folder_still_counts_for_audits(self):
        self.fm("sync", "on")
        before = c.worktree_id(self.repo)
        with open(os.path.join(self.mirror, "payload.py"), "w") as f:
            f.write("import os\n")
        self.assertNotEqual(c.worktree_id(self.repo), before)

    def test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror(self):
        self.fm("sync", "on")
        self.fm("focus", self.tid)
        self.fm("checkpoint", "--note", "x")
        self.assertNotIn(".foreman", c.find_brief(c.find_project(self.repo), self.tid).section("Resume here"))
        other = os.path.join(self.tmp, "other-home")
        os.makedirs(other)
        env = {"FOREMAN_HOME": other}
        self.fm("init", env=env)
        self.fm("sync", "off", env=env)
        self.hook("SessionStart", {"source": "startup"}, env=env)
        os.environ["FOREMAN_HOME"] = other
        self.assertFalse(c.read_meta(c.find_project(self.repo)).get("sync"))

    def test_on_fails_cleanly_when_the_mirror_cannot_be_written_and_warns_when_ignored(self):
        with open(self.mirror, "w") as f:
            f.write("a file where the folder would go\n")
        p = self.fm("sync", "on", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertNotIn("Traceback", p.stderr)
        self.assertFalse(c.read_meta(c.find_project(self.repo)).get("sync"))
        os.remove(self.mirror)
        with open(os.path.join(self.repo, ".gitignore"), "a") as f:
            f.write(".*\n")
        self.assertIn("ignored", self.fm("sync", "on").stdout)

    def test_pulled_titles_cannot_carry_terminal_sequences(self):
        # round-4 adversary audit: fm queue printed titles straight from disk
        self.fm("sync", "on")
        self.pulled(lambda t: t.replace("# Add export", "# Add\x1b]0;pwned\x07 export‮", 1))
        self.fm("sync", "import")
        self.assertNotIn("\x1b", c.find_brief(c.find_project(self.repo), self.tid).title)
        self.assertNotIn("\x1b]0;pwned", self.fm("queue").stdout)

    def test_exports_are_redacted_and_huge_imports_skipped(self):
        # round 4 (brainstorm, security): the mirror is committed, so no secret may reach it from any older note
        p = c.find_project(self.repo)
        with open(os.path.join(p.dir, "research", "old-note.md"), "w") as f:
            f.write("deploy with token ghp_abcdefghijklmnopqrstuvwxyz0123456789AB\n")  # pragma: allowlist secret
        self.fm("sync", "on")
        text = read_text(os.path.join(self.mirror, "research", "old-note.md"))
        self.assertNotIn("ghp_", text)
        self.assertIn("[REDACTED]", text)
        with open(os.path.join(self.mirror, "research", "huge.md"), "w") as f:
            f.write("x" * 2_000_001)
        self.assertIn("too large", self.fm("sync", "import").stdout)
        self.assertFalse(os.path.exists(os.path.join(p.dir, "research", "huge.md")))

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
