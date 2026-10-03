"""T-0132: fm secrets finds credentials in the working tree, in git history and in Claude Code's config without printing
them; Foreman's own commits carry a Foreman-Task trailer and refuse lines that look like a secret."""
import json
import os
import subprocess
import unittest

from helpers import ForemanTestCase

# built at run time, so this file holds no secret-shaped literal of its own
AWS = "AKIA" + "Q7ZT4M2XK9" + "PL3VBN"
SLACK = "xoxb-" + "4815162342" + "-abcdefghij"
GITHUB = "ghp_" + "a1B2c3D4" * 5
ANTHROPIC = "sk-ant-" + "api03-" + "x9Y8w7V6" * 3
VENDOR = "v3nd0r" + "Key" + "7781aZ"


class Secrets(ForemanTestCase):
    def write(self, rel, text, root=None):
        path = os.path.join(root or self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        return path

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo, *args], capture_output=True, text=True, check=True).stdout

    def test_tree_history_and_claude_config_are_found_without_printing_a_value(self):
        self.fm("init")
        self.write("settings.py", f'AWS_KEY = "{AWS}"\n')
        self.write("db.py", f'DB_PASSWORD = "{VENDOR}"\n')  # review: a prefixed name is still a secret's name
        self.write(".env", f"API_KEY={VENDOR}\n")  # unquoted, in config
        self.write(".env.example", f"API_KEY={VENDOR}\n")  # a template's value isn't one
        self.write("fixture.py", f'TOKEN = "{GITHUB}"  # pragma: allowlist secret\n')
        self.write("old.txt", f"slack {SLACK}\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "add")
        self.git("rm", "-q", "old.txt")
        self.git("commit", "-qm", "drop the token")
        self.write(".mcp.json", json.dumps({"mcpServers": {"vendor": {"command": "vendor-mcp", "env": {
            "VENDOR_API_KEY": VENDOR, "FROM_ENV": "${VENDOR_TOKEN}"}}}}))
        home = os.path.join(self.tmp, "home")
        os.chmod(self.write(".claude/settings.json", json.dumps({"env": {"ANTHROPIC_API_KEY": ANTHROPIC}}), home), 0o644)
        self.write(".claude/settings.local.json", '{\n  // not JSON\n  "env": {"GH": "%s"}\n}\n' % GITHUB, home)
        env = {"HOME": home}

        p = self.fm("secrets", check=False, env=env)
        out = p.stdout + p.stderr
        self.assertEqual(p.returncode, 1, out)
        self.assertIn("settings.py:1", out)
        self.assertIn("db.py:1", out)
        self.assertIn(".env:1", out)
        self.assertNotIn(".env.example", out)
        self.assertIn("settings.local.json line 3 — GitHub token", out)  # read as text when it isn't JSON
        self.assertIn("VENDOR_API_KEY", out)  # a literal in an MCP server's env, whatever its format
        self.assertNotIn("FROM_ENV", out)  # a ${VAR} reference is how it should be done
        self.assertIn(".claude/settings.json", out)
        self.assertIn("other users", out)  # the settings file holding it is readable by others
        self.assertNotIn("fixture.py", out)  # allowlisted
        self.assertNotIn("old.txt", out)  # history only with --history
        for value in (AWS, VENDOR, ANTHROPIC, SLACK, GITHUB):
            self.assertNotIn(value, out)

        hist = self.fm("secrets", "--history", check=False, env=env).stdout
        self.assertIn("old.txt", hist)
        self.assertIn(self.git("log", "-1", "--format=%h", "HEAD~1").strip(), hist)  # the commit that added it
        self.assertNotIn(SLACK, hist)

        data = json.loads(self.fm("secrets", "--json", check=False, env=env).stdout)
        self.assertTrue(any(f["path"] == "settings.py" and f["line"] == 1 for f in data["findings"]))

    def test_a_clean_repo_passes(self):
        self.fm("init")
        self.write("app.py", "password = input()\n")
        p = self.fm("secrets", check=False, env={"HOME": os.path.join(self.tmp, "nohome")})
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_finish_commit_tags_the_task_logs_it_and_refuses_a_secret(self):
        self.fm("init")
        self.fm("task", "new", "One", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus")
        self.write("a.py", "x = 1\n")
        self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check", "--commit", "Add a")
        self.assertIn("Foreman-Task: T-0001", self.git("log", "-1", "--format=%B"))
        sha = self.git("log", "-1", "--format=%h").strip()
        self.assertIn(f"committed {sha}", self.fm("task", "show", "T-0001").stdout)

        self.git("config", "diff.noprefix", "true")  # review: git's own config mustn't hide a line from the check
        self.git("config", "diff.mnemonicPrefix", "true")
        self.fm("task", "new", "Two", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus")
        self.write(".gitattributes", "b.py -diff\n")  # git would call it binary
        self.write("b.py", f'KEY = "{GITHUB}"\n')
        p = self.fm("task", "finish", "T-0002", "--run", "true", "--audit", "self check", "--commit", "Add b", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("b.py:1", p.stderr)
        self.assertNotIn(GITHUB, p.stdout + p.stderr)
        self.assertEqual(self.git("log", "-1", "--format=%h").strip(), sha, "nothing committed")
        self.assertEqual(self.git("diff", "--cached", "--name-only").strip(), "", "and nothing left staged")

    def test_finish_commit_leaves_out_what_was_staged_before_the_task(self):
        self.fm("init")
        self.write("staged.txt", f"slack {SLACK}\n")
        self.git("add", "staged.txt")
        self.fm("task", "new", "One", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a", "--focus")
        self.write("c.py", "c = 1\n")
        self.fm("task", "finish", "T-0001", "--run", "true", "--audit", "self check", "--commit", "Add c")
        self.assertEqual(self.git("show", "--name-only", "--format=").split(), ["c.py"])
        self.assertEqual(self.git("diff", "--cached", "--name-only").split(), ["staged.txt"], "still staged, not committed")


if __name__ == "__main__":
    unittest.main()
