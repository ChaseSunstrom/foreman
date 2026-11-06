---
id: T-1764
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T08:18:00Z
updated: 2026-10-23T08:21:46Z
base: 444a6cb120a10d0d0d02d843edf7fc89979b5383
base_tree: 39142ebcc353be79ded67e3ebf6ba1447835b070
plan0_at: 2026-10-23T08:18:07Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
verified: strong
---
# fm code: a model run's edit leases outlive it (drop_session ran only for worker runs), so the next run on the same code is refused for 20 minutes
## Raw request
> fm code: a model run's edit leases outlive it (drop_session ran only for worker runs), so the next run on the same code is refused for 20 minutes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two model runs editing the same function back to back both close: the first run's leases end with it — verify with `python3 plugin/tests/run.py test_code.Leases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then drop the run's leases whenever it has a task
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_code.Leases` → ✗ exit 1 · Ran 1 tests in 2.9s (1 classes, 16 at a time; slowest: Leases 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7475258bbe3f] (2026-10-23T08:18:13Z)
- `python3 plugin/tests/run.py test_code.Leases` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Leases 1s) / FAILED (1 classes) [ran] [tree 7475258bbe3f] (2026-10-23T08:18:13Z)
- `python3 plugin/tests/run.py test_code.Leases` → ✗ exit 1 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: Leases 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1f7e14dfd0f5] (2026-10-23T08:18:26Z)
- `python3 plugin/tests/run.py test_code.Leases` → exit 0 · Ran 1 tests in 2.6s (1 classes, 16 at a time; slowest: Leases 2s) / OK [ran] [tree 1f7e14dfd0f5] (2026-10-23T08:18:26Z)
- (step 1) `python3 plugin/tests/run.py test_code.Leases test_bus` → exit 0 · Ran 22 tests in 6.3s (7 classes, 16 at a time; slowest: Watch 6s, Lease 4s, Approvals 4s) / OK [ran] [tree 1f7e14dfd0f5] (2026-10-23T08:19:58Z)
- (audit intent) `self` → pass: a model run's leases end with it (tested back to back) [tree 7981e49ee6be] (2026-10-23T08:20:22Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Leases` → exit 0 · Ran 1 tests in 2.6s (1 classes, 16 at a time; slowest: Leases 2s) / OK [ran] [tree 7981e49ee6be] (2026-10-23T08:20:25Z)
- (audit intent) `self: intent, edge` → the next run on the same code is no longer refused [tree 7981e49ee6be] (2026-10-23T08:20:25Z)
- (audit edge) `self: intent, edge` → a run with no task (a question, a dry plan) holds no leases to drop; a worker run behaves as before [tree 7981e49ee6be] (2026-10-23T08:20:25Z)
- (audit self) `self: intent, edge` → no findings [tree 7981e49ee6be] (2026-10-23T08:20:25Z)
## Log
- 2026-10-23T08:18:00Z created
- 2026-10-23T08:18:06Z set priority=urgent, scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-10-23T08:18:07Z focused
- 2026-10-23T08:20:08Z scope: plugin/tests/test_code_tui.py — the plain-output test now allows T-1349's first-close note after the closed line; both changes share fmcode.py
- 2026-10-23T08:20:08Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T08:21:44Z done
- 2026-10-23T08:21:46Z committed 2de05a16 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- research T-1294-review: Verdict: approve with nits.** The diff file holds only the CHANGELOG hunk. I reviewed the real working-tree changes in `fmbus.py`, `fmcode.py` an…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
- likely tests for the scope: plugin/tests/test_code.py
## Why not caught
every fm code test ran one model run per project, and T-1294's lease drop was tested only with a worker
## Lessons
- Cleanup tied to one kind of run (worker) must be checked against every kind that takes the resource
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- plugin/tests/test_code_tui.py
