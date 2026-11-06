---
id: T-0303
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T13:17:33Z
updated: 2026-10-04T13:17:40Z
base: b194b51817a7dd1da6afa0fc1c1c8813b0b2ff04
base_tree: 65697cac5cb8b74298773121c690997ebc773421
---
# Install foreman-ui 0.6.0 for other sessions
## Raw request
> Install foreman-ui 0.6.0 for other sessions
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the installed foreman-ui is 0.6.0 — verify with `fm doctor | grep -v 'foreman-ui release'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] claude plugin update foreman-ui@foreman  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-04T13:17:33Z created
- 2026-10-04T13:17:33Z focused
- 2026-10-04T13:17:40Z dropped: dropped: criterion's verify always passed; recreated
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0091 [CLEAN S, dropped, 1 steps] Remove the session dev-mods copy of foreman-ui (installed plugin replaces it)
- T-0039 [SECURITY S, done, 1 steps] setup-plugins.sh refuses a real run inside a Claude Code session (CLAUDECODE=1): install one plugin with fm ask --pin + fm plugins ins…
- T-0276 [FEATURE L, done, 4 steps] fm second: one primitive for independent second reads — rival-model plan review, debate rebuttal, daily session review,… — lesson: Anyt…
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- similar finished tasks took 1–4 steps
