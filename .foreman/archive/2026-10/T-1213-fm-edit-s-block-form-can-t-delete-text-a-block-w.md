---
id: T-1213
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T15:19:18Z
updated: 2026-10-16T15:25:43Z
base: 7fa38c9ee33082601c7fb470057aa5b3b1769a5e
base_tree: 5e75611cd048af5effb87ba16628bb1804224870
plan0_at: 2026-10-16T15:23:47Z
plan0_scope: []
verified: strong
---
# fm edit's block form deletes with an empty new text
## Raw request
> fm edit's block form can't delete text: a block whose === line is followed straight by >>> (an empty new text) is counted as incomplete and the whole batch is refused; treat it as replacing the old text with nothing
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a block whose === is followed straight by >>> removes the old text instead of refusing the batch — verify with `python3 plugin/tests/run.py test_batch_edit`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Port the recorded session's fix (BLOCK regex and the empty group) and its test
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_batch_edit` → ✗ exit 1 · Ran 25 tests in 8.9s (4 classes, 16 at a time; slowest: BatchEdit 8s, Sub 2s, Hint 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6e4291270bde] (2026-10-16T15:24:23Z)
- `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 25 tests in 8.6s (4 classes, 16 at a time; slowest: BatchEdit 8s, Sub 2s, Hint 1s) / OK [ran] [tree 6e4291270bde] (2026-10-16T15:24:23Z)
- (step 1) `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 25 tests in 17.2s (4 classes, 16 at a time; slowest: BatchEdit 17s, Sub 4s, Hint 3s) / OK [ran] [tree d156d4ed937a] (2026-10-16T15:24:47Z)
- (ac 1) `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 25 tests in 11.2s (4 classes, 16 at a time; slowest: BatchEdit 11s, Sub 4s, Hint 3s) / OK [ran] [tree d156d4ed937a] (2026-10-16T15:25:00Z)
- (audit self) `self: ported verbatim from the recorded session's commit 2eef1e1; the optional group only matches when === is followed directly by >>>; a non-empty new text parses as before (the other 24 batch-edit tests pass)` → no findings [tree d156d4ed937a] (2026-10-16T15:25:00Z)
## Log
- 2026-10-16T15:19:18Z created
- 2026-10-16T15:19:35Z in progress: the demo recorder is fixing it in a clone of this repo (record-live3); its change gets ported here after the recording, as T-1035's was
- 2026-10-16T15:23:46Z planned from capture
- 2026-10-16T15:23:47Z focused
- 2026-10-16T15:24:47Z scope: CHANGELOG line
- 2026-10-16T15:25:42Z done
- 2026-10-16T15:25:43Z committed 89384049 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- research rsi-20261006b: 1. **Answer.** I found three grounded findings, one for each of your frictions. For friction (1) I traced the code path but did not run a reprodu…
- research T-0384-review: Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each …
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Files touched
- plugin/tests/test_batch_edit.py
- plugin/lib/fmedit.py
- CHANGELOG.md
