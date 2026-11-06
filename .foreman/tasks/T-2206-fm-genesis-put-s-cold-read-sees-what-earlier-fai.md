---
id: T-2206
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T19:55:20Z
updated: 2026-10-30T19:55:30Z
---
# fm genesis put's cold read sees what earlier failed reads of the same file named, so it checks those were met instead of re-litigating them; it still fails any unmet one and any new breach, and the list clears when the file passes
## Raw request
> fm genesis put's cold read sees what earlier failed reads of the same file named, so it checks those were met instead of re-litigating them; it still fails any unmet one and any new breach, and the list clears when the file passes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a failed read's findings reach the next read of that file, fenced, and clear on a pass — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red: GenesisRead test for previous-reads carry, fence and clear  <- CURRENT
2. [ ] fmgenesis: READS store, prompt block, READ_CHILD instruction; MASTER + CHANGELOG
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-30T19:55:20Z created
- 2026-10-30T19:55:30Z dropped: duplicate of T-2205, which takes its criterion and steps
## Follow-ups captured
