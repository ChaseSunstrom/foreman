"""fm doctor: each check passes on good fixtures and fails on bad ones; the command runs end to end."""
import json
import os
import subprocess
import tempfile
import unittest

from helpers import PLUGIN, ForemanTestCase, git_repo

import fmcore as c
import fmdoctor as d
import fmsetup


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

    def test_mod_release(self):
        # T-0191: every other session draws the installed foreman-ui; it lagged this repo (0.4.0 vs 0.5.0) unnoticed
        repo = os.path.join(self.t, "fhome")
        self.write("fhome/mods/foreman-ui/.claude-plugin/plugin.json", json.dumps({"name": "foreman-ui", "version": "0.5.0"}))
        self.write("fhome/mods/foreman-ui/hooks/register.tsx", "new panels\n")
        inst = os.path.join(self.t, "cache", "foreman-ui", "0.4.0")
        self.write("cache/foreman-ui/0.4.0/hooks/register.tsx", "old rows\n")
        listing = self.write("home/.claude/plugins/installed_plugins.json", json.dumps(
            {"plugins": {"foreman-ui@foreman": [{"installPath": inst, "version": "0.4.0"}]}}))
        r = d.check_mod_release(repo, listing)
        self.assertEqual(r.status, "WARN")
        self.assertIn("0.4.0", r.detail)
        self.assertIn("0.5.0", r.detail)
        self.write("cache/foreman-ui/0.4.0/hooks/register.tsx", "new panels\n")  # released: the same code
        self.assertEqual(d.check_mod_release(repo, listing).status, "PASS")
        self.assertEqual(d.check_mod_release(repo, os.path.join(self.t, "none.json")).status, "PASS")  # not installed

    def test_a_busy_machine_skips_hook_timing(self):
        # T-0367: at load 35 JARVIS spent 21 s on 136 timed hook runs, and slow numbers there say nothing of the hooks
        bench = {"Stop": {"p95": 900, "budget": 150, "ok": False, "exit_codes": [0]}}
        r = d.check_hook_latency(bench, busy="load 35.1 on 16 cores")
        self.assertEqual((r.status, "not measured" in r.detail), ("WARN", True))
        self.assertEqual(d.check_hook_latency(bench).status, "FAIL")
        self.assertEqual(d.bench_runs("load 35.1 on 16 cores"), 1)
        self.assertEqual(d.bench_runs(None), 5)

    def test_python_below_the_floor_fails(self):
        for v, want in [((3, 12, 3), "FAIL"), ((3, 13, 0), "FAIL"), ((3, 12, 7), "PASS"), ((3, 14, 7), "PASS")]:
            self.assertEqual(d.check_python(v).status, want, v)
        self.assertIn("3.12.7", d.check_python((3, 10, 12)).detail)
        # T-0368: below the floor, Foreman runs under a supported interpreter it found, and says which
        r = d.check_python((3, 11, 2), refresh=lambda: "/u/.local/bin/python3.12")
        self.assertEqual((r.status, "/u/.local/bin/python3.12" in r.detail), ("WARN", True))
        r = d.check_python((3, 12, 14), child=True)
        self.assertEqual((r.status, "runs under" in r.detail), ("WARN", True))

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

    def test_self_docs_match_the_code(self):
        self.assertEqual(d.check_self_docs().status, "PASS", d.check_self_docs().detail)

    def test_self_docs_flags_drift(self):
        home = os.path.join(self.t, "fh")
        self.write("fh/MASTER.md", "CLI: `fm state|queue`\nSkills: intake. Prose that says doctor and docs doesn't count.\n")
        self.write("fh/README.md", "Flags: `--no-plugins`, `--frobnicate`.\n")
        self.write("fh/install.sh", "#!/bin/bash\n#   --no-plugins     skip\n#   --no-wiring      skip wiring\nset -e\n")
        self.write("fh/plugin/rules/foreman.md", "Run `fm teleport now` then `fm task set T-1 x=y`.\n")
        self.write("fh/plugin/skills/intake/SKILL.md", "---\nname: intake\ndescription: x\n---\n")
        self.write("fh/plugin/skills/extra/SKILL.md", "---\nname: extra\ndescription: x\n---\n")
        r = d.check_self_docs(home, os.path.join(home, "plugin"))
        self.assertEqual(r.status, "FAIL")
        for needle in ("fm teleport", "MASTER.md lacks fm agents, ask", "doctor", "extra", "--frobnicate", "--no-wiring"):
            self.assertIn(needle, r.detail)

    def test_state_location(self):
        home = os.path.join(self.t, "fh")
        self.assertEqual(d.check_state_dir(home, os.path.join(home, "state")).status, "PASS")
        r = d.check_state_dir(home, os.path.join(self.t, "xdg", "foreman"))
        self.assertEqual(r.status, "WARN")
        self.assertIn("fallback", r.detail)
        self.assertIn("fm doctor --restore-state", r.detail)

    def test_hooks_json_registers_every_handler(self):
        self.assertEqual(d.check_hook_events().status, "PASS")
        self.assertEqual(d.check_hook_events(registered={"PreToolUse", "Stop"}).status, "FAIL")
        self.assertIn("PermissionRequest", d.check_hook_events(registered={"PreToolUse", "Stop"}).detail)

    def test_serve_units(self):
        self.assertEqual(d.check_serve({}).status, "PASS")
        self.assertEqual(d.check_serve({"app-1": "active"}).status, "PASS")
        r = d.check_serve({"app-1": "active", "api-2": "failed"})
        self.assertEqual(r.status, "WARN")
        self.assertIn("api-2 failed", r.detail)
        self.assertIn("fm serve status", r.detail)

    def test_env(self):
        both = dict(fmsetup.ENV)
        self.assertEqual(d.check_env({"env": both}, {}).status, "PASS")
        self.assertEqual(d.check_env({"env": dict(both, CLAUDE_AUTOCOMPACT_PCT_OVERRIDE="50")}, {}).status, "PASS",
                         "the user's own value counts")
        self.assertEqual(d.check_env({}, None).status, "PASS", "not wired (--no-wiring): nothing expected")
        r = d.check_env({"env": {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "60"}}, {})
        self.assertEqual(r.status, "WARN")
        self.assertIn("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE", r.detail)
        self.assertIn("fm install-user", r.detail)

    def test_empty_tool_list_is_not_read_only(self):
        # Claude Code treats an empty or omitted tools list as "every tool" (sub-agents docs).
        for tools in ("[]", ""):
            with self.subTest(tools=tools):
                self.write("empty/agents/a.md", f"---\nname: a\ndescription: agent\ntools: {tools}\n---\n400 words\n")
                r = d.check_frontmatter(os.path.join(self.t, "empty"))
                self.assertEqual(r.status, "FAIL")
                self.assertIn("every tool", r.detail)

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

    def test_running_code(self):
        # T-0391: a JARVIS session ran 1.2.3 from its Folder marketplace clone while 1.2.4 was synced into cache
        # folders it never loads; the root and version each session ran must be visible, and a mismatch flagged
        for root, ver in (("old", "1.2.3"), ("new", "1.2.4")):
            self.write(f"{root}/.claude-plugin/plugin.json", json.dumps({"name": "foreman", "version": ver}))
        installed = self.write("installed_plugins.json", json.dumps({"version": 2, "plugins": {"foreman@foreman": [
            {"installPath": os.path.join(self.t, "new"), "version": "1.2.4"}]}}))
        ledger = os.path.join(self.t, "ledger.jsonl")
        with open(ledger, "w") as f:
            for root in ("new", "old"):  # the newest session_start counts
                f.write(json.dumps({"event": "session_start", "data": {"root": os.path.join(self.t, root)}}) + "\n")
        r = d.check_running_code(ledger, installed, plugin=os.path.join(self.t, "new"))  # not this repo's own version
        self.assertEqual(r.status, "WARN")
        self.assertIn("1.2.3", r.detail)
        self.assertIn(os.path.join(self.t, "old"), r.detail)
        with open(ledger, "a") as f:
            f.write(json.dumps({"event": "session_start", "data": {"root": os.path.join(self.t, "new")}}) + "\n")
        self.assertEqual(d.check_running_code(ledger, installed, plugin=os.path.join(self.t, "new")).status, "PASS")
        self.assertEqual(d.check_running_code(os.path.join(self.t, "none.jsonl"), installed, plugin=os.path.join(self.t, "new")).status, "PASS")
        stale = self.write("stale.json", json.dumps({"plugins": {"foreman@foreman": [
            {"installPath": os.path.join(self.t, "old")}]}}))  # a dev checkout newer than the install record
        self.assertEqual(d.check_running_code(ledger, stale, plugin=os.path.join(self.t, "old")).status, "PASS")

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
        self.write("r/config.py", "API_KEY = 'sk-ant-api03-abcdefghijklmnopqrstu'\n")  # pragma: allowlist secret
        subprocess.run(["git", "-C", repo, "add", "config.py"], check=True)
        r = d.check_git_hygiene(repo)
        self.assertEqual(r.status, "FAIL")
        self.assertIn("config.py", r.detail)
        subprocess.run(["git", "-C", repo, "rm", "-q", "--cached", "config.py"], check=True)
        self.write("r/notes.txt", "".join(f"line {i}\n" for i in range(40)))
        subprocess.run(["git", "-C", repo, "add", "notes.txt"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "notes"], check=True)
        subprocess.run(["git", "-C", repo, "mv", "notes.txt", "moved.txt"], check=True)
        with open(os.path.join(repo, "moved.txt"), "a") as f:  # T-0382: a rename that also adds a secret
            f.write("API_KEY = 'sk-ant-api03-abcdefghijklmnopqrstu'\n")  # pragma: allowlist secret
        subprocess.run(["git", "-C", repo, "add", "moved.txt"], check=True)
        self.assertIn("moved.txt", d.check_git_hygiene(repo).detail)

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


