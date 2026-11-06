---
id: T-2685
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T22:35:49Z
updated: 2026-11-02T22:44:13Z
base: 33b4ee6f798786eae6c7669eb2cef21022fddec6
base_tree: 9cfdfd32a98872475f4c567f91c6b6505f7fefe4
plan0_at: 2026-11-02T22:35:50Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# Ship 9 commits to main (Mission 7 briefs, T-2676)
## Raw request
> Ship 9 commits to main (Mission 7 briefs, T-2676)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main has them — verify with `fm ship --check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 33b4ee6f [ran] [tree 9cfdfd32a988] [world 2f1906870a] (2026-11-02T22:44:06Z)
- (ac 1) `fm ship --check` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:44:06Z [ran] [tree 9cfdfd32a988] [world 2f1906870a] (2026-11-02T22:44:10Z)
- (audit operator) `fm ship ran the full suite on Python 3.12 (5807 tests OK) and pushed 9 commits to origin main at cd03fd0f; fm ship --check now says main has HEAD's changes` → the oldest shipped commit landed 16:15 and the push followed at about 16:47, within the hour, under the standing push grant [tree 9cfdfd32a988] (2026-11-02T22:44:10Z)
- (audit self) `fm ship ran the full suite on Python 3.12 (5807 tests OK) and pushed 9 commits to origin main at cd03fd0f; fm ship --check now says main has HEAD's changes` → no findings [tree 9cfdfd32a988] (2026-11-02T22:44:10Z)
## Log
- 2026-11-02T22:35:49Z created
- 2026-11-02T22:35:49Z focused
- 2026-11-02T22:35:53Z guard authorization added: publish
- 2026-11-02T22:43:56Z publish grant used by fm ship
- 2026-11-02T22:44:13Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- T-2682 [FEATURE S, done, 3 steps] with commits main lacks, the queue closed and the user's standing push grant on record, fm next makes fm ship the required action; with…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
