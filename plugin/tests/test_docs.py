"""Static checks on the prose parts of the plugin: budgets, frontmatter, read-only agents, attribution, index."""
import json
import os
import re
import unittest

from helpers import PLUGIN

SKILLS = ["intake", "next", "resume", "status", "capture", "tidy", "doctor", "reflect", "improve", "playbooks"]
USER_ONLY = {"status", "capture", "tidy", "doctor", "improve"}
READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}
HOOK_EVENTS = {"SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "PostToolUseFailure", "PreCompact",
               "Stop", "TaskCompleted", "SubagentStart", "SubagentStop", "MessageDisplay", "Notification", "SessionEnd"}
OWN_REFERENCES = {"language.md", "planning.md", "execute.md", "delegate.md"}


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
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
        lines = open(os.path.join(PLUGIN, "rules", "foreman.md")).read().splitlines()
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
            body = open(os.path.join(PLUGIN, "skills", name, "SKILL.md")).read()
            for ref in re.findall(r"`(references/[\w./-]+\.md)`", body):
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue(os.path.exists(os.path.join(PLUGIN, "skills", name, ref)))

    def test_playbook_index_covers_every_reference(self):
        body = open(os.path.join(PLUGIN, "skills", "playbooks", "SKILL.md")).read()
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
                        self.assertIn(marker, open(path, encoding="utf-8").read(400))

    def test_third_party_licenses(self):
        text = open(os.path.join(PLUGIN, "THIRD_PARTY_LICENSES.md")).read()
        self.assertIn("Copyright (c) 2026 Affaan Mustafa", text)
        self.assertIn("Copyright (c) 2025 Jesse Vincent", text)


class Agents(unittest.TestCase):
    def test_agents_are_read_only(self):
        agents = sorted(os.listdir(os.path.join(PLUGIN, "agents")))
        self.assertIn("fm-recon.md", agents)
        self.assertIn("fm-reviewer.md", agents)
        for a in agents:
            with self.subTest(agent=a):
                meta, body = frontmatter(os.path.join(PLUGIN, "agents", a))
                tools = {t.strip() for t in meta["tools"].split(",")}
                self.assertTrue(tools <= READ_ONLY_TOOLS, tools - READ_ONLY_TOOLS)
                self.assertIn("400 words", body)


class PluginFiles(unittest.TestCase):
    def test_settings_only_supported_keys(self):
        settings = json.load(open(os.path.join(PLUGIN, "settings.json")))
        self.assertTrue(set(settings) <= {"agent", "subagentStatusLine"})

    def test_theme_is_valid(self):
        theme = json.load(open(os.path.join(PLUGIN, "themes", "foreman.json")))
        self.assertIn(theme["base"], {"dark", "light", "dark-daltonized", "light-daltonized", "dark-ansi", "light-ansi"})
        for v in theme["overrides"].values():
            self.assertRegex(v, r"^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|ansi:\w+|ansi256\(\d+\)|rgb\(\d+,\d+,\d+\))$")

    def test_hooks_json_uses_known_events_and_one_handler_each(self):
        hooks = json.load(open(os.path.join(PLUGIN, "hooks", "hooks.json")))["hooks"]
        self.assertEqual(set(hooks), HOOK_EVENTS)
        for event, groups in hooks.items():
            handlers = [h for g in groups for h in g["hooks"]]
            self.assertEqual(len(handlers), 1, event)
            self.assertEqual(handlers[0]["args"], [event])

    def test_build_command_still_present(self):
        self.assertTrue(os.path.exists(os.path.join(PLUGIN, "commands", "build.md")))

    def test_executables_are_executable(self):
        for f in ("bin/fm", "hooks/hook", "hooks/statusline", "hooks/subagent-statusline"):
            with self.subTest(f=f):
                self.assertTrue(os.access(os.path.join(PLUGIN, f), os.X_OK))


if __name__ == "__main__":
    unittest.main()
