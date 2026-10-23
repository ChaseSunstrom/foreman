"""Static checks on the prose parts of the plugin: budgets, frontmatter, read-only agents, attribution, index."""
import json
import os
import re
import unittest

from helpers import PLUGIN, read_text, read_json

SKILLS = ["intake", "next", "resume", "status", "capture", "tidy", "doctor", "reflect", "improve", "playbooks", "brainstorm",
          "directions", "design-extract", "ui-design"]
# everything else Claude may start itself when the user asks in plain words; design-extract: the 2,000-character
# listing has no room for it, so Claude reaches its verbs through the directions skill and the UI playbooks (T-1507)
USER_ONLY = {"capture", "design-extract", "tidy", "doctor"}  # T-1705: the rules map these plain words to the fm verbs, not the skills
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


def fm_mention_problems(text):
    """T-1701: each `fm VERB [word]` in backticks that names no command, or a lowercase word that isn't one of the
    verb's subcommands or its first positional's choices. The one checker every skill test shares."""
    import fmcli

    def first_positional_choices(parser):
        pos = next((a for a in parser._actions if not a.option_strings), None)
        return pos.choices if pos is not None else None

    verbs, bad = first_positional_choices(fmcli.build_parser()), []
    for verb, word in re.findall(r"`fm ([\w-]+)((?: [a-z][\w-]*)?)", text):
        inner = first_positional_choices(verbs[verb]) if verb in verbs else None
        if verb not in verbs:
            bad.append(f"fm {verb}")
        elif inner and word and word.strip() not in inner:
            bad.append(f"fm {verb}{word}")
    return bad


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

    def test_every_skill_the_rules_map_plain_words_to_is_model_invocable(self):
        # T-1705: a user-only skill can't be loaded by the model, so the rules may not send it there
        rules = read_text(os.path.join(PLUGIN, "rules", "foreman.md"))
        for name in re.findall(r"→ `/foreman:([\w-]+)`", rules):
            self.assertNotIn(name, USER_ONLY)

    def test_plain_requests_rank_their_own_skill_first_by_description_overlap(self):
        # T-1704: a static stand-in for "would Claude pick this skill": rank every model-invocable description by
        # distinct shared words with the request. The intended skill must win outright, with no tie.
        stop = set("a an and are as at be by do for from have i in is it its me my of on or the this that to up we "
                   "what when whenever with you your use about into out not so than then them there these they".split())

        def words(text):
            return {w.rstrip("s") for w in re.findall(r"[a-z]{2,}", text.lower()) if w not in stop}

        skills_dir = os.path.join(PLUGIN, "skills")
        desc = {}
        for name in sorted(os.listdir(skills_dir)):
            path = os.path.join(skills_dir, name, "SKILL.md")
            if os.path.isfile(path):
                meta, _ = frontmatter(path)
                if meta.get("disable-model-invocation") != "true":
                    desc[name] = words(meta.get("description", ""))
        corpus = json.loads(read_text(os.path.join(os.path.dirname(__file__), "fixtures", "skill_triggers.json")))
        for name in desc:
            with self.subTest(skill=name):
                self.assertGreaterEqual(
                    len(corpus.get(name, [])), 3,
                    f'plugin/tests/fixtures/skill_triggers.json needs "{name}": [three or more plain requests a user '
                    f"would type that this skill should answer] (T-1704)")
        for name, requests in corpus.items():
            if name not in desc:
                continue  # user-only or removed skills may keep entries; they are not ranked
            for req in requests:
                with self.subTest(skill=name, request=req):
                    w = words(req)
                    scores = sorted(((len(w & d), n) for n, d in desc.items()), reverse=True)
                    self.assertEqual(scores[0][1], name, f"{req!r} ranks {scores[:3]}")
                    self.assertGreater(scores[0][0], scores[1][0], f"{req!r} ties {scores[:3]}")

    def test_the_listing_foreman_adds_stays_small(self):
        # T-1253: Claude Code 2.1.304 sends the skill listing again after every compaction, so Foreman's share of it
        # (model-visible skill and command descriptions, workflow descriptions) is paid once per compaction
        total = 0
        for kind in ("skills", "commands"):
            for path in [os.path.join(d, "SKILL.md") for d in
                         (os.path.join(PLUGIN, "skills", n) for n in os.listdir(os.path.join(PLUGIN, "skills")))
                         if os.path.isfile(os.path.join(d, "SKILL.md"))] if kind == "skills" else \
                    [os.path.join(PLUGIN, "commands", n) for n in os.listdir(os.path.join(PLUGIN, "commands"))
                     if n.endswith(".md")]:
                meta, _ = frontmatter(path)
                if meta.get("disable-model-invocation") != "true":
                    total += len(meta.get("description", ""))
        for name in os.listdir(os.path.join(PLUGIN, "workflows")):
            text = read_text(os.path.join(PLUGIN, "workflows", name))
            total += sum(len(m) for m in re.findall(r"(?m)^\s*(?:description|whenToUse): '([^']*)'", text))
        self.assertLessEqual(total, 2200, "Foreman's part of the skill listing")  # T-1700/T-1701: four job skills

    def test_the_rules_carry_the_reply_format_and_stay_small(self):
        # T-1279: the rules ride once a session; the output style's reminder rode every turn
        path = os.path.join(PLUGIN, "rules", "foreman.md")
        text = read_text(path)
        self.assertIn("## Replies", text)
        self.assertLess(os.path.getsize(path), 6800)

    def test_skill_references_exist(self):
        for name in SKILLS:
            body = read_text(os.path.join(PLUGIN, "skills", name, "SKILL.md"))
            for ref in re.findall(r"`((?:\.\./[\w-]+/)?references/[\w./-]+\.md)`", body):  # ../playbooks/…: a sibling's
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue(os.path.exists(os.path.join(PLUGIN, "skills", name, ref)))

    def test_the_job_skills_are_short_and_name_only_real_playbooks_and_verbs(self):
        # T-1701: debug-test, release and research wrap playbooks and fm verbs that exist, and fire on task words
        import fmdoctor
        self.assertEqual(fm_mention_problems("`fm nosuch` `fm lane nosuch ID` `fm lane brief ID` `fm task hypo ID add`"),
                         ["fm nosuch", "fm lane nosuch"], "the checker itself")
        jobs, chars = ("debug-test", "release", "research"), 0
        for name in jobs:
            with self.subTest(skill=name):
                meta, body = frontmatter(os.path.join(PLUGIN, "skills", name, "SKILL.md"))
                self.assertEqual(meta.get("name"), name)
                self.assertTrue(meta.get("description", "").startswith("Use whenever "), "task words, not Foreman's")
                self.assertNotEqual(meta.get("disable-model-invocation"), "true")
                chars += len(meta["description"])
                self.assertLess(len(body.splitlines()), 60)
                refs = re.findall(r"`((?:\.\./[\w-]+/)?references/[\w./-]+\.md)`", body)
                self.assertTrue(refs, "wraps at least one playbook")
                for ref in refs:
                    self.assertTrue(os.path.exists(os.path.join(PLUGIN, "skills", name, ref)), ref)
                self.assertIn("`fm ", body, "wraps at least one fm verb")
                self.assertEqual(fm_mention_problems(body), [])
        self.assertLessEqual(chars, 360, "three of the 2,200-character listing's job-skill room")
        self.assertEqual([p for p in fmdoctor._description_problems(os.path.join(PLUGIN, "skills"))
                          if any(j in p for j in jobs)], [])

    def test_the_directions_skill_offers_six_measured_cards_and_saves_the_pick(self):
        # T-1508: one sentence in, six distinct one-screen directions out, the pick saved as DESIGN.md with an
        # audacity level; the worked example is held to the card format and its stated contrasts are measured
        import fmcodetui
        body = read_text(os.path.join(PLUGIN, "skills", "directions", "SKILL.md"))
        for word in ("six", "DESIGN.md", "audacity", "AskUserQuestion", "fm decide", "runner-up",
                     "`../playbooks/references/ui/design-direction.md`", "references/cards.md"):
            self.assertIn(word, body)
        cards = read_text(os.path.join(PLUGIN, "skills", "directions", "references", "cards.md"))
        for default in ("terracotta", "acid", "hairline", "card kit", "template chrome"):
            self.assertIn(default, cards, "the generic defaults the six must avoid")
        example = cards.split("\n## Example", 1)[1]
        self.assertEqual(len(re.findall(r"(?m)^### [1-6]\. ", example)), 6)
        for field in ("Feels like:", "Palette:", "Type:", "Layout:", "Motion:", "Signature move:", "Audacity:",
                      "Fits because:"):
            self.assertEqual(len(re.findall(rf"(?m)^- \*\*{field}\*\*", example)), 6, field)
        self.assertEqual(len(set(re.findall(r"(?m)^- \*\*Audacity:\*\* (safe|bold|wild)", example))), 3)
        stated = re.findall(r"(#[0-9A-F]{6}) on (#[0-9A-F]{6}) ([\d.]+):1", example)
        self.assertGreaterEqual(len(stated), 6)
        for fg, bg, ratio in stated:
            with self.subTest(pair=(fg, bg)):
                got = fmcodetui.contrast(fg, bg)
                self.assertAlmostEqual(got, float(ratio), delta=0.05)
                self.assertGreaterEqual(got, 4.5)

    def test_the_ui_design_skill_routes_to_real_playbooks_and_verbs(self):
        # T-1700: one job skill for UI, motion and 3D work; every playbook and fm verb it names exists
        body = read_text(os.path.join(PLUGIN, "skills", "ui-design", "SKILL.md"))
        self.assertLess(len(body.splitlines()), 100)
        for ref in ("design-direction", "type-and-colour", "composition", "motion", "scene-3d", "visual-qa"):
            self.assertIn(f"`../playbooks/references/ui/{ref}.md`", body)
        named = set(re.findall(r"`fm ([\w-]+)", body))
        for need in ("design", "scene", "motion", "looks", "page", "img", "new"):
            self.assertIn(need, named)
        self.assertEqual(fm_mention_problems(body), [])  # T-1701: the checker every skill test shares
        self.assertIn("Skill foreman:directions", body)
        # T-1714: palette writes --out (it was ignored before); extract writes DESIGN.md's Tokens section unless --out
        palette = next(line for line in body.splitlines() if "fm design palette" in line)
        self.assertRegex(palette, r"`fm design palette \S+ --out \S+`")
        self.assertRegex(body, r"`fm design extract SRC`[^.]*DESIGN\.md")

    def test_audit_reference_defines_every_lens_fm_requires(self):
        import fmcore as c
        body = read_text(os.path.join(PLUGIN, "skills", "intake", "references", "audit.md"))
        for lens in c.AUDIT_LENSES:
            with self.subTest(lens=lens):
                self.assertIn(f"**{lens}**", body)
        for tier in ("S", "M", "L"):
            self.assertIn(f"| {tier} |", body)
        self.assertIn("references/audit.md", read_text(os.path.join(PLUGIN, "skills", "intake", "SKILL.md")))

    # the playbook index rule (T-1569: SKILL.md or the stage's INDEX.md) is fm check playbooks' (test_playbook_check)

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


