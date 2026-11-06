---
id: T-0037
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-09-26T18:58:46Z
updated: 2026-09-26T19:06:29Z
done_in: T-0018
---
# Self-lockout #2: a bug in fmcore (record decorator on Python 3.14) made the hook unable to
## Raw request
> Self-lockout #2: a bug in fmcore (record decorator on Python 3.14) made the hook unable to load the active task, so its core grant vanished and every core edit (including the fix) was refused; fm itself was broken too, so the user had to run git checkout. Extend the committed fallback from fmguard to the library the guard context needs (fmcore via git HEAD), and test with a broken fmcore
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
- 2026-09-26T18:58:46Z created
- 2026-09-26T19:06:29Z done in T-0018
## Follow-ups captured
