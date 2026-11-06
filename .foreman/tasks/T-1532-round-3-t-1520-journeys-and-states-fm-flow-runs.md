---
id: T-1532
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmflow.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/tests/test_flow.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:46Z
updated: 2026-10-22T20:59:25Z
---
# Round 3 (T-1520): Journeys and states: fm flow runs user journeys as verify commands, fm s
## Raw request
> Round 3 (T-1520): Journeys and states: fm flow runs user journeys as verify commands, fm stories renders a component state matrix, screens declared as state charts with every state shot, and a crawler that maps a generated web app into a UI state graph (c052 c053 c069 c097). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Journeys and states: fm flow runs user journeys as verify commands, fm stories renders a component state matrix, screens declared as state charts with every state shot, and a crawler that maps a generated web app into a UI state graph (c052 c053 c069 c097). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm flow runs a journey file and fails on a missing element; fm stories builds a state matrix page — verify with `cd plugin/tests && python3 -m unittest test_flow`
## Non-goals
## Approach (options → choice → why)
Options: Playwright test files (a dependency on the project); chosen: fm flow FILE runs a journey (goto, click, type, expect) through the smoke harness as a verify command; fm stories renders a component state matrix page; a state-chart file lists states to shoot; a crawler follows links and buttons into a state graph.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] fm flow
3. [ ] fm stories and state charts
4. [ ] crawler
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:46Z created
- 2026-10-22T17:58:15Z set scope=['plugin/lib/fmflow.py', 'plugin/lib/fmcli.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_flow.py', 'CHANGELOG.md']
- 2026-10-22T20:59:25Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1532
## Follow-ups captured
