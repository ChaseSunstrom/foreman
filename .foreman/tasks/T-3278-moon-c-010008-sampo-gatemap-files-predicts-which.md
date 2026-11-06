---
id: T-3278
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/gatemap.py, plugin/tests/test_gatemap.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:28:07Z
updated: 2026-11-06T04:33:32Z
builder: 2026-11-06T02:28:41Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a0ee7e1bd75bbc04e
lane_branch: worktree-agent-a0ee7e1bd75bbc04e
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:54Z
plan0_scope: [plugin/lib/sampo/gatemap.py, plugin/tests/test_gatemap.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:33:32Z
---
# Moon C-010008: sampo gatemap FILES predicts which gates a self-change will hit, from past refusals, with the smallest fix
## Raw request
> Moon C-010008: sampo gatemap FILES predicts which gates a self-change will hit, from past refusals, with the smallest fix
## Interpretation
Reading 1 (chosen): friction.classes already counts today's refusals by class, but keeps no trigger (file, rule, command) and predicts nothing. Add a hidden dependency map: history of refusals keyed gate -> triggers, then a before-edit/close forecast for a file list with the smallest fix. Partial: friction.py:404 classes() and selfgate.py:489 self_change_refused rows exist; this adds the trigger map and prediction. Reading 2 (ruled out): a full simulator that runs the gates early. That is selfgate.gate itself, minutes of bench, so it defeats the point of a cheap forecast.
## Assumptions (confidence)
## Acceptance criteria
- [ ] gatemap.learn(p) turns past refusals (self_change_refused rows, merge_refused reasons, guard blocks, failed closes) into per-gate records of trigger (file, rule or command) and count — verify with `python3 plugin/tests/run.py test_gatemap`
- [ ] gatemap.predict(files) names the gates a change will likely hit (self-change timing/footprint/verbs/guard-case, tests owed, CHANGELOG/docs owed) with confidence from history and one smallest fix each — verify with `python3 plugin/tests/run.py test_gatemap`
- [ ] sampo gatemap [FILES] [--json] runs from the git diff when no files are given and prints the gates and fixes in under 15 lines — verify with `python3 plugin/tests/run.py test_gatemap`
## Non-goals
## Approach (options → choice → why)
1. New gatemap.py: learn() from ledger and events, a path-rule table, predict(files), one lazy verb. Likely outcome: cheap forecast, one new file, little collision with other lanes.
2. Extend friction.classes with triggers and a predict flag inside friction.py. Likely outcome: smaller diff, but friction.py is shared and grows past its focus.
3. Run selfgate.gate in a dry mode before each edit. fails if: the bench takes minutes and loads the CPU every time, the exact cost T-3252 is trying to avoid.
4. Do less: only print the static rule table, no learning from history. Likely outcome: fast, but misses which gates actually bit, so no confidence.

Choice 1 (85%): separate module keeps lanes apart and the history gives the confidence. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] Write test_gatemap.py first: fake ledger events and a file list, expect gates, counts and fixes  <- CURRENT
2. [x] Add plugin/lib/sampo/gatemap.py: learn (read-only over ledger_events and events.jsonl), a small path-rule table reusing selfgate.needs_timing/_judged/_benched, predict, cmd_gatemap
3. [x] Register the gatemap verb lazily in cli.py next to friction; CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T03:46:03Z step 1/3: Write test_gatemap.py first: fake ledger events and a file list, expect gates, counts and fixes
- git: worktree-agent-a0ee7e1bd75bbc04e; 6 uncommitted: MASTER.md, docs/map/files-lib-2.md, plugin/lib/sampo/cli.py, plugin/lib/fmgatemap.py, plugin/lib/sampo/gatemap.py, plugin/tests/test_gatemap.py
- touched since last checkpoint: plugin/lib/sampo/gatemap.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_gatemap` → ✗ exit 1 · Ran 5 tests in 4.5s (1 jobs, 16 at a time; slowest: Gatemap 3s) / FAILED (1 classes: test_gatemap.Gatemap) [ran] [tree c6efc3d4f7c1] [world 2f1906870a] (2026-11-06T02:33:53Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_gatemap` → exit 0 · Ran 6 tests in 17.4s (6 jobs, 16 at a time; slowest: Gatemap.test_the_verb_prints_gates_and_fixes_in_under_15_lines_and_json_on_request 10s, Gatemap.test_a_cached_hook_map_decides_the_timing_bench_and [ran] [tree a6d45ab44d73] [world 2f1906870a] (2026-11-06T02:38:53Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_gatemap` → exit 0 · Ran 6 tests in 24.8s (6 jobs, 16 at a time; slowest: Gatemap.test_a_cached_hook_map_decides_the_timing_bench_and_a_bad_path_is_refused 8s, Gatemap.test_the_verb_prints_gates_and_fixes_in_under_15_line [ran] [tree e8ab67e1724a] [world 2f1906870a] (2026-11-06T02:40:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_gatemap test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2156 tests in 3646.6s (698 jobs, 16 at a time; slowest: GenerationReview 486s, GoalReview 486s, Approvals 485s) / FAILED (42 classes: test_cli.TaskLifecycle, test_proof.Proof, test_cli.CaptureAndI [ran] [tree e8ab67e1724a] [world 2f1906870a] (2026-11-06T03:41:06Z)
## Log
- 2026-11-06T02:28:07Z created
- 2026-11-06T02:28:08Z set scope=['plugin/lib/sampo/gatemap.py', 'plugin/tests/test_gatemap.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:28:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3278.builder.md
- 2026-11-06T02:28:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3278.builder.md
- 2026-11-06T02:28:54Z focused
- 2026-11-06T02:28:54Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:35:55Z scope: plugin/lib/fmgatemap.py added, the fm shim the standing rule requires for a new plugin/lib module (fmfriction.py is the model)
- 2026-11-06T02:39:40Z scope: MASTER.md bullet and docs/map/files-lib-2.md line for the new module (the standing rule: a new plugin/lib module needs its fm shim, a MASTER.md bullet and a docs/map line)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-3276 [FEATURE M, active, 4 steps] Moon C-000717: 'sampo audit ahead ID' lists the objections reviewers most likely raise on this diff, before the review
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar finished tasks took 4–9 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
