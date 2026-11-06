---
id: T-1989
type: FIX
tier: S
status: done
priority: normal
scope: [path, plugin/lib/fmcore.py]
depends_on: []
source: user
created: 2026-10-29T14:00:57Z
updated: 2026-10-29T14:11:13Z
done_in: T-1992
---
# An @path-only intake line under an item is dropped as untagged text instead of scoping that item
## Raw request
> FIX: an intake line made only of @path tokens, right under an item or its block lines, is dropped as untagged text instead of scoping that item (fmcore.parse_intake) @plugin/lib/fmcore.py
> DONE-WHEN: parse_intake attaches an @path-only line under an item to that item's scopes :: python3 plugin/tests/run.py test_core
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
- 2026-10-29T14:00:57Z created
- 2026-10-29T14:01:15Z set tier=S, title=An @path-only intake line under an item is dropped as untagged text instead of scoping that item
- 2026-10-29T14:01:19Z batched into T-1992
- 2026-10-29T14:11:13Z done in T-1992 (batch)
## Follow-ups captured
