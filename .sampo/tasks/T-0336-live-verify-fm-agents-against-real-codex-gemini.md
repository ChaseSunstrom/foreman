---
id: T-0336
type: RESEARCH
tier: S
status: blocked
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T02:40:33Z
updated: 2026-10-16T13:19:20Z
revisit: installed codex
---
# Live-verify fm agents on real codex, gemini and opencode
## Raw request
> Live-verify fm agents against real codex, gemini and opencode installs (tool names, exit-code semantics, Codex hooks.json load) — none are installed on this machine
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] each agent's real hook run refuses rm -rf ~ and shows Foreman's context
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] install and log in each agent, run fm agents install, try a refused command  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-06T02:40:33Z created
- 2026-10-06T02:40:54Z planned from capture
- 2026-10-06T02:40:54Z blocked: needs codex, gemini and opencode installed and logged in (API logins are the user's); none are on this machine
- 2026-10-16T13:19:20Z blocked: needs codex, gemini and opencode installed and logged in (API logins are the user's); none are on this machine (revisit installed codex)
## Follow-ups captured
