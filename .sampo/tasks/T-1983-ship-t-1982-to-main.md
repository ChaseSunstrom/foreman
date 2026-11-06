---
id: T-1983
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T12:57:13Z
updated: 2026-10-29T13:22:13Z
base: 2abd17ceb4298f7d846a48a479563f817aaa8e66
base_tree: 6ad45df6e5d8c1f4ce272ddbb969a9b1c7fb8363
plan0_at: 2026-10-29T12:57:17Z
plan0_scope: []
verified: ok
---
# Ship T-1982 to main
## Raw request
> Ship T-1982 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 2abd17ce is on origin main and CI is green — verify with `fm ship --check 2abd17ce`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check 2abd17ce` → exit 0 · origin main has the changes of 2abd17ce [ran] [tree 6ad45df6e5d8] (2026-10-29T13:22:12Z)
- (step 1) `fm ship --check 2abd17ce` → exit 0 · origin main has the changes of 2abd17ce [ran] [tree 6ad45df6e5d8] (2026-10-29T13:22:12Z)
- (audit self) `self: ship output shows tests OK, pushed, CI green` → no findings [tree 6ad45df6e5d8] (2026-10-29T13:22:12Z)
## Log
- 2026-10-29T12:57:13Z created
- 2026-10-29T12:57:16Z guard authorization added: publish
- 2026-10-29T12:57:17Z focused
- 2026-10-29T13:00:11Z publish grant used by fm ship
- 2026-10-29T13:22:13Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
