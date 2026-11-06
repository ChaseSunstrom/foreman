---
id: T-1795
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-27T22:28:59Z
updated: 2026-10-27T22:29:29Z
---
# Cut Foreman's usage burn: compact at 200k, builders on Sonnet, watchdog for headless runs
## Raw request
> Cut Foreman's usage burn: compact at 200k, builders on Sonnet, watchdog for headless runs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm setup adds CLAUDE_CODE_AUTO_COMPACT_WINDOW=200k and every builder lane runs on Sonnet with an earlier compact window — verify with `python3 plugin/tests/run.py test_setup test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests for the compact window env and the Sonnet M builder  <- CURRENT
2. [ ] fmsetup ENV + fmlanes model + fm-builder autoCompactWindow
3. [ ] apply to the user's settings via fm setup and confirm
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-27T22:28:59Z created
- 2026-10-27T22:29:29Z dropped: recreated with interpretation and approach
## Follow-ups captured
