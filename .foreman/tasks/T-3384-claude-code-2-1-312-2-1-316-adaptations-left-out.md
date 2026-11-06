---
id: T-3384
type: FEATURE
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:41:43Z
updated: 2026-11-06T06:42:28Z
---
# Claude Code 2.1.312-2.1.316 adaptations left out of T-3341: per-lane-class subagent…
## Raw request
> FEATURE: Claude Code 2.1.312-2.1.316 adaptations left out of T-3341: per-lane-class subagent effort (CLAUDE_CODE_SUBAGENT_EFFORT), the 24-concurrent-hooks cap warning, safety_event ingestion, group budgets, the worktree-lifetime gate (see T-3341's raw request)
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
- 2026-11-06T06:41:43Z created
- 2026-11-06T06:42:28Z scope after T-3341 review: keep CLAUDE_CODE_SUBAGENT_EFFORT per lane class (2.1.316) and the subagent worktree-lifetime doctor gate (2.1.311); drop as moot: 24-hook cap (prompt/agent hooks only, Sampo has none), safety_event (CC stopped sending it in 2.1.312), pooled group budgets (gateway admin only)
## Follow-ups captured
