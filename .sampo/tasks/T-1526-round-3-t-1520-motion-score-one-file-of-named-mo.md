---
id: T-1526
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmmotion.py, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, mods/foreman-ui/hooks, plugin/tests/test_motion_score.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:44Z
updated: 2026-10-22T20:59:21Z
---
# Round 3 (T-1520): Motion Score: one file of named motions that compiles to CSS, WAAPI, thr
## Raw request
> Round 3 (T-1520): Motion Score: one file of named motions that compiles to CSS, WAAPI, three.js tweens, the fm code app clock and the foreman-ui pane, with a motion lab page and a player that edits timing by dragging (a061 a084 b033 c172 a158). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Motion Score: one file of named motions that compiles to CSS, WAAPI, three.js tweens, the fm code app clock and the foreman-ui pane, with a motion lab page and a player that edits timing by dragging (a061 a084 b033 c172 a158). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] one score compiles to CSS, WAAPI, three.js and the TUI clock with the same timings; every motion has a reduced form — verify with `cd plugin/tests && python3 -m unittest test_motion_score`
## Non-goals
## Approach (options → choice → why)
Options: per-surface motion code; chosen: a Motion Score JSON (named motions: duration token, easing, properties, reduced form) in plugin/lib/fmmotion.py that compiles to CSS custom properties and keyframes, a WAAPI object, three.js tween parameters, the fm code app clock and the foreman-ui option set; a lab page renders each motion and a player edits timing.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] score format and validation
3. [ ] compilers
4. [ ] lab page and player
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:44Z created
- 2026-10-22T17:57:57Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcodetui.py', 'mods/foreman-ui/hooks', 'plugin/tests/test_motion_score.py', 'CHANGELOG.md']
- 2026-10-22T20:59:21Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1526
## Follow-ups captured
