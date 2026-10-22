"""fm doctor: each check passes on good fixtures and fails on bad ones; the command runs end to end."""
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
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

    def test_claude_code_features(self):
        # T-0785: a feature the installed Claude Code is too old for silently does nothing; only used features count
        self.write("pl/agents/a.md", "---\nname: a\nomitClaudeMd: true\n---\n")
        self.write("pl/hooks/hooks.json", '{"hooks": {"Stop": [{"hooks": [{"onFailure": "block"}]}]}}')
        pl = os.path.join(self.t, "pl")
        r = d.check_cc_features((2, 1, 100), pl)
        self.assertEqual(r.status, "WARN")
        self.assertIn("omitClaudeMd", r.detail)
        self.assertIn("onFailure", r.detail)
        self.assertNotIn("monitors", r.detail)
        self.assertNotIn("sessionTitle", r.detail)
        self.assertEqual(d.check_cc_features((2, 1, 299), pl).status, "PASS")
        self.assertEqual(d.check_cc_features((), pl).status, "PASS")  # unknown version: nothing to compare

    def test_upstream_issues(self):
        # T-1076: a recurring error that is a known Claude Code bug is named with the version that fixes it
        url = "https://github.com/anthropics/claude-code/issues/25990"
        issues = [{"id": "zsh-heredoc", "pattern": r"can't create temp file for here document", "issue_url": url,
                   "fixed_in": "2.1.47", "note": "sandboxed zsh heredocs"}]
        text = "(eval):1: can't create temp file for here document: read-only file system"
        before, after = "2026-10-01T00:00:00Z", "2026-10-03T00:00:00Z"
        update = c.parse_ts("2026-10-02T00:00:00Z").timestamp()  # the installed Claude Code arrived
        err = (after, text)
        r = d.check_upstream([err, (after, "other"), err], (2, 1, 40), issues, update)
        self.assertEqual(r.status, "WARN")
        self.assertIn(url, r.detail)
        self.assertIn("seen 2×", r.detail)
        self.assertIn("fixed in 2.1.47", r.detail)
        self.assertIn("claude update", r.detail)
        r = d.check_upstream([err, err], (2, 1, 50), issues, update)
        self.assertEqual(r.status, "WARN")
        self.assertIn("recurs", r.detail)
        self.assertNotIn("claude update", r.detail)
        # review: errors from before the update that fixed them don't recur; when the update time is unknown, say so
        self.assertEqual(d.check_upstream([(before, text)] * 3 + [err], (2, 1, 50), issues, update).status, "PASS")
        r = d.check_upstream([(before, text)] * 2, (2, 1, 50), issues, 0)
        self.assertEqual(r.status, "WARN")
        self.assertIn("seen 2× in 7 days (possibly before an update)", r.detail)
        r = d.check_upstream([err, err], (), issues, update)
        self.assertIn("installed version unknown", r.detail)
        self.assertNotIn("claude update", r.detail)
        self.assertEqual(d.check_upstream([err], (2, 1, 40), issues, update).status, "PASS")  # once is not a pattern
        self.assertEqual(d.check_upstream([], (2, 1, 40), issues, update).status, "PASS")
        self.assertEqual(d.check_upstream([err, err], (2, 1, 40), [], update).status, "PASS")
        r = d.check_upstream([(after, text.upper()), err], (2, 1, 40), [dict(issues[0], fixed_in=None)], update)
        self.assertEqual(r.status, "WARN")  # case doesn't hide it; an open issue has no fix to name
        self.assertIn("no fix released", r.detail)
        # review: a bad entry is a finding, never a crashed doctor run
        r = d.check_upstream([err, err], (2, 1, 40), [{"id": "broken", "pattern": "("}, "junk"] + issues, update)
        self.assertEqual(r.status, "WARN")
        self.assertIn("broken", r.detail)
        self.assertIn(url, r.detail)

    def test_the_installed_claude_code_arrived_when_its_binary_did(self):
        binary = self.write("versions/2.1.301", "#!/bin/sh\n")
        os.chmod(binary, 0o755)
        os.makedirs(os.path.join(self.t, "bin"))
        os.symlink(binary, os.path.join(self.t, "bin", "claude"))
        self.assertEqual(d._cc_installed_at(os.path.join(self.t, "bin")), os.stat(binary).st_ctime)
        self.assertEqual(d._cc_installed_at(os.path.join(self.t, "none")), 0)  # not found: unknown

    def test_the_shipped_upstream_list_is_well_formed(self):
        issues = json.load(open(os.path.join(PLUGIN, "lib", "upstream-issues.json"), encoding="utf-8"))
        self.assertIsInstance(issues, list)
        ids = [i["id"] for i in issues]
        self.assertEqual(len(ids), len(set(ids)))
        for i in issues:
            self.assertEqual(set(i), {"id", "pattern", "issue_url", "fixed_in", "note"}, i)
            re.compile(i["pattern"])
            self.assertRegex(i["issue_url"], r"^https://github\.com/anthropics/claude-code/issues/\d+$")
            self.assertTrue(i["fixed_in"] is None or re.fullmatch(r"\d+\.\d+\.\d+", i["fixed_in"]), i)

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
        # T-1451: a directory marketplace is read in place (claude plugin list: "Read from" the checkout), so the
        # stale cache record isn't what any session draws
        self.write("cache/foreman-ui/0.4.0/hooks/register.tsx", "old rows\n")
        self.write("home/.claude/plugins/known_marketplaces.json", json.dumps(
            {"foreman": {"source": {"source": "directory", "path": repo + "/"}}}))
        r = d.check_mod_release(repo, listing)
        self.assertEqual(r.status, "PASS", r.detail)
        self.assertIn("in place", r.detail)
        self.write("home/.claude/plugins/known_marketplaces.json", json.dumps(
            {"foreman": {"source": {"source": "github", "repo": "x/foreman"}}}))
        self.assertEqual(d.check_mod_release(repo, listing).status, "WARN")

    def test_a_busy_machine_skips_hook_timing(self):
        # T-0367: at load 35 JARVIS spent 21 s on 136 timed hook runs, and slow numbers there say nothing of the hooks
        bench = {"Stop": {"p95": 900, "budget": 150, "ok": False, "exit_codes": [0]}}
        r = d.check_hook_latency(bench, busy="load 35.1 on 16 cores")
        self.assertEqual((r.status, "not measured" in r.detail), ("WARN", True))
        self.assertEqual(d.check_hook_latency(bench).status, "FAIL")
        self.assertEqual(d.bench_runs("load 35.1 on 16 cores"), 1)
        self.assertEqual(d.bench_runs(None), 5)

    def test_cpu_pressure_counts_as_busy_before_the_load_average_catches_up(self):
        # T-1219: 16 CPU burners left the 1-minute load at 13.8 on 16 cores while the bench ran slow and doctor failed
        from unittest import mock
        psi = os.path.join(self.t, "cpu")
        with open(psi, "w") as f:
            f.write("some avg10=28.72 avg60=14.95 avg300=16.51 total=17932752381\n")
        with mock.patch.object(d, "PSI_CPU", psi), mock.patch.object(d.os, "getloadavg", lambda: (3.0, 3.0, 3.0)):
            self.assertIn("cpu pressure", d.busy() or "")
            with open(psi, "w") as f:
                f.write("some avg10=1.20 avg60=0.90 avg300=0.50 total=1\n")
            self.assertIsNone(d.busy())
        with mock.patch.object(d, "PSI_CPU", os.path.join(self.t, "absent")), \
                mock.patch.object(d.os, "getloadavg", lambda: (40.0, 40.0, 40.0)):
            self.assertIn("load", d.busy() or "")  # no PSI (macOS): the load average still decides

    def test_python_below_the_floor_fails(self):
        for v, want in [((3, 12, 3), "FAIL"), ((3, 13, 0), "FAIL"), ((3, 12, 7), "PASS"), ((3, 14, 7), "PASS")]:
            self.assertEqual(d.check_python(v).status, want, v)
        self.assertIn("3.12.7", d.check_python((3, 10, 12)).detail)
        # T-0368: below the floor, Foreman runs under a supported interpreter it found, and says which
        r = d.check_python((3, 11, 2), refresh=lambda: "/u/.local/bin/python3.12")
        self.assertEqual((r.status, "/u/.local/bin/python3.12" in r.detail), ("WARN", True))
        r = d.check_python((3, 12, 14), child=True)
        self.assertEqual((r.status, "runs under" in r.detail), ("WARN", True))

    def test_fm_link_says_whether_fm_works_in_any_shell(self):
        # T-1324: an install from before T-0853 had no ~/.local/bin/fm, so fm worked only inside Claude Code
        bin_, target = os.path.join(self.t, "bin"), os.path.join(self.t, "plugin-bin-fm")
        os.makedirs(bin_)
        with open(target, "w") as f:
            f.write("#!/bin/sh\n")
        link = os.path.join(bin_, "fm")
        r = d.check_fm_link(link, target, bin_)
        self.assertEqual(r.status, "WARN")
        self.assertIn("fm install-user", r.detail)
        os.symlink(target, link)
        self.assertEqual(d.check_fm_link(link, target, bin_).status, "PASS")
        r = d.check_fm_link(link, target, "/usr/bin")
        self.assertEqual(r.status, "WARN")
        self.assertIn("PATH", r.detail)
        os.unlink(link)
        os.symlink("/elsewhere/fm", link)
        r = d.check_fm_link(link, target, bin_)
        self.assertEqual(r.status, "WARN")
        self.assertIn("/elsewhere/fm", r.detail)

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
        # T-0768: Claude Code ignores a mistyped effort, maxTurns or omitClaudeMd, so the saving silently never happens
        for field in ("effort: lo", "maxTurns: 0", "omitClaudeMd: yes"):
            self.write("plug/agents/a.md", f"---\nname: a\ndescription: agent\ntools: Read\n{field}\n---\nbody\n")
            self.assertIn(field.split(":")[0], d.check_frontmatter(root).detail, field)
        self.write("plug/agents/a.md", "---\nname: a\ndescription: agent\ntools: Read\neffort: low\nmaxTurns: 20\n"
                                       "omitClaudeMd: true\n---\nbody\n")
        self.assertNotIn("a.md", d.check_frontmatter(root).detail)

    def test_a_skill_that_breaks_the_agent_skills_spec_fails(self):
        # T-1396: name 1-64 lowercase letters, digits and single hyphens, equal to its folder; description 1-1024
        root = os.path.join(self.t, "plug")
        self.write("plug/skills/good/SKILL.md", "---\nname: good\ndescription: does one thing well\n---\nbody\n")
        self.assertEqual(d.check_frontmatter(root).status, "PASS")
        for folder, name, desc, why in (("Bad_Name", "Bad_Name", "fine", "breaks the spec"),
                                        ("x", "y", "fine", "doesn't match its folder"),
                                        ("a" * 65, "a" * 65, "fine", "over 64 characters"),
                                        ("long", "long", "d" * 1025, "description over 1,024"),
                                        ("greedy", "greedy", "Use for every task.", "over-broad description")):
            with self.subTest(why):
                self.write(f"plug/skills/{folder}/SKILL.md", f"---\nname: {name}\ndescription: {desc}\n---\nbody\n")
                r = d.check_frontmatter(root)
                self.assertEqual(r.status, "FAIL")
                self.assertIn(why, r.detail)
                shutil.rmtree(os.path.join(root, "skills", folder))

    def test_worktree_base(self):
        # T-0803: builder lanes need worktree.baseRef head; the default makes them start from the remote's branch
        self.assertEqual(d.check_worktree_base({"worktree": {"baseRef": "head"}}).status, "PASS")
        for s in ({}, {"worktree": {"baseRef": "fresh"}}):
            r = d.check_worktree_base(s)
            self.assertEqual(r.status, "WARN")
            self.assertIn("baseRef", r.detail)

    def test_self_docs_match_the_code(self):
        self.assertEqual(d.check_self_docs().status, "PASS", d.check_self_docs().detail)

    def test_self_docs_hold_fm_help_to_every_command_once(self):
        # T-1011: T-0974 added fm approve-reads with no help tier; only the full suite's test_help noticed, after commit
        import fmcli
        from unittest import mock
        fmcli.build_parser()
        tiers = [(t, " ".join(w for w in n.split() if w != "approve-reads") + (" status teleport" if i == 0 else ""))
                 for i, (t, n) in enumerate(fmcli.HELP_TIERS)]
        real, saved = fmcli.build_parser, list(fmcli.HELP_TIERS)  # T-1378: the parser is built once, so put them back

        def broken():
            parser = real()
            fmcli.HELP_TIERS[:] = tiers
            return parser
        try:
            with mock.patch.object(fmcli, "build_parser", broken):
                r = d.check_self_docs()
        finally:
            fmcli.HELP_TIERS[:] = saved
        self.assertEqual(r.status, "FAIL")
        for needle in ("fm help's tiers lack approve-reads", "list status twice", "teleport isn't an fm command"):
            self.assertIn(needle, r.detail)

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
        for needle in ("fm teleport", "MASTER.md lacks fm adopt, agents, approve-reads, ask", "doctor", "extra", "--frobnicate", "--no-wiring"):
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
        self.assertEqual(d.check_backup(home).status, "WARN", "T-0844: a fresh install has none yet; not a failure")
        self.write("fh/backups/claude-20260101-000000.tgz", "x")
        self.assertEqual(d.check_backup(home).status, "FAIL")  # T-0574: an archive that doesn't open isn't a backup
        import tarfile
        with tarfile.open(os.path.join(home, "backups", "claude-20260102-000000.tgz"), "w:gz") as t:
            t.add(os.path.join(home, "backups", "claude-20260101-000000.tgz"), "x")
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
                  "deny rules", "rules symlink", "scripts", "name collisions", "hook state writers", "upstream issues"):
            self.assertIn(n, names)

    def test_plain_output_lists_only_problems_unless_verbose(self):
        # T-0844: a newcomer's first doctor run printed 40 lines of passes around the one line that mattered
        self.fm("init")
        quiet = self.fm("doctor", check=False, env={"HOME": self.tmp}).stdout
        loud = self.fm("doctor", "-v", check=False, env={"HOME": self.tmp}).stdout
        self.assertNotIn("PASS ", quiet)
        self.assertIn("PASS ", loud)
        self.assertIn("fm doctor:", quiet)
        self.assertIn("pass", quiet.splitlines()[-1], "the summary still counts them")

    def test_the_tests_skip_the_hook_bench_and_doctor_says_so(self):
        # T-1379: the bench is ~100 hook runs (13 of doctor's 18 s at load 44, past 30 s at 60), and the tests that run
        # fm doctor for its other checks waited on it inside a 30 s limit; FOREMAN_DOCTOR_BENCH=0 (set for every test)
        self.fm("init")
        rs = {r["name"]: r for r in json.loads(self.fm("doctor", "--json", check=False, env={"HOME": self.tmp}).stdout)
              ["results"]}
        for n in ("hook latency", "hook exit codes", "injection budgets"):
            self.assertEqual(rs[n]["status"], "WARN", rs[n])
            self.assertIn("FOREMAN_DOCTOR_BENCH=0", rs[n]["detail"])


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

    def test_an_error_from_code_changed_since_is_stale(self):
        # T-1139: NameError BATCH_AT came from a half-written edit; the line it names no longer reads that way
        log = os.path.join(self.home, "state", "logs", "hooks.log")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        src = os.path.join(d.PLUGIN, "lib", "fmdoctor.py")
        with open(src) as f:
            first = f.readline().rstrip("\n")
        frame = f"  File \"{src}\", line 1, in <module>\n"
        with open(log, "w") as f:
            f.write(f"{c.now()} PostToolUse Traceback (most recent call last):\n{frame}    if n == BATCH_AT and x:\n"
                    "NameError: name 'BATCH_AT' is not defined\n")
        r = d.check_hook_errors()
        self.assertEqual(r.status, "PASS", r.detail)
        self.assertIn("changed since", r.detail)
        with open(log, "a") as f:  # the same line as the file has now: a live error
            f.write(f"{c.now()} PostToolUse Traceback (most recent call last):\n{frame}    {first.strip()}\n"
                    "ValueError: still broken\n")
        self.assertEqual(d.check_hook_errors().status, "WARN")

    def test_upstream_reads_a_week_of_hook_errors_and_failures(self):
        # T-1076: hooks.log entries and every project's failure signatures of the last 7 days, matched case-blind
        self.fm("init")
        p = c.find_project(self.repo)
        ago = lambda days: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - days * 86400))
        log = os.path.join(self.home, "state", "logs", "hooks.log")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w") as f:
            f.write(f"{ago(10)} SubagentStop failed: classifyHandoffIfNeeded is not defined\n"  # too old
                    f"{ago(3)} SubagentStop Traceback (most recent call last):\n"
                    "ReferenceError: classifyHandoffIfNeeded is not defined\n")
        with open(os.path.join(p.dir, "failures.jsonl"), "a") as f:
            rec = {"sig": "agent failed: classifyhandoffifneeded is not defined", "task": None, "at": c.now()}
            f.write(json.dumps(rec) + "\n" + json.dumps(dict(rec, hinted=True)) + "\n[1]\n")  # neither is a new error
        r = d.check_upstream(version=(2, 1, 40))
        self.assertEqual(r.status, "WARN")
        self.assertIn("issues/22087 (seen 2×)", r.detail)
        self.assertEqual(d.check_upstream(errors=[], version=(2, 1, 40)).status, "PASS")


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


