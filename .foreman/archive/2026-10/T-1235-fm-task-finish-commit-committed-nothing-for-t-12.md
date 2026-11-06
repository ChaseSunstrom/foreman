---
id: T-1235
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T17:43:39Z
updated: 2026-10-16T20:24:12Z
done_in: T-1242
---
# Fm task finish --commit committed nothing for T-1234: its files were edited while T-1231 w
## Raw request
> fm task finish --commit committed nothing for T-1234: its files were edited while T-1231 was focused, though a 'scope:' log line named them; finish should commit the files its scope and scope-log name, or say which changed files it is leaving out and why
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
- 2026-10-16T17:43:39Z created
- 2026-10-16T20:24:12Z done in T-1242: finish --commit names uncommitted files it didn't change and --with commits one; tests in test_dirty_at_focus.EditedUnderAnotherTask
## Follow-ups captured
