"""Static checks on the prose parts of the plugin: budgets, frontmatter, read-only agents, attribution, index."""
import json
import os
import re
import unittest

from helpers import PLUGIN, read_text, read_json

SKILLS = ["intake", "next", "resume", "status", "capture", "tidy", "doctor", "reflect", "improve", "playbooks", "brainstorm"]
USER_ONLY = {"capture"}  # everything else Claude may start itself when the user asks in plain words
READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}
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
                        self.assertIn(marker, read_text(path, limit=400))

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
                self.assertTrue(tools <= READ_ONLY_TOOLS, tools - READ_ONLY_TOOLS)
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
        for needle in ("▸ Step", "✓", "Changed:", "Next:", "Needs you"):
            self.assertIn(needle, body)
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
            self.assertEqual(len(handlers), 1, event)
            self.assertEqual(handlers[0]["args"], [event])

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


if __name__ == "__main__":
    unittest.main()
