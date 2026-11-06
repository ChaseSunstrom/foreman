---
id: T-2391
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:03:14Z
updated: 2026-10-31T17:53:08Z
builder_model: sonnet
base: 82f3cc90e2db630790192ea945e34c0b4cef83e1
base_tree: 3c62d6c04196678bd316eae8ad81a9e7b2dbebc7
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:12:44Z
plan0_scope: []
lane_stop: merged 2026-10-31T17:43:29Z
verified: strong
---
# Unproven rollup by domain (Mission 7, #6): one proof-kinds table adds docs, infra, migration, data, typed perf, uncited research and hollow checks, each row with its one-command upgrade, and stops counting red-first steps as unproven
## Raw request
> Unproven rollup by domain (Mission 7, #6): one proof-kinds table adds docs, infra, migration, data, typed perf, uncited research and hollow checks, each row with its one-command upgrade, and stops counting red-first steps as unproven
## Interpretation
Reading 1: one proof-kinds table (need, clearing run, upgrade command per kind) read by unproven(), adding docs, infra, migration, data, typed perf, uncited research and hollow checks, and no longer counting red-first steps whose command later ran green. Reading 2: a function per kind. Rejected: each new proof kind would then edit unproven().
## Assumptions (confidence)
## Acceptance criteria
- [x] fmcore's proof-kinds table maps each kind to what makes a done task need it (a touched-file pattern, the lines it added or the task type) and the green run that clears it; fm proof lists docs (a checkable claim in doc lines the task added, so prose-only edits never count), infra, migration, data, perf-typed (a PERFORMANCE close whose Measurements didn't come from --bench), research-uncited (a RESEARCH Decision naming no saved note with a verified claim) and hollow (a criterion fm task prove --vacuous found passing on the start tree) beside typed, inconclusive and ui-unshot, and each row prints its upgrade command — verify with `python3 plugin/tests/run.py test_proof -k proof_kind`
- [x] A step or criterion whose only runs are red counts as proven only when the same command ran green later in the task (a red-then-green pair); a red with no later green stays unproven; on 2026-10-31, 227 of fm proof's 351 rows were red-first steps whose command later ran green — verify with `python3 plugin/tests/run.py test_proof -k rollup_red_first`
- [x] fm status, fm digest, fm genesis status and fm exam scorecard print the count through one shared line function, and fm proof --json carries per-kind counts — verify with `python3 plugin/tests/run.py test_proof -k unproven_line`
- [x] fm task finish's Not verified list names each rollup kind the closing task still needs, with its upgrade command, before the task leaves the session — verify with `python3 plugin/tests/run.py test_proof -k proof_kind_finish`
- [x] With the queue empty, fm next names the newest unproven row whose upgrade can run here (its tool present, the tree trusted) as the next action, so the drive works the rollup down; a row waiting on an install or another grant is shown in fm proof as waiting and goes to the final report, never named by fm next again — verify with `python3 plugin/tests/run.py test_proof -k proof_kind_next`
- [x] A PERFORMANCE close whose --bench medians differ by less than the bench gate's noise band (T-1439) is listed under perf-noise, so a speedup inside the noise is labelled, never counted — verify with `python3 plugin/tests/run.py test_proof -k perf_noise`
## Non-goals
## Approach (options → choice → why)
1) A data table of kinds read by unproven(); a new proof kind is a row; _UI_FILE and _UI_PROOF become the ui row; upgrade commands per row; per-kind counts in --json; one unproven_line() for the four renderers. Fails if: a row's clearing run is too loose, which each new kind's test with one done task pins. 2) Use what exists: T-2273's rollup as it is. Likely outcome: 227 of 351 rows on 2026-10-31 stay noise and 53 PERFORMANCE closes resting on typed numbers stay uncounted. 3) Do less: fix only the red-first rule. Fails if: the per-domain kinds the gap map asks for are still missing. 4) Block closes on any unproven kind. Breaks T-2273's reason: typed proof is legitimate where a check can't run here and the label is the point. Choice 1 (80%): a table keeps each new kind to a row.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a red-first step later green, one done task per new kind
2. [x] the table; unproven() reads it; _UI_FILE and _UI_PROOF become its ui row
3. [x] upgrade commands per row; per-kind counts in --json
4. [x] one unproven_line() for the four renderers; MASTER.md, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T16:54:47Z steps 4/4 done
- git: worktree-agent-ac5c97147401cbb1e; 2 uncommitted: plugin/lib/fmcore.py, plugin/tests/test_proof.py
- touched since last checkpoint: plugin/tests/test_proof.py, plugin/lib/fmcore.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proof` → red as expected (exit 1) · Ran 22 tests in 14.8s (3 classes, 16 at a time; slowest: Proof 14s, Palette 0s, FindRankValue 0s) / FAILED (1 classes: test_proof.Proof) [ran] [tree 45675c7e2232] (2026-10-31T16:20:14Z)
- (step 2) `python3 plugin/tests/run.py test_proof 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)|Error|rror:" | head -40` → exit 0 · Ran 22 tests in 26.8s (3 classes, 16 at a time; slowest: Proof 26s, Palette 0s, FindRankValue 0s) / OK [ran] [tree 8a20b6f48425] (2026-10-31T16:29:03Z)
- (step 2) `python3 plugin/tests/run.py test_proof -k proof_kind` → exit 0 · Ran 10 tests in 8.0s (1 classes, 16 at a time; slowest: Proof 7s) / OK [ran] [tree 8a20b6f48425] (2026-10-31T16:29:14Z)
- (step 3) `python3 plugin/tests/run.py test_proof -k rollup_red_first` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree 8a20b6f48425] (2026-10-31T16:29:16Z)
- (step 4) `python3 plugin/tests/run.py test_proof test_not_verified` → exit 0 · Ran 26 tests in 14.4s (4 classes, 16 at a time; slowest: Proof 14s, NotVerified 2s, Palette 0s) / OK [ran] [tree 9d6041d1d114] (2026-10-31T16:29:49Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_cost test_cost_forecast test_docs test_economics test_exam test_export test_genesis test_guard_cases test_paused test_proof test_robustness test_round_g test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [15.76s] [ran] [tree 9d6041d1d114] (2026-10-31T16:31:16Z)
- (step 1) `python3 plugin/tests/run.py test_proof -k review` → exit 0 · Ran 8 tests in 5.7s (1 classes, 16 at a time; slowest: Proof 5s) / OK [ran] [tree 61f976504225] (2026-10-31T16:59:43Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_backlog test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_compact test_conflict_history test_core test_cost test_cost_forecast test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_economics test_edit_cards test_evidence_quality test_exam test_export test_extras test_followups test_genesis test_goal test_graph test_guard test_guard_cases test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_mcp test_metacog test_nudges test_onwrite test_outcomes test_pass4 test_paused test_playbook_use test_plugin_parity test_plugins test_proof test_reasoning test_recall test_replan test_robustness test_round_g test_round_i test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_statusline_ui test_steering test_supply_delta test_taste_ledger test_tidy test_tool_proof test_trust test_ui test_ui_signals test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.92s] [ran] [tree 61f976504225] (2026-10-31T17:03:51Z)
- (step 1) `python3 plugin/tests/run.py test_proof test_not_verified test_exam test_genesis` → exit 0 · Ran 246 tests in 75.7s (32 classes, 16 at a time; slowest: ExamAuthors 75s, ExamGen 61s, Proof 45s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:48:00Z)
- `python3 plugin/tests/run.py test_proof` → ✗ exit 1 · Ran 30 tests in 14.9s (3 classes, 16 at a time; slowest: Proof 14s, Palette 0s, FindRankValue 0s) / FAILED (1 classes: test_proof.Proof) (start tree + this task's tests) [ran] [tree 3612e21a3e3b] (2026-10-31T17:48:46Z)
- `python3 plugin/tests/run.py test_proof` → exit 0 · Ran 30 tests in 18.0s (3 classes, 16 at a time; slowest: Proof 18s, Palette 0s, FindRankValue 0s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:48:46Z)
- (ac 1) `python3 plugin/tests/run.py test_proof -k proof_kind` → exit 0 · Ran 10 tests in 4.7s (1 classes, 16 at a time; slowest: Proof 4s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (ac 2) `python3 plugin/tests/run.py test_proof -k rollup_red_first` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (ac 3) `python3 plugin/tests/run.py test_proof -k unproven_line` → exit 0 · Ran 2 tests in 3.8s (1 classes, 16 at a time; slowest: Proof 4s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (ac 4) `python3 plugin/tests/run.py test_proof -k proof_kind_finish` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Proof 0s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (ac 5) `python3 plugin/tests/run.py test_proof -k proof_kind_next` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (ac 6) `python3 plugin/tests/run.py test_proof -k perf_noise` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed test-first in f2f89238 before merge; T-2352's gate passed it` → PROOF_KINDS by domain, upgrade per row, one unproven_line on four surfaces [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed test-first in f2f89238 before merge; T-2352's gate passed it` → no 'true' fallback; clears matched from the first word, after the last edit; nothing runs automatically [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed test-first in f2f89238 before merge; T-2352's gate passed it` → git failures not memoized; no-base docs unknown; 0 s medians handled [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 MEDIUM, 4 LOW fixed test-first in f2f89238 before merge; T-2352's gate passed it` → cache keyed on done briefs, 40 diffs cap per cold call, cold timing reported [tree 3612e21a3e3b] (2026-10-31T17:49:01Z)
## Log
- 2026-10-31T14:03:14Z created
- 2026-10-31T14:11:13Z criterion 2 text: A step or criterion whose only runs are red counts as proven when the same command ran green later in the task or the red run was an expected one; on 2026-10-31, 227 of fm proof's 351 rows were that case → A step or criterion whose only runs are red counts as proven only when the same command ran green later in the task (a red-then-green pair); a red with no later green stays unproven; on 2026-10-31, 227 of fm proof's 351 rows were red-first steps whose command later ran green
- 2026-10-31T14:22:58Z criterion 5 text: With the queue empty, fm next names the newest unproven row's upgrade command as the next action, so the drive works the rollup down instead of stopping → With the queue empty, fm next names the newest unproven row whose upgrade can run here (its tool present, the tree trusted) as the next action, so the drive works the rollup down; a row waiting on an install or another grant is shown in fm proof as waiting and goes to the final report, never named by fm next again
- 2026-10-31T16:08:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2391.builder.md
- 2026-10-31T16:08:09Z builder slot freed
- 2026-10-31T16:11:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2391.builder.md
- 2026-10-31T16:11:31Z builder slot freed
- 2026-10-31T16:12:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2391.builder.md
- 2026-10-31T16:12:43Z focused
- 2026-10-31T16:12:44Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T16:16:48Z focused
- 2026-10-31T17:43:29Z merged worktree-agent-ac5c97147401cbb1e (8 file(s))
- 2026-10-31T17:43:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac5c97147401cbb1e
- 2026-10-31T17:46:42Z focused
- 2026-10-31T17:48:00Z scope: files outside the globs came from merging foreman/build and the changelog line
- 2026-10-31T17:51:11Z done
- 2026-10-31T17:53:08Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
- research mission-20261031-083836: Request: Mission 7, Genesis gen 1: 6. Verifying anything. Proof beyond unit tests: UI (`fm shot`, `fm flow`), data, docs against code, …
- T-2273 [FEATURE M, done, 3 steps] Unproven rollup (Mission 7, #6): done tasks whose criteria rest on typed or inconclusive evidence, or UI changes with no visual check, …
- research mission-20261031-083836.pack: Mission 7, Genesis gen 1: 6. Verifying anything. Proof beyond unit tests: UI (`fm shot`, `fm flow`), data, docs against code, infr…
## Lessons
- An upgrade hint is a command someone will run: never print a fallback that passes vacuously
## Files touched
- plugin/tests/test_proof.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmexam.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmlanes.py
- plugin/lib/fmmcp.py
- plugin/lib/fmnew.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmtoolproof.py
- plugin/lib/fmwhich.py
- plugin/skills/intake/references/planning.md
- plugin/tests/helpers.py
- plugin/tests/test_backlog.py
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_cli.py
- plugin/tests/test_conflict_history.py
- plugin/tests/test_core.py
- plugin/tests/test_defect_classes.py
- plugin/tests/test_deliberation.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_goal.py
- plugin/tests/test_graph.py
