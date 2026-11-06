---
id: T-2450
type: FIX
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T06:11:41Z
updated: 2026-11-01T07:17:24Z
---
# fm find's secrets finder flags a date under a secret-like name as a secret literal…
## Raw request
> FIX: fm find's secrets finder flags a date under a secret-like name as a secret literal (token_expires = "2030-01-09" in a .toml); a value that is a plain ISO date (or a number) can't be a credential. Found by T-2409's breakage render in test_find.FindRenders
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
- 2026-11-01T06:11:41Z created
- 2026-11-01T07:17:24Z deferred: round 1 first: standing rule 2 (user steer 2026-10-31) bars maintenance until round 1 is done; picked up after
## Follow-ups captured
