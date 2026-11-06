---
id: T-3058
type: FIX
tier: L
status: dropped
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:08Z
updated: 2026-11-05T04:09:31Z
trigger: genesis-review
trigger_key: 4d5a9bf88aec95f5
---
# FIX: cross-cutting review gen-4 #2 (what got worse): Failed tool calls per 100 doubled…
## Raw request
> FIX: cross-cutting review gen-4 #2 (what got worse): Failed tool calls per 100 doubled over the pass, most of them the harness's own worktree isolation ("21× Bash cat", 8× sed, 8× python3) refusing its builders' commands. [0.6 → 1.3]
> genesis-review 4:2
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
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
- 2026-11-05T00:31:08Z created
- 2026-11-05T04:09:31Z dropped: covered by T-3129 (its T-3114 part: the builder prompt tells lanes to use the Edit tool for test additions and never read /tmp or the scratchpad)
## Follow-ups captured
