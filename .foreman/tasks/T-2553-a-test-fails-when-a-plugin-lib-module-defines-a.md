---
id: T-2553
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/test_redefinitions.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-11-02T06:08:43Z
updated: 2026-11-02T06:34:28Z
base: 04ef6f9f8935237ea713d95574d26c5ed96b9608
base_tree: 218d72ce945cf09b67832e7c628477b7a7552551
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T06:08:52Z
plan0_scope: [plugin/tests/test_redefinitions.py, CHANGELOG.md]
verified: strong
---
# A test fails when a plugin/lib module silently redefines a top-level name
## Raw request
> A test fails when a plugin/lib module defines a top-level name twice (a def, class or assignment silently replacing an earlier one); twice today a new helper was shadowed by a later def of the same name (_grounded in fmgenesis, _TID in fmrecall)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a module defining a top-level def, class or assignment twice fails the test naming file:line and the first definition; a rebinding that reads the old value (DEFS = {… DEFS …}) passes; today's plugin/lib passes — verify with `python3 plugin/tests/run.py test_redefinitions`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a fixture module with a shadowed def fails the check; the in-place compile rebinding passes
2. [x] test_redefinitions walks plugin/lib/*.py with ast and asserts no silent redefinition
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_redefinitions.Redefinitions.test_a_shadowed_helper_is_caught_and_an_in_place_rebinding_is_not` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Redefinitions 0s) / OK [ran] [tree b919fd43c9c6] [world 2f1906870a] (2026-11-02T06:09:05Z)
- (step 2) `python3 plugin/tests/run.py test_redefinitions` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Redefinitions 1s) / OK [ran] [tree b919fd43c9c6] [world 2f1906870a] (2026-11-02T06:09:13Z)
- (ac 1) `python3 plugin/tests/run.py test_redefinitions` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Redefinitions 1s) / OK [ran] [tree 3d1bbcebcaa0] [world 2f1906870a] (2026-11-02T06:14:57Z)
- (audit edge) `self-review: stdlib ast over plugin/lib top-level defs, classes and plain assignments; a rebinding that reads its old value is allowed (fmfind's DEFS compile); today's tree has none` → an annotated assignment or a conditional def under if isn't counted (top-level body only, plain Assign); a fixture shows a shadowed def caught and the in-place rebinding passing [tree 3d1bbcebcaa0] (2026-11-02T06:14:57Z)
- (audit self) `self-review: stdlib ast over plugin/lib top-level defs, classes and plain assignments; a rebinding that reads its old value is allowed (fmfind's DEFS compile); today's tree has none` → no findings [tree 3d1bbcebcaa0] (2026-11-02T06:14:57Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 6be8ae6fa74c] [world 2f1906870a] (2026-11-02T06:16:29Z)
## Log
- 2026-11-02T06:08:43Z created
- 2026-11-02T06:08:50Z planned from capture
- 2026-11-02T06:08:50Z focused
- 2026-11-02T06:08:52Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T06:09:16Z scope: new plugin/tests/test_redefinitions.py (stdlib ast; no linter is installed and adding one goes through the install queue); CHANGELOG
- 2026-11-02T06:15:12Z done
- 2026-11-02T06:15:14Z committed 1c7e9227 (2 files)
- 2026-11-02T06:16:29Z guard authorization added: publish
- 2026-11-02T06:22:23Z publish grant used by fm ship
- 2026-11-02T06:22:24Z publish grant given back: fm ship's push failed
- 2026-11-02T06:23:26Z guard authorization added: publish
- 2026-11-02T06:34:28Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2547 [FEATURE S, done, 2 steps] fm genesis put refuses a Mission whose intake block has more briefs than grounding lines (a ## Grounding bullet per brief naming the co…
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Lessons
- a stdlib ast test can stand in for a linter rule nobody installed: F811-style redefinition in 30 lines
## Files touched
- plugin/tests/test_redefinitions.py
- CHANGELOG.md
