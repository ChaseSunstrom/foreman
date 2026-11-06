---
id: T-0304
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T13:17:40Z
updated: 2026-10-04T13:19:12Z
base: b194b51817a7dd1da6afa0fc1c1c8813b0b2ff04
base_tree: 65697cac5cb8b74298773121c690997ebc773421
---
# Install foreman-ui 0.6.0 for other sessions
## Raw request
> Install foreman-ui 0.6.0 for other sessions
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] doctor no longer reports the installed foreman-ui lagging — verify with `! fm doctor | grep -q 'foreman-ui release'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] claude plugin update foreman-ui@foreman
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `! fm doctor | grep -q 'foreman-ui release'` → ✗ exit 1 · (no output) [ran] [tree 65697cac5cb8] (2026-10-04T13:18:40Z)
- (step 1) `! fm doctor | grep -q 'foreman-ui release'` → ✗ exit 1 · (no output) [ran] [tree 65697cac5cb8] (2026-10-04T13:18:40Z)
- (step 1) `fm doctor | grep -q 'PASS  foreman-ui release'` → exit 0 · (no output) [ran] [tree 65697cac5cb8] (2026-10-04T13:19:01Z)
- (ac 1) `! fm doctor | grep -q 'foreman-ui release'` → ✗ exit 1 · (no output) [ran] [tree 65697cac5cb8] (2026-10-04T13:19:08Z)
## Log
- 2026-10-04T13:17:40Z created
- 2026-10-04T13:17:40Z focused
- 2026-10-04T13:18:29Z user approved plugin in Claude Code's permission prompt
- 2026-10-04T13:18:30Z plugin grant used for: claude plugin update changes Claude Code's plugins, MCP servers or config
- 2026-10-04T13:19:12Z dropped: dropped: the install itself succeeded (0.5.0 → 0.6.0; fm doctor: PASS foreman-ui release), but criterion 1 was miswritten (its grep also matches the PASS line) and criteria can't be edited
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0303 [FEATURE S, dropped, 1 steps] Install foreman-ui 0.6.0 for other sessions
- T-0091 [CLEAN S, dropped, 1 steps] Remove the session dev-mods copy of foreman-ui (installed plugin replaces it)
- T-0039 [SECURITY S, done, 1 steps] setup-plugins.sh refuses a real run inside a Claude Code session (CLAUDECODE=1): install one plugin with fm ask --pin + fm plugins ins…
- T-0276 [FEATURE L, done, 4 steps] fm second: one primitive for independent second reads — rival-model plan review, debate rebuttal, daily session review,… — lesson: Anyt…
- similar finished tasks took 1–4 steps
