---
id: T-3353
type: CLEAN
tier: M
status: planned
priority: normal
scope: [plugin/rules/foreman.md, MASTER.md, docs/map/ops-1.md, plugin/agents/fm-builder.md, plugin/agents/fm-reviewer.md, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T05:33:56Z
updated: 2026-11-06T05:33:57Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a879c1c0c29cef328
lane_branch: worktree-agent-a879c1c0c29cef328
---
# Tonight's lessons into the prompts every session loads: the operating rules, MASTER.md and its ops map, and the builder and reviewer agent definitions plus the lane brief
## Raw request
> Tonight's lessons into the prompts every session loads: the operating rules, MASTER.md and its ops map, and the builder and reviewer agent definitions plus the lane brief
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the builder contract (fm-builder.md and the lane brief, kept in step by test_lanes T-1151) says: a red affected check reruns only its failing classes alone and, if they pass alone and touch none of the lane's files, records that run and commits naming them; 'lock busy' (exit 3) means rerun the same command; never pipe a run through tail/grep when its exit code is the evidence; no PYTHON_CPU_COUNT prefix (the slot pool shares CPUs) — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] the operating rules and MASTER.md say: every finished lane gets one review (/foreman:review, or one fm-reviewer) against the integration branch, not main; should-level findings go back to the same builder (SendMessage) before the merge; anything new shown to the user uses the current product name; every fixed list or limit gets asked whether it binds; the reviewer definition says to diff against the base the brief names — verify with `python3 plugin/tests/run.py test_docs test_rules`
## Non-goals
## Approach (options → choice → why)
1) a line each in the files sessions already load: cheapest, no new machinery. 2) a new 'lessons' file sessions read: one more file nobody loads. 3) only memory: invisible to builders and other sessions. Choice 1; the rules file stays within its context budget.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] builder contract lines in fm-builder.md and the lane brief, test_lanes in step  <- CURRENT
2. [ ] rules, MASTER and ops-1 lines for the lead, reviewer base line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:33:56Z created
## Follow-ups captured
