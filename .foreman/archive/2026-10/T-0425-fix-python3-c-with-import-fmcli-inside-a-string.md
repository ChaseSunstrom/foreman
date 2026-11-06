---
id: T-0425
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T14:00:49Z
updated: 2026-10-09T14:13:17Z
---
# FIX: python3 -c with 'import fmcli' inside a string (diff-parser test data) is refused as
## Raw request
> FIX: python3 -c with 'import fmcli' inside a string (diff-parser test data) is refused as core via _drives_fm (fmguard.py:1116-1120); only a real import statement should count (related to T-0275)
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
- 2026-10-09T14:00:49Z created
- 2026-10-09T14:13:17Z dropped: working as intended: python -c importing Foreman's modules next to writer-looking text is core by design (_drives_fm relaxes only parsed heredocs it can prove); the T-0413 builder's ad hoc check of fmcli belongs in a unit test, which it then wrote. Loosening -c parsing trades core protection for a rare dev-only convenience
## Follow-ups captured
