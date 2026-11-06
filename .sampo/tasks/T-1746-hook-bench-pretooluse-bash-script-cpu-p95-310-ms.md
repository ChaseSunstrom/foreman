---
id: T-1746
type: PERFORMANCE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-23T04:27:30Z
updated: 2026-10-23T05:58:05Z
---
# Hook bench: PreToolUse:Bash:script CPU p95 ~310 ms over its 300 ms budget at the current b
## Raw request
> Hook bench: PreToolUse:Bash:script CPU p95 ~310 ms over its 300 ms budget at the current base
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
- 2026-10-23T04:27:30Z created
- 2026-10-23T05:58:05Z dropped: not reproducible on a quiet machine: bench_hooks --runs 20 at load 0.6 per core gives PreToolUse:Bash:script median 266.5 ms, p95 272.3 ms against its 300 ms budget (the 310 ms reading was taken at 3.4-6.4 load per core); the full gates' bench passed twice since
## Follow-ups captured
