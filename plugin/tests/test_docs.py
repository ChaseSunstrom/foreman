"""Static checks on the prose parts of the plugin: budgets, frontmatter, read-only agents, attribution, index."""
import json
import os
import re
import unittest

from helpers import PLUGIN, read_text, read_json

SKILLS = ["intake", "next", "resume", "status", "capture", "tidy", "doctor", "reflect", "improve", "playbooks", "brainstorm"]
USER_ONLY = {"capture"}  # everything else Claude may start itself when the user asks in plain words
READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}
EDITING_AGENTS = {"fm-builder.md": {"Edit", "Write", "Bash"},  # T-0234: the exceptions, worktree-bound
                  "fm-reproducer.md": {"Edit", "Write", "Bash"}}  # T-0608
HOOK_EVENTS = {"SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "PostToolUseFailure", "PreCompact",
               "Stop", "TaskCompleted", "SubagentStart", "SubagentStop", "MessageDisplay", "Notification", "SessionEnd", "PermissionRequest"}
OWN_REFERENCES = {"language.md", "planning.md", "execute.md", "delegate.md", "audit.md"}


def frontmatter(path):
    text = read_text(path, encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    assert m, f"{path}: no frontmatter"
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        if k.strip():
            meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2)


def rel(path):
    return os.path.relpath(path, PLUGIN)


class Rules(unittest.TestCase):
    def test_rules_file_within_always_on_budget(self):
        lines = read_text(os.path.join(PLUGIN, "rules", "foreman.md")).splitlines()
        self.assertLessEqual(len(lines), 80)
        self.assertTrue(lines[0].startswith("# "))


