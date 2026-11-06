---
id: T-3178
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T08:08:42Z
updated: 2026-11-05T08:08:42Z
---
# A builder edited a file whose lease another lane held (T-3174 on cli.py::cmd_check, held…
## Raw request
> A builder edited a file whose lease another lane held (T-3174 on cli.py::cmd_check, held by T-3160) after lease take refused: the lane's commit should be refused or flagged at lane merge when it touches a symbol leased to another open lane
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
- 2026-11-05T08:08:42Z created
## Follow-ups captured
