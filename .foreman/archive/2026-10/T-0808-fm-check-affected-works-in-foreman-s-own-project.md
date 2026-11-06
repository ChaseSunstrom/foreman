---
id: T-0808
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py, plugin/lib/fmlanes.py, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-10-14T17:08:42Z
updated: 2026-10-14T17:11:51Z
base: d7b9f1c7b196821c65864e694a779e4d168f8ed5
base_tree: 5013984f2d49f13f72dd7e33114f4c85d8c30cc3
verified: strong
---
# fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains
## Raw request
> fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains
## Interpretation
T-0806 told builders to run fm check --affected, but this project has no affected-tests command (fm check affected), so it errors ('no affected-tests command'); and builders' 'fm task evidence … --run "cd plugin/tests && …"' was refused by Claude Code's isolation as too complex (T-0399), so lanes skipped recording red runs. run.py takes test module names as positional arguments (each like -k), this project registers 'python3 plugin/tests/run.py {names}', and the builder contract says to run checks from the repo root without cd chains.
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py accepts module names positionally like -k; fm check affected is set for this project; the builder contract says to avoid cd chains in verify commands — verify with `python3 plugin/tests/run.py test_run test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests
2. [x] run.py names, the project's affected command, the contract line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_run` → ✗ exit 1 · Ran 12 tests in 1.7s (12 classes, 16 at a time; slowest: Bench 2s, Run 1s, Fit 1s) / FAILED (1 classes) [ran] [tree c1e155ec40d7] (2026-10-14T17:08:51Z)
- (step 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 12 tests in 1.7s (12 classes, 16 at a time; slowest: Bench 2s, Run 1s, Fit 1s) / OK [ran] [tree b4ad9ceb2406] (2026-10-14T17:09:40Z)
- (step 2) `fm check --affected` → exit 0 · ✓ affected tests only (1): python3 plugin/tests/run.py test_lanes → exit 0 · Ran 13 tests in 5.3s (2 classes, 16 at a time; slowest: Lanes 5s, BuilderGates 0s) / OK / (the full gates still decide befo [ran] [tree b4ad9ceb2406] (2026-10-14T17:09:46Z)
- (ac 1) `python3 plugin/tests/run.py test_run test_lanes` → exit 0 · Ran 25 tests in 5.4s (14 classes, 16 at a time; slowest: Lanes 5s, Bench 2s, Run 1s) / OK [ran] [tree b4ad9ceb2406] (2026-10-14T17:09:52Z)
- `python3 plugin/tests/run.py test_run` → exit 0 · Ran 12 tests in 1.9s (12 classes, 16 at a time; slowest: Bench 2s, Run 1s, Fit 1s) / OK (start tree + this task's tests) [ran] [tree b4ad9ceb2406] (2026-10-14T17:09:56Z)
- `python3 plugin/tests/run.py test_run` → exit 0 · Ran 12 tests in 1.7s (12 classes, 16 at a time; slowest: Bench 2s, Run 1s, Fit 1s) / OK [ran] [tree b4ad9ceb2406] (2026-10-14T17:09:56Z)
- (ac 1) `python3 plugin/tests/run.py test_run test_lanes` → exit 0 · Ran 25 tests in 5.5s (14 classes, 16 at a time; slowest: Lanes 5s, Bench 2s, Run 1s) / OK [ran] [tree b4ad9ceb2406] (2026-10-14T17:11:51Z)
- (audit edge) `self: diff read; run.py's names join -k (intermixed parsing so names may sit either side of -k), this project's affected command is 'python3 plugin/tests/run.py {names}', and the builder contract says to run checks from the worktree root without cd chains; fm check --affected ran test_lanes for real` → a name that is also a substring of other test ids selects those too (same as -k, which run.py documents) [tree b4ad9ceb2406] (2026-10-14T17:11:51Z)
- (audit self) `self: diff read; run.py's names join -k (intermixed parsing so names may sit either side of -k), this project's affected command is 'python3 plugin/tests/run.py {names}', and the builder contract says to run checks from the worktree root without cd chains; fm check --affected ran test_lanes for real` → no findings [tree b4ad9ceb2406] (2026-10-14T17:11:51Z)
## Log
- 2026-10-14T17:08:42Z created
- 2026-10-14T17:08:42Z focused
- 2026-10-14T17:11:51Z done
- 2026-10-14T17:11:51Z committed 3e8ceca (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- research rsi-20261009-review: 1. **Answer.** Two guard-related frictions are grounded in code: the guard misreads remote interpreter code run over `ssh` as local Foreman…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 1–2 steps
- likely tests for the scope: plugin/tests/test_lanes.py
## Regression test
test_run.Args and test_lanes.BuilderGates (red before the change: step 1's first ✗ run). fm task prove can't separate them: run.py lives in plugin/tests, so prove carries it over as a test file
## Lessons
- an instruction to a builder must be checked against the project it runs in: --affected needs a configured command
## Plan gaps
- failed first: step 1 Failing tests
## Files touched
- plugin/tests/test_run.py
- plugin/lib/fmlanes.py
- plugin/tests/run.py
- plugin/tests/test_lanes.py
