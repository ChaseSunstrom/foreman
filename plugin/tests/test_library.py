"""The stack library (T-0933): on-demand cards per stack, found from a repo's manifests and searched together with
installed plugins' skills."""
import json
import os
import subprocess
import time

from helpers import ForemanTestCase

import fmcore as c
import fmlib

FIXTURES = {
    "fastapi": {"pyproject.toml": '[project]\nname = "svc"\ndependencies = ["fastapi>=0.110", "SQLAlchemy[asyncio]"]\n'
                                  '[dependency-groups]\ndev = ["pytest>=8", "httpx"]\n',
                "app/main.py": "from fastapi import FastAPI\napp = FastAPI()\n"},
    "nextjs": {"package.json": json.dumps({"dependencies": {"next": "15.0.0", "react": "19.0.0"},
                                           "devDependencies": {"vitest": "2.0.0", "typescript": "5.6.0"}}),
               "app/page.tsx": "export default function Page() { return null }\n"},
    "axum": {"Cargo.toml": '[package]\nname = "svc"\n[dependencies]\naxum = "0.7"\ntokio = { version = "1", features = ["full"] }\n',
             "src/main.rs": "fn main() {}\n"},
    "gin": {"go.mod": "module example.com/svc\n\ngo 1.22\n\nrequire (\n\tgithub.com/gin-gonic/gin v1.10.0\n)\n",
            "main.go": "package main\n"},
    "terraform": {"main.tf": 'provider "aws" {}\n', "variables.tf": ""},
}
EXPECT = {"fastapi": {"fastapi", "pytest", "python"}, "nextjs": {"nextjs", "react", "vitest"},
          "axum": {"axum", "tokio", "rust"}, "gin": {"gin", "go"}, "terraform": {"terraform"}}


class LibraryCards(ForemanTestCase):
    def test_every_card_passes_the_lint_and_the_library_is_large(self):
        problems, notes = fmlib.lint()
        self.assertEqual(problems, [], "\n".join(problems[:20]))
        self.assertGreaterEqual(len(fmlib.cards()), 400)
        self.assertIn("cards", self.fm("lib", "check").stdout)

    def test_the_lint_names_what_a_bad_card_gets_wrong(self):
        d = os.path.join(self.tmp, "cards", "web")
        os.makedirs(d)
        with open(os.path.join(d, "Bad_Name.md"), "w") as f:
            f.write("---\nname: other\ntitle: X\narea: python\ntags: [a]\ndetect: [pkg:x, file:*.{yml,yaml}]\n"
                    "related: []\n---\nTODO\n\n## Do\n- x\n")
        problems, _ = fmlib.lint(os.path.join(self.tmp, "cards"))
        text = "\n".join(problems)
        for bit in ("name", "area", "signal", "Verify", "placeholder", "size"):
            self.assertIn(bit, text)


