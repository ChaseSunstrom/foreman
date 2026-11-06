---
id: T-0833
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-14T18:41:25Z
updated: 2026-10-14T19:45:18Z
base: 3ea18f4701a10a912e3597d51d7cb18c2b3821f4
base_tree: aa97f7e4c98e24ad71c04017cae8daa09248f79e
verified: strong
---
# Fm lane rm: offer to delete the lane's ignored build output (target/, voltc/target/) itsel
## Raw request
> fm lane rm: offer to delete the lane's ignored build output (target/, voltc/target/) itself (or a --clean flag), so removing a merged builder lane doesn't need a throwaway task to authorize git clean -fdX; hit twice on 2026-10-14 (T-0421 and T-0412's lane)
## Interpretation
fm lane rm refuses a lane whose only leftovers are ignored build output (target/, voltc/target/) because _CACHE knows test and package caches, not build dirs; twice on 10-14 a throwaway task was needed to authorize git clean -fdX. A lane worktree starts with no ignored files, so a build dir in it was made by the lane's own runs and is rebuilt on the next build. Count common build-output dirs (target, build, dist, zig-out, zig-cache, cmake-build-*) as caches; ignored files like .env still refuse.
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane whose only ignored leftovers are target/ and voltc/target/ is removed; one with an ignored .env still refuses — verify with `python3 plugin/tests/run.py test_builder`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then build dirs in _CACHE
## Resume here
## Docs impact
none: refusal wording unchanged
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 20 tests in 5.2s (6 classes, 16 at a time; slowest: Contract 5s, Brief 3s, Flow 1s) / OK [ran] [tree 049d083d9143] (2026-10-14T19:43:20Z)
- `python3 plugin/tests/run.py test_builder` → ✗ exit 1 · Ran 20 tests in 5.2s (6 classes, 16 at a time; slowest: Contract 5s, Brief 3s, Flow 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 049d083d9143] (2026-10-14T19:43:31Z)
- `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 20 tests in 5.2s (6 classes, 16 at a time; slowest: Contract 5s, Brief 3s, Flow 1s) / OK [ran] [tree 049d083d9143] (2026-10-14T19:43:31Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.0    35.2     150  [0] / SessionEnd                  30.4    31.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 049d083d9143] (2026-10-14T19:45:07Z)
- (ac 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 20 tests in 5.3s (6 classes, 16 at a time; slowest: Contract 5s, Brief 3s, Flow 1s) / OK [ran] [tree 049d083d9143] (2026-10-14T19:45:17Z)
- (audit edge) `self: build dirs join the lane cache list, and lane rm asks git for the matching ignored paths so a folder holding only voltc/target/ isn't reported as voltc/` → an ignored .env (or any ignored path that isn't a known cache or build dir) still refuses; a tracked folder named build/ is never in the ignored list, so it's untouched by this rule [tree 049d083d9143] (2026-10-14T19:45:17Z)
- (audit self) `self: build dirs join the lane cache list, and lane rm asks git for the matching ignored paths so a folder holding only voltc/target/ isn't reported as voltc/` → no findings [tree 049d083d9143] (2026-10-14T19:45:17Z)
## Log
- 2026-10-14T18:41:25Z created
- 2026-10-14T19:42:28Z focused
- 2026-10-14T19:45:18Z done
- 2026-10-14T19:45:18Z committed fc60fd9 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- decision 2026-09-26: fm sync keeps the automatic import at session start and before fm commands: imported content can't grant, mark runs, count as audits or take focus, …
## Lessons
- git status --ignored collapses a folder whose content is all ignored; --ignored=matching shows the paths a rule actually matched
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
