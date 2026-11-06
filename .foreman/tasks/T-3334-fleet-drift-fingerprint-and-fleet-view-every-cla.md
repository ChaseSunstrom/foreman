---
id: T-3334
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/claims.py, plugin/lib/sampo/mandate.py, plugin/lib/sampo/sync.py, plugin/tests/test_drift_fleet.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:32:05Z
updated: 2026-11-06T04:32:05Z
---
# Fleet: drift fingerprint and fleet view: every claim carries a hash of mandate, root seal, tower gen-0s, steers, standing intent and plugin version; a mismatch refuses tower claims and names the differing part; sampo fleet lists who works what where from the refs
## Raw request
> Fleet: drift fingerprint and fleet view: every claim carries a hash of mandate, root seal, tower gen-0s, steers, standing intent and plugin version; a mismatch refuses tower claims and names the differing part; sampo fleet lists who works what where from the refs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a clone with a different mandate is listed by sampo fleet with the differing part named and its tower claims refused; mandate and gen-0 hashes travel in the mirror — verify with `python3 plugin/tests/run.py test_drift_fleet`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test, red  <- CURRENT
2. [ ] fingerprint + refusal
3. [ ] sampo fleet from refs
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:32:05Z created
## Follow-ups captured
