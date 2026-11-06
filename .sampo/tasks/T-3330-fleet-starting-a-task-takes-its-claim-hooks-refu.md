---
id: T-3330
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/tests/test_claims_remote.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:31:57Z
updated: 2026-11-06T04:31:58Z
---
# Fleet: starting a task takes its claim; hooks refuse edits once the claim is lost, naming the holder's machine
## Raw request
> Fleet: starting a task takes its claim; hooks refuse edits once the claim is lost, naming the holder's machine
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] with fleet on, clone A focuses T-x and holds its claim; clone B's focus of T-x is refused naming A's machine and until; after A's lease lapses B can take it; with fleet off nothing changes — verify with `python3 plugin/tests/run.py test_claims_remote test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test, red  <- CURRENT
2. [ ] focus takes the claim; edits check it at most once per 10 minutes
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:31:57Z created
## Follow-ups captured
