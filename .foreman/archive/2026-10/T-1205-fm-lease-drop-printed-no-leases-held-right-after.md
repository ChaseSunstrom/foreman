---
id: T-1205
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:48:42Z
updated: 2026-10-16T14:52:12Z
base: 9373e4b9f5b64be8a1b2acce1612b15c459c3f7c
base_tree: a981aad9e726056e2988e69f4e360d1b11f9dede
plan0_at: 2026-10-16T14:48:58Z
plan0_scope: []
verified: strong
---
# fm lease drop says how many leases it released, not only what's left
## Raw request
> fm lease drop printed 'No leases held.' right after a builder took leases in the same session (T-1194 builder): check whether lease take and drop agree on the holder key in a worktree
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lease drop (bare or with targets) prints 'Dropped N lease(s)' before the remaining list, so 'No leases held.' after a drop no longer reads as if nothing had been taken — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test: take two, bare drop says Dropped 2; drop of an unheld target says Dropped 0
2. [x] Count before and after in cmd_lease's drop branches
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 16 tests in 8.0s (3 classes, 16 at a time; slowest: Claims 7s, ClaimsReview 7s, Stop 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b5cfc8dc8e0b] (2026-10-16T14:49:34Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 5.4s (3 classes, 16 at a time; slowest: Claims 5s, ClaimsReview 5s, Stop 3s) / OK [ran] [tree b5cfc8dc8e0b] (2026-10-16T14:49:34Z)
- (step 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 25.4s (3 classes, 16 at a time; slowest: ClaimsReview 25s, Claims 25s, Stop 14s) / OK [ran] [tree 7267dea232e1] (2026-10-16T14:50:08Z)
- (step 2) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 24.1s (3 classes, 16 at a time; slowest: Claims 23s, ClaimsReview 22s, Stop 13s) / OK [ran] [tree 7267dea232e1] (2026-10-16T14:50:34Z)
- (ac 1) `python3 plugin/tests/run.py test_lease` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.7s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 7267dea232e1] (2026-10-16T14:50:49Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 11.5s (3 classes, 16 at a time; slowest: Claims 11s, ClaimsReview 11s, Stop 9s) / OK [ran] [tree 7267dea232e1] (2026-10-16T14:50:49Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 5.2s (3 classes, 16 at a time; slowest: Claims 5s, ClaimsReview 5s, Stop 3s) / OK [ran] [tree 7267dea232e1] (2026-10-16T14:51:25Z)
- (audit self) `self: count is taken under the same lock as the drop; only drop prints it; --json gains a dropped field; list and take output unchanged` → no findings [tree 7267dea232e1] (2026-10-16T14:51:25Z)
## Log
- 2026-10-16T14:48:42Z created
- 2026-10-16T14:48:57Z planned from capture
- 2026-10-16T14:48:58Z focused
- 2026-10-16T14:50:35Z scope: CHANGELOG lines (this one and T-1202's, which closed without one)
- 2026-10-16T14:51:19Z criterion 1 verify: `python3 plugin/tests/run.py test_lease` → `python3 plugin/tests/run.py test_claims`
- 2026-10-16T14:51:20Z steer: criterion 1 named a test module that doesn't exist (test_lease); the lease tests live in test_claims
- 2026-10-16T14:52:11Z done
- 2026-10-16T14:52:12Z committed 06d79fdc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1134 [FIX S, done, 1 steps] Fm lease drop with no FILE drops every lease this session holds (5 builders today ran it b — lesson: When a brief tells agents to run a com…
- T-1068 [FEATURE M, done, 3 steps] Lane symbol claims: parallel builders claim the files and symbols they will change on the — lesson: A shared lock table keyed by resour…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
