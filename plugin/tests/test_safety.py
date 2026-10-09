"""T-0672: the guard-and-safety milestone — six first slices that only add checks or logging."""
import json
import os
import random
import re
import subprocess

from helpers import ForemanTestCase

import fmcore as c
import fmdoctor
import fmguard as g
import fmhooks


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True, check=True).stdout

    def finished_task(self, files, scope=None):
        """A small task that writes `files` (path -> text) and is closed with fm task finish; its output."""
        args = ["task", "new", "Add config", "--type", "FEATURE", "--tier", "S", "--ac", "config exists :: true",
                "--step", "write it", "--focus"] + sum((["--scope", s] for s in scope or []), [])
        tid = re.search(r"T-\d+", self.fm(*args).stdout).group(0)
        for path, text in files.items():
            full = os.path.join(self.repo, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as f:
                f.write(text)
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        return self.fm("task", "finish", tid, "--audit", "self: test", "--docs", "none: test", "--lesson", "none: test",
                       check=False)


class SecretsGate(Base):
    def test_a_secret_in_the_task_diff_is_flagged_at_finish(self):
        out = self.finished_task({"conf/app.env": "AWS_ACCESS_KEY_ID=AKIAQ3EGRTWBZ7XKP2MN\n"})
        self.assertIn("secret", (out.stdout + out.stderr).lower())
        self.assertIn("conf/app.env", out.stdout + out.stderr)
        self.assertNotIn("AKIAQ3EGRTWBZ7XKP2MN", out.stdout + out.stderr, "never the value itself")  # pragma: allowlist secret

    def test_a_placeholder_is_not(self):
        out = self.finished_task({"conf/example.env": "AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX  # example\n"})
        self.assertNotIn("secret", (out.stdout + out.stderr).lower())


class CleanupGate(Base):
    def test_ignored_leftovers_outside_the_scope_are_listed_not_blocked(self):
        # untracked files outside the scope are refused already (scope drift); what slips past is ignored output
        with open(os.path.join(self.repo, ".gitignore"), "w") as f:
            f.write("tmp/\n")
        self.git("add", ".gitignore")
        self.git("commit", "-qm", "ignore tmp")
        out = self.finished_task({"src/app.py": "x = 1\n", "tmp/scratch.log": "debug\n"}, scope=["src/**"])
        text = out.stdout + out.stderr
        self.assertEqual(out.returncode, 0, text)
        self.assertIn("left behind", text)
        self.assertIn("tmp/", text.split("left behind", 1)[1])
        self.assertNotIn("src/app.py", text.split("left behind", 1)[1].split("\n")[0])


class UndoPoint(Base):
    def test_an_undo_point_names_head_and_a_stash_of_uncommitted_work(self):
        with open(os.path.join(self.repo, "wip.txt"), "w") as f:
            f.write("uncommitted\n")
        self.git("add", "wip.txt")
        status = self.git("status", "--porcelain")
        point = fmhooks.undo_point(self.repo, "T-0001")
        self.assertEqual(point["head"], self.git("rev-parse", "HEAD").strip())
        self.assertTrue(point.get("stash"), "staged work is captured in a stash commit")
        self.assertEqual(self.git("stash", "list").strip(), "", "stash create never touches the stash list")
        self.assertEqual(self.git("status", "--porcelain"), status, "nor the working tree or index")
        self.assertEqual(self.git("rev-parse", point["ref"]).strip(), point["stash"], "pinned so gc keeps it")

    def test_the_ask_text_says_what_can_be_undone(self):
        self.assertIn("irreversible", fmhooks.restorable("rm-outside"))
        self.assertIn("partly restorable", fmhooks.restorable("git-destructive"))
        self.assertIn("force push", fmhooks.restorable("git-destructive"), "it says what it can't bring back")


class SupplyChainHash(Base):
    def setUp(self):
        super().setUp()
        self.claude = os.path.join(self.tmp, "claude")
        self.plugin = os.path.join(self.claude, "plugins", "cache", "m", "p", "1.0")
        os.makedirs(os.path.join(self.plugin, "hooks"))
        with open(os.path.join(self.plugin, "hooks", "hooks.json"), "w") as f:
            f.write('{"hooks": {}}')
        with open(os.path.join(self.claude, "plugins", "installed_plugins.json"), "w") as f:
            json.dump({"plugins": {"p@m": [{"installPath": self.plugin, "version": "1.0"}]}}, f)

    def test_first_run_is_a_baseline_and_a_change_warns_until_accepted(self):
        first = fmdoctor.check_supply(self.claude)
        self.assertEqual(first.status, "PASS", first.detail)
        with open(os.path.join(self.plugin, "hooks", "hooks.json"), "w") as f:
            f.write('{"hooks": {"PreToolUse": []}}')
        changed = fmdoctor.check_supply(self.claude)
        self.assertEqual(changed.status, "WARN")
        self.assertIn("p@m", changed.detail)
        fmdoctor.check_supply(self.claude, accept=True)
        self.assertEqual(fmdoctor.check_supply(self.claude).status, "PASS")
        with open(os.path.join(self.plugin, "hooks", "run.sh"), "w") as f:  # code, not just the manifest
            f.write("curl x\n")
        self.assertEqual(fmdoctor.check_supply(self.claude).status, "WARN")

    def test_a_garbled_baseline_or_registry_warns_and_never_rebaselines(self):
        fmdoctor.check_supply(self.claude)
        with open(os.path.join(c.state_dir(), "supply.json"), "w") as f:
            f.write("{not json")
        self.assertEqual(fmdoctor.check_supply(self.claude).status, "WARN")
        self.assertEqual(fmdoctor.check_supply(self.claude).status, "WARN", "still: it didn't re-baseline")
        with open(os.path.join(self.claude, "plugins", "installed_plugins.json"), "w") as f:
            f.write("[1, 2]")
        self.assertIn(fmdoctor.check_supply(self.claude, accept=True).status, ("PASS", "WARN"))


class RenderSanitizer(Base):
    def test_terminal_escapes_never_reach_rendered_titles(self):
        evil = "Fix login \x1b]0;pwned\x07\x1b[2J now"
        tid = json.loads(self.fm("task", "new", evil, "--type", "FIX", "--tier", "S", "--json").stdout)["id"]
        shown = self.fm("task", "show", tid).stdout + self.fm("state").stdout
        self.assertNotIn("\x1b", shown)
        self.assertIn("Fix login", shown)

    def test_approval_phrases_fuzzed(self):
        rnd = random.Random(672)
        words = ["yes", "no", "ok", "not", "don't", "go", "ahead", "approved", "never", "lgtm", "wait", "please"]
        for _ in range(500):
            text = " ".join(rnd.choice(words) for _ in range(rnd.randint(1, 6)))
            fmhooks._YES.search(text)  # must never raise
        self.assertTrue(fmhooks._YES.search("yes, go ahead"))
        self.assertFalse(fmhooks._YES.search("no, not yet"))


class RuleIds(Base):
    def test_a_block_carries_a_stable_rule_id(self):
        ctx = g.Ctx(cwd=self.repo, project_root=self.repo, home=os.path.expanduser("~"), foreman_home=self.home,
                    scratch=[], allow=set(), task_id="T-1")
        a = g.check("Bash", {"command": "rm -rf ~"}, ctx)
        b = g.check("Bash", {"command": "rm -rf /home/other"}, ctx)
        self.assertTrue(a.rule.startswith("rm-outside:"), a.rule)
        self.assertEqual(a.rule, b.rule, "the same check fires the same rule whatever the path")

    def test_guard_block_events_carry_it_and_friction_counts_it(self):
        self.fm("task", "new", "x", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        for _ in range(2):
            self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "rm -rf ~"}})
        events = [json.loads(line) for line in open(os.path.join(c.find_project(self.repo).dir, "ledger.jsonl"))]
        blocks = [e for e in events if e.get("event") == "guard_block"]
        self.assertTrue(blocks)
        self.assertTrue(all((e.get("data") or {}).get("rule", "").startswith("rm-outside:") for e in blocks), blocks)
        self.assertIn("rm-outside:recursive-delete-of", self.fm("friction").stdout)
