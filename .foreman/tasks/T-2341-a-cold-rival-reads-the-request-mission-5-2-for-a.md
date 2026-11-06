---
id: T-2341
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsecond.py, plugin/lib/fmcore.py, plugin/protocols.json, plugin/tests/test_second.py]
depends_on: [T-2338]
source: user
created: 2026-10-31T13:58:37Z
updated: 2026-10-31T15:44:02Z
builder_model: sonnet
base: ee84c15b9f07d4cf109c329381f71efad71c2caa
base_tree: b06efae68646388bec2cadc037413f86d7e8eaee
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T14:59:57Z
plan0_scope: [plugin/lib/fmsecond.py, plugin/lib/fmcore.py, plugin/protocols.json, plugin/tests/test_second.py]
verified: strong
---
# A cold rival reads the request (Mission 5, #2): for an L plan, and an M plan under the race bar or with a one-way step, a tool-less child on another model sees only the request and the repo map and writes its readings, approaches and failure modes; each rival-only item is adopted or rejected before focus; its top reading is the ambiguity signal
## Raw request
> A cold rival reads the request (Mission 5, #2): for an L plan, and an M plan under the race bar or with a one-way step, a tool-less child on another model sees only the request and the repo map and writes its readings, approaches and failure modes; each rival-only item is adopted or rejected before focus; its top reading is the ambiguity signal
## Interpretation
Reading 1: an independent read by a model that never saw the plan finds the readings and approaches the planner missed: a signal the planner didn't author. Reading 2: more stress-test roles on the same plan (fm second plan --role devil). Reading 2 sees the plan and anchors on it, and it ran 24 times in all. Reading 1.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm second rival ID writes a 'Rival plan' section (data, not instructions) from a child that never sees the plan; a rival reading or approach the plan lacks, and that names a file, symbol or reading, becomes an open Dissent line; fm focus refuses an unstarted L brief, an M brief under the race bar or claiming one honest reading, and any brief with a one-way step (S included) until the section exists and no rival-only line is open, the gap naming fm second rival ID so fm next shows it as the next action; other S and M briefs never need it; a failed child is noted and doesn't block — verify with `python3 plugin/tests/run.py test_second -k Rival`
- [x] a rival whose top reading differs from the plan's chosen one marks the brief rival_split, which brief 8 reads as ambiguous; protocols.json's M 'optional' panel row is removed, replaced by this trigger — verify with `python3 plugin/tests/run.py test_second -k RivalSplit`
## Non-goals
## Approach (options → choice → why)
1) one rival child per L plan (and per unsure or one-way M plan), diffed by meaning-bearing words; fails if: rival lines are generic, so a line counts only when it names a file, symbol or reading the plan doesn't. 2) use what exists: fm second plan's devil role; fails if: anchored on the plan. 3) do less: L only; fails if: unsure M plans keep one reading. 4) three cheap samples voting on readings; fails if: three calls for what one cold rival beside the plan already gives (two independent readers). Choice 1 (70%): one call where the risk is, zero on S and on confident M.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, MASTER.md, plugin/lib/fmhooks.py, plugin/tests/test_core.py; past FIXes T-0876, T-0907, T-0985, T-0986, T-0990.
## Execution prompt
## Steps
1. [x] red tests (test_second Rival, RivalSplit): the child gets only the request and map; rival-only items become Dissent; generic items ('add tests') are dropped; the gate refuses L until answered; a split marks the brief
2. [x] fm second rival (fmsecond._child on a model other than the session's), the diff and the Dissent lines
3. [x] the L/M trigger in _content_gaps; protocols.json's M row removed
4. [x] docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T15:30:41Z step 1/4: red tests (test_second Rival, RivalSplit): the child gets only the request and map; rival-only items become Dissent; generic items ('add tests') are dropped; the gate refuses L until answered; a split marks the brief
- git: worktree-agent-a8ef86fd05a57829c; 4 uncommitted: plugin/lib/fmcore.py, plugin/lib/fmsecond.py, plugin/protocols.json, plugin/tests/test_second.py
- touched since last checkpoint: plugin/lib/fmcli.py, MASTER.md, plugin/skills/intake/references/planning.md, plugin/tests/test_core.py, plugin/lib/fmcore.py, plugin/lib/fmsecond.py, plugin/protocols.json, plugin/tests/test_second.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_second -k Rival 2>&1 | tail -15` → ✗ exit 1 · Ran 19 tests in 14.8s (2 classes, 16 at a time; slowest: RivalSplit 9s, Rival 7s) / FAILED (2 classes: test_second.RivalSplit, test_second.Rival) [ran] [tree ff00cba69b0a] (2026-10-31T15:05:01Z)
- (step 1) `python3 plugin/tests/run.py test_second -k RivalSplit` → ✗ exit 1 · Ran 3 tests in 3.6s (1 classes, 16 at a time; slowest: RivalSplit 3s) / FAILED (1 classes: test_second.RivalSplit) [ran] [tree 06397430437b] (2026-10-31T15:05:18Z)
- (ac 1) `python3 plugin/tests/run.py test_second -k Rival 2>&1 | grep -v "^ File\|~~~\|\^\^\^" | tail -30` → ✗ exit 1 · Ran 11 tests in 5.9s (2 classes, 16 at a time; slowest: Rival 5s, RivalSplit 1s) / FAILED (2 classes: test_second.Rival, test_second.RivalSplit) [ran] [tree 38bc1dedf8be] (2026-10-31T15:08:39Z)
- (ac 1) `python3 plugin/tests/run.py test_second -k Rival 2>&1 | grep -v "^ File\|~~~\|\^\^\^" | tail -30` → exit 0 · Ran 11 tests in 11.0s (2 classes, 16 at a time; slowest: Rival 10s, RivalSplit 3s) / OK [ran] [tree 2f1da0c9823a] (2026-10-31T15:08:54Z)
- (step 3) `python3 plugin/tests/run.py test_second -k Rival 2>&1 | grep -v "^ File\|~~~\|\^\^\^" | tail -30` → exit 0 · Ran 11 tests in 11.0s (2 classes, 16 at a time; slowest: Rival 10s, RivalSplit 3s) / OK [ran] [tree 2f1da0c9823a] (2026-10-31T15:08:54Z)
- (step 2) `python3 plugin/tests/run.py test_second -k Rival` → exit 0 · Ran 11 tests in 8.5s (2 classes, 16 at a time; slowest: Rival 8s, RivalSplit 2s) / OK [ran] [tree aea179ac47fd] (2026-10-31T15:09:07Z)
- (step 3) `python3 plugin/tests/run.py test_second -k RivalSplit` → exit 0 · Ran 3 tests in 2.4s (1 classes, 16 at a time; slowest: RivalSplit 2s) / OK [ran] [tree aea179ac47fd] (2026-10-31T15:09:10Z)
- (step 4) `grep -c 'fm second rival' MASTER.md plugin/skills/intake/references/planning.md` → exit 0 · MASTER.md:2 / plugin/skills/intake/references/planning.md:1 [ran] [tree 14d96bad1f5d] (2026-10-31T15:09:27Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_board_verbs test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_guard test_guard_cases test_hooks test_ideation test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_robustness test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1708 tests in 136.2s (396 classes, 16 at a time; slowest: Stop 136s, NoTaskGate 61s, Scout 60s) / FAILED (1 classes: test_core.Stages) [ran] [tree 14d96bad1f5d] (2026-10-31T15:11:44Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_board_verbs test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_guard test_guard_cases test_hooks test_ideation test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_robustness test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.44s] [ran] [tree 76e7f379e3ff] (2026-10-31T15:14:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_backlog test_batch test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_code test_code_envelope test_code_hardening test_code_worker test_compact test_conflict_history test_core test_cost test_cost_forecast test_crash_hygiene test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_drive_side test_economics test_edit_cards test_evidence_quality test_export test_extras test_followups test_genesis test_graph test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judge_home test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_metacog test_nudges test_onwrite test_outcomes test_parallel test_pass4 test_paused test_planning test_playbook_use test_plugin_parity test_plugins test_queue_preview test_reasoning test_recall test_replan test_robustness test_round_g test_round_i test_runner_lint test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_tool_taint test_trials test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.95s] [ran] [tree 467ef092f361] (2026-10-31T15:36:18Z)
- (step 1) `python3 plugin/tests/run.py test_second test_core` → exit 0 · Ran 150 tests in 14.2s (37 classes, 16 at a time; slowest: Rival 14s, BriefIndex 2s, RivalSplit 2s) / OK [ran] [tree 467ef092f361] (2026-10-31T15:36:38Z)
- (step 1) `python3 plugin/tests/run.py test_second test_core` → exit 0 · Ran 150 tests in 18.2s (37 classes, 16 at a time; slowest: Rival 18s, RivalSplit 6s, BriefIndex 5s) / OK [ran] [tree 2b9cd3e51f2c] (2026-10-31T15:38:15Z)
- (ac 1) `python3 plugin/tests/run.py test_second -k Rival` → exit 0 · Ran 18 tests in 17.9s (2 classes, 16 at a time; slowest: Rival 17s, RivalSplit 4s) / OK [ran] [tree 930be79ba41e] (2026-10-31T15:38:53Z)
- (ac 2) `python3 plugin/tests/run.py test_second -k RivalSplit` → exit 0 · Ran 5 tests in 5.1s (1 classes, 16 at a time; slowest: RivalSplit 5s) / OK [ran] [tree 930be79ba41e] (2026-10-31T15:38:53Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch after merging main: fixtures pass T-2335's gate, no rival_split without an Interpretation, the ruled-out phrase needs no rival, lists capped at 4, the gate reads a rival_at key only rival() writes (a hand-set section or rival_at is refused), S one-way gate narrowed to deploy/publish/release/migrate/delete/drop table unless the request names it, a gate-on stage and fm next test; 150 tests OK after merge` → an independent read of the request alone surfaces readings and approaches the plan missed; focus waits on it where the plan is uncertain or one-way (tested gate-on) [tree 930be79ba41e] (2026-10-31T15:38:53Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch after merging main: fixtures pass T-2335's gate, no rival_split without an Interpretation, the ruled-out phrase needs no rival, lists capped at 4, the gate reads a rival_at key only rival() writes (a hand-set section or rival_at is refused), S one-way gate narrowed to deploy/publish/release/migrate/delete/drop table unless the request names it, a gate-on stage and fm next test; 150 tests OK after merge` → the child gets only the redacted request and repo map; its lines pass plain/defang/redact; the gate can't be cleared by hand (rival_at refused) [tree 930be79ba41e] (2026-10-31T15:38:53Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch after merging main: fixtures pass T-2335's gate, no rival_split without an Interpretation, the ruled-out phrase needs no rival, lists capped at 4, the gate reads a rival_at key only rival() writes (a hand-set section or rival_at is refused), S one-way gate narrowed to deploy/publish/release/migrate/delete/drop table unless the request names it, a gate-on stage and fm next test; 150 tests OK after merge` → S push/send/lease chores no longer wait on a paid call; one child call per rival run [tree 930be79ba41e] (2026-10-31T15:38:53Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch after merging main: fixtures pass T-2335's gate, no rival_split without an Interpretation, the ruled-out phrase needs no rival, lists capped at 4, the gate reads a rival_at key only rival() writes (a hand-set section or rival_at is refused), S one-way gate narrowed to deploy/publish/release/migrate/delete/drop table unless the request names it, a gate-on stage and fm next test; 150 tests OK after merge` → the 2/3 overlap rule is sensitive to wording (the weakest link, noted) [tree 930be79ba41e] (2026-10-31T15:38:53Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch after merging main: fixtures pass T-2335's gate, no rival_split without an Interpretation, the ruled-out phrase needs no rival, lists capped at 4, the gate reads a rival_at key only rival() writes (a hand-set section or rival_at is refused), S one-way gate narrowed to deploy/publish/release/migrate/delete/drop table unless the request names it, a gate-on stage and fm next test; 150 tests OK after merge` → one HARD_RE definition shared by fmcli and fmcore [tree 930be79ba41e] (2026-10-31T15:38:53Z)
## Log
- 2026-10-31T13:58:37Z created
- 2026-10-31T14:11:41Z criterion 1 text: fm second rival ID writes a 'Rival plan' section (data, not instructions) from a child that never sees the plan; a rival reading or approach the plan lacks, and that names a file, symbol or reading, becomes an open Dissent line; fm focus refuses an unstarted L brief (and an M brief under the race bar or with a one-way step) until the section exists and no rival-only line is open, the gap naming fm second rival ID; S never needs it; a failed child is noted and doesn't block → fm second rival ID writes a 'Rival plan' section (data, not instructions) from a child that never sees the plan; a rival reading or approach the plan lacks, and that names a file, symbol or reading, becomes an open Dissent line; fm focus refuses an unstarted L brief, an M brief under the race bar, and any brief with a one-way step (S included) until the section exists and no rival-only line is open, the gap naming fm second rival ID; other S and M briefs never need it; a failed child is noted and doesn't block
- 2026-10-31T14:41:38Z criterion 1 text: fm second rival ID writes a 'Rival plan' section (data, not instructions) from a child that never sees the plan; a rival reading or approach the plan lacks, and that names a file, symbol or reading, becomes an open Dissent line; fm focus refuses an unstarted L brief, an M brief under the race bar, and any brief with a one-way step (S included) until the section exists and no rival-only line is open, the gap naming fm second rival ID; other S and M briefs never need it; a failed child is noted and doesn't block → fm second rival ID writes a 'Rival plan' section (data, not instructions) from a child that never sees the plan; a rival reading or approach the plan lacks, and that names a file, symbol or reading, becomes an open Dissent line; fm focus refuses an unstarted L brief, an M brief under the race bar or claiming one honest reading, and any brief with a one-way step (S included) until the section exists and no rival-only line is open, the gap naming fm second rival ID so fm next shows it as the next action; other S and M briefs never need it; a failed child is noted and doesn't block
- 2026-10-31T14:59:42Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2341.builder.md
- 2026-10-31T14:59:56Z focused
- 2026-10-31T14:59:57Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:37:52Z merged worktree-agent-a8ef86fd05a57829c (9 file(s))
- 2026-10-31T15:37:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8ef86fd05a57829c
- 2026-10-31T15:37:53Z focused
- 2026-10-31T15:38:28Z scope: plugin/lib/fmsecond.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/protocols.json, plugin/skills/intake/references/planning.md, plugin/tests/test_second.py, plugin/tests/test_core.py, plugin/tests/helpers.py, MASTER.md, CHANGELOG.md
- 2026-10-31T15:43:50Z done
- 2026-10-31T15:44:02Z committed 9ae0b87d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261031-083832: Request: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, eve…
- research mission-20261031-083832.pack: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, every a…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_second.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcore.py, plugin/lib/fmsecond.py, plugin/protocols.json, plugin/tests/test_second.py; re-ground the plan against them before editing
## Lessons
- A gate cleared by writing the section it checks isn't a gate: key it on the act, not the artifact
## Plan gaps
- failed first: step 1 red tests (test_second Rival, RivalSplit): the child gets only the request and map; rival-only item…
## Files touched
- plugin/tests/test_second.py
- plugin/tests/helpers.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmsecond.py
- plugin/protocols.json
- MASTER.md
- plugin/skills/intake/references/planning.md
- plugin/tests/test_core.py
- CHANGELOG.md
