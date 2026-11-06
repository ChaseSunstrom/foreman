---
id: T-3004
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T19:11:37Z
updated: 2026-11-04T19:21:37Z
base: 45f1001cc9c44238f13d21bc93963454a352c20d
base_tree: 7fe5b8963f01f42a29f92e556ca1aef4b740a731
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T19:11:43Z
plan0_scope: []
verified: strong
---
# Minted scenarios name the test command in their request, and a no-think jarvis profile for acting: the 27B fixed 0 of 4 because the request never said which tests were red (it chased the UI's vitest in a big repo) and its reasoning used the whole output budget
## Raw request
> Minted scenarios name the test command in their request, and a no-think jarvis profile for acting: the 27B fixed 0 of 4 because the request never said which tests were red (it chased the UI's vitest in a big repo) and its reasoning used the whole output budget
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a minted scenario's request names the test command that went red — verify with `python3 plugin/tests/run.py test_mint`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the request names the command
## Resume here
## Docs impact
none: the request text is internal to minted scenarios; CHANGELOG at the next minting line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mint` → ✗ exit 1 · Ran 17 tests in 5.8s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 5s, MintFromRepo 4s) / FAILED (2 classes: test_mint.MintWithUntrackedDeps, test_mint.MintFromRepo) [ran] [tree 6edc0abd566e] [world 2f1906870a] (2026-11-04T19:13:49Z)
- (step 1) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 127 tests in 205.6s (29 classes, 16 at a time; slowest: LeanKind 205s, ExamAuthors 82s, JudgmentKinds 76s) / OK [ran] [tree c57609df58d8] [world 2f1906870a] (2026-11-04T19:20:46Z)
- `python3 plugin/tests/run.py test_mint` → ✗ exit 1 · Ran 17 tests in 6.4s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 5s, MintFromRepo 3s) / FAILED (2 classes: test_mint.MintWithUntrackedDeps, test_mint.MintFromRepo) (start tree + this task's tests) [ran] [tree c57609df58d8] [world 2f1906870a] (2026-11-04T19:21:13Z)
- `python3 plugin/tests/run.py test_mint` → exit 0 · Ran 17 tests in 5.0s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 5s, MintFromRepo 3s) / OK [ran] [tree c57609df58d8] [world 2f1906870a] (2026-11-04T19:21:13Z)
- (ac 1) `python3 plugin/tests/run.py test_mint` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T19:21:13Z [ran] [tree c57609df58d8] [world 2f1906870a] (2026-11-04T19:21:14Z)
- (audit edge) `diff read: REQUEST names the failing command in key and scenario; the 27B transcripts showed the cause (it chased the UI's vitest in a big repo; reasoning used the whole budget); a jarvis-nothink profile added to the user's models.json for acting` → the command is the one minting proved red, so the request never names a suite that wasn't red [tree c57609df58d8] (2026-11-04T19:21:14Z)
- (audit self) `diff read: REQUEST names the failing command in key and scenario; the 27B transcripts showed the cause (it chased the UI's vitest in a big repo; reasoning used the whole budget); a jarvis-nothink profile added to the user's models.json for acting` → no findings [tree c57609df58d8] (2026-11-04T19:21:14Z)
## Log
- 2026-11-04T19:11:37Z created
- 2026-11-04T19:11:39Z focused
- 2026-11-04T19:11:43Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T19:21:35Z done
- 2026-11-04T19:21:37Z committed 5ef6667e (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-smithbench-gpu: `fm code bench --model PROFILE --seed-timeout 600` on an RTX 5070 Ti (16 GB) through Ollama 0.40.11, one model at a time,
- T-2978 [FEATURE M, done, 3 steps] Scenario minting in real repos: plant one defect by mutation in a Sampo project's real… — lesson: Minting from a real project is gated …
- research T-2978-minting: `sampo exam gen --from-repo PATH [--only GLOB] [--test-cmd CMD] --n N --seed S`: [stale: plugin/lib/sampo/lake.py changed since it was written]
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- similar past tasks were M: consider --tier M
## Lessons
- Read a failing model's transcript before judging the model: two of four 27B misses were the scenario never naming what was red
## Plan gaps
- failed first: step 1 failing test, then the request names the command
## Files touched
- plugin/tests/test_mint.py
- plugin/lib/sampo/mint.py
- models.json
