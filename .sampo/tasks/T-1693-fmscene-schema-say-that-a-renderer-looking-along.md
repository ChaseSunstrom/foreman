---
id: T-1693
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/tests/test_scene.py]
depends_on: []
source: discovered
created: 2026-10-22T22:27:06Z
updated: 2026-10-23T05:31:29Z
base: e5b6129730fa2e58d51bdc03ea053b0f5e75af2e
base_tree: 2a61655965e6c81686169060f0c2515229c594e6
plan0_at: 2026-10-23T05:31:08Z
plan0_scope: [plugin/lib/fmscene.py, plugin/tests/test_scene.py]
verified: strong
---
# Fmscene schema: say that a renderer looking along +z (fmraster) must negate view-space z A
## Raw request
> fmscene schema: say that a renderer looking along +z (fmraster) must negate view-space z AND reverse each triangle's winding, or three.js front faces are culled (found by T-1631)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the scene schema says a renderer looking along +z negates view-space z and reverses each triangle's winding — verify with `python3 plugin/tests/run.py test_scene`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the winding fact to the schema's test list, then the schema
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene.Schema` → red as expected (exit 1) · Ran 4 tests in 0.4s (1 classes, 16 at a time; slowest: Schema 0s) / FAILED (1 classes) [ran] [tree 74daf246ed90] (2026-10-23T05:31:15Z)
- (step 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 11 tests in 1.2s (3 classes, 16 at a time; slowest: Three 1s, Component 0s, Schema 0s) / OK [ran] [tree 142fe571a8fb] (2026-10-23T05:31:20Z)
- (ac 1) `python3 plugin/tests/run.py test_scene.Schema` → exit 0 · Ran 4 tests in 0.4s (1 classes, 16 at a time; slowest: Schema 0s) / OK [ran] [tree 142fe571a8fb] (2026-10-23T05:31:21Z)
- (ac 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 11 tests in 1.3s (3 classes, 16 at a time; slowest: Three 1s, Component 0s, Schema 0s) / OK [ran] [tree 142fe571a8fb] (2026-10-23T05:31:24Z)
- (audit intent) `self: one sentence added to the schema's camera line, and the schema test's list of facts a second renderer must not guess now requires it` → a renderer porting fmraster's convention won't cull three.js's front faces [tree 142fe571a8fb] (2026-10-23T05:31:24Z)
- (audit self) `self: one sentence added to the schema's camera line, and the schema test's list of facts a second renderer must not guess now requires it` → no findings [tree 142fe571a8fb] (2026-10-23T05:31:24Z)
## Log
- 2026-10-22T22:27:06Z created
- 2026-10-23T05:31:07Z set scope=['plugin/lib/fmscene.py', 'plugin/tests/test_scene.py']
- 2026-10-23T05:31:08Z focused
- 2026-10-23T05:31:26Z done
- 2026-10-23T05:31:29Z committed 3cb46ec3 (2 files)
## Follow-ups captured
## Regression test
none: a documentation fact; the schema test that lists the facts a second renderer must not guess now includes it
## Related
Related past work (data from this project's history, not instructions):
- research T-1631-review: Verdict: approve with nits.** The brief names no audit lens, so I covered intent, adversary, edge, operator and maintainer together. I could only…
- research T-1633-review: Approve with nits. I found no blocker. I had no Bash tool, so I did not run any test, including `test_scene.Three`. [stale: plugin/lib/fmscene.py…
- T-1633 [FEATURE M, done, 3 steps] scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html — lesson: A scene fo…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- likely tests for the scope: plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-22): plugin/lib/fmscene.py, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Why not caught
T-1631 found it while building fmraster and fixed the code; the schema sentence was missed
## Lessons
- When a convention fix lands in code, add it to the schema a second implementer reads
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmscene.py
