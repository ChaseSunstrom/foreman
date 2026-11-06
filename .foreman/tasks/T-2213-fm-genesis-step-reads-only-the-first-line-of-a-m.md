---
id: T-2213
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T20:53:18Z
updated: 2026-10-30T21:18:59Z
base: d9201d3363e53bd67696ee21632fe073679ebb53
base_tree: 48b50a5bb1a727d4fc92aebeee468e470a27b201
plan0_at: 2026-10-30T21:03:27Z
plan0_scope: []
verified: strong
---
# fm genesis step reads only the first line of a Mission's wrapped Task: paragraph, so Mission 3 shows 4 of 8 briefs intaken and asks for a duplicate fm intake
## Raw request
> fm genesis step reads only the first line of a Mission's wrapped Task: paragraph, so Mission 3 shows 4 of 8 briefs intaken and asks for a duplicate fm intake
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a Task: paragraph wrapped over several lines yields every T-id it names — verify with python3 plugin/tests/run.py test_genesis
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: wrapped Task paragraph test; TASKS reads continuation lines
## Resume here
## Docs impact
CHANGELOG line. MASTER unchanged (it doesn't describe the Task: line parse).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisStep.test_a_task_paragraph_wrapped_over_lines_names_every_brief` → red as expected (exit 1) · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GenesisStep 0s) / FAILED (1 classes) [ran] [tree c5c70d5dfbd2] (2026-10-30T21:03:47Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 95 tests in 9.9s (13 classes, 16 at a time; slowest: GenesisCheck 9s, GenesisSweep 7s, GenesisLive 7s) / OK [ran] [tree 5a55c0c5dde9] (2026-10-30T21:04:16Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 95 tests in 10.5s (13 classes, 16 at a time; slowest: GenesisCheck 10s, GenesisSweep 8s, GenesisLive 7s) / OK [ran] [tree 5a55c0c5dde9] (2026-10-30T21:04:27Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep` → ✗ exit 1 · Ran 12 tests in 6.2s (1 classes, 16 at a time; slowest: GenesisStep 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5a55c0c5dde9] (2026-10-30T21:04:43Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep` → exit 0 · Ran 12 tests in 4.6s (1 classes, 16 at a time; slowest: GenesisStep 4s) / OK [ran] [tree 5a55c0c5dde9] (2026-10-30T21:04:43Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 95 tests in 6.2s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree fa62982d6af2] (2026-10-30T21:08:26Z)
- (audit intent) `self-review, S tier: one regex; the test fails on the old parse (intake 1 of 2) and covers a fence right under the paragraph naming its own #T-id` → every T-id a wrapped Task: paragraph names counts as intaken; the live step moved on to Mission 3's critique [tree fa62982d6af2] (2026-10-30T21:08:26Z)
- (audit edge) `self-review, S tier: one regex; the test fails on the old parse (intake 1 of 2) and covers a fence right under the paragraph naming its own #T-id` → continuation stops at a blank line, a heading or a code fence, so an intake block's #T-ids aren't read; a wrapped line starting '#2' still counts [tree fa62982d6af2] (2026-10-30T21:08:26Z)
- (audit self) `self-review, S tier: one regex; the test fails on the old parse (intake 1 of 2) and covers a fence right under the paragraph naming its own #T-id` → no findings [tree fa62982d6af2] (2026-10-30T21:08:26Z)
## Log
- 2026-10-30T20:53:18Z created
- 2026-10-30T21:03:27Z focused
- 2026-10-30T21:04:28Z scope: fmgenesis TASKS regex + its test
- 2026-10-30T21:08:46Z done
- 2026-10-30T21:08:48Z committed f37ac44e (3 files)
- 2026-10-30T21:16:24Z guard authorization added: publish
- 2026-10-30T21:18:59Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2095-review: Verdict:** approve with nits. It meets the criteria as written. One resumability gap and one silent-skip case are worth fixing. I did not run `pl…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: [revisited: defer the full foreman-vs-plain exam] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pendi…
## Why not caught
every test fixture wrote Task: on one line; the real Mission 3 file was the first to wrap
## Lessons
- A field written as one line will wrap once it grows: parse the paragraph, and stop at the next block's own syntax
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
