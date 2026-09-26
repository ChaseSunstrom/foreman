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

    def test_cli(self):
        p = self.fm("docs", "--json", cwd=self.repo)
        self.assertEqual(len(json.loads(p.stdout)["findings"]), 5)
        self.assertEqual(self.fm("docs", "--strict", cwd=self.repo, check=False).returncode, 1)
        for rel in ("README.md", "docs/guide.md"):
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write("Nothing to check.\n")
        self.assertEqual(self.fm("docs", "--strict", cwd=self.repo).returncode, 0)
