---
id: T-0742
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T19:57:45Z
updated: 2026-10-09T19:59:18Z
base: 7f0683df38cf7edb54fd48d693c4ed1d64aacbb4
base_tree: 09c9dbb99935e2d63a051e8f67408c11d2969c55
verified: strong
---
# fm task finish --run always runs once as the final check, even when every step already has evidence
## Raw request
> fm task finish --run always runs once as the final check, even when every step already has evidence
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finish whose steps all have evidence still runs --run, and a failing --run stops the close — verify with `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinalRun`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] run --run as the final check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinalRun` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FinalRun 0s) / FAILED (1 classes) [ran] [tree e195a8d42159] (2026-10-09T19:57:51Z)
- (step 2) `python3 plugin/tests/run.py -p test_bookkeeping.py -p test_round_i.py -p test_verification.py -p test_stack.py` → exit 0 · Ran 31 tests in 6.0s (14 classes, 16 at a time; slowest: RoundI 6s, CommitOwnFiles 2s, StepEvidence 2s) / OK [ran] [tree 0082d57555af] (2026-10-09T19:58:09Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinalRun` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FinalRun 0s) / OK [ran] [tree 0082d57555af] (2026-10-09T19:58:10Z)
- (ac 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinalRun` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FinalRun 0s) / OK [ran] [tree 0082d57555af] (2026-10-09T19:59:18Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1180 tests in 63.2s (357 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 0082d57555af] (2026-10-09T19:59:18Z)
- (audit self) `self: --run joins the close's runs when no step or criterion used it; recorded as plain ran evidence; a failure stops the close before audits; the full suite ran as this close's own final check` → no findings [tree 0082d57555af] (2026-10-09T19:59:18Z)
## Log
- 2026-10-09T19:57:45Z created
- 2026-10-09T19:57:45Z focused
- 2026-10-09T19:59:18Z done
- 2026-10-09T19:59:18Z committed 5a60245 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- T-0142 [FIX S, done, 1 steps] fm task finish closes a step that already has evidence, and names what still needs --run — lesson: Name the thing in an error: 'a step or c…
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Why not caught
none: found by its own nudge on T-0741, the first close after T-0686
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
