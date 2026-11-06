---
id: T-2550
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: foresight
created: 2026-11-02T06:00:06Z
updated: 2026-11-02T06:07:46Z
trigger: foresight-cochange
trigger_key: 5f7c4f5e5612a450
---
# Breakage ahead: 048da03 changed plugin/tests/test_core.py without plugin/lib/fmcore.py,…
## Raw request
> Breakage ahead: 048da03 changed plugin/tests/test_core.py without plugin/lib/fmcore.py, which changed with it in most past commits
> foresight-cochange plugin/lib/fmcore.py
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
- 2026-11-02T06:07:46Z dropped: false alarm: 048da03 (T-2525) changed the evidence writer in plugin/lib/fmcli.py; its StartPoint tests live in test_core.py, so fmcore.py had nothing to change (git show --stat 048da03)
## Follow-ups captured
