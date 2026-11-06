---
id: T-0360
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T05:46:11Z
updated: 2026-10-06T05:49:40Z
base: 5c9d7164587175f56c017e23123e01d0e75b8702
base_tree: 80256f58c27430dd80cc91520fc6f8a0e21fd9e6
verified: strong
---
# fm task finish --commit names the other repos a task edited, which it doesn't commit
## Raw request
> fm task finish --commit says 'nothing to commit' when the task's files are in another repo (T-0359: ~/projects/foreman-desktop); commit there, or name the repo it skipped
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a task whose edit is in another git repo: finish --commit names that repo and says not committed — verify with `python3 plugin/tests/run.py -k test_finish_commit_names_edits_in_another_repo`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + fix in _commit_task
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_finish_commit_names_edits_in_another_repo` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: RoundI 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0082f099a802] (2026-10-06T05:47:43Z)
- `python3 plugin/tests/run.py -k test_finish_commit_names_edits_in_another_repo` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: RoundI 0s) / OK [ran] [tree 0082f099a802] (2026-10-06T05:47:43Z)
- (ac 1) `python3 plugin/tests/run.py -k test_finish_commit_names_edits_in_another_repo` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: RoundI 0s) / OK [ran] [tree 023d8f3c3f0e] (2026-10-06T05:49:40Z)
- (step 1) `python3 plugin/tests/run.py -k test_round_i` → exit 0 · Ran 13 tests in 5.1s (1 classes, 16 at a time; slowest: RoundI 5s) / OK [ran] [tree 023d8f3c3f0e] (2026-10-06T05:49:40Z)
- (audit edge) `self: reads the same touched ledger events task_touches does, only the ones outside the project; a path in no git repo is skipped; nothing is committed in the other repo (its own snapshot and secrets check would be needed)` → a file inside the project still commits as before; a non-repo outside path prints nothing; prefix check uses root + '/', so a sibling like /repo-other isn't taken for /repo [tree 023d8f3c3f0e] (2026-10-06T05:49:40Z)
- (audit self) `self: reads the same touched ledger events task_touches does, only the ones outside the project; a path in no git repo is skipped; nothing is committed in the other repo (its own snapshot and secrets check would be needed)` → no findings [tree 023d8f3c3f0e] (2026-10-06T05:49:40Z)
## Log
- 2026-10-06T05:46:11Z created
- 2026-10-06T05:46:46Z planned from capture
- 2026-10-06T05:46:48Z focused
- 2026-10-06T05:49:40Z done
- 2026-10-06T05:49:40Z committed 8819f91 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0268-review-1: Verdict: changes needed.** There are two MEDIUM bugs in repair and one in the scan. I could not run anything because Bash is disabled here, so …
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-0126-review: Verdict:** changes needed. Two gates can be skipped when a covered file changed (renames, and the wrapped-around skip chain). One skipped pass is…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
## Files touched
- plugin/tests/test_round_i.py
- plugin/lib/fmcli.py
- CHANGELOG.md