class RestoreState(ForemanTestCase):
    def test_restore_state_moves_a_fallback_back_once_the_default_is_writable(self):
        self.fm("init")
        default = os.path.join(self.home, "state")
        os.chmod(self.home, 0o500)
        os.chmod(default, 0o500)
        try:
            self.assertNotEqual(c.state_dir(), default)
            p = self.fm("doctor", "--restore-state", check=False)
            self.assertEqual(p.returncode, 1)
            self.assertIn("still isn't writable", p.stderr)
        finally:
            os.chmod(self.home, 0o700)
            os.chmod(default, 0o700)
        self.assertIn(default, self.fm("doctor", "--restore-state").stdout)
        self.assertEqual(c.state_dir(), default)


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


class HookErrors(ForemanTestCase):
    def test_the_latest_error_is_named(self):
        # round 5 (brainstorm, reliability): "2 hook errors" alone sends the user digging through the log
        log = os.path.join(self.home, "state", "logs", "hooks.log")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w") as f:
            f.write(f"{c.now()} Stop Traceback (most recent call last):\n  File \"x\", line 1\nKeyError: 'drive'\n"
                    f"{c.now()} PreToolUse Traceback (most recent call last):\n  File \"y\", line 2\n"
                    "NameError: name '_new_context_file' is not defined\n")
        r = d.check_hook_errors()
        self.assertEqual(r.status, "WARN")
        self.assertIn("2 hook error(s)", r.detail)
        self.assertIn("PreToolUse NameError: name '_new_context_file' is not defined", r.detail)
        with open(log, "a") as f:
            f.write(f"{c.now()} Stop\x1b]0;x\x07 ValueError: bad \x1b[2Jtitle\n")
        self.assertNotIn("\x1b", d.check_hook_errors().detail)