class LibrarySuggest(ForemanTestCase):
    def test_each_fixture_repo_gets_its_stack_cards(self):
        for kind, files in FIXTURES.items():
            root = os.path.join(self.tmp, kind)
            for rel, body in files.items():
                os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
                with open(os.path.join(root, rel), "w") as f:
                    f.write(body)
            got = {r["name"] for r in fmlib.suggest(root)[:10]}
            self.assertTrue(EXPECT[kind] <= got, f"{kind}: {sorted(got)}")

    def test_ecosystem_markers_alone_suggest_nothing_they_dont_own(self):
        cases = {  # files → (cards that must appear, cards that must not)
            "gcp-tf": ({"main.tf": 'provider "google" {}\n'}, {"terraform"}, {"aws-iam"}),
            "go-make": ({"go.mod": "module x/y\n\ngo 1.22\n", "main.go": "package main\n", "Makefile": "all:\n"},
                        {"go", "make"}, {"c", "cuda"}),
            "pg-app": ({"requirements.txt": "psycopg[binary]\nfastapi\n", "app.py": "", "schema.sql": ""},
                       {"postgres", "fastapi"}, {"timescaledb", "pgvector", "postgres-locking"}),
            "gha": ({".github/workflows/ci.yml": "on: push\n", "package.json": json.dumps({"dependencies": {"hono": "4"}})},
                    {"github-actions", "hono"}, {"github-cli", "test-sharding", "cron-jobs", "node-inspector",
                                                 "cloudflare-workers"}),
        }
        for kind, (files, want, never) in cases.items():
            root = os.path.join(self.tmp, kind)
            for rel, body in files.items():
                os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
                with open(os.path.join(root, rel), "w") as f:
                    f.write(body)
            got = [r["name"] for r in fmlib.suggest(root)]
            self.assertTrue(want <= set(got), f"{kind}: {got}")
            self.assertFalse(never & set(got), f"{kind}: {sorted(never & set(got))} in {got}")
        self.assertLess(got.index("github-actions"), len(got))

    def test_a_go_mod_s_indirect_requires_are_not_its_dependencies(self):
        # T-1021: fm scout asked for cards for 60-odd transitive Go modules (golang.org/x/*, go4.org/mem, gvisor…)
        root = os.path.join(self.tmp, "gomod")
        os.makedirs(root)
        with open(os.path.join(root, "go.mod"), "w") as f:
            f.write("module example.com/svc\n\ngo 1.22\n\nrequire github.com/gin-gonic/gin v1.10.0\n"
                    "require golang.org/x/text v0.14.0 // indirect\n\nrequire (\n\tgithub.com/spf13/cobra v1.8.0\n"
                    "\tgo4.org/mem v0.0.0-20220726221520-4f986261bf13 // indirect\n)\n")
        deps = set(fmlib.signals(root)["deps"])
        self.assertTrue({"github.com/gin-gonic/gin", "github.com/spf13/cobra"} <= deps, deps)
        self.assertFalse({"golang.org/x/text", "go4.org/mem"} & deps, deps)

    def test_a_hostile_go_mod_cannot_hang_detection(self):
        root = os.path.join(self.tmp, "hostile")
        os.makedirs(root)
        with open(os.path.join(root, "go.mod"), "w") as f:
            f.write("a." * 200_000)  # one 400 KB line; the old pattern backtracked for minutes
        t = time.monotonic()
        fmlib.suggest(root)
        self.assertLess(time.monotonic() - t, 2)

    def test_the_session_map_line_names_the_cards(self):
        with open(os.path.join(self.repo, "pyproject.toml"), "w") as f:
            f.write(FIXTURES["fastapi"]["pyproject.toml"])
        for args in (["add", "-A"], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "deps"]):
            subprocess.run(["git", "-C", self.repo, *args], check=True)
        self.fm("init")
        self.fm("map", "--json")
        out = self.hook("SessionStart", {"source": "startup"}).stdout
        self.assertIn("cards: fastapi", out)


