---
id: T-1527
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmmotion.py, plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/tests/test_motion_verify.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:44Z
updated: 2026-10-22T20:59:22Z
---
# Round 3 (T-1520): Motion verification: assert motion as sampled frames and filmstrips, a c
## Raw request
> Round 3 (T-1520): Motion verification: assert motion as sampled frames and filmstrips, a choreography diff with measured easing, a frame-time budget, an afterglow lint, motion regressions as eval cases, a sound-off motion diff in review, a motion X-ray overlay and score extraction from a recording (b158 c174 c113 c178 c117 c182 c179 b101 c100). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Motion verification: assert motion as sampled frames and filmstrips, a choreography diff with measured easing, a frame-time budget, an afterglow lint, motion regressions as eval cases, a sound-off motion diff in review, a motion X-ray overlay and score extraction from a recording (b158 c174 c113 c178 c117 c182 c179 b101 c100). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampled frames match the score within tolerance; a changed timing shows in the motion diff; the afterglow lint flags a state change with no trace — verify with `cd plugin/tests && python3 -m unittest test_motion_verify`
## Non-goals
## Approach (options → choice → why)
Options: video analysis (a dependency); chosen: sampled frames from fm smoke's frozen-time profile (T-1509) asserted against the Motion Score, a choreography diff of measured timings before/after, a frame-time budget from performance marks, an afterglow lint over CSS, motion regressions saved as eval cases, and a text motion diff in reviews.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] sampled frames and the diff
3. [ ] frame budget and afterglow lint
4. [ ] regressions as evals
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:44Z created
- 2026-10-22T17:58:00Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmsmoke.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_motion_verify.py', 'CHANGELOG.md']
- 2026-10-22T20:59:22Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1527
## Follow-ups captured
