---
id: T-1779
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T11:35:25Z
updated: 2026-10-23T12:05:15Z
base: 71fadccca4446534bf8f6674f9719b1339138fda
base_tree: 5a15c99cbacf37fd4dbaf02ec5f6bf0efbb81615
plan0_at: 2026-10-23T12:03:25Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Fm code works the queue unattended, the rest of T-1773: the app's g works the queue until
## Raw request
> fm code works the queue unattended, the rest of T-1773: the app's g works the queue until empty, a task blocks twice or a stop line; a while-you-were-away digest on return; fm run --runner NAME --all-projects
## Interpretation
In the fm code app, g works the project's queue: one fm code --task run after another (fm queue's order), until the queue is empty, two tasks in a row block, or s stops it; then a digest lands in Activity, headed 'While you were away' when no key came for five minutes. 'A stop line' is read as s (the stop key), as no stop-line mechanism exists. fm run --runner --all-projects is captured as its own item.
## Assumptions (confidence)
## Acceptance criteria
- [x] g runs queued tasks in turn, stops on two blocks in a row, an empty queue or s, and leaves a digest — verify with `python3 plugin/tests/run.py test_code_tui.WorkQueue`
## Non-goals
## Approach (options → choice → why)
Options: (1) the app chains runs itself on each exit event, the queue's next id from fm queue --json, the digest as Activity notes (chosen: the app already owns one run's lifecycle; nothing new to supervise); (2) spawn fm run --runner from the app and show its log (rejected: fm run's output isn't fm code's event stream, so the app couldn't show the runs); (3) a queue mode in fm code itself (rejected: duplicates fm run). Stops on the same task coming first twice too (no move).
## Risks and rollback
## Execution prompt
## Steps
1. [x] g and the queue loop with its digest, test first
## Resume here
## Docs impact
CHANGELOG line; the app's help (?) lists g from COMMAND_LABELS, and fm settings shows it under keys (rebindable).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui.WorkQueue` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: WorkQueue 0s) / FAILED (1 classes) [ran] [tree eccc2c6b7c5a] (2026-10-23T12:03:27Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_settings test_settings_safety test_settings_power test_code` → exit 0 · Ran 521 tests in 77.6s (107 classes, 16 at a time; slowest: Worker 77s, Fakes 44s, Bench 21s) / OK [ran] [tree eb33f17052c5] (2026-10-23T12:04:53Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.WorkQueue` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: WorkQueue 0s) / OK [ran] [tree eb33f17052c5] (2026-10-23T12:05:02Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.WorkQueue` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: WorkQueue 0s) / OK [ran] [tree eb33f17052c5] (2026-10-23T12:05:03Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the loop hangs off the exit event the app already gets; each step reads fm queue fresh, so a task planned meanwhile joins and a blocked one leaves; three ends (empty, two blocks in a row, anything else such as s or an error) all go through one digest` → g works the queue in the app until it's empty, two tasks in a row block, or s stops it, then says what happened, as 'While you were away' after five quiet minutes [tree eb33f17052c5] (2026-10-23T12:05:03Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the loop hangs off the exit event the app already gets; each step reads fm queue fresh, so a task planned meanwhile joins and a blocked one leaves; three ends (empty, two blocks in a row, anything else such as s or an error) all go through one digest` → a run going when g is pressed is not interrupted (g waits for it to end); a task that stays first after its run (no move) stops the loop instead of spinning; an unreadable fm queue reads as empty; one blocked task between closes doesn't stop it [tree eb33f17052c5] (2026-10-23T12:05:03Z)
## Log
- 2026-10-23T11:35:25Z created
- 2026-10-23T11:51:07Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T12:03:24Z focused
- 2026-10-23T12:05:14Z done
- 2026-10-23T12:05:15Z committed 6cbaf090 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1773 [FEATURE M, done, 1 steps] Fm code works the queue unattended, the rest of T-1342: fm run --runner NAME [--all-projec — lesson: Give a loop one seam for what it r…
- T-1342 [FEATURE M, done, 1 steps] Fm code works the queue unattended (R17+U20): a per-project run lock (a second run says wh — lesson: Worktrees share a project's state …
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-23: T-1779: 'a stop line' read as the s key; --all-projects left out
- similar finished tasks took 1–3 steps
## Lessons
- A loop driven by another process's exit must stop when the next item is the same as the last: no progress is its own end
## Plan gaps
- failed first: step 1 g and the queue loop with its digest, test first
## Files touched
- plugin/tests/test_code_tui.py
- CHANGELOG.md
- plugin/lib/fmcodetui.py
