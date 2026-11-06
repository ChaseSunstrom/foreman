---
id: T-1617
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T20:54:57Z
updated: 2026-10-22T20:55:10Z
---
# No test shows an absolute-path program can't write outside the temp folder (e.g. `/usr/bin
## Raw request
> no test shows an absolute-path program can't write outside the temp folder (e.g. `/usr/bin/touch /etc/x`)
> (noticed by an agent; research T-1553-review)
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
- 2026-10-22T20:54:57Z created
- 2026-10-22T20:55:10Z dropped: covered in T-1553: test_nothing_real_runs now runs /usr/bin/touch on the line's folder, the home and /etc and checks nothing was written
## Follow-ups captured
