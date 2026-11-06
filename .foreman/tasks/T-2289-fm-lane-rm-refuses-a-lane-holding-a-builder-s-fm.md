---
id: T-2289
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T07:09:37Z
updated: 2026-10-31T07:12:31Z
base: 1c5e1aee592fb5c5d32e92c0c34e09a392acb503
base_tree: 359a83f4fb3cef06de5b0a304d45c408312e2860
plan0_at: 2026-10-31T07:09:38Z
plan0_scope: []
verified: strong
---
# fm lane rm refuses a lane holding a builder's .fm-scratch/ (T-2259's scratch folder): treat it as throwaway like the guard's script cache
## Raw request
> fm lane rm refuses a lane holding a builder's .fm-scratch/ (T-2259's scratch folder): treat it as throwaway like the guard's script cache
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane rm removes a lane whose only ignored files are under .fm-scratch/, and still refuses one with another ignored file (.env) — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_lanes, then .fm-scratch/ in fmlanes' lane cache pattern
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_lanes` → ✗ exit 1 · Ran 45 tests in 14.552s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree d4a3c6916014] (2026-10-31T07:11:32Z)
- `cd plugin/tests && python3 -m unittest -q test_lanes` → exit 0 · Ran 45 tests in 14.127s / OK [ran] [tree d4a3c6916014] (2026-10-31T07:11:32Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 45 tests in 13.8s (5 classes, 16 at a time; slowest: Lanes 14s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree d4a3c6916014] (2026-10-31T07:11:46Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 45 tests in 13.8s (5 classes, 16 at a time; slowest: Lanes 14s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 299a06608b4d] (2026-10-31T07:12:01Z)
- (audit intent) `self: .fm-scratch/ at the lane root joins the guard's script cache as throwaway; any other ignored file still blocks rm` → T-2259's scratch folder no longer blocks a merged lane's removal (test_lanes red-to-green) [tree 299a06608b4d] (2026-10-31T07:12:01Z)
- (audit edge) `self: .fm-scratch/ at the lane root joins the guard's script cache as throwaway; any other ignored file still blocks rm` → only a root .fm-scratch/ matches; a .env beside it still refuses [tree 299a06608b4d] (2026-10-31T07:12:01Z)
- (audit self) `self: .fm-scratch/ at the lane root joins the guard's script cache as throwaway; any other ignored file still blocks rm` → no findings [tree 299a06608b4d] (2026-10-31T07:12:01Z)
## Log
- 2026-10-31T07:09:37Z created
- 2026-10-31T07:09:37Z focused
- 2026-10-31T07:11:46Z scope: plugin/lib/fmlanes.py (_LANE_CACHE), plugin/tests/test_lanes.py, CHANGELOG.md
- 2026-10-31T07:12:29Z done
- 2026-10-31T07:12:31Z committed b358c171 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1685 [FIX S, done, 2 steps] fm lane rm discards a lane's own guard script cache (state/guard-scripts.json) instead of refusing — lesson: When git lists an ignored fold…
- T-0833 [FEATURE S, done, 1 steps] Fm lane rm: offer to delete the lane's ignored build output (target/, voltc/target/) itsel — lesson: git status --ignored collapses a f…
- T-1923 [SECURITY M, done, 1 steps] Guard judges tree writes after a cd to a folder it can't name — lesson: bare is None whenever a command word is computed: branches gat…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–2 steps
## Why not caught
T-2259 changed where builders write but no test removed a lane with that folder; the first real lane rm after it refused
## Lessons
- A new place for files must be checked against every verb that refuses to delete files
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
