---
id: T-1706
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, plugin/skills/playbooks/references/ui/scene-3d.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T22:40:57Z
updated: 2026-10-23T12:01:42Z
base: 208e7540df1cd5fa3c2486c9ec0b9d10a5ad1e5d
base_tree: 6f06636ccf0d4b2ab4d942610747a2d88c337da1
plan0_at: 2026-10-23T12:00:36Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, plugin/skills/playbooks/references/ui/scene-3d.md, CHANGELOG.md]
verified: strong
---
# Fm scene compile --to component --tag NAME so two scenes can share a page, and an observed
## Raw request
> fm scene compile --to component --tag NAME so two scenes can share a page, and an observed label attribute on <fm-scene> (T-1634 review)
## Interpretation
fm scene compile --to component --tag NAME defines the element under NAME (its module's comments and box rules naming it too), so two scenes can share a page; NAME must be a valid custom element name. And <fm-scene>'s label becomes an observed attribute: changed, it renames the canvas; removed, the canvas hides so the text twin speaks.
## Assumptions (confidence)
## Acceptance criteria
- [x] a tagged component defines that name and refuses an invalid one; label changes reach the canvas — verify with `python3 plugin/tests/run.py test_scene`
## Non-goals
## Approach (options → choice → why)
Options: (1) replace fm-scene in the component's head and element text with the tag, validated against the custom element name grammar (ASCII subset) and the spec's reserved names (chosen: one string, nothing to drift); (2) a page-side define call the user writes (rejected: the T-1634 review asked for the flag); (3) an auto-suffixed name at runtime (rejected: the markup must know the name). label: observedAttributes plus one #label() used by connect and change.
## Risks and rollback
## Execution prompt
## Steps
1. [x] the --tag flag and the watched label, test first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene` → ✗ exit 1 · Ran 12 tests in 0.8s (4 classes, 16 at a time; slowest: Three 1s, Component 0s, Schema 0s) / FAILED (2 classes) [ran] [tree 3776e6ad7efe] (2026-10-23T12:00:39Z)
- (step 1) `python3 plugin/tests/run.py test_scene test_cli test_docs` → exit 0 · Ran 198 tests in 22.9s (54 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 8s) / OK [ran] [tree 64bbe520a430] (2026-10-23T12:01:07Z)
- (ac 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 12 tests in 0.8s (4 classes, 16 at a time; slowest: Three 1s, Component 0s, Tag 0s) / OK [ran] [tree 64bbe520a430] (2026-10-23T12:01:08Z)
- (ac 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 12 tests in 0.8s (4 classes, 16 at a time; slowest: Three 1s, Tag 0s, Component 0s) / OK [ran] [tree 64bbe520a430] (2026-10-23T12:01:16Z)
- (audit edge) `self: the tag replaces fm-scene in the component's head and element text only (the shared runtime is untouched and still embedded whole); the name is checked before any text is built; label handling moved into one #label() used on connect and on change` → an invalid tag (no hyphen, uppercase, digit first, non-ASCII, a quote, </script, a reserved name) is refused with exit 2; --tag without --to component is refused; the default output is byte-identical with tag=fm-scene; a label set before the element is connected changes nothing until connect names it; removing the label hides the canvas so the twin speaks [tree 64bbe520a430] (2026-10-23T12:01:16Z)
- (audit adversary) `self: the tag replaces fm-scene in the component's head and element text only (the shared runtime is untouched and still embedded whole); the name is checked before any text is built; label handling moved into one #label() used on connect and on change` → the tag lands in JS strings and comments, so only [a-z0-9._-] with a letter first pass: no quote, backslash or < can reach the module [tree 64bbe520a430] (2026-10-23T12:01:16Z)
- (audit self) `self: the tag replaces fm-scene in the component's head and element text only (the shared runtime is untouched and still embedded whole); the name is checked before any text is built; label handling moved into one #label() used on connect and on change` → no findings [tree 64bbe520a430] (2026-10-23T12:01:16Z)
## Log
- 2026-10-22T22:40:57Z created
- 2026-10-23T11:39:05Z set tier=S, scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'plugin/skills/playbooks/references/ui/scene-3d.md', 'CHANGELOG.md']
- 2026-10-23T12:00:35Z focused
- 2026-10-23T12:01:40Z done
- 2026-10-23T12:01:42Z committed 1b096483 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1634 [FEATURE S, done, 2 steps] fm scene compile --to component: an <fm-scene> web component sharing the camera and materials — lesson: A custom element must use this.…
- T-1633 [FEATURE M, done, 3 steps] scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html — lesson: A scene fo…
- playbook 3D on the web: a designed scene that never breaks the page (fm playbooks show ui/scene-3d)
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Lessons
- Validate a name that is pasted into generated code against the grammar it must satisfy, so nothing else can reach the text
## Plan gaps
- failed first: step 1 the --tag flag and the watched label, test first
## Files touched
- plugin/tests/test_scene.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/skills/playbooks/references/ui/scene-3d.md
