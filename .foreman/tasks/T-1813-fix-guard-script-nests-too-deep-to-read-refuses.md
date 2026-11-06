---
id: T-1813
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-28T07:30:23Z
updated: 2026-10-28T08:19:02Z
---
# FIX: guard 'script nests too deep to read' refuses a harmless 3-deep sh chain (fmguard.py:
## Raw request
> FIX: guard 'script nests too deep to read' refuses a harmless 3-deep sh chain (fmguard.py:3856 _IN_SCRIPT >= 3); refuse only when the deep script holds a finding or raise to 5; add a FORMS case
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
- 2026-10-28T07:30:23Z created
- 2026-10-28T08:19:02Z dropped: measured 2026-10-28 over every transcript: 0 'script nests too deep to read' refusals ever. T-1298 chose the refusal on purpose: a chain three scripts deep hides its last one, and its hint already says to run the innermost script directly; raising the limit without a single real false refusal only widens what the guard can't see
## Follow-ups captured
