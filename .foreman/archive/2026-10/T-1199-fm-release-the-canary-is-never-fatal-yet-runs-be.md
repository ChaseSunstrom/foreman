---
id: T-1199
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:03:31Z
updated: 2026-10-16T14:09:05Z
base: d0b47da07e86a1eb05d2e595a0869e72437fb744
base_tree: d6c3a889d6b585cf567a8f0a1e57d2c523156c6c
plan0_at: 2026-10-16T14:05:08Z
plan0_scope: []
verified: strong
---
# fm release runs the canary after the push, its sentinels in parallel
## Raw request
> fm release: the canary is never fatal yet runs before the push, one sentinel per project in turn (12 projects, ~3 min each held the 1.2.34 push ~35 min); run the sentinels in parallel (cap 4) and after the push, reporting only
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] STEPS orders canary after push and round (still reported, never fatal); the canary runs up to 4 sentinels at once with each project's line printed in project order; test_release's canary test and the step-order tests pass — verify with `python3 plugin/tests/run.py test_release`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test: canary is listed after push in --dry-run and a stub sentinel that sleeps 1 s in 4 projects finishes in under 3 s
2. [x] Move canary in STEPS; run sentinels with a ThreadPoolExecutor(4), printing results in order
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_release` → ✗ exit 1 · Ran 28 tests in 16.5s (5 classes, 16 at a time; slowest: BoardVerbs 16s, Release 12s, Release 1s) / FAILED (1 classes) [ran] [tree 8929dc664b7e] (2026-10-16T14:06:35Z)
- (step 2) `python3 plugin/tests/run.py test_release test_release_py` → ✗ exit 1 · Ran 28 tests in 21.3s (5 classes, 16 at a time; slowest: BoardVerbs 21s, Release 19s, Release 3s) / FAILED (1 classes) [ran] [tree 8929dc664b7e] (2026-10-16T14:06:57Z)
- (step 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 28 tests in 10.5s (5 classes, 16 at a time; slowest: Release 10s, BoardVerbs 10s, Release 2s) / OK [ran] [tree 8929dc664b7e] (2026-10-16T14:07:42Z)
- (step 2) `python3 plugin/tests/run.py test_release test_release_py` → exit 0 · Ran 28 tests in 8.8s (5 classes, 16 at a time; slowest: Release 9s, BoardVerbs 8s, Release 2s) / OK [ran] [tree 8929dc664b7e] (2026-10-16T14:07:51Z)
- (ac 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 28 tests in 10.3s (5 classes, 16 at a time; slowest: BoardVerbs 10s, Release 8s, Release 1s) / OK [ran] [tree 8929dc664b7e] (2026-10-16T14:08:17Z)
- `python3 plugin/tests/run.py test_release test_release_py` → exit 0 · Ran 28 tests in 10.1s (5 classes, 16 at a time; slowest: BoardVerbs 10s, Release 8s, Release 1s) / OK [ran] [tree 8929dc664b7e] (2026-10-16T14:08:17Z)
- (audit self) `self: canary moved after push and round (it never fails a release, so ordering can't hide a failure); ThreadPoolExecutor(4) with pool.map keeps project order; each sentinel keeps its own 1800 s timeout and exceptions are caught per project, so one hung project still can't fail the release; output flushed so a redirected log shows progress` → no findings [tree 8929dc664b7e] (2026-10-16T14:08:17Z)
## Log
- 2026-10-16T14:03:31Z created
- 2026-10-16T14:04:00Z planned from capture
- 2026-10-16T14:05:08Z focused
- 2026-10-16T14:07:56Z scope: CHANGELOG line
- 2026-10-16T14:09:04Z done
- 2026-10-16T14:09:05Z committed 22653d77 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0492 [FEATURE M, done, 0 steps] Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
- T-0562 [FEATURE M, dropped, 0 steps] Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
- T-0678 [FEATURE M, done, 3 steps] Milestone: Features — Releases and delivery — lesson: A release done by hand four times in a day is a script; the script is the checkli…
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
- similar past tasks were M: consider --tier M
- similar finished tasks took 0–3 steps
## Measurements
Before: the canary ran before the push, one project at a time; in the 1.2.34 run it had spent more than 3.5 minutes on the first two of 12 projects (foreman, volt) when it was stopped, so the push waited an estimated 20-35 minutes for a step that never fails. After: the push and round close come first (canary time before the push: 0); sentinels run 4 at a time, so 12 projects take about 3 rounds instead of 12. Test proof: test_the_canary_runs_sentinels_side_by_side_and_reports_in_project_order shows at least two 0.5 s stub sentinels overlapping and lines in project order.
## Plan gaps
- failed first: step 1 Test: canary is listed after push in --dry-run and a stub sentinel that sleeps 1 s in 4 projects fi…
- failed first: step 2 Move canary in STEPS; run sentinels with a ThreadPoolExecutor(4), printing results in order
## Files touched
- plugin/tests/test_release.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
