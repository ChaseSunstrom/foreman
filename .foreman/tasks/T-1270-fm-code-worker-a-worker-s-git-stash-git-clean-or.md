---
id: T-1270
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: [T-1271]
source: discovered
created: 2026-10-20T14:15:27Z
updated: 2026-10-20T17:37:30Z
base: dcce07f0c24bf76471cbc2a7a714f7c0a3912ddc
base_tree: fcdd4f34a84c19724d782aa745f37cc36ea1b2d7
plan0_at: 2026-10-20T17:34:09Z
plan0_scope: []
verified: strong
---
# fm code --worker: the user's own uncommitted work that a worker turn deletes, stashes or cleans away is put back and reported
## Raw request
> fm code --worker: a worker's git stash, git clean or deletion of the user's own uncommitted work isn't undone; refuse a dirty tree at start, or put back pre-existing dirty files a turn deleted
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a file that was modified or untracked before a worker turn and is gone or back at HEAD's content after it (git stash, git clean, rm) is restored from the turn's snapshot and reported; the worker's own edits to such files stay — verify with `python3 plugin/tests/run.py test_code_worker`
## Non-goals
## Approach (options → choice → why)
Options: (a) after each turn, a pre-turn dirty file now missing, or now equal to HEAD while it differed before, gets its snapshot bytes back (a worker's real edit leaves different bytes, so it stays); (b) refuse --worker on a dirty tree (safe, but most trees have some untracked file); (c) stash the user's work before the turn and pop it after (conflicts with the worker's edits). Choice: (a); the snapshot already holds those bytes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a worker that runs git stash -u, and one that deletes an untracked notes file, while fixing calc.py
2. [x] Restore vanished pre-turn changes in Run.judge; docs
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_worker.Worker.test_the_users_own_uncommitted_work_survives_a_stash_or_a_delete` → ✗ exit 1 · Ran 1 test in 1.116s / FAILED (failures=1) [ran] [tree e581386a10b5] (2026-10-20T17:34:10Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 22 tests in 44.4s (1 classes, 16 at a time; slowest: Worker 44s) / OK [ran] [tree b40ecbb1b085] (2026-10-20T17:35:12Z)
- `cd plugin/tests && python3 -m unittest test_code_worker.Worker.test_the_users_own_uncommitted_work_survives_a_stash_or_a_delete` → ✗ exit 1 · Ran 1 test in 2.502s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 682f2b24bb4e] (2026-10-20T17:35:26Z)
- `cd plugin/tests && python3 -m unittest test_code_worker.Worker.test_the_users_own_uncommitted_work_survives_a_stash_or_a_delete` → exit 0 · Ran 1 test in 1.969s / OK [ran] [tree 682f2b24bb4e] (2026-10-20T17:35:26Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 22 tests in 45.6s (1 classes, 16 at a time; slowest: Worker 45s) / OK [ran] [tree 682f2b24bb4e] (2026-10-20T17:36:13Z)
- (audit intent) `self review against the T-1214 review's note; the snapshot already held the bytes, so the fix only decides when to use them` → a worker CLI must never cost the user their in-progress work, whatever git command it runs [tree 682f2b24bb4e] (2026-10-20T17:36:13Z)
- (audit edge) `self review against the T-1214 review's note; the snapshot already held the bytes, so the fix only decides when to use them` → a worker's real edit to a dirty file leaves bytes that are neither HEAD's nor missing, so it stays; a dirty file the worker deletes comes back; a link or folder isn't judged this way; the stash entry itself is left in git's stash list [tree 682f2b24bb4e] (2026-10-20T17:36:13Z)
- (audit self) `self review against the T-1214 review's note; the snapshot already held the bytes, so the fix only decides when to use them` → no findings [tree 682f2b24bb4e] (2026-10-20T17:36:13Z)
## Log
- 2026-10-20T14:15:27Z created
- 2026-10-20T17:25:54Z planned from capture
- 2026-10-20T17:34:08Z focused
- 2026-10-20T17:37:29Z done
- 2026-10-20T17:37:30Z committed 9ba71e01 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1214-review: Verdict: changes needed.** The judge works for the tested cases, but several simple moves get past it. [stale: site/pages.py changed since it was…
- T-1271 [SECURITY S, done, 2 steps] fm code --worker --verify: the worker can't change the files the user's verify names; such edits are put back and reported — lesson: P…
- T-0884 [FEATURE M, done, 3 steps] Snapshot uncommitted work before a Bash command discards it (git reset --hard, checkout -- — lesson: A hook that does real work before …
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 2–3 steps
## Why not caught
the judge compared files against the guard's refusals only; deleting or reverting a user's own file is allowed to the guard
## Lessons
- Judging a worker's diff needs the user's side too: what it removes can matter more than what it writes
## Plan gaps
- failed first: step 1 Failing test: a worker that runs git stash -u, and one that deletes an untracked notes file, while …
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- CHANGELOG.md
