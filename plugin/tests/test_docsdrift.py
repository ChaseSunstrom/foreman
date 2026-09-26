"""fm docs: markdown that drifted from the repo (missing paths, npm/make commands that don't exist)."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmdocs


class DocsDrift(ForemanTestCase):
    def setUp(self):
        super().setUp()
        files = {
            "src/app.py": "x = 1\n",
            "package.json": json.dumps({"scripts": {"test": "jest"}}),
            "Makefile": "test:\n\tpytest\n",
            ".gitignore": "local/\nnode_modules/\n",
            "README.md": "Run `src/app.py` or `src/gone.py`; build with `npm run build`, test with `npm run test`.\n"
                         "```\nsrc/in-a-code-block.py\n```\n`local/notes.md` is machine-specific.\n",
            "docs/guide.md": "See `../README.md`, `docs/setup.md`, `./install.md`, `STATE.md`, `org/repo`, "
                             "`foreman/build` and `make deploy`.\n",
            "node_modules/pkg/README.md": "`missing/everywhere.js`\n",
        }
        for rel, text in files.items():
            path = os.path.join(self.repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(text)

    def kinds(self, findings):
        return sorted((f["file"], f["kind"], f["detail"]) for f in findings)

    def test_scan_reports_drift_only(self):
        found = self.kinds(fmdocs.scan(self.repo))
        self.assertEqual(found, [
            ("README.md", "command", "npm run build"),
            ("README.md", "path", "src/gone.py"),
            ("docs/guide.md", "command", "make deploy"),
            ("docs/guide.md", "path", "./install.md"),
            ("docs/guide.md", "path", "docs/setup.md"),
        ])  # bare names, other repos and branch names aren't repo paths: never reported

    def test_a_folder_holding_only_ignored_files_is_not_a_repo_path(self):
        # Claude Code drops .claude/scheduled_tasks.lock (ignored) into repos; `.claude/…` in docs means the user's
        os.makedirs(os.path.join(self.repo, ".claude"))
        open(os.path.join(self.repo, ".claude", "scheduled_tasks.lock"), "w").close()
        with open(os.path.join(self.repo, ".git", "info", "exclude"), "a") as f:
            f.write("**/.claude/scheduled_tasks.lock\n")
        with open(os.path.join(self.repo, "SETUP.md"), "w") as f:
            f.write("Put overrides in `.claude/settings.local.json`; the app is `src/app.py`, not `src/old.py`.\n")
        found = [f["detail"] for f in fmdocs.scan(self.repo) if f["file"] == "SETUP.md"]
        self.assertEqual(found, ["src/old.py"])

    def test_cli(self):
        p = self.fm("docs", "--json", cwd=self.repo)
        self.assertEqual(len(json.loads(p.stdout)["findings"]), 5)
        self.assertEqual(self.fm("docs", "--strict", cwd=self.repo, check=False).returncode, 1)
        for rel in ("README.md", "docs/guide.md"):
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write("Nothing to check.\n")
        self.assertEqual(self.fm("docs", "--strict", cwd=self.repo).returncode, 0)