class DoctorStateSize(ForemanTestCase):
    # T-0920: state grows quietly (ledger, research, outputs); past a budget doctor says so and names the fix
    def test_a_project_past_the_budget_warns_with_its_biggest_part_and_fm_tidy(self):
        self.fm("init")
        p = c.find_project(self.repo)
        os.makedirs(os.path.join(p.dir, "research"), exist_ok=True)
        with open(os.path.join(p.dir, "research", "big.md"), "w") as f:
            f.write("x" * 50_000)
        self.assertEqual(d.check_state_size([p], budget=1_000_000).status, "PASS")
        os.makedirs(os.path.join(p.dir, "backups"), exist_ok=True)  # round-7 review: tidy's own backups don't count
        with open(os.path.join(p.dir, "backups", "20260101T000000Z.tar.gz"), "w") as f:
            f.write("x" * 2_000_000)
        self.assertEqual(d.check_state_size([p], budget=1_000_000).status, "PASS")
        r = d.check_state_size([p], budget=20_000)
        self.assertEqual(r.status, "WARN")
        self.assertIn(p.slug, r.detail)
        self.assertIn("research", r.detail)
        self.assertIn("fm tidy", r.detail)


class DoctorDualInstall(ForemanTestCase):
    # T-0923: Foreman from a GitHub marketplace beside install.sh's copy in its home: sessions run either, and drift
    def setUp(self):
        super().setUp()
        self.t = tempfile.mkdtemp(dir=self.tmp)
        self.fmhome = os.path.join(self.t, "foreman")
        for root, v in ((os.path.join(self.fmhome, "plugin"), "1.2.28"), (os.path.join(self.t, "cache", "1.2.20"), "1.2.20")):
            os.makedirs(os.path.join(root, ".claude-plugin"))
            with open(os.path.join(root, ".claude-plugin", "plugin.json"), "w") as f:
                json.dump({"name": "foreman", "version": v}, f)
        self.installed = os.path.join(self.t, "installed.json")
        with open(self.installed, "w") as f:
            json.dump({"plugins": {"foreman@foreman": [{"version": "1.2.20", "installPath": os.path.join(self.t, "cache", "1.2.20")}]}}, f)
        self.known = os.path.join(self.t, "known.json")

    def known_as(self, source):
        with open(self.known, "w") as f:
            json.dump({"foreman": {"source": source}}, f)

    def test_a_github_install_beside_this_home_at_another_version_warns(self):
        self.known_as({"source": "github", "repo": "ChaseSunstrom/foreman"})
        r = d.check_dual_install(self.fmhome, self.known, self.installed)
        self.assertEqual(r.status, "WARN")
        self.assertIn("1.2.20", r.detail)
        self.assertIn("1.2.28", r.detail)

    def test_the_marketplace_being_this_home_is_one_install(self):
        self.known_as({"source": "directory", "path": self.fmhome})
        self.assertEqual(d.check_dual_install(self.fmhome, self.known, self.installed).status, "PASS")
        os.remove(self.installed)
        self.assertEqual(d.check_dual_install(self.fmhome, self.known, self.installed).status, "PASS")


