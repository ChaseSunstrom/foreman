---
id: T-3151
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:37:03Z
updated: 2026-11-05T06:43:49Z
base: c51a8108fbfb8427437080e3bdf3819d4a5fe922
base_tree: af7f2ca2c607bf33ebb286cca787815f3b59d785
plan0_at: 2026-11-05T06:25:52Z
plan0_scope: []
verified: ok
unproven: [perf-typed]
---
# NoTaskGate's 30 subprocess-heavy tests run serially in one class (35-55 s): split it into classes of about ten so run.py runs them in parallel
## Raw request
> NoTaskGate tests take 35-55 s each run: find the slow setup and cut it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_hooks' NoTaskGate tests live in three or more classes with the same tests (the count of test methods unchanged), and the slowest of them takes under 20 s in a run of test_hooks — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] measure the class's time now, then split it and measure again
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.NoTaskGate test_hooks.NoTaskGateClose test_hooks.NoTaskGateRefusals` → exit 0 · Ran 31 tests in 45.5s (3 classes, 16 at a time; slowest: NoTaskGateClose 44s, NoTaskGateRefusals 30s, NoTaskGate 29s) / OK [ran] [tree 8ad54d2bd1b8] [world 2f1906870a] (2026-11-05T06:33:31Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.NoTaskGate test_hooks.NoTaskGateMulti test_hooks.NoTaskGateClose test_hooks.NoTaskGateQueue test_hooks.NoTaskGateRefusals test_hooks.NoTaskGateKinds` → exit 0 · Ran 31 tests in 12.8s (6 classes, 16 at a time; slowest: NoTaskGateMulti 12s, NoTaskGateClose 10s, NoTaskGateKinds 9s) / OK [ran] [tree 6531bc5f1ec0] [world 2f1906870a] (2026-11-05T06:38:35Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 101.5s (36 classes, 16 at a time; slowest: Stop 101s, PreToolUse 43s, SessionStart 41s) / OK [ran] [tree 6531bc5f1ec0] [world 2f1906870a] (2026-11-05T06:40:21Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 69.7s (36 classes, 16 at a time; slowest: Stop 69s, PreToolUse 37s, SessionStart 36s) / OK [ran] [tree dae032d6b1fe] [world 2f1906870a] (2026-11-05T06:41:59Z)
- (audit self) `self: the tests moved unchanged into six classes sharing NoTaskGateKit (pre, first_task_session, HEADLESS); a mixin, not a base class, so no test runs twice; 31 tests before and after; nothing else named the class` → no findings [tree dae032d6b1fe] (2026-11-05T06:41:59Z)
## Log
- 2026-11-05T05:37:03Z created
- 2026-11-05T06:09:06Z planned from capture
- 2026-11-05T06:25:51Z focused
- 2026-11-05T06:43:18Z done
- 2026-11-05T06:43:21Z committed cfa46b09 (2 files)
- 2026-11-05T06:43:49Z open: the 57.9 s -> 12.8 s numbers are typed, not benched; a back-to-back --bench of HEAD^ vs HEAD on the same load is owed, run after the merge queue drains (main-checkout runs are held so merges land)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1597 [FIX S, done, 1 steps] Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load — lesson: Under heavy machine load the …
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Measurements
NoTaskGate wall time: 57.9 s (one class, 31 tests) → 12.8 s (six classes, 31 tests); slowest class 57 s → 12 s
## Files touched
- plugin/tests/test_hooks.py
- CHANGELOG.md
