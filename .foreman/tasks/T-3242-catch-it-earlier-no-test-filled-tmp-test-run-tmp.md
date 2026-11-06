---
id: T-3242
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-05T20:51:28Z
updated: 2026-11-05T20:51:28Z
---
# Catch it earlier: no test filled /tmp; test_run.Tmp now raises ENOSPC from mkdtemp
## Raw request
> T-3236 (run.py: a class whose temp folder can't be made (/tmp full: OSError 28) crashes the…) wasn't caught before it shipped: no test filled /tmp; test_run.Tmp now raises ENOSPC from mkdtemp
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
- 2026-11-05T20:51:28Z created
## Follow-ups captured
