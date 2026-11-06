---
id: T-0918
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:18Z
updated: 2026-10-15T19:27:24Z
base: 7102c9142c9226c8aa246cd1baf9686f23c15158
base_tree: c136b2c12a99560c5e68f00092c6235ed789c981
verified: strong
---
# A close names its undo and says when nothing is needed from you
## Raw request
> A close names its undo and says when nothing is needed from you
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish prints 'Undo: git revert <sha>' after a commit and 'Nothing needed from you' when no criterion needs a check by hand — verify with `python3 plugin/tests/run.py -k CloseUndo`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then two lines in the finish output
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k CommitOwnFiles` → ✗ exit 1 · Ran 3 tests in 4.7s (1 classes, 16 at a time; slowest: CommitOwnFiles 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 05b4400d9dc4] (2026-10-15T19:27:08Z)
- `python3 plugin/tests/run.py -k CommitOwnFiles` → exit 0 · Ran 3 tests in 3.8s (1 classes, 16 at a time; slowest: CommitOwnFiles 4s) / OK [ran] [tree 05b4400d9dc4] (2026-10-15T19:27:08Z)
- (ac 1) `python3 plugin/tests/run.py -k CloseUndo` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 05b4400d9dc4] (2026-10-15T19:27:09Z)
- (step 1) `python3 plugin/tests/run.py -k Verifying` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 05b4400d9dc4] (2026-10-15T19:27:09Z)
- (ac 1) `python3 plugin/tests/run.py -k CloseUndo` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CloseUndo 0s) / OK [ran] [tree 536b188de08a] (2026-10-15T19:27:23Z)
- (step 1) `python3 plugin/tests/run.py -k CommitOwnFiles` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: CommitOwnFiles 1s) / OK [ran] [tree 536b188de08a] (2026-10-15T19:27:23Z)
- (audit edge) `self: the commit line ends with Undo: git revert --no-edit <sha>; a close with no check-by-hand criteria and no unverified assumptions says Nothing needed from you; nothing parses the commit line (grep)` → a stacked commit prints its own lines (fmstack), unchanged; a close with unverified assumptions doesn't claim nothing is needed [tree 536b188de08a] (2026-10-15T19:27:23Z)
- (audit self) `self: the commit line ends with Undo: git revert --no-edit <sha>; a close with no check-by-hand criteria and no unverified assumptions says Nothing needed from you; nothing parses the commit line (grep)` → no findings [tree 536b188de08a] (2026-10-15T19:27:23Z)
## Log
- 2026-10-15T19:25:18Z created
- 2026-10-15T19:26:11Z focused
- 2026-10-15T19:27:24Z done
- 2026-10-15T19:27:24Z committed 95bb32f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- T-0896 [FEATURE S, done, 1 steps] A RESEARCH task can't close without a Decision section, and its decision lands in decision
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar finished tasks took 1–2 steps
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
