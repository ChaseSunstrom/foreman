---
id: T-0022
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-09-26T15:13:41Z
updated: 2026-09-26T17:14:44Z
explore: true
---
# Foreman state that travels with the repo: opt-in `fm sync on` mirrors briefs (without allo
## Raw request
> FEATURE?: Foreman state that travels with the repo: opt-in `fm sync on` mirrors briefs (without allow/approved/pending fields), decisions, research and a compact history into a committed .foreman/ folder and imports them after a clone or on another machine; approvals, pending asks, sessions, locks and logs stay local; sensitive repos default off
> CONTEXT: user asked "shouldn't all context/things foreman tracks/needs be in source control? like tasks, etc.? so it's easier to resume? or no?" — answered: partly, opt-in; authorization data must never come from git
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
- 2026-09-26T15:13:41Z created
- 2026-09-26T17:14:44Z dropped: done in T-0018 round 3 (c9870a7): fm sync on|off|status|import|export
## Follow-ups captured
