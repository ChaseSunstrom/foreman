---
id: T-0822
type: CLEAN
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-14T18:16:02Z
updated: 2026-10-14T18:35:48Z
---
# Round-1 review noticed: fmguard._run_dir (≈line 1287) duplicates _chain_dir's cd resolutio
## Raw request
> Round-1 review noticed: fmguard._run_dir (≈line 1287) duplicates _chain_dir's cd resolution with different semantics — merge them
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
- 2026-10-14T18:16:02Z created
- 2026-10-14T18:35:48Z dropped: Not a true duplicate: _run_dir finds where python - runs for the shadowed-module check (None already errs toward refusing), while _chain_dir must prove one folder for write targets and so refuses relative cd targets; merging either way changes behaviour (stricter would block the common cd plugin/lib && python3 - form)
## Follow-ups captured
