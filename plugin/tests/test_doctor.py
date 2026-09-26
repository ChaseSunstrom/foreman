"""fm doctor: each check passes on good fixtures and fails on bad ones; the command runs end to end."""
import json
import os
import subprocess
import tempfile
import unittest

from helpers import PLUGIN, ForemanTestCase, git_repo

import fmcore as c
import fmdoctor as d


class Checks(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.t = os.path.realpath(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = os.path.join(self.t, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        return path

    def test_settings_json(self):
        good = self.write("good.json", '{"a": 1}')
        bad = self.write("bad.json", "{nope")
        self.assertEqual(d.check_settings_json([good]).status, "PASS")
        r = d.check_settings_json([good, bad, os.path.join(self.t, "missing.json")])
        self.assertEqual(r.status, "FAIL")
        self.assertIn("bad.json", r.detail)

    def test_footprint(self):
        rules = self.write("rules.md", "# r\n" + "x\n" * 60)
        md = self.write("CLAUDE.md", "# me\n<!-- foreman:begin -->\n# Foreman\nline\n<!-- foreman:end -->\n")
        self.assertEqual(d.check_footprint(rules, md).status, "PASS")
        long_rules = self.write("long.md", "# r\n" + "x\n" * 90)
        self.assertEqual(d.check_footprint(long_rules, md).status, "FAIL")

    def test_frontmatter(self):
        self.assertEqual(d.check_frontmatter(PLUGIN).status, "PASS")
        root = os.path.join(self.t, "plug")
        self.write("plug/skills/x/SKILL.md", "---\nname: x\ndescription: does things well enough\n---\nbody\n")
        self.write("plug/agents/a.md", "---\nname: a\ndescription: agent\ntools: Read, Write\n---\n400 words\n")
        r = d.check_frontmatter(root)
        self.assertEqual(r.status, "FAIL")
        self.assertIn("Write", r.detail)
        self.write("plug/skills/y/SKILL.md", "no frontmatter here\n")
        self.assertIn("y", d.check_frontmatter(root).detail)

    def test_file_map(self):
        home = os.path.join(self.t, "fh")
        for rel in ("plugin/bin/fm", "plugin/lib/x.py", "README.md"):
            self.write(os.path.join("fh", rel), "x")
        master = self.write("fh/MASTER.md", "# M\n## 3. File map\n| Path | Purpose |\n|---|---|\n"
                                             "| `plugin/bin/` | cli |\n| `plugin/lib/` | code |\n| `README.md` | readme |\n"
                                             "| `state/logs/hooks.log` | hook errors (runtime) |\n## 4. Next\n")
        self.assertEqual(d.check_file_map(home, master).status, "PASS")
        self.write("fh/plugin/newdir/thing", "x")
        r = d.check_file_map(home, master)
        self.assertEqual(r.status, "FAIL")
        self.assertIn("plugin/newdir", r.detail)
        master2 = self.write("fh/MASTER2.md", "## 3. File map\n| `plugin/` | all |\n| `gone.md` | x |\n")
        self.assertIn("gone.md", d.check_file_map(home, master2).detail)
        self.assertEqual(d.check_file_map(home, os.path.join(home, "nope.md")).status, "FAIL")

    def test_git_hygiene(self):
        repo = git_repo(self.t, "r")
        self.write("r/.gitignore", "state/\n")
        subprocess.run(["git", "-C", repo, "add", ".gitignore"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "ignore"], check=True)
        self.assertEqual(d.check_git_hygiene(repo).status, "PASS")
        self.write("r/state/x.json", "{}")
        subprocess.run(["git", "-C", repo, "add", "-f", "state/x.json"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "oops"], check=True)
        self.assertIn("state/x.json", d.check_git_hygiene(repo).detail)
        subprocess.run(["git", "-C", repo, "rm", "-q", "--cached", "state/x.json"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "fix"], check=True)
        self.write("r/config.py", "API_KEY = 'sk-ant-api03-abcdefghijklmnopqrstu'\n")
        subprocess.run(["git", "-C", repo, "add", "config.py"], check=True)
        r = d.check_git_hygiene(repo)
        self.assertEqual(r.status, "FAIL")
        self.assertIn("config.py", r.detail)

    def test_backup(self):
        home = os.path.join(self.t, "fh")
        self.assertEqual(d.check_backup(home).status, "FAIL")
        self.write("fh/backups/claude-20260101-000000.tgz", "x")
        self.assertEqual(d.check_backup(home).status, "PASS")

    def test_statusline_and_deny(self):
        wrapper = "/x/plugin/hooks/statusline"
        manifest = {"statusLine_original": {"command": "orig"}, "deny_added": ["Bash(mkfs *)"]}
        settings = {"statusLine": {"command": wrapper}, "permissions": {"deny": ["Bash(mkfs *)"]}}
        self.assertEqual(d.check_statusline(settings, manifest, wrapper).status, "PASS")
        self.assertEqual(d.check_statusline({"statusLine": {"command": "other"}}, manifest, wrapper).status, "FAIL")
        self.assertEqual(d.check_statusline({}, None, wrapper).status, "WARN")
        self.assertEqual(d.check_deny_rules(settings, manifest).status, "PASS")
        self.assertEqual(d.check_deny_rules({"permissions": {"deny": []}}, manifest).status, "FAIL")


class Briefs(ForemanTestCase):
    def test_briefs_and_state(self):
        self.fm("task", "new", "a", "--type", "FIX", "--tier", "S")
        p = c.find_project(self.repo)
        self.assertEqual(d.check_briefs(p).status, "PASS")
        with open(os.path.join(p.dir, "STATE.md"), "a") as f:
            f.write("tampered\n")
        self.assertEqual(d.check_briefs(p).status, "WARN")
        with open(os.path.join(p.dir, "tasks", "T-0009-broken.md"), "w") as f:
            f.write("no frontmatter")
        r = d.check_briefs(p)
        self.assertEqual(r.status, "FAIL")
        self.assertIn("T-0009", r.detail)


class Command(ForemanTestCase):
    def test_doctor_json_runs_and_names_every_check(self):
        self.fm("init")
        p = self.fm("doctor", "--json", check=False, env={"HOME": self.tmp})
        self.assertIn(p.returncode, (0, 1))
        names = {r["name"] for r in json.loads(p.stdout)["results"]}
        for n in ("settings json", "hook scripts", "hook latency", "hook exit codes", "injection budgets", "footprint",
                  "frontmatter", "briefs", "file map", "backup", "plugin validate", "git hygiene", "statusline",
                  "deny rules", "rules symlink", "scripts", "name collisions", "hook state writers"):
            self.assertIn(n, names)


if __name__ == "__main__":
    unittest.main()
