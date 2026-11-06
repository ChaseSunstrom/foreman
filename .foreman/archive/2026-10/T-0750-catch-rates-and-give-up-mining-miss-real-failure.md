---
id: T-0750
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmfriction.py, plugin/lib/fmcore.py, plugin/tests/test_verifying.py, plugin/tests/test_outcomes.py]
depends_on: []
source: user
created: 2026-10-09T21:28:57Z
updated: 2026-10-09T21:30:37Z
base: f59c73dfa227ea7705cb284de553ab2cca3f1a5a
base_tree: a7b61a747f741e4c2beef321ef5148b339f26de0
verified: strong
---
# Catch rates and give-up mining miss real failures: stored results start '✗ exit N', the code matched 'exit N'
## Raw request
> Catch rates and give-up mining miss real failures: stored results start '✗ exit N', the code matched 'exit N'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] real-format failing evidence counts in catch rates and give-up points — verify with `python3 plugin/tests/run.py -p test_verifying.py -p test_outcomes.py -k CatchRate -k Mining`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests use run_result's real format; parse both through one helper
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_verifying.py -p test_outcomes.py -k CatchRate -k Mining` → ✗ exit 1 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: CatchRate 0s, Mining 0s) / FAILED (2 classes) [ran] [tree 72630103a0f0] (2026-10-09T21:29:06Z)
- (step 1) `python3 plugin/tests/run.py -p test_verifying.py -p test_outcomes.py -k CatchRate -k Mining` → exit 0 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: CatchRate 0s, Mining 0s) / OK [ran] [tree 3abf8f739876] (2026-10-09T21:29:14Z)
- (ac 1) `python3 plugin/tests/run.py -p test_verifying.py -p test_outcomes.py -k CatchRate -k Mining` → exit 0 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: CatchRate 0s, Mining 0s) / OK [ran] [tree dc0b79f3560c] (2026-10-09T21:30:36Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1247 tests in 74.3s (414 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 26s, Bench 23s) / OK [ran] [tree dc0b79f3560c] (2026-10-09T21:30:36Z)
- (audit self) `self: one parser (c.result_exit) now reads run results for catch rates, give-up mining and plan gaps; tests build their rows with c.run_result, the real producer, so the format can't drift from them again` → no findings [tree dc0b79f3560c] (2026-10-09T21:30:36Z)
## Log
- 2026-10-09T21:28:57Z created
- 2026-10-09T21:28:57Z focused
- 2026-10-09T21:30:36Z done
- 2026-10-09T21:30:37Z committed a6c5799 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0261-review-1: No bypass found. [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py changed since it was written]
- research rsi-pass-20261009b: 1. **Answer.** I could ground three improvements. The biggest is that the guard-block log records the wrong part of the command. That made t…
- T-0174 [FIX M, done, 4 steps] Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally — lesson: A cleanup that covers onl…
- decision 2026-09-26: Brainstorm subagents get no tools; the main thread builds one context pack and grounds every idea against the code afterwards
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_friction.py
## Why not caught
none: the T-0658 and T-0697 tests hand-wrote result strings in a format the producer never emits; they now call run_result
## Lessons
- A test fixture that hand-writes a producer's output can pass against a format that never occurs; build fixtures with the producer itself
## Plan gaps
- failed first: step 1 tests use run_result's real format; parse both through one helper
## Files touched
- plugin/tests/test_outcomes.py
- plugin/tests/test_verifying.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmfriction.py
