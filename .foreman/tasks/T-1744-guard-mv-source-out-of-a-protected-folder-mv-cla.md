---
id: T-1744
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-23T04:27:24Z
updated: 2026-10-23T05:09:28Z
done_in: T-1751
---
# Guard: mv SOURCE out of a protected folder (mv ~/.claude/plugins/cache/x/hooks/hooks.json
## Raw request
> Guard: mv SOURCE out of a protected folder (mv ~/.claude/plugins/cache/x/hooks/hooks.json /tmp/x, or out of core) isn't refused because _write_targets returns only mv's destination; a move removes the source and must be judged as a write there too
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
- 2026-10-23T04:27:24Z created
- 2026-10-23T05:06:05Z batched into T-1751
- 2026-10-23T05:09:28Z done in T-1751 (batch)
## Follow-ups captured
