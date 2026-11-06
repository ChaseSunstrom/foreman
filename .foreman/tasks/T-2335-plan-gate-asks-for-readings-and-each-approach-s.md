---
id: T-2335
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, plugin/skills/intake/references/planning.md, plugin/tests/*.py, plugin/lib/fmcli.py, plugin/lib/fmcode.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-31T13:58:33Z
updated: 2026-10-31T15:25:37Z
builder_model: sonnet
base: 7dc0a3c37edf95354d9a47ff66c5017afb0b2f07
base_tree: b415a68886d18835d82a7deefa8562ebbebd58c0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T14:14:20Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, plugin/skills/intake/references/planning.md]
verified: strong
---
# Plan gate asks for readings and each approach's outcome (Mission 5, #2): M plans name 2+ readings or why one; every M/L option says its likely outcome or failure mode; the options include use-what-exists or do-less; near-copy options count once
## Raw request
> Plan gate asks for readings and each approach's outcome (Mission 5, #2): M plans name 2+ readings or why one; every M/L option says its likely outcome or failure mode; the options include use-what-exists or do-less; near-copy options count once
## Interpretation
Reading 1: gen-0 #2's list (the readings of the request; every approach, including use-what-exists and do-less; the likely outcome and failure mode of each) becomes the M/L plan gate's content check, extending T-2269 (which counts options and a choice for M/L, and readings and risks for L only). Reading 2: a nudge in the intake skill, no gate. History decides: 0 of 29 M briefs since T-2277 list 2+ readings and 6 of 33 M/L briefs name use-what-exists or do-less, so the prose rule isn't followed: Reading 1.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm focus refuses an unstarted M or L brief with fewer than 2 distinct readings in Interpretation (a request with one honest reading names the reading it ruled out and why), an Approach option with no likely outcome or failure mode, an Approach with neither a use-what-exists nor a do-less option, and counts options or readings that share most of their words as one; each gap names its fix; a started task isn't re-gated; S is untouched — verify with `python3 plugin/tests/run.py test_core -k PlanContent`
## Non-goals
## Approach (options → choice → why)
1) extend _content_gaps with the four checks, deterministic, zero tokens; fails if: word markers miss real options (T-2285's lesson), so the tests use flag- and code-led options. 2) use what exists: fm second plan's devil role argues the missing approach; fails if: advisory, and protocols.json makes it optional for M, so it rarely runs. 3) do less: only the use-what-exists/do-less check; fails if: M plans keep one reading. 4) a cold child judges whether options differ; fails if: a model call per focus for what word overlap catches. Choice 1 (80%): one place, no tokens. A gate checks format only: whether the plan's choice was right is scored by the calibration ledger (brief 3) and the race and exists exam kinds.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_cli.py, README.md, plugin/tests/test_hooks.py; past FIXes T-0875, T-0876, T-0880, T-0907, T-0908.
## Execution prompt
## Steps
1. [x] red tests (test_core PlanContent): each new gap refused with its fix named; a complete M brief starts; an S brief and a started M brief untouched; three near-copy options count as one; an option that starts with a flag or code still counts (T-2285)
2. [x] _content_gaps grows the four checks, splitting options with _count_options' markers
3. [x] planning.md and fm task new --help name the plan shape (readings, options with outcomes, use-what-exists/do-less, choice)
4. [x] docs: MASTER plan-gate line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T14:53:41Z steps 4/4 done
- git: worktree-agent-acb592b76720e886f; 6 uncommitted: plugin/lib/fmcore.py, plugin/tests/helpers.py, plugin/tests/test_batch.py, plugin/tests/test_code.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py
- touched since last checkpoint: plugin/tests/test_hooks.py, plugin/tests/helpers.py, plugin/tests/test_core.py, plugin/tests/test_batch.py, plugin/tests/test_code.py, plugin/lib/fmcore.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -15` → ✗ exit 1 · Ran 8 tests in 1.9s (1 classes, 16 at a time; slowest: PlanContent 0s) / FAILED (1 classes: test_core.PlanContent) [ran] [tree 3fb988d4b87b] (2026-10-31T14:15:16Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -30` → ✗ exit 1 · Ran 8 tests in 0.6s (1 classes, 16 at a time; slowest: PlanContent 0s) / FAILED (1 classes: test_core.PlanContent) [ran] [tree 96ac0a9abda3] (2026-10-31T14:15:49Z)
- (step 1) `python3 plugin/tests/run.py test_core -k PlanContent` → exit 0 · Ran 8 tests in 0.7s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree 209460556a2c] (2026-10-31T14:16:11Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -12` → exit 0 · Ran 9 tests in 0.7s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree f2f32d1bf82d] (2026-10-31T14:25:57Z)
- (step 3) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -12` → exit 0 · Ran 9 tests in 0.7s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree f2f32d1bf82d] (2026-10-31T14:25:57Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -3` → exit 0 · Ran 9 tests in 0.9s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree 5454213f190d] (2026-10-31T14:28:17Z)
- (step 4) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -3` → exit 0 · Ran 9 tests in 0.9s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree 5454213f190d] (2026-10-31T14:28:17Z)
- (step 2) `python3 plugin/tests/run.py test_core -k PlanContent` → exit 0 · Ran 9 tests in 0.6s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree 47c27409fc4b] (2026-10-31T14:31:19Z)
- (step 3) `python3 plugin/tests/run.py test_cli -k lifecycle` → ✗ exit 1 · run.py: no test matches test_cli with -k lifecycle; did you mean -k TaskLifecycle? [ran] [tree 47c27409fc4b] (2026-10-31T14:31:19Z)
- (step 3) `python3 plugin/tests/run.py test_cli -k TaskLifecycle` → exit 0 · Ran 31 tests in 25.5s (1 classes, 16 at a time; slowest: TaskLifecycle 25s) / OK [ran] [tree 47c27409fc4b] (2026-10-31T14:31:47Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_backlog test_batch test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_code test_code_envelope test_code_hardening test_code_worker test_compact test_conflict_history test_core test_cost test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_edit_cards test_evidence_quality test_extras test_followups test_graph test_guard test_guard_cases test_hooks test_ideation test_judge_home test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_metacog test_nudges test_onwrite test_parallel test_pass4 test_paused test_planning test_playbook_use test_plugin_parity test_plugins test_queue_preview test_reasoning test_recall test_replan test_robustness test_round_i test_runner_lint test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.29s] [ran] [tree 9e6d50fea5aa] (2026-10-31T14:40:55Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k PlanContent 2>&1 | tail -40` → ✗ exit 1 · Ran 18 tests in 0.4s (1 classes, 16 at a time; slowest: PlanContent 0s) / FAILED (1 classes: test_core.PlanContent) [ran] [tree d784b75f4cd8] (2026-10-31T14:54:27Z)
- (step 1) `python3 plugin/tests/run.py test_core test_batch test_code` → exit 0 · Ran 600 tests in 123.6s (126 classes, 16 at a time; slowest: Worker 123s, Fakes 54s, Bench 35s) / OK [ran] [tree 23de73526fac] (2026-10-31T15:00:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_backlog test_batch test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_code test_code_envelope test_code_hardening test_code_worker test_compact test_conflict_history test_core test_cost test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_drive_side test_edit_cards test_evidence_quality test_extras test_followups test_graph test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judge_home test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_metacog test_nudges test_onwrite test_parallel test_pass4 test_paused test_planning test_playbook_use test_plugin_parity test_plugins test_queue_preview test_reasoning test_recall test_replan test_robustness test_round_i test_runner_lint test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_tool_taint test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [28.05s] [ran] [tree 23de73526fac] (2026-10-31T15:05:34Z)
- (step 1) `python3 plugin/tests/run.py test_core test_cli test_batch test_code` → exit 0 · Ran 722 tests in 97.5s (167 classes, 16 at a time; slowest: Worker 97s, Fakes 55s, TaskLifecycle 53s) / OK [ran] [tree 83f956bf8a2b] (2026-10-31T15:14:11Z)
- (step 1) `python3 plugin/tests/run.py test_core test_cli test_batch test_code` → exit 0 · Ran 741 tests in 100.0s (168 classes, 16 at a time; slowest: Worker 99s, Fakes 53s, TaskLifecycle 50s) / OK [ran] [tree caae2df1a352] (2026-10-31T15:23:16Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k PlanContent` → exit 0 · Ran 18 tests in 0.3s (1 classes, 16 at a time; slowest: PlanContent 0s) / OK [ran] [tree 2e8312694243] (2026-10-31T15:23:35Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed (4 MEDIUM), all fixed on the branch: numbered runs win over sub-bullets, bullets aren't readings, use-what-exists and do-less come from different options, fm batch writes two readings, fm code's and the hook's plans are exempt by --harness-plan, outcome words narrowed, a ruled-out reading needs a reason, _CHOICE_AT_RE bounded; merge conflict on MASTER resolved keeping both sides; 741 tests OK after merge, full suite green before it` → M/L plans need 2+ readings, an outcome per option and use-what-exists plus do-less options from different options; each gap names its fix (tested) [tree 2e8312694243] (2026-10-31T15:23:35Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed (4 MEDIUM), all fixed on the branch: numbered runs win over sub-bullets, bullets aren't readings, use-what-exists and do-less come from different options, fm batch writes two readings, fm code's and the hook's plans are exempt by --harness-plan, outcome words narrowed, a ruled-out reading needs a reason, _CHOICE_AT_RE bounded; merge conflict on MASTER resolved keeping both sides; 741 tests OK after merge, full suite green before it` → a label alone (use what exists:) no longer passes when one option carries both; a bare 'rejected' needs a reason; still a keyword floor, not substance (the calibration ledger scores choices) [tree 2e8312694243] (2026-10-31T15:23:35Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed (4 MEDIUM), all fixed on the branch: numbered runs win over sub-bullets, bullets aren't readings, use-what-exists and do-less come from different options, fm batch writes two readings, fm code's and the hook's plans are exempt by --harness-plan, outcome words narrowed, a ruled-out reading needs a reason, _CHOICE_AT_RE bounded; merge conflict on MASTER resolved keeping both sides; 741 tests OK after merge, full suite green before it` → unstarted M/L briefs written before the gate show stage planning and must be re-planned before a lane takes them (noted in MASTER) [tree 2e8312694243] (2026-10-31T15:23:35Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed (4 MEDIUM), all fixed on the branch: numbered runs win over sub-bullets, bullets aren't readings, use-what-exists and do-less come from different options, fm batch writes two readings, fm code's and the hook's plans are exempt by --harness-plan, outcome words narrowed, a ruled-out reading needs a reason, _CHOICE_AT_RE bounded; merge conflict on MASTER resolved keeping both sides; 741 tests OK after merge, full suite green before it` → regex bounded (\W{0,8}, 40 marks), no tokens [tree 2e8312694243] (2026-10-31T15:23:35Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed (4 MEDIUM), all fixed on the branch: numbered runs win over sub-bullets, bullets aren't readings, use-what-exists and do-less come from different options, fm batch writes two readings, fm code's and the hook's plans are exempt by --harness-plan, outcome words narrowed, a ruled-out reading needs a reason, _CHOICE_AT_RE bounded; merge conflict on MASTER resolved keeping both sides; 741 tests OK after merge, full suite green before it` → valid_m_plan helper for fixtures [tree 2e8312694243] (2026-10-31T15:23:35Z)
## Log
- 2026-10-31T13:58:33Z created
- 2026-10-31T14:06:07Z criterion 1 text: fm focus refuses an unstarted M brief with fewer than 2 readings in Interpretation and no 'One reading: <why>' line, an M/L Approach option with no outcome or failure mode, an M/L Approach with neither a use-what-exists nor a do-less option, and counts options that share most of their words as one; each gap names its fix; a started task isn't re-gated; S is untouched → fm focus refuses an unstarted M or L brief with fewer than 2 distinct readings in Interpretation (a request with one honest reading names the reading it ruled out and why), an Approach option with no likely outcome or failure mode, an Approach with neither a use-what-exists nor a do-less option, and counts options or readings that share most of their words as one; each gap names its fix; a started task isn't re-gated; S is untouched
- 2026-10-31T14:14:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2335.builder.md
- 2026-10-31T14:14:19Z focused
- 2026-10-31T14:14:20Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T14:25:32Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_core.py', 'plugin/skills/intake/references/planning.md', 'plugin/tests/*.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcode.py', 'MASTER.md']
- 2026-10-31T14:25:32Z scope widened: the stricter M/L plan gate needs every M/L test fixture to carry 2 readings and outcome-bearing options; fm code's generated plan and fm task new --help follow
- 2026-10-31T15:21:33Z merged worktree-agent-acb592b76720e886f (38 file(s))
- 2026-10-31T15:21:33Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acb592b76720e886f
- 2026-10-31T15:21:33Z focused
- 2026-10-31T15:23:34Z scope: plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmhooks.py, plugin/skills/intake/references/planning.md, plugin/tests/* (M/L fixtures, valid_m_plan helper), MASTER.md, CHANGELOG.md
- 2026-10-31T15:25:35Z done
- 2026-10-31T15:25:37Z committed 28626409 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2269 [FEATURE M, done, 3 steps] Plan gate checks content by tier (Mission 5, #2): M/L Approach names 3+ options and a choice; L adds 2+ readings and risks; a low-confi…
- research mission-20261031-083832: Request: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, eve…
- research mission-20261031-083832.pack: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, every a…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (sixth): the frame may grow, never shrink] [check: pending T-2188] Standing rule from gen 2 on: the Genesis fram…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_cost.py, plugin/test…
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcore.py, plugin/skills/intake/references/planning.md, plugin/tests/bench_hooks.py, plugin/tests/helpers.py, plugin/tests/test_backlo…; re-ground the plan against them before editing
## Lessons
- A gate that tightens retroactively must say what it strands: the queued briefs written before it
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/skills/intake/references/planning.md
- plugin/lib/fmcli.py
- MASTER.md
- plugin/lib/fmcode.py
- .fm-scratch/batch.json
- plugin/tests/test_backlog.py
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_cli.py
- plugin/tests/test_conflict_history.py
- plugin/tests/test_defect_classes.py
- plugin/tests/test_deliberation.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_graph.py
- plugin/tests/test_hooks.py
- plugin/tests/test_lane_stall.py
- plugin/tests/test_lanes.py
- plugin/tests/test_metacog.py
- plugin/tests/test_parallel.py
- plugin/tests/test_pass4.py
- plugin/tests/test_planning.py
- plugin/tests/test_queue_preview.py
- plugin/tests/test_reasoning.py
- plugin/tests/test_recall.py
- plugin/tests/test_replan.py
- plugin/tests/test_round_i.py
