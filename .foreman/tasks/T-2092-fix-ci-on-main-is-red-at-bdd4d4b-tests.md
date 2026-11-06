---
id: T-2092
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T04:18:04Z
updated: 2026-10-30T10:30:32Z
base: 7f3fc3f345b859a9f7135fd1b700c4e9439db3d7
base_tree: ec6493cd3d8ae78567ff4b0750323fa90a0b0686
plan0_at: 2026-10-30T04:50:53Z
plan0_scope: []
verified: ok
---
# CI flake: test_projects.Follow failed on one of six runners at bdd4d4b
## Raw request
> FIX: CI on main is red at bdd4d4b (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/foreman/commit/bdd4d4b7db8269be37c7f8fcc49cf713d27447c6
> CI-red: bdd4d4b7db8269be37c7f8fcc49cf713d27447c6
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_projects.Follow passes locally three runs in a row — verify with `python3 plugin/tests/run.py test_projects`
- [x] the last finished main CI run is green — verify with `gh run list --branch main --workflow tests --status completed --limit 1 --json conclusion --jq '.[0].conclusion' | grep -qx success`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce locally (three runs of test_projects.Follow)
2. [x] confirm on the next main CI run; if Follow fails again, widen its timing bounds
## Resume here
<!-- auto -->
- 2026-10-30T04:51:13Z step 2/2: confirm on the next main CI run; if Follow fails again, widen its timing bounds
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_projects test_projects test_projects` → exit 0 · Ran 7 tests in 1.0s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 0s) / OK [ran] [tree b33f8a3d2bf5] (2026-10-30T04:50:56Z)
- (step 2) `gh run list --branch main --workflow tests --limit 1 --json conclusion --jq '.[0].conclusion'` → ✗ exit 1 · couldn't fetch workflows for ChaseSunstrom/foreman: HTTP 403: API rate limit exceeded for 173.252.145.9. (But here's the good news: Authenticated requests get a higher rate limit. Check out the docume [ran] [tree b33f8a3d2bf5] (2026-10-30T04:50:56Z)
- (step 2) `fm ci-watch --commit 1a78a3f (main CI after bdd4d4b)` → CI green (gh API rate-limited here, so the ci-watch result stands) [tree b33f8a3d2bf5] (2026-10-30T04:51:02Z)
- (ac 1) `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 7 tests in 1.3s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 1s) / OK [ran] [tree b33f8a3d2bf5] (2026-10-30T04:51:06Z)
- (ac 2) `gh run list --branch main --workflow tests --limit 1 --json conclusion --jq '.[0].conclusion' | grep -qx success` → ✗ exit 1 · couldn't fetch workflows for ChaseSunstrom/foreman: HTTP 403: API rate limit exceeded for 173.252.145.9. (But here's the good news: Authenticated requests get a higher rate limit. Check out the docume [ran] [tree b33f8a3d2bf5] (2026-10-30T04:51:06Z)
- (step 2) `gh run list --branch main --workflow tests --limit 1 --json conclusion --jq '.[0].conclusion'` → ✗ exit 1 · couldn't fetch workflows for ChaseSunstrom/foreman: HTTP 403: API rate limit exceeded for 173.252.145.9. (But here's the good news: Authenticated requests get a higher rate limit. Check out the docume [ran] [tree b33f8a3d2bf5] (2026-10-30T04:51:06Z)
- (step 2) `gh run list --branch main --workflow tests --status completed --limit 10 --json conclusion --jq '[.[].conclusion] | unique' | grep -qx '\["success"\]'` → exit 0 · (no output) [ran] [tree ec6493cd3d8a] (2026-10-30T10:26:10Z)
- (ac 2) `gh run list --branch main --workflow tests --limit 1 --json conclusion --jq '.[0].conclusion' | grep -qx success` → ✗ exit 1 · (no output) [ran] [tree ec6493cd3d8a] (2026-10-30T10:30:19Z)
- `gh run list --branch main --workflow tests --status completed --limit 10 --json conclusion --jq '[.[].conclusion] | unique' | grep -qx '\["success"\]'` → exit 0 · (no output) [ran] [tree ec6493cd3d8a] (2026-10-30T10:30:19Z)
- (ac 2) `gh run list --branch main --workflow tests --status completed --limit 1 --json conclusion --jq '.[0].conclusion' | grep -qx success` → exit 0 · (no output) [ran] [tree ec6493cd3d8a] (2026-10-30T10:30:30Z)
- `gh run list --branch main --workflow tests --status completed --limit 10 --json conclusion --jq '[.[].conclusion] | unique' | grep -qx '\["success"\]'` → exit 0 · (no output) [ran] [tree ec6493cd3d8a] (2026-10-30T10:30:30Z)
- (audit self) `self: the flake did not recur in 10 finished main CI runs since; no code changed` → no findings [tree ec6493cd3d8a] (2026-10-30T10:30:30Z)
## Log
- 2026-10-30T04:18:04Z created
- 2026-10-30T04:25:42Z planned from capture
- 2026-10-30T04:50:53Z focused
- 2026-10-30T04:51:13Z CI green per fm ci-watch; gh API rate-limited (unauthenticated) — retry the ac 2 evidence after the hourly reset
- 2026-10-30T04:51:20Z paused: focus moved to T-2095
- 2026-10-30T10:30:08Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T10:30:08Z focused
- 2026-10-30T10:30:27Z steer: criterion 2 reads the last finished run (an in-progress run has no conclusion yet)
- 2026-10-30T10:30:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2014 [FIX M, dropped, 0 steps] FIX: CI on main is red at 104c441 (tests)
- T-1816 [FIX M, dropped, 0 steps] FIX: CI on main is red at eba6705 (tests)
- T-1842 [FIX S, done, 2 steps] FIX: CI tests time out: split the suite into 2 shards per job
- decision 2026-10-30: T-2079: no spike lane; the unknown (six renderers from one spec) is proven by the red tests themselves in step 1-2
- the similar finished task took 2 steps
- start here (files T-1842 touched): plugin/tests/test_run.py, plugin/tests/run.py, .github/workflows/test.yml, CHANGELOG.md
## Regression test
none: a one-off runner flake at bdd4d4b; three local runs and the 10 finished main runs since are green, so there is nothing red to prove
## Lessons
- A single-runner CI flake that stays green for 10 runs closes on the record, without widening timing bounds speculatively
## Plan gaps
- failed first: step 2 confirm on the next main CI run; if Follow fails again, widen its timing bounds
