---
id: T-1616
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T20:54:38Z
updated: 2026-10-23T05:30:50Z
base: fe3648e5f54afd39e103b5219079338c544d95e1
base_tree: 0ef42254285fe7ddb00847741080dff6ad8e7fce
plan0_at: 2026-10-23T05:29:14Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, CHANGELOG.md]
verified: strong
---
# Fmcore _AC_RE and _STEP_RE end in a lazy (.*?) then \s*$, which backtracks quadratically o
## Raw request
> fmcore _AC_RE and _STEP_RE end in a lazy (.*?) then \s*$, which backtracks quadratically on a long line of spaces; every brief parse pays it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a step or criterion line with a 50,000-space run parses in well under a second, with the same groups as before on ordinary lines — verify with `python3 plugin/tests/run.py test_core.BriefLines`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing timing test on a long internal space run
2. [x] lookahead-only patterns, no lazy scan
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.BriefLines` → red as expected (exit 1) · Ran 1 tests in 5.7s (1 classes, 16 at a time; slowest: BriefLines 5s) / FAILED (1 classes) [ran] [tree 336b7508c45f] (2026-10-23T05:29:28Z)
- (step 2) `python3 plugin/tests/run.py test_core test_integrations test_planning test_verify_strength` → ✗ exit 1 · Ran 125 tests in 14.6s (33 classes, 16 at a time; slowest: VerifyStrength 14s, Repeat 10s, CalibrationLedger 5s) / FAILED (1 classes) [ran] [tree d43fa1f45d99] (2026-10-23T05:29:51Z)
- (step 1) `python3 plugin/tests/run.py test_core.BriefLines` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BriefLines 0s) / FAILED (1 classes) [ran] [tree d43fa1f45d99] (2026-10-23T05:29:51Z)
- (ac 1) `python3 plugin/tests/run.py test_core.BriefLines` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BriefLines 0s) / FAILED (1 classes) [ran] [tree d43fa1f45d99] (2026-10-23T05:29:52Z)
- (step 2) `python3 plugin/tests/run.py test_core test_integrations test_planning test_verify_strength` → exit 0 · Ran 125 tests in 14.7s (33 classes, 16 at a time; slowest: VerifyStrength 14s, Repeat 10s, CalibrationLedger 5s) / OK [ran] [tree da1acfbf7769] (2026-10-23T05:30:17Z)
- (step 1) `python3 plugin/tests/run.py test_core.BriefLines` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BriefLines 0s) / OK [ran] [tree da1acfbf7769] (2026-10-23T05:30:18Z)
- (ac 1) `python3 plugin/tests/run.py test_core.BriefLines` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BriefLines 0s) / OK [ran] [tree da1acfbf7769] (2026-10-23T05:30:18Z)
- (ac 1) `python3 plugin/tests/run.py test_core.BriefLines` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BriefLines 0s) / OK [ran] [tree 2a61655965e6] (2026-10-23T05:30:32Z)
- (audit intent) `self: replaced the lazy (.*?) before \s*$ with a text group made of non-space characters and space runs followed by a non-space (the step pattern also refuses a run followed by '<- CURRENT' at the end), lookaheads only so it runs on Pythons without possessive quantifiers; compared groups old vs new on 16 sample lines (0 differences) and ran test_core, test_integrations, test_planning, test_verify_strength` → no brief line can make every brief parse (and so every hook) slow [tree 2a61655965e6] (2026-10-23T05:30:32Z)
- (audit edge) `self: replaced the lazy (.*?) before \s*$ with a text group made of non-space characters and space runs followed by a non-space (the step pattern also refuses a run followed by '<- CURRENT' at the end), lookaheads only so it runs on Pythons without possessive quantifiers; compared groups old vs new on 16 sample lines (0 differences) and ran test_core, test_integrations, test_planning, test_verify_strength` → an empty step text, a marker with two spaces, a marker not at the end, tabs inside text and trailing spaces keep their old groups [tree 2a61655965e6] (2026-10-23T05:30:32Z)
- (audit self) `self: replaced the lazy (.*?) before \s*$ with a text group made of non-space characters and space runs followed by a non-space (the step pattern also refuses a run followed by '<- CURRENT' at the end), lookaheads only so it runs on Pythons without possessive quantifiers; compared groups old vs new on 16 sample lines (0 differences) and ran test_core, test_integrations, test_planning, test_verify_strength` → no findings [tree 2a61655965e6] (2026-10-23T05:30:32Z)
## Log
- 2026-10-22T20:54:38Z created
- 2026-10-23T05:29:13Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_core.py', 'CHANGELOG.md']
- 2026-10-23T05:29:13Z focused
- 2026-10-23T05:30:48Z done
- 2026-10-23T05:30:50Z committed e5b61297 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1551-review: Verdict: changes needed.** There are two ways to crash `fm lsp` with crafted input, and one test that cannot fail. I could not run anything (read…
- T-1676 [FEATURE M, dropped, 0 steps] Capture a follow-up task for the unbuilt desk card and animated SVG charts (b094 a096). Se
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcore.py, plugin/tests/test_core.py; re-ground the plan against them before editing
## Measurements
_STEP_RE on a step line with a 20,000-space internal run: 1.483 s before → under 0.001 s after; 200,000 spaces: 0.0002 s after. _AC_RE, 20,000: 0.833 s → under 0.001 s. 'a ' x 200,000 (alternating): 0.042 s after (linear). Ordinary lines: identical groups on 16 sample lines (old vs new).
## Lessons
- A lazy .*? followed by \s*$ is quadratic on internal whitespace runs: make the text group unable to end in whitespace
## Plan gaps
- failed first: step 2 lookahead-only patterns, no lazy scan
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
