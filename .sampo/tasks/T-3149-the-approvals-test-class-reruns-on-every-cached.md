---
id: T-3149
type: PERFORMANCE
tier: S
status: captured
priority: normal
scope: []
depends_on: [T-3296]
source: discovered
created: 2026-11-05T05:37:01Z
updated: 2026-11-06T03:56:14Z
inferred_deps: [T-3140]
inferred_why: T-3140: named in its request
group: fast merges and merge trains
---
# The Approvals test class reruns on every cached pass (~15 s): its children go untraced;…
## Raw request
> The Approvals test class reruns on every cached pass (~15 s): its children go untraced; trace them so it can be reused (T-3140 follow-up)
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
- 2026-11-05T05:37:01Z created
- 2026-11-05T05:56:34Z blocked: needs T-3140's test cache merged first (its builder is fixing review findings)
- 2026-11-06T03:56:13Z set depends_on=['T-3296']
- 2026-11-06T03:56:13Z retargeted: T-3140 was dropped (no warm gain); the pass cache is now T-3296
- 2026-11-06T03:56:14Z unblocked
## Follow-ups captured
