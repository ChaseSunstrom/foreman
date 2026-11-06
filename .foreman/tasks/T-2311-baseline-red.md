---
id: T-2311
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T10:25:10Z
updated: 2026-10-31T10:32:27Z
baseline: true
base: f2a42707281219e57f50e0cbbc3f58f49cadb99a
base_tree: 397248500785a9ee79edae8f84ef37131f409070
plan0_at: 2026-10-31T10:27:07Z
plan0_scope: []
verified: strong
---
# fm task evidence --repeat works again: _repeat_runs calls run_command with its own root
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_robustness.Robustness.test_a_mutating_verb_run_twice_changes_nothing_the_second_time, test_verify_strength.Repeat.test_a_failing_run_among_the_repeats_fails_it_with_its_count, test_verify_strength.Repeat.test_a_ui_tasks_receipt_lists_files_in_reading_order, test_verify_strength.Repeat.test_repeat_is_capped_and_bounded_in_time, test_verify_strength.Repeat.test_repeat_records_median_and_spread, test_verify_strength.Repeat.test_timed_out_runs_stay_out_of_the_numbers. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
ship73 went red: T-2303's scripted rename turned _repeat_runs' c.run_command(root, cmd, left) into c.run_command(root_dir, cmd, left, env), names only _bench defines, so every --repeat run raised NameError (test_verify_strength.Repeat); test_robustness's checkpoint-twice failure is checked separately.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task evidence --run CMD --repeat N records the median and spread again — verify with `python3 plugin/tests/run.py test_verify_strength`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Restore _repeat_runs' run_command call to (root, cmd, left); run test_verify_strength and test_robustness
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verify_strength test_robustness` → exit 0 · Ran 21 tests in 46.1s (3 classes, 16 at a time; slowest: Robustness 44s, VerifyStrength 43s, Repeat 20s) / OK [ran] [tree 1b521df84755] (2026-10-31T10:29:17Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_strength` → exit 0 · Ran 18 tests in 42.5s (2 classes, 16 at a time; slowest: VerifyStrength 41s, Repeat 18s) / OK [ran] [tree 1b521df84755] (2026-10-31T10:30:14Z)
- (audit intent) `self-review: the one line T-2303's scripted rename changed outside _bench is restored to c.run_command(root, cmd, left); grep shows root_dir only inside _bench's side() now` → --repeat runs record median and spread again [tree 1b521df84755] (2026-10-31T10:30:14Z)
- (audit edge) `self-review: the one line T-2303's scripted rename changed outside _bench is restored to c.run_command(root, cmd, left); grep shows root_dir only inside _bench's side() now` → test_robustness's checkpoint-twice failure in ship73 passes alone (44 s), so it isn't this change; watched at the next ship [tree 1b521df84755] (2026-10-31T10:30:14Z)
- (audit self) `self-review: the one line T-2303's scripted rename changed outside _bench is restored to c.run_command(root, cmd, left); grep shows root_dir only inside _bench's side() now` → no findings [tree 1b521df84755] (2026-10-31T10:30:14Z)
## Log
- 2026-10-31T10:25:10Z created
- 2026-10-31T10:27:02Z planned from capture
- 2026-10-31T10:27:05Z focused
- 2026-10-31T10:29:18Z scope: plugin/lib/fmcli.py (_repeat_runs)
- 2026-10-31T10:32:20Z done
- 2026-10-31T10:32:27Z committed c7493a76 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2309 [FIX S, done, 1 steps] Guard speed tests time CPU, not the wall clock, so a loaded host can't fail them — lesson: A complexity bar measures CPU (time.process_time…
- T-2305 [FIX S, done, 1 steps] Hooks import no glob: T-2297's leads-record prune lists the folder without a top-level import — lesson: A new top-level import in fmhooks c…
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- similar finished tasks took 1–1 steps
- start here (files T-2309 touched): plugin/tests/test_guard.py
## Regression test
existing: test_verify_strength.Repeat.test_repeat_records_median_and_spread caught it (red in ship73's scratch tree at f2a42707 with NameError: root_dir; green now); no new test needed
## Why not caught
the builder's fm check --affected ran test_evidence_quality (the bench tests) but not test_verify_strength, which holds --repeat's tests in the same fmcli function family; and the builder edited with a script against the brief's Edit-only rule, so the rename spread beyond its function
## Lessons
- A scripted rename spreads past the function it was meant for: Edit one site at a time, or grep every site after
## Files touched
- plugin/lib/fmcli.py
