---
id: T-2690
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:00:50Z
updated: 2026-11-02T23:08:40Z
base: 7e93963bdfad7a7c2ac6f4b38afb466f53a1014a
base_tree: 1dfc39b2016cd605807eb1efd8afcbb0799572b0
plan0_at: 2026-11-02T23:00:51Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# Ship 3 commits to main (T-2686, T-2687, T-2688)
## Raw request
> Ship 3 commits to main (T-2686, T-2687, T-2688)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main has them — verify with `fm ship --check 1ed400df cdcd3339 7e93963b`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm ship --check 1ed400df cdcd3339 7e93963b` → exit 0 · origin main has the changes of 1ed400df, cdcd3339, 7e93963b [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:08:37Z)
- (ac 1) `fm ship --check 1ed400df cdcd3339 7e93963b` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:08:37Z [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:08:37Z)
- (audit operator) `fm ship ran the full suite and pushed T-2687, T-2686 and T-2688 to origin main at 7326b22a; T-2691 landed during the run and waits for the next ship` → focusing another task mid-ship would have made the push refuse (fm ship re-reads the active task's grant at push time); refocused before the push, and captured the fix [tree 1dfc39b2016c] (2026-11-02T23:08:37Z)
- (audit self) `fm ship ran the full suite and pushed T-2687, T-2686 and T-2688 to origin main at 7326b22a; T-2691 landed during the run and waits for the next ship` → no findings [tree 1dfc39b2016c] (2026-11-02T23:08:37Z)
## Log
- 2026-11-02T23:00:50Z created
- 2026-11-02T23:00:51Z focused
- 2026-11-02T23:00:54Z guard authorization added: publish
- 2026-11-02T23:03:33Z paused: focus moved to T-2691
- 2026-11-02T23:08:17Z publish grant used by fm ship
- 2026-11-02T23:08:19Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T23:08:19Z focused
- 2026-11-02T23:08:35Z criterion 1 verify: `fm ship --check` → `fm ship --check 1ed400df cdcd3339 7e93963b`
- 2026-11-02T23:08:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2685 [CLEAN S, done, 1 steps] Ship 9 commits to main (Mission 7 briefs, T-2676)
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- similar finished tasks took 1–2 steps