class PluginParity(unittest.TestCase):
    """T-1520: every user-facing fm verb is reachable from a Claude Code session, not only from fm code: named in the
    plugin's rules, commands or skills, or found by fm which (which the rules point at)."""

    def test_every_user_facing_verb_is_reachable(self):
        import glob
        import sys
        sys.path.insert(0, os.path.join(PLUGIN, "lib"))
        import fmwhich
        src = read_text(os.path.join(PLUGIN, "lib", "fmcli.py"))
        tiers = {m.group(1): m.group(2) for m in re.finditer(
            r'\badd\("([a-z][\w-]*)"[^\n]*?(?:\n[^\n]*?){0,6}?tier=\("([^"]+)"', src)}
        docs = "".join(read_text(p) for p in glob.glob(os.path.join(PLUGIN, "commands", "*.md"))
                       + glob.glob(os.path.join(PLUGIN, "skills", "*", "SKILL.md"))
                       + glob.glob(os.path.join(PLUGIN, "skills", "*", "references", "*.md"))
                       + [os.path.join(PLUGIN, "rules", "foreman.md")])
        indexed = {x["name"] for x in fmwhich.commands()}
        lost = [v for v, tier in sorted(tiers.items()) if not tier.startswith("Internal")
                and v not in indexed | fmwhich.SELF | fmwhich.FOREMAN_ONLY and not re.search(rf"\bfm {v}\b", docs)]
        self.assertEqual(lost, [], "verbs a Claude Code session can't find")
        self.assertGreater(len(tiers), 100, "the tier parse found the verbs")
        rules = read_text(os.path.join(PLUGIN, "rules", "foreman.md"))
        self.assertRegex(rules, r"fm which", "the rules point a session at fm which")


