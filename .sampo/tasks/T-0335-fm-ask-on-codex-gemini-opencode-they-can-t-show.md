---
id: T-0335
type: FEATURE
tier: M
status: blocked
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T02:40:33Z
updated: 2026-10-06T03:15:30Z
---
# fm ask grants on Codex, Gemini CLI and opencode
## Raw request
> fm ask on Codex/Gemini/opencode: they can't show Claude Code's permission prompt, so a guard category can only be granted from a Claude session; give them a grant path (e.g. the agent's own ask decision or fm grant from a terminal)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a grant on another agent comes only from the user's own input — verify with `true`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] verify host hooks live (T-0336), then design  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-06T02:40:33Z created
- 2026-10-06T03:15:30Z planned from capture
- 2026-10-06T03:15:30Z blocked: depends on T-0336: whether Codex/Gemini/opencode fire their prompt hook for agent-written subagent prompts decides if a chat yes is safe
## Follow-ups captured
