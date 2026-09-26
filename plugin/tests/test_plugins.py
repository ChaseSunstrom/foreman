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

    def test_cli(self):
        out = self.fm("plugins", "find", "rust", "language", "server", env={"CLAUDE_CONFIG_DIR": self.cc}).stdout
        self.assertIn("rust-analyzer-lsp@official", out)
        self.assertIn("Rust language server", out)


class Install(PluginsCase):
    def setUp(self):
        super().setUp()
        self.bin, self.calls = os.path.join(self.tmp, "bin"), os.path.join(self.tmp, "calls.log")
        write(os.path.join(self.bin, "claude"), f'#!/usr/bin/env bash\necho "claude $*" >> {self.calls}\n')
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
