---
id: T-1418
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T18:57:46Z
updated: 2026-10-21T21:25:32Z
done_in: T-1432
---
# Fm code: an inline --worker 'CMD --yolo {prompt}' skips T-1395's dangerous-flag lint; gemi
## Raw request
> fm code: an inline --worker 'CMD --yolo {prompt}' skips T-1395's dangerous-flag lint; gemini's -y isn't in DANGEROUS; fmcodetui._choices doesn't catch CodeError from all_runners, so a bad code.toml can break the TUI picker
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
- 2026-10-21T18:57:46Z created
- 2026-10-21T20:44:12Z batched into T-1432
- 2026-10-21T21:25:32Z done in T-1432 (batch)
## Follow-ups captured
