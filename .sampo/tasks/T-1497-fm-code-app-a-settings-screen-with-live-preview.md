---
id: T-1497
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/commands/settings.md, plugin/tests/test_code_tui.py, plugin/tests/test_settings.py, mods/foreman-ui/hooks, mods/foreman-ui/tests, CHANGELOG.md]
depends_on: [T-1496]
source: followup
created: 2026-10-22T17:36:13Z
updated: 2026-10-22T18:11:54Z
---
# fm code app: a settings screen with live preview
## Raw request
> fm code app: a settings screen with live preview
## Interpretation
Brainstorm T-1479 cluster 6: change themes, layout, keys, motion and models from inside the app: a settings overlay (one key opens it) listing the schema by group, with search, a modified-only view, the current value and default, a takes-effect badge (now / next run), live preview of theme and motion changes behind the overlay, a :set key value line, and revert in 10 s unless kept (any key keeps it). Writes go through the comment-preserving writer.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the overlay lists every setting by group, search narrows it, and changing a theme value repaints the screen behind it — verify with `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen`
- [ ] a change not kept within 10 s reverts in the file and on screen; :set writes one key — verify with `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen.test_revert_and_set_line`
- [ ] /foreman:settings lists both surfaces' settings and sets one through fm settings set; the foreman-ui pane applies a changed motion or palette without a restart — verify with `cd plugin/tests && python3 -m unittest test_settings.PluginSurface`
## Non-goals
## Approach (options → choice → why)
Options: a separate settings app (two UIs); a web control room (out of scope); chosen: one more view in fmcodetui's view stack, reusing _overlay and _list_view, driven by the schema; the preview applies the candidate config to the app's cfg without writing until kept.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] overlay: groups, search, modified-only, badge
3. [ ] live preview and revert timer
4. [ ] :set line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:36:13Z created
- 2026-10-22T17:36:39Z set depends_on=['T-1496']
- 2026-10-22T17:41:39Z steer (user, T-1520): Claude Code plugin parity: a /foreman:settings command (plugin/commands) shows the grouped settings of both surfaces and sets one through fm settings set; the foreman-ui pane picks a changed motion/palette up on its next poll
- 2026-10-22T17:41:40Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/commands/settings.md', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_settings.py', 'mods/foreman-ui/hooks', 'mods/foreman-ui/tests', 'CHANGELOG.md']
- 2026-10-22T18:11:54Z dropped: split into three M tasks (T-1572 overlay, T-1573 preview and revert, T-1574 Claude Code command and pane) so builders can take them
## Follow-ups captured
