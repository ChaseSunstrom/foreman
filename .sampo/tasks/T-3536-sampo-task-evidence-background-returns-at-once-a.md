---
id: T-3536
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T21:55:01Z
updated: 2026-11-07T00:52:13Z
lane: ~/.claude/foreman.lanes/T-3536
lane_branch: foreman/T-3536
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:37:42Z
plan0_scope: []
---
# Sampo task evidence --background returns at once and sampo task wait ID prints the…
## Raw request
> FEATURE: sampo task evidence --background returns at once and sampo task wait ID prints the recorded result: 36 builder calls ended in a timed-out tail (exit 124) waiting on foreground evidence runs past the 120 s tool limit (cli.py:823-826)
## Interpretation
Reading 1: --background starts the same foreground evidence run detached (it records its own evidence when it ends), prints where and how to wait, and returns at once; sampo task wait ID [--timeout S] blocks until that task's pending background runs end and prints their results (0 all passed, 1 any failed, 124 still running at the timeout). Reading 2 (ruled out): only a shorter default timeout on the foreground run; it would cut long test runs short instead of letting them finish.
## Assumptions (confidence)
## Acceptance criteria
- [ ] --background returns at once and the detached run records the evidence; sampo task wait prints its result with exit 0 on pass, 1 on fail, 124 on timeout — verify with `nice -n 10 python3 plugin/tests/run.py test_evidence_background`
## Non-goals
## Approach (options → choice → why)
1) Re-exec the same sampo task evidence argv minus --background, detached (start_new_session), under a sh wrapper that writes its exit code beside a marker JSON in the project state dir; wait polls the markers. Likely outcome: one recording path, no daemon; fails if: the child is killed (wait reports it lost). 2) use what exists: Claude Code's run_in_background on the foreground call; fails if: the builder forgets it (36 timed-out calls show it does) and there is no sampo verb to read the result. 3) do less: a help line telling builders to background long runs; fails if: the same 36 misses keep happening. 4) a daemon job queue; fails if: one more long-lived process to keep alive. Choice 1 (85%): reuses the foreground path unchanged, survives the caller's exit, plain files wait reads and clears.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for --background and task wait
2. [x] Implement --background (detached re-exec + marker) and sampo task wait
3. [x] Builder-facing docs/help line for background evidence
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_evidence_background` → red as expected (exit 1) · Ran 4 tests in 2.9s (1 jobs, 16 at a time; slowest: Background 1s) / FAILED (1 classes: test_evidence_background.Background) [ran] [tree a36d540d6404] [world 2f1906870a] (2026-11-07T00:37:52Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_evidence_background` → ✗ exit 1 · Ran 4 tests in 22.2s (1 jobs, 16 at a time; slowest: Background 5s) / FAILED (1 classes: test_evidence_background.Background) [ran] [tree 548d77834ece] [world 2f1906870a] (2026-11-07T00:38:51Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_evidence_background` → exit 0 · Ran 4 tests in 65.2s (4 jobs, 16 at a time; slowest: Background.test_wait_gives_124_while_it_runs_then_the_result 2s, Background.test_it_returns_before_the_run_ends_and_wait_prints_the_recorded_pass 2 [ran] [tree fc29ea54b53f] [world 2f1906870a] (2026-11-07T00:41:56Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_docs test_which test_map test_audit test_cli_ergonomics` → ✗ exit 1 · Ran 208 tests in 31.9s (52 jobs, 16 at a time; slowest: Fences 17s, DesignLens 17s, AuditRun 9s) / FAILED (1 classes: test_docs.PluginFiles) [ran] [tree 8f1e9f30d214] [world 2f1906870a] (2026-11-07T00:42:49Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_docs test_which test_map test_audit test_cli_ergonomics test_doctor` → exit 0 · Ran 327 tests in 78.6s (160 jobs, 16 at a time; slowest: Fences.test_a_panel_that_quits_or_hangs_never_passes 9s, ViewsRepair 9s, LockProbe 5s) / OK [ran] [tree 40773ff9a269] [world 2f1906870a] (2026-11-07T00:44:18Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_evidence_background` → exit 0 · Ran 4 tests in 3.6s (1 jobs, 16 at a time; slowest: Background 3s) / OK [ran] [tree 40773ff9a269] [world 2f1906870a] (2026-11-07T00:44:27Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_evidence_background` → exit 0 · Ran 6 tests in 15.9s (1 jobs, 16 at a time; slowest: Background 8s) / OK [ran] [tree e73d5558d80b] [world 2f1906870a] (2026-11-07T00:51:04Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_evidence_background test_evidence_quality test_finish_reuse` → exit 0 · Ran 28 tests in 62.0s (11 jobs, 16 at a time; slowest: Bench 12s, FinishReuse 6s, Assume 3s) / OK [ran] [tree e73d5558d80b] [world 2f1906870a] (2026-11-07T00:52:13Z)
## Log
- 2026-11-06T21:55:01Z created
- 2026-11-07T00:31:15Z planned: it has criteria and steps
- 2026-11-07T00:37:22Z lane: ~/.claude/foreman.lanes/T-3536 on foreman/T-3536
- 2026-11-07T00:37:40Z focused
- 2026-11-07T00:37:42Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Docs: task-first pages, examples that run (fm playbooks show context/docs)
- research T-2878-taxonomy: Louhi's smith arm, `sampo exam run RUN --agent smith --model PROFILE --split all --limit 44`, on seeded exam runs of the
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-10-30: [revisited: long-horizon tier is the deciding end-of-run score] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run]…
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
