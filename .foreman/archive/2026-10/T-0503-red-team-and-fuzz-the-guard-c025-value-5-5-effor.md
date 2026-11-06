---
id: T-0503
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:30:32Z
---
# Red-team and fuzz the guard (C025, value 5/5, effort M, risk med)
## Raw request
> SECURITY: Red-team and fuzz the guard (C025, value 5/5, effort M, risk med)
>   first version: First version: a differential fuzzer in tests that generates shell snippets from a grammar of mutations on known-blocked fixtures, runs fmguard and asserts no known-dangerous effect passes (oracle: bash -n plus a dry effect list in a tmp dir); escapes are saved as test fixtures. Read-only against the guard, so it only tightens.
>   what it is: Attack the guard unattended with adversary agents, fuzzers and leagues, and keep every escape as a regression case.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:30:32Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
