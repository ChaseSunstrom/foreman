"""Foreman on Codex, Gemini CLI and opencode (T-0324): the hook takes `--agent X EVENT`, reads that agent's payload
and answers in its format, through the same guard and context Claude Code gets; `fm agents install X` wires the hooks,
the MCP server and an instructions block in, idempotently, and `uninstall` leaves the user's own config as it was."""
import json
import os
import shutil
import subprocess
import sys

from helpers import HOOK, ForemanTestCase, read_text


class Hook(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.hook("SessionStart", {})  # the repo becomes a Foreman project with no task: edits need a brief

    def agent_hook(self, agent, event, payload, cwd=None):
        e = dict(os.environ, FOREMAN_HOME=self.home)
        return subprocess.run([sys.executable, HOOK, "--agent", agent, event], input=json.dumps(payload), env=e,
                              capture_output=True, text=True, timeout=15, cwd=cwd or self.repo)

    def focus(self):
        out = self.fm("task", "new", "Export CSV", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                      "--step", "write it", "--focus", "--json").stdout
        return json.JSONDecoder().raw_decode(out)[0]["id"]  # --focus prints a second object

    def test_codex_refuses_rm_home_in_claude_compatible_json(self):
        p = self.agent_hook("codex", "PreToolUse", {"session_id": "c-1", "cwd": self.repo, "tool_name": "Bash",
                                                    "tool_input": {"command": "rm -rf ~"}})
        self.assertEqual(p.returncode, 2, p.stderr)
        out = json.loads(p.stdout)["hookSpecificOutput"]
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertTrue(out["permissionDecisionReason"].strip())

    def test_codex_shell_array_and_apply_patch_are_guarded(self):
        p = self.agent_hook("codex", "PreToolUse", {"session_id": "c-1", "cwd": self.repo, "tool_name": "shell",
                                                    "tool_input": {"command": ["bash", "-lc", "rm -rf ~"]}})
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        patch = "*** Begin Patch\n*** Add File: a.py\n+print(1)\n*** End Patch\n"
        pl = {"session_id": "c-1", "cwd": self.repo, "tool_name": "apply_patch", "tool_input": {"command": patch}}
        self.assertEqual(self.agent_hook("codex", "PreToolUse", pl).returncode, 2)  # no brief: edits are refused
        self.focus()
        p = self.agent_hook("codex", "PreToolUse", pl)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_codex_never_gets_ask_or_claude_only_keys(self):
        self.focus()
        p = self.agent_hook("codex", "SessionStart", {"session_id": "c-2", "cwd": self.repo, "source": "startup"})
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(set(out), {"hookSpecificOutput"})
        self.assertEqual(set(out["hookSpecificOutput"]), {"hookEventName", "additionalContext"})
        self.assertIn("Export CSV", out["hookSpecificOutput"]["additionalContext"])
        self.assertIn("Next:", out["hookSpecificOutput"]["additionalContext"])

    def test_gemini_denies_with_its_decision_and_clean_stdout(self):
        p = self.agent_hook("gemini", "BeforeTool", {"session_id": "g-1", "cwd": self.repo, "hook_event_name":
                                                     "BeforeTool", "tool_name": "run_shell_command",
                                                     "tool_input": {"command": "rm -rf ~"}})
        self.assertEqual(p.returncode, 2)
        self.assertEqual(json.loads(p.stdout)["decision"], "deny")  # stdout is the one JSON object, nothing else
        self.assertTrue(p.stderr.strip())
        w = {"session_id": "g-1", "cwd": self.repo, "tool_name": "write_file",
             "tool_input": {"file_path": os.path.join(self.repo, "a.py"), "content": "x"}}
        self.assertEqual(self.agent_hook("gemini", "BeforeTool", w).returncode, 2)
        self.focus()
        p = self.agent_hook("gemini", "BeforeTool", w)
        self.assertEqual((p.returncode, p.stdout.strip()), (0, ""))

    def test_gemini_session_start_and_prompt_get_context_under_its_event_names(self):
        self.focus()
        p = self.agent_hook("gemini", "SessionStart", {"session_id": "g-2", "cwd": self.repo,
                                                       "transcript_path": "/nonexistent/g.json"})
        out = json.loads(p.stdout)["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "SessionStart")
        self.assertIn("Next:", out["additionalContext"])
        p = self.agent_hook("gemini", "BeforeAgent", {"session_id": "g-2", "cwd": self.repo, "prompt": "go on"})
        self.assertEqual(p.returncode, 0, p.stderr)
        if p.stdout.strip():
            self.assertEqual(json.loads(p.stdout)["hookSpecificOutput"]["hookEventName"], "BeforeAgent")

    def test_opencode_plugin_payload_maps_tools_and_answers_deny_or_context(self):
        p = self.agent_hook("opencode", "PreToolUse", {"session_id": "o-1", "cwd": self.repo, "tool": "bash",
                                                       "args": {"command": "rm -rf ~"}})
        self.assertEqual(p.returncode, 2)
        self.assertIn("deny", json.loads(p.stdout))
        e = {"session_id": "o-1", "cwd": self.repo, "tool": "edit",
             "args": {"filePath": os.path.join(self.repo, "a.py"), "oldString": "", "newString": "x"}}
        self.assertEqual(self.agent_hook("opencode", "PreToolUse", e).returncode, 2)
        self.focus()
        self.assertEqual(self.agent_hook("opencode", "PreToolUse", e).returncode, 0)
        p = self.agent_hook("opencode", "SessionStart", {"session_id": "o-1", "cwd": self.repo})
        self.assertIn("Next:", json.loads(p.stdout)["context"])

    def test_review_fail_closed_on_odd_input_and_unknown_shell_names(self):
        p = self.agent_hook("codex", "PreToolUse", {"cwd": self.repo, "tool_name": "Write",
                                                    "tool_input": {"file_path": ["/etc/x"]}})
        self.assertEqual(p.returncode, 2, p.stderr)  # an adapter crash is a refusal, never Python's exit 1
        self.assertEqual(json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")
        for name in ("shell_command", "terminal"):  # any tool with a command string is judged as a shell command
            p = self.agent_hook("codex", "PreToolUse", {"cwd": self.repo, "tool_name": name,
                                                        "tool_input": {"command": "rm -rf ~"}})
            self.assertEqual(p.returncode, 2, name)

    def test_unknown_agent_fails_closed_on_tool_events_only(self):
        p = self.agent_hook("nope", "PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "ls"}})
        self.assertEqual(p.returncode, 2)
        self.assertEqual(self.agent_hook("nope", "SessionStart", {}).returncode, 0)


class Install(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.h = os.path.join(self.tmp, "home")
        os.makedirs(self.h)
        self.env = {"HOME": self.h, "XDG_CONFIG_HOME": "", "CODEX_HOME": ""}

    def agents(self, *args, check=True):
        return self.fm("agents", *args, env=self.env, check=check)

    def snapshot(self):
        out = {}
        for root, _, names in os.walk(self.h):
            for n in names:
                text = read_text(os.path.join(root, n))  # JSON is compared as data: install re-indents it
                out[os.path.relpath(os.path.join(root, n), self.h)] = json.loads(text) if n.endswith(".json") else text
        return out

    def wired(self):
        return {a["agent"]: a["installed"] for a in json.loads(self.agents("list", "--json").stdout)["agents"]}

    def seed(self):
        """The user's own config, which install must keep and uninstall must give back byte for byte."""
        files = {
            ".codex/hooks.json": json.dumps({"hooks": {"PreToolUse": [{"hooks": [{"type": "command",
                                                                                   "command": "mine.sh"}]}]}}),
            ".codex/config.toml": 'model = "o4"\n\n[mcp_servers.other]\ncommand = "x"\n',
            ".codex/AGENTS.md": "# My rules\nBe brief.\n",
            ".gemini/settings.json": json.dumps({"theme": "dark", "mcpServers": {"other": {"command": "x"}}}),
            ".config/opencode/opencode.json": json.dumps({"$schema": "https://opencode.ai/config.json",
                                                          "model": "x/y"}),
        }
        for rel, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(self.h, rel)), exist_ok=True)
            with open(os.path.join(self.h, rel), "w") as f:
                f.write(text)
        return self.snapshot()

    def test_install_is_idempotent_and_uninstall_restores_the_users_config(self):
        before = self.seed()
        self.assertEqual(self.wired(), {"codex": False, "gemini": False, "opencode": False})
        for a in ("codex", "gemini", "opencode"):
            self.agents("install", a, "--json")
        once = self.snapshot()
        for a in ("codex", "gemini", "opencode"):
            self.agents("install", a)
        self.assertEqual(self.snapshot(), once)
        self.assertEqual(self.wired(), {"codex": True, "gemini": True, "opencode": True})

        hooks = once[".codex/hooks.json"]["hooks"]
        self.assertIn("mine.sh", json.dumps(hooks["PreToolUse"]))
        self.assertTrue(any("--agent codex PreToolUse" in h["command"] for g in hooks["PreToolUse"] for h in g["hooks"]))
        self.assertIn("[mcp_servers.fm]", once[".codex/config.toml"])
        self.assertIn("Be brief.", once[".codex/AGENTS.md"])
        self.assertIn("fm next", once[".codex/AGENTS.md"])
        g = once[".gemini/settings.json"]
        self.assertEqual((g["theme"], g["mcpServers"]["other"]), ("dark", {"command": "x"}))
        self.assertEqual(g["mcpServers"]["fm"]["args"], ["mcp"])
        self.assertTrue(any("--agent gemini BeforeTool" in h["command"] for grp in g["hooks"]["BeforeTool"]
                            for h in grp["hooks"]))
        self.assertIn("fm next", once[".gemini/GEMINI.md"])
        o = once[".config/opencode/opencode.json"]
        self.assertEqual((o["model"], o["mcp"]["fm"]["command"][-1]), ("x/y", "mcp"))
        plugin = once[".config/opencode/plugins/foreman.ts"]
        self.assertIn("--agent", plugin)
        self.assertNotIn("__HOOK__", plugin)

        for a in ("codex", "gemini", "opencode"):
            self.agents("uninstall", a)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.wired(), {"codex": False, "gemini": False, "opencode": False})

    def test_review_never_takes_over_the_users_own_fm_server_or_plugin_file(self):
        mine = {"mcpServers": {"fm": {"command": "my-fm"}}, "note": "caf\u00e9"}
        os.makedirs(os.path.join(self.h, ".gemini"))
        path = os.path.join(self.h, ".gemini", "settings.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(mine, f, ensure_ascii=False)
        p = self.agents("install", "gemini", "--json")
        self.assertTrue(json.loads(p.stdout)["notes"])
        self.assertEqual(read_text(path).count("caf\u00e9"), 1)  # not escaped to \u00e9
        self.assertEqual(json.loads(read_text(path))["mcpServers"]["fm"], {"command": "my-fm"})
        self.agents("uninstall", "gemini")
        self.assertEqual(json.loads(read_text(path)), mine)
        own = os.path.join(self.h, ".config", "opencode", "plugins", "foreman.ts")
        os.makedirs(os.path.dirname(own))
        with open(own, "w") as f:
            f.write("// my own plugin\n")
        self.assertNotEqual(self.agents("install", "opencode", check=False).returncode, 0)
        self.agents("uninstall", "opencode")
        self.assertEqual(read_text(own), "// my own plugin\n")

    def test_review_symlinked_config_stays_a_symlink(self):
        real = os.path.join(self.tmp, "dotfiles", "AGENTS.md")
        os.makedirs(os.path.dirname(real))
        with open(real, "w") as f:
            f.write("# mine\n")
        os.makedirs(os.path.join(self.h, ".codex"))
        link = os.path.join(self.h, ".codex", "AGENTS.md")
        os.symlink(real, link)
        self.agents("install", "codex")
        self.assertTrue(os.path.islink(link))
        self.assertIn("fm next", read_text(real))

    def test_codex_home_and_xdg_config_are_honoured(self):
        codex, xdg = os.path.join(self.tmp, "ch"), os.path.join(self.tmp, "xdg-config")
        self.env.update(CODEX_HOME=codex, XDG_CONFIG_HOME=xdg)
        self.agents("install", "codex")
        self.agents("install", "opencode")
        self.assertTrue(os.path.exists(os.path.join(codex, "hooks.json")))
        self.assertTrue(os.path.exists(os.path.join(xdg, "opencode", "plugins", "foreman.ts")))

    def test_a_config_it_cannot_parse_is_left_alone(self):
        os.makedirs(os.path.join(self.h, ".gemini"))
        with open(os.path.join(self.h, ".gemini", "settings.json"), "w") as f:
            f.write("{ // comments\n}")
        p = self.agents("install", "gemini", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("settings.json", p.stderr + p.stdout)
        self.assertEqual(read_text(os.path.join(self.h, ".gemini", "settings.json")), "{ // comments\n}")

    def test_opencode_plugin_blocks_through_the_hook_under_bun(self):
        bun = shutil.which("bun")
        if not bun:
            self.skipTest("bun not installed")
        self.agents("install", "opencode")
        plugin = os.path.join(self.h, ".config", "opencode", "plugins", "foreman.ts")
        script = (f"import {{ Foreman }} from {json.dumps(plugin)};\n"
                  f"const h = await Foreman({{ directory: {json.dumps(self.repo)} }});\n"
                  "try { await h['tool.execute.before']({ tool: 'bash', sessionID: 's', callID: 'c' },"
                  " { args: { command: 'rm -rf ~' } }); console.log('allowed'); }"
                  " catch (e) { console.log('denied ' + e.message); }\n"
                  "await h['tool.execute.before']({ tool: 'bash', sessionID: 's', callID: 'd' },"
                  " { args: { command: 'ls' } }); console.log('ls ok');\n")
        path = os.path.join(self.tmp, "t.ts")
        with open(path, "w") as f:
            f.write(script)
        p = subprocess.run([bun, path], capture_output=True, text=True, timeout=60,
                           env=dict(os.environ, FOREMAN_HOME=self.home))
        self.assertIn("denied", p.stdout, p.stderr)
        self.assertIn("ls ok", p.stdout, p.stderr)


class Block(ForemanTestCase):
    def test_removing_the_block_never_joins_the_users_lines(self):
        import fmagents as a
        put = a._block("a\n", "S", "E", "x")
        self.assertEqual(a._block(put, "S", "E", None), "a\n")
        self.assertEqual(a._block(put + "b\n", "S", "E", None), "a\n\nb\n")
        self.assertEqual(a._block(a._block(put + "b\n", "S", "E", "y"), "S", "E", None), "a\n\nb\n")
