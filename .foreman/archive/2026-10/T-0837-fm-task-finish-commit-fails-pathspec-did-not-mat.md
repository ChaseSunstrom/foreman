---
id: T-0837
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-14T19:32:23Z
updated: 2026-10-14T19:37:19Z
base: bb3fb4284c89785e5c159f4806a3070ccd3900e6
base_tree: b96d282267fffa4d75e8aeb02c5b5bb7853c3bb3
verified: strong
---
# Fm task finish --commit fails ('pathspec did not match') when a task file was removed with
## Raw request
> fm task finish --commit fails ('pathspec did not match') when a task file was removed with git rm --cached: git add of a path that's neither on disk nor in the index; the staged deletion should just be committed
## Interpretation
fm task finish --commit runs git add -A -- <task files>; a file the task untracked with git rm --cached and deleted is on neither disk nor index, so git add fails the pathspec and the commit never happens (T-0836). Add only paths on disk or in the index; git commit -- <files> already includes the staged deletion.
## Assumptions (confidence)
## Acceptance criteria
- [x] finish --commit commits a task that untracked and deleted a file (git rm --cached, rm) along with its other edits — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then add only paths on disk or in the index
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 10 tests in 1.6s (7 classes, 16 at a time; slowest: CommitOwnFiles 1s, StepEvidence 1s, CommitAfterFocus 1s) / OK [ran] [tree 94f797b54407] (2026-10-14T19:35:31Z)
- `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 10 tests in 1.9s (7 classes, 16 at a time; slowest: CommitOwnFiles 2s, CommitAfterFocus 1s, StepEvidence 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 94f797b54407] (2026-10-14T19:35:35Z)
- `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 10 tests in 1.6s (7 classes, 16 at a time; slowest: CommitOwnFiles 2s, CommitAfterFocus 1s, StepEvidence 1s) / OK [ran] [tree 94f797b54407] (2026-10-14T19:35:35Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.6    35.1     150  [0] / SessionEnd                  30.6    31.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 94f797b54407] (2026-10-14T19:37:11Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 10 tests in 1.6s (7 classes, 16 at a time; slowest: CommitOwnFiles 1s, StepEvidence 1s, CommitAfterFocus 1s) / OK [ran] [tree 94f797b54407] (2026-10-14T19:37:18Z)
- (audit edge) `self: the commit helper adds only paths on disk or in the index; a staged deletion (git rm --cached + rm) is left to git commit -- <files>, which takes it` → a directory path in files counts when any tracked file sits under it; a path on neither side and never tracked is simply not added (git commit -- it would still fail loudly, as before) [tree 94f797b54407] (2026-10-14T19:37:18Z)
- (audit self) `self: the commit helper adds only paths on disk or in the index; a staged deletion (git rm --cached + rm) is left to git commit -- <files>, which takes it` → no findings [tree 94f797b54407] (2026-10-14T19:37:18Z)
## Log
- 2026-10-14T19:32:23Z created
- 2026-10-14T19:34:31Z focused
- 2026-10-14T19:37:18Z done
- 2026-10-14T19:37:19Z committed 99f4dc7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- T-0413 [FIX M, done, 3 steps] Audit diffs leave out secrets — lesson: A frozen copy of the working tree is a second place secrets live: redact at the point it's written,…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Why not caught
none: first task to untrack a file and finish with --commit
## Lessons
- git add and git commit read pathspecs differently: add needs the path in the index or on disk, commit also matches HEAD
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
