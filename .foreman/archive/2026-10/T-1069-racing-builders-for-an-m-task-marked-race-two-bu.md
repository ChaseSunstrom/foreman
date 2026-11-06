---
id: T-1069
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_race.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:50:51Z
base: 25bc528d1d39f6a3c3454932e0431fad1965540e
base_tree: a405f90368e0a9b6887707347a49b18654a43bfa
plan0_at: 2026-10-16T09:38:25Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_race.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Racing builders: for an M task marked race, two builders work it in separate worktrees and
## Raw request
> FEATURE: Racing builders: for an M task marked race, two builders work it in separate worktrees and the reviewer picks the better diff by tests, size and review (wild C13)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
For an M task marked race, two builders work it in separate lanes. fm lane race T --score compares them (tests passing, lines changed) and names a leader; pick merges only the winner and removes both lanes. L tasks are refused.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm lane race T` makes two lanes and `fm lane race T --score` prints tests, lines changed and a leader — verify with `python3 plugin/tests/run.py test_race`
- [x] `pick` merges only the winner, removes both lanes, and refuses an L task — verify with `python3 plugin/tests/run.py test_race`
## Non-goals
## Approach (options → choice → why)
fmlanes gains race() (two lanes, -a and -b, meta race mapping), score() (runs the task's checks in each worktree, diffstat) and pick() (lane merge for the winner, rm for both, race_pick event). Options considered: N-way races (cost), or auto-pick (the main thread judges).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: in a temp repo, race on an S task creates two worktrees, and `--score` output contains "tests" and "lines" for both. `pick a` leaves branch `foreman/T-a` merged, `-b` gone, and a `race_pick` event. Race on an L task, or a second race, raises PolicyError.
2. [x] Add the `race` and `pick` actions to the `fm lane` choices (`fmcli.py:4915`), `--score` as a flag, and `race()`, `score()` and `pick()` in `fmlanes.py`.
3. [x] Show both lanes in `fm lane list` through the `meta["race"]` mapping.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_race` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.5s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree a405f90368e0] (2026-10-16T09:38:26Z)
- (step 1) `python3 plugin/tests/run.py test_race` → ✗ exit 1 · Ran 3 tests in 2.2s (1 classes, 16 at a time; slowest: Race 2s) / FAILED (1 classes) [ran] [tree dcf339f7813f] (2026-10-16T09:38:44Z)
- (step 2) `python3 plugin/tests/run.py test_race test_lanes test_builder test_cli test_help test_claims` → exit 0 · Ran 173 tests in 41.1s (44 classes, 16 at a time; slowest: TaskLifecycle 41s, Lanes 32s, Contract 25s) / OK [ran] [tree 2cae67a5893d] (2026-10-16T09:40:19Z)
- (step 3) `python3 plugin/tests/run.py test_race test_lanes test_builder test_cli test_help test_claims` → exit 0 · Ran 174 tests in 30.5s (44 classes, 16 at a time; slowest: TaskLifecycle 30s, Lanes 20s, StateViews 14s) / OK [ran] [tree 4da5c83116ec] (2026-10-16T09:49:20Z)
- (ac 1) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 4 tests in 2.9s (1 classes, 16 at a time; slowest: Race 3s) / OK [ran] [tree 52d932415381] (2026-10-16T09:49:36Z)
- (ac 2) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 4 tests in 2.9s (1 classes, 16 at a time; slowest: Race 3s) / OK [ran] [tree 52d932415381] (2026-10-16T09:49:36Z)
- (step 1) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 4 tests in 2.9s (1 classes, 16 at a time; slowest: Race 3s) / OK [ran] [tree 52d932415381] (2026-10-16T09:49:36Z)
- (audit intent) `fm-reviewer (intent, adversary, edge, operator, maintainer): pick could half-finish (loser lane locked, cleanup fatal) → loser unlocked, cleanup non-fatal and reported; race wrote before builder_brief's checks → _ready checks everything under one lock, rollback if a brief fails; diffstat used a tree base and silently read 0 → HEAD...branch from main with returncode checked (test asserts ≥ 40 lines); a side could edit its own criteria to win → race_checks snapshot used by score and pick (tested); the Race section never reached the b brief → added; race sides' pre-claims clashed → skipped. Verified by the reviewer: a merge conflict raises before any drop, next_id under the lock` → two approaches compete, the better one merges, the other is kept as a branch [tree 52d932415381] (2026-10-16T09:49:36Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge, operator, maintainer): pick could half-finish (loser lane locked, cleanup fatal) → loser unlocked, cleanup non-fatal and reported; race wrote before builder_brief's checks → _ready checks everything under one lock, rollback if a brief fails; diffstat used a tree base and silently read 0 → HEAD...branch from main with returncode checked (test asserts ≥ 40 lines); a side could edit its own criteria to win → race_checks snapshot used by score and pick (tested); the Race section never reached the b brief → added; race sides' pre-claims clashed → skipped. Verified by the reviewer: a merge conflict raises before any drop, next_id under the lock` → a side can't move its goalposts; checks are guard_stored; the loser's branch is never deleted [tree 52d932415381] (2026-10-16T09:49:36Z)
- (audit edge) `fm-reviewer (intent, adversary, edge, operator, maintainer): pick could half-finish (loser lane locked, cleanup fatal) → loser unlocked, cleanup non-fatal and reported; race wrote before builder_brief's checks → _ready checks everything under one lock, rollback if a brief fails; diffstat used a tree base and silently read 0 → HEAD...branch from main with returncode checked (test asserts ≥ 40 lines); a side could edit its own criteria to win → race_checks snapshot used by score and pick (tested); the Race section never reached the b brief → added; race sides' pre-claims clashed → skipped. Verified by the reviewer: a merge conflict raises before any drop, next_id under the lock` → no worktree yet, a locked loser, no free slots, a second race, an L task [tree 52d932415381] (2026-10-16T09:49:36Z)
- (audit operator) `fm-reviewer (intent, adversary, edge, operator, maintainer): pick could half-finish (loser lane locked, cleanup fatal) → loser unlocked, cleanup non-fatal and reported; race wrote before builder_brief's checks → _ready checks everything under one lock, rollback if a brief fails; diffstat used a tree base and silently read 0 → HEAD...branch from main with returncode checked (test asserts ≥ 40 lines); a side could edit its own criteria to win → race_checks snapshot used by score and pick (tested); the Race section never reached the b brief → added; race sides' pre-claims clashed → skipped. Verified by the reviewer: a merge conflict raises before any drop, next_id under the lock` → --score names a leader; pick reports pending cleanup [tree 52d932415381] (2026-10-16T09:49:36Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge, operator, maintainer): pick could half-finish (loser lane locked, cleanup fatal) → loser unlocked, cleanup non-fatal and reported; race wrote before builder_brief's checks → _ready checks everything under one lock, rollback if a brief fails; diffstat used a tree base and silently read 0 → HEAD...branch from main with returncode checked (test asserts ≥ 40 lines); a side could edit its own criteria to win → race_checks snapshot used by score and pick (tested); the Race section never reached the b brief → added; race sides' pre-claims clashed → skipped. Verified by the reviewer: a merge conflict raises before any drop, next_id under the lock` → race reuses builder_brief, merge, remove; _ready mirrors builder_brief's checks [tree 52d932415381] (2026-10-16T09:49:36Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:01:18Z set scope=['plugin/lib/fmlanes.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_race.py']
- 2026-10-16T05:01:19Z set tier=L
- 2026-10-16T09:38:22Z set scope=['plugin/lib/fmlanes.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_race.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:38:23Z set approved=True
- 2026-10-16T09:38:24Z focused
- 2026-10-16T09:40:27Z scope: CHANGELOG.md, MASTER.md — docs
- 2026-10-16T09:49:32Z scope: MASTER.md — the review's fixes described
- 2026-10-16T09:50:49Z done
- 2026-10-16T09:50:51Z committed f165e02 (5 files)
## Follow-ups captured
## Build vs reuse
Reuses builder_brief (two briefs), fm focus binding each builder's worktree as a lane, merge() (guard-checked --no-ff merge with criteria), fm task drop --done-in, and remove() for both lanes. New: race() clones the brief under a new id, score() runs each side's criteria in its worktree with a diffstat, and pick() orchestrates the verbs above.
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-16): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmlanes.py; re-ground the plan against them before editing
## Lessons
- A multi-step command that lands something irreversible first must make every later step non-fatal and report it
## Plan gaps
- failed first: step 1 Failing tests: in a temp repo, race on an S task creates two worktrees, and `--score` output contai…
## Files touched
- plugin/tests/test_race.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
