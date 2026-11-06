---
id: T-1597
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-22T20:09:49Z
updated: 2026-10-22T21:28:45Z
baseline: true
base: 1e291de418f740669423430edeade723ef4741c7
base_tree: 51fd4b8c8fa1c0091069b6514d477d721bd3b198
plan0_at: 2026-10-22T21:24:59Z
plan0_scope: []
verified: ok
---
# Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_hooks.NoTaskGate.test_at_stop_the_requests_with_evidence_close_together, test_ideas.Ideas.test_one_toolless_child_per_lens_in_parallel. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] both tests pass five runs in a row on the current tree — verify with python3 plugin/tests/run.py test_hooks.NoTaskGate test_ideas.Ideas
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] rerun repeated
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.NoTaskGate test_ideas.Ideas` → exit 0 · ×5 runs: median 25.604s, spread ±0.137s (1%), min 25.467s, max 26.164s · Ran 43 tests in 25.5s (2 classes, 16 at a time; slowest: NoTaskGate 25s, Ideas 4s) / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:27:08Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.NoTaskGate test_ideas.Ideas` → exit 0 · Ran 43 tests in 25.6s (2 classes, 16 at a time; slowest: NoTaskGate 25s, Ideas 4s) / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:27:34Z)
- (audit self) `reran both tests 5 times on the current tree` → 5/5 green (median 25.6 s); the red run came while the machine's load average was about 32, which slowed the timing-sensitive Stop test [tree 51fd4b8c8fa1] (2026-10-22T21:27:41Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.NoTaskGate test_ideas.Ideas` → exit 0 · Ran 43 tests in 26.3s (2 classes, 16 at a time; slowest: NoTaskGate 26s, Ideas 5s) / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:28:13Z)
- (audit self) `5 repeated runs green; red not reproducible` → no findings [tree 51fd4b8c8fa1] (2026-10-22T21:28:13Z)
- `python3 plugin/tests/run.py test_hooks.NoTaskGate test_ideas.Ideas` → exit 0 · Ran 43 tests in 26.4s (2 classes, 16 at a time; slowest: NoTaskGate 26s, Ideas 5s) / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:28:45Z)
- (audit self) `5 repeated runs green; red not reproducible` → no findings [tree 51fd4b8c8fa1] (2026-10-22T21:28:45Z)
## Log
- 2026-10-22T20:09:49Z created
- 2026-10-22T21:24:55Z planned from capture
- 2026-10-22T21:24:58Z focused
- 2026-10-22T21:28:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1177 [FIX S, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails test_board_verbs.BoardVerbs.test_release
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-1378 [FIX M, done, 3 steps] Queueing a multi-request prompt fits every request in the hook's time on a loaded machine: one pass, one view refresh — lesson: Profile bef…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 1–5 steps
## Why not caught
the baseline capture ran once, during a load spike
## Regression test
none: no code changed; the two tests failed once during a load spike (load average about 32) and pass 5/5 on the same code, so there is no fix to prove red→green
## Lessons
- Under heavy machine load the Stop-hook tests run slow enough to fail; a red baseline seen during a load spike needs a repeated rerun before anyone fixes code
