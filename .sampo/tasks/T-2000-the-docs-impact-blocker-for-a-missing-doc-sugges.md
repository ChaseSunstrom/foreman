---
id: T-2000
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdocs.py, plugin/tests/test_docsdrift.py]
depends_on: []
source: user
created: 2026-10-29T14:47:35Z
updated: 2026-10-29T15:19:28Z
done_in: T-2001
---
# The docs-impact blocker for a missing doc suggests up to three tracked paths when…
## Raw request
> FEATURE: the docs-impact blocker for a missing doc suggests up to three tracked paths when several end with the name (one exact match already suggested, T-1995)
> @plugin/lib/fmdocs.py @plugin/tests/test_docsdrift.py
> DONE-WHEN: two tracked docs ending with the name are both suggested :: python3 plugin/tests/run.py test_docsdrift -k suggests
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
- 2026-10-29T14:47:35Z created
- 2026-10-29T14:47:39Z set tier=S
- 2026-10-29T14:47:48Z batched into T-2001
- 2026-10-29T15:19:28Z done in T-2001 (batch)
## Follow-ups captured
