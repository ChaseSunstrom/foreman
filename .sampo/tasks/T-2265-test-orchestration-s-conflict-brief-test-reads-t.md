---
id: T-2265
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T03:49:01Z
updated: 2026-10-31T03:50:25Z
base: 6d8e5f6432d26157c0d2b2e7efeec94eedcc18a6
base_tree: 9afca3ec4280d39d441ed984a917b752a5d42d81
plan0_at: 2026-10-31T03:49:02Z
plan0_scope: []
verified: strong
---
# test_orchestration's conflict-brief test reads T-2208's resolve steps (cd into the worktree, or message the builder)
## Raw request
> test_orchestration's conflict-brief test reads T-2208's resolve steps (cd into the worktree, or message the builder)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_orchestration.ConflictBrief passes against the new brief text — verify with `cd plugin/tests && python3 -m unittest -q test_orchestration test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] assert the brief names cd <worktree> and the merge step, not git -C
## Resume here
## Docs impact
none: test only
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_orchestration test_lanes` → exit 0 · Ran 46 tests in 22.101s / OK [ran] [tree bb9a2c3ee1a7] (2026-10-31T03:49:37Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_orchestration test_lanes` → exit 0 · Ran 46 tests in 22.027s / OK [ran] [tree bb9a2c3ee1a7] (2026-10-31T03:50:00Z)
- (audit edge) `self: the assertion now checks the brief names cd <worktree> and git merge and no longer says git -C; test_orchestration and test_lanes green` → the test still checks the main checkout is left clean after the aborted merge [tree bb9a2c3ee1a7] (2026-10-31T03:50:00Z)
- (audit self) `self: the assertion now checks the brief names cd <worktree> and git merge and no longer says git -C; test_orchestration and test_lanes green` → no findings [tree bb9a2c3ee1a7] (2026-10-31T03:50:00Z)
## Log
- 2026-10-31T03:49:01Z created
- 2026-10-31T03:49:02Z focused
- 2026-10-31T03:49:37Z scope: plugin/tests/test_orchestration.py
- 2026-10-31T03:50:23Z done
- 2026-10-31T03:50:25Z committed 81432c02 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2208 [FIX S, done, 1 steps] A lane conflict brief tells the main session how to resolve it from where it stands — lesson: Instructions a tool writes for its operator m…
- T-1136 [FIX S, done, 1 steps] Fm lane rm right after a conflicted fm lane merge removes the worktree and the builder rec — lesson: A cleanup verb must refuse while the t…
- T-2047 [FIX S, done, 2 steps] fm lib check lints the checkout it runs in, not the installed plugin's cards — lesson: A check that reads the plugin's own files must resol…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–2 steps
## Regression test
the existing test_orchestration.ConflictBrief went red in ship62's scratch tree against T-2208's new brief text; updated to assert the new steps
## Why not caught
T-2208's builder ran test_lanes only; the brief text is also asserted in test_orchestration (captured as T-2255's pattern: run every test file naming the changed text)
## Lessons
- Before changing a user-facing string, grep the tests for it; two test files asserted the conflict brief
## Files touched
- plugin/tests/test_orchestration.py
