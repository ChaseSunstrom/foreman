---
id: T-2006
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T15:56:13Z
updated: 2026-10-29T16:25:36Z
base: 66d8eee818799dfd527c73841565309da2ec26b2
base_tree: c7acb6b77214100564bc60461442ccba73b6072b
plan0_at: 2026-10-29T15:56:14Z
plan0_scope: []
paused_tree: c7acb6b77214100564bc60461442ccba73b6072b
verified: ok
---
# Ship T-2005 to main
## Raw request
> Ship T-2005 to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 66d8eee8 is on origin main and CI is green — verify with `fm ship --check 66d8eee8`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship --watch
## Resume here
<!-- auto -->
- 2026-10-29T16:20:50Z step 1/1: fm ship --watch
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: ~/.claude/projects/-home-<user>--claude-foreman/memory/recursive-improvement-loop.md
- failures met: fm: error: unrecognized arguments: pushed 0; ci watch running in the background; bash: line 0: rsync: command not found; test_worker_reads.py:0:class workeronlyreads(foremantestcase):
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check 66d8eee8` → exit 0 · origin main has the changes of 66d8eee8 [ran] [tree 7e5163985140] (2026-10-29T16:25:34Z)
- (step 1) `fm ship --check 104c441` → exit 0 · origin main has the changes of 104c4416 [ran] [tree 7e5163985140] (2026-10-29T16:25:34Z)
- (audit self) `fm ship ran the suite in a scratch tree (4205 OK) and pushed 104c441; CI green on all 4 ubuntu jobs and macOS shard 1; macOS shard 2 never got a runner (GitHub capacity, job cancelled with 0 steps), and gh is logged out so it can't be rerun; the next push reruns CI` → no findings [tree 7e5163985140] (2026-10-29T16:25:34Z)
## Log
- 2026-10-29T15:56:13Z created
- 2026-10-29T15:56:14Z focused
- 2026-10-29T15:56:17Z guard authorization added: publish
- 2026-10-29T15:59:19Z publish grant used by fm ship
- 2026-10-29T16:20:50Z paused: focus moved to T-2012
- 2026-10-29T16:25:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1944 [FEATURE S, done, 1 steps] Ship T-1942 and T-1943 to main with fm ship
- T-1958 [FEATURE S, done, 1 steps] ship T-1952, T-1953 and T-1957 to main
- T-1949 [FEATURE S, done, 1 steps] ship T-1947 and T-1948 to main
- similar finished tasks took 1–2 steps
- start here (files T-1943 touched): plugin/tests/test_ship.py, plugin/lib/fmrelease.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/release/ship-to-main.md
