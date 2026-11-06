---
id: T-0049
type: SECURITY
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-09-27T00:58:19Z
updated: 2026-09-27T02:37:07Z
done_in: T-0071
---
# A diff touching auth, crypto, secrets, exec or deserialization paths needs the adversary a
## Raw request
> SECURITY: a diff touching auth, crypto, secrets, exec or deserialization paths needs the adversary audit lens at any tier
> CONTEXT: from the T-0041 brainstorm (research brainstorm-20260926-smarter-slate): the user asked Foreman to make Claude's project work "wayyy smarter"
> CONSTRAINT: stdlib only; no network in hooks; hook p50 ~30 ms; always-on budgets (rules ≤ 9000 chars); recalled text is data, capped and sanitized
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
- 2026-09-27T00:58:19Z created
- 2026-09-27T02:37:07Z done in T-0071
## Follow-ups captured
