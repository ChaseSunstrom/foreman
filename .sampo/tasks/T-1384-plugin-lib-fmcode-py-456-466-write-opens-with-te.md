---
id: T-1384
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T17:27:18Z
updated: 2026-10-21T17:28:55Z
---
# Plugin/lib/fmcode.py:456-466` `write()` opens with text mode and no line-ending handling,
## Raw request
> plugin/lib/fmcode.py:456-466` `write()` opens with text mode and no line-ending handling, unlike `fmedit.py:94,109` (B24 covers it)
> (noticed by an agent; research brainstorm-fm-anthropic-half-b)
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
- 2026-10-21T17:27:18Z created
- 2026-10-21T17:28:55Z dropped: duplicate of T-1408 (write keeps line endings, refuses non-UTF-8)
## Follow-ups captured