class Skills(unittest.TestCase):
    def test_every_spec_skill_exists_with_valid_frontmatter(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                meta, body = frontmatter(os.path.join(PLUGIN, "skills", name, "SKILL.md"))
                self.assertEqual(meta.get("name"), name)
                self.assertTrue(20 < len(meta.get("description", "")) <= 1024)
                self.assertLess(len(body.splitlines()), 500)
                self.assertEqual(meta.get("disable-model-invocation") == "true", name in USER_ONLY)

    def test_skill_references_exist(self):
        for name in SKILLS:
            body = read_text(os.path.join(PLUGIN, "skills", name, "SKILL.md"))
            for ref in re.findall(r"`(references/[\w./-]+\.md)`", body):
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue(os.path.exists(os.path.join(PLUGIN, "skills", name, ref)))

    def test_audit_reference_defines_every_lens_fm_requires(self):
        import fmcore as c
        body = read_text(os.path.join(PLUGIN, "skills", "intake", "references", "audit.md"))
        for lens in c.AUDIT_LENSES:
            with self.subTest(lens=lens):
                self.assertIn(f"**{lens}**", body)
        for tier in ("S", "M", "L"):
            self.assertIn(f"| {tier} |", body)
        self.assertIn("references/audit.md", read_text(os.path.join(PLUGIN, "skills", "intake", "SKILL.md")))

    def test_playbook_index_covers_every_reference(self):
        body = read_text(os.path.join(PLUGIN, "skills", "playbooks", "SKILL.md"))
        root = os.path.join(PLUGIN, "skills", "playbooks", "references")
        for dirpath, _, files in os.walk(root):
            for f in files:
                with self.subTest(file=f):
                    self.assertIn(os.path.relpath(os.path.join(dirpath, f), os.path.dirname(root)), body)

    def test_ported_files_carry_attribution(self):
        for skill, marker in (("playbooks", "Ported from ECC"), ("intake", "Ported from superpowers")):
            root = os.path.join(PLUGIN, "skills", skill, "references")
            for dirpath, _, files in os.walk(root):
                for f in files:
                    if skill == "intake" and f in OWN_REFERENCES:
                        continue
                    path = os.path.join(dirpath, f)
                    with self.subTest(file=rel(path)):
                        head = read_text(path, limit=400)
                        self.assertTrue(marker in head or "Foreman's own" in head, "ported files say from where")

    def test_third_party_licenses(self):
        text = read_text(os.path.join(PLUGIN, "THIRD_PARTY_LICENSES.md"))
        self.assertIn("Copyright (c) 2026 Affaan Mustafa", text)
        self.assertIn("Copyright (c) 2025 Jesse Vincent", text)


class Agents(unittest.TestCase):
    def test_agents_are_read_only(self):
        agents = sorted(os.listdir(os.path.join(PLUGIN, "agents")))
        self.assertIn("fm-recon.md", agents)
        self.assertIn("fm-reviewer.md", agents)
        self.assertNotIn("fm-ideas.md", agents, "a subagent can't be tool-less; brainstormers run via fm ideas")
        for a in agents:
            with self.subTest(agent=a):
                meta, body = frontmatter(os.path.join(PLUGIN, "agents", a))
                tools = {t.strip() for t in meta["tools"].split(",") if t.strip()}
                self.assertTrue(tools, "an empty tools list means every tool")
                allowed = READ_ONLY_TOOLS | EDITING_AGENTS.get(a, set())
                self.assertTrue(tools <= allowed, tools - allowed)
                self.assertIn("400 words", body)


class PluginConflicts(unittest.TestCase):
    def test_setup_plugins_and_fm_plugins_share_one_curated_conflict_list(self):
        import fmplugins
        with open(os.path.join(os.path.dirname(PLUGIN), "setup-plugins.sh")) as f:
            names = {m.split("@")[0] for m in re.findall(r'^conflict "([^"]+)"', f.read(), re.M)}
        self.assertEqual(names, set(fmplugins.KNOWN_CONFLICTS))


class OutputStyle(unittest.TestCase):
    def test_foreman_style_is_well_formed_and_keeps_the_coding_instructions(self):
        import fmsetup
        path = os.path.join(PLUGIN, "output-styles", "foreman.md")
        with open(path) as f:
            text = f.read()
        head, body = text.split("---\n")[1], text.split("---\n", 2)[2]
        self.assertIn("name: Foreman", head)
        self.assertIn("keep-coding-instructions: true", head)
        self.assertEqual(fmsetup.OUTPUT_STYLE, "foreman:Foreman")  # plugin styles are selected as <plugin>:<name>
        for needle in ("✓", "Changed:", "Next:", "Needs you", "write nothing between tool calls"):
            self.assertIn(needle, body)
        self.assertNotIn("▸ Step", body, "the band and tool rows show steps; replies don't repeat them (T-0095)")
        self.assertLess(len(body.split()), 260, "it's in every prompt: keep it short")


class PluginFiles(unittest.TestCase):
    def test_settings_only_supported_keys(self):
        settings = read_json(os.path.join(PLUGIN, "settings.json"))
        self.assertTrue(set(settings) <= {"agent", "subagentStatusLine"})

    def test_theme_is_valid(self):
        theme = read_json(os.path.join(PLUGIN, "themes", "foreman.json"))
        self.assertIn(theme["base"], {"dark", "light", "dark-daltonized", "light-daltonized", "dark-ansi", "light-ansi"})
        for v in theme["overrides"].values():
            self.assertRegex(v, r"^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|ansi:\w+|ansi256\(\d+\)|rgb\(\d+,\d+,\d+\))$")

    def test_hooks_json_uses_known_events_and_one_handler_each(self):
        hooks = read_json(os.path.join(PLUGIN, "hooks", "hooks.json"))["hooks"]
        self.assertEqual(set(hooks), HOOK_EVENTS)
        for event, groups in hooks.items():
            handlers = [h for g in groups for h in g["hooks"]]
            # T-0724: PreToolUse has a second entry, for Read (outline-first), with its own failure rule; T-0784: a
            # third, for the tools that send content off the machine; T-0947: PostToolUse is sync for file writes
            # (their validators block, handler PostToolUseValidate) beside the async catch-all
            self.assertEqual(len(handlers), {"PreToolUse": 3, "PostToolUse": 2}.get(event, 1), event)
            self.assertTrue(all(h["args"] in ([event], [event + "Validate"]) for h in handlers), event)

    def test_the_guard_hook_fails_closed(self):
        hooks = read_json(os.path.join(PLUGIN, "hooks", "hooks.json"))["hooks"]
        for event, groups in hooks.items():
            for g in groups:
                for h in g["hooks"]:
                    if event == "PreToolUse" and g["matcher"] != "Read":
                        self.assertEqual(h.get("onFailure"), "block")
                    else:
                        self.assertNotIn("onFailure", h, event)

    def test_rules_never_contain_a_frontmatter_delimiter(self):
        # Eval cases embed the rules in YAML frontmatter; `claude plugin eval` ends the frontmatter at any "---",
        # which left every case prompt starting mid-rules (found in the 1.1 eval run).
        self.assertNotIn("---", read_text(os.path.join(PLUGIN, "rules", "foreman.md")))

    def test_eval_cases_embed_the_current_rules(self):
        """Eval runs use a temp HOME where ~/.claude/rules/foreman.md isn't installed; each case carries the rules instead."""
        rules = read_text(os.path.join(PLUGIN, "rules", "foreman.md"))
        root = os.path.join(PLUGIN, "evals")
        cases = [d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "prompt.md"))]
        self.assertGreaterEqual(len(cases), 5)
        for case in cases:
            with self.subTest(case=case):
                text = read_text(os.path.join(root, case, "prompt.md"))
                m = re.search(r"^append_system_prompt: \|\n((?:  .*\n|\n)*)", text, re.M)
                self.assertIsNotNone(m, "append_system_prompt block missing (run tests/e2e/sync_evals.py)")
                embedded = "\n".join(l[2:] for l in m.group(1).rstrip("\n").split("\n"))
                self.assertEqual(embedded.strip(), rules.strip())

    def test_build_command_still_present(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN, "commands", "build.md")))

    def test_executables_are_executable(self):
        for f in ("bin/fm", "hooks/hook", "hooks/statusline", "hooks/subagent-statusline"):
            with self.subTest(f=f):
                self.assertTrue(os.access(os.path.join(PLUGIN, f), os.X_OK))


