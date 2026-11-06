---
id: T-1528
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/templates, plugin/tests/test_scene.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:44Z
updated: 2026-10-22T20:59:23Z
---
# Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js,
## Raw request
> Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js, an <fm-scene> web component and the terminal; one shader subset and one material language for browser, SVG and TUI cells; a reverse import from hand-written three.js (a155 a181 c095 c111 c074 c171). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js, an <fm-scene> web component and the terminal; one shader subset and one material language for browser, SVG and TUI cells; a reverse import from hand-written three.js (a155 a181 c095 c111 c074 c171). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] one scene.json compiles to three.js, the web component and terminal cells with the same camera and materials — verify with `cd plugin/tests && python3 -m unittest test_scene`
## Non-goals
## Approach (options → choice → why)
Options: three.js only; chosen: scene.json (camera, lights, meshes from primitives, materials from a small material language, motion from the score) compiled to a three.js module, an <fm-scene> web component built on the WebGL2 template, and terminal cells via the stdlib rasteriser (T-1529); a reverse import reads simple three.js code into scene.json.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] scene.json schema
3. [ ] compilers
4. [ ] reverse import
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:44Z created
- 2026-10-22T17:58:03Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/templates', 'plugin/tests/test_scene.py', 'CHANGELOG.md']
- 2026-10-22T20:59:23Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1528
## Follow-ups captured
