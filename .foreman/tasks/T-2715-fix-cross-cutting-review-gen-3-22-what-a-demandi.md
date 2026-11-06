---
id: T-2715
type: FIX
tier: L
status: blocked
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:48Z
updated: 2026-11-02T23:19:45Z
trigger: genesis-review
trigger_key: 61549e5e034df198
---
# FIX: cross-cutting review gen-3 #22 (what a demanding user would complain about first):…
## Raw request
> FIX: cross-cutting review gen-3 #22 (what a demanding user would complain about first): a grep for "guard_block" counts in the agent's own ledger was refused as reading a credential, and T-2665 explicitly reverted the fix; the agent is blocked from measuring the guard's own over-refusals by the rule it was measuring. [1× credentials: '.ssh]
> genesis-review 3:22
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
- 2026-11-02T23:14:48Z created
- 2026-11-02T23:19:45Z blocked: needs the user: relaxing the guard's credential-path refusal is guard design under the standing safety hold (T-1937, T-1928), and T-2665's read-API exemption was reverted for failing open (io.FileIO, linecache, fileinput); the user decides whether a narrower form is safe
## Follow-ups captured
