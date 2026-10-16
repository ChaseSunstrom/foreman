"""T-0963: postures and rivals: fm posture lite, compact-output shadow mode, verify commands that read Foreman's
state, a bare-Claude bench arm and hollow subagent returns."""
import json
import os
import shlex
import subprocess
import sys

from helpers import ForemanTestCase, read_json
import test_bench_family as tbf

import fmcore as c
import fmhooks


class BoardPosture(ForemanTestCase):
    def test_posture_lite_skips_every_hook_but_the_guard(self):
        self.fm("init")
        start = lambda: self.hook("SessionStart", {"source": "startup"}).stdout.strip()
        write = lambda: self.hook("PreToolUse", {"tool_name": "Write", "tool_input": {
            "file_path": os.path.join(self.repo, "app.py"), "content": "x"}})
        self.assertTrue(start(), "full: SessionStart injects the project's state")
        self.fm("posture", "lite")
        self.assertIn("lite", self.fm("posture").stdout)
        self.assertEqual(start(), "", "lite: no injection")
        self.assertEqual(write().returncode, 2, "lite: the guard still refuses an unbriefed edit")
        self.fm("posture", "full")
        self.assertTrue(start(), "full again: the hooks are back")

    def test_lite_keeps_the_unbreakable_gates_and_only_the_user_turns_it_on(self):
        # T-0963 security review: lite must not switch off what refuses unevidenced work, and an agent may not
        # lower the posture itself (like fm pause off, it's the user's to type)
        import fmguard
        self.fm("init")
        self.fm("task", "new", "x", "--type", "FIX", "--tier", "S", "--ac", "a :: true", "--step", "s", "--focus")
        self.fm("posture", "lite")
        done = self.hook("TaskCompleted", {"task_subject": "T-0001 step 1", "cwd": self.repo})
        self.assertEqual(done.returncode, 2, "lite: TaskCompleted still refuses a step with no evidence")
        ctx = fmguard.Ctx(cwd=self.repo, project_root=self.repo, home=self.tmp, foreman_home=self.home,
                          state_dir=c.state_dir(), state_fallbacks=[])
        cats = lambda cmd: [cat for cat, _ in fmguard.check_bash(cmd, ctx)]  # noqa: E731
        for cmd in ("fm posture lite", "fm posture --json lite", "fm posture -p x lite", "fm pause -p x off",
                    "fm pause --json off"):
            self.assertIn("self-authorize", cats(cmd), cmd)  # review: a flag before the word slipped past
        self.assertNotIn("self-authorize", cats("fm posture full"))
        self.assertNotIn("self-authorize", cats("fm posture"))
        # review: an fm ask still grants in a lite project (the dialog's PermissionRequest and the grant's PostToolUse)
        self.assertIn("PermissionRequest", fmhooks.LITE_KEEPS)
        self.assertIn("PostToolUse", fmhooks.LITE_KEEPS)

    def test_lint_flags_foreman_state_not_a_repos_own_state_folder(self):
        self.assertTrue(c.lint_verify("cat ~/.claude/foreman/state/projects/x/tasks/T-1.md", self.repo))
        self.assertTrue(c.lint_verify("grep done .foreman/tasks/T-0001.md", self.repo))
        self.assertFalse(c.lint_verify("python3 -m pytest tests/state/tasks", self.repo), "a repo's own state/tasks folder")

    def test_compact_output_shadow_records_savings_and_never_rewrites(self):
        home = os.path.join(self.tmp, "userhome")
        os.makedirs(os.path.join(home, ".claude"))
        env = {"HOME": home}
        self.fm("compact-output", "shadow", env=env)
        settings = read_json(os.path.join(home, ".claude", "settings.json"))
        [cmd] = [h["command"] for g in settings["hooks"]["PostToolUse"] for h in g["hooks"]]
        text = "\n".join(f"test_{i} ... ok" for i in range(2000))
        payload = {"session_id": "s1", "tool_name": "Bash", "hook_event_name": "PostToolUse",
                   "tool_input": {"command": "PYTHONPATH=. pytest -q"},
                   "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False}}
        argv = shlex.split(cmd)
        p = subprocess.run([sys.executable, *argv], input=json.dumps(payload), capture_output=True, text=True,
                           env=dict(os.environ, FOREMAN_HOME=self.home), timeout=30)
        self.assertEqual((p.returncode, p.stdout), (0, ""), "shadow never rewrites the output")
        outputs = os.path.join(self.home, "state", "outputs")
        with open(os.path.join(outputs, "shadow.jsonl")) as f:
            [rec] = [json.loads(x) for x in f]
        self.assertEqual(rec["cmd_family"], "pytest")
        self.assertGreater(rec["saved_chars"], 10000)
        self.assertFalse(os.path.exists(os.path.join(outputs, "s1")), "no full-text file: nothing points at it")
        status = self.fm("compact-output", env=env).stdout
        self.assertIn("shadow", status)
        self.assertIn("would have cut", status)
        self.fm("compact-output", "on", env=env)  # one mode at a time
        settings = read_json(os.path.join(home, ".claude", "settings.json"))
        self.assertEqual(len([h for g in settings["hooks"]["PostToolUse"] for h in g["hooks"]]), 1)
        self.fm("compact-output", "off", env=env)
        self.assertNotIn("hooks", read_json(os.path.join(home, ".claude", "settings.json")))

    def test_lint_verify_flags_a_check_that_reads_foremans_state(self):
        for cmd in ("grep -q done .foreman/tasks/T-0001.md",
                    "test -f ~/.claude/foreman/state/projects/app-1/tasks/T-0001.md",
                    "cat state/briefs/T-0001.md"):
            self.assertTrue(any("Foreman's state" in x for x in c.lint_verify(cmd, self.repo)), cmd)
        self.assertEqual(c.lint_verify("python3 -c 'import os'", self.repo), [])

    def test_a_hollow_builder_return_is_logged_and_fm_next_names_it(self):
        self.fm("init")
        p = c.find_project(self.repo)
        stop = lambda agent, msg: self.hook("SubagentStop", {"agent_type": agent, "agent_id": "a1",
                                                              "last_assistant_message": msg})
        stop("foreman:fm-builder", "x" * 200)
        stop("Explore", "ok")
        self.assertFalse([e for e in c.ledger_tail(p) if e.get("event") == "hollow_return"])
        self.assertNotIn("hollow", self.fm("next").stdout)
        stop("foreman:fm-reviewer", "Done.")
        [e] = [e for e in c.ledger_tail(p) if e.get("event") == "hollow_return"]
        self.assertEqual(e["data"]["agent_type"], "foreman:fm-reviewer")
        self.assertIn("fm-reviewer", self.fm("next").stdout)


class BoardPostureBench(tbf._Bench):
    def test_duel_vs_none_adds_an_arm_with_no_plugins(self):
        self.fm("bench", "build", env=self.env)
        res = json.loads(self.fm("bench", "duel", "--vs", "none", "--json", env=self.env).stdout)
        args = [s["args"] for s in self.calls() if s["args"][:1] == ["-p"] and s["args"][1].startswith("Task:")]
        dirs = [[a[i + 1] for i, x in enumerate(a) if x == "--plugin-dir"] for a in args]
        self.assertEqual(dirs, [[c.PLUGIN_ROOT], []], "Foreman's arm, then a bare one")
        bare = args[1]
        hooks = json.loads(bare[bare.index("--settings") + 1])["hooks"]["PreToolUse"]
        self.assertIn("hooks/hook", hooks[0]["hooks"][0]["command"], "the bare arm keeps the guard (bypass mode)")
        self.assertIn("none", res["with"])
        self.assertIn("verdict", res)
