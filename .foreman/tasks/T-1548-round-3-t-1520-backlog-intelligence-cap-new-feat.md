---
id: T-1548
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_backlog.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:51Z
updated: 2026-10-22T20:59:35Z
---
# Round 3 (T-1520): Backlog intelligence: cap new FEATURE captures against closed work, reje
## Raw request
> Round 3 (T-1520): Backlog intelligence: cap new FEATURE captures against closed work, reject duplicate proposals at capture, a good-first-task list, swipe through the deferred backlog, learn priorities from two-way choices, attach deferred ideas to active work by file overlap, re-verify closed tasks when later commits touch their files, a premise probe before building, a spike before any L feature, and a pasted ticket or error configuring the next run (b078 a145 b092 c014 c035 c030 c026 c029 c101 b119). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Backlog intelligence: cap new FEATURE captures against closed work, reject duplicate proposals at capture, a good-first-task list, swipe through the deferred backlog, learn priorities from two-way choices, attach deferred ideas to active work by file overlap, re-verify closed tasks when later commits touch their files, a premise probe before building, a spike before any L feature, and a pasted ticket or error configuring the next run (b078 a145 b092 c014 c035 c030 c026 c029 c101 b119). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] a capture near a closed task names it; a duplicate is refused with the existing id; a later commit to a closed task's files queues its re-verify — verify with `cd plugin/tests && python3 -m unittest test_backlog`
## Non-goals
## Approach (options → choice → why)
Options: manual triage; chosen: capture-time checks (a new FEATURE near a closed one is flagged with that id; duplicates rejected with the existing id), a good-first-task list, a swipe page for the deferred backlog (fm page), priorities learned from two-way choices, deferred ideas attached to active work by file overlap, closed tasks re-verified when later commits touch their files (a sentinel job), a premise probe step before building, a spike before any L feature, and a pasted ticket or error turned into a planned brief.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] capture checks
3. [ ] good-first list, swipe page, two-way priorities
4. [ ] re-verify, premise probe, spike rule, pasted ticket
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:51Z created
- 2026-10-22T18:06:20Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
- 2026-10-22T20:59:35Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1548
## Follow-ups captured
