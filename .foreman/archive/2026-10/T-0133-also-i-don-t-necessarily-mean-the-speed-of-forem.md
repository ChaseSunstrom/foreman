---
id: T-0133
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:52:05Z
updated: 2026-10-03T05:17:10Z
base: 6e552055c6ee28419b125a992dadd04ce161f28e
base_tree: d8d4135d76773f5ec2f45346b57786457e204bb6
verified: ok
---
# Agents feel slow: parallel test runner for the gate, measured before and after
## Raw request
> also I don't necessarily mean the speed of foreman itself, but agents using foreman, it feels slow, i dont know
## Interpretation
User: not fm's own speed, agents using Foreman feel slow. Measured this session: every task close runs fm check at ~175 s, almost all of it the Python suite (535 tests, one process, 16 cores idle); I ran it 12+ times today (~35 min of waiting).
## Assumptions (confidence)
## Acceptance criteria
- [x] the suite passes through the parallel runner and the gate is at least 3x faster — verify with `python3 plugin/tests/run.py`
## Non-goals
## Approach (options → choice → why)
Options: (a) a stdlib runner that runs each test module in its own process across the cores (tests already isolate FOREMAN_HOME per test) and prints a unittest-style summary; the gate uses it; (b) gates by changed paths (T-0126). Choice (a) first: it speeds every task with no risk of skipping a needed check; (b) stays queued for the rest. Measure: before ~150 s for the suite.
## Risks and rollback
## Execution prompt
## Steps
1. [x] baseline timing
2. [x] plugin/tests/run.py
3. [x] gate uses it; measure fm check
## Resume here
## Docs impact
README.md, MASTER.md, CHANGELOG.md: run.py
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -q` → serial baseline 154 s (535 tests) (2026-10-03T05:13:21Z)
- (step 2) `python3 plugin/tests/run.py` → exit 0 · Ran 537 tests in 19.4s (105 classes, 16 at a time; slowest: Stop 19s, TaskLifecycle 18s, VerifyStrength 14s) / OK [ran] [tree 0a8f13d1a4ad] (2026-10-03T05:16:00Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 0 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.8    33.6     150  [0] / SessionEnd                  28.4    29.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.83s]; python3 plugin/tests/run.py → exit 0 · Ran 537 tests in 19.1s (1 [ran] [tree 0a8f13d1a4ad] (2026-10-03T05:16:41Z)
- (ac 1) `python3 plugin/tests/run.py` → exit 0 · Ran 537 tests in 19.4s (105 classes, 16 at a time; slowest: Stop 19s, TaskLifecycle 17s, VerifyStrength 13s) / OK [ran] [tree 0a8f13d1a4ad] (2026-10-03T05:17:10Z)
- (audit intent) `four parallel runs all OK (no timing flakes); same tests as discover (537)` → agents wait on the gate at every close; it is now 41 s instead of 176 s [tree 0a8f13d1a4ad] (2026-10-03T05:17:10Z)
- (audit edge) `four parallel runs all OK (no timing flakes); same tests as discover (537)` → timing-sensitive tests (ideas concurrency, hook budgets) passed under full load four times; a class that fails prints its whole report; zero tests found exits 1 [tree 0a8f13d1a4ad] (2026-10-03T05:17:10Z)
## Log
- 2026-10-03T04:52:05Z created
- 2026-10-03T05:10:20Z planned from capture
- 2026-10-03T05:10:20Z focused
- 2026-10-03T05:17:10Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Profiling (skills/playbooks/references/perf/profiling.md)
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- T-0116 [FEATURE M, done, 4 steps] Size words with meaning: typical time per type and size, time on task, gate ETA — lesson: Medians need a floor on samples; with fewer t…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- the similar finished task took 4 steps
## Measurements
Before: python suite 154 s serial (535 tests); fm check 176 s. After: run.py 17.8-19.5 s over four runs (537 tests, 105 classes, 16 cores) = 8.5x; fm check 40.4 s = 4.3x. Slowest classes now: Stop 19 s, TaskLifecycle 17 s, VerifyStrength 13 s.
## Lessons
- Measure the wait before optimising: one serial test process on a 16-core machine was the biggest agent-visible delay
## Files touched
- plugin/tests/run.py
- README.md
- MASTER.md
- CHANGELOG.md
