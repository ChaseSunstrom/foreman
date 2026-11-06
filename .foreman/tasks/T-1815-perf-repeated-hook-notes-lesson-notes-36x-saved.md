---
id: T-1815
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-28T07:30:24Z
updated: 2026-10-28T08:15:59Z
---
# PERF: repeated hook notes (lesson notes 36x, 'saved what this command' 22x, changelog scop
## Raw request
> PERF: repeated hook notes (lesson notes 36x, 'saved what this command' 22x, changelog scope 21x) have no per-session dedupe; dedupe by text per session like _bus_note (fmhooks.py:2072)
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
- 2026-10-28T07:30:24Z created
- 2026-10-28T08:15:59Z dropped: measured this session (10 h, ~1500 turns): 62 hook notes, 25 exact repeats, 12 of them the session-start banner, each after a compaction cleared the context; _said_once (T-1258) already dedupes per window; ~1k tokens against 10.7M input-equivalent
## Follow-ups captured
