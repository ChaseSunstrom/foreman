---
id: T-2801
type: RESEARCH
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: cold
created: 2026-11-03T08:30:32Z
updated: 2026-11-03T21:11:20Z
---
# Read the hot files no session has read: MASTER.md, README.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/tests/test_guard.py, plugin/lib/fmdoctor.py, plugin/tests/test_cli.py, plugin/…
## Raw request
> Research debt (fm map --cold, T-0660): read and note what each does — MASTER.md, README.md, plugin/lib/fmgenesis.py, site/genesis/genesis.json, plugin/tests/test_guard.py, plugin/lib/fmdoctor.py, plugin/tests/test_cli.py, plugin/lib/fmexam.py, 15 left out. Local reading only.
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
- 2026-11-03T08:30:32Z created
- 2026-11-03T21:11:20Z dropped: stale: the cold-read list names the fm*.py paths, now shims since T-2748 moved the code to plugin/lib/sampo/; this session read MASTER, README, the genesis, doctor, exam and guard modules and their tests during the rename; fm map --cold will relist what is still unread under the new paths
## Follow-ups captured
