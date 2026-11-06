---
id: T-1499
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/looks, plugin/tests/test_library.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:14Z
updated: 2026-10-22T18:55:23Z
base: 1fba8c8e6e77a6abbce2649ef3b5a9a739409178
base_tree: 88cfd767318170525a60548724ba1ebd876bd404
plan0_at: 2026-10-22T18:17:39Z
plan0_scope: [plugin/skills/library/cards/looks, plugin/tests/test_library.py, CHANGELOG.md]
verified: strong
---
# Style shelf: shader looks, light and material recipes, an SVG icon system
## Raw request
> Style shelf: shader looks, light and material recipes, an SVG icon system
## Interpretation
Brainstorm T-1479 cluster 7: eight original shader-look cards (each a GLSL fragment under 60 lines with uniforms, cost and a reduced-motion still: e.g. ink diffusion, contour lines, halftone, soft caustics, grain gradient, aurora bands, dither fade, paper fibre), a light-and-material recipe card (three-point, rim, studio, overcast; PBR presets), and an SVG icon-system card (grid, stroke, corner, optical size rules).
## Assumptions (confidence)
## Acceptance criteria
- [x] the ten cards exist with their fields, and every GLSL block parses as a fragment shader skeleton (void main, precision, gl_FragColor or out vec4) — verify with `cd plugin/tests && python3 -m unittest test_library.ShaderLooks`
## Non-goals
## Approach (options → choice → why)
Options: copy shader snippets from galleries (licences, generic looks); a shader library dependency; chosen: ten original cards in the looks area: eight shader looks (each a GLSL ES 3.00 fragment under 60 lines with its uniforms, cost class and a reduced-motion still), a light-and-material recipe card and an SVG icon-system card; a test parses each GLSL block for a fragment skeleton and, where a headless browser exists, compiles it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] write the cards
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks` → ✗ exit 1 · Ran 5 tests in 0.297s / FAILED (failures=1, errors=2) [ran] [tree c352f795f6b8] (2026-10-22T18:21:53Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks test_library.Looks` → exit 0 · Ran 8 tests in 0.877s / OK [ran] [tree 4523eda914cb] (2026-10-22T18:28:32Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks test_library.Looks` → exit 0 · Ran 8 tests in 0.905s / OK [ran] [tree 7719ab7ee082] (2026-10-22T18:29:04Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks` → ✗ exit 1 · Ran 6 tests in 1.013s / FAILED (failures=2) [ran] [tree 65ba3cbe73cf] (2026-10-22T18:44:25Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks test_library.Looks` → exit 0 · Ran 9 tests in 1.175s / OK [ran] [tree 7a7955771933] (2026-10-22T18:46:22Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks` → exit 0 · Ran 6 tests in 1.952s / OK [ran] [tree 2328580a5f27] (2026-10-22T18:54:05Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_library` → exit 0 · Ran 39 tests in 31.693s / OK [ran] [tree 2328580a5f27] (2026-10-22T18:54:38Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.ShaderLooks` → exit 0 · Ran 6 tests in 1.339s / OK [ran] [tree f4e4da034b8f] (2026-10-22T18:54:55Z)
- (audit intent) `one fm-reviewer pass: 5 MEDIUM + 6 LOW fixed test-first in 54285bef; the new plain-colour pixel test failed on the old halftone (73/255 off) and passes now` → eight shader looks, light-and-material recipes and an SVG icon system as library cards, each shader compiled in a headless browser [tree f4e4da034b8f] (2026-10-22T18:54:55Z)
- (audit adversary) `one fm-reviewer pass: 5 MEDIUM + 6 LOW fixed test-first in 54285bef; the new plain-colour pixel test failed on the old halftone (73/255 off) and passes now` → icon checker refuses DOCTYPE/ENTITY before parsing; browser runs in its own process group and is killed whole on timeout [tree f4e4da034b8f] (2026-10-22T18:54:55Z)
- (audit edge) `one fm-reviewer pass: 5 MEDIUM + 6 LOW fixed test-first in 54285bef; the new plain-colour pixel test failed on the old halftone (73/255 off) and passes now` → integer PCG hash instead of sin-hash at large pixel coordinates; contour width uses the L2 gradient with a floor; 1em and % sizes reported, not crashed [tree f4e4da034b8f] (2026-10-22T18:54:55Z)
- (audit maintainer) `one fm-reviewer pass: 5 MEDIUM + 6 LOW fixed test-first in 54285bef; the new plain-colour pixel test failed on the old halftone (73/255 off) and passes now` → ShaderLooks 6 tests ran (browser present, not skipped); uIntensity=0 checked by pixels, not by name [tree f4e4da034b8f] (2026-10-22T18:54:55Z)
## Log
- 2026-10-22T17:36:14Z created
- 2026-10-22T17:58:59Z set scope=['plugin/skills/library/cards/looks', 'plugin/tests/test_library.py', 'CHANGELOG.md']
- 2026-10-22T18:17:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1499.builder.md
- 2026-10-22T18:17:39Z focused
- 2026-10-22T18:53:36Z merged worktree-agent-a679f97a47499a53c (11 file(s))
- 2026-10-22T18:53:45Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a679f97a47499a53c
- 2026-10-22T18:53:47Z focused
- 2026-10-22T18:55:18Z done
- 2026-10-22T18:55:23Z committed f81c9c3c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook 3D on the web: a designed scene that never breaks the page (skills/playbooks/references/ui/scene-3d.md)
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- T-1498 [FEATURE M, done, 2 steps] Style shelf: twelve original named looks as library cards — lesson: Name taste cards with a prefix (look-) so a single everyday word in…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- similar finished tasks took 2–2 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/skills/library/cards/looks/light-and-material.md, plugin/skills/library/cards/looks/look-archive-ledger.md, plugin/skills/library/cards/looks/look-broadcast-graphics.md, plugin/s…; re-ground the plan against them before editing
## Why not caught
the first tests only checked that uIntensity was declared
## Lessons
- Check a shader's promised neutral state by reading pixels: a uniform that exists isn't a uniform that works (the halftone kept a speck at intensity 0)
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_library.py
- plugin/skills/library/cards/looks/shader-ink-diffusion.md
- plugin/skills/library/cards/looks/shader-contour-lines.md
- plugin/skills/library/cards/looks/shader-halftone.md
- plugin/skills/library/cards/looks/shader-soft-caustics.md
- plugin/skills/library/cards/looks/shader-grain-gradient.md
- plugin/skills/library/cards/looks/shader-aurora-bands.md
- plugin/skills/library/cards/looks/shader-dither-fade.md
- plugin/skills/library/cards/looks/shader-paper-fibre.md
- plugin/skills/library/cards/looks/light-and-material.md
- plugin/skills/library/cards/looks/svg-icon-system.md
- CHANGELOG.md
