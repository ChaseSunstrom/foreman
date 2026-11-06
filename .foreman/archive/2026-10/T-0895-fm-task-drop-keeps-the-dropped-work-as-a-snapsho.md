---
id: T-0895
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T16:45:27Z
updated: 2026-10-15T16:48:42Z
base: 92ce4ac2acebd40d194c7175b4a5764fbdbf7925
base_tree: 90022784c3829c5e9c714198567ea319243f1bec
verified: strong
---
# Fm task drop keeps the dropped work as a snapshot (refs/foreman/snapshots) and the brief s
## Raw request
> FEATURE: fm task drop keeps the dropped work as a snapshot (refs/foreman/snapshots) and the brief says how to bring it back
> CONTEXT: round 6 #33. fmcore.snapshot (T-0884) and pause_snapshot exist; block/defer snapshot a tree, drop keeps nothing
## Interpretation
Dropping a task that was in progress (active or verifying) saves the working files first (fmcore.snapshot, the refs from T-0884) when they differ from HEAD, and the brief's log names the snapshot and its restore line, so dropped work can be picked up again
## Assumptions (confidence)
## Acceptance criteria
- [x] a dropped in-progress task's work is in a snapshot named in its log — verify with `python3 plugin/tests/run.py test_snapshots`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_snapshots, then snapshot before the drop
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_snapshots test_cli` → exit 0 · Ran 95 tests in 17.7s (25 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree 577cdcc371a8] (2026-10-15T16:46:43Z)
- `python3 plugin/tests/run.py test_snapshots` → ✗ exit 1 · Ran 7 tests in 2.4s (1 classes, 16 at a time; slowest: Snapshots 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 577cdcc371a8] (2026-10-15T16:46:48Z)
- `python3 plugin/tests/run.py test_snapshots` → exit 0 · Ran 7 tests in 2.1s (1 classes, 16 at a time; slowest: Snapshots 2s) / OK [ran] [tree 577cdcc371a8] (2026-10-15T16:46:48Z)
- (ac 1) `python3 plugin/tests/run.py test_snapshots` → exit 0 · Ran 7 tests in 2.1s (1 classes, 16 at a time; slowest: Snapshots 2s) / OK [ran] [tree 577cdcc371a8] (2026-10-15T16:48:41Z)
- (audit self) `self review: only a drop of an active or verifying task snapshots (30 s budget, a failure warns and the drop still happens); the brief's log and the output name the sha and restore line; --done-in drops are untouched` → no findings [tree 577cdcc371a8] (2026-10-15T16:48:41Z)
## Log
- 2026-10-15T16:45:27Z created
- 2026-10-15T16:45:31Z set tier=S
- 2026-10-15T16:45:46Z focused
- 2026-10-15T16:48:41Z done
- 2026-10-15T16:48:42Z committed 468a790 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0884 [FEATURE M, done, 3 steps] Snapshot uncommitted work before a Bash command discards it (git reset --hard, checkout -- — lesson: A hook that does real work before …
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research brainstorm-round6-20261015: Probe: `fm ideas` with user value + bold bets, 2 rounds, past every earlier ideas.md (brainstorm-20261015-113737): 49 new titles, ea…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Files touched
- plugin/tests/test_snapshots.py
- plugin/lib/fmcli.py
