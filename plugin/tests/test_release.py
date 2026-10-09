"""T-0678: release.py releases Foreman in one command — versions, changelog, gates, commit, push — and can first
re-run each local project's sentinel (a canary)."""
import json
import os
import subprocess
import sys

from helpers import ForemanTestCase, read_text

RELEASE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "release.py")


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, check=True).stdout


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fx = os.path.join(self.tmp, "fx")
        os.makedirs(os.path.join(self.fx, "plugin", ".claude-plugin"))
        os.makedirs(os.path.join(self.fx, ".claude-plugin"))
        self.put("plugin/.claude-plugin/plugin.json", json.dumps({"name": "foreman", "version": "1.0.0"}, indent=2))
        self.put(".claude-plugin/marketplace.json", json.dumps(
            {"name": "foreman", "metadata": {"version": "1.0.0"},
             "plugins": [{"name": "foreman", "version": "1.0.0"}, {"name": "other", "version": "0.6.1"}]}, indent=2))
        self.put("CHANGELOG.md", "# Changelog\n\n## Unreleased\n- a change\n\n## 1.0.0\n- first\n")
        for args in (["init", "-q", "-b", "build"], ["add", "-A"], ["commit", "-qm", "base"]):
            git(self.fx, *args)

    def put(self, rel, text):
        with open(os.path.join(self.fx, rel), "w") as f:
            f.write(text)

    def release(self, *args, check=True):
        p = subprocess.run([sys.executable, RELEASE, *args, "--root", self.fx], capture_output=True, text=True,
                           env=dict(os.environ, FOREMAN_HOME=self.home))
        if check:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return p


class Release(Base):
    def test_one_command_bumps_heads_and_commits(self):
        self.release("1.0.1", "--no-check")
        self.assertEqual(json.loads(read_text(os.path.join(self.fx, "plugin/.claude-plugin/plugin.json")))["version"],
                         "1.0.1")
        market = read_text(os.path.join(self.fx, ".claude-plugin/marketplace.json"))
        self.assertEqual(market.count('"1.0.1"'), 2)
        self.assertIn('"0.6.1"', market, "another plugin's version is left alone")
        log = read_text(os.path.join(self.fx, "CHANGELOG.md"))
        self.assertTrue(log.startswith("# Changelog\n\n## Unreleased\n\n## 1.0.1 — "), log)
        self.assertIn("- a change", log.split("## 1.0.0")[0])
        self.assertEqual(git(self.fx, "log", "-1", "--format=%s").strip(), "Foreman 1.0.1")
        self.assertEqual(git(self.fx, "status", "--porcelain").strip(), "")

    def test_it_refuses_a_dirty_tree_or_an_older_version(self):
        self.put("stray.txt", "x\n")
        self.assertNotEqual(self.release("1.0.1", "--no-check", check=False).returncode, 0)
        os.remove(os.path.join(self.fx, "stray.txt"))
        p = self.release("0.9.0", "--no-check", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("newer", p.stderr)

    def test_push_merges_into_the_remotes_main(self):
        remote = os.path.join(self.tmp, "remote.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", remote], check=True)
        git(self.fx, "push", "-q", remote, "build:main")
        self.release("1.0.1", "--no-check", "--push", remote)
        self.assertIn("Foreman 1.0.1", git(remote, "log", "-3", "--format=%s", "main"))


class Canary(Base):
    def test_canary_runs_each_local_projects_sentinel(self):
        self.fm("init")
        p = self.release("1.0.1", "--no-check", "--canary")
        self.assertIn("canary", p.stdout)
        self.assertIn("sentinel", p.stdout)
