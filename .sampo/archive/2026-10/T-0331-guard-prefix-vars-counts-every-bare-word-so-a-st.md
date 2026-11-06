---
id: T-0331
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T02:25:26Z
updated: 2026-10-06T03:01:51Z
done_in: T-0338
---
# Guard: _prefix_vars counts every bare word, so a stray -S or path segment named like a var
## Raw request
> Guard: _prefix_vars counts every bare word, so a stray -S or path segment named like a var makes S=…; (cmd > $S/log &) unknown; count only assignment targets
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
- 2026-10-06T02:25:26Z created
- 2026-10-06T02:40:57Z batched into T-0338
- 2026-10-06T03:01:51Z done in T-0338 (batch)
## Follow-ups captured
