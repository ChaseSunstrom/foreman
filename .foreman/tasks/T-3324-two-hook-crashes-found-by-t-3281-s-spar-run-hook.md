---
id: T-3324
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T04:30:12Z
updated: 2026-11-06T04:30:12Z
---
# Two hook crashes found by T-3281's spar run: hooks.py:1417…
## Raw request
> Two hook crashes found by T-3281's spar run: hooks.py:1417 meta.pop('resume_after_reload') has no default and raises KeyError; hooks.py:130 json.loads on hook stdin is unguarded, so malformed input is a traceback, not a clean refusal. Test each with the malformed payload
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
- 2026-11-06T04:30:12Z created
## Follow-ups captured
