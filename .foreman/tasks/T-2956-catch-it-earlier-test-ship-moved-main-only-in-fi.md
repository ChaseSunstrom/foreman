---
id: T-2956
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-04T11:48:44Z
updated: 2026-11-04T11:48:44Z
group: affected-test set gaps
---
# Catch it earlier: test_ship moved main only in files the branch never touched (T-2212);…
## Raw request
> T-2955 (fm ship can't ship a branch that touched a file fm genesis live keeps publishing to main: the tower's commits make the replay fall back to git cherry (382 commits) and the cherry-pick conflicts on site/genesis/genesis.json; files the live tower owns should take main's version and not count as overlap) wasn't caught before it shipped: test_ship moved main only in files the branch never touched (T-2212); no test had the tower move a file the branch also changed
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
- 2026-11-04T11:48:44Z created
## Follow-ups captured
