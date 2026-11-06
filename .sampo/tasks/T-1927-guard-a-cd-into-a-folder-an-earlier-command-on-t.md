---
id: T-1927
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T06:54:07Z
updated: 2026-10-29T07:05:11Z
done_in: T-1924
---
# Guard: a cd into a folder an earlier command on the line removes is read as certain (rm -r
## Raw request
> Guard: a cd into a folder an earlier command on the line removes is read as certain (rm -rf S/wx; cd S/wx; git reset --hard from Foreman passes): treat a cd target that an earlier rm/rmdir/mv/unlink/find -delete/git worktree remove names as one that may fail
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
- 2026-10-29T06:54:07Z created
- 2026-10-29T07:05:11Z done in T-1924: T-1924 review fix: any cd after a command that isn't a pure reader may fail; rm/rmdir/find -delete/git worktree remove + cd into the folder now refused (probe t1927.txt, rows in test_repeated_cds_in_a_line_are_judged_fast)
## Follow-ups captured
