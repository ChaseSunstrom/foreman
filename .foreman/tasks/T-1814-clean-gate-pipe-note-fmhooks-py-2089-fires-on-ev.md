---
id: T-1814
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
# CLEAN: _gate_pipe_note (fmhooks.py:2089) fires on every piped fm check (13x seen); emit on
## Raw request
> CLEAN: _gate_pipe_note (fmhooks.py:2089) fires on every piped fm check (13x seen); emit once per session
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
- 2026-10-28T08:15:59Z dropped: already once per context window: _said_once (T-1258) drops a one-line note given since the session's start or last compaction; this session's 4 firings were one per compaction
## Follow-ups captured
