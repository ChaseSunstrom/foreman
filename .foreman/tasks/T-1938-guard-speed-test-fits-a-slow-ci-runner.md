---
id: T-1938
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T08:31:49Z
updated: 2026-10-29T08:34:37Z
base: fc8f43743b589689e8ff4e599ad77f07d1ede0d0
base_tree: d38640e44997adedb3bd5dba0e035d4598c99bf6
plan0_at: 2026-10-29T08:31:50Z
plan0_scope: []
verified: strong
---
# Guard speed test fits a slow CI runner
## Raw request
> Guard speed test fits a slow CI runner
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] The cd speed test passes with headroom for a 3x slower runner and still fails at the old 7 s cost — verify with `python3 plugin/tests/run.py test_guard -k unfollowable_cds`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Measure local CPU time, set the cap with headroom
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 301 tests in 17.7s (88 classes, 16 at a time; slowest: Mutation 17s, GuardAgainstBash 15s, Trust 10s) / OK [ran] [tree d6d428c9e8bc] (2026-10-29T08:33:40Z)
- (ac 1) `python3 plugin/tests/run.py test_guard -k unfollowable_cds` → exit 0 · Ran 301 tests in 19.4s (88 classes, 16 at a time; slowest: Mutation 18s, GuardAgainstBash 18s, Trust 10s) / OK [ran] [tree d6d428c9e8bc] (2026-10-29T08:34:11Z)
- (audit edge) `Test-only change: the CPU-time cap goes from 2 to 6 s; local run is about 0.5 s, CI measured 2.6 s, the bug it guards cost 7-17 s` → at the old cost (7 s for 2 substitutions) the test still fails, so it still catches the blowup [tree d6d428c9e8bc] (2026-10-29T08:34:11Z)
- (audit adversary) `Test-only change: the CPU-time cap goes from 2 to 6 s; local run is about 0.5 s, CI measured 2.6 s, the bug it guards cost 7-17 s` → no guard code changes; both refusal assertions in the test are untouched [tree d6d428c9e8bc] (2026-10-29T08:34:11Z)
- (audit self) `Test-only change: the CPU-time cap goes from 2 to 6 s; local run is about 0.5 s, CI measured 2.6 s, the bug it guards cost 7-17 s` → no findings [tree d6d428c9e8bc] (2026-10-29T08:34:11Z)
## Log
- 2026-10-29T08:31:49Z created
- 2026-10-29T08:31:50Z focused
- 2026-10-29T08:34:33Z done
- 2026-10-29T08:34:37Z committed a4060741 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0133 [PERFORMANCE M, done, 3 steps] Agents feel slow: parallel test runner for the gate, measured before and after — lesson: Measure the wait before optimising: one se…
- T-1280 [FIX S, done, 2 steps] Hook paths that start fm under a time limit are tested with every Python start slowed by 0.4 s — lesson: A time budget for a child process …
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-1378 [FIX M, done, 3 steps] Queueing a multi-request prompt fits every request in the hook's time on a loaded machine: one pass, one view refresh — lesson: Profile bef…
## Regression test
none: a load-dependent timing failure on a slower CI runner (check run 123338888828: 2.6 s against 2); it doesn't reproduce on this box
## Why not caught
The cap was set from this box's speed only; CI runners are about 5x slower
## Lessons
- Set timing caps between the slowest runner's time and the regression's cost, not just above the local time
## Files touched
- plugin/tests/test_guard.py
