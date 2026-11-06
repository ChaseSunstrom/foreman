---
id: T-0356
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T04:57:15Z
updated: 2026-10-06T05:13:48Z
---
# Guard judges 'fm task new … --focus && <edit>' before the task exists and refuses the edit
## Raw request
> Guard judges 'fm task new … --focus && <edit>' before the task exists and refuses the edit as unbriefed; when an fm task new --focus heads an && chain, the rest of the chain may count as briefed (adversary lens: ; and || must not)
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
- 2026-10-06T04:57:15Z created
- 2026-10-06T05:13:48Z dropped: YAGNI: separate calls cost one tool call; loosening the brief gate adds guard surface (see fm decide)
## Follow-ups captured
