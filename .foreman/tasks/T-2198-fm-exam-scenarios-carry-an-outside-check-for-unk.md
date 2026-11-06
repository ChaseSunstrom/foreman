---
id: T-2198
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T18:02:42Z
updated: 2026-10-30T18:02:55Z
---
# fm exam scenarios carry an outside check for unkeyed findings: README edge-contract…
## Raw request
> fm exam scenarios carry an outside check for unkeyed findings: README edge-contract clauses each with a hidden edge test, so a finding that breaks a clause and whose hidden test fails on the clean render counts as an exam defect (T-2170 keeps self-proved findings as false alarms until then)
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
- 2026-10-30T18:02:42Z created
- 2026-10-30T18:02:55Z dropped: not needed: T-2120's README edge contract is already asserted clause by clause by the clean suite, which fm exam gen checks passes on the clean render, so an outside-confirmed exam defect would be a generator bug that gen's own check catches
## Follow-ups captured
