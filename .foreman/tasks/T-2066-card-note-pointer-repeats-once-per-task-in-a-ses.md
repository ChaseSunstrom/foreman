---
id: T-2066
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T00:29:08Z
updated: 2026-10-30T00:30:16Z
---
# Card-note pointer repeats once per task in a session (33x in the last friction digest):…
## Raw request
> Card-note pointer repeats once per task in a session (33x in the last friction digest): after a session has seen a card's note, inject nothing for it (fmhooks._card_note ~1958); done when a second task in the same session injects no card note
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
- 2026-10-30T00:29:08Z created
- 2026-10-30T00:30:16Z dropped: the per-task pointer is T-1193's design (after compaction the earlier card note is gone from context); ~100 chars, at most 2 per edit
## Follow-ups captured
