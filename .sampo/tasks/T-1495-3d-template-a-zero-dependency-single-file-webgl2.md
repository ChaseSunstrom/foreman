---
id: T-1495
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/templates/scene.html, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:12Z
updated: 2026-10-22T18:05:40Z
base: 8ecf37422b929ce3b81bbd31c7a068e4ade2f9aa
base_tree: b05087f2ccf70dac56d04f9047b2314cbc5e1683
plan0_at: 2026-10-22T17:54:42Z
plan0_scope: [plugin/skills/playbooks/references/ui/templates/scene.html]
verified: strong
---
# 3D template: a zero-dependency single-file WebGL2 scene
## Raw request
> 3D template: a zero-dependency single-file WebGL2 scene
## Interpretation
Brainstorm T-1479 cluster 3: a starting point that already honours the 3D survival contract: one HTML file, raw WebGL2, no CDN: a lit procedural mesh, DPR capped at 2, resize, webglcontextlost/restored, reduced motion stops the clock, a poster and text twin when WebGL2 is missing, and a frame-time readout behind a flag. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] the template holds every survival-contract hook and loads no external script — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/templates/scene.html').read(); miss=[s for s in ['webglcontextlost','webglcontextrestored','prefers-reduced-motion','devicePixelRatio','getContext(\"webgl2\"','aria-label',] if s not in t]; assert not miss, miss" && ! grep -q '<script src=' plugin/skills/playbooks/references/ui/templates/scene.html`
## Non-goals
## Approach (options → choice → why)
Options: three.js from a CDN (a dependency and a network fetch); chosen: raw WebGL2 in about 250 lines, commented as the playbook's sections.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write templates/scene.html
2. [x] open it in a headless browser through fm smoke when one is installed (fm smoke set web file://…; fm smoke run), else say so
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/SKILL.md index
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/templates/scene.html').read(); miss=[s for s in ['webglcontextlost','webglcontextrestored','prefers-reduced-motion','devicePixelRatio','getContext(\"webgl2\"','aria-label',] if s not in t]; assert not miss, miss" && ! grep -q '<script src=' plugin/skills/playbooks/references/ui/templates/scene.html` → exit 0 · (no output) [ran] [tree e9bcba01aed9] (2026-10-22T18:02:06Z)
- (step 2) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe_scene.py plugin/skills/playbooks/references/ui/templates/scene.html /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad >/dev/null; python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/cdp_probe.py /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad` → exit 0 · badshader {"state1": "failed", "tab": null, "label": "A clay pebble with three soft lobes, lit warm from the upper left", "size": [1024, 640], "corners": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [ran] [tree e9bcba01aed9] (2026-10-22T18:02:27Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/templates/scene.html').read(); miss=[s for s in ['webglcontextlost','webglcontextrestored','prefers-reduced-motion','devicePixelRatio','getContext(\"webgl2\"','aria-label'] if s not in t]; assert not miss, miss" && ! grep -q '<script src=' plugin/skills/playbooks/references/ui/templates/scene.html` → exit 0 · (no output) [ran] [tree e63cf3b04914] (2026-10-22T18:04:03Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/templates/scene.html').read(); miss=[s for s in ['webglcontextlost','webglcontextrestored','prefers-reduced-motion','devicePixelRatio','getContext(\"webgl2\"','aria-label'] if s not in t]; assert not miss, miss" && ! grep -q '<script src=' plugin/skills/playbooks/references/ui/templates/scene.html` → exit 0 · (no output) [ran] [tree e63cf3b04914] (2026-10-22T18:04:03Z)
- (step 2) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe_scene.py plugin/skills/playbooks/references/ui/templates/scene.html /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/scene-probe` → exit 0 · badshader {"no probe": "storedState = fig.dataset.state; r.centreAfter = px(c.width >> 1, c.height >> 1);\n  }\n  if (mode === \"dispose\") { window.disposeScene(); await wait(300); r.afterDispose = f [ran] [tree e63cf3b04914] (2026-10-22T18:04:17Z)
- (step 2) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/cdp_probe.py plugin/skills/playbooks/references/ui/templates/scene.html /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/scene-probe` → ✗ exit 1 · ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ / NotADirectoryError: [Errno 20] Not a directory: 'plugin/skills/playbooks/references/ui/templates/scene.html/shot-live.png' [ran] [tree e63cf3b04914] (2026-10-22T18:04:39Z)
- (step 2) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe_scene.py plugin/skills/playbooks/references/ui/templates/scene.html /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/scene-probe >/dev/null && python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/cdp_probe.py /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/scene-probe` → exit 0 · badshader {"state1": "failed", "tab": null, "label": "A clay pebble with three soft lobes, lit warm from the upper left", "size": [1024, 640], "corners": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [ran] [tree e63cf3b04914] (2026-10-22T18:05:20Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/templates/scene.html').read(); miss=[s for s in ['webglcontextlost','webglcontextrestored','prefers-reduced-motion','devicePixelRatio','getContext(\"webgl2\"','aria-label',] if s not in t]; assert not miss, miss" && ! grep -q '<script src=' plugin/skills/playbooks/references/ui/templates/scene.html` → exit 0 · (no output) [ran] [tree e63cf3b04914] (2026-10-22T18:05:35Z)
- (audit intent) `builder wrote it; I re-ran the DevTools survival probe from the main checkout: live (moves, corners exactly the backdrop token, no errors), reduced motion (still), no WebGL2 (poster, not focusable), context lost then restored (poster then scene), broken shader (one error, poster), dispose (context released); looked at the live frame: a lit clay form with warm key, cool fill and rim on a dithered vignette, not a default cube` → a starting point that already meets the 3D survival contract and looks directed [tree e63cf3b04914] (2026-10-22T18:05:35Z)
- (audit edge) `builder wrote it; I re-ran the DevTools survival probe from the main checkout: live (moves, corners exactly the backdrop token, no errors), reduced motion (still), no WebGL2 (poster, not focusable), context lost then restored (poster then scene), broken shader (one error, poster), dispose (context released); looked at the live frame: a lit clay form with warm key, cool fill and rim on a dithered vignette, not a default cube` → the probe sets failIfMajorPerformanceCaveat false so SwiftShader renders, so the software-renderer-gets-poster path was not exercised; a DPR change without a resize isn't picked up [tree e63cf3b04914] (2026-10-22T18:05:35Z)
- (audit maintainer) `builder wrote it; I re-ran the DevTools survival probe from the main checkout: live (moves, corners exactly the backdrop token, no errors), reduced motion (still), no WebGL2 (poster, not focusable), context lost then restored (poster then scene), broken shader (one error, poster), dispose (context released); looked at the live frame: a lit clay form with warm key, cool fill and rim on a dithered vignette, not a default cube` → one file, raw WebGL2, colours from CSS custom properties; scene-3d.md links it [tree e63cf3b04914] (2026-10-22T18:05:35Z)
- (audit operator) `builder wrote it; I re-ran the DevTools survival probe from the main checkout: live (moves, corners exactly the backdrop token, no errors), reduced motion (still), no WebGL2 (poster, not focusable), context lost then restored (poster then scene), broken shader (one error, poster), dispose (context released); looked at the live frame: a lit clay form with warm key, cool fill and rim on a dithered vignette, not a default cube` → indexed in the playbooks skill [tree e63cf3b04914] (2026-10-22T18:05:35Z)
## Log
- 2026-10-22T17:36:12Z created
- 2026-10-22T17:54:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1495.builder.md
- 2026-10-22T17:54:42Z focused
- 2026-10-22T18:01:59Z set scope=['plugin/skills/playbooks/references/ui/templates/scene.html plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-22T18:02:02Z set scope=['plugin/skills/playbooks/references/ui/templates/scene.html', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-22T18:03:51Z merged worktree-agent-ad83172857925cc1c (2 file(s))
- 2026-10-22T18:03:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad83172857925cc1c
- 2026-10-22T18:03:52Z focused
- 2026-10-22T18:04:02Z set scope=['plugin/skills/playbooks/references/ui/templates/scene.html', 'plugin/skills/playbooks/references/ui/scene-3d.md', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T18:05:37Z done
- 2026-10-22T18:05:40Z committed f5badffb (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- T-1500 [FEATURE S, planned, 1 steps] UI playbook: visual QA with screenshots and receipts
- T-1493 [FEATURE S, planned, 1 steps] Motion playbook: game feel with intensity caps
- decision 2026-10-22: Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or…
- the similar finished task took 2 steps
## Why not caught
new template
## Lessons
- A probe that can't drive animation frames (dump-dom) passes vacuously; check a probe's output names real states before trusting its exit code.
## Files touched
- plugin/skills/playbooks/references/ui/templates/scene.html
- plugin/skills/playbooks/references/ui/scene-3d.md
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
