---
id: T-2603
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T10:54:32Z
updated: 2026-11-02T11:58:46Z
genesis_sweep: 2:mission tasks
base: 6176c50ba5314b6c5ff85305a935127584238894
base_tree: a3445cec02d772da8e84c954d8ca228c36046c70
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T11:02:55Z
plan0_scope: []
verified: strong
---
# The sweep's mission-tasks row counts a deferred task with a revisit date as carried, as the build loop does (T-2541), not as open
## Raw request
> fm genesis sweep 2: ✗ mission tasks: T-2558 deferred; T-2533 deferred; T-2535 deferred
> Done when the rerun's mission tasks line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a gen's mission task deferred with a revisit date passes the mission-tasks row and is named as carried in its good text; one deferred without a revisit, or planned, still fails the row — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test beside the sweep's tests
2. [x] carried branch in the mission-tasks row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisSweep` → ✗ exit 1 · Ran 13 tests in 7.6s (1 classes, 16 at a time; slowest: GenesisSweep 7s) / FAILED (1 classes: test_genesis.GenesisSweep) [ran] [tree 9ec1b156a81d] [world 2f1906870a] (2026-11-02T11:03:12Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 15.4s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 12s) / OK [ran] [tree 869ffe90eb72] [world 2f1906870a] (2026-11-02T11:04:56Z)
- `python3 plugin/tests/run.py test_genesis.GenesisSweep` → ✗ exit 1 · Ran 13 tests in 8.8s (1 classes, 16 at a time; slowest: GenesisSweep 8s) / FAILED (1 classes: test_genesis.GenesisSweep) (start tree + this task's tests) [ran] [tree e58dae26cebd] [world 2f1906870a] (2026-11-02T11:11:53Z)
- `python3 plugin/tests/run.py test_genesis.GenesisSweep` → exit 0 · Ran 13 tests in 7.8s (1 classes, 16 at a time; slowest: GenesisSweep 8s) / OK [ran] [tree e58dae26cebd] [world 2f1906870a] (2026-11-02T11:11:53Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 15.2s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 11s) / OK [ran] [tree e58dae26cebd] [world 2f1906870a] (2026-11-02T11:12:18Z)
- (audit intent) `self-review: the mission-tasks row skips a deferred task with a revisit date and names the carried count; an undated deferral or an open task still fails; full gate green but for the known LeanKind flake (T-2605), which passed on rerun` → a dated deferral passes as carried; an undated one fails with its status (test) [tree e58dae26cebd] (2026-11-02T11:12:18Z)
- (audit edge) `self-review: the mission-tasks row skips a deferred task with a revisit date and names the carried count; an undated deferral or an open task still fails; full gate green but for the known LeanKind flake (T-2605), which passed on rerun` → the meta key is revisit, as T-2541's build loop reads it; a deferral that later loses its date turns red again [tree e58dae26cebd] (2026-11-02T11:12:18Z)
- (audit self) `self-review: the mission-tasks row skips a deferred task with a revisit date and names the carried count; an undated deferral or an open task still fails; full gate green but for the known LeanKind flake (T-2605), which passed on rerun` → no findings [tree e58dae26cebd] (2026-11-02T11:12:18Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 0ec19e39d506] [world 2f1906870a] (2026-11-02T11:58:46Z)
## Log
- 2026-11-02T10:54:32Z created
- 2026-11-02T10:57:15Z planned from capture
- 2026-11-02T11:02:54Z set approved=True
- 2026-11-02T11:02:54Z focused
- 2026-11-02T11:02:55Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T11:12:48Z done
- 2026-11-02T11:12:51Z committed f19090be (3 files)
## Follow-ups captured
## Regression test
The sweep's mission tasks row: every fm genesis sweep reruns it, so this can't come back unseen.
## Related
Related past work (data from this project's history, not instructions):
- T-2541 [FEATURE S, done, 2 steps] fm genesis step carries a Mission task deferred with a revisit date (named, listed for the critique) instead of stalling on 'finish T-N…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-11-02: [costly] Genesis build stage: a deferred Mission task is carried, named, not a blocker
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- similar finished tasks took 2–5 steps
## Lessons
- Two readers of the same state (the build loop and the sweep) must share one rule for it, or the run passes one stage and fails the next on the same task
## Plan gaps
- failed first: step 1 red test beside the sweep's tests
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