class CodeExamples(unittest.TestCase):  # T-1353
    """Every `fm code …` example in README's Foreman Code section parses with fm's own parser to the code verb, so
    a renamed or removed flag can't linger in the docs."""
    FILL = ((r"\[NAME\]", "claude"), (r"\bID\b", "T-0001"), (r"\bUSD\b", "1"), (r"\bN\b", "1"))

    def examples(self):
        text = read_text(os.path.join(os.path.dirname(PLUGIN), "README.md"))
        section = re.search(r"(?ms)^### Foreman Code.*?(?=^### |\Z)", text).group(0)
        return sorted(set(re.findall(r"`(fm code[^`]*)`", section)))

    def parse(self, example):
        import contextlib
        import io
        import shlex
        import fmcli
        line = example.split(" > ")[0]  # a shell redirect isn't fm's
        for pat, value in self.FILL:
            line = re.sub(pat, value, line)
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                return fmcli.build_parser().parse_args(shlex.split(line)[1:])
        except SystemExit:
            return None

    def test_every_fm_code_example_parses_to_the_code_verb(self):
        found = self.examples()
        self.assertGreater(len(found), 10, found)
        self.assertEqual([x for x in found if getattr(self.parse(x), "cmd", None) != "code"], [])
        self.assertIsNone(self.parse("fm code runners --made-up-flag"), "a flag fm doesn't have fails")


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

    def test_master_lists_every_lib_module_with_its_own_bullet(self):
        # T-1724: MASTER.md's '### plugin/lib modules' is one bullet per module (T-1713); a new module needs its line
        text = read_text(os.path.join(os.path.dirname(PLUGIN), "MASTER.md"))
        self.assertIn("\n### plugin/lib modules\n", text)
        section = re.split(r"\n#", text.split("\n### plugin/lib modules\n", 1)[1], maxsplit=1)[0]
        bullets = re.findall(r"^- `(\w+)`", section, re.M)
        modules = {f[:-3] for f in os.listdir(os.path.join(PLUGIN, "lib")) if f.endswith(".py")}
        self.assertEqual(sorted(modules - set(bullets)), [], "a module with no bullet")
        self.assertEqual(sorted(set(bullets) - modules), [], "a bullet for no module")
        self.assertEqual(sorted({b for b in bullets if bullets.count(b) > 1}), [], "a module with two bullets")


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

    def test_the_fm_code_page_shows_each_real_example(self):
        # T-1320: each card is a recorded fm code run (its own events, every one timed), not a made-up one
        build = self._site("build")
        html = build.examples_html()
        self.assertGreaterEqual(len(build.EXAMPLES), 6)
        for name, _ in build.EXAMPLES:
            ex = build.load_example(os.path.join(self.ROOT, "demo", "examples", name + ".jsonl"))
            self.assertEqual(ex["events"][0].get("event"), "start", name)
            self.assertTrue(all(isinstance(e.get("ts"), (int, float)) for e in ex["events"]), name)
            self.assertIn(ex["end"], ("closed", "answer"), f"{name} ended {ex['end']}: {ex['end_text'][:200]}")
            self.assertIn(f'id="ex-{name}"', html)
            self.assertIn(build.esc(ex["request"]), html)

    def test_the_build_refuses_to_wipe_the_repo_its_source_or_home(self):
        # site review: build.py OUT ran shutil.rmtree on whatever it was given (python3 site/build.py . wiped the repo)
        build = self._site("build")
        for bad in (self.ROOT, os.path.join(self.ROOT, "site"), os.path.expanduser("~"), "/", os.path.dirname(self.ROOT)):
            self.assertFalse(build.safe_out(bad), bad)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(build.safe_out(os.path.join(tmp, "_site")))
        self.assertTrue(build.safe_out(os.path.join(self.ROOT, "_site")))

    def test_an_option_is_never_taken_as_the_output_folder(self):
        # T-1371: `python3 site/build.py --check` built into a folder named --check, which then got committed
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, os.path.join(self.ROOT, "site", "build.py"), "--check"], cwd=tmp,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("usage", r.stderr)
            self.assertEqual(os.listdir(tmp), [], "nothing written")

    def test_the_build_fails_on_a_page_that_loads_an_outside_host(self):
        # T-1411: every page pulled Google Fonts, against nothing leaving the machine; the real site's build (the test
        # below) exits 0, so its pages load no outside host
        import shutil
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(os.path.join(self.ROOT, "site"), os.path.join(tmp, "site"),
                            ignore=shutil.ignore_patterns("__pycache__"))
            for d in ("demo", "plugin"):
                os.symlink(os.path.join(self.ROOT, d), os.path.join(tmp, d))
            with open(os.path.join(tmp, "site", "fixture.html"), "w", encoding="utf-8") as f:
                f.write('<link href="https://fonts.googleapis.com/css2?family=Barlow" rel="stylesheet">')
            r = subprocess.run([sys.executable, os.path.join(tmp, "site", "build.py"), os.path.join(tmp, "out")],
                               capture_output=True, text=True, timeout=120)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertIn("fixture.html: https://fonts.googleapis.com/css2?family=Barlow", r.stderr)

    def test_what_counts_as_loading_an_outside_host(self):
        # T-1411: what the browser fetches counts (src, srcset, a link's href, CSS url() and @import, a script's URL);
        # a link to follow, a URL in the text, the site's own host and an SVG namespace don't
        build = self._site("build")
        bad = ['<img src="https://x.test/a.png">', "<script src=//x.test/a.js></script>", '<LINK HREF="//x.test/f">',
               '<img srcset="a.png 1x, https://x.test/b.png 2x">', '<video poster="http://x.test/p.jpg"></video>',
               '<svg><image href="https://x.test/i.png"/></svg>', '<svg><use xlink:href="https://x.test/s.svg#a"/></svg>',
               '<div style="background:url(\'//x.test/bg.png\')"></div>', '<style>@import "https://x.test/c.css";</style>',
               '<script>fetch("https://x.test/collect")</script>', '<img src="https:\\\\x.test/a.png">',
               '<link rel="preconnect" href="https://x.test">', '<a href="#top" ping="https://x.test/p">top</a>']
        for page in bad:
            self.assertEqual(len(build.outside_loads(page, ".html")), 1, page)
        self.assertTrue(build.outside_loads("body { background: url(https://x.test/a.png) }", ".css"))
        self.assertTrue(build.outside_loads('fetch("https://x.test/a")', ".js"))
        good = ['<a href="https://github.com/ChaseSunstrom/foreman">Source</a>', "<code>curl https://x.test/i.sh</code>",
                '<svg xmlns="http://www.w3.org/2000/svg"><a href="https://x.test">x</a></svg>',
                '<meta property="og:image" content="https://x.test/poster.jpg">', '<img src="assets/a.png">',
                '<link rel="icon" href="https://chasesunstrom.github.io/foreman/assets/foreman.svg">',
                '<img src="data:image/png;base64,iVBOR//x.test">', '<script>// see //x.test\nvar a = 1;</script>']
        for page in good:
            self.assertEqual(build.outside_loads(page, ".html"), [], page)
        self.assertEqual(build.outside_loads(".a { marker-end: url(#arrow) } /* https://x.test */", ".css"), [])

    def test_where_foreman_loses_is_generated_with_a_rerun_per_row(self):  # T-1261
        pages, stats = self._site("pages"), self._site("stats")
        side = lambda ok, cost, secs: {"pass": ok, "cost": cost, "seconds": secs, "runs": 1, "passed": int(ok)}
        duels = {"duels": [{"name": "hard", "label": "duel-none-foreman-1", "cases": [
            {"case": "wrap", "id": "c1", "foreman": side(False, 0.1, 10), "bare": side(True, 0.1, 10)},
            {"case": "<ini>", "id": "c2", "foreman": side(True, 0.30, 10), "bare": side(True, 0.20, 10)},
            {"case": "lru", "id": "c3", "foreman": side(True, 0.1, 10), "bare": side(True, 0.1, 10)}]}]}
        html = pages._loses(duels)
        self.assertIn("2 row(s) where Foreman did worse", html)
        self.assertIn("Claude Code passed, Foreman didn&#x27;t", html)  # escaped, as every cell
        self.assertIn("cost 50% higher", html)
        self.assertIn("fm bench repro duel-none-foreman-1 c1", html)
        self.assertIn("&lt;ini&gt;", html)
        self.assertNotIn(">lru<", html)
        self.assertIn("lost no row", pages._loses({"duels": [{"name": "q", "cases": [duels["duels"][0]["cases"][2]]}]}))
        import shutil
        import tempfile
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        state = os.path.join(tmp, "state")
        res = os.path.join(state, "bench", "results")
        os.makedirs(res)
        for arm in ("foreman", "bare"):
            with open(os.path.join(res, f"duel-none-{arm}-20261023.json"), "w") as f:
                json.dump({"model": "haiku", "cases": [{"id": "c9", "pass": True, "cost_usd": 0.1}]}, f)
        d = stats.duel(state)
        self.assertEqual((d["label"], d["cases"][0]["id"]), ("duel-none-foreman-20261023", "c9"))

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
        same = pages._long({"duels": [{"name": "long", "cases": [{"case": "x", "foreman": side(105, 0),
                                                                  "bare": side(105, 0)}]}]}, "long")
        self.assertNotIn("105, 105", same)
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
        stats = read_json(os.path.join(self.ROOT, "site", "data", "stats.json"))
        stats.update(read_json(os.path.join(self.ROOT, "site", "data", "bench.json")))
        text = body(stats)
        for words in ("24 dangerous", "both sides pass", "more", "6 of 6", "3 of 6", "compact"):
            self.assertIn(words, text)

    def test_the_why_section_is_computed_from_the_data(self):
        # T-1246: the figures were typed into the prose and could drift from the charts beside them
        pages = self._site("pages")
        side = lambda ok, cost, secs: {"pass": ok, "cost": cost, "seconds": secs, "runs": 3, "passed": 3}
        long_ = lambda f, b, fc, bc: {"model": "haiku", "runs": 3, "f_pass": f, "b_pass": b, "f_cost": fc, "b_cost": bc}
        stats = {"safety": {"dangerous": [{"decision": "deny"}] * 7 + [{"decision": "saved"}] * 2,
                            "everyday": [{"decision": "allow"}] * 11},
                 "duels": [{"name": "quality", "cases": [{"foreman": side(True, 0.6, 10), "bare": side(True, 0.5, 10)}]},
                           {"name": "hard-haiku", "cases": [{"foreman": side(True, 0.15, 15),
                                                             "bare": side(True, 0.1, 10)}]},
                           {"name": "long", "history": [long_(3, 1, 0.3, 0.2), long_(2, 2, 0.3, 0.2)], "cases": [{}]}]}
        _, _, body = next(p for p in pages.PAGES if p["slug"] == "benchmarks")["blocks"][0]
        text = body(stats)
        for words in ("9 dangerous", "stopped 7", "other 2", "none of 11", "20% more with Sonnet",
                      "50% more with Haiku", "5 of 6", "3 of 6", "50% more there"):
            self.assertIn(words, text)
        # T-1254: per session that passed every test, Foreman cost 1.8 / 5 = $0.360 and Claude Code 1.2 / 3 = $0.400
        self.assertIn("$0.360 against $0.400", text)
        self.assertIn("10% less per fully correct session", text)
        stats["duels"][2]["history"] = [long_(3, 0, 0.3, 0.2)]
        self.assertIn("Claude Code alone never passed every test", body(stats))

    def test_each_duel_names_the_claude_code_it_ran_on(self):
        # T-1255
        pages, stats = self._site("pages"), self._site("stats")
        side = {"pass": True, "cost": 0.1, "seconds": 5, "runs": 1, "passed": 1}
        s = {"duels": [{"name": "quality", "claude": "2.1.304", "cases": [{"case": "a", "foreman": side, "bare": side}]},
                       {"name": "hard", "cases": [{"case": "a", "foreman": side, "bare": side}]}]}
        self.assertIn("Claude Code 2.1.304", pages._duel(s, "quality"))
        self.assertIn("Claude Code version wasn't recorded", pages._duel(s, "hard"))
        import tempfile
        with tempfile.TemporaryDirectory() as state:
            res = os.path.join(state, "bench", "results")
            os.makedirs(res)
            case = {"id": "x", "pass": True, "cost_usd": 0.1}
            for arm, extra in (("foreman", {"claude": "2.1.304"}), ("bare", {})):
                with open(os.path.join(res, f"duel-none-{arm}-1.json"), "w") as f:
                    json.dump(dict(extra, model="haiku", cases=[case]), f)
            self.assertEqual(stats.duel(state)["claude"], "2.1.304")

    def test_the_foreman_code_page_counts_come_from_the_repo(self):
        stats = self._site("stats")
        counts = stats.code_counts()
        self.assertEqual(counts["model_tests"], len(re.findall(r"(?m)^    def test_", read_text(
            os.path.join(self.ROOT, "plugin", "tests", "test_models.py")))))
        self.assertGreater(counts["endpoints"], 5)

    def test_the_saved_theme_is_set_before_first_paint(self):
        build = self._site("build")
        head = build.layout("T", "d", "<p>x</p>", [], "x").split("</head>")[0]
        self.assertIn("fm-theme", head, "a stored light theme flashed dark until site.js ran at the end of body")

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
                head = page.split("</head>")[0]  # T-1244: every page sets the stored theme before <body>
                self.assertIn('getItem("fm-theme")', head, os.path.relpath(path, out))
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


