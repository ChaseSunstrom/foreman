---
id: T-2762
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T04:13:59Z
updated: 2026-11-03T04:19:38Z
---
# The stack-card pointer note ('shown earlier this session; fm lib show NAME') repeats…
## Raw request
> FIX: the stack-card pointer note ('shown earlier this session; fm lib show NAME') repeats once per card per task, not per session (fmhooks.py:2195-2198, digest 4x): mark the card and continue without the note
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
- 2026-11-03T04:13:59Z created
- 2026-11-03T04:19:38Z dropped: by design (T-1193, plugin/lib/sampo/hooks.py:2172-2196): a later task in the same session gets one ~90-character pointer per card, so a compacted context can still find the card's notes; the digest's 4x is four tasks each getting it once, which is the design working, not a repeat
## Follow-ups captured
