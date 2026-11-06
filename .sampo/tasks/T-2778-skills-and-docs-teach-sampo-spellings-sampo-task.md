---
id: T-2778
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T04:57:12Z
updated: 2026-11-03T22:01:29Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (590) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T21:06:10Z
rival_split: true
builder_model: haiku
route_probe: 1
base: 8f8da4f673f3089040922dcc0ebbf5daea680774
base_tree: a483dd2ab993b03032035d6e53c0cb5ee02ccd12
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-03T21:06:44Z
plan0_scope: []
lane_stop: merged 2026-11-03T21:52:18Z
verified: strong
unproven: [docs]
---
# Skills and docs teach sampo spellings (sampo task new, sampo check …) once every hook…
## Raw request
> FEATURE: skills and docs teach sampo spellings (sampo task new, sampo check …) once every hook pattern that matches an fm command (gate-pipe, finish detection, evidence parsing, guard verbs) matches sampo too; a test greps hooks.py/core.py/fmguard.py for fm-only command regexes first (T-2742 step 5, after T-2768)
## Interpretation
SAMPO.md: sampo is the command and fm the compatibility alias. Docs and skills still teach fm spellings, so every session copies fm. Switch the taught spelling to sampo once the hooks treat both alike. The hooks already share FM_NAME_RE ('(?:fm|sampo)') and _GATE_PIPE matches both, so step 1 is a test proving no fm-only command regex remains. Reading 2: rename every fm token in the docs, including code examples of the guard's own refusal text and the fm-* agent names; ruled out because agent ids and quoted program output must match what runs.
## Assumptions (confidence)
## Acceptance criteria
- [x] a test finds no regex in hooks.py, core.py or fmguard.py that matches an fm command spelling without also matching sampo (agent names like fm-reviewer excepted) — verify with `python3 plugin/tests/run.py test_rename_scan`
- [x] skills, commands, agents, the output style, rules, README, MASTER and INSTALL teach sampo spellings (sampo task new, sampo check …), with one line each in README and INSTALL saying fm still works; a ratchet counts fm command spellings left on those surfaces and only goes down — verify with `python3 plugin/tests/run.py test_rename_scan test_docs`
## Non-goals
## Approach (options → choice → why)
1) A test scans hooks.py, core.py and fmguard.py regex literals for an fm command spelling that lacks sampo; then a mechanical rewrite of 'fm <verb>' to 'sampo <verb>' on the doc surfaces (skills, commands, agents, output style, rules, README, MASTER, INSTALL), keeping agent ids, file names, paths and quoted output; a ratchet test counts what is left. Likely outcome: sessions learn sampo; fm keeps working. Fails if a hook matches a doc phrase verbatim and the rewrite breaks the match; the suite catches those.
2) Rewrite only the rules file and the top skills (intake, next). Likely outcome: most taught spellings change for a tenth of the diff. Fails if: the remaining skills keep teaching fm and the ratchet can't reach 0.
3) Do less: leave docs on fm until fm's deprecation line has run two releases. Likely outcome: no churn. Fails if: SAMPO.md's 'sampo is the command' is never met in what sessions read.
4) Use what exists: fm sub (the repo's mechanical rewrite verb) for the sweep, fmguard.FM_NAME_RE for any regex the scan flags, and test_rename_scan's SURFACES/KEPT pattern for the ratchet. Likely outcome: no new tooling. Fails if: fm sub can't express 'keep agent ids and quoted output'; then a small script with the same allowlist.

Choice 1 with 4's tools (75%): the rename's scope names every surface; a mechanical pass with a ratchet is the pattern T-2768 used.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py.
## Execution prompt
## Steps
1. [x] test: no fm-only command regex in hooks.py, core.py, fmguard.py
2. [x] rewrite fm <verb> to sampo <verb> on the doc surfaces, keeping ids, paths and quoted output; README and INSTALL say fm still works
3. [x] ratchet: count fm command spellings left on those surfaces, baseline at the new count
## Resume here
<!-- auto -->
- 2026-11-03T21:28:01Z steps 3/3 done
- git: worktree-agent-a31e34a6c2dd6b79d; 149 uncommitted: INSTALL.md, MASTER.md, README.md, plugin/agents/fm-builder.md, plugin/agents/fm-debugger.md, plugin/agents/fm-reproducer.md, plugin/agents/fm-reviewer.md, plugin/commands/backlog.md, plugin/commands/build.md, plugin/commands/looks.md
- touched since last checkpoint: .fm-scratch/edits4.json, plugin/tests/test_docs.py, README.md, plugin/tests/test_playbook_machinery.py, plugin/lib/sampo/doctor.py, .fm-scratch/edits5.json, plugin/evals/guard-force-push/prompt.md, plugin/evals/guard-publish/prompt.md, plugin/evals/intake-block/prompt.md, plugin/evals/mid-task-capture/prompt.md, plugin/evals/one-liner/prompt.md, plugin/rules/foreman.md, plugin/skills/playbooks/ratchet.json, MASTER.md, plugin/agents/fm-builder.md
## Docs impact
README, INSTALL, MASTER, skills, commands, agents, rules, output style
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 6 tests in 1.1s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree afeae328a23c] [world 2f1906870a] (2026-11-03T21:08:18Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_doctor test_docs test_docsdrift test_agents test_brainstorm_skill test_playbook_evals test_playbook_machinery test_playbook_route test_playbook_use test_skillroute test_user_rules test_finish_self_docs test_rename_scan` → exit 0 · Ran 384 tests in 22.3s (103 classes, 16 at a time; slowest: Use 19s, Hook 18s, UserRules 17s) / OK [ran] [tree 20ee9d39c474] [world 2f1906870a] (2026-11-03T21:15:44Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_docs test_doctor test_playbook_check test_playbook_machinery` → exit 0 · Ran 287 tests in 24.0s (81 classes, 16 at a time; slowest: Load 18s, Fences 17s, ViewsRepair 14s) / OK [ran] [tree 20ee9d39c474] [world 2f1906870a] (2026-11-03T21:17:50Z)
- (step 3) `python3 plugin/tests/run.py test_rename_scan test_docs` → exit 0 · Ran 115 tests in 8.4s (26 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree b3a48ff0b05c] [world 2f1906870a] (2026-11-03T21:18:21Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_backlog test_bench_family test_board_export test_board_surfaces test_brainstorm_skill test_builder test_claude test_cli test_context_tax test_core test_cost test_critique test_debug test_design_surfaces test_design_tokens test_diagnosis test_docs test_docsdrift test_doctor test_edit_cards test_exam test_export test_extras test_followups test_foresight test_genesis test_guard test_guard_cases test_guard_mine test_handoff test_hooks test_ideation test_inbox_more test_incident test_judgment test_lanes test_learning2 test_lib_hostile test_lib_source_kill test_library test_map test_mcp test_nudges test_onwrite test_pass1 test_playbook_evals test_playbook_machinery test_playbook_route test_playbook_use test_plugin_parity test_plugins test_release test_rename_scan test_repeats test_replan test_roles test_scaffold test_scene test_scout test_second test_session test_session_fixes test_settings test_settings_power test_settings_safety test_setup test_shade test_ship test_showpieces test_site_gallery test_site_sections test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_tool_queue test_ui test_unattended test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 3095 tests in 240.2s (686 classes, 16 at a time; slowest: LeanKind 114s, Stop 100s, ExamAuthors 81s) / FAILED (18 classes: test_design_tokens.Extract, test_settings_power.Profile, test_which.Which [ran] [tree b3a48ff0b05c] [world 2f1906870a] (2026-11-03T21:22:24Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_backlog test_bench_family test_board_export test_board_surfaces test_brainstorm_skill test_builder test_claude test_cli test_context_tax test_core test_cost test_critique test_debug test_design_surfaces test_design_tokens test_diagnosis test_docs test_docsdrift test_doctor test_edit_cards test_exam test_export test_extras test_followups test_foresight test_genesis test_guard test_guard_cases test_guard_mine test_handoff test_hooks test_ideation test_inbox_more test_incident test_judgment test_lanes test_learning2 test_lib_hostile test_lib_source_kill test_library test_map test_mcp test_nudges test_onwrite test_pass1 test_playbook_evals test_playbook_machinery test_playbook_route test_playbook_use test_plugin_parity test_plugins test_recall test_release test_rename_scan test_repeats test_replan test_roles test_scaffold test_scene test_scout test_second test_session test_session_fixes test_settings test_settings_power test_settings_safety test_setup test_shade test_ship test_showpieces test_site_gallery test_site_sections test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_tool_queue test_ui test_unattended test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.86s] [ran] [tree bb26f1639ffe] [world 2f1906870a] (2026-11-03T21:34:40Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_backlog test_bench_family test_board_export test_board_surfaces test_brainstorm_skill test_builder test_claude test_cli test_context_tax test_core test_cost test_critique test_debug test_design_surfaces test_design_tokens test_diagnosis test_docs test_docsdrift test_doctor test_edit_cards test_exam test_export test_extras test_followups test_foresight test_genesis test_guard test_guard_cases test_guard_mine test_handoff test_hooks test_ideation test_inbox_more test_incident test_judgment test_lanes test_learning2 test_lib_hostile test_lib_source_kill test_library test_map test_mcp test_nudges test_onwrite test_pass1 test_playbook_evals test_playbook_machinery test_playbook_route test_playbook_use test_plugin_parity test_plugins test_recall test_release test_rename_scan test_repeats test_replan test_roles test_scaffold test_scene test_scout test_second test_session test_session_fixes test_settings test_settings_power test_settings_safety test_setup test_shade test_ship test_showpieces test_site_gallery test_site_sections test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_tool_queue test_ui test_unattended test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.40s] [ran] [tree 893b25bb28cb] [world 2f1906870a] (2026-11-03T21:44:55Z)
- `python3 plugin/tests/run.py test_genesis test_rename_scan` → ✗ exit 1 · Ran 224 tests in 17.7s (25 classes, 16 at a time; slowest: GenerationReview 15s, ProofBeforePresentation 14s, GenesisRead 12s) / FAILED (3 classes: test_rename_scan.RenameScan, test_genesis.SealedPred (start tree + this task's tests) [ran] [tree b8e26785e3c4] [world 2f1906870a] (2026-11-03T21:53:16Z)
- `python3 plugin/tests/run.py test_genesis test_rename_scan` → exit 0 · Ran 224 tests in 17.0s (25 classes, 16 at a time; slowest: GenerationReview 15s, ProofBeforePresentation 14s, GenesisRead 13s) / OK [ran] [tree b8e26785e3c4] [world 2f1906870a] (2026-11-03T21:53:16Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree b8e26785e3c4] [world 2f1906870a] (2026-11-03T21:53:56Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan test_docs` → exit 0 · Ran 115 tests in 8.4s (26 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree b8e26785e3c4] [world 2f1906870a] (2026-11-03T21:53:56Z)
- `python3 plugin/tests/run.py test_rename_scan test_docs test_genesis test_judgment` → exit 0 · Ran 397 tests in 28.3s (70 classes, 16 at a time; slowest: ProofBeforePresentation 22s, GenerationReview 19s, GenesisRead 14s) / OK [ran] [tree b8e26785e3c4] [world 2f1906870a] (2026-11-03T21:53:56Z)
- (audit intent) `fm-reviewer pass on the 164-file diff: no guard weakening, every hook/core/guard widening keeps fm, every renamed verb exists in cli.RENAMES; its four findings fixed on the branch (sampo rune check argv, sampo outcomes proof citations, check_argv text, the rules' commit note restored); the rest is T-2845` → sessions read and copy sampo spellings; fm keeps working and README/INSTALL say so [tree b8e26785e3c4] (2026-11-03T21:53:56Z)
- (audit edge) `fm-reviewer pass on the 164-file diff: no guard weakening, every hook/core/guard widening keeps fm, every renamed verb exists in cli.RENAMES; its four findings fixed on the branch (sampo rune check argv, sampo outcomes proof citations, check_argv text, the rules' commit note restored); the rest is T-2845` → program output quoted in docs may still print fm (hooks and guard say fm until T-2845); rules fit the 6400 cap at 6392 [tree b8e26785e3c4] (2026-11-03T21:53:56Z)
- (audit adversary) `fm-reviewer pass on the 164-file diff: no guard weakening, every hook/core/guard widening keeps fm, every renamed verb exists in cli.RENAMES; its four findings fixed on the branch (sampo rune check argv, sampo outcomes proof citations, check_argv text, the rules' commit note restored); the rest is T-2845` → regex widenings are alternations that keep fm; a sampo-spelled dangerous command is refused exactly as the fm one [tree b8e26785e3c4] (2026-11-03T21:53:56Z)
## Log
- 2026-11-03T04:57:12Z created
- 2026-11-03T05:37:00Z blocked: waits on T-2779 (the library's messages) and a check of every hook regex for fm-only command patterns
- 2026-11-03T21:05:19Z unblocked
- 2026-11-03T21:05:25Z criterion 2 verify: `python3 plugin/tests/run.py test_rename_scan test_docs test_skills` → `python3 plugin/tests/run.py test_rename_scan test_docs`
- 2026-11-03T21:05:55Z planned: it has criteria and steps
- 2026-11-03T21:05:56Z set tier=M
- 2026-11-03T21:06:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2778.builder.md
- 2026-11-03T21:06:43Z focused
- 2026-11-03T21:06:44Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-03T21:52:18Z merged worktree-agent-a31e34a6c2dd6b79d (167 file(s))
- 2026-11-03T21:52:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a31e34a6c2dd6b79d
- 2026-11-03T21:52:22Z focused
- 2026-11-03T22:01:29Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a three-part change. (1) Widen every command-matching regex in `plugin/lib/fmhooks.py`, `fmcore.py` and `fmguard.py` (gate-pipe, finish detection, evidence parsing, guard verbs) so `sampo ...` matches wherever `fm ...` does. (2) Add a test that greps those files for fm-only command regex…
- The "test greps first" clause means a lint-style test that runs before the skill rewrite, so it fails if any fm-only regex is left. It does not mean a behavioural test.
- Narrower: only the skill and doc spellings change, and the hook widening is already done under T-2768. The task would then be a sweep plus the grep test.
- Broader: `fm` becomes a deprecated alias, with the hooks normalizing the command name before matching. This is a refactor, not a regex widening.
Approaches:
- Add one shared command-prefix fragment (for example `(?:fm|sampo)`) in a single module that `fmhooks.py`, `fmcore.py` and `fmguard.py` import. Replace each hard-coded `fm` in the regexes with it. The grep test then asserts that no regex literal in those three files contains a bare `fm\b` outside th…
- Normalize at the entry point: rewrite a leading `sampo` to `fm` in the tokenized command before any matcher sees it. This is fewer edits, but evidence parsing and finish detection that read the raw command or its output can still be missed. The grep test would also need a different assertion.
- For the test, add a file under `plugin/tests/` that scans for regex literals via `ast` or `re` and carries an allowlist. Name it so `plugin/tests/run.py` runs it first. Separately, add a parametrized behavioural test that feeds each hook pattern both an `fm` and a `sampo` command.
- Do the skills sweep as a scripted rewrite of fenced command examples only, run after the grep test passes. Keep a dry-run diff for review and leave the prose and `fm` references in historical docs (`CHANGELOG.md`) alone.
Failure modes:
- A regex that anchors on `fm` in a pattern which is not obviously a command (a path like `plugin/bin/fm`, a `.fm/` directory, or an `fm doctor` string in an evidence line) gets widened or rewritten wrongly, which changes behaviour. Conversely, the grep test's allowlist hides a real fm-only matcher.
- `plugin/lib/sampo/` duplicates the `fm*.py` modules, so fixing only `fmhooks.py`, `fmcore.py` and `fmguard.py` leaves the sampo-side copies fm-only. Hooks then fire for `fm` but not for `sampo task new`, and the skills teach a spelling the guards silently skip.
- The sweep misses the output side. Evidence parsing and finish detection also match text that `sampo` prints (its banner or prefix). If `sampo` prints different text from `fm`, the command matches but the parse fails.
- The bulk rewrite across the skill files breaks the gates: `fm replay`, `plugin/tests/e2e/roundtrip.py` and fixtures that assert on exact skill text. It also changes `bench_hooks.py` timings if the widened regexes backtrack more.
## Dissent
- [x] rival reading: Likeliest: a three-part change. (1) Widen every command-matching regex in `plugin/lib/fmhooks.py`, `fmcore.py` and `fmguard.py` (gate-pipe, finish detection, evidence parsing, guard verbs) so `sampo ...` matches wherever `fm ...` does. (2) Add a test that greps those files for fm-only command regex… — answered: adopted: widen any regex step 1's test finds; FM_NAME_RE and _GATE_PIPE already cover the main ones
- [x] rival reading: The "test greps first" clause means a lint-style test that runs before the skill rewrite, so it fails if any fm-only regex is left. It does not mean a behavioural test. — answered: adopted: step 1 is a lint-style scan that runs before the rewrite
- [x] rival reading: Narrower: only the skill and doc spellings change, and the hook widening is already done under T-2768. The task would then be a sweep plus the grep test. — answered: adopted in part: the widening is mostly done (FM_NAME_RE); the test proves it, then the sweep
- [x] rival reading: Broader: `fm` becomes a deprecated alias, with the hooks normalizing the command name before matching. This is a refactor, not a regex widening. — answered: rejected: SAMPO.md keeps fm as an alias that works exactly as before; matching both spellings is enough
- [x] rival approach: Add one shared command-prefix fragment (for example `(?:fm|sampo)`) in a single module that `fmhooks.py`, `fmcore.py` and `fmguard.py` import. Replace each hard-coded `fm` in the regexes with it. The grep test then asserts that no regex literal in those three files contains a bare `fm\b` outside th… — answered: adopted: reuse fmguard.FM_NAME_RE (or its core twin) for any regex the scan flags
- [x] rival approach: Normalize at the entry point: rewrite a leading `sampo` to `fm` in the tokenized command before any matcher sees it. This is fewer edits, but evidence parsing and finish detection that read the raw command or its output can still be missed. The grep test would also need a different assertion. — answered: rejected: evidence parsing and finish detection read raw commands and output, so a front-door rewrite misses them
- [x] rival approach: For the test, add a file under `plugin/tests/` that scans for regex literals via `ast` or `re` and carries an allowlist. Name it so `plugin/tests/run.py` runs it first. Separately, add a parametrized behavioural test that feeds each hook pattern both an `fm` and a `sampo` command. — answered: adopted: an ast scan of regex literals with an allowlist (agent ids like fm-reviewer), plus one behavioural case each for gate-pipe and finish detection spelled sampo
- [x] rival approach: Do the skills sweep as a scripted rewrite of fenced command examples only, run after the grep test passes. Keep a dry-run diff for review and leave the prose and `fm` references in historical docs (`CHANGELOG.md`) alone. — answered: adopted: a scripted rewrite of command spellings (fenced and inline code) on the doc surfaces, CHANGELOG and tower records untouched
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-11-03: [costly] [cites: user steer: read SAMPO.md (protected core queued for the user; nothing a user has may break)] The rename's guard step comes first: …
## Lessons
- Before a docs rename, list every parser that reads those docs or the user's typed commands; the rewrite breaks each one that matches only the old spelling
## Files touched
- .fm-scratch/probe.py
- plugin/tests/test_rename_scan.py
- .fm-scratch/edits.json
- plugin/lib/sampo/core.py
- plugin/lib/sampo/hooks.py
- .fm-scratch/edits2.json
- plugin/lib/fmguard.py
- .fm-scratch/verbs.py
- MASTER.md
- plugin/commands/settings.md
- plugin/skills/design-extract/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/intake/references/planning.md
- plugin/skills/playbooks/references/ui/interaction.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/ui/visual-qa.md
- plugin/skills/genesis/SKILL.md
- plugin/skills/playbooks/references/security/command-guard.md
- plugin/agents/fm-builder.md
- plugin/agents/fm-debugger.md
- plugin/agents/fm-reproducer.md
- plugin/agents/fm-reviewer.md
- plugin/commands/backlog.md
- plugin/commands/build.md
- plugin/commands/looks.md
- plugin/rules/foreman.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- plugin/skills/capture/SKILL.md
- plugin/skills/debug-test/SKILL.md
