---
id: T-3570
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T02:05:52Z
updated: 2026-11-07T02:05:52Z
---
# A logged 'scope: <why>' reason can never cover a deleted tracked file: _task_files…
## Raw request
> A logged 'scope: <why>' reason can never cover a deleted tracked file: _task_files (cli.py ~1995) gives a deleted file touches = c.now() at check time, so the reason is always 'before the edit' unless the log and the close fall in the same second (which also made T-3550's test flaky under load). Use the time the deletion was first seen (e.g. the newest of the file's last recorded touch, the task's last ledger event before the check) or accept a reason logged after the file was last present
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
- 2026-11-07T02:05:52Z created
## Follow-ups captured