def _fm_temp(tmp, *args):
    """fm from this checkout with a temporary HOME, Foreman home and state: nothing of the user's."""
    import subprocess
    import sys
    env = {k: v for k, v in os.environ.items() if not k.startswith(("FOREMAN_", "CLAUDE"))}
    env.update(HOME=tmp, FOREMAN_HOME=os.path.join(tmp, "fh"), XDG_STATE_HOME=os.path.join(tmp, "xdg"),
               FOREMAN_NO_BACKGROUND="1")
    return subprocess.run([sys.executable, os.path.join(PLUGIN, "bin", "fm"), *args], cwd=tmp, env=env,
                          capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)


class Fences(unittest.TestCase):
    """T-1519: the command fences README.md and MASTER.md mark runnable (```bash runnable) run green in a temporary
    home, and each template fm new copies passes its own check."""
    ROOT = Site.ROOT
    _site = Site._site

    def fixture(self, tmp, text):
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as f:
            f.write(text)

    def test_the_documented_runnable_fences_run_green_in_a_temp_home(self):
        import fmdemo
        found = fmdemo.fences()
        self.assertEqual({w.split(":")[0] for w, _ in found}, {"README.md", "MASTER.md"}, "each doc marks one")
        self.assertEqual(fmdemo.run_fences(), [])

    def test_a_failing_fence_is_named_and_runs_away_from_the_real_home(self):
        import tempfile
        import fmdemo
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(tmp, "Prose.\n\n```bash\nexit 3\n```\n\n```bash runnable\n"
                              "cat\necho \"in its folder: ${HOME#$PWD/} ${FOREMAN_HOME#$PWD/} ${FOREMAN_STATE#$PWD/}"
                              " ${TMPDIR#$PWD/}\" >&2\ntest -d \"$TMPDIR\"\nexit 4\n```\n")
            fails = fmdemo.run_fences(tmp, timeout=20)
        self.assertEqual(len(fails), 1, "an unmarked fence never runs")
        # cat met a closed stdin (no hang); HOME, Foreman's home, state and TMPDIR all sit in the fence's own folder
        self.assertEqual(fails[0], "README.md:7: fence exited 4: in its folder: home foreman foreman/state tmp")

    def test_a_hung_fence_is_stopped(self):
        import tempfile
        import fmdemo
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(tmp, "~~~sh runnable\nsleep 30\n~~~\n")
            self.assertEqual(fmdemo.run_fences(tmp, timeout=1), ["README.md:1: timed out after 1 s"])

    def test_each_template_passes_its_own_check(self):
        import fmnew
        build = self._site("build")
        self.assertEqual(set(fmnew.TEMPLATES), {"web", "scene", "panel"})
        for name in fmnew.TEMPLATES:
            path = fmnew.source(name)
            self.assertTrue(os.path.isfile(path), path)
            self.assertEqual(fmnew.check(path, run=True), [], name)  # run: the shipped panel sits in Foreman's repo
            if path.endswith(".html"):  # and loads nothing from another host
                self.assertEqual(build.outside_loads(read_text(path), ".html"), [], name)

    def test_the_checks_catch_a_template_gone_loose(self):
        import tempfile
        import unittest.mock
        import fmnew
        with tempfile.TemporaryDirectory() as tmp:
            page = os.path.join(tmp, "index.html")
            with open(page, "w", encoding="utf-8") as f:
                f.write(re.sub(r"--font-(\w+):[^;]+;", r"--font-\1: Inter, sans-serif;", read_text(fmnew.source("web")))
                        .replace("var(--font-body)", "Inter, sans-serif").replace("var(--font-display)", "Inter"))
            self.assertIn("generic-font", " ".join(fmnew.check(page)))
            panels = {"wide": "lambda st, w, h, app: [[('x' * (w + 1), 'text')]]",
                      "lines": "lambda st, w, h, app: [[('x', 'text')]] * (h + 1)",
                      "style": "lambda st, w, h, app: [[('x', 'purple')]]",
                      "ZeroDivisionError": "lambda st, w, h, app: 1 / 0",
                      " ms": "lambda st, w, h, app: __import__('time').sleep(0.12) or []"}
            for want, fn in panels.items():
                path = os.path.join(tmp, "p.py")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"def setup(api):\n    api.panel('p', 'P', {fn})\n")
                self.assertIn(want, " ".join(fmnew.check(path)), want)
            with open(path, "w", encoding="utf-8") as f:
                f.write("def setup(api):\n    raise RuntimeError('boom')\n")
            self.assertIn("boom", " ".join(fmnew.check(path)))
            self.assertFalse(os.path.exists(os.path.join(tmp, "__pycache__")), "a check writes nothing beside it")

    def test_a_panel_that_quits_or_hangs_never_passes(self):
        # the check runs in a child (limits, a timeout, a process-group kill): nothing the file does ends it early green
        import tempfile
        import unittest.mock
        import fmnew
        draw = "def setup(api):\n    api.panel('p', 'P', draw)\n\n\ndef draw(st, w, h, app):\n"
        files = {"sys.exit(0)": "import sys\nsys.exit(0)\n",  # at import
                 "sys.exit(0) ": draw + "    __import__('sys').exit(0)\n",  # while drawing
                 "timed out": draw + "    while True:\n        try:\n            __import__('time').sleep(5)\n"
                                     "        except:  # noqa: E722\n            pass\n",
                 "timed out ": "import signal\nsignal.alarm(0)\n" + draw + "    while True:\n        pass\n",
                 "ended before the check finished": draw + "    print('[]')\n    __import__('os')._exit(0)\n"}
        with tempfile.TemporaryDirectory() as tmp, unittest.mock.patch.object(fmnew, "CHECK_SECONDS", 2):
            for want, body in files.items():
                path = os.path.join(tmp, "p.py")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(body)
                found = fmnew.check(path)
                self.assertEqual(len(found), 1, (want, found))
                self.assertIn(want.strip(), found[0], want)

    def test_a_panel_check_runs_only_what_fm_code_would(self):
        import subprocess
        import tempfile
        import fmnew
        good = "def setup(api):\n    api.panel('p', 'P', lambda st, w, h, app: [])\n"
        with tempfile.TemporaryDirectory() as tmp:
            loose = os.path.join(tmp, "loose.py")
            with open(loose, "w", encoding="utf-8") as f:
                f.write(good)
            os.chmod(loose, 0o664)
            self.assertIn("another user can change it", " ".join(fmnew.check(loose, run=True)))
            repo = os.path.join(tmp, "repo")
            subprocess.run(["git", "init", "-q", repo], check=True)
            mark, inside = os.path.join(tmp, "ran"), os.path.join(repo, "tools", "p.py")
            os.makedirs(os.path.dirname(inside))
            with open(inside, "w", encoding="utf-8") as f:
                f.write(f"open({mark!r}, 'w').close()\n" + good)
            found = fmnew.check(inside)
            self.assertIn("--run", " ".join(found))
            self.assertFalse(os.path.exists(mark), "a project's file never ran")
            p = _fm_temp(tmp, "new", "check", inside)
            self.assertEqual(p.returncode, 1, p.stdout)
            self.assertFalse(os.path.exists(mark))
            p = _fm_temp(tmp, "new", "check", inside, "--run")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertTrue(os.path.exists(mark), "with --run it does")
            self.assertIn("runs the file", " ".join(_fm_temp(tmp, "new", "-h").stdout.split()))

    def test_fm_new_lists_copies_and_never_overwrites(self):
        import tempfile
        import fmnew
        with tempfile.TemporaryDirectory() as tmp:
            p = _fm_temp(tmp, "new", "templates", "list")
            self.assertEqual(p.returncode, 0, p.stderr)
            for name in ("web", "scene", "panel"):
                self.assertRegex(p.stdout, rf"(?m)^\s*{name}\b")
            p = _fm_temp(tmp, "new", "web", "site")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(read_text(os.path.join(tmp, "site", "index.html")), read_text(fmnew.source("web")))
            p = _fm_temp(tmp, "new", "web", "site")
            self.assertEqual(p.returncode, 1, "a second copy never overwrites the first")
            self.assertIn("--force", p.stderr)
            p = _fm_temp(tmp, "new", "panel")
            self.assertEqual(p.returncode, 0, p.stderr)
            panel = os.path.join(tmp, "fh", "tui", "panel.py")  # where fm code loads extensions from
            self.assertTrue(os.path.isfile(panel), p.stdout)
            p = _fm_temp(tmp, "new", "check", os.path.join(tmp, "site", "index.html"), panel)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            p = _fm_temp(tmp, "new", "nope")
            self.assertEqual(p.returncode, 1)
            self.assertIn("web", p.stderr)
            os.makedirs(os.path.join(tmp, "s2"))  # a link planted where the copy lands, pointing nowhere yet
            link, target = os.path.join(tmp, "s2", "index.html"), os.path.join(tmp, "elsewhere.html")
            os.symlink(target, link)
            self.assertEqual(_fm_temp(tmp, "new", "web", "s2").returncode, 1, "a link there counts as a file")
            p = _fm_temp(tmp, "new", "web", "s2", "--force")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertFalse(os.path.islink(link) or os.path.exists(target), "the link replaced, not written through")


