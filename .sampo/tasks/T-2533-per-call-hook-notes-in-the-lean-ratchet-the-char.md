---
id: T-2533
type: FEATURE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T04:14:14Z
updated: 2026-11-02T04:21:39Z
revisit: 2026-12-01
---
# Per-call hook notes in the lean ratchet: the chars PreToolUse and PostToolUse notes…
## Raw request
> FEATURE: per-call hook notes in the lean ratchet: the chars PreToolUse and PostToolUse notes injected per session (the median of the newest sessions, counted as fm cost counts hook notes) are recorded in the ship footprint and judged by fmdoctor.grown
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
- 2026-11-02T04:14:14Z created
- 2026-11-02T04:19:57Z dropped: measured: hook notes are 0.8% of what entered the context (fm cost) and vary with session length and kind, so a 2% ratchet would trip on noise; the friction digest already lists notes by kind with counts and chars for the self-improvement pass
- 2026-11-02T04:21:38Z set status=planned
- 2026-11-02T04:21:39Z deferred: revive when hook notes pass 3% of what enters the context (fm cost), or a per-tool-call rate stays within 10% across a week of sessions (revisit 2026-12-01)
## Follow-ups captured
