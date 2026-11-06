---
id: T-0577
type: SECURITY
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-09T14:43:54Z
updated: 2026-10-09T16:03:04Z
done_in: T-0669
---
# SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
## Raw request
> SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): a backslash-newline inside single quotes that a second shell reads: eval 'claude plugin ins\<newline>tall x@y', bash -c 'r\<newline>m -rf ~', the same through trap. Fix so the fixture's open mark comes off; real-bash rows
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
- 2026-10-09T14:43:54Z created
- 2026-10-09T15:33:09Z batched into T-0669
- 2026-10-09T16:03:04Z done in T-0669 (batch)
## Follow-ups captured
