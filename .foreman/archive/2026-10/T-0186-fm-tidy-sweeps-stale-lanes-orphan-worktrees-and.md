---
id: T-0186
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtidy.py,plugin/lib/fmlanes.py,plugin/tests/test_lanes.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T19:12:03Z
updated: 2026-10-03T19:41:54Z
base: ba9e34ff3e2ca4c92e49db82092b8831274de154
base_tree: 58df7cf362ea2ff1b9cc998bb7400f2d887b870f
verified: strong
---
# fm tidy sweeps stale lanes: a closed task's lane and merged foreman/T-* branches no lane holds
## Raw request
> fm tidy sweeps stale lanes: orphan worktrees and merged foreman/T-* branches — brainstorm round 4, value 2
## Interpretation
Lanes (fm lane new, fm run's parallel sessions) leave a worktree and a foreman/T-* branch behind when their task closes; nothing removes them unless someone runs fm lane rm. fm tidy should list them and, with --apply, remove what is safe to remove.
## Assumptions (confidence)
## Acceptance criteria
- [x] tidy lists and removes a closed task's clean lane and a merged lane branch; keeps a dirty lane — verify with `python3 plugin/tests/run.py -k test_tidy_sweeps_stale_lanes`
## Non-goals
## Approach (options → choice → why)
A (chosen): fm tidy finds lanes whose task is closed and merged foreman/T-* branches no worktree holds; --apply removes each lane through fm lane rm's own removal (refuses uncommitted or ignored files, keeps an unmerged branch) and deletes merged branches with git branch -d (refuses unmerged). B (rejected): a separate fm lane prune — tidy already is the cleanup command with a dry run and an apply step.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] fmlanes.remove factored out; tidy's lane check
3. [x] gates, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (lanes: tidy)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_tidy_sweeps_stale_lanes` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Lanes 1s) / FAILED (1 classes) [ran] [tree d6aebfadf83b] (2026-10-03T19:39:57Z)
- (step 2) `python3 plugin/tests/run.py -k test_tidy_sweeps_stale_lanes` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 6b638de8f2ff] (2026-10-03T19:40:10Z)
- (step 2) `python3 plugin/tests/run.py -k test_tidy_sweeps_stale_lanes` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 8fc838ecd1e1] (2026-10-03T19:40:29Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.9    44.2     150  [0] / SessionEnd                  38.1    41.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 8fc838ecd1e1] (2026-10-03T19:41:42Z)
- (ac 1) `python3 plugin/tests/run.py -k test_tidy_sweeps_stale_lanes` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 8fc838ecd1e1] (2026-10-03T19:41:54Z)
- (audit intent) `self: the test (a done task's clean lane removed, a dropped task's dirty lane kept, the unmerged branch kept until merged, then deleted); fm lane rm's tests still pass through the factored remove` → lanes and branches no longer pile up after fm run's parallel sessions; tidy's dry run names each one first [tree 8fc838ecd1e1] (2026-10-03T19:41:54Z)
- (audit adversary) `self: the test (a done task's clean lane removed, a dropped task's dirty lane kept, the unmerged branch kept until merged, then deleted); fm lane rm's tests still pass through the factored remove` → nothing is lost on --apply: a lane with uncommitted or ignored files is a DECIDE item, git branch -d refuses an unmerged branch, a branch any worktree has checked out is skipped, and only foreman/T-* branches are considered [tree 8fc838ecd1e1] (2026-10-03T19:41:54Z)
- (audit edge) `self: the test (a done task's clean lane removed, a dropped task's dirty lane kept, the unmerged branch kept until merged, then deleted); fm lane rm's tests still pass through the factored remove` → a lane folder deleted by hand is pruned; git failing to remove a worktree turns the item into a decision instead of stopping tidy [tree 8fc838ecd1e1] (2026-10-03T19:41:54Z)
## Log
- 2026-10-03T19:12:03Z created
- 2026-10-03T19:39:30Z planned from capture
- 2026-10-03T19:39:30Z focused
- 2026-10-03T19:41:54Z done
- 2026-10-03T19:41:54Z committed 3985e30 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower.
- T-0174 [FIX M, done, 4 steps] Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally — lesson: A cleanup that covers onl…
- T-0134 [FEATURE L, done, 5 steps] Lanes: a git worktree is a lane of its project with its own active task — lesson: When a 'single X per project' rule becomes 'per lane'…
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- similar finished tasks took 4–5 steps
- likely tests for the scope: plugin/tests/test_lanes.py, plugin/tests/test_tidy.py
## Lessons
- Cleanup belongs in the command that already has a dry run: reusing fm lane rm's removal gave tidy the same never-discard rules for free.
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
- MASTER.md
