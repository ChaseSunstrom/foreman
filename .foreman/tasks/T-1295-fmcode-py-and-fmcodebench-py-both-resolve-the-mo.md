---
id: T-1295
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:30:59Z
updated: 2026-10-20T23:28:16Z
---
# Fmcode.py` and `fmcodebench.py` both resolve the `models.json` location separately. A shar
## Raw request
> fmcode.py` and `fmcodebench.py` both resolve the `models.json` location separately. A shared `models_path` helper might be worth its own task
> (noticed by an agent; research T-1215-review)
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
- 2026-10-20T21:30:59Z created
- 2026-10-20T23:28:16Z dropped: not worth a helper: two call sites of one os.path.join(foreman_home(), 'models.json'); a shared helper adds more than it saves
## Follow-ups captured
