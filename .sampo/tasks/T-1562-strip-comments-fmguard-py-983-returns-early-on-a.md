---
id: T-1562
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T17:49:19Z
updated: 2026-10-22T17:49:32Z
---
# _strip_comments` (fmguard.py:983) returns early on any `$'`. After this change that branch
## Raw request
> _strip_comments` (fmguard.py:983) returns early on any `$'`. After this change that branch is reachable only through the heredoc skip, so the fail-closed comment only covers the case that finding 1 s…
> (noticed by an agent; research T-1480-review)
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
- 2026-10-22T17:49:19Z created
- 2026-10-22T17:49:32Z dropped: kept on purpose in T-1480: after decoding, a remaining $' is inside double quotes, a heredoc body or unclosed, where the early return only reads comments as code (adds refusals); _heredoc_starts still needs it on raw text
## Follow-ups captured
