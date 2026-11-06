---
id: T-2162
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: [T-2263]
source: user
created: 2026-10-30T14:08:42Z
updated: 2026-10-31T06:15:55Z
---
# Long-horizon exam tier, the deciding end-of-run score: replay real repos (Foreman's own…
## Raw request
> Long-horizon exam tier, the deciding end-of-run score: replay real repos (Foreman's own history included) rolled back to a past commit, goal = the multi-task change that followed, hidden checks from what shipped; planted faults mid-run (forced compaction, killed session, usage-limit pause, misleading test); foreman vs plain on the same goals; per finished goal: true-done rate, false-done claims, regressions and reverts, human interventions, hours to the first, guard-worthy actions attempted, cost (steer 2026-10-30 rule 3)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-30T14:08:42Z created
- 2026-10-31T05:48:22Z split into T-2258 (gen/run/grade, zero-token arms; done), T-2262 (foreman/plain session arms with planted faults; done), T-2263 (per-goal metrics and the deciding scorecard row; building): closes when T-2263 lands; the real run is the end-of-run exam on the production model (steer 1)
- 2026-10-31T05:48:22Z set depends_on=['T-2263']
- 2026-10-31T06:15:55Z dropped: delivered in three slices, all done: T-2258 (gen/run/grade, zero-token arms), T-2262 (foreman/plain session arms with planted faults), T-2263 (per-goal metrics and the deciding scorecard row on status, export and site); the real run is the end-of-run exam on the production model
## Follow-ups captured
