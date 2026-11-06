---
id: T-1933
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T07:46:30Z
updated: 2026-10-29T07:57:04Z
---
# _DCWD["seen"]` (3304) is cleared only at depth 0, which fmmcp already handles at 3301. Oth
## Raw request
> _DCWD["seen"]` (3304) is cleared only at depth 0, which fmmcp already handles at 3301. Otherwise none
> (noticed by an agent; research T-1923-review)
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
- 2026-10-29T07:46:30Z created
- 2026-10-29T07:57:04Z dropped: no change needed: every check_bash entry point (the hook, fmmcp.py:288) is a depth-0 call, which clears _DCWD and its seen pairs; script and nested reads run inside that call
## Follow-ups captured
