---
id: T-1540
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmsettings.py, plugin/lib/fmcli.py, .claude-plugin/marketplace.json, plugin/tests/test_design_surfaces.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:48Z
updated: 2026-10-22T20:59:29Z
---
# Round 3 (T-1520): One token file for every surface: DESIGN.md tokens drive the web, the fm
## Raw request
> Round 3 (T-1520): One token file for every surface: DESIGN.md tokens drive the web, the fm code app and the foreman-ui pane; brand assets from DESIGN.md; tokens inferred from hand edits; a token x-ray; the design source projected into Claude-native channels; tokens imported through a Figma MCP behind the guard; the design playbooks also offered as an optional foreman-design plugin (a022 a089 b071 b153 b164 c072 c076 a059). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): One token file for every surface: DESIGN.md tokens drive the web, the fm code app and the foreman-ui pane; brand assets from DESIGN.md; tokens inferred from hand edits; a token x-ray; the design source projected into Claude-native channels; tokens imported through a Figma MCP behind the guard; the design playbooks also offered as an optional foreman-design plugin (a022 a089 b071 b153 b164 c072 c076 a059). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] one DESIGN.md compiles to CSS variables, an fm code app theme and the pane's palette; the foreman-design plugin entry validates — verify with `cd plugin/tests && python3 -m unittest test_design_surfaces`
## Non-goals
## Approach (options → choice → why)
Options: per-surface token files; chosen: DESIGN.md tokens compiled by fm design tokens into CSS variables, the fm code app's theme (tui.toml palette through fm settings) and the foreman-ui pane's options; brand assets (favicon, social card) from DESIGN.md; tokens inferred from hand edits; a token x-ray overlay; a Figma import only through an MCP the user configured, read as data behind the guard; the design playbooks and skills also packaged as an optional foreman-design plugin in the marketplace.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] token compiler to three surfaces
3. [ ] brand assets and inferred tokens
4. [ ] x-ray, Figma-as-data and the foreman-design plugin
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:48Z created
- 2026-10-22T18:06:02Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', '.claude-plugin/marketplace.json', 'plugin/tests/test_design_surfaces.py', 'CHANGELOG.md']
- 2026-10-22T20:59:29Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1540
## Follow-ups captured
