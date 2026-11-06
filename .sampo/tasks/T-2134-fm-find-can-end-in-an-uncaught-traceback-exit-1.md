---
id: T-2134
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:25:50Z
updated: 2026-10-30T10:25:58Z
---
# fm find` can end in an uncaught traceback (exit 1) outside the try at fmfind.py:548.…
## Raw request
> fm find` can end in an uncaught traceback (exit 1) outside the try at fmfind.py:548. Move `precision(p)` inside the try, so a crash exits 2 for every caller, not just MCP
> (noticed by an agent; research T-2127-review)
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
- 2026-10-30T10:25:50Z created
- 2026-10-30T10:25:58Z dropped: fixed inline in T-2127: precision(p) now sits inside cmd_find's try
## Follow-ups captured
