---
id: T-3564
type: FEATURE
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:55:32Z
updated: 2026-11-07T00:55:32Z
---
# SECURITY guard (prove first): _HEREDOC_START (fmguard.py ~759) has no boundary after the…
## Raw request
> SECURITY guard (prove first): _HEREDOC_START (fmguard.py ~759) has no boundary after the closing quote, so <<"E"OF is read as delimiter E while bash ends the body at EOF; commands after the real end may be hidden from the guard. sampo prove with a FORMS row (a write after the heredoc must still be refused), then fix the delimiter parse to bash's word rules (T-3538 security review)
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
- 2026-11-07T00:55:32Z created
## Follow-ups captured
