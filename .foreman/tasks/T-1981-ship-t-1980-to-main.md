---
id: T-1981
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T12:25:28Z
updated: 2026-10-29T12:50:56Z
base: a359778137806186a335be4a6d6072a1242ad3a6
base_tree: 05fc7fc5627e74909828647e9ec751d1086bd387
plan0_at: 2026-10-29T12:25:36Z
plan0_scope: []
verified: ok
---
# Ship T-1980 to main
## Raw request
> Ship T-1980 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a3597781 is on origin main and CI is green — verify with `fm ship --check a3597781`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm ship --check a3597781` → exit 0 · origin main has the changes of a3597781 [ran] [tree 05fc7fc5627e] (2026-10-29T12:50:52Z)
- (ac 1) `fm ship --check a3597781` → exit 0 · origin main has the changes of a3597781 [ran] [tree 05fc7fc5627e] (2026-10-29T12:50:54Z)
- (audit self) `self: ship output shows 4195 tests OK, pushed 6e6c9aa, CI green` → no findings [tree 05fc7fc5627e] (2026-10-29T12:50:54Z)
## Log
- 2026-10-29T12:25:28Z created
- 2026-10-29T12:25:35Z guard authorization added: publish
- 2026-10-29T12:25:35Z focused
- 2026-10-29T12:28:32Z publish grant used by fm ship
- 2026-10-29T12:50:56Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