class BoardDoctor(unittest.TestCase):  # T-0954
    def test_invisible_text_in_instruction_files_warns_with_file_and_line(self):
        with tempfile.TemporaryDirectory() as t:
            bad, clean = os.path.join(t, "CLAUDE.md"), os.path.join(t, "rules.md")
            with open(bad, "w", encoding="utf-8") as f:
                f.write("# Rules\nbe nice​\nok ‮evil‬\nhidden \U000E0041 tag\n")
            with open(clean, "w", encoding="utf-8") as f:
                f.write("# Rules\nnothing hidden — even em dashes and émojis 🎉\n")
            r = d.check_invisible_text([bad, clean, os.path.join(t, "missing.md")])
            self.assertEqual(r.status, "WARN")
            for line in (2, 3, 4):
                self.assertIn(f"CLAUDE.md:{line}", r.detail)
            self.assertNotIn("rules.md", r.detail)
            self.assertEqual(d.check_invisible_text([clean]).status, "PASS")
            for hidden in ("joined⁠", "﻿mid-file", "soft­hyphen", "vs︁", "é‍‍é",
                           "a️", "sup\U000e0101"):
                with open(bad, "w", encoding="utf-8") as f:
                    f.write("ok\n" + hidden + "\n")
                self.assertEqual(d.check_invisible_text([bad]).status, "WARN", repr(hidden))
            with open(clean, "w", encoding="utf-8") as f:
                f.write("﻿# BOM first\nfamily 👨‍👩‍👧 and ❤️\n")
            self.assertEqual(d.check_invisible_text([clean]).status, "PASS")

    def test_the_shipped_instruction_files_are_clean(self):
        files = [f for f in d.instruction_files() if f.startswith(PLUGIN)]
        self.assertTrue(any(f.endswith(os.path.join("output-styles", "foreman.md")) for f in files))
        self.assertTrue(any(os.sep + "references" + os.sep in f for f in files))
        self.assertEqual(d.check_invisible_text(files).status, "PASS")

    def test_readme_naming_an_fm_verb_the_parser_lacks_fails(self):
        with tempfile.TemporaryDirectory() as t:
            with open(os.path.join(t, "README.md"), "w") as f:
                f.write("Run `fm nosuchverb` to see.\n\n```bash\n$ fm fencedverb --x\nfm task new \"t\"\n```\n")
            r = d.check_self_docs(t)
            self.assertEqual(r.status, "FAIL")
            self.assertIn("`fm nosuchverb` isn't an fm command", r.detail)
            self.assertIn("`fm fencedverb` isn't an fm command", r.detail)  # usage examples sit in fences
            self.assertNotIn("`fm task", r.detail)
