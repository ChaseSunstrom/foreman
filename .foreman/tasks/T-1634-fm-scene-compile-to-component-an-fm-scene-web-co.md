---
id: T-1634
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/tests/test_scene.py, CHANGELOG.md, plugin/lib/fmcli.py, MASTER.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: [T-1633]
source: user
created: 2026-10-22T20:57:35Z
updated: 2026-10-22T22:57:46Z
base: 967082f672875134c889b591eebd76c7c1784505
base_tree: d80a345cfdc5b174608b9c9c91fb0d7724ce1c3d
plan0_at: 2026-10-22T22:28:18Z
plan0_scope: [plugin/lib/fmscene.py, plugin/tests/test_scene.py, CHANGELOG.md]
verified: strong
---
# fm scene compile --to component: an <fm-scene> web component sharing the camera and materials
## Raw request
> fm scene compile --to component: an <fm-scene> web component sharing the camera and materials
## Interpretation
fm scene compile --to component wraps the three.js output in an <fm-scene> custom element (shadow DOM, the canvas, a slot for the poster fallback), sharing the camera and material values with the module output.
## Assumptions (confidence)
## Acceptance criteria
- [x] the component holds the same camera and material values as the three.js output — verify with `python3 plugin/tests/run.py test_scene.Component`
## Non-goals
## Approach (options → choice → why)
Options: a framework component (React: a dependency); a plain custom element; an iframe. Choice: the custom element: works in any page, no build step, and the poster slot keeps the fallback in the author's hands.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] custom element reusing the three.js body
## Resume here
## Docs impact
plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_scene.Component` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (1.6 s; last 25 of 25 lines) [ran] [tree d45f7a8d2ce0] (2026-10-22T22:31:37Z)
- (step 1) `python3 plugin/tests/run.py test_scene.Component` → ✗ exit 1 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Component 0s) / FAILED (1 classes) [ran] [tree d45f7a8d2ce0] (2026-10-22T22:31:40Z)
- (step 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 11 tests in 5.3s (3 classes, 16 at a time; slowest: Three 4s, Component 1s, Schema 1s) / OK [ran] [tree 9476a36bfdf5] (2026-10-22T22:34:47Z)
- (ac 1) `python3 plugin/tests/run.py test_scene.Component` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (0.5 s; last 31 of 31 lines) [ran] [tree 90d43ca18551] (2026-10-22T22:41:46Z)
- (step 1) `python3 plugin/tests/run.py test_scene.Component` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Component 0s) / FAILED (1 classes) [ran] [tree 90d43ca18551] (2026-10-22T22:41:50Z)
- (step 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 11 tests in 2.2s (3 classes, 16 at a time; slowest: Three 2s, Component 0s, Schema 0s) / OK [ran] [tree 38c7ce2740a8] (2026-10-22T22:42:55Z)
- (ac 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 11 tests in 1.5s (3 classes, 16 at a time; slowest: Three 1s, Component 0s, Schema 0s) / OK [ran] [tree 86e1cd499f02] (2026-10-22T22:55:53Z)
- (step 1) `python3 plugin/tests/run.py test_scene.Component` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Component 0s) / OK [ran] [tree 86e1cd499f02] (2026-10-22T22:56:00Z)
- (ac 1) `python3 plugin/tests/run.py test_scene.Component` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Component 0s) / OK [ran] [tree 86e1cd499f02] (2026-10-22T22:56:02Z)
- (audit intent) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → fm scene compile --to component emits an <fm-scene> web component holding the same camera and material values as the three.js output [tree 86e1cd499f02] (2026-10-22T22:56:02Z)
- (audit edge) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → a declared shadow root without a canvas is filled, not re-attached; removing and re-adding the element gives a fresh canvas; the poster stays until live [tree 86e1cd499f02] (2026-10-22T22:56:02Z)
- (audit maintainer) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → the playbook and module header carry the same CSS rules and rename note; a test checks both [tree 86e1cd499f02] (2026-10-22T22:56:02Z)
- (audit self) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → no findings [tree 86e1cd499f02] (2026-10-22T22:56:02Z)
- (audit intent) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → fm scene compile --to component emits an <fm-scene> web component holding the same camera and material values as the three.js output [tree 86e1cd499f02] (2026-10-22T22:56:55Z)
- (audit adversary) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → the one innerHTML assigns SHADOW, a constant template literal with no interpolation (checked: no ${ in it); the page's label attribute goes through setAttribute, never markup; scene values are emitted through the same json.dumps path as the three.js target [tree 86e1cd499f02] (2026-10-22T22:56:55Z)
- (audit edge) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → a declared shadow root without a canvas is filled, not re-attached; removing and re-adding the element gives a fresh canvas; the poster stays until live [tree 86e1cd499f02] (2026-10-22T22:56:55Z)
- (audit maintainer) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → the playbook and module header carry the same CSS rules and rename note; a test checks both [tree 86e1cd499f02] (2026-10-22T22:56:55Z)
- (audit self) `fm-reviewer full pass on the lane; four review items fixed test-first: pre-definition CSS documented, slotted poster object-fit, a page-declared shadow root reused (stub that throws on a second attachShadow), renaming explained; headless Chromium rerun` → no findings [tree 86e1cd499f02] (2026-10-22T22:56:55Z)
## Log
- 2026-10-22T20:57:35Z created
- 2026-10-22T20:57:36Z set scope=['plugin/lib/fmscene.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md']
- 2026-10-22T20:57:38Z split from T-1528 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:57:39Z set depends_on=['T-1633']
- 2026-10-22T21:29:53Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_scene.Component`
- 2026-10-22T21:30:17Z criterion 1 text: the component holds the same camera and material values as the three.js output — verify with python3 plugin/tests/run.py test_scene.Component → the component holds the same camera and material values as the three.js output
- 2026-10-22T22:28:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1634.builder.md
- 2026-10-22T22:28:17Z focused
- 2026-10-22T22:37:01Z set scope=['plugin/lib/fmscene.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'MASTER.md']
- 2026-10-22T22:37:01Z scope: fmcli.py for the --to choices (component), MASTER.md for the one-line fmscene mention the main thread asked for
- 2026-10-22T22:42:21Z set scope=['plugin/lib/fmscene.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'MASTER.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-22T22:55:38Z merged worktree-agent-a110e87089e1ac111 (6 file(s))
- 2026-10-22T22:55:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a110e87089e1ac111
- 2026-10-22T22:55:42Z focused
- 2026-10-22T22:55:54Z scope: plugin/skills/playbooks/references/ui/scene-3d.md — the playbook documents --to component, pre-definition CSS and renaming (review item)
- 2026-10-22T22:57:46Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1633 [FEATURE M, done, 3 steps] scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html — lesson: A scene fo…
- research T-1633-review: Approve with nits. I found no blocker. I had no Bash tool, so I did not run any test, including `test_scene.Three`.
- playbook 3D on the web: a designed scene that never breaks the page (skills/playbooks/references/ui/scene-3d.md)
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Lessons
- A custom element must use this.shadowRoot ?? attachShadow(): a page can declare the shadow root before the element upgrades
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmscene.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/scene-3d.md
- plugin/skills/playbooks/ratchet.json
