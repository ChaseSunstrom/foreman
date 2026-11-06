---
id: T-0893
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T16:40:34Z
updated: 2026-10-15T18:29:47Z
---
# Guard: claude plugin install with HOME=<scratch literal> (a sandbox HOME) counts as a chan
## Raw request
> Guard: claude plugin install with HOME=<scratch literal> (a sandbox HOME) counts as a change to the real Claude config; exempt a literal scratch HOME only (unresolvable or real HOME still blocks) — loosens a USER_ONLY category, needs a security review
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
- 2026-10-15T16:40:34Z created
- 2026-10-15T18:29:47Z dropped: not worth loosening a user-only category: the sandbox-HOME install happened once (T-0874) and the pinned fm ask plugin grant covered it; a safe exemption would also have to model CLAUDE_CONFIG_DIR and every other way claude finds its config
## Follow-ups captured
