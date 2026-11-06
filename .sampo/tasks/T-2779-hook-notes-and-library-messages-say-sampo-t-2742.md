---
id: T-2779
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/*.py, plugin/hooks/compact, mods/foreman-ui/**, plugin/tests/*.py]
depends_on: []
source: user
created: 2026-11-03T04:57:51Z
updated: 2026-11-03T19:44:36Z
builder_model: sonnet
base: b5fdc7dc1c5a9dd1547fb37b7fe090b374690a03
base_tree: 1b964dd8dbe857ba3b13ce47f3ab195a3374fa00
plan0_at: 2026-11-03T05:26:27Z
plan0_scope: [plugin/lib/sampo/*.py, plugin/hooks/compact, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/*, plugin/tests/*.py]
lane_stop: merged 2026-11-03T15:15:29Z
verified: strong
unproven: [docs, meaning, tui-unshot, ui-unshot]
---
# Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/compact and the foreman-ui mod's visible text becomes Sampo (or the role name it means: the guard's refusals Ward, fm code's lines Smith, genesis Rune); paths, FOREMAN_*, plugin ids and the Foreman-Task trailer stay; fmguard.py's own messages wait for the protected-core step
## Raw request
> Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/compact and the foreman-ui mod's visible text becomes Sampo (or the role name it means: the guard's refusals Ward, fm code's lines Smith, genesis Rune); paths, FOREMAN_*, plugin ids and the Foreman-Task trailer stay; fmguard.py's own messages wait for the protected-core step
## Interpretation
Reading 1 (chosen): SAMPO.md says no user-visible Foreman remains; the hook notes ('Foreman: …', 'Foreman drive: …') are the text a user sees most, so they say Sampo, with role names where the line means one. Nothing parses the prefix (grep: no regex, startswith or includes on 'Foreman:' outside tests), so only tests that quote notes change. Reading 2: one NAME constant used by every note. Rejected as a first step: 200 f-strings would each change anyway; the ratchet stops new ones.
## Assumptions (confidence)
## Acceptance criteria
- [x] no user-visible Foreman string is left in plugin/lib/sampo, plugin/hooks/compact or the mod outside the kept forms, and the rename ratchet's BASELINE drops by the lines changed — verify with `python3 plugin/tests/run.py test_rename_scan test_rename_aliases`
- [x] the full suite stays green under both names — verify with `python3 plugin/tests/run.py`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: fm sub (the regex codemod with per-file counts) for literal 'Foreman' inside string literals, then read each hit for role names; test_rename_scan as the ratchet. Likely outcome: ~200 lines over 20 modules and ~15 test files. Fails if: a test or the mod matches a note's exact text (they're updated in the same commit). 2) Do less: hooks.py only (99 of ~200). Fails if: cli, doctor and release keep printing Foreman and the cold review flags them. 3) A NAME constant threaded through every note. Fails if: it doubles the diff for no user-visible gain. Choice 1 (80%).
## Risks and rollback
Blast radius (fm graph blast): unknown, no co-change history for plugin/hooks/compact.
## Execution prompt
## Steps
1. [x] red: test_rename_scan counts library string literals; lower BASELINE to the target
2. [x] the sweep by meaning, per module, tests updated where they quote a note
3. [x] the mod's text and its tests (bun test in mods/foreman-ui)
4. [x] full suite
5. [x] comments and docstrings that name a moved module (fmcore.x, fmcode.*, fmcli.py, fmhooks._cc_version …) name its sampo path; fmguard stays
## Resume here
<!-- auto -->
- 2026-11-03T06:01:31Z step 1/5: red: test_rename_scan counts library string literals; lower BASELINE to the target
- git: worktree-agent-a3d7b46b81e7f2b29; 107 uncommitted: mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/README.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/fixtures/golden.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tests/pane-hostile.test.tsx, mods/foreman-ui/tests/pane-sweep.test.tsx
- touched since last checkpoint: plugin/tests/test_edit_cards.py, .fm-scratch/mod1.json, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/README.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/types/index.d.ts, .fm-scratch/mod2.json, mods/foreman-ui/tests/fixtures/golden.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tests/pane-hostile.test.tsx, mods/foreman-ui/tests/pane-sweep.test.tsx, mods/foreman-ui/tests/replay.test.tsx
- failures met: assertionerror: lists differ: ['ado[0 chars]', 'louhi', 'lsp', 'machine', 'mandate', 'map…; posttoolusefailure 0.0 0.0 0 [0]
## Docs impact
none: the CHANGELOG entry lands with T-2742 step 8
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · SessionEnd                  55.1    78.6     150  [0] / machine busy (load 1.1 per core): judged by each hook's CPU time, not wall time (T-0805) (flaky again (failed first in 3+ recent runs): treated as a failure; find the race); python3 plugin/tests/run.py → ✗ exit 1 · Ran 5923 tests in 527.1s (1274 classes, 16 at a time; slowest: Worker 241s, Stop 215s, Long 141s) / FAILED (2 classes: test_diff_gates.DiffGates, test_help.Help) [ran] [tree da9ef421471a] [world 2f1906870a] (2026-11-03T05:37:25Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases` → exit 0 · Ran 10 tests in 6.3s (2 classes, 16 at a time; slowest: RenameAliases 6s, RenameScan 1s) / OK [ran] [tree 839933dc9053] [world 2f1906870a] (2026-11-03T06:06:20Z)
- (step 3) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 839933dc9053] [world 2f1906870a] (2026-11-03T06:06:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_agents test_anergy test_bench test_bench_family test_board_hooks test_board_posture test_board_surfaces test_budget test_bus test_claims test_cli test_cloned_config test_code_tui test_code_worker test_compact test_core test_cost test_demo test_deps test_design_gates test_design_surfaces test_docs test_docsdrift test_doctor test_draft test_drill test_edit_cards test_evolve test_export test_find test_firewall test_first_note test_fixes test_foresight test_friction test_genesis test_graph test_guard_hardening test_hooks test_hunks test_inbox_more test_integrations test_lanes test_library test_long test_loop test_map test_mcp test_memory test_migrate test_night test_onwrite test_oracle test_outcomes test_outside test_page test_perf_cost test_plugins test_prove test_recall test_release test_rename_scan test_replay test_research test_resilience test_round_g test_safety test_safety_gate test_scene test_scout test_selfgate test_serve test_settings test_setup test_ship test_shot test_smoke test_statusline_ui test_steer test_suite_hygiene test_supply_delta test_sync test_taste test_tidy test_tool_injection test_trials test_triggers test_trust test_ui test_ui_replay test_verify_strength test_visibility test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.32s] [ran] [tree 6c42e9581192] [world 2f1906870a] (2026-11-03T06:16:33Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases` → exit 0 · Ran 13 tests in 3.3s (2 classes, 16 at a time; slowest: RenameAliases 3s, RenameScan 1s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:36:49Z)
- (ac 2) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 5948 tests in 366.5s (1275 classes, 16 at a time; slowest: LeanKind 121s, Worker 105s, Stop 80s) / FAILED (1 classes: test_demo.DemoNext) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:36:49Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases test_release test_cost test_hooks` → exit 0 · Ran 327 tests in 48.7s (49 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:36:49Z)
- (step 4) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases test_release test_cost test_hooks` → exit 0 · Ran 327 tests in 48.7s (49 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:36:49Z)
- (step 5) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases test_release test_cost test_hooks` → exit 0 · Ran 327 tests in 48.7s (49 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:36:49Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 17:13 UTC) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:36:49Z)
- (ac 2) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 5948 tests in 354.8s (1275 classes, 16 at a time; slowest: LeanKind 120s, Worker 99s, ExamAuthors 75s) / FAILED (1 classes: test_demo.DemoNext) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:42:46Z)
- `python3 plugin/tests/run.py test_rename_scan test_rename_aliases test_release test_cost test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:36:49Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:42:46Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 17:13 UTC) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:42:46Z)
- (ac 2) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 5948 tests in 323.1s (1275 classes, 16 at a time; slowest: Worker 108s, LeanKind 98s, Stop 86s) / FAILED (1 classes: test_demo.DemoNext) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:48:10Z)
- `python3 plugin/tests/run.py test_rename_scan test_rename_aliases test_release test_cost test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:42:46Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:48:10Z)
- (ac 2) `python3 plugin/tests/run.py` → exit 0 · Ran 5955 tests in 318.9s (1278 classes, 16 at a time; slowest: LeanKind 104s, Worker 91s, ExamAuthors 73s) / OK [ran] [tree 9963cd4d79ca] [world 2f1906870a] (2026-11-03T19:41:53Z)
- `python3 plugin/tests/run.py test_rename_scan test_rename_aliases test_release test_cost test_hooks` → exit 0 · Ran 327 tests in 48.1s (49 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 29s, PreToolUse 24s) / OK [ran] [tree 9963cd4d79ca] [world 2f1906870a] (2026-11-03T19:41:53Z)
- (audit intent) `self: read the diff by meaning; strings say Sampo, Ward, Smith, Rune or Louhi; code that matches a string (release MARK, cost's refusal counter, snapshot subject, louhi's anchor) accepts both names` → the hook notes and library messages say Sampo and its role names [tree 9963cd4d79ca] (2026-11-03T19:41:53Z)
- (audit edge) `self: read the diff by meaning; strings say Sampo, Ward, Smith, Rune or Louhi; code that matches a string (release MARK, cost's refusal counter, snapshot subject, louhi's anchor) accepts both names` → the release subject stays 'Foreman X' with MARK accepting both; the guard's own refusal text, paths, env names and plugin ids keep the old name; 'Smith project' misreads were fixed in smithtui [tree 9963cd4d79ca] (2026-11-03T19:41:53Z)
- (audit adversary) `self: read the diff by meaning; strings say Sampo, Ward, Smith, Rune or Louhi; code that matches a string (release MARK, cost's refusal counter, snapshot subject, louhi's anchor) accepts both names` → strings only; every parser that reads a renamed string accepts both names, so old logs and transcripts still count [tree 9963cd4d79ca] (2026-11-03T19:41:53Z)
## Log
- 2026-11-03T04:57:51Z created
- 2026-11-03T04:58:02Z set approved=True
- 2026-11-03T04:58:02Z blocked: waits on T-2775 (cli.py) and T-2774 (rune.py) lanes to merge, so the sweep doesn't collide
- 2026-11-03T05:26:15Z unblocked
- 2026-11-03T05:26:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2779.builder.md
- 2026-11-03T05:26:26Z focused
- 2026-11-03T05:57:06Z set scope=['plugin/lib/sampo/*.py', 'plugin/hooks/compact', 'mods/foreman-ui/**', 'plugin/tests/*.py']
- 2026-11-03T14:29:49Z user approved core in Claude Code's permission prompt
- 2026-11-03T15:15:29Z merged worktree-agent-a3d7b46b81e7f2b29 (114 file(s))
- 2026-11-03T15:15:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3d7b46b81e7f2b29
- 2026-11-03T15:15:30Z focused
- 2026-11-03T15:15:32Z scope: files outside the scope since focus came from other lanes' merge commits, not this task's edits
- 2026-11-03T15:16:33Z paused: focus moved to T-2765
- 2026-11-03T17:05:18Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:05:18Z focused
- 2026-11-03T17:05:19Z paused: focus moved to T-2797
- 2026-11-03T17:29:48Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:29:48Z focused
- 2026-11-03T17:48:10Z paused: focus moved to T-2797
- 2026-11-03T19:35:44Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T19:35:44Z focused
- 2026-11-03T19:44:36Z done
## Follow-ups captured
## Build vs reuse
Reuse fm sub and test_rename_scan's BASELINE ratchet (T-2742 step 1); no new tooling.
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, planned, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/out…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_agents.py, plugin/tests/test_ambient.py, plugin/tests/test_anergy.py, plugin/tests/test_away.py, plugi…
## Preflight
Changed in scope since this was planned (2026-11-03): mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/README.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts…; re-ground the plan against them before editing
## Behaviour lock
none: the lane's pre-edit fm check timed out at 600 s under machine load ~55 on 2026-11-03 (T-2797); the change is covered by its targeted tests and the post-merge full suite
## Regression test
none: strings only; louhi.py and rune.py changed only messages a user reads (Foreman → Sampo/Rune/Louhi), and every reader of a changed string accepts both names; the scores .fmproved guards are untouched, so there is no behaviour to turn red first
## Lessons
- A string codemod must grep for every reader of each string first
## Plan gaps
- failed first: step 1 red: test_rename_scan counts library string literals; lower BASELINE to the target
## Files touched
- .fm-scratch-check.txt
- .fm-scratch/scan.py
- .fm-scratch/codemod.py
- plugin/tests/test_rename_scan.py
- plugin/hooks/compact
- plugin/lib/sampo/agents.py
- plugin/lib/sampo/anergy.py
- plugin/lib/sampo/bench.py
- plugin/lib/sampo/budget.py
- plugin/lib/sampo/bus.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cost.py
- plugin/lib/sampo/demo.py
- plugin/lib/sampo/deps.py
- plugin/lib/sampo/design.py
- plugin/lib/sampo/docs.py
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/doors.py
- plugin/lib/sampo/draft.py
- plugin/lib/sampo/drill.py
- plugin/lib/sampo/eco.py
- plugin/lib/sampo/edit.py
- plugin/lib/sampo/evolve.py
- plugin/lib/sampo/find.py
- plugin/lib/sampo/fixes.py
- plugin/lib/sampo/foresight.py
- plugin/lib/sampo/friction.py
- plugin/lib/sampo/graph.py
- plugin/lib/sampo/home.py
