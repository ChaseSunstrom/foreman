---
id: T-1633
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/skills/playbooks/references/ui/templates/scene.html, MASTER.md]
depends_on: []
source: user
created: 2026-10-22T20:57:29Z
updated: 2026-10-22T22:25:37Z
base: ca53a87d916e87a67bef2eea11c77ebfadb56e45
base_tree: dd88c694b653529bc854e2f92c8a508d6394de87
plan0_at: 2026-10-22T21:56:19Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, CHANGELOG.md]
verified: strong
---
# scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html
## Raw request
> scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html
## Interpretation
scene.json describes a 3D scene once: camera, lights, meshes (box, sphere, plane, or vertices), materials (colour, roughness, emissive) and named animations. plugin/lib/fmscene.py validates it and fm scene compile --to three emits an ES module that builds the scene with three.js, modelled on templates/scene.html (context loss, DPR cap, reduced motion). The scene-3d playbook names the verb.
## Assumptions (confidence)
## Acceptance criteria
- [x] a scene with camera, light, mesh and material compiles to a module holding the same camera values — verify with `python3 plugin/tests/run.py test_scene.Three`
## Non-goals
## Approach (options → choice → why)
Options: hand-written three.js per scene (repeats the survival code); glTF as the source (verbose, binary buffers); a small JSON schema compiled to code. Choice: the small schema: diffable, validated, and the same file can later feed the rasteriser (T-1635) and the component (T-1634).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] schema and validation
3. [x] string emitter
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene` → ✗ exit 1 · Ran 7 tests in 1.5s (2 classes, 16 at a time; slowest: Three 0s, Schema 0s) / FAILED (2 classes) [ran] [tree a2faf30f67d9] (2026-10-22T22:06:37Z)
- (step 2) `python3 plugin/tests/run.py test_scene.Schema` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Schema 0s) / OK [ran] [tree 34727995b36f] (2026-10-22T22:08:43Z)
- (step 3) `python3 plugin/tests/run.py test_scene.Three` → exit 0 · Ran 4 tests in 1.9s (1 classes, 16 at a time; slowest: Three 1s) / OK [ran] [tree 34727995b36f] (2026-10-22T22:08:46Z)
- (step 1) `python3 plugin/tests/run.py test_scene` → ✗ exit 1 · Ran 9 tests in 0.8s (2 classes, 16 at a time; slowest: Three 1s, Schema 0s) / FAILED (2 classes) [ran] [tree 8ecad0a92d44] (2026-10-22T22:16:42Z)
- (step 2) `python3 plugin/tests/run.py test_scene.Schema` → exit 0 · Ran 4 tests in 0.3s (1 classes, 16 at a time; slowest: Schema 0s) / OK [ran] [tree 0627d80a9a40] (2026-10-22T22:18:09Z)
- (step 3) `python3 plugin/tests/run.py test_scene.Three` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: Three 1s) / OK [ran] [tree 0627d80a9a40] (2026-10-22T22:18:11Z)
- (ac 1) `python3 plugin/tests/run.py test_scene.Three` → exit 0 · Ran 5 tests in 0.8s (1 classes, 16 at a time; slowest: Three 1s) / OK [ran] [tree b70f38fa5e28] (2026-10-22T22:23:43Z)
- (step 3) `python3 plugin/tests/run.py test_scene test_help test_playbook_check` → exit 0 · Ran 45 tests in 2.6s (13 classes, 16 at a time; slowest: Snippets 2s, Repo 2s, Help 1s) / OK [ran] [tree b70f38fa5e28] (2026-10-22T22:23:46Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1633-review.md)` → no free-form strings reach SCENE (colours, names, enums); JSON escapes non-ASCII; output asserted free of </ and non-ASCII; --out refuses a symlink to the source [tree b70f38fa5e28] (2026-10-22T22:23:47Z)
- (audit edge) `review edge lens` → schema states rotation order, T*R*S, camera up and forward, sphere segments, light decay, smooth vs flat; a straight-up or -down camera refused [tree b70f38fa5e28] (2026-10-22T22:23:47Z)
- (audit operator) `fm scene compile run through tests and node against a stubbed three.js` → remount after dispose uses a fresh canvas; fail() frees everything once [tree b70f38fa5e28] (2026-10-22T22:23:48Z)
- (audit maintainer) `templates/scene.html got the same IntersectionObserver fix; --to kept for T-1634` → clean [tree b70f38fa5e28] (2026-10-22T22:23:48Z)
- (audit intent) `criterion: camera, light, mesh and material compile to a module holding the same camera values` → met [tree b70f38fa5e28] (2026-10-22T22:23:48Z)
- (step 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 9 tests in 1.6s (2 classes, 16 at a time; slowest: Three 1s, Schema 0s) / OK [ran] [tree b70f38fa5e28] (2026-10-22T22:24:16Z)
- (ac 1) `python3 plugin/tests/run.py test_scene.Three` → exit 0 · Ran 5 tests in 1.5s (1 classes, 16 at a time; slowest: Three 1s) / OK [ran] [tree b70f38fa5e28] (2026-10-22T22:24:18Z)
- (audit adversary) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → scene data can't become code [tree b70f38fa5e28] (2026-10-22T22:24:18Z)
- (audit edge) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → conventions written down for a second renderer [tree b70f38fa5e28] (2026-10-22T22:24:18Z)
- (audit intent) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → met [tree b70f38fa5e28] (2026-10-22T22:24:18Z)
## Log
- 2026-10-22T20:57:29Z created
- 2026-10-22T20:57:31Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md']
- 2026-10-22T20:57:32Z split from T-1528 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:53Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_scene.Three`
- 2026-10-22T21:30:16Z criterion 1 text: a scene with camera, light, mesh and material compiles to a module holding the same camera values — verify with python3 plugin/tests/run.py test_scene.Three → a scene with camera, light, mesh and material compiles to a module holding the same camera values
- 2026-10-22T21:55:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1633.builder.md
- 2026-10-22T21:56:19Z focused
- 2026-10-22T22:07:54Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-22T22:07:55Z scope: + scene-3d.md, the interpretation says the playbook names the verb
- 2026-10-22T22:17:50Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md', 'plugin/skills/playbooks/references/ui/templates/scene.html', 'MASTER.md']
- 2026-10-22T22:17:51Z steer: review nits — schema conventions, vertical camera refused, fresh canvas per mount, fail() frees, IntersectionObserver reads the latest entry (template too), MASTER.md fmscene entry; scope + scene.html, MASTER.md
- 2026-10-22T22:23:33Z merged worktree-agent-ae3a1da88ddd9cde5 (7 file(s))
- 2026-10-22T22:23:33Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae3a1da88ddd9cde5
- 2026-10-22T22:23:34Z focused
- 2026-10-22T22:23:49Z scope: MASTER.md fmscene entry, the scene-3d playbook (one sentence), templates/scene.html (observer fix), fmcli registration
- 2026-10-22T22:25:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook 3D on the web: a designed scene that never breaks the page (skills/playbooks/references/ui/scene-3d.md)
- T-1528 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js,
- T-1634 [FEATURE S, planned, 2 steps] fm scene compile --to component: an <fm-scene> web component sharing the camera and materials
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/skills/playbooks/references/ui/templates/scene.html, plugin/tests/test_s…; re-ground the plan against them before editing
## Why not caught
only one renderer existed when the schema was written
## Lessons
- A scene format meant for two renderers must state its conventions (rotation order, handedness, up, segment counts) in the schema, or the second renderer guesses
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmscene.py
- plugin/lib/fmcli.py
- plugin/skills/playbooks/references/ui/scene-3d.md
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/templates/scene.html
- MASTER.md
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdesign.py
- plugin/lib/fmlanes.py
- plugin/lib/fmmotion.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/verify/verification-loop.md
- plugin/tests/test_lanes.py
- plugin/tests/test_motion_score.py
- plugin/tests/test_playbook_machinery.py
