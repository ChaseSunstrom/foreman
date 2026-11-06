---
id: T-1964
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:34:02Z
updated: 2026-10-29T11:01:44Z
done_in: T-1967
---
# A full fm check first waits (at most 5 minutes, saying so) for a running ambient test run
## Raw request
> FEATURE: a full fm check first waits (at most 5 minutes, saying so) for a running ambient test run on the tree, so two test runs never share the machine and a session doesn't prefix every background gate run with a pgrep wait loop
> DONE-WHEN: fm check with a live ambient run.pid prints that it waits for the ambient run and starts after it ends
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
- 2026-10-29T10:34:02Z created
- 2026-10-29T10:34:07Z set tier=S
- 2026-10-29T10:34:08Z batched into T-1967
- 2026-10-29T11:01:44Z done in T-1967 (batch)
## Follow-ups captured
