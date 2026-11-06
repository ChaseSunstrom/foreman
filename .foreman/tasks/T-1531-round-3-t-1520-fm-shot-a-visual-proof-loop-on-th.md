---
id: T-1531
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmshot.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/lib/fmdoctor.py, plugin/tests/test_shot.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:45Z
updated: 2026-10-22T20:59:24Z
---
# Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames,
## Raw request
> Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames, one poster frame per animated artifact, a fail on fallback fonts, a calibrated noise floor per baseline, a visual-diff verify step, and fm doctor probing headless rendering (a079 a151 c085 c084 c161 a147). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames, one poster frame per animated artifact, a fail on fallback fonts, a calibrated noise floor per baseline, a visual-diff verify step, and fm doctor probing headless rendering (a079 a151 c085 c084 c161 a147). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm shot captures viewports and frames where a browser exists and says why not otherwise; a fallback font fails; a diff under the noise floor passes — verify with `cd plugin/tests && python3 -m unittest test_shot`
## Non-goals
## Approach (options → choice → why)
Options: a new browser stack; chosen: fm shot on the existing smoke harness: shots at given viewports and frames, one poster frame per animated page, a fallback-font failure (document.fonts check), a noise floor per baseline, a visual-diff verify step using fm img, and fm doctor's headless rendering probe.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] fm shot
3. [ ] fonts and noise floor
4. [ ] visual-diff verify and doctor probe
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:45Z created
- 2026-10-22T17:58:12Z set scope=['plugin/lib/fmshot.py', 'plugin/lib/fmcli.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmdoctor.py', 'plugin/tests/test_shot.py', 'CHANGELOG.md']
- 2026-10-22T20:59:24Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1531
## Follow-ups captured
