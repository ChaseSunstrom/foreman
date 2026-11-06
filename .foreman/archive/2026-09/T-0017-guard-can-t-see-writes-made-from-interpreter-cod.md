---
id: T-0017
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-09-26T13:06:12Z
updated: 2026-09-26T13:08:06Z
---
# Guard can't see writes made from interpreter code (python3 - <<EOF … open(core_path,'w')…,
## Raw request
> Guard can't see writes made from interpreter code (python3 - <<EOF … open(core_path,'w')…, python -c, node -e): a Bash command that names a protected-core path together with a write primitive should count as a core write
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Verification evidence
## Log
- 2026-09-26T13:06:12Z created
- 2026-09-26T13:08:06Z dropped: merged into T-0009: the gap weakens T-0009's acceptance criterion 'protected core covers plugin/lib, bin, hooks'; fixed inline under T-0009's core grant
## Follow-ups captured
