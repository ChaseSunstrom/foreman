---
id: T-0879
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T14:57:21Z
updated: 2026-10-15T14:57:28Z
done_in: T-0875
---
# Catch it earlier: the test only covered tracked, already-linked tests; the map is built fr
## Raw request
> T-0875 (fm check --affected runs a test file the task added or changed, even one the map hasn't linked) wasn't caught before it shipped: the test only covered tracked, already-linked tests; the map is built from git ls-files so untracked files never had links
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
- 2026-10-15T14:57:21Z created
- 2026-10-15T14:57:28Z done in T-0875: the task's own test now covers an untracked test file
## Follow-ups captured
