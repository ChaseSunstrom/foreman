---
id: T-0762
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-14T15:36:31Z
updated: 2026-10-14T15:42:40Z
---
# FIX: 'claude plugin update foreman-ui@foreman' refused while a foreman-ui pin is held (fmg
## Raw request
> FIX: 'claude plugin update foreman-ui@foreman' refused while a foreman-ui pin is held (fmguard.py:2733 marks targets only for install/enable; fmhooks.py:694 refuses untargeted changes) — allow updating the pinned plugin; unblocks T-0418
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
- 2026-10-14T15:36:31Z created
- 2026-10-14T15:42:40Z dropped: working as intended: a plugin pin approves one plugin's content at a hash (T-0036); an update fetches content the user never saw, so it needs its own plain fm ask, which the block message says
## Follow-ups captured
