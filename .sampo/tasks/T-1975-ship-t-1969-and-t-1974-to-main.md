---
id: T-1975
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T11:38:32Z
updated: 2026-10-29T12:09:25Z
base: 24df129229f1db89aa08f156627689bc6b9f149f
base_tree: 3d1eb91bb1e9877bb416253c92115a94b99f10e4
plan0_at: 2026-10-29T11:43:30Z
plan0_scope: []
verified: strong
---
# ship T-1969 and T-1974 to main
## Raw request
> ship T-1969 and T-1974 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main has the commits and CI is green — verify with `fm ship --check HEAD`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
<!-- auto -->
- 2026-10-29T11:44:15Z step 1/1: fm ship --watch
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `fm ship --check 52af012a 24df1292` → exit 0 · origin main has the changes of 52af012a, 24df1292 [ran] [tree 3d1eb91bb1e9] (2026-10-29T12:09:12Z)
- (ac 1) `fm ship --check HEAD` → exit 0 · origin main has the changes of 24df1292 [ran] [tree 3d1eb91bb1e9] (2026-10-29T12:09:14Z)
- (audit edge) `ship output: 4190 tests OK in scratch tree, CI green on 357d22d; fm ship --check confirms main has both commits` → main moved check passed; grant spent [tree 3d1eb91bb1e9] (2026-10-29T12:09:14Z)
- (audit self) `ship output: 4190 tests OK in scratch tree, CI green on 357d22d; fm ship --check confirms main has both commits` → no findings [tree 3d1eb91bb1e9] (2026-10-29T12:09:14Z)
- (audit edge) `ship output: 4190 tests OK in scratch tree, CI green on 357d22d; fm ship --check confirms main has both commits` → main moved check passed; grant spent [tree 3d1eb91bb1e9] (2026-10-29T12:09:24Z)
- (audit self) `ship output: 4190 tests OK in scratch tree, CI green on 357d22d; fm ship --check confirms main has both commits` → no findings [tree 3d1eb91bb1e9] (2026-10-29T12:09:24Z)
## Log
- 2026-10-29T11:38:32Z created
- 2026-10-29T11:38:35Z guard authorization added: publish
- 2026-10-29T11:43:29Z focused
- 2026-10-29T11:46:30Z publish grant used by fm ship
- 2026-10-29T12:09:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
## Behaviour lock
none: a ship edits no files; its scratch-tree suite (4190 OK) and CI are the lock
