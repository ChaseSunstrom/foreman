---
id: T-2628
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T18:33:57Z
updated: 2026-11-02T18:41:41Z
---
# - `--jobs 1` is silently raised to 4 in the exam parser (fmcli.py ~7686-7719), a small…
## Raw request
> - `--jobs 1` is silently raised to 4 in the exam parser (fmcli.py ~7686-7719), a small bug that deserves its own task
> (noticed by an agent; research T-2625-review)
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
- 2026-11-02T18:33:57Z created
- 2026-11-02T18:41:41Z dropped: fixed in T-2625 (ea67498a): --jobs defaults to None in the shared parser; steer run 4, long and short runs 1, --jobs 0 still refused
## Follow-ups captured
