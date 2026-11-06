---
id: T-2219
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T21:30:44Z
updated: 2026-10-30T21:46:23Z
base: e930a8469e25193fe3998ab4904eac7805bda2e4
base_tree: f0d5aac4d6e85bbe7ffb2eac1f981f1c2abba860
plan0_at: 2026-10-30T21:31:13Z
plan0_scope: []
verified: strong
---
# fm exam scorecard's top gap compares a free arm's found count with a session line that answered fewer scenarios (s0-001: finders 30/36 vs a 1-scenario foreman line shown as 1/36), so the gap is an artefact of sample size
## Raw request
> fm exam scorecard's top gap compares a free arm's found count with a session line that answered fewer scenarios (s0-001: finders 30/36 vs a 1-scenario foreman line shown as 1/36), so the gap is an artefact of sample size
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] free_beats compares the two arms only on held-out scenarios both answered, by rate, and names the sample — verify with python3 plugin/tests/run.py test_genesis
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: unequal samples; compare on the shared scenarios
## Resume here
## Docs impact
CHANGELOG line; MASTER's free_beats description still holds (a free arm beating the session on a run).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisSelect.test_a_free_arm_beating_the_session_tops_the_scorecard_and_on_train_the_seed` → red as expected (exit 1) · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisSelect 0s) / FAILED (1 classes) [ran] [tree c37ef4c8e34b] (2026-10-30T21:32:22Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 95 tests in 10.4s (13 classes, 16 at a time; slowest: GenesisCheck 10s, GenesisSweep 8s, GenesisLive 7s) / OK [ran] [tree 1d779b9767e7] (2026-10-30T21:33:28Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 95 tests in 10.7s (13 classes, 16 at a time; slowest: GenesisCheck 10s, GenesisSweep 8s, GenesisLive 7s) / OK [ran] [tree 1d779b9767e7] (2026-10-30T21:33:39Z)
- `python3 plugin/tests/run.py test_genesis.GenesisSelect` → ✗ exit 1 · Ran 8 tests in 3.1s (1 classes, 16 at a time; slowest: GenesisSelect 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1d779b9767e7] (2026-10-30T21:33:45Z)
- `python3 plugin/tests/run.py test_genesis.GenesisSelect` → exit 0 · Ran 8 tests in 1.7s (1 classes, 16 at a time; slowest: GenesisSelect 1s) / OK [ran] [tree 1d779b9767e7] (2026-10-30T21:33:45Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 95 tests in 10.6s (13 classes, 16 at a time; slowest: GenesisCheck 10s, GenesisSweep 8s, GenesisLive 8s) / OK [ran] [tree eac7a6485a5a] (2026-10-30T21:34:08Z)
- (audit intent) `self-review, S tier: one comparison; the s0-001 artefact gone from the live scorecard, s31-006 (equal 18-defect samples) kept` → a top gap is reported only where the free arm and the session answered the same scenarios, with each side's own denominator [tree eac7a6485a5a] (2026-10-30T21:34:08Z)
- (audit edge) `self-review, S tier: one comparison; the s0-001 artefact gone from the live scorecard, s31-006 (equal 18-defect samples) kept` → lines without answered ids compare only on equal keyed counts; a session line that answered fewer scenarios is no gap [tree eac7a6485a5a] (2026-10-30T21:34:08Z)
- (audit self) `self-review, S tier: one comparison; the s0-001 artefact gone from the live scorecard, s31-006 (equal 18-defect samples) kept` → no findings [tree eac7a6485a5a] (2026-10-30T21:34:08Z)
## Log
- 2026-10-30T21:30:44Z created
- 2026-10-30T21:31:12Z focused
- 2026-10-30T21:33:45Z scope: fmgenesis free_beats + test_genesis fixtures
- 2026-10-30T21:34:35Z done
- 2026-10-30T21:34:37Z committed 36a26d0b (3 files)
- 2026-10-30T21:43:46Z guard authorization added: publish
- 2026-10-30T21:46:23Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: [revisited: free arm beats the session arm] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3 plugin/tests/ru…
- T-2184 [FEATURE M, done, 5 steps] Foreman sessions use fm find by default (steer 2026-10-30 #3): the exam shows a Foreman… — lesson: a capability the session never hears…
## Why not caught
the fixtures gave every arm the same keyed count; the live run had a 1-scenario smoke line beside a full finders line
## Lessons
- Compare two arms only on the same sample: a raw count from 36 scenarios against one from 1 is a sampling artefact, not a gap
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
