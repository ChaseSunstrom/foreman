---
id: T-2143
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:40:19Z
updated: 2026-10-31T04:44:43Z
inferred_deps: [T-2139]
inferred_why: T-2139: card must match what SessionStart carries
---
# Goal card byte-stable across sessions so the SessionStart prefix stays prompt-cached…
## Raw request
> Goal card byte-stable across sessions so the SessionStart prefix stays prompt-cached (Mission 4 inbox)
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
- 2026-10-30T10:40:19Z created
- 2026-10-31T04:44:43Z dropped: no cache win: the SessionStart context also carries Active/Next/Queue/Inbox/Watch lines that change every session, and the goal line sits after them, so a byte-stable goal line keeps no extra prefix cached; the cached prefix is the system prompt, tools and CLAUDE.md, which already don't carry it
## Follow-ups captured
