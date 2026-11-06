---
id: T-1416
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T18:57:45Z
updated: 2026-10-21T19:48:18Z
base: 63b5f2c9f55460bb474fa1c8099d7cf2a58ab2be
base_tree: cb4ab27e7769ef8105323fa02de6e74bde784b83
plan0_at: 2026-10-21T19:44:16Z
plan0_scope: []
verified: strong
---
# A file-named fm lease drop frees only the calling task's leases, like a bare drop
## Raw request
> fm lease drop releases by session, so a builder lane's drop frees other parallel lanes' leases (all lanes share the main session id); drop only the calling task's leases
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] in one session, task Two's fm lease drop a.py frees Two's a.py::g and keeps task One's a.py::f — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_claims beside T-1216's bare-drop test, then one shared 'mine' predicate in fmbus.cmd_lease for both drop paths
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 19 tests in 19.9s (3 classes, 16 at a time; slowest: Claims 19s, ClaimsReview 12s, Stop 8s) / FAILED (1 classes) [ran] [tree a106c5fd5b1c] (2026-10-21T19:44:44Z)
- (step 1) `python3 plugin/tests/run.py test_claims test_bus` → exit 0 · Ran 35 tests in 24.6s (8 classes, 16 at a time; slowest: Claims 24s, Watch 16s, ClaimsReview 16s) / OK [ran] [tree 1859ac445858] (2026-10-21T19:45:21Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 19 tests in 21.2s (3 classes, 16 at a time; slowest: Claims 21s, ClaimsReview 13s, Stop 9s) / OK [ran] [tree 94961b2d2f4a] (2026-10-21T19:45:53Z)
- (audit intent) `self: one 'mine' predicate now serves both drop paths (bare and file-named); take still uses act for claim_overlaps and _claim as before; list computes no act` → task Two's drop of a.py frees a.py::g and keeps task One's a.py::f (test_claims) [tree 94961b2d2f4a] (2026-10-21T19:45:53Z)
- (audit edge) `self: one 'mine' predicate now serves both drop paths (bare and file-named); take still uses act for claim_overlaps and _claim as before; list computes no act` → with no active task, mine() falls back to the whole session as before (test_a_bare_drop_releases_every_lease_this_session_holds passes); a lease with no task is anyone's in the session to drop [tree 94961b2d2f4a] (2026-10-21T19:45:53Z)
- (audit self) `self: one 'mine' predicate now serves both drop paths (bare and file-named); take still uses act for claim_overlaps and _claim as before; list computes no act` → no findings [tree 94961b2d2f4a] (2026-10-21T19:45:53Z)
## Log
- 2026-10-21T18:57:45Z created
- 2026-10-21T19:44:14Z planned from capture
- 2026-10-21T19:44:15Z focused
- 2026-10-21T19:48:15Z done
- 2026-10-21T19:48:18Z committed 43bd0881 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1216 [FIX S, done, 2 steps] fm lease drop releases only the current task's leases, and a file's drop releases all its symbols
- T-1134 [FIX S, done, 1 steps] Fm lease drop with no FILE drops every lease this session holds (5 builders today ran it b — lesson: When a brief tells agents to run a com…
- T-1205 [FIX S, done, 2 steps] fm lease drop says how many leases it released, not only what's left
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- similar finished tasks took 1–2 steps
- start here (files T-1216 touched): plugin/tests/test_claims.py, plugin/lib/fmbus.py, CHANGELOG.md
## Regression test
test_claims.test_a_file_named_drop_keeps_another_tasks_leases_in_the_same_session: red before (step 1 evidence exit 1), green after
## Why not caught
T-1216 tested only the bare drop; the file-named path kept the session-wide filter
## Lessons
- When a fix scopes one path of a command (T-1216's bare drop), apply the same predicate to its sibling paths in the same change
## Plan gaps
- failed first: step 1 failing test in test_claims beside T-1216's bare-drop test, then one shared 'mine' predicate in fmb…
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
