---
id: T-1304
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T23:44:42Z
updated: 2026-10-21T03:44:16Z
group: TUI recording and export
---
# Fm code tui --record PATH run through fm printed the path but no file appeared there (the
## Raw request
> fm code tui --record PATH run through fm printed the path but no file appeared there (the same record() called directly writes it): find where fm's run puts it
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
- 2026-10-20T23:44:42Z created
- 2026-10-21T03:44:16Z dropped: doesn't reproduce now: fm code tui --record out.mp4 --events ev.jsonl run through fm from a scratch folder wrote out.mp4 there (96 KB). T-1320 passes ffmpeg an absolute path, and the earlier miss came from this session's sandbox not showing files ffmpeg wrote via fm across calls
## Follow-ups captured
