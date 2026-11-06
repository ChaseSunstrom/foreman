---
id: T-0309
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T18:28:00Z
updated: 2026-10-04T18:30:04Z
base: 8ae2e897713ff587ebdc634d1166fba599adbac4
base_tree: 583266aa24898473b1756a6f7b3c946f3ad84602
verified: strong
---
# fm bench: a replay stopped at its budget cap is inconclusive, not a failed judgement
## Raw request
> fm bench: a replay stopped at its budget cap is inconclusive, not a failed judgement
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a run whose cost reaches --budget reports a budget-cap error and pays no judge — verify with `python3 plugin/tests/run.py -p test_bench_family.py -k Judged`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then flag capped runs in fmbench._session
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_bench_family.py -k Judged` → ✗ exit 1 · Ran 5 tests in 7.8s (1 classes, 16 at a time; slowest: Judged 8s) / FAILED (1 classes) [ran] [tree 0d53c9977ab0] (2026-10-04T18:28:15Z)
- (step 1) `python3 plugin/tests/run.py -p test_bench_family.py -k Judged` → exit 0 · Ran 5 tests in 7.9s (1 classes, 16 at a time; slowest: Judged 8s) / OK [ran] [tree c96141de685c] (2026-10-04T18:28:36Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.1    32.5     150  [0] / SessionEnd                  29.3    30.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:59 UTC; python3 plugin/tests/run.py → exit 0 · Ran 823 tests in [ran] [tree 5397a2eac0cd] (2026-10-04T18:29:56Z)
- (ac 1) `python3 plugin/tests/run.py -p test_bench_family.py -k Judged` → exit 0 · Ran 5 tests in 7.9s (1 classes, 16 at a time; slowest: Judged 8s) / OK [ran] [tree 5397a2eac0cd] (2026-10-04T18:30:04Z)
- (audit intent) `self: red→green Judged (a capped run was judged and passed; now an inconclusive error, no judge call); bench, bench family, night and evolve suites pass` → the court run's R-T-0205 hit its $0.50 cap and was scored 1/5 as a finished attempt [tree 5397a2eac0cd] (2026-10-04T18:30:04Z)
- (audit edge) `self: red→green Judged (a capped run was judged and passed; now an inconclusive error, no judge call); bench, bench family, night and evolve suites pass` → claude -p stops after the turn that crosses the cap, so cost >= budget means it was cut off; a run that ends exactly at the cap counts as capped (raise --budget to rerun); soak turns use the same runner [tree 5397a2eac0cd] (2026-10-04T18:30:04Z)
- (audit self) `self: red→green Judged (a capped run was judged and passed; now an inconclusive error, no judge call); bench, bench family, night and evolve suites pass` → no findings [tree 5397a2eac0cd] (2026-10-04T18:30:04Z)
## Log
- 2026-10-04T18:28:00Z created
- 2026-10-04T18:28:01Z focused
- 2026-10-04T18:30:04Z done
- 2026-10-04T18:30:04Z committed 59b03fd (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- T-0298 [FEATURE M, done, 2 steps] Unattended checks: fm bench stranger (a newcomer session from the README) and fm night (budgeted background work while … — lesson: A bu…
- research T-0298-review-1: Findings
- T-0280 [FEATURE M, done, 5 steps] Bench family: judged cases, plugin duels, version replays, regression court, shadow-user soak — lesson: Git run after a bypass-mode ses…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–5 steps
## Lessons
- A capped run is missing data, not a failed attempt: say so before paying a judge
## Files touched
- plugin/tests/test_bench_family.py
- plugin/lib/fmbench.py
- CHANGELOG.md
