---
id: T-1545
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_control_room.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:50Z
updated: 2026-10-22T20:59:34Z
---
# Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from
## Raw request
> Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from the settings schema for both surfaces, a mouse-sketched layout, rotary dials with detents, a probe of which key chords the terminal delivers, and a model run as a first-time user of the settings screen (b149 c023 b066 b062 c070). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from the settings schema for both surfaces, a mouse-sketched layout, rotary dials with detents, a probe of which key chords the terminal delivers, and a model run as a first-time user of the settings screen (b149 c023 b066 b062 c070). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm settings serve binds 127.0.0.1 only, refuses a request without its token and writes through fm settings set; the key-chord probe lists what arrives — verify with `cd plugin/tests && python3 -m unittest test_control_room`
## Non-goals
## Approach (options → choice → why)
Options: a full web app framework; chosen: fm settings serve, a loopback-only web page generated from the settings schema for both surfaces (a token on the URL, bound to 127.0.0.1, writes through fm settings set so the guard rules hold), a mouse-sketched layout in the app, rotary dials with detents for numbers, a probe of which key chords the terminal delivers, and a scripted fake-model first-time-user run of the settings screen.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] Control Room page
3. [ ] mouse layout and dials
4. [ ] chord probe and first-time-user run
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:50Z created
- 2026-10-22T18:06:14Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_control_room.py', 'CHANGELOG.md']
- 2026-10-22T20:59:34Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1545
## Follow-ups captured
