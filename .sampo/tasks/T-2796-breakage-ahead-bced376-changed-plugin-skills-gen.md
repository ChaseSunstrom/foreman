---
id: T-2796
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: foresight
created: 2026-11-03T06:00:04Z
updated: 2026-11-03T21:07:47Z
trigger: foresight-cochange
trigger_key: f04b4c3d82032f09
---
# Breakage ahead: bced376 changed plugin/skills/genesis/SKILL.md without…
## Raw request
> Breakage ahead: bced376 changed plugin/skills/genesis/SKILL.md without plugin/lib/fmgenesis.py, which changed with it in most past commits
> foresight-cochange plugin/lib/fmgenesis.py
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
- 2026-11-03T06:00:04Z created
- 2026-11-03T21:07:47Z dropped: not a breakage: bced376 renamed wording in the genesis skill (T-2768); no behaviour in fmgenesis.py (now sampo/genesis) depends on that prose, and test_genesis passed at every close since
## Follow-ups captured
