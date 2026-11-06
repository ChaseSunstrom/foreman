---
id: T-1997
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T14:46:36Z
updated: 2026-10-29T15:12:27Z
base: b49ccf6d2b3e575ed7781fdb9bad4e1faff59d5d
base_tree: d9d71bc8f2431d88165d838224a052120a2e8c18
plan0_at: 2026-10-29T14:46:37Z
plan0_scope: []
verified: ok
---
# Ship T-1996 to main
## Raw request
> Ship T-1996 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] b49ccf6d is on origin main and CI is green — verify with `fm ship --check b49ccf6d`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check b49ccf6d` → exit 0 · origin main has the changes of b49ccf6d [ran] [tree d9d71bc8f243] (2026-10-29T15:12:25Z)
- (step 1) `fm ship --check 213bcf0d` → exit 0 · origin main has the changes of 213bcf0d [ran] [tree d9d71bc8f243] (2026-10-29T15:12:25Z)
- (audit self) `self: fm ship pushed b49ccf6d to origin main as 213bcf0, its test run passed and CI went green` → no findings [tree d9d71bc8f243] (2026-10-29T15:12:25Z)
## Log
- 2026-10-29T14:46:36Z created
- 2026-10-29T14:46:36Z focused
- 2026-10-29T14:46:39Z guard authorization added: publish
- 2026-10-29T14:49:36Z publish grant used by fm ship
- 2026-10-29T15:12:27Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
