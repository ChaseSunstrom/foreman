---
id: T-3281
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T02:28:23Z
updated: 2026-11-06T04:54:50Z
builder: 2026-11-06T02:28:40Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-aea2002317a95e045
lane_branch: worktree-agent-aea2002317a95e045
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:29:13Z
plan0_scope: []
predict_noted: 2026-11-06T04:41:42Z
builder_returned: 2026-11-06T04:49:04Z
---
# Moon C-001120: nightly spar (spar.py) feeds mutated hook payloads and CLI args to a temp home, files any traceback as a FIX with the reproducer
## Raw request
> Moon C-001120: nightly spar (spar.py) feeds mutated hook payloads and CLI args to a temp home, files any traceback as a FIX with the reproducer
## Interpretation
Reading 1 (chosen): the rival is a seeded mutator of the real hook payload shapes (drill.DAY plus one per HANDLERS event) run in drill.Day's temp home; a traceback in output is a crash and becomes a FIX with the reproducer. Reading 2 (ruled out): coverage-guided fuzzing of every CLI verb, because it needs unbounded time and the hooks are the entry points Claude Code feeds; CLI verbs get a small args slice only. Existing: test_guard_diff fuzzes only the Bash guard text, drill.py plants state faults but never mutates inputs; this adds the input side.
## Assumptions (confidence)
## Acceptance criteria
- [ ] spar.mutate(seed payload, rng) yields malformed, huge, unicode, missing-field variants, same seed same list — verify with `python3 plugin/tests/run.py test_spar`
- [ ] spar.run(seed, budget_s) runs the mutants through drill.Day hooks, stops at the time bound, and returns a crash (event, payload, stderr tail) for a planted traceback — verify with `python3 plugin/tests/run.py test_spar`
- [ ] sampo spar --capture files one deduped FIX per crash with the reproducer; night.jobs lists 'spar' at idle priority — verify with `python3 plugin/tests/run.py test_spar`
## Non-goals
## Approach (options → choice → why)
1. New spar.py reusing drill.Day and drill.crash, mutators in stdlib random, capture via eco.capture_once, one night job. Likely outcome: small, no big-file collisions, finds real tracebacks.
2. Extend drill.py with a spar mode. Likely outcome: fewer files but mixes two jobs and collides with other drill edits.
3. Record real payloads from hooks.log and mutate them. fails if: payloads are not logged (they are redacted and not stored), so there is nothing to replay.
4. Do less: hooks only, no CLI args, no night job. Likely outcome: misses the nightly part of the moon.

Choice 1 (85%): reuses the temp-home harness and crash detector already proven by drill; seeds come from the shapes in DAY and HANDLERS. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Test first: mutate determinism, planted-crash detection, time bound, capture dedupe  <- CURRENT
2. [x] Write plugin/lib/sampo/spar.py: seeds from drill.DAY plus one payload per HANDLERS event; mutate; run via drill.Day and drill.crash; capture via eco.capture_once
3. [x] Register verb sampo spar in cli.py and a free job in night.jobs (nice 19, 120 s bound); CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T04:41:05Z step 1/3: Test first: mutate determinism, planted-crash detection, time bound, capture dedupe
- git: worktree-agent-aea2002317a95e045; 5 uncommitted: MASTER.md, docs/map/files-lib-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/spar.py, plugin/tests/test_spar.py
- touched since last checkpoint: plugin/tests/test_spar.py, plugin/lib/sampo/spar.py, plugin/lib/sampo/cli.py, MASTER.md, docs/map/files-lib-1.md
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_spar` → ✗ exit 1 (never ran: no tests ran) · Ran 1 tests in 15.5s (2 jobs, 16 at a time; slowest: Page 13s, loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 3104040f1eb8] [world 2f1906870a] (2026-11-06T02:34:47Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_spar` → ✗ exit 1 · Ran 14 tests in 76.7s (12 jobs, 16 at a time; slowest: Page 65s, Cli 44s, Capture.test_a_different_traceback_is_a_different_fix 10s) / FAILED (1 classes: test_live_page.Page) [ran] [tree c8f546e08b0b] [world 2f1906870a] (2026-11-06T02:41:42Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_spar.` → exit 0 · Ran 13 tests in 30.9s (13 jobs, 16 at a time; slowest: Cli 20s, Capture.test_the_brief_names_its_signature_and_a_runnable_reproducer 9s, NightJob 7s) / OK [ran] [tree c8f546e08b0b] [world 2f1906870a] (2026-11-06T02:43:53Z)
- (step 3) `PYTHON_CPU_COUNT=2 python3 plugin/tests/run.py test_spar.` → exit 0 · Ran 13 tests in 51.8s (13 jobs, 2 at a time; slowest: Cli 49s, NightJob 3s, Run.test_a_zero_budget_is_a_well_formed_empty_report 3s) / OK [ran] [tree f3341dee6e28] [world 2f1906870a] (2026-11-06T03:08:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_night test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_spar test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2121 tests in 3649.7s (718 jobs, 16 at a time; slowest: Repairs 486s, GenesisLive 486s, OutcomeEscalation 485s) / FAILED (43 classes: test_cli.TaskLifecycle, test_proof.Proof, test_cli.CaptureAndI [ran] [tree f3341dee6e28] [world 2f1906870a] (2026-11-06T03:45:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_night test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_spar test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2405 tests in 3983.6s (716 jobs, 2 at a time; slowest: TaskLifecycle 282s, Proof 262s, Parallel 145s) / FAILED (2 classes: test_doctor.Checks, test_night.Night) [ran] [tree f3341dee6e28] [world 2f1906870a] (2026-11-06T04:14:48Z)
- (step 3) `PYTHON_CPU_COUNT=2 python3 plugin/tests/run.py test_spar. test_night.` → exit 0 · Ran 58 tests in 40.0s (37 jobs, 2 at a time; slowest: Cli 8s, Night.test_a_night_records_the_tasks_the_queue_closed_and_the_digest_says_so 7s, NightGuards 6s) / OK [ran] [tree a030bfee5af2] [world 2f1906870a] (2026-11-06T04:18:17Z)
- (step 3) `python3 plugin/tests/run.py test_spar.` → exit 0 · Ran 26 tests in 21.3s (8 jobs, 16 at a time; slowest: Cli.test_fm_spar_reports_a_bounded_run_at_idle_priority 20s, Cli.test_the_replay_flag_reruns_one_mutant_in_a_sandbox 16s, Run 3s) / OK [ran] [tree 025f0bab46a8] [world 2f1906870a] (2026-11-06T04:42:35Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_night test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_spar test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2418 tests in 343.7s (1445 jobs, 16 at a time; slowest: LeanKindGateHookDelay 152s, LeanKindGateSessionLine 140s, LeanKindGateGuardAllow 137s) / FAILED (2 classes: test_docs.MapShards, test_docs.P [ran] [tree 025f0bab46a8] [world 2f1906870a] (2026-11-06T04:54:50Z)
## Log
- 2026-11-06T02:28:23Z created
- 2026-11-06T02:28:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3281.builder.md
- 2026-11-06T02:29:12Z focused
- 2026-11-06T02:29:13Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
