"""T-1188: fm release VERSION: the release ritual as named steps with a checkpoint after each."""
import json
import os
import shutil
import subprocess

from helpers import ForemanTestCase, read_json, read_text

import fmcore as c

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def put(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def sh(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


class Release(ForemanTestCase):
    def setUp(self):
        super().setUp()
        shutil.copy(os.path.join(ROOT, "release.py"), self.repo)
        put(self.repo, "plugin/.claude-plugin/plugin.json", '{\n  "name": "foreman",\n  "version": "1.0.0"\n}\n')
        put(self.repo, "CHANGELOG.md", "# Changelog\n\n## Unreleased\n- a thing\n\n## 1.0.0 — 2026-01-01\n- first\n")
        put(self.repo, "mods/foreman-ui/.claude-plugin/plugin.json", '{\n  "name": "foreman-ui",\n  "version": "0.1.0"\n}\n')
        put(self.repo, "mods/foreman-ui/hooks/a.tsx", "a\n")
        self.market = {"name": "foreman", "metadata": {"version": "1.0.0"}, "plugins": [
            {"name": "foreman", "version": "1.0.0"}, {"name": "foreman-ui", "version": "0.1.0"}]}
        put(self.repo, ".claude-plugin/marketplace.json", json.dumps(self.market))
        self.fm("init")
        sh(self.repo, "add", ".")
        sh(self.repo, "commit", "-qm", "Foreman 1.0.0")

    def rel(self, *a, check=True):
        return self.fm("release", *a, check=check)

    def tid(self):
        t = json.loads(self.fm("task", "new", "ship", "--type", "FEATURE", "--tier", "S", "--json").stdout)["id"]
        self.fm("task", "step", t, "add", "ship it")
        self.fm("task", "ac", t, "add", "shipped", "--verify", "true")
        return t

    def test_dry_run_lists_every_step_and_changes_nothing(self):
        out = self.rel("9.9.9", "--dry-run").stdout
        for name in ("tree", "check", "bump", "changelog", "commit", "release-check", "canary", "push", "round"):
            self.assertIn(name, out)
        self.assertEqual(sh(self.repo, "status", "--porcelain"), "")
        self.assertEqual(read_json(os.path.join(self.repo, "plugin/.claude-plugin/plugin.json"))["version"], "1.0.0")

    def test_a_run_stopped_after_step_two_resumes_at_step_three(self):
        mk = os.path.join(self.repo, ".claude-plugin/marketplace.json")
        put(self.repo, ".claude-plugin/marketplace.json", "{broken")  # step 3 can't bump it
        sh(self.repo, "commit", "-qam", "break it")
        r = self.rel("9.9.9", "--no-check", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("bump", r.stderr + r.stdout)
        self.assertEqual(sh(self.repo, "log", "-1", "--format=%s").strip(), "break it")
        put(self.repo, ".claude-plugin/marketplace.json", json.dumps(self.market))
        sh(self.repo, "commit", "-qam", "fix it")
        self.assertNotEqual(self.rel("8.0.0", "--resume", "--no-check", check=False).returncode, 0, "another version")
        out = self.rel("9.9.9", "--resume", "--no-check").stdout
        self.assertIn("resuming at step 3", out)
        self.assertEqual(sh(self.repo, "log", "-1", "--format=%s").strip(), "Foreman 9.9.9")
        self.assertEqual(read_json(mk)["plugins"][0]["version"], "9.9.9")
        self.assertEqual(read_json(mk)["plugins"][1]["version"], "0.1.0", "the UI didn't change")
        self.assertIn("## 9.9.9 — ", read_text(os.path.join(self.repo, "CHANGELOG.md")))
        self.assertIn("round-1", sh(self.repo, "tag", "--list"))
        self.assertEqual(self.rel("9.9.9", "--resume", "--no-check", check=False).returncode, 0, "finished: nothing to do")

    def test_a_changed_ui_needs_its_version_and_gets_it(self):
        put(self.repo, "mods/foreman-ui/hooks/a.tsx", "b\n")
        sh(self.repo, "commit", "-qam", "ui change")
        r = self.rel("9.9.9", "--no-check", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--ui", r.stderr + r.stdout)
        self.rel("9.9.9", "--resume", "--ui", "0.2.0", "--no-check")
        mk = read_json(os.path.join(self.repo, ".claude-plugin/marketplace.json"))
        self.assertEqual(mk["plugins"][1]["version"], "0.2.0")
        self.assertEqual(read_json(os.path.join(self.repo, "mods/foreman-ui/.claude-plugin/plugin.json"))["version"], "0.2.0")

    def test_push_without_the_publish_grant_refuses_before_any_change(self):
        r = self.rel("9.9.9", "--push", "--no-check", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("publish", r.stderr + r.stdout)
        self.assertEqual(sh(self.repo, "status", "--porcelain"), "")
        self.assertEqual(sh(self.repo, "log", "-1", "--format=%s").strip(), "Foreman 1.0.0")

    def test_push_with_the_grant_merges_into_origin_main_and_spends_it(self):
        origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin], check=True)
        sh(self.repo, "remote", "add", "origin", origin)
        sh(self.repo, "push", "-q", "origin", "main")
        sh(self.repo, "checkout", "-q", "-b", "work")
        tid = self.tid()
        self.fm("focus", tid)
        p = c.find_project(self.repo)
        b = c.find_brief(p, tid)
        b.meta["allow"] = ["publish"]
        c.save_brief(p, b)
        self.rel("9.9.9", "--push", "--no-check")
        self.assertEqual(sh(origin, "log", "-1", "--format=%s", "main").strip(), "Foreman 9.9.9")
        self.assertEqual(sh(origin, "log", "-1", "--format=%p", "main").count(" "), 1, "a --no-ff merge")
        self.assertNotIn("publish", c.find_brief(p, tid).meta.get("allow") or [])
        self.assertEqual(sh(self.repo, "branch", "--show-current").strip(), "work")

    def test_outside_foremans_own_repo_it_refuses(self):
        os.remove(os.path.join(self.repo, "release.py"))
        self.assertIn("release.py", self.rel("9.9.9", "--dry-run", check=False).stderr)
