---
id: T-1592
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T19:31:16Z
updated: 2026-10-22T20:29:17Z
---
# Perl -pi -e … /etc/hosts` is not in `_write_targets`; perl, ruby and node script files are
## Raw request
> perl -pi -e … /etc/hosts` is not in `_write_targets`; perl, ruby and node script files are never scanned by `_interpreter_reads
> (noticed by an agent; research T-1585-review)
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
- 2026-10-22T19:31:16Z created
- 2026-10-22T20:29:17Z dropped: done in T-1585: perl/ruby -i operands are write targets; script files run later stay a known ceiling (same as python script.py)
## Follow-ups captured
