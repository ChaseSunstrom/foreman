---
id: T-3341
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, plugin/agents/fm-builder.md]
depends_on: []
source: discovered
created: 2026-11-06T05:09:24Z
updated: 2026-11-06T05:52:53Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ae02f38ec38d05dfc
lane_branch: worktree-agent-ae02f38ec38d05dfc
---
# Claude Code 2.1.311-2.1.318 adaptation: doctor gate for SubagentStop firing once per subagent (2.1.311; older versions overcount budget rows), and fm-builder.md pins effort: high like every other agent (2.1.316-317 effort routing), with a test that every agent names effort
## Raw request
> Adapt to Claude Code 2.1.313-2.1.318 (release watch 2026-11-06): doctor's CC_FEATURES (doctor.py:1099) stops at 2.1.312. Add: pooled group budgets and CLAUDE_CODE_SUBAGENT_EFFORT (2.1.316) set per lane class (builder, reviewer, scout) and shown by doctor; a doctor warning when hook fan-out passes the 24-concurrent-hooks cap (2.1.312); ingest the claude_code.safety_event OTel event (2.1.307) into the guard's audit stats; gate the subagent worktree lifetime fix (2.1.311) for lanes. Source: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] check_cc_features((2,1,310)) warns naming SubagentStop and (2,1,318) passes; every plugin/agents/*.md names effort: — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] two failing tests  <- CURRENT
2. [ ] CC_FEATURES row and the builder's effort line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:09:24Z created
- 2026-11-06T05:52:52Z planned from capture
## Follow-ups captured
