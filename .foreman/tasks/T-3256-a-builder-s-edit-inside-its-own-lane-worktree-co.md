---
id: T-3256
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T00:29:29Z
updated: 2026-11-06T00:32:52Z
base: 4a79fe32646411faf49b319a7ae4546b5c0c0d43
base_tree: dff69c4704d0629144e0b09c8e88b75066009390
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T00:29:33Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# A builder's edit inside its own lane worktree counts for the lane's task, never for the main checkout's active task (a Write to .claude/worktrees/<lane>/x was booked to the main task, so its close kept failing the scope gate while builders worked)
## Raw request
> A builder's edit inside its own lane worktree counts for the lane's task, never for the main checkout's active task (a Write to .claude/worktrees/<lane>/x was booked to the main task, so its close kept failing the scope gate while builders worked)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an Edit or Write under .claude/worktrees/<lane>/ is booked to that lane's active task, or to none, never to the main checkout's — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the hook reads the lane from the edited path
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks -k lane_worktree` → ✗ exit 1 · Ran 1 tests in 1.5s (1 jobs, 16 at a time; slowest: PostToolUse 1s) / FAILED (1 classes: test_hooks.PostToolUse) [ran] [tree 9c318edd3478] [world 2f1906870a] (2026-11-06T00:29:42Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 259 tests in 33.3s (248 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 22s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 0849340a7f74] [world 2f1906870a] (2026-11-06T00:30:25Z)
- `python3 plugin/tests/run.py test_hooks -k lane_worktree` → ✗ exit 1 · Ran 1 tests in 3.8s (1 jobs, 16 at a time; slowest: PostToolUse 1s) / FAILED (1 classes: test_hooks.PostToolUse) (start tree + this task's tests) [ran] [tree 1395d0f856bc] [world 2f1906870a] (2026-11-06T00:30:41Z)
- `python3 plugin/tests/run.py test_hooks -k lane_worktree` → exit 0 · Ran 1 tests in 1.6s (1 jobs, 16 at a time; slowest: PostToolUse 1s) / OK [ran] [tree 1395d0f856bc] [world 2f1906870a] (2026-11-06T00:30:41Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 259 tests in 41.8s (237 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 27s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 1395d0f856bc] [world 2f1906870a] (2026-11-06T00:31:31Z)
- (audit edge) `self: one hook branch reads the lane from the edited path; tested with a subagent Write into a lane worktree` → a path outside p.root, or p.lane already set (the session runs inside the lane), keeps today's behaviour; a worktree with no lane task books the edit to no task [tree 1395d0f856bc] (2026-11-06T00:31:31Z)
- (audit intent) `self: one hook branch reads the lane from the edited path; tested with a subagent Write into a lane worktree` → the main task's scope gate sees only main-checkout edits [tree 1395d0f856bc] (2026-11-06T00:31:31Z)
- (audit self) `self: one hook branch reads the lane from the edited path; tested with a subagent Write into a lane worktree` → no findings [tree 1395d0f856bc] (2026-11-06T00:31:31Z)
## Log
- 2026-11-06T00:29:29Z created
- 2026-11-06T00:29:30Z focused
- 2026-11-06T00:29:33Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T00:30:46Z scope: other uncommitted files (README, docs/map, works, cli, figures) are T-3247's, and builder edits in their worktrees were booked here before this fix
- 2026-11-06T00:32:49Z done
- 2026-11-06T00:32:52Z committed f41ebf15 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2784 [FIX M, done, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's l…
- T-0807 [FIX S, done, 2 steps] A lane's edits recorded under .claude/worktrees/<lane>/ count as the repo files they are — lesson: record a lane's edits as the repo files …
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar finished tasks took 2–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Why not caught
Builders used to run with worktree isolation (their own cwd, so p.lane was set); resumed builders work from the main cwd into an existing worktree
## Lessons
- Edits are attributed by the session's focus, but a session's subagents edit other trees: attribute by the path's own tree
## Plan gaps
- failed first: step 1 failing test, then the hook reads the lane from the edited path
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
