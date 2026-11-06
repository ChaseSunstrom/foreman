---
id: T-2451
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T06:38:56Z
updated: 2026-11-01T06:40:35Z
base: c22061b58df1bf3fe1ad2178d9482c9b69145c1a
base_tree: 96d345cc8aadebc9a72fcdec4e82385b1e4bfcc9
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T06:38:57Z
plan0_scope: []
verified: strong
---
# Scorecard maps #6 to proof and #10 to beyond (Mission 7's own exam kinds were never mapped, so neither capability is graded on them)
## Raw request
> Scorecard maps #6 to proof and #10 to beyond (Mission 7's own exam kinds were never mapped, so neither capability is graded on them)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmgenesis._kinds maps gen-0's #6 text to proof and #10's to beyond, and neither borrows the other's kind — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] KIND_WORDS rows
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis -k test_verifying_maps_to_proof` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes: test_genesis.GenesisDraft) [ran] [tree 6985aac2ec1e] (2026-11-01T06:39:15Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 177 tests in 11.5s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisCheck 9s, GenesisSweep 9s) / OK [ran] [tree 9070660e133c] (2026-11-01T06:39:38Z)
- `python3 plugin/tests/run.py test_genesis -k test_verifying_maps_to_proof` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes: test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree 9070660e133c] (2026-11-01T06:39:48Z)
- `python3 plugin/tests/run.py test_genesis -k test_verifying_maps_to_proof` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / OK [ran] [tree 9070660e133c] (2026-11-01T06:39:48Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 177 tests in 9.6s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 9070660e133c] (2026-11-01T06:39:58Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 177 tests in 9.6s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 9070660e133c] (2026-11-01T06:40:09Z)
- (audit self) `self: red→green; genesis suite 177 OK; fm exam scorecard now lists proof under #6 and beyond under #10; the #6 text's 'proof beyond unit tests' doesn't read as beyond (asserted)` → no findings [tree 9070660e133c] (2026-11-01T06:40:09Z)
## Log
- 2026-11-01T06:38:56Z created
- 2026-11-01T06:38:57Z focused
- 2026-11-01T06:38:57Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T06:39:58Z scope: plugin/lib/fmgenesis.py (KIND_WORDS) and plugin/tests/test_genesis.py (the test)
- 2026-11-01T06:40:33Z done
- 2026-11-01T06:40:35Z committed 2976bb13 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2363 [FEATURE M, done, 3 steps] #12 exam kind lean: planted growth the self-change gate must refuse; the scorecard stops borrowing kinds (Mission 8, #12) — lesson: A m…
- T-2394 [FEATURE M, done, 4 steps] #6/#10 exam kinds (Mission 7): fm exam gains proof and beyond kinds, child-authored, nine per kind with three held out, graded on claim…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
## Lessons
- A new exam kind isn't on the scorecard until KIND_WORDS maps it: check fm exam scorecard after adding one
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
