---
id: T-2990
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T17:04:32Z
updated: 2026-11-05T03:53:33Z
trigger: ci-red
trigger_key: 09aeed4b8bce88fb
group: CI red on branch and main
---
# FIX: CI on main is red at e8c214a (tests)
## Raw request
> FIX: CI on main is red at e8c214a (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/sampo/commit/e8c214af278b6ab462f2e2c48fdaa4501dff6728
> CI-red: e8c214af278b6ab462f2e2c48fdaa4501dff6728
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
- 2026-11-04T17:04:32Z created
- 2026-11-05T03:53:33Z dropped: duplicate of T-2969 (CI on main red since d1901b5: test_moons_scale needs an embedder, test_ui_replay's child outlives its timeout)
## Follow-ups captured
