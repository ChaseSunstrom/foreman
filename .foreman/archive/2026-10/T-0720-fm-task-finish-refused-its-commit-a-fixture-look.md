---
id: T-0720
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T16:59:17Z
updated: 2026-10-09T17:10:12Z
done_in: T-0722
---
# Fm task finish refused its commit (a fixture looked like a secret) and left the task done
## Raw request
> fm task finish refused its commit (a fixture looked like a secret) and left the task done but its files uncommitted; nothing retries the commit for a done task, so it took a new task (T-0719) and a raw git commit: add fm task finish ID --commit-only (or let --commit rerun on a done task)
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
- 2026-10-09T16:59:17Z created
- 2026-10-09T17:06:10Z batched into T-0722
- 2026-10-09T17:10:12Z done in T-0722 (batch)
## Follow-ups captured
