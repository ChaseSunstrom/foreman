---
id: T-3150
type: PERFORMANCE
tier: S
status: captured
priority: normal
scope: []
depends_on: [T-3296]
source: discovered
created: 2026-11-05T05:37:02Z
updated: 2026-11-06T03:56:17Z
inferred_deps: [T-3140]
inferred_why: T-3140: named in its request
group: fast merges and merge trains
---
# Sampo check --no-cache: wire run.py's --no-cache drift comparison into sampo check and…
## Raw request
> sampo check --no-cache: wire run.py's --no-cache drift comparison into sampo check and the nightly run (T-3140 follow-up)
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
- 2026-11-05T05:37:02Z created
- 2026-11-05T05:56:35Z blocked: needs T-3140's test cache merged first (its builder is fixing review findings)
- 2026-11-06T03:56:15Z set depends_on=['T-3296']
- 2026-11-06T03:56:16Z retargeted: T-3140 was dropped (no warm gain); the pass cache is now T-3296
- 2026-11-06T03:56:17Z unblocked
## Follow-ups captured
