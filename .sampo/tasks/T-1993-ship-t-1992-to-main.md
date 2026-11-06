---
id: T-1993
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T14:11:21Z
updated: 2026-10-29T14:37:50Z
base: db2eddf2810c69c09e1d917c9c402ec185975220
base_tree: 423798ddabfcccbc134c18e78272f614a97b6ad5
plan0_at: 2026-10-29T14:11:22Z
plan0_scope: []
verified: ok
---
# Ship T-1992 to main
## Raw request
> Ship T-1992 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] db2eddf2 is on origin main and CI is green — verify with `fm ship --check db2eddf2`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check db2eddf2` → exit 0 · origin main has the changes of db2eddf2 [ran] [tree 423798ddabfc] (2026-10-29T14:37:48Z)
- (step 1) `fm ship --check 7cdc36d` → exit 0 · origin main has the changes of 7cdc36d3 [ran] [tree 423798ddabfc] (2026-10-29T14:37:48Z)
- (audit self) `fm ship pushed db2eddf2 as 7cdc36d to origin main; CI green; exit 0 read before closing` → no findings [tree 423798ddabfc] (2026-10-29T14:37:48Z)
## Log
- 2026-10-29T14:11:21Z created
- 2026-10-29T14:11:22Z focused
- 2026-10-29T14:11:25Z guard authorization added: publish
- 2026-10-29T14:14:20Z publish grant used by fm ship
- 2026-10-29T14:37:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
