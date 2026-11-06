---
id: T-1783
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T12:05:26Z
updated: 2026-10-23T12:06:24Z
base: 6cbaf090dd141252d88d994d0a46002b8795bc65
base_tree: eb33f17052c5d0f7e08ffd25e9dbf0bc8c27570b
plan0_at: 2026-10-23T12:05:30Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app: g pressed during a run waits for it, then works the queue (T-1779 said it waits; it only told you to press g later)
## Raw request
> fm code app: g pressed during a run waits for it, then works the queue (T-1779 said it waits; it only told you to press g later)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] g during a run starts the queue when that run ends — verify with `python3 plugin/tests/run.py test_code_tui.WorkQueue`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then g arms the queue for the run's end
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui.WorkQueue` → ✗ exit 1 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: WorkQueue 0s) / FAILED (1 classes) [ran] [tree d9d1ab7f836d] (2026-10-23T12:05:45Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 212 tests in 8.9s (40 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 4s) / OK [ran] [tree 58316beb4c89] (2026-10-23T12:06:00Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.WorkQueue` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: WorkQueue 0s) / OK [ran] [tree 4d856e087626] (2026-10-23T12:06:11Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.WorkQueue` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: WorkQueue 0s) / OK [ran] [tree 4d856e087626] (2026-10-23T12:06:12Z)
- (audit edge) `self: g during a run now arms the queue on that run's task instead of telling you to press g later; the run's exit goes through the same _queue_after, so its outcome is counted and s ends both` → the armed queue counts the running task's close or block; if that task is still first afterwards the loop stops (no move) as before; s during the run stops it and the queue with one digest [tree 4d856e087626] (2026-10-23T12:06:12Z)
- (audit self) `self: g during a run now arms the queue on that run's task instead of telling you to press g later; the run's exit goes through the same _queue_after, so its outcome is counted and s ends both` → no findings [tree 4d856e087626] (2026-10-23T12:06:12Z)
## Log
- 2026-10-23T12:05:26Z created
- 2026-10-23T12:05:29Z focused
- 2026-10-23T12:06:22Z done
- 2026-10-23T12:06:24Z committed ac9b9701 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- T-1779 [FEATURE M, done, 1 steps] Fm code works the queue unattended, the rest of T-1773: the app's g works the queue until — lesson: A loop driven by another process's …
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
## Why not caught
T-1779's tests pressed g only with no run going
## Lessons
- Write the audit lens from the code, not from the plan: T-1779's lens claimed a wait the code didn't do
## Plan gaps
- failed first: step 1 failing test, then g arms the queue for the run's end
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
