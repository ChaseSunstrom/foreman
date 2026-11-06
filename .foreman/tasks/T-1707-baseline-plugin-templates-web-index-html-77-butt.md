---
id: T-1707
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmdesign.py, plugin/tests/test_design_lint.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T22:58:39Z
updated: 2026-10-22T23:02:12Z
base: 677094ca4ed07c1863ec9ed33f356d01728d420e
base_tree: 86e1cd499f0226e40b424167e8ccdd17377bf6a2
plan0_at: 2026-10-22T22:59:38Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/tests/test_design_lint.py, CHANGELOG.md]
verified: strong
---
# fm design lint afterglow: a transition whose duration is a var() token counts as moving
## Raw request
> Baseline: plugin/templates/web/index.html:77 .button:hover changes transform with no transition on .button, so T-1628's afterglow rule in fm design lint fails three test_docs.Fences tests (template self-check, fm new, README fence)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the web template lints clean and a var()-timed transition covers its :hover, while a 0s or none transition still flags — verify with `python3 plugin/tests/run.py test_design_lint test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] treat var() durations as moving
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_motion_verify` → red as expected (exit 1) · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Afterglow 0s) / FAILED (1 classes) [ran] [tree 159f5c21afa3] (2026-10-22T22:59:46Z)
- (step 2) `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 4 tests in 0.2s (1 classes, 16 at a time; slowest: Afterglow 0s) / OK [ran] [tree 9cf46e4cc74e] (2026-10-22T23:01:18Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify test_design_lint test_docs` → exit 0 · Ran 95 tests in 11.4s (19 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 2s, Allow 1s) / OK [ran] [tree 9cf46e4cc74e] (2026-10-22T23:01:30Z)
- (ac 1) `python3 plugin/tests/run.py test_design_lint test_docs` → exit 0 · Ran 91 tests in 11.7s (18 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 4s, Allow 2s) / OK [ran] [tree 9cf46e4cc74e] (2026-10-22T23:01:49Z)
- (audit intent) `self-review of a 15-line rule change; tested against the web template and the looks gallery's 8 findings (7 false, 1 real kept)` → the starter template's var()-timed transition covers its :hover, so test_docs.Fences is green again; a 0s or none transition and a transition on a different element still flag [tree 9cf46e4cc74e] (2026-10-22T23:01:49Z)
- (audit edge) `self-review of a 15-line rule change; tested against the web template and the looks gallery's 8 findings (7 false, 1 real kept)` → an unresolvable var() counts as moving (a 0-valued token slips through; the untokened_duration rule pushes tokens anyway); subsequence matching is selector text, no cascade: .b covers .x .b:hover, .x .b doesn't cover .b:hover [tree 9cf46e4cc74e] (2026-10-22T23:01:49Z)
- (audit self) `self-review of a 15-line rule change; tested against the web template and the looks gallery's 8 findings (7 false, 1 real kept)` → no findings [tree 9cf46e4cc74e] (2026-10-22T23:01:49Z)
- `python3 plugin/tests/run.py test_motion_verify` → ✗ exit 1 · Ran 4 tests in 1.8s (1 classes, 16 at a time; slowest: Afterglow 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9cf46e4cc74e] (2026-10-22T23:02:03Z)
- `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 4 tests in 0.4s (1 classes, 16 at a time; slowest: Afterglow 0s) / OK [ran] [tree 9cf46e4cc74e] (2026-10-22T23:02:03Z)
- (audit intent) `self-review of a 15-line rule change; tested against the web template and the looks gallery's 8 findings (7 false, 1 real kept)` → the starter template's var()-timed transition covers its :hover, so test_docs.Fences is green again; a 0s or none transition and a transition on a different element still flag [tree 9cf46e4cc74e] (2026-10-22T23:02:04Z)
- (audit edge) `self-review of a 15-line rule change; tested against the web template and the looks gallery's 8 findings (7 false, 1 real kept)` → an unresolvable var() counts as moving (a 0-valued token slips through; the untokened_duration rule pushes tokens anyway); subsequence matching is selector text, no cascade: .b covers .x .b:hover, .x .b doesn't cover .b:hover [tree 9cf46e4cc74e] (2026-10-22T23:02:04Z)
- (audit self) `self-review of a 15-line rule change; tested against the web template and the looks gallery's 8 findings (7 false, 1 real kept)` → no findings [tree 9cf46e4cc74e] (2026-10-22T23:02:04Z)
## Log
- 2026-10-22T22:58:39Z created
- 2026-10-22T22:58:57Z planned from capture
- 2026-10-22T22:58:59Z set scope=['plugin/lib/fmdesign.py', 'plugin/tests/test_design_lint.py', 'CHANGELOG.md']
- 2026-10-22T22:59:00Z set priority=urgent
- 2026-10-22T22:59:37Z focused
- 2026-10-22T23:01:18Z scope: plugin/tests/test_motion_verify.py holds the afterglow tests (T-1628), not test_design_lint.py
- 2026-10-22T23:02:09Z done
- 2026-10-22T23:02:12Z committed f4b25c5c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1628-review: Verdict: approve with nits.** I read the code only and ran no tests; this session had no execution tool. The rule is cheap and its fixtures match…
- T-1519 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 24): strict-by-default templates for web, 3D and fm cod — lesson: A check that runs user code in-pro…
- research T-1506-review: Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes shoul…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
## Lessons
- A lint rule that asks for tokens must itself read tokens as valid; test the fix advice against the rule
## Files touched
- plugin/tests/test_motion_verify.py
- plugin/lib/fmdesign.py
- CHANGELOG.md
