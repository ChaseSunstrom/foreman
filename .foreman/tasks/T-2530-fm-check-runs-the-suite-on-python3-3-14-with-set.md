---
id: T-2530
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T03:46:27Z
updated: 2026-11-02T03:47:09Z
---
# fm check runs the suite on python3 (3.14, with setuptools) while fm ship's remembered…
## Raw request
> fm check runs the suite on python3 (3.14, with setuptools) while fm ship's remembered test runs uv python3.12 (none): a host-dependent failure passes the gate and fails the ship (T-2524 → T-2529); the gate could say so, or run the affected tests on the ship's interpreter too
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
- 2026-11-02T03:46:27Z created
- 2026-11-02T03:47:09Z dropped: measured: 1 of 22 ship baselines was interpreter-specific (T-2529); fm ship's affected-first run already catches it in minutes before any push; revisit if a second one appears
## Follow-ups captured
