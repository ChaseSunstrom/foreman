---
id: T-1685
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-22T21:56:34Z
updated: 2026-10-22T22:00:24Z
base: 8baa1e592bf4c8a2c565c061af2c5a9f5c40efe4
base_tree: e956103ad731986634bd55bc287b989c80e12f11
plan0_at: 2026-10-22T21:56:40Z
plan0_scope: []
verified: strong
---
# fm lane rm discards a lane's own guard script cache (state/guard-scripts.json) instead of refusing
## Raw request
> fm lane rm discards a lane's own guard script cache (state/guard-scripts.json) instead of refusing
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane whose only ignored file is state/guard-scripts.json is removed; any other ignored file still refuses — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] treat the known cache as discardable
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → red as expected (exit 1) · Ran 31 tests in 11.4s (5 classes, 16 at a time; slowest: Lanes 11s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) [ran] [tree da912d384864] (2026-10-22T21:57:24Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | grep -E "^(FAIL|ERROR)|Error|assert" | head -8` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree fabbed528183] (2026-10-22T21:58:17Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 31 tests in 12.3s (5 classes, 16 at a time; slowest: Lanes 12s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 20f0bc958ba2] (2026-10-22T21:59:21Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 31 tests in 11.4s (5 classes, 16 at a time; slowest: Lanes 11s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 20f0bc958ba2] (2026-10-22T21:59:21Z)
- (step 2) `python3 plugin/tests/run.py test_builder test_lanes` → exit 0 · Ran 52 tests in 11.5s (11 classes, 16 at a time; slowest: Lanes 11s, Contract 7s, Brief 3s) / OK [ran] [tree 20f0bc958ba2] (2026-10-22T21:59:40Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 31 tests in 11.4s (5 classes, 16 at a time; slowest: Lanes 11s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 20f0bc958ba2] (2026-10-22T21:59:52Z)
- (audit self) `read the diff; a cache-only folder is walked file by file, symlinked folders never followed, the first non-cache file stops the walk` → an ignored folder with any other file still refuses (tested), so nothing that could be work is discarded [tree 0b7fc7ed1d7b] (2026-10-22T21:59:52Z)
- (audit adversary) `could a lane hide work inside state/ named guard-scripts.json` → only that exact path at a state/ folder is treated as cache; it's a cache the guard rebuilds, and lanes never keep work there [tree 0b7fc7ed1d7b] (2026-10-22T21:59:52Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 31 tests in 11.4s (5 classes, 16 at a time; slowest: Lanes 11s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 0b7fc7ed1d7b] (2026-10-22T22:00:09Z)
- (audit self) `self and adversary review of a 20-line change; red on the start tree, green now` → no findings [tree 0b7fc7ed1d7b] (2026-10-22T22:00:09Z)
## Log
- 2026-10-22T21:56:34Z created
- 2026-10-22T21:56:39Z focused
- 2026-10-22T22:00:22Z done
- 2026-10-22T22:00:24Z committed 58e647f6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0961 [FEATURE M, done, 3 steps] Lanes and internals: the merge base saved before the merge, one _git helper — lesson: When a helper turns exceptions into return codes,…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- decision 2026-10-16: Round 4 skips 'bare fm re-executes the worktree's own copy'
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
## Why not caught
lanes of other repos never get a state/ folder; only Foreman's own lanes do
## Lessons
- When git lists an ignored folder whole, judge what's inside it, not the folder name; otherwise a cache-only folder blocks cleanup
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
