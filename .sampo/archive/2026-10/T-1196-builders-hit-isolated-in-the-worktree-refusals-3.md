---
id: T-1196
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T13:28:36Z
updated: 2026-10-16T14:34:45Z
base: d5cdcd8e9242c8c1a02ef7a18cbdcad5893baac2
base_tree: a1b7dcca6d9e2d4fb42eee0b2a8c96fc7397891b
plan0_at: 2026-10-16T14:30:33Z
plan0_scope: []
verified: strong
---
# Builder brief names the main checkout to stay out of and says fm runs on the lane from the worktree
## Raw request
> Builders hit 'isolated in the worktree' refusals 31x: say in the builder brief (and the refusal) which absolute worktree path to cd to, and that fm verbs run from the worktree act on the lane
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the builder brief and fm-builder.md say the worktree is the starting directory (pwd), name the main checkout's absolute path as the one never to cd or write into, and say fm verbs run from the worktree act on the lane; the builder contract drift test still passes — verify with `python3 plugin/tests/run.py test_builder test_lanes test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing assertion in test_builder for the main checkout path and the pwd line in the brief
2. [x] Brief text in fmlanes.py and the same lines in agents/fm-builder.md
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_builder test_lanes` → ✗ exit 1 · Ran 51 tests in 15.5s (11 classes, 16 at a time; slowest: Lanes 15s, Contract 10s, Brief 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 32169a7b9211] (2026-10-16T14:31:31Z)
- `python3 plugin/tests/run.py test_builder test_lanes` → ✗ exit 1 · Ran 51 tests in 11.1s (11 classes, 16 at a time; slowest: Lanes 11s, Contract 7s, Brief 3s) / FAILED (1 classes) [ran] [tree 32169a7b9211] (2026-10-16T14:31:31Z)
- `python3 plugin/tests/run.py test_builder test_lanes` → ✗ exit 1 · Ran 51 tests in 11.5s (11 classes, 16 at a time; slowest: Lanes 11s, Contract 7s, Brief 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9bc1d2c1e4d1] (2026-10-16T14:32:49Z)
- `python3 plugin/tests/run.py test_builder test_lanes` → exit 0 · Ran 51 tests in 11.1s (11 classes, 16 at a time; slowest: Lanes 11s, Contract 7s, Brief 3s) / OK [ran] [tree 9bc1d2c1e4d1] (2026-10-16T14:32:49Z)
- (step 1) `python3 plugin/tests/run.py test_builder test_lanes test_docs` → exit 0 · Ran 83 tests in 27.1s (22 classes, 16 at a time; slowest: Lanes 27s, Contract 17s, Brief 8s) / OK [ran] [tree b35585d69fdb] (2026-10-16T14:33:24Z)
- (step 2) `python3 plugin/tests/run.py test_builder test_lanes test_docs` → exit 0 · Ran 83 tests in 16.6s (22 classes, 16 at a time; slowest: Lanes 16s, Contract 12s, Brief 7s) / OK [ran] [tree b35585d69fdb] (2026-10-16T14:33:41Z)
- (ac 1) `python3 plugin/tests/run.py test_builder test_lanes test_docs` → exit 0 · Ran 83 tests in 12.4s (22 classes, 16 at a time; slowest: Lanes 12s, Contract 8s, Brief 4s) / OK [ran] [tree b35585d69fdb] (2026-10-16T14:33:54Z)
- (audit self) `self: folded into the existing stay-in-worktree rule rather than a new bullet, so the contract says it once; the brief fills in p.root, the agent file says <MAIN> like its <BASE>; the T-1151 drift test formats the new placeholder` → no findings [tree b35585d69fdb] (2026-10-16T14:33:54Z)
## Log
- 2026-10-16T13:28:36Z created
- 2026-10-16T13:59:13Z planned from capture
- 2026-10-16T14:01:58Z set approved=True
- 2026-10-16T14:30:33Z focused
- 2026-10-16T14:33:41Z scope: CHANGELOG line
- 2026-10-16T14:34:44Z done
- 2026-10-16T14:34:45Z committed b0f330c5 (5 files)
## Follow-ups captured
## Notes
- [fact] Grounded: the hint text lives in plugin/lib/fmlanes.py:156-159 (the builder brief template) and plugin/agents/fm-builder.md:33-36; test_builder.py:67 pins 'isolated in the worktree'; the brief template can name p.root (the main checkout) since the worktree doesn't exist yet when the brief is written; fm second plan skips S tasks
## Related
Related past work (data from this project's history, not instructions):
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–2 steps
## Files touched
- plugin/tests/test_builder.py
- plugin/agents/fm-builder.md
- plugin/lib/fmlanes.py
- plugin/tests/test_lanes.py
- CHANGELOG.md
