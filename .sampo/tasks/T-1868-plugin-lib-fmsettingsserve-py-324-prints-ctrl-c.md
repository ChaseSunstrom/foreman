---
id: T-1868
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T22:40:28Z
updated: 2026-10-28T22:42:53Z
---
# Plugin/lib/fmsettingsserve.py:324` prints "Ctrl-C stops it, so do 30 idle minutes", which
## Raw request
> plugin/lib/fmsettingsserve.py:324` prints "Ctrl-C stops it, so do 30 idle minutes", which is garbled wording from the original and now shared by both pages
> (noticed by an agent; research T-1858-review)
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
- 2026-10-28T22:40:28Z created
- 2026-10-28T22:42:53Z dropped: fixed in T-1858: the hint now reads 'Ctrl-C or 30 idle minutes stop it'
## Follow-ups captured
