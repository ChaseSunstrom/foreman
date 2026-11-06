---
id: T-3062
type: FIX
tier: L
status: dropped
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:10Z
updated: 2026-11-05T04:18:01Z
trigger: genesis-review
trigger_key: f7571d1760f32acc
---
# FIX: cross-cutting review gen-4 #6 (what grew without earning it): 974 files and 136k…
## Raw request
> FIX: cross-cutting review gen-4 #6 (what grew without earning it): 974 files and 136k lines in one generation, most of it a package rename that duplicates every fmX.py as sampo/X.py plus a shim, so the library now exists twice in the tree. [136193 insertions]
> genesis-review 4:6
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
- 2026-11-05T00:31:10Z created
- 2026-11-05T04:18:01Z dropped: premise false: each plugin/lib/fmX.py is a 4-line shim (sys.modules alias) to sampo/X.py, pinned by test_rename_aliases, so the library exists once; the file count is the rename's moves, not a second copy
## Follow-ups captured
