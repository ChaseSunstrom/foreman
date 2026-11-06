---
id: T-1160
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:44:16Z
---
# Retry a red lane-merge criterion once (with a scaled timeout) when the host was strained o
## Raw request
> FEATURE: Retry a red lane-merge criterion once (with a scaled timeout) when the host was strained or the failing test is in the flake ledger, and log it as retried.
> DONE-WHEN: a test with FOREMAN_HOST load set high and a criterion that fails once then passes merges the lane and logs a retry; the same criterion failing twice still refuses
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
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:44:16Z dropped: premise false: fm lane merge runs no criteria (fmlanes.merge only merges); fm check reruns a failed gate once (fmcli ~3431, T-0047) and the close's linked tests rerun a flake once (T-1117); fm task evidence records a single run on purpose
## Follow-ups captured
