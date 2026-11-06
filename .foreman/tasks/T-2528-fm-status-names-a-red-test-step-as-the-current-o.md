---
id: T-2528
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T03:30:48Z
updated: 2026-11-02T03:31:19Z
---
# fm status names a red-test step as the current one after its failing evidence and the…
## Raw request
> fm status names a red-test step as the current one after its failing evidence and the next step's green run (T-2527: Step 1/2 while fm next says every step has its evidence); a red step's expected failure could count as its proof
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
- 2026-11-02T03:30:48Z created
- 2026-11-02T03:31:19Z dropped: by design: finish reruns a red step's own failed command (fmcli.py:1282, T-1844) and closes it on the pass; until then its newest run did fail, so status naming it current is accurate
## Follow-ups captured
