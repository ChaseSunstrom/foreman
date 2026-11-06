---
id: T-1581
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T18:27:53Z
updated: 2026-10-22T18:42:40Z
---
# Fmsettings.py `in_claude_code` is detectable-by-env only, so it deserves its own guard tas
## Raw request
> fmsettings.py `in_claude_code` is detectable-by-env only, so it deserves its own guard task (see the adversary finding)
> (noticed by an agent; research T-1574-review)
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
- 2026-10-22T18:27:53Z created
- 2026-10-22T18:42:40Z dropped: fixed in T-1572: in_claude_code fails closed unless stdin and stdout are a terminal
## Follow-ups captured
