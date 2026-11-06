---
id: T-0091
type: CLEAN
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T19:09:28Z
updated: 2026-10-02T19:09:34Z
base: 994a4aa912590170d992e89c24c3fc45429e824c
---
# Remove the session dev-mods copy of foreman-ui (installed plugin replaces it)
## Raw request
> Remove the session dev-mods copy of foreman-ui (installed plugin replaces it)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] no dev-mods copy left — verify with `test ! -e ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] remove the copy  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-02T19:09:28Z created
- 2026-10-02T19:09:28Z focused
- 2026-10-02T19:09:28Z guard authorization added: rm-outside
- 2026-10-02T19:09:34Z dropped: rm of the dev-mods copy was denied by the user; left in place
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- playbook Verification Loop Skill (skills/playbooks/references/verify/verification-loop.md)
- T-0009 [FEATURE L, done, 10 steps] Autonomy: plain-chat approvals, Claude runs everything, multi-lens audits before done
- research t0018-r1-edge: sh` is missing, and will raise `UnicodeDecodeError` if the command's stdout/stderr contains bytes that aren't valid UTF‑8 (binary output, or any …
- similar past tasks were L: consider --tier L
- the similar finished task took 10 steps
