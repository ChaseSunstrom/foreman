---
id: T-1689
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/tests/test_motion_verify.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T22:09:09Z
updated: 2026-10-23T09:04:34Z
base: 0aedfab4f03c4c33da9f7ad3a6eea1eeef559645
base_tree: 52398c64d5843cc1b4dfa2b9ed32f7ef7f188709
plan0_at: 2026-10-23T09:03:56Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/tests/test_motion_verify.py, CHANGELOG.md]
verified: strong
---
# Fm design lint afterglow: cover Tailwind hover:/focus: utilities and CSS-in-JS state style
## Raw request
> fm design lint afterglow: cover Tailwind hover:/focus: utilities and CSS-in-JS state styles, and say so in NOT_COVERED (T-1628 review)
## Interpretation
fm design lint's afterglow rule reads CSS state rules only. Read Tailwind state classes too: a state variant (hover, focus, focus-visible, focus-within, active, aria-*, group-/peer-) on a colour, background, opacity or transform utility, on an element whose class list holds no transition-*, duration-* (nonzero: transition-property defaults to all) or animate-* class, is flagged. CSS-in-JS state styles stay unread and NOT_COVERED says so, with @apply (its rule's CSS isn't read here).
## Assumptions (confidence)
## Acceptance criteria
- [x] a Tailwind state class for colour, background, opacity or transform with no transition, nonzero duration or animate class on the same element is an afterglow finding; NOT_COVERED names CSS-in-JS and @apply — verify with `python3 plugin/tests/run.py test_motion_verify`
## Non-goals
## Approach (options → choice → why)
Options: read Tailwind's generated CSS (needs a build); match per element class string (what the lint already reads for gradients and radii); also resolve nested &:hover and styled templates (a CSS-in-JS parser: an M on its own). Choice: per element class string; the CSS-in-JS part is stated in NOT_COVERED, not guessed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then TW_STATE/TW_GLOW/TW_MOVES and afterglow_classes, NOT_COVERED
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_motion_verify` → ✗ exit 1 · Ran 13 tests in 1.1s (2 classes, 16 at a time; slowest: Sample 1s, Afterglow 0s) / FAILED (1 classes) [ran] [tree 08474cc1de13] (2026-10-23T09:03:59Z)
- (step 1) `python3 plugin/tests/run.py test_motion_verify test_design_lint` → exit 0 · Ran 44 tests in 1.1s (7 classes, 16 at a time; slowest: Sample 1s, Allow 1s, Rules 1s) / OK [ran] [tree 6282256d51ab] (2026-10-23T09:04:28Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 13 tests in 1.1s (2 classes, 16 at a time; slowest: Sample 1s, Afterglow 0s) / OK [ran] [tree 6282256d51ab] (2026-10-23T09:04:30Z)
- (audit edge) `self review; the four design suites green; fm design lint over site/ and plugin/templates adds no finding` → text-lg, text-[14px] and focus:underline aren't glow props; transition-none moves nothing; a nonzero duration-* alone counts (transition-property defaults to all); group-hover/aria-[…] states and the allow comment are honoured (test) [tree 6282256d51ab] (2026-10-23T09:04:30Z)
- (audit self) `self review; the four design suites green; fm design lint over site/ and plugin/templates adds no finding` → no findings [tree 6282256d51ab] (2026-10-23T09:04:30Z)
## Log
- 2026-10-22T22:09:09Z created
- 2026-10-23T09:01:05Z set tier=S, scope=['plugin/lib/fmdesign.py', 'plugin/tests/test_motion_verify.py', 'CHANGELOG.md']
- 2026-10-23T09:03:55Z focused
- 2026-10-23T09:04:33Z done
- 2026-10-23T09:04:34Z committed b78ed61b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1628-review: Verdict: approve with nits.** I read the code only and ran no tests; this session had no execution tool. The rule is cheap and its fixtures match…
- T-1628 [FEATURE S, done, 2 steps] Afterglow lint: a state change with no transition, as a rule in fm design lint — lesson: A lint that exits 1 must close its known false…
- research T-1506-review: Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes shoul…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmdesign.py, plugin/tests/test_motion_verify.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 test, then TW_STATE/TW_GLOW/TW_MOVES and afterglow_classes, NOT_COVERED
## Files touched
- plugin/tests/test_motion_verify.py
- CHANGELOG.md
- plugin/lib/fmdesign.py
