---
id: T-3332
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py]
depends_on: []
source: discovered
created: 2026-11-06T04:32:01Z
updated: 2026-11-06T04:32:02Z
lane: ~/.claude/foreman/.claude/worktrees/agent-acd1b9b94054d0907
lane_branch: worktree-agent-acd1b9b94054d0907
---
# Kalevala: _decide and the restarted check run outside the project lock, so two concurrent steps can snapshot a tower twice and log an act twice
## Raw request
> Kalevala: _decide and the restarted check run outside the project lock, so two concurrent steps can snapshot a tower twice and log an act twice
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] two concurrent kalevala.step calls on one project log each act once and snapshot a stalled tower once — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] concurrency test, red  <- CURRENT
2. [ ] take c.lock around _decide and the restarted check (kalevala.py:228-230, :584)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:32:01Z created
## Follow-ups captured