class CoreIntegrity(unittest.TestCase):
    """Round 7: protected core that differs from the last commit is named (a tamper and half-edit check)."""

    def test_uncommitted_core_changes_are_named(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(d.check_core_integrity(t).status, "PASS", "not a git checkout: nothing to compare")
            repo = git_repo(t, "fh")
            os.makedirs(os.path.join(repo, "plugin", "lib"))
            path = os.path.join(repo, "plugin", "lib", "fmx.py")
            with open(path, "w") as f:
                f.write("x = 1\n")
            subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
            subprocess.run(["git", "-C", repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"],
                           check=True)
            self.assertEqual(d.check_core_integrity(repo).status, "PASS")
            with open(path, "w") as f:
                f.write("x = 2\n")
            r = d.check_core_integrity(repo)
            self.assertEqual(r.status, "WARN")
            self.assertIn("plugin/lib/fmx.py", r.detail)
            wt = os.path.join(t, "wt")  # a worktree's .git is a file, and it is still a checkout
            subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "--detach", wt], check=True)
            with open(os.path.join(wt, "plugin", "lib", "fmx.py"), "w") as f:
                f.write("x = 3\n")
            self.assertEqual(d.check_core_integrity(wt).status, "WARN")

    def test_description_budget(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "skills", "big"))
            with open(os.path.join(t, "skills", "big", "SKILL.md"), "w") as f:
                f.write("---\nname: big\ndescription: " + "x" * 7000 + "\n---\n")
            r = d.check_footprint(os.path.join(t, "none.md"), os.path.join(t, "none.md"), plugin=t)
            self.assertEqual(r.status, "FAIL")
            self.assertIn("descriptions", r.detail)
            dense = os.path.join(t, "dense.md")  # few lines, many tokens: the line budget alone misses it
            with open(dense, "w") as f:
                f.write(("x" * 300 + "\n") * 40)
            r = d.check_footprint(dense, os.path.join(t, "none.md"), plugin=os.path.join(t, "none"))
            self.assertEqual(r.status, "FAIL")
            self.assertIn("chars", r.detail)
        self.assertEqual(d.check_footprint(os.path.join(PLUGIN, "rules", "foreman.md"),
                                           os.path.join(PLUGIN, "none.md")).status, "PASS")
