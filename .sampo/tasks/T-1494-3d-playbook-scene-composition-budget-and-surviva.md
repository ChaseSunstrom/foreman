---
id: T-1494
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/scene-3d.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:11Z
updated: 2026-10-22T17:46:02Z
base: c2b83287a04a7973fefffd06c2fd87208e16c4c9
base_tree: 9581979fb82d6a9ec7086ac9cd0de23a4f98a8b5
plan0_at: 2026-10-22T17:37:02Z
plan0_scope: [plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# 3D playbook: scene composition, budget and survival contract
## Raw request
> 3D playbook: scene composition, budget and survival contract
## Interpretation
Brainstorm T-1479 cluster 3: web 3D that looks designed and never breaks the page: composition (subject, camera, lens, framing), light and material recipes, a perf budget (draw calls, triangles, texture memory, DPR cap, 60 fps on a mid laptop), the survival contract (webglcontextlost/restored, no GPU, reduced motion, poster fallback, aria label and a text twin), shader looks, and black-screen triage. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/scene-3d.md covers composition, light and material, the budget, the survival contract and black-screen triage — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); miss=[s for s in ['## Composition','## Light and material','## Budget','## Survival contract','webglcontextlost','## Black screen',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
Options: a three.js tutorial (the cards cover the API); chosen: decisions, budgets and failure handling that apply to three.js, R3F or raw WebGL, with a triage table symptom → cause → probe.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/scene-3d.md
2. [x] link web/three-js, web/react-three-fiber, web/postprocessing, games/glsl, games/shader-performance
## Resume here
## Docs impact
CHANGELOG.md line
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); miss=[s for s in ['## Composition','## Light and material','## Budget','## Survival contract','webglcontextlost','## Black screen',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 6324b1d7608f] (2026-10-22T17:40:00Z)
- (step 2) `python3 -c "import subprocess as s; t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); n=['three-js','react-three-fiber','postprocessing','glsl','shader-performance']; miss=[x for x in n if 'fm lib show '+x+'\'' not in t or s.run(['fm','lib','show',x],capture_output=True).returncode]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 6324b1d7608f] (2026-10-22T17:40:01Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); miss=[s for s in ['## Composition','## Light and material','## Budget','## Survival contract','webglcontextlost','## Black screen'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 76a6a54b20d1] (2026-10-22T17:45:46Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); miss=[s for s in ['## Composition','## Light and material','## Budget','## Survival contract','webglcontextlost','## Black screen'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 76a6a54b20d1] (2026-10-22T17:45:47Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); miss=[s for s in ['## Composition','## Light and material','## Budget','## Survival contract','webglcontextlost','## Black screen'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 76a6a54b20d1] (2026-10-22T17:45:47Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/scene-3d.md').read(); miss=[s for s in ['## Composition','## Light and material','## Budget','## Survival contract','webglcontextlost','## Black screen',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 5b3943b1a8d9] (2026-10-22T17:45:58Z)
- (audit intent) `builder wrote it; one fm-reviewer pass verified the mediump 32 s figure, the 4096² texture size, the fit formula, the context-loss flow and failIfMajorPerformanceCaveat; its 3D nits fixed (forceContextLoss, PerformanceMonitor onDecline only, discard wording, isnan WebGL2-only, both FOV defaults, guarded renderer construction, context-cap wording, DESIGN.md and motion.md cross-references)` → web 3D that looks directed and never breaks the page, each rule with a probe [tree 5b3943b1a8d9] (2026-10-22T17:45:58Z)
- (audit edge) `builder wrote it; one fm-reviewer pass verified the mediump 32 s figure, the 4096² texture size, the fit formula, the context-loss flow and failIfMajorPerformanceCaveat; its 3D nits fixed (forceContextLoss, PerformanceMonitor onDecline only, discard wording, isnan WebGL2-only, both FOV defaults, guarded renderer construction, context-cap wording, DESIGN.md and motion.md cross-references)` → the context cap numbers stay approximate and marked as varying; isnan's limits stated [tree 5b3943b1a8d9] (2026-10-22T17:45:58Z)
- (audit maintainer) `builder wrote it; one fm-reviewer pass verified the mediump 32 s figure, the 4096² texture size, the fit formula, the context-loss flow and failIfMajorPerformanceCaveat; its 3D nits fixed (forceContextLoss, PerformanceMonitor onDecline only, discard wording, isnan WebGL2-only, both FOV defaults, guarded renderer construction, context-cap wording, DESIGN.md and motion.md cross-references)` → colours from DESIGN.md, reduced motion from motion.md [tree 5b3943b1a8d9] (2026-10-22T17:45:58Z)
- (audit operator) `builder wrote it; one fm-reviewer pass verified the mediump 32 s figure, the 4096² texture size, the fit formula, the context-loss flow and failIfMajorPerformanceCaveat; its 3D nits fixed (forceContextLoss, PerformanceMonitor onDecline only, discard wording, isnan WebGL2-only, both FOV defaults, guarded renderer construction, context-cap wording, DESIGN.md and motion.md cross-references)` → indexed in the playbooks skill [tree 5b3943b1a8d9] (2026-10-22T17:45:58Z)
## Log
- 2026-10-22T17:36:11Z created
- 2026-10-22T17:36:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1494.builder.md
- 2026-10-22T17:37:02Z focused
- 2026-10-22T17:40:40Z merged worktree-agent-a6d44b40eb065f77c (1 file(s))
- 2026-10-22T17:40:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6d44b40eb065f77c
- 2026-10-22T17:45:29Z focused
- 2026-10-22T17:45:45Z steer: review: forceContextLoss on dispose, PerformanceMonitor onDecline only, discard wording, isnan WebGL2-only, R3F's fov 75 default, renderer construction guarded when getContext is null, context-cap wording, cross-references to DESIGN.md and motion.md
- 2026-10-22T17:45:56Z set scope=['plugin/skills/playbooks/references/ui/scene-3d.md', 'CHANGELOG.md']
- 2026-10-22T17:45:57Z scope: SKILL.md and design-direction.md edits were T-1488's, committed in 329256b6
- 2026-10-22T17:46:00Z done
- 2026-10-22T17:46:02Z committed 49d12b66 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1495 [FEATURE M, planned, 2 steps] 3D template: a zero-dependency single-file WebGL2 scene
- T-1500 [FEATURE S, planned, 1 steps] UI playbook: visual QA with screenshots and receipts
- T-1490 [FEATURE M, planned, 2 steps] UI playbook: composition, depth and states
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Why not caught
new playbook
## Lessons
- API facts from memory in a playbook need a reviewer who checks each one; three of nine were incomplete.
## Files touched
- plugin/skills/playbooks/references/ui/scene-3d.md
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/design-direction.md
- plugin/skills/playbooks/references/ui/motion.md
