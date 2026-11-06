---
id: T-2736
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:34:16Z
updated: 2026-11-03T00:39:59Z
base: fc60bb351a236ab7e8ad5a2692bce16d2ceda040
base_tree: 969e58d66189c640f97e2b1fe73c094ea954f00a
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-03T00:34:17Z
plan0_scope: []
verified: ok
unproven: [meaning]
---
# Ship 4 commit(s) to main
## Raw request
> Ship 4 commit(s) to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main has them — verify with `fm ship --check 8170d5d3 ee300ad7 fc60bb35 f01818ae`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm ship --check 8170d5d3 ee300ad7 fc60bb35 f01818ae` → exit 0 · origin main has the changes of 8170d5d3, ee300ad7, fc60bb35, f01818ae [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:39:57Z)
- (ac 1) `fm ship --check 8170d5d3 ee300ad7 fc60bb35 f01818ae` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:39:57Z [ran] [tree 969e58d66189] [world 2f1906870a] (2026-11-03T00:39:58Z)
- (audit self) `fm ship ran the full suite and pushed T-2731, T-2732, T-2733 and T-2735 at ff42c2dd; T-2738 landed during the run and waits for the next ship` → no findings [tree 969e58d66189] (2026-11-03T00:39:58Z)
## Log
- 2026-11-03T00:34:16Z created
- 2026-11-03T00:34:17Z focused
- 2026-11-03T00:34:17Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-03T00:34:21Z guard authorization added: publish
- 2026-11-03T00:35:13Z paused: focus moved to T-2737
- 2026-11-03T00:39:44Z publish grant used by fm ship
- 2026-11-03T00:39:55Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T00:39:55Z focused
- 2026-11-03T00:39:56Z criterion 1 verify: `fm ship --check` → `fm ship --check 8170d5d3 ee300ad7 fc60bb35 f01818ae`
- 2026-11-03T00:39:59Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2685 [CLEAN S, done, 1 steps] Ship 9 commits to main (Mission 7 briefs, T-2676)
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- similar finished tasks took 1–2 steps
