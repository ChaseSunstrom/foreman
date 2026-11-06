---
id: T-1988
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T13:33:24Z
updated: 2026-10-29T13:59:19Z
base: b4df3e9f5dd04542dc2e6b01a179cd2cd28239fd
base_tree: 2c2f2e0c5dc2c997f2785f04c3c8d19b3b2936fa
plan0_at: 2026-10-29T13:33:25Z
plan0_scope: []
verified: ok
---
# Ship T-1987 to main
## Raw request
> Ship T-1987 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] b4df3e9f is on origin main and CI is green — verify with `fm ship --check b4df3e9f`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check b4df3e9f` → exit 0 · origin main has the changes of b4df3e9f [ran] [tree 2c2f2e0c5dc2] (2026-10-29T13:59:18Z)
- (step 1) `fm ship --check b4df3e9f` → exit 0 · origin main has the changes of b4df3e9f [ran] [tree 2c2f2e0c5dc2] (2026-10-29T13:59:18Z)
- (audit self) `self: ship output shows tests OK, pushed, CI green` → no findings [tree 2c2f2e0c5dc2] (2026-10-29T13:59:18Z)
## Log
- 2026-10-29T13:33:24Z created
- 2026-10-29T13:33:24Z focused
- 2026-10-29T13:33:29Z guard authorization added: publish
- 2026-10-29T13:36:22Z publish grant used by fm ship
- 2026-10-29T13:59:19Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
