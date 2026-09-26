"""fm plugins: find in the known marketplaces, check enabled plugins for conflicts, install after the user's yes."""
import json
import os

from helpers import ForemanTestCase, read_json, read_text

import fmplugins


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text if isinstance(text, str) else json.dumps(text))


class PluginsCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")
        self.cc = os.path.join(self.uhome, ".claude")
        pl = os.path.join(self.cc, "plugins")
        mk = os.path.join(pl, "marketplaces", "official")
        write(os.path.join(mk, ".claude-plugin", "marketplace.json"), {"name": "official", "plugins": [
            {"name": "rust-analyzer-lsp", "source": "./plugins/rust-analyzer-lsp", "category": "development",
             "description": "Rust language server for code intelligence and diagnostics"},
            {"name": "superpowers", "source": {"source": "github", "repo": "obra/superpowers"},
             "description": "TDD, brainstorming-before-coding and planning, all auto-triggering"},
            {"name": "postgres-mcp", "source": "./plugins/postgres-mcp", "description": "Postgres MCP server"},
            {"name": "db-tools", "source": "./plugins/db-tools", "description": "Database helpers with a Postgres MCP"},
        ]})
        write(os.path.join(mk, "plugins", "rust-analyzer-lsp", "skills", "rust", "SKILL.md"),
              "---\nname: rust\ndescription: Rust idioms and the borrow checker.\n---\nbody\n")
        cache = os.path.join(pl, "cache", "official")
        self.paths = {n: os.path.join(cache, n, "1.0") for n in ("ralph-loop", "postgres-mcp", "db-tools", "ideas-kit")}
        write(os.path.join(self.paths["ralph-loop"], "hooks", "hooks.json"),
              {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "loop.sh"}]}]}})
        for n in ("postgres-mcp", "db-tools"):
            write(os.path.join(self.paths[n], ".mcp.json"), {"mcpServers": {"postgres": {"command": "npx", "args": ["pg-mcp"]}}})
        write(os.path.join(self.paths["ideas-kit"], "skills", "brainstorming", "SKILL.md"),
              "---\nname: brainstorming\ndescription: Use before any creative work to explore ideas first.\n---\n")
        write(os.path.join(pl, "installed_plugins.json"), {"version": 2, "plugins": {
            f"{n}@official": [{"scope": "user", "installPath": p}] for n, p in self.paths.items()}})
        write(os.path.join(self.cc, "settings.json"), {"enabledPlugins": {f"{n}@official": True for n in self.paths}})
        os.environ["CLAUDE_CONFIG_DIR"] = self.cc

    def tearDown(self):
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
        super().tearDown()


class Find(PluginsCase):
    def test_ranks_marketplace_plugins_for_a_need(self):
        hits = fmplugins.find("rust language server")
        self.assertEqual(hits[0]["id"], "rust-analyzer-lsp@official")
        self.assertFalse(hits[0]["installed"])
        self.assertGreater(hits[0]["tokens"], 0, "measured from the marketplace's local copy")
        self.assertEqual({h["id"] for h in fmplugins.find("postgres")}, {"postgres-mcp@official", "db-tools@official"})
        self.assertEqual(fmplugins.find("kubernetes operator"), [])

    def test_short_words_match_whole_words(self):
        self.assertEqual(fmplugins.find("db"), [h for h in fmplugins.find("db") if "db" in h["id"]])
        self.assertEqual(fmplugins.find("go"), [], "go is not google, mongo or django")

    def test_cli(self):
        out = self.fm("plugins", "find", "rust", "language", "server", env={"CLAUDE_CONFIG_DIR": self.cc}).stdout
        self.assertIn("rust-analyzer-lsp@official", out)
        self.assertIn("Rust language server", out)


