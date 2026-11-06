---
id: T-1292
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:07:24Z
updated: 2026-10-20T21:12:50Z
done_in: T-1284
---
# Test_reaper._Stubbed.tearDown finds leftover sleepers via /proc/PID/cmdline, so on macOS a
## Raw request
> test_reaper._Stubbed.tearDown finds leftover sleepers via /proc/PID/cmdline, so on macOS a failed test leaves them running: use the ps path there too
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
- 2026-10-20T21:07:24Z created
- 2026-10-20T21:12:50Z done in T-1284: test_reaper's tearDown now falls back to ps when /proc is absent (T-1284's review round)
## Follow-ups captured
