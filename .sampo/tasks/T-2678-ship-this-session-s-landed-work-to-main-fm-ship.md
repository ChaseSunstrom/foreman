---
id: T-2678
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T21:52:03Z
updated: 2026-11-02T22:00:16Z
base: 6a4e4a506c481f9b3d962c77382a90a5e0344f3d
base_tree: 37c80f3d08ed6a0467af181a91ae9b09c862dc51
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T21:52:04Z
plan0_scope: []
---
# Ship this session's landed work to main (fm ship)
## Raw request
> Ship this session's landed work to main (fm ship)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm ship pushed the local commits to origin main with its gates green — verify with `git fetch -q origin && test -z "$(git cherry origin/main HEAD | grep '^+')"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship
## Resume here
<!-- auto -->
- 2026-11-02T21:52:27Z step 1/1: fm ship
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && git log -1 --format=%H origin/main` → exit 0 · 0625fd09f2f787cab87d67c11b50c137b28740ae [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:59:53Z)
- (ac 1) `git fetch -q origin && test -z "$(git cherry origin/main HEAD | grep '^+')"` → ✗ exit 1 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:59:54Z)
## Log
- 2026-11-02T21:52:03Z created
- 2026-11-02T21:52:04Z focused
- 2026-11-02T21:52:04Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T21:52:09Z guard authorization added: publish
- 2026-11-02T21:59:40Z publish grant used by fm ship
- 2026-11-02T22:00:16Z dropped: its check was wrong: fm ship landed everything at 0625fd09 (5793 tests green), but git cherry flags two builder commits (T-2643, T-2672) whose content reached main through their merges with different patches; redone with a tree-equality check
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- T-2598 [FIX M, done, 4 steps] fm release's push lands on a main that fm ship fed by cherry-pick: a conflicting merge falls back to a merge commit of the release tree plu…
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar past tasks were M: consider --tier M
