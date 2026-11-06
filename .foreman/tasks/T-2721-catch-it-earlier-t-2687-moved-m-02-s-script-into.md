---
id: T-2721
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-02T23:18:52Z
updated: 2026-11-02T23:20:23Z
base: 7157321a2aca1b5b00bd3d128c446871b2501aca
base_tree: e6e91a66d21b28be570710d9fc16e2a6f89ffe41
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-02T23:19:54Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# every kill script in bench/moonshot has its result file beside it with a verdict, held by a test
## Raw request
> T-2720 (M-02's kill result sits beside its script in bench/moonshot (3 of 3 rebuilt, viable)) wasn't caught before it shipped: T-2687 moved M-02's script into bench/ without its output, which lived only in a scratch file's tail
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_moonshot_bench fails for a kill_*.py with no matching *-result.json holding a verdict — verify with `python3 plugin/tests/run.py test_moonshot_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the test
## Resume here
## Docs impact
none: a repo test, no user-facing change
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_moonshot_bench 2>&1 | tail -2` → exit 0 · OK [ran] [tree cf1037024547] [world 2f1906870a] (2026-11-02T23:20:00Z)
- (step 1) `python3 plugin/tests/run.py test_moonshot_bench 2>&1 | tail -2` → exit 0 · OK [ran] [tree cf1037024547] [world 2f1906870a] (2026-11-02T23:20:00Z)
- (step 1) `python3 plugin/tests/run.py test_moonshot_bench` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: MoonshotBench 0s) / OK [ran] [tree cf1037024547] [world 2f1906870a] (2026-11-02T23:20:05Z)
- (ac 1) `python3 plugin/tests/run.py test_moonshot_bench` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:20:05Z [ran] [tree cf1037024547] [world 2f1906870a] (2026-11-02T23:20:06Z)
- (audit edge) `the test names any bench/moonshot kill_*.py whose <id>-result.json is absent or has no viable/not-yet verdict (top level or under 'result'); both shipped scripts (m02, m12) pass; a planted temp folder with one missing result is named` → a result file that isn't JSON, or holds another verdict word, counts as missing [tree cf1037024547] (2026-11-02T23:20:06Z)
- (audit self) `the test names any bench/moonshot kill_*.py whose <id>-result.json is absent or has no viable/not-yet verdict (top level or under 'result'); both shipped scripts (m02, m12) pass; a planted temp folder with one missing result is named` → no findings [tree cf1037024547] (2026-11-02T23:20:06Z)
## Log
- 2026-11-02T23:18:52Z created
- 2026-11-02T23:19:53Z planned from capture
- 2026-11-02T23:19:54Z focused
- 2026-11-02T23:19:54Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-02T23:20:04Z scope: plugin/tests/test_moonshot_bench.py
- 2026-11-02T23:20:20Z done
- 2026-11-02T23:20:23Z committed 46a868c5 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2720 [FIX S, done, 1 steps] M-02's kill result sits beside its script in bench/moonshot (3 of 3 rebuilt, viable)
- T-2679 [RESEARCH M, done, 2 steps] Kill test M-02 (code as a regenerable cache of intent and proofs): rebuild three deleted spec-suite modules from their spec and tests …
- T-2719 [FIX S, dropped, 3 steps] bench/moonshot keeps verdicts only: M-02's result beside its script, the confounded M-12 run removed
- decision 2026-11-02: Recommendation: M-02 is viable at the kill stage (3 of 3 spec-suite modules rebuilt blind passed every test) and moves to its slice: regenerate one …
- similar finished tasks took 1–2 steps
- start here (files T-2720 touched): bench/moonshot/m02-result.json
## Files touched
- plugin/tests/test_moonshot_bench.py
