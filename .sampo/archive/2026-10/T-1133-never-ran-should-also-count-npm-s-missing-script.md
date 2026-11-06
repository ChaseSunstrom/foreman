---
id: T-1133
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_never_ran.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T08:40:47Z
updated: 2026-10-16T09:15:48Z
base: 67a1b5409b3aebb3a32007c9a4b017369663948c
base_tree: db387db88f44cdc6cc66547b0330d53f4287ccc7
plan0_at: 2026-10-16T09:14:52Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_never_ran.py, CHANGELOG.md]
verified: strong
---
# Never_ran() should also count npm's 'Missing script: "<name>"' (and yarn/pnpm's equivalent
## Raw request
> never_ran() should also count npm's 'Missing script: "<name>"' (and yarn/pnpm's equivalents) as a run that never reached its check (T-1045's npm test criterion locked red)
## Interpretation
A verify command whose script doesn't exist (npm's 'Missing script: "test"', yarn's 'Command "test" not found', pnpm's 'Missing script') never reached its check, so it shouldn't lock the criterion. That is what happened to T-1045's npm test.
## Assumptions (confidence)
## Acceptance criteria
- [x] never_ran names npm, yarn and pnpm missing-script failures, and the criterion stays editable — verify with `python3 plugin/tests/run.py test_never_ran`
## Non-goals
## Approach (options → choice → why)
Add the three messages to never_ran's patterns, as T-1128 did for 'no tests ran'.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then the patterns
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_never_ran` → ✗ exit 1 · Ran 4 tests in 1.9s (1 classes, 16 at a time; slowest: NeverRanUnlocks 2s) / FAILED (1 classes) [ran] [tree b238d576dfc0] (2026-10-16T09:14:57Z)
- (step 1) `python3 plugin/tests/run.py test_never_ran test_core` → exit 0 · Ran 72 tests in 2.2s (17 classes, 16 at a time; slowest: NeverRanUnlocks 2s, WritesAndLocks 2s, PreToolUse 1s) / OK [ran] [tree 17a0834c5e56] (2026-10-16T09:15:08Z)
- `python3 plugin/tests/run.py test_never_ran` → ✗ exit 1 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: NeverRanUnlocks 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7f52c0c5b488] (2026-10-16T09:15:14Z)
- `python3 plugin/tests/run.py test_never_ran` → exit 0 · Ran 4 tests in 2.1s (1 classes, 16 at a time; slowest: NeverRanUnlocks 2s) / OK [ran] [tree 7f52c0c5b488] (2026-10-16T09:15:14Z)
- (ac 1) `python3 plugin/tests/run.py test_never_ran` → exit 0 · Ran 4 tests in 1.9s (1 classes, 16 at a time; slowest: NeverRanUnlocks 2s) / OK [ran] [tree 7f52c0c5b488] (2026-10-16T09:15:16Z)
- (audit self) `self: three package managers' own missing-script messages only (unambiguous phrases); a real test failure under npm test still locks (tested)` → no findings [tree 7f52c0c5b488] (2026-10-16T09:15:16Z)
## Log
- 2026-10-16T08:40:47Z created
- 2026-10-16T08:51:56Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_never_ran.py', 'CHANGELOG.md']
- 2026-10-16T09:14:52Z focused
- 2026-10-16T09:15:09Z scope: CHANGELOG.md — release note
- 2026-10-16T09:15:47Z done
- 2026-10-16T09:15:48Z committed d19ea2c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0985 [FIX M, done, 2 steps] A run that never reached the check doesn't lock a criterion: fm task ac edit can fix a wrong verify path — lesson: A lock meant to stop wea…
- T-1049 [FEATURE M, done, 3 steps] Dependency-install check in the guard: a new npm/pip/cargo package named in an install get — lesson: A hook that touches the network ne…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- Each runner says 'nothing to run' its own way; the lock needs all of them
## Plan gaps
- failed first: step 1 Test then the patterns
## Files touched
- plugin/tests/test_never_ran.py
- plugin/lib/fmcore.py
- CHANGELOG.md
