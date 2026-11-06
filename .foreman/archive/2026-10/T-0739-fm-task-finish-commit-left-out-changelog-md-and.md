---
id: T-0739
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T19:43:53Z
updated: 2026-10-09T19:45:44Z
base: e3d6b64b71aad1a5a36bd30a3be5f9ad8d2c7eb4
base_tree: 32f5e0433dfd3739ebf48552d0a81136ba214a94
verified: strong
---
# Fm task finish --commit left out CHANGELOG.md and MASTER.md from T-0684: the T-0738 filter
## Raw request
> fm task finish --commit left out CHANGELOG.md and MASTER.md from T-0684: the T-0738 filter counts other tasks' edits since this task was created, so T-0683's edits before T-0684 was focused excluded files T-0684 also changed through the shell; use the task's first focus as the cutoff
## Interpretation
The commit filter from T-0738 drops files another task touched since this task was created; a task created long before it is focused (most captured items) then loses files it changed itself through the shell. The cutoff is this task's first focus: only other tasks' edits made while this task was being worked keep a file out.
## Assumptions (confidence)
## Acceptance criteria
- [x] a file another task edited before this task was focused, then changed by this task through the shell, is in this task's commit — verify with `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] cutoff at the first focus
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitAfterFocus` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: CommitAfterFocus 1s) / OK [ran] [tree 44d3296c6ec1] (2026-10-09T19:44:09Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitAfterFocus` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: CommitAfterFocus 1s) / FAILED (1 classes) [ran] [tree 306c7aff5cc4] (2026-10-09T19:45:01Z)
- (step 2) `python3 plugin/tests/run.py -p test_bookkeeping.py -k Commit` → exit 0 · Ran 3 tests in 1.3s (2 classes, 16 at a time; slowest: CommitOwnFiles 1s, CommitAfterFocus 1s) / OK [ran] [tree fc68acdb9e0d] (2026-10-09T19:45:09Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitAfterFocus` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: CommitAfterFocus 1s) / FAILED (1 classes) [ran] [tree fc68acdb9e0d] (2026-10-09T19:45:11Z)
- (step 2) `python3 plugin/tests/run.py -p test_bookkeeping.py -k Commit` → exit 0 · Ran 3 tests in 2.5s (2 classes, 16 at a time; slowest: CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree 5b0075278f6f] (2026-10-09T19:45:33Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitAfterFocus` → exit 0 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: CommitAfterFocus 1s) / OK [ran] [tree 5b0075278f6f] (2026-10-09T19:45:35Z)
- (ac 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k CommitOwnFiles` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: CommitOwnFiles 2s) / OK [ran] [tree 5b0075278f6f] (2026-10-09T19:45:43Z)
- (audit self) `self: the cutoff is the task's first focus, by ledger order (seconds tie), with created as the fallback when its focus left the window; reproduced from the CLI first` → no findings [tree 5b0075278f6f] (2026-10-09T19:45:43Z)
## Log
- 2026-10-09T19:43:53Z created
- 2026-10-09T19:43:58Z focused
- 2026-10-09T19:45:44Z done
- 2026-10-09T19:45:44Z committed bcd1e0d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0738 [FIX S, done, 2 steps] Fm task finish --commit took another task's new files: with T-0707 focused while T-0706 wa
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- research T-0295-review-1: MEDIUM — `~/.claude/foreman/MASTER.md:10`.** It says "the bench judge and soak ... run through `fmideas.run_child`". Nothing in `plug…
- decision 2026-10-06: [revisit: after 2026-12-01] Drop T-0356: keep 'fm task new --focus' and the first edit as separate calls
- similar finished tasks took 2–3 steps
- start here (files T-0738 touched): plugin/tests/test_bookkeeping.py, plugin/lib/fmcli.py
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
