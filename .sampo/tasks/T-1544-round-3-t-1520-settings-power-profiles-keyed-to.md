---
id: T-1544
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings_power.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:49Z
updated: 2026-10-22T20:59:33Z
---
# Round 3 (T-1520): Settings power: profiles keyed to the terminal (ssh, tmux, TERM, width,
## Raw request
> Round 3 (T-1520): Settings power: profiles keyed to the terminal (ssh, tmux, TERM, width, docked pane) and a phone-over-ssh profile, layouts switched by rule, extension settings schemas, settings as small rules, 'say it in words' config diffs, a config macro, a self-written settings changelog and a distilled minimal patch, two configs side by side or in a duel, a stress replay, a what-breaks simulator, and settings that adapt to repeated undos (b061 b115 b065 b064 c141 c009 a126 a127 b067 b068 c140 b069 c137 c138). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Settings power: profiles keyed to the terminal (ssh, tmux, TERM, width, docked pane) and a phone-over-ssh profile, layouts switched by rule, extension settings schemas, settings as small rules, 'say it in words' config diffs, a config macro, a self-written settings changelog and a distilled minimal patch, two configs side by side or in a duel, a stress replay, a what-breaks simulator, and settings that adapt to repeated undos (b061 b115 b065 b064 c141 c009 a126 a127 b067 b068 c140 b069 c137 c138). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] a profile is picked from the terminal facts; a layout rule switches the layout while verify runs; an extension's settings appear in the screen — verify with `cd plugin/tests && python3 -m unittest test_settings_power`
## Non-goals
## Approach (options → choice → why)
Options: more knobs only; chosen: profiles keyed to the terminal (ssh, tmux, TERM, width, a docked pane) chosen automatically, a phone-over-ssh profile with a soft-key row, layouts switched by rule (show tests while verify runs), extension settings schemas merged into the settings screen, settings as small rules, 'say it in words' config diffs through the model, a config macro, a self-written settings changelog and a distilled patch, two configs side by side or in a duel on the same event stream, a stress replay, a what-breaks simulator on past runs, and settings that adapt to repeated undos (as a suggestion). Profiles and rules also apply to the pane where they make sense.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] profiles
3. [ ] rules and extension schemas
4. [ ] words-to-diff, macro, changelog, duel, replay, simulator
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:49Z created
- 2026-10-22T18:06:12Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_power.py', 'CHANGELOG.md']
- 2026-10-22T20:59:33Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1544
## Follow-ups captured
