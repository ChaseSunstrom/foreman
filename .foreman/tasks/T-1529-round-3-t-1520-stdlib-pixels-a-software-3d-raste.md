---
id: T-1529
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmraster.py, plugin/lib/fmimg.py, plugin/lib/fmcli.py, plugin/tests/test_raster.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:45Z
updated: 2026-10-22T20:59:24Z
---
# Round 3 (T-1520): Stdlib pixels: a software 3D rasteriser for deterministic frames (intege
## Raw request
> Round 3 (T-1520): Stdlib pixels: a software 3D rasteriser for deterministic frames (integer maths for the TUI), fm img (a stdlib PNG codec with pixel diff) and fm view for glTF models in the terminal (c162 a018 a060 a099 b017 c031 c063). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Stdlib pixels: a software 3D rasteriser for deterministic frames (integer maths for the TUI), fm img (a stdlib PNG codec with pixel diff) and fm view for glTF models in the terminal (c162 a018 a060 a099 b017 c031 c063). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] the rasteriser draws a lit cube deterministically (same bytes each run); fm img round-trips a PNG and diffs two; fm view renders a glTF box — verify with `cd plugin/tests && python3 -m unittest test_raster`
## Non-goals
## Approach (options → choice → why)
Options: numpy (a dependency); chosen: a pure-Python rasteriser (integer edge functions, z-buffer, flat and Gouraud shading) good to about 200×100 cells at interactive rates, fm img (PNG encode/decode with zlib, pixel diff), and fm view for glTF meshes in the terminal.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] rasteriser
3. [ ] fm img
4. [ ] fm view
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:45Z created
- 2026-10-22T17:58:06Z set scope=['plugin/lib/fmraster.py', 'plugin/lib/fmimg.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_raster.py', 'CHANGELOG.md']
- 2026-10-22T20:59:24Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1529
## Follow-ups captured
