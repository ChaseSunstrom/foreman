---
id: T-2046
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T20:21:26Z
updated: 2026-10-29T21:44:59Z
---
# plugin/lib/fmcore.py:925` — `write_atomic` fails on a bare filename (`dirname == ""`);…
## Raw request
> plugin/lib/fmcore.py:925` — `write_atomic` fails on a bare filename (`dirname == ""`); fixing it there would cover every caller
> (noticed by an agent; research T-1784-review)
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
- 2026-10-29T20:21:26Z created
- 2026-10-29T21:44:59Z dropped: already fixed in ee98a137: fmcore.write_atomic falls back to '.'; covered in test_scene_verify
## Follow-ups captured