class HelpAnswers(unittest.TestCase):
    """T-1519: 'can Foreman do X?' is answered from fm help: the commands whose help says so, or a plain no."""

    def test_the_commands_whose_help_answers_the_question(self):
        import fmrecall
        self.assertEqual(fmrecall.can("Can Foreman scaffold an MCP server?")[0][0], "mcp")
        self.assertEqual(fmrecall.can("can it start me from a web page template")[0][0], "new")
        self.assertEqual(fmrecall.can("can foreman bake a cake"), [])
        self.assertEqual(fmrecall.can("can foreman do it?"), [], "a question of stop words names nothing")

    def test_fm_help_with_words_answers_and_says_no_plainly(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = _fm_temp(tmp, "help", "can", "foreman", "notify", "me", "when", "a", "run", "finishes?")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("fm notify", p.stdout)
            p = _fm_temp(tmp, "help", "bake", "a", "cake")
            self.assertEqual(p.returncode, 1)
            self.assertIn("fm help --all", p.stdout)
            p = _fm_temp(tmp, "help", "can", "foreman", "scaffold", "an", "mcp", "server")
            self.assertTrue(all(len(ln) <= 100 for ln in p.stdout.splitlines()), p.stdout)
            self.assertIn("scaffold", next(ln for ln in p.stdout.splitlines() if "fm mcp" in ln), "the matched words")
            p = _fm_temp(tmp, "help", "--all", "scaffold")
            self.assertEqual(p.returncode, 1, "--all lists everything; words ask a question: not both")
            self.assertIn("--all", p.stderr)
            p = _fm_temp(tmp, "help", "can", "it", "do", "that?")
            self.assertEqual(p.returncode, 1)
            self.assertIn("nothing to look up", p.stderr)


class CardDates(unittest.TestCase):
    """T-1519: a library card may carry `verified: YYYY-MM-DD`, the day someone ran its Verify commands; fm lib check
    holds the field to a real, past date and notes one over a year old."""

    def test_a_verified_date_is_held_to_a_real_past_day(self):
        import datetime
        import tempfile
        import fmlib
        card = read_text(os.path.join(fmlib.CARDS, "tools", "jq.md"))
        today = datetime.date.today()
        cases = {"2026-13-01": "not a date", (today + datetime.timedelta(days=2)).isoformat(): "in the future",
                 "2020-01-01": None, today.isoformat(): None,
                 (today + datetime.timedelta(days=1)).isoformat(): None}  # a day ahead: another time zone's today
        for value, problem in cases.items():
            with tempfile.TemporaryDirectory() as tmp:
                os.makedirs(os.path.join(tmp, "tools"))
                with open(os.path.join(tmp, "tools", "jq.md"), "w", encoding="utf-8") as f:
                    bare = re.sub(r"(?m)^verified:.*\n", "", card)
                    f.write(bare.replace("\n---\n", f"\nverified: {value}\n---\n", 1))
                problems, notes = fmlib.lint(tmp)
                if problem:
                    self.assertEqual(len(problems), 1, problems)
                    self.assertIn(problem, problems[0])
                else:
                    self.assertEqual(problems, [], value)
                self.assertEqual(any("over a year ago" in n for n in notes), value == "2020-01-01", notes)

    def test_fm_lib_show_says_when_a_card_was_verified(self):
        import tempfile
        import fmlib
        dated = [x for x in fmlib.cards() if x.get("verified")]
        self.assertTrue(dated, "at least one card has been verified")
        with tempfile.TemporaryDirectory() as tmp:
            p = _fm_temp(tmp, "lib", "show", dated[0]["name"])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn(f"Verified {dated[0]['verified']}", p.stdout)


if __name__ == "__main__":
    unittest.main()
