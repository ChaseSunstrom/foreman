---
id: T-0729
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T17:27:26Z
updated: 2026-10-09T17:30:48Z
batch: [T-0725, T-0726]
base: 6933ae7cd32dfd5338a8d5e6abd2a93244f56e27
base_tree: 303c3f375c6ce2cd2ef1edf1f7e5f31fd5500931
verified: strong
---
# Friction: lane rm unlocks a finished builder's worktree; no false re-ask note on capture
## Raw request
> T-0725: fm lane rm fails on a worktree Claude Code still locks for a finished builder ('locked … claude agent … pid <this session>'): when the branch is merged and the lock names a claude agent, unlock it (or say the one command that does)
> T-0726: fm capture prints 'Dropped before: T-0260 (Evidence quality…)' for unrelated requests (4 times today: audit diffs, lane locks, commit retry): the re-ask match fires on T-0260's huge batch request text; cap or skip batch-shell requests in the match
## Interpretation
Do T-0725, T-0726 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0729. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0725 fm lane rm unlocks a worktree a Claude Code agent still locks once its branch is in main, and says so plainly when it isn't — verify with `python3 plugin/tests/run.py -p test_lanes.py -k Lanes`
- [x] T-0726 a capture sharing words with a dropped batch's huge request isn't called a re-ask; a real re-ask still is — verify with `python3 plugin/tests/run.py -p test_cli.py -k reask`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] both failing tests first
2. [x] fmlanes.remove: unlock a claude-agent lock when the branch is merged
3. [x] fmrecall.nearest_dropped: the shared words must be a real share of the dropped request too
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_lanes.py -p test_cli.py` → ✗ exit 1 · Ran 87 tests in 26.9s (17 classes, 16 at a time; slowest: TaskLifecycle 27s, StateViews 11s, Lanes 10s) / FAILED (2 classes) [ran] [tree d98f66bd0407] (2026-10-09T17:28:29Z)
- (step 1) `python3 plugin/tests/run.py -p test_cli.py -k reask` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree fa620fe991d3] (2026-10-09T17:29:55Z)
- (ac 1) `python3 plugin/tests/run.py -p test_lanes.py -k Lanes` → exit 0 · Ran 10 tests in 4.1s (1 classes, 16 at a time; slowest: Lanes 4s) / OK [ran] [tree 376592ea9c63] (2026-10-09T17:30:47Z)
- (ac 2) `python3 plugin/tests/run.py -p test_cli.py -k reask` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 376592ea9c63] (2026-10-09T17:30:47Z)
- (step 2) `python3 plugin/tests/run.py -p test_lanes.py -p test_cli.py` → exit 0 · Ran 87 tests in 16.8s (17 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 6s, Lanes 5s) / OK [ran] [tree 376592ea9c63] (2026-10-09T17:30:47Z)
- (step 3) `python3 plugin/tests/run.py -p test_lanes.py -p test_cli.py` → exit 0 · Ran 87 tests in 16.8s (17 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 6s, Lanes 5s) / OK [ran] [tree 376592ea9c63] (2026-10-09T17:30:47Z)
- (audit adversary) `self: unlock happens only for a 'claude agent' lock whose branch tip is an ancestor of main's HEAD, after the existing clean-tree check; the re-ask share check keeps the T-0438 test passing` → a live builder's unmerged worktree stays locked and the error says merge first; merged work is in main, so removing its folder loses nothing (uncommitted files still refuse the removal) [tree 376592ea9c63] (2026-10-09T17:30:47Z)
- (audit self) `self: unlock happens only for a 'claude agent' lock whose branch tip is an ancestor of main's HEAD, after the existing clean-tree check; the re-ask share check keeps the T-0438 test passing` → no findings [tree 376592ea9c63] (2026-10-09T17:30:47Z)
## Log
- 2026-10-09T17:27:26Z created
- 2026-10-09T17:27:51Z focused
- 2026-10-09T17:30:47Z done
- 2026-10-09T17:30:48Z committed 9d1c16b (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0722 [FIX S, done, 3 steps] Close-out friction: audit prep reads a builder's branch; a refused commit can be retried
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0678 [FEATURE M, planned, 2 steps] Milestone: Features — Releases and delivery
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 3–3 steps
- start here (files T-0722 touched): plugin/tests/test_builder.py, plugin/tests/test_secrets.py, plugin/lib/fmcli.py, CHANGELOG.md
## Files touched
- plugin/tests/test_lanes.py
- plugin/tests/test_cli.py
- plugin/lib/fmlanes.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
