---
id: T-1134
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/tests/test_claims.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T08:50:21Z
updated: 2026-10-16T09:14:48Z
base: b5973bfe4007dd1d73e09200f11f3193617407ce
base_tree: c8c7e04a2bbbaf0358b3bee60ae9e7d59091c92a
plan0_at: 2026-10-16T09:13:21Z
plan0_scope: [plugin/lib/fmbus.py, plugin/tests/test_claims.py, CHANGELOG.md]
verified: strong
---
# Fm lease drop with no FILE drops every lease this session holds (5 builders today ran it b
## Raw request
> fm lease drop with no FILE drops every lease this session holds (5 builders today ran it bare, got usage, and left leases to expire)
## Interpretation
The builder brief says 'fm lease drop when done', but drop needs FILE arguments, so every builder printed usage and left its leases to expire (5 reports on 2026-10-16). A bare drop should release every lease this session holds in the project.
## Assumptions (confidence)
## Acceptance criteria
- [x] a bare fm lease drop releases every lease this session holds in the project and leaves other sessions' leases — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
In cmd_lease, drop with no target filters out this session's leases in this project. Take still needs targets.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then the bare drop
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 15 tests in 5.5s (3 classes, 16 at a time; slowest: ClaimsReview 5s, Claims 5s, Stop 4s) / FAILED (1 classes) [ran] [tree 6446759ee5fe] (2026-10-16T09:13:36Z)
- (step 1) `python3 plugin/tests/run.py test_claims test_bus` → exit 0 · Ran 30 tests in 6.2s (8 classes, 16 at a time; slowest: Watch 6s, ClaimsReview 5s, Claims 5s) / OK [ran] [tree c3d4c637ecd7] (2026-10-16T09:14:00Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 15 tests in 4.6s (3 classes, 16 at a time; slowest: ClaimsReview 4s, Claims 4s, Stop 3s) / OK [ran] [tree db387db88f44] (2026-10-16T09:14:05Z)
- (audit self) `self: bare drop filters this session's leases in this project only (another session's lease stays, tested); take still needs targets; same lock as before` → no findings [tree db387db88f44] (2026-10-16T09:14:05Z)
## Log
- 2026-10-16T08:50:21Z created
- 2026-10-16T08:51:55Z set scope=['plugin/lib/fmbus.py', 'plugin/tests/test_claims.py', 'CHANGELOG.md']
- 2026-10-16T09:13:21Z focused
- 2026-10-16T09:14:00Z scope: CHANGELOG.md — release note
- 2026-10-16T09:14:48Z done
- 2026-10-16T09:14:48Z committed 67a1b54 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-0777 [FEATURE M, done, 3 steps] Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux — les…
- T-1068 [FEATURE M, done, 3 steps] Lane symbol claims: parallel builders claim the files and symbols they will change on the — lesson: A shared lock table keyed by resour…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_bus.py
## Lessons
- When a brief tells agents to run a command, the command must work in exactly the form the brief gives
## Plan gaps
- failed first: step 1 Test then the bare drop
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
