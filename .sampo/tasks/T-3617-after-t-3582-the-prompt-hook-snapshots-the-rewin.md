---
id: T-3617
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T04:53:30Z
updated: 2026-11-07T04:53:30Z
---
# After T-3582 the prompt hook snapshots the rewind tree before the lock while…
## Raw request
> FIX: after T-3582 the prompt hook snapshots the rewind tree before the lock while reconcile_rewind reads the brief under it, so a proof recorded in between (another session edits files to Y2 and proves step 2 at Y2) is compared with the older tree Y1 and step 2 is wrongly reopened and its proof dropped (core.py ~3642/3652, hooks.py ~1581-1610). Have rewind_tree return a cheap signature of the brief's evidence and re-snapshot under the lock when it changed; and give reconcile_rewind a sentinel instead of tree=None meaning both 'no proof' and 'no tree passed' (T-3582 review)
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
- 2026-11-07T04:53:30Z created
## Follow-ups captured
