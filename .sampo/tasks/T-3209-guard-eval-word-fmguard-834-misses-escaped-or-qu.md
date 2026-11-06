---
id: T-3209
type: SECURITY
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T13:54:51Z
updated: 2026-11-05T13:54:51Z
group: guard bypasses and over-refusals
---
# Guard: _EVAL_WORD (fmguard ~834) misses escaped or quoted builtins (e\val, ev""al, '.'…
## Raw request
> guard: _EVAL_WORD (fmguard ~834) misses escaped or quoted builtins (e\val, ev""al, '.' f, \. f), the same blind spot T-2261's review found in _FILTER_REDEFINED
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
- 2026-11-05T13:54:51Z created
## Follow-ups captured
