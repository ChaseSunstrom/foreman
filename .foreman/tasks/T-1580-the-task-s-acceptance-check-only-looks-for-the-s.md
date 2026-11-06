---
id: T-1580
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T18:27:36Z
updated: 2026-10-22T18:42:42Z
---
# - The task's acceptance check only looks for the substring `1.`, so any file containing "0
## Raw request
> - The task's acceptance check only looks for the substring `1.`, so any file containing "0.1" would pass. A stricter check would be a regex for `^1\. \*\*`, plus a check that SKILL.md links each file
> (noticed by an agent; research T-1503-review)
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
- 2026-10-22T18:27:36Z created
- 2026-10-22T18:42:42Z dropped: folded into T-1505 (numbered-procedure check)
## Follow-ups captured
