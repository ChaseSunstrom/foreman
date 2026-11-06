---
id: T-1864
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T21:51:14Z
updated: 2026-10-28T21:57:05Z
done_in: T-1661
---
# The hint row in plugin/lib/fmcodetui.py:1868 grew to about 119 cells and may clip "l layou
## Raw request
> the hint row in plugin/lib/fmcodetui.py:1868 grew to about 119 cells and may clip "l layout" and "Esc close" below 120 columns, which is worth a width check
> (noticed by an agent; research T-1661-review)
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
- 2026-10-28T21:51:14Z created
- 2026-10-28T21:57:05Z done in T-1661: settings hints wrap onto the note's spare line; test_settings_room covers 120/100/80 columns
## Follow-ups captured