class Install(PluginsCase):
    def setUp(self):
        super().setUp()
        self.bin, self.calls = os.path.join(self.tmp, "bin"), os.path.join(self.tmp, "calls.log")
        # like the real CLI, a successful install lands in installed_plugins.json
        reg = os.path.join(self.cc, "plugins", "installed_plugins.json")
        write(os.path.join(self.bin, "claude"), f'#!/usr/bin/env bash\necho "claude $*" >> {self.calls}\n'
              f'if [ "$2" = install ]; then python3 -c "import json,sys; p=sys.argv[1]; d=json.load(open(p)); '
              f'd[\'plugins\'][sys.argv[2]]=[{{\'scope\':\'user\'}}]; json.dump(d,open(p,\'w\'))" {reg} "$3"; fi\n')
        os.chmod(os.path.join(self.bin, "claude"), 0o755)
        self.env = {"CLAUDE_CONFIG_DIR": self.cc, "HOME": self.uhome, "PATH": self.bin + os.pathsep + os.environ["PATH"]}

    def manifest(self):
        return read_json(os.path.join(self.home, "state", "install-manifest.json"))

    def test_install_records_it_for_uninstall(self):
        out = self.fm("plugins", "install", "rust-analyzer-lsp@official", env=self.env).stdout
        self.assertIn("claude plugin install rust-analyzer-lsp@official --scope user", read_text(self.calls))
        self.assertIn("installed", out)
        self.assertEqual(self.manifest()["plugins_installed"], ["rust-analyzer-lsp@official"])
        self.fm("uninstall-user", env=self.env)
        self.assertIn("claude plugin uninstall rust-analyzer-lsp@official --scope user", read_text(self.calls))

    def test_an_installed_but_disabled_plugin_is_enabled_instead(self):
        write(os.path.join(self.cc, "settings.json"), {"enabledPlugins": {"db-tools@official": False}})
        self.fm("plugins", "install", "db-tools@official", env=self.env)
        self.assertIn("claude plugin enable db-tools@official", read_text(self.calls))
        self.assertNotIn("plugin install", read_text(self.calls))

    def test_a_new_marketplace_is_added_recorded_and_removed_on_uninstall(self):
        mk = os.path.join(self.cc, "plugins", "marketplaces", "newmk", ".claude-plugin")
        write(os.path.join(self.bin, "claude"), f'#!/usr/bin/env bash\necho "claude $*" >> {self.calls}\n'
              f'if [ "$2" = marketplace ] && [ "$3" = add ]; then mkdir -p {mk}; '
              f"echo '{{\"name\": \"newmk\", \"plugins\": []}}' > {mk}/marketplace.json; fi\n")
        out = self.fm("plugins", "add-marketplace", "some-org/some-plugins", env=self.env).stdout
        self.assertIn("claude plugin marketplace add some-org/some-plugins", read_text(self.calls))
        self.assertIn("newmk", out)
        self.assertEqual(self.manifest()["marketplaces_added"], ["newmk"])
        self.fm("uninstall-user", env=self.env)
        self.assertIn("claude plugin marketplace remove newmk", read_text(self.calls))

    def test_forget_keeps_a_plugin_through_uninstall(self):
        self.fm("plugins", "install", "rust-analyzer-lsp@official", env=self.env)
        self.fm("plugins", "forget", "rust-analyzer-lsp@official", env=self.env)
        self.assertEqual(self.manifest()["plugins_installed"], [])
        self.fm("uninstall-user", env=self.env)
        self.assertNotIn("plugin uninstall", read_text(self.calls))

    def test_an_install_that_did_not_land_is_not_recorded(self):
        write(os.path.join(self.bin, "claude"), f'#!/usr/bin/env bash\necho "claude $*" >> {self.calls}\n')
        p = self.fm("plugins", "install", "rust-analyzer-lsp@official", env=self.env, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("isn't installed", p.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.home, "state", "install-manifest.json"))
                         and self.manifest().get("plugins_installed"))

    def test_a_missing_claude_cli_is_a_clean_error(self):
        env = dict(self.env, PATH=os.path.dirname(os.path.realpath(__import__("sys").executable)))
        p = self.fm("plugins", "install", "rust-analyzer-lsp@official", env=env, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn("claude", p.stderr)

    def test_install_shows_conflicts_first_and_refuses_unknown_ids(self):
        p = self.fm("plugins", "install", "nope@nowhere", env=self.env, check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("fm plugins find", p.stderr)


class Check(PluginsCase):
    def kinds(self):
        return {(f["plugin"], f["kind"]) for f in fmplugins.check()}

    def test_flags_stop_hooks_duplicate_mcp_servers_and_process_overlap(self):
        found = self.kinds()
        self.assertIn(("ralph-loop@official", "stop-hook"), found)
        self.assertEqual(len({p for p, k in found if k == "duplicate-mcp"} & {"db-tools@official", "postgres-mcp@official"}), 1)
        self.assertIn(("ideas-kit@official", "overlaps-foreman"), found)
        self.assertTrue(all(f["action"] for f in fmplugins.check()), "every finding says what to do")

    def test_curated_conflicts_are_reported(self):
        ecc = os.path.join(self.cc, "plugins", "cache", "ecc", "ecc", "1.0")
        os.makedirs(ecc)
        data = read_json(os.path.join(self.cc, "plugins", "installed_plugins.json"))
        data["plugins"]["ecc@ecc"] = [{"scope": "user", "installPath": ecc}]
        write(os.path.join(self.cc, "plugins", "installed_plugins.json"), data)
        s = read_json(os.path.join(self.cc, "settings.json"))
        s["enabledPlugins"]["ecc@ecc"] = True
        write(os.path.join(self.cc, "settings.json"), s)
        self.assertIn(("ecc@ecc", "known-conflict"), self.kinds())

    def test_profile_reads_block_scalars_and_plugin_json(self):
        d = os.path.join(self.tmp, "p")
        write(os.path.join(d, "skills", "long", "SKILL.md"),
              "---\nname: long\ndescription: >\n  Use this whenever the user asks about anything at all,\n"
              "  which is a very long always-on description.\nother: x\n---\nbody\n")
        write(os.path.join(d, ".claude-plugin", "plugin.json"), {"name": "p", "hooks": {"Stop": []},
                                                                 "mcpServers": {"pg": {"command": "pg"}}})
        prof = fmplugins.profile(d)
        self.assertIn("very long always-on", prof["skills"][0][1])
        self.assertNotIn("other", prof["skills"][0][1])
        self.assertEqual((prof["hooks"], set(prof["mcp"])), ({"Stop"}, {"pg"}))

    def test_the_install_entry_that_exists_is_used_and_project_settings_apply(self):
        data = read_json(os.path.join(self.cc, "plugins", "installed_plugins.json"))
        data["plugins"]["ralph-loop@official"].insert(0, {"scope": "project", "installPath": "/nonexistent"})
        write(os.path.join(self.cc, "plugins", "installed_plugins.json"), data)
        self.assertIn(("ralph-loop@official", "stop-hook"), self.kinds())
        write(os.path.join(self.repo, ".claude", "settings.local.json"), {"enabledPlugins": {"ralph-loop@official": False}})
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            self.assertNotIn(("ralph-loop@official", "stop-hook"), self.kinds())
        finally:
            os.chdir(cwd)

    def test_disabled_plugins_are_ignored(self):
        write(os.path.join(self.cc, "settings.json"), {"enabledPlugins": {"db-tools@official": False,
                                                                          "postgres-mcp@official": True}})
        self.assertNotIn("duplicate-mcp", {k for _, k in self.kinds()})

    def test_cli_and_doctor(self):
        out = self.fm("plugins", "check", env={"CLAUDE_CONFIG_DIR": self.cc}).stdout
        self.assertIn("ralph-loop@official", out)
        import fmdoctor
        r = fmdoctor.check_plugins()
        self.assertEqual(r.status, "WARN")
        self.assertIn("fm plugins check", r.detail)
