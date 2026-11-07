---
id: T-3610
type: FIX
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-07T04:30:00Z
updated: 2026-11-07T04:30:00Z
---
# The guard refuses scratch .py drafts that import Sampo's modules (9x 'shell text it…
## Raw request
> FIX: the guard refuses scratch .py drafts that import Sampo's modules (9x 'shell text it can't read as python names Sampo's modules'): _DRAFT_EXT (fmguard.py ~2041) lacks .py. Add .py with adversarial tests: running the draft in the same command, -m, PYTHONPATH, sitecustomize/usercustomize/conftest names and a later python of a script in the draft's folder all stay refused (self-improvement pass; loosens the guard: review it security-first)
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
- 2026-11-07T04:30:00Z created
## Follow-ups captured
