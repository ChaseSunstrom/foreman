---
id: T-2552
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: foresight
created: 2026-11-02T06:00:06Z
updated: 2026-11-02T06:08:08Z
trigger: foresight-cochange
trigger_key: eff98a75b342c7f4
---
# Breakage ahead: 18101f0 changed plugin/lib/fmgenesis.py without…
## Raw request
> Breakage ahead: 18101f0 changed plugin/lib/fmgenesis.py without plugin/tests/test_genesis.py, which changed with it in most past commits
> foresight-cochange plugin/tests/test_genesis.py
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
- 2026-11-02T06:00:06Z created
- 2026-11-02T06:08:08Z dropped: false alarm: 18101f0 (T-2524) added one KIND_WORDS entry to fmgenesis.py; its test is in test_exam.py (asserts 'package' in fmgenesis.KIND_WORDS), not test_genesis.py
## Follow-ups captured
