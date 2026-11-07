---
id: T-3589
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:19:22Z
updated: 2026-11-07T03:19:22Z
---
# PERFORMANCE pipeline: merge batches run their phases one after another (pre-check…
## Raw request
> PERFORMANCE pipeline: merge batches run their phases one after another (pre-check probes, gate, ~12 serial closes), so the machine idles at ~50% between phases while 80+ reviewed lanes wait; while one batch closes, pre-check the next batch's lanes on scratch trees (merge-tree + their affected tests against the current build tip) so its train starts with its probes done, reusing a probe whose code tree still matches (T-3531's green-evidence skip)
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
- 2026-11-07T03:19:22Z created
## Follow-ups captured
