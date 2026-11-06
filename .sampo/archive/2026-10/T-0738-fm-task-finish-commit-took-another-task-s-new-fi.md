---
id: T-0738
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T18:57:17Z
updated: 2026-10-09T18:59:08Z
base: c9686102fdfdd63a170ab91282e868ca0da9f7c6
base_tree: c370a1daa6057c1819630b1f0010b0d5e4d2babd
verified: strong
---
# Fm task finish --commit took another task's new files: with T-0707 focused while T-0706 wa
## Raw request
> fm task finish --commit took another task's new files: with T-0707 focused while T-0706 was checkpointed, T-0706's commit (c968610) included fmgraph.py and test_graph.py, since it commits everything changed since its start snapshot; files the hooks saw another task create or edit after this one's focus should stay out
## Interpretation
fm task finish --commit commits every file changed since the task's start snapshot, so with two tasks interleaved (one checkpointed, another focused) the first to finish takes the other's files; and a commit with nothing left reports a blank failure. Files the hooks saw another task edit, and this one never, stay out of the commit; nothing to commit says so.
## Assumptions (confidence)
## Acceptance criteria
- [x] a file another task edited after this task's focus is left out of this task's commit, and an empty commit says nothing to commit — verify with `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] leave other tasks' files out; say nothing to commit
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: CommitOwnFiles 1s) / OK [ran] [tree 5a55652f3eb6] (2026-10-09T18:57:50Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles` → ✗ exit 1 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: CommitOwnFiles 1s) / FAILED (1 classes) [ran] [tree 4946741a5671] (2026-10-09T18:58:26Z)
- (step 2) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles` → exit 0 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: CommitOwnFiles 1s) / OK [ran] [tree 7a6a64c88833] (2026-10-09T18:58:41Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles` → exit 0 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: CommitOwnFiles 1s) / OK [ran] [tree 7a6a64c88833] (2026-10-09T18:59:06Z)
- (ac 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles` → exit 0 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: CommitOwnFiles 1s) / OK [ran] [tree 7a6a64c88833] (2026-10-09T18:59:08Z)
- (audit self) `self: the filter only drops files another task's touched events name since this task was created and this task never touched; a file both edited stays (unavoidable without hunks); nothing staged now prints nothing to commit; commit-related test files pass` → no findings [tree 7a6a64c88833] (2026-10-09T18:59:08Z)
## Log
- 2026-10-09T18:57:17Z created
- 2026-10-09T18:57:34Z focused
- 2026-10-09T18:57:49Z criterion 1 verify: `python3 plugin/tests/run.py -p test_cli.py -k CommitOwnFiles` → `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles`
- 2026-10-09T18:59:08Z done
- 2026-10-09T18:59:08Z committed 829d7f1 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- T-0192 [FIX S, done, 3 steps] A task's commit includes the files it touched that still differ from HEAD, even when its focus snapshot already held them — lesson: When on…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar finished tasks took 3–3 steps
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
