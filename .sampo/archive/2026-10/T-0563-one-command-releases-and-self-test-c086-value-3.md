---
id: T-0563
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:43Z
---
# One-command releases and self-test (C086, value 3/5, effort M, risk low)
## Raw request
> FEATURE: One-command releases and self-test (C086, value 3/5, effort M, risk low)
>   first version: scripts/release: clean git worktree, run tests, install-user into a temp HOME, then uninstall and diff the tree for a round trip, bump versions and changelog; skip blue/green.
>   what it is: Cut releases from a clean throwaway worktree with clean-install and upgrade tests.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:43Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
