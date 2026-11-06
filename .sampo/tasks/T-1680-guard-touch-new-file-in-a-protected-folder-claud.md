---
id: T-1680
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T21:40:23Z
updated: 2026-10-23T05:05:44Z
group: guard corpus and false blocks
done_in: T-1727
---
# Guard: touch NEW_FILE in a protected folder (Claude Code's plugin cache, e.g. ~/.claude/pl
## Raw request
> Guard: touch NEW_FILE in a protected folder (Claude Code's plugin cache, e.g. ~/.claude/plugins/cache/x/hooks/hooks.json) is allowed while echo/cp/truncate there are refused; touch creating a file there should be judged as a write (found by T-1605's probe)
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
- 2026-10-22T21:40:23Z created
- 2026-10-23T03:33:02Z batched into T-1727
- 2026-10-23T05:05:44Z done in T-1727 (batch)
## Follow-ups captured
