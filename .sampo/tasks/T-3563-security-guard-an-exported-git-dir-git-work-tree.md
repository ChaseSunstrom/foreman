---
id: T-3563
type: FEATURE
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:51:19Z
updated: 2026-11-07T00:51:19Z
---
# SECURITY guard: an exported GIT_DIR / GIT_WORK_TREE / GIT_CONFIG_* set earlier on the…
## Raw request
> SECURITY guard: an exported GIT_DIR / GIT_WORK_TREE / GIT_CONFIG_* set earlier on the line (export X=…; …; git <write verb>) is never seen: the guard reads only git_env inline on the git argv (fmguard.py ~3715), so a later git checkout/merge/reset can write into another tree than the guard judged. Treat any GIT_\w*= assignment or export earlier in the command as making every later git write's target unknown (refuse as tree write), with FORMS rows (T-3537 security review)
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
- 2026-11-07T00:51:19Z created
## Follow-ups captured
