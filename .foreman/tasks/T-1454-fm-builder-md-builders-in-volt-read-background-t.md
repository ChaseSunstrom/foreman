---
id: T-1454
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/agents/fm-builder.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T05:50:56Z
updated: 2026-10-22T14:46:34Z
base: 218fdc78f0588649abe379227e619a87c3ee3377
base_tree: 4b537fe8dd858ac19993f00b5aa31f13a13cbc24
plan0_at: 2026-10-22T14:17:13Z
plan0_scope: [plugin/agents/fm-builder.md, CHANGELOG.md]
verified: strong
---
# Builder rules name reads outside the worktree as refused
## Raw request
> fm-builder.md: builders in volt read background-task output files under /tmp/claude-*/…/tasks (53× refused by Claude Code's worktree isolation) and gitter builders ran fm task evidence (34×) despite fm-builder.md:35: add the task-output case and check the lane brief repeats both
## Interpretation
Claude Code's worktree isolation refused 53 volt builder reads of background-task output files under /tmp/claude-*/…/tasks and 8 Foreman builder scratchpad commands; fm-builder.md's refusal list names only commands (make, fm task evidence…), so builders retried.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm-builder.md names task output files and the scratchpad among refused paths, and a lane brief carries it — verify with `grep -q 'task output' plugin/agents/fm-builder.md`
## Non-goals
## Approach (options → choice → why)
One clause in fm-builder.md's isolation bullet: reads or writes outside the worktree (another session's task output files, the main thread's scratchpad) are refused too; use the worktree or report what's needed. fm lane brief reads the file (T-1290), so briefs pick it up.
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the clause
## Resume here
## Docs impact
fm-builder.md, CHANGELOG
## Verification evidence
- (step 1) `grep -q 'task output' plugin/agents/fm-builder.md && python3 -m unittest discover -s plugin/tests -p 'test_builder.py' -q` → exit 0 · Ran 20 tests in 35.471s / OK [ran] [tree fcbb72ca9483] (2026-10-22T14:17:56Z)
- (ac 1) `grep -q 'task output' plugin/agents/fm-builder.md` → exit 0 · (no output) [ran] [tree 6a3af19f1fdd] (2026-10-22T14:17:58Z)
- (audit intent) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → the 53 volt refusals were reads of task outputs, now named [tree 6a3af19f1fdd] (2026-10-22T14:17:58Z)
- (audit self) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → no findings [tree 6a3af19f1fdd] (2026-10-22T14:17:58Z)
- (audit intent) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → the 53 volt refusals were reads of task outputs, now named [tree 455c1d1060b1] (2026-10-22T14:23:20Z)
- (audit self) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → no findings [tree 455c1d1060b1] (2026-10-22T14:23:20Z)
- (audit intent) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → the 53 volt refusals were reads of task outputs, now named [tree 455c1d1060b1] (2026-10-22T14:34:36Z)
- (audit self) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → no findings [tree 455c1d1060b1] (2026-10-22T14:34:36Z)
- (audit intent) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → the 53 volt refusals were reads of task outputs, now named [tree 455c1d1060b1] (2026-10-22T14:45:15Z)
- (audit adversary) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → this task changes only a doc clause; the guard files in its diff are T-1452's (dea9379b), whose message-only hint changes no decision [tree 455c1d1060b1] (2026-10-22T14:45:15Z)
- (audit self) `self: one clause in fm-builder.md's isolation bullet; fm lane brief reads the file (fmlanes.py:140), so every brief carries it; test_builder green.` → no findings [tree 455c1d1060b1] (2026-10-22T14:45:15Z)
## Log
- 2026-10-22T05:50:56Z created
- 2026-10-22T14:03:14Z planned from capture
- 2026-10-22T14:17:12Z focused
- 2026-10-22T14:21:15Z paused: focus moved to T-1452
- 2026-10-22T14:23:19Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-22T14:23:19Z focused
- 2026-10-22T14:34:35Z scope: plugin/lib/fmguard.py and plugin/tests/test_guard.py are T-1452's, committed in dea9379b while this task was open; this task changes only fm-builder.md (its CHANGELOG line landed in dea9379b too)
- 2026-10-22T14:46:33Z done
- 2026-10-22T14:46:34Z committed 9a94ae65 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- T-0316 [RESEARCH M, done, 1 steps] Re-run one real fm-builder lane end to end after a Claude Code update — lesson: A block that waits on an outside update should name th…
- T-1450 [FEATURE S, done, 2 steps] Doctor warns before the disk fills
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–2 steps
- start here (files T-0379 touched): plugin/tests/test_builder.py, plugin/lib/fmlanes.py, CHANGELOG.md
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md; re-ground the plan against them before editing
## Regression test
none: a one-clause doc change to fm-builder.md; the grep criterion is its check and test_builder covers the brief that carries it
## Files touched
- plugin/agents/fm-builder.md
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
