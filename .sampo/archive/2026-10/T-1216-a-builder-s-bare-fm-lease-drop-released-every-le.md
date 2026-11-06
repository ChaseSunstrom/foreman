---
id: T-1216
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T15:22:26Z
updated: 2026-10-16T16:17:56Z
base: 82ad225c802cd5bb99abdd7cec1ca6314829c814
base_tree: 86abab6a5ec76b3bb92d724b38d980bb21d8c65c
plan0_at: 2026-10-16T16:14:05Z
plan0_scope: []
verified: strong
---
# fm lease drop releases only the current task's leases, and a file's drop releases all its symbols
## Raw request
> A builder's bare fm lease drop released every lease of the parent session (19, including the main thread's T-1206/T-1209/T-1203 leases), because lanes share the session id; a bare drop should release only the current task's leases, and fm lease take on a lease the same task already holds should succeed quietly, not exit 2 with an overlap list
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a bare fm lease drop releases the active task's leases of this session and leaves another task's (a lane shares the session id); fm lease drop FILE releases every symbol lease this session holds on FILE — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: two tasks in one session, bare drop under the second; symbol leases dropped by file
2. [x] Scope the bare drop to the active task; a file drop matches every symbol
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 18 tests in 9.4s (3 classes, 16 at a time; slowest: Claims 9s, ClaimsReview 6s, Stop 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d309c71273dc] (2026-10-16T16:14:53Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 18 tests in 13.2s (3 classes, 16 at a time; slowest: Claims 13s, ClaimsReview 9s, Stop 6s) / OK [ran] [tree d309c71273dc] (2026-10-16T16:14:53Z)
- (step 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 18 tests in 16.7s (3 classes, 16 at a time; slowest: Claims 16s, ClaimsReview 13s, Stop 9s) / OK [ran] [tree 3297e239ab6f] (2026-10-16T16:15:17Z)
- (step 2) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 18 tests in 28.7s (3 classes, 16 at a time; slowest: Claims 28s, ClaimsReview 22s, Stop 12s) / OK [ran] [tree 3297e239ab6f] (2026-10-16T16:15:47Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 18 tests in 12.8s (3 classes, 16 at a time; slowest: Claims 12s, ClaimsReview 10s, Stop 8s) / OK [ran] [tree 3297e239ab6f] (2026-10-16T16:16:01Z)
- (audit self) `self: the bare drop keeps leases of other tasks in the same session (and drops task-less ones with the active task's); a file drop matches every symbol only when no symbol is named; take is unchanged` → no findings [tree 3297e239ab6f] (2026-10-16T16:16:01Z)
## Log
- 2026-10-16T15:22:26Z created
- 2026-10-16T15:28:28Z more from the T-1211 builder: dropping by file leaves the per-function leases recorded after each edit, so a lane can't fully release its own claims; a bare drop in a lane should release every lease of the lane's task
- 2026-10-16T16:13:52Z third occurrence: the T-1224 builder's bare fm lease drop released all 25 of the session's leases, including the main thread's T-1220 site/ leases
- 2026-10-16T16:14:04Z planned from capture
- 2026-10-16T16:14:05Z focused
- 2026-10-16T16:15:48Z scope: CHANGELOG line
- 2026-10-16T16:17:55Z done
- 2026-10-16T16:17:56Z committed 066afb9d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1134 [FIX S, done, 1 steps] Fm lease drop with no FILE drops every lease this session holds (5 builders today ran it b — lesson: When a brief tells agents to run a com…
- T-1068 [FEATURE M, done, 3 steps] Lane symbol claims: parallel builders claim the files and symbols they will change on the — lesson: A shared lock table keyed by resour…
- T-1205 [FIX S, done, 2 steps] fm lease drop says how many leases it released, not only what's left
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
