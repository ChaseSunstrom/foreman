---
id: T-1588
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/tests/test_claims.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T19:20:57Z
updated: 2026-10-22T20:28:45Z
base: 3454f1e56ee78220afd38b4f91f12361dd6c5608
base_tree: f06f7b0cdb4f34eeaf6f5d9751ee4ae786881576
plan0_at: 2026-10-22T20:24:45Z
plan0_scope: [plugin/lib/fmbus.py, plugin/tests/test_bus.py, CHANGELOG.md]
verified: strong
---
# Fm lease take hands a live lease from one lane task to another when both run under the sam
## Raw request
> fm lease take hands a live lease from one lane task to another when both run under the same session id (T-1509's fmcli lease went to T-1510): leases should be keyed by task or lane, not session
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lease take refuses a file another task of the same session holds (naming that task) and both claims coexist with --warn; the same task retaking its own lease still works — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] same-session leases of another task overlap; claims keyed per task
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims` → red as expected (exit 1) · Ran 20 tests in 9.9s (3 classes, 16 at a time; slowest: Claims 10s, ClaimsReview 5s, Stop 3s) / FAILED (1 classes) [ran] [tree 90422f3e9a7a] (2026-10-22T20:26:41Z)
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 20 tests in 13.3s (3 classes, 16 at a time; slowest: Claims 12s, ClaimsReview 8s, Stop 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b1eed4cb9d0e] (2026-10-22T20:27:55Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 20 tests in 11.7s (3 classes, 16 at a time; slowest: Claims 12s, ClaimsReview 7s, Stop 5s) / OK [ran] [tree b1eed4cb9d0e] (2026-10-22T20:27:55Z)
- (step 2) `python3 plugin/tests/run.py test_claims test_bus test_lanes` → exit 0 · Ran 67 tests in 14.0s (14 classes, 16 at a time; slowest: Lanes 14s, Claims 11s, Watch 7s) / OK [ran] [tree b1eed4cb9d0e] (2026-10-22T20:28:09Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 20 tests in 12.1s (3 classes, 16 at a time; slowest: Claims 12s, ClaimsReview 7s, Stop 4s) / OK [ran] [tree b1eed4cb9d0e] (2026-10-22T20:28:22Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 20 tests in 9.5s (3 classes, 16 at a time; slowest: Claims 9s, ClaimsReview 5s, Stop 3s) / OK [ran] [tree dc65d5eb35c0] (2026-10-22T20:28:32Z)
- (audit edge) `self: intent: same-session leases of another task overlap; claims keyed per task · adversary: leases are coordination, not a security boundary; edit-time checks unchanged (lanes edit separate worktrees) · edge: a lease with no task (old entries, the user) behaves as before; old keys without #task stay readable · operator: no install change · maintainer: test_claims red first; test_bus and test_lanes pass` → removing a lane releases its pre-claims and its task's session leases [tree dc65d5eb35c0] (2026-10-22T20:28:32Z)
- (audit self) `self: intent: same-session leases of another task overlap; claims keyed per task · adversary: leases are coordination, not a security boundary; edit-time checks unchanged (lanes edit separate worktrees) · edge: a lease with no task (old entries, the user) behaves as before; old keys without #task stay readable · operator: no install change · maintainer: test_claims red first; test_bus and test_lanes pass` → no findings [tree dc65d5eb35c0] (2026-10-22T20:28:32Z)
## Log
- 2026-10-22T19:20:57Z created
- 2026-10-22T20:24:44Z set scope=['plugin/lib/fmbus.py', 'plugin/tests/test_bus.py', 'CHANGELOG.md']
- 2026-10-22T20:24:45Z focused
- 2026-10-22T20:25:19Z set scope=['plugin/lib/fmbus.py', 'plugin/tests/test_claims.py', 'CHANGELOG.md']
- 2026-10-22T20:25:19Z criterion 1 verify: `python3 plugin/tests/run.py test_bus` → `python3 plugin/tests/run.py test_claims`
- 2026-10-22T20:28:44Z done
- 2026-10-22T20:28:45Z committed 2c7e617b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- research T-1294-review: Verdict: approve with nits.** The diff file holds only the CHANGELOG hunk. I reviewed the real working-tree changes in `fmbus.py`, `fmcode.py` an…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_bus.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
T-1216/T-1416 fixed drop per task but left take's overlap per session
## Lessons
- Identity for coordination must be the unit of work (task or lane), not the session: lanes share sessions
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
