---
id: T-2002
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T15:19:38Z
updated: 2026-10-29T15:47:59Z
base: 0f5e8a5c25c5e2ce8008e9b56d73f311e34a8f1f
base_tree: 2e0e05de4e2ff32fd2d3568c672354e019920310
plan0_at: 2026-10-29T15:19:39Z
plan0_scope: []
verified: ok
---
# Ship T-2001 to main
## Raw request
> Ship T-2001 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 0f5e8a5c is on origin main and CI is green — verify with `fm ship --check 0f5e8a5c`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check 0f5e8a5c` → exit 0 · origin main has the changes of 0f5e8a5c [ran] [tree 2e0e05de4e2f] (2026-10-29T15:47:57Z)
- (step 1) `fm ship --check a3abe686` → exit 0 · origin main has the changes of a3abe686 [ran] [tree 2e0e05de4e2f] (2026-10-29T15:47:57Z)
- (audit self) `self: fm ship pushed 0f5e8a5c to origin main as a3abe68 after its test run passed; --check confirms main has it` → no findings [tree 2e0e05de4e2f] (2026-10-29T15:47:57Z)
## Log
- 2026-10-29T15:19:38Z created
- 2026-10-29T15:19:38Z focused
- 2026-10-29T15:19:39Z guard authorization added: publish
- 2026-10-29T15:22:37Z publish grant used by fm ship
- 2026-10-29T15:47:59Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