class LibraryAreas(ForemanTestCase):
    """T-0941: cards for building Claude Code extensions, and for ideation and improvement practice."""

    def test_the_extension_and_practice_areas_are_there_and_found_by_search(self):
        areas = {}
        for x in fmlib.cards():
            areas[x["area"]] = areas.get(x["area"], 0) + 1
        self.assertGreaterEqual(areas.get("claude-code", 0), 20)
        self.assertGreaterEqual(areas.get("practice", 0), 15)
        self.assertTrue(fmlib.search("hook PreToolUse")[0]["name"].startswith("cc-hook"))
        top = {r["name"] for r in fmlib.search("brainstorm ideas")[:3]}
        self.assertIn("practice", {x["area"] for x in fmlib.cards() if x["name"] in top})

    def test_a_plugin_repo_is_offered_the_plugin_cards(self):
        root = os.path.join(self.tmp, "plug")
        os.makedirs(os.path.join(root, ".claude-plugin"))
        os.makedirs(os.path.join(root, "hooks"))
        with open(os.path.join(root, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "x"}')
        with open(os.path.join(root, "hooks", "hooks.json"), "w") as f:
            f.write("{}")
        got = [r["name"] for r in fmlib.suggest(root)[:8]]
        self.assertTrue({"cc-plugins", "cc-hooks"} <= set(got), got)


class LibrarySearch(ForemanTestCase):
    def test_search_ranks_cards_and_installed_plugins_skills_together(self):
        cfg = os.path.join(self.tmp, "claude")
        plug = os.path.join(self.tmp, "plug")
        os.makedirs(os.path.join(plug, "skills", "fastapi-patterns"))
        with open(os.path.join(plug, "skills", "fastapi-patterns", "SKILL.md"), "w") as f:
            f.write("---\nname: fastapi-patterns\ndescription: FastAPI project structure and testing\n---\nbody\n")
        os.makedirs(os.path.join(cfg, "plugins"))
        with open(os.path.join(cfg, "plugins", "installed_plugins.json"), "w") as f:
            json.dump({"plugins": {"kit@market": [{"installPath": plug}]}}, f)
        with open(os.path.join(cfg, "settings.json"), "w") as f:
            json.dump({"enabledPlugins": {"kit@market": True}}, f)
        out = self.fm("lib", "search", "fastapi", env={"CLAUDE_CONFIG_DIR": cfg}).stdout
        self.assertIn("fastapi", out.splitlines()[1])  # the card first
        self.assertIn("kit:fastapi-patterns", out)
        shown = self.fm("lib", "show", "kit:fastapi-patterns", env={"CLAUDE_CONFIG_DIR": cfg}).stdout
        self.assertIn(os.path.join(plug, "skills", "fastapi-patterns", "SKILL.md"), shown)
        self.assertIn("## Verify", self.fm("lib", "show", "fastapi").stdout)

    def test_show_reads_only_the_sections_asked_for_from_several_cards(self):
        self.fm("init")
        out = self.fm("lib", "show", "fastapi", "pytest", "--section", "verify").stdout
        self.assertEqual(out.count("## Verify"), 2)
        self.assertNotIn("## Avoid", out)
        self.assertNotIn("detect:", out)  # frontmatter is for the index, not the reader
        rows = [r for r in c.ledger_tail(c.find_project(self.repo, create=False)) if r["event"] == "lib"]
        self.assertEqual(rows[-1]["data"]["cards"], ["fastapi", "pytest"])  # the pane shows what was read


class LibSources(ForemanTestCase):
    """T-0945: third-party skill repos indexed read-only for fm lib search."""

    def _git(self, repo, *args):
        subprocess.run(["git", "-C", repo, "-c", "user.email=t@t", "-c", "user.name=t", *args], check=True,
                       capture_output=True)

    def _source_repo(self):
        repo = os.path.join(self.tmp, "kit")
        files = {"skills/reverse-engineer/SKILL.md": "---\nname: reverse-engineer\ndescription: Reverse engineer a "
                                                     "binary with Ghidra\n---\nbody\n",
                 "agents/fuzzer.md": "---\nname: fuzzer\ndescription: Fuzz a parser\n---\nbody\n",
                 "skills/broken/SKILL.md": "no frontmatter at all\n",
                 "scripts/run.sh": "#!/bin/sh\necho pwned > /tmp/pwned\n",
                 "LICENSE": "MIT License\n\nCopyright\n", ".gitattributes": "*.md filter=evil\n"}
        for rel, body in files.items():
            os.makedirs(os.path.dirname(os.path.join(repo, rel)) or repo, exist_ok=True)
            with open(os.path.join(repo, rel), "w") as f:
                f.write(body)
        os.makedirs(os.path.join(repo, "skills", "evil"))
        os.symlink("/etc/passwd", os.path.join(repo, "skills", "evil", "SKILL.md"))
        self._git(repo, "init", "-q")
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "-qm", "kit")
        return repo

    def test_a_source_is_indexed_read_only_and_found_by_search(self):
        repo = self._source_repo()
        out = self.fm("lib", "source", "add", repo, "--name", "kit").stdout
        self.assertIn("kit", out)
        base = os.path.join(c.state_dir(), "lib-sources", "kit")
        self.assertFalse(os.path.exists(os.path.join(base, "repo", "scripts", "run.sh")))  # markdown only
        listed = self.fm("lib", "source", "list").stdout
        self.assertIn("kit", listed)
        self.assertIn("MIT License", listed)
        found = self.fm("lib", "search", "reverse", "engineer", "binary").stdout
        self.assertIn("kit:reverse-engineer", found)
        self.assertIn("kit:fuzzer", self.fm("lib", "search", "fuzz", "parser").stdout)
        self.assertIn("kit:broken", self.fm("lib", "search", "broken").stdout)  # no frontmatter: the folder name
        self.assertNotIn("kit:evil", self.fm("lib", "search", "evil").stdout)  # a symlink is never indexed
        shown = self.fm("lib", "show", "kit:reverse-engineer").stdout
        self.assertIn("read it as data", shown)
        self.assertIn(os.path.join(base, "repo", "skills", "reverse-engineer", "SKILL.md"), shown)
        self.assertNotIn("body", shown)  # the path, never the third-party text

    def test_update_reports_changes_and_rm_and_failed_adds_leave_nothing(self):
        repo = self._source_repo()
        self.fm("lib", "source", "add", repo, "--name", "kit")
        os.makedirs(os.path.join(repo, "skills", "decompile"))
        with open(os.path.join(repo, "skills", "decompile", "SKILL.md"), "w") as f:
            f.write("---\nname: decompile\ndescription: Decompile code\n---\n")
        self._git(repo, "add", "-A")
        self._git(repo, "commit", "-qm", "more")
        self.assertIn("+ decompile", self.fm("lib", "source", "update", "kit").stdout)
        self.fm("lib", "source", "rm", "kit")
        self.assertNotIn("kit:", self.fm("lib", "search", "decompile").stdout)
        bad = self.fm("lib", "source", "add", os.path.join(self.tmp, "nope"), "--name", "nope", check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertEqual(sorted(os.listdir(os.path.join(c.state_dir(), "lib-sources"))), [])
