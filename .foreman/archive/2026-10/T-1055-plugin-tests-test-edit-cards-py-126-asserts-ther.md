---
id: T-1055
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T03:47:16Z
updated: 2026-10-16T04:59:31Z
---
# Plugin/tests/test_edit_cards.py:126` asserts there are no `dep:` signals in the map, which
## Raw request
> plugin/tests/test_edit_cards.py:126` asserts there are no `dep:` signals in the map, which contradicts this feature; reword it. Also: the Python distribution-to-import-name alias table is too small t…
> (noticed by an agent; research T-1036-review)
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
- 2026-10-16T03:47:16Z created
- 2026-10-16T04:59:31Z dropped: done in T-1036: the test now says there are no dep signals in this repo, matching the feature
## Follow-ups captured
