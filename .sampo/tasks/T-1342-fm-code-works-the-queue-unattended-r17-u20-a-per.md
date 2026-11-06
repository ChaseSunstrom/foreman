---
id: T-1342
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:29Z
updated: 2026-10-23T10:31:49Z
base: 430711e04e35188b3396e9a0fba85574a85b0ac7
base_tree: 9ad1784be7abba0bd499bffeb07b4400a8af7f83
plan0_at: 2026-10-23T10:26:22Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
verified: strong
---
# Fm code works the queue unattended (R17+U20): a per-project run lock (a second run says wh
## Raw request
> fm code works the queue unattended (R17+U20): a per-project run lock (a second run says which run holds it), fm notify on close or block, fm run --runner NAME [--all-projects] through fm code --task, and in the app g works the queue until empty, a task blocks twice or a stop line; on return a 'while you were away' digest
## Interpretation
This pass: (1) one fm code run per working tree: a lock keyed by the tree's real path (a lane's worktree has its own, since worktrees share the project's state folder) holding pid, task or request and start time; a second run stops naming it, with Next: fm code tui; a dry plan takes no lock. (2) fm notify hears a run that closes, blocks or stops after making its task. The rest (fm run --runner through fm code --task, the app's g to work the queue, a while-you-were-away digest) is captured as its own item.
## Assumptions (confidence)
## Acceptance criteria
- [x] a second run in a held tree exits 1 naming the holder's task, pid and time; a dry plan still runs; a close reaches fm notify — verify with `python3 plugin/tests/run.py test_code.TreeLock`
## Non-goals
## Approach (options → choice → why)
Options: a lock on the project's state folder (lanes' worktrees share it, so parallel lanes would refuse each other); a lock per task (exists: two different tasks can still edit one tree at once); a lock per working tree, keyed by its real path, holding who has it. Choice: per tree; dry plans take none. Notify through fmserve._notify, which already guards the stored command, on close, block and a stop after the task exists.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then _hold_tree, _tell on close, block and stop
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.TreeLock` → ✗ exit 1 · Ran 2 tests in 5.2s (1 classes, 16 at a time; slowest: TreeLock 5s) / FAILED (1 classes) [ran] [tree 507e0192e2a5] (2026-10-23T10:26:34Z)
- (step 1) `python3 plugin/tests/run.py test_code.TreeLock` → exit 0 · Ran 2 tests in 2.9s (1 classes, 16 at a time; slowest: TreeLock 3s) / OK [ran] [tree 07bd5d100c2c] (2026-10-23T10:28:53Z)
- (ac 1) `python3 plugin/tests/run.py test_code.TreeLock` → exit 0 · Ran 2 tests in 3.0s (1 classes, 16 at a time; slowest: TreeLock 3s) / OK [ran] [tree 07bd5d100c2c] (2026-10-23T10:28:56Z)
- (audit intent) `self review; test_code, test_code_worker and test_code_tui green` → a second run in a held tree exits 1 naming the holder's task, pid and time with Next: fm code tui; a dry plan takes no lock; a close reaches fm notify (tests) [tree 07bd5d100c2c] (2026-10-23T10:28:56Z)
- (audit edge) `self review; test_code, test_code_worker and test_code_tui green` → the lock is keyed by the tree's real path, so a lane's worktree (same project state) has its own; the holder note is read only when the lock is held; notify failures never fail the run [tree 07bd5d100c2c] (2026-10-23T10:28:56Z)
- (audit intent) `self review; test_code, test_code_worker and test_code_tui green` → a second run in a held tree exits 1 naming the holder's task, pid and time with Next: fm code tui; a dry plan takes no lock; a close reaches fm notify (tests) [tree 07bd5d100c2c] (2026-10-23T10:30:26Z)
- (audit edge) `self review; test_code, test_code_worker and test_code_tui green` → the lock is keyed by the tree's real path, so a lane's worktree (same project state) has its own; the holder note is read only when the lock is held; notify failures never fail the run [tree 07bd5d100c2c] (2026-10-23T10:30:26Z)
- (audit adversary) `self review; test_code, test_code_worker and test_code_tui green` → sha1 only names the lock file (no security use); the holder note is JSON read with a 4 KB cap and parse fallback, printed through _one_line; the notify command is the user's own and fmserve._notify guards it and passes the message as $1, never in the shell text [tree 07bd5d100c2c] (2026-10-23T10:30:26Z)
## Log
- 2026-10-21T03:47:29Z created
- 2026-10-23T10:18:24Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-10-23T10:26:20Z focused
- 2026-10-23T10:31:47Z done
- 2026-10-23T10:31:49Z committed 633e4693 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1754 [FEATURE M, done, 3 steps] fm code: a Next: line on every failure, the start event names the Foreman running it, and a registry that stops runners… — lesson: A re…
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- decision 2026-10-16: Recommendation: build the 9 grounded items T-1180..T-1188 with builders; the worktree-fm re-exec idea is skipped (unreviewed lane code would write r…
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Lessons
- Worktrees share a project's state folder: key a lock that guards files by the working tree's real path, not by the state folder
## Plan gaps
- failed first: step 1 failing tests, then _hold_tree, _tell on close, block and stop
## Files touched
- CHANGELOG.md
- plugin/lib/fmcode.py
- plugin/tests/test_code.py
