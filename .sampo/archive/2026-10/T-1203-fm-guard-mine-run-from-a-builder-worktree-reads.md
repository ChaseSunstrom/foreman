---
id: T-1203
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:48:41Z
updated: 2026-10-16T15:18:33Z
base: 6d4d43b85bc351e5f30bcfbdf87b2f84fd98ca2e
base_tree: 40d42a6a82ee953edcc4890f03d50a90d2c3a789
plan0_at: 2026-10-16T15:16:20Z
plan0_scope: []
verified: strong
---
# fm guard mine from a linked worktree reads the main checkout's transcripts
## Raw request
> fm guard mine run from a builder worktree reads the worktree's transcript folder and finds nothing; read the main checkout's project folder too (the worktree is under it)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] run from a builder's linked worktree, fm guard mine finds the refusals recorded under the main checkout's project folder (and the worktree's own) — verify with `python3 plugin/tests/run.py test_guard_mine`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a linked worktree of the test repo, mine run from it, transcripts seeded at the main root
2. [x] mine() resolves a linked worktree to its main checkout with fmcore.main_worktree
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_guard_mine` → ✗ exit 1 · Ran 6 tests in 1.3s (1 classes, 16 at a time; slowest: GuardMine 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 09ce73e6f20d] (2026-10-16T15:16:35Z)
- `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 6 tests in 0.9s (1 classes, 16 at a time; slowest: GuardMine 1s) / OK [ran] [tree 09ce73e6f20d] (2026-10-16T15:16:35Z)
- (step 1) `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 6 tests in 1.5s (1 classes, 16 at a time; slowest: GuardMine 1s) / OK [ran] [tree b5f4bb31762a] (2026-10-16T15:16:43Z)
- (step 2) `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 6 tests in 1.7s (1 classes, 16 at a time; slowest: GuardMine 2s) / OK [ran] [tree b5f4bb31762a] (2026-10-16T15:16:45Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 6 tests in 1.8s (1 classes, 16 at a time; slowest: GuardMine 2s) / OK [ran] [tree b5f4bb31762a] (2026-10-16T15:16:48Z)
- (audit self) `self: main_worktree returns None for a main checkout or submodule, so only linked worktrees change; the calls' own cwd still decides which project a session belongs to; reads only` → no findings [tree b5f4bb31762a] (2026-10-16T15:16:48Z)
- `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 6 tests in 0.8s (1 classes, 16 at a time; slowest: GuardMine 1s) / OK [ran] [tree b5f4bb31762a] (2026-10-16T15:17:52Z)
- (audit adversary) `self: main_worktree returns None for a main checkout or submodule, so only linked worktrees change; the calls' own cwd still decides which project a session belongs to; reads only` → a read-only report; it now reads the main project's transcript folder, which the main checkout itself already reads; no verdict or state changes [tree b5f4bb31762a] (2026-10-16T15:17:52Z)
- (audit self) `self: main_worktree returns None for a main checkout or submodule, so only linked worktrees change; the calls' own cwd still decides which project a session belongs to; reads only` → no findings [tree b5f4bb31762a] (2026-10-16T15:17:52Z)
## Log
- 2026-10-16T14:48:41Z created
- 2026-10-16T15:16:19Z planned from capture
- 2026-10-16T15:16:20Z focused
- 2026-10-16T15:16:45Z scope: CHANGELOG line
- 2026-10-16T15:18:32Z done
- 2026-10-16T15:18:33Z committed 7fa38c9e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research T-0296-review-1: Verdict:** approve with nits. I found no HIGH findings. I read the diff and `fmcore`'s `find_project`/`routing` but did not run any tests. [sta…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- the similar finished task took 3 steps
## Files touched
- plugin/tests/test_guard_mine.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
