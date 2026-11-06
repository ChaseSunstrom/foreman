---
id: T-2723
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:21:46Z
updated: 2026-11-02T23:33:33Z
base: 4992e2d2a78993ffc29fafeaac12af32e1b618fd
base_tree: 9e8cae51c4ca774fb6b6fb58683c3c574aeb4910
plan0_at: 2026-11-02T23:21:47Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# Ship 5 commit(s) to main
## Raw request
> Ship 5 commit(s) to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main has them — verify with `fm ship --check 2c3010df 478e8d3b 7157321a 46a868c5 4992e2d2`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm ship --check 2c3010df 478e8d3b 7157321a 46a868c5 4992e2d2` → exit 0 · origin main has the changes of 2c3010df, 478e8d3b, 7157321a, 46a868c5, 4992e2d2 [ran] [tree 9e8cae51c4ca] [world 2f1906870a] (2026-11-02T23:33:30Z)
- (ac 1) `fm ship --check 2c3010df 478e8d3b 7157321a 46a868c5 4992e2d2` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:33:30Z [ran] [tree 9e8cae51c4ca] [world 2f1906870a] (2026-11-02T23:33:31Z)
- (audit operator) `fm ship ran the full suite, found main moved only in files these commits don't touch (fm genesis live's site), re-picked onto it and pushed 5 commits at d8809c2b; T-2724 landed during the run and waits for the next ship` → the first ship fm next itself led with (T-2722's rule under an open tower) [tree 9e8cae51c4ca] (2026-11-02T23:33:31Z)
- (audit self) `fm ship ran the full suite, found main moved only in files these commits don't touch (fm genesis live's site), re-picked onto it and pushed 5 commits at d8809c2b; T-2724 landed during the run and waits for the next ship` → no findings [tree 9e8cae51c4ca] (2026-11-02T23:33:31Z)
## Log
- 2026-11-02T23:21:46Z created
- 2026-11-02T23:21:46Z focused
- 2026-11-02T23:21:49Z guard authorization added: publish
- 2026-11-02T23:25:03Z paused: focus moved to T-2724
- 2026-11-02T23:27:49Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T23:27:49Z focused
- 2026-11-02T23:33:17Z publish grant used by fm ship
- 2026-11-02T23:33:29Z criterion 1 verify: `fm ship --check` → `fm ship --check 2c3010df 478e8d3b 7157321a 46a868c5 4992e2d2`
- 2026-11-02T23:33:33Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2685 [CLEAN S, done, 1 steps] Ship 9 commits to main (Mission 7 briefs, T-2676)
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- similar finished tasks took 1–2 steps