class Site(unittest.TestCase):
    """T-1206, T-1220: the Pages site builds (site/build.py, as the workflow runs it) into pages whose local links all
    resolve, and every feature page carries a chart or figures from site/data/stats.json."""
    ROOT = os.path.dirname(PLUGIN)

    def test_a_long_chart_label_stays_inside_its_card(self):
        # T-1239: the harder suite's task names ("Add ledger.lexer.tokenize") ran out of the paired bars' card
        import importlib.util
        import re
        spec = importlib.util.spec_from_file_location("site_build", os.path.join(self.ROOT, "site", "build.py"))
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        svg = build.pairs("Cost", "note", [("Add ledger.lexer.tokenize", 0.07, 0.08), ("Group thousands in invoice "
                                                                                       "amounts", 0.1, 0.09)])
        labels = re.findall(r'(<text class="lab"[^>]*>)([^<]+)<', svg)
        self.assertEqual(len(labels), 2)
        for tag, label in labels:
            x, anchor = float(re.search(r' x="([\d.]+)"', tag)[1]), (re.search(r'text-anchor="(\w+)"', tag) or [0, ""])[1]
            left = x - (len(label) * 6.5 if anchor == "end" else 0)
            self.assertGreaterEqual(left, 0, label)
            self.assertLessEqual(x + (0 if anchor == "end" else len(label) * 6.5), 640, label)

    def _site(self, name):
        import importlib.util
        import sys
        sys.path.insert(0, os.path.join(self.ROOT, "site"))
        try:
            spec = importlib.util.spec_from_file_location(name, os.path.join(self.ROOT, "site", name + ".py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        finally:
            sys.path.pop(0)

    def test_a_task_name_in_the_duel_table_is_escaped(self):
        # site review: the case name (from an agent-written title) was the one unescaped value
        pages = self._site("pages")
        side = {"pass": True, "cost": 0.1, "seconds": 10, "runs": 1, "passed": 1, "turns": 3, "score": None}
        html = pages._duel({"duels": [{"name": "q", "cases": [{"case": "<b>x</b> & y", "foreman": side,
                                                               "bare": side}]}]}, "q")
        self.assertNotIn("<b>x</b>", html)
        self.assertIn("&lt;b&gt;x&lt;/b&gt; &amp; y", html)

    def test_the_build_refuses_to_wipe_the_repo_its_source_or_home(self):
        # site review: build.py OUT ran shutil.rmtree on whatever it was given (python3 site/build.py . wiped the repo)
        build = self._site("build")
        for bad in (self.ROOT, os.path.join(self.ROOT, "site"), os.path.expanduser("~"), "/", os.path.dirname(self.ROOT)):
            self.assertFalse(build.safe_out(bad), bad)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(build.safe_out(os.path.join(tmp, "_site")))
        self.assertTrue(build.safe_out(os.path.join(self.ROOT, "_site")))

    def test_a_new_duel_keeps_the_saved_ones(self):
        # site review: stats.py --duel long=DIR alone replaced quality, hard and hard-haiku with nothing
        stats = self._site("stats")
        merged = stats.merge_duels([{"name": "quality", "cases": [1]}, {"name": "long", "cases": [1]}],
                                   [{"name": "long", "cases": [2]}, {"name": "marathon", "cases": [3]}])
        self.assertEqual([(d["name"], d["cases"]) for d in merged],
                         [("quality", [1]), ("long", [2]), ("marathon", [3])])

    def test_the_long_session_section_shows_each_run_and_each_request(self):
        pages = self._site("pages")
        side = lambda t, f: {"pass": True, "cost": 0.1, "seconds": 400, "runs": 2, "passed": 2, "turns": 60,
                             "score": None, "each": [{"tests": [t, 105], "compactions": 3}, {"tests": [105, 105],
                                                                                           "compactions": 4}],
                             "requests": [{"title": "Add <ini>", "failed": f}], "found": ["Fix a crash (discovered)"]}
        html = pages._long({"duels": [{"name": "marathon", "marathon": 5, "cases": [
            {"case": "x", "foreman": side(100, 5), "bare": side(105, 0)}]}]}, "marathon")
        self.assertIn("100, 105 of 105", html)
        self.assertIn("3, 4", html)
        self.assertIn("✗ 5 failing", html)
        self.assertIn("Add &lt;ini&gt;", html)
        self.assertIn("Fix a crash", html)
        self.assertNotIn("(discovered)", html)

    def test_a_line_chart_with_no_rows_says_so(self):
        build = self._site("build")
        self.assertIn("No data", build.line("Releases", "note", [], "n", "day"))

    def test_the_benchmarks_page_opens_with_why_use_foreman(self):
        # T-1241: a reader saw equal pass rates and asked why anyone would use Foreman; the page answers first
        import sys
        sys.path.insert(0, os.path.join(self.ROOT, "site"))
        try:
            import pages
        finally:
            sys.path.pop(0)
        bench = next(p for p in pages.PAGES if p["slug"] == "benchmarks")
        kind, title, body = bench["blocks"][0]
        self.assertEqual((kind, title), ("text", "Why use Foreman"))
        for words in ("24 dangerous", "both sides pass", "more", "not measured yet"):
            self.assertIn(words, body)

    def test_the_site_builds_and_every_local_link_resolves(self):
        import subprocess
        import sys
        import tempfile
        flow = read_text(os.path.join(self.ROOT, ".github", "workflows", "pages.yml"))
        self.assertIn("python3 site/build.py _site", flow)
        with tempfile.TemporaryDirectory() as out:
            p = subprocess.run([sys.executable, os.path.join(self.ROOT, "site", "build.py"), out], capture_output=True,
                               text=True, timeout=120)
            self.assertEqual(p.returncode, 0, p.stderr)
            pages = [os.path.join(d, f) for d, _, fs in os.walk(out) for f in fs if f.endswith(".html")]
            features = [f for f in pages if os.sep + "features" + os.sep in f and not f.endswith("index.html")]
            self.assertGreaterEqual(len(features), 12)
            for path in pages:
                page = read_text(path)
                for u in re.findall(r'(?:src|href|poster)="([^"]+)"', page):
                    u = u.split("#")[0].split("?")[0]
                    if u and ":" not in u and not u.startswith("//"):
                        self.assertTrue(os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), u))),
                                        f"{os.path.relpath(path, out)} links to {u}")
                for anchor in re.findall(r'href="#([\w-]+)"', page):
                    self.assertIn(f'id="{anchor}"', page, os.path.relpath(path, out))
            for path in features:
                page = read_text(path)
                self.assertTrue('class="viz"' in page or 'class="tiles"' in page or 'class="flow"' in page, path)
                self.assertIn('class="side"', page)


if __name__ == "__main__":
    unittest.main()
