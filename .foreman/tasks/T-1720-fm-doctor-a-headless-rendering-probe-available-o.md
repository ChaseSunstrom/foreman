---
id: T-1720
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T02:01:21Z
updated: 2026-10-23T02:01:58Z
base: 177c6ce8fb07e6dd16986f28b0903437d7e7cabb
base_tree: 27cc290df6b7fbdc366e43324e396e760bd09283
plan0_at: 2026-10-23T02:01:29Z
plan0_scope: []
verified: strong
---
# fm doctor: a headless-rendering probe (available, or why not)
## Raw request
> fm doctor: a headless-rendering probe (available, or why not)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor reports headless rendering available or why not — verify with `python3 plugin/tests/run.py test_doctor.Headless`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests
2. [x] probe
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:01:31Z)
- (step 2) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:01:32Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:01:33Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor.Headless` → exit 0 · Ran 4 tests in 0.5s (1 classes, 16 at a time; slowest: Headless 0s) / OK [ran] [tree 5946eb90ec00] (2026-10-23T02:01:35Z)
- (audit intent) `self-review of the probe (built under T-1638, merged): fmshot.chrome() reused, a 5 s --version probe with stdin closed, output cleaned and cut, always PASS; live fm doctor --json shows the available row` → fm doctor says whether headless rendering is available and why not, never failing on an optional browser [tree 5946eb90ec00] (2026-10-23T02:01:35Z)
- (audit edge) `self-review of the probe (built under T-1638, merged): fmshot.chrome() reused, a 5 s --version probe with stdin closed, output cleaned and cut, always PASS; live fm doctor --json shows the available row` → no browser, an unusable FOREMAN_CHROME, a start that fails or times out each get their own reason [tree 5946eb90ec00] (2026-10-23T02:01:35Z)
- (audit self) `self-review of the probe (built under T-1638, merged): fmshot.chrome() reused, a 5 s --version probe with stdin closed, output cleaned and cut, always PASS; live fm doctor --json shows the available row` → no findings [tree 5946eb90ec00] (2026-10-23T02:01:35Z)
- (audit intent) `self-review of the probe (built under T-1638, merged): fmshot.chrome() reused, a 5 s --version probe with stdin closed, output cleaned and cut, always PASS; live fm doctor --json shows the available row` → fm doctor says whether headless rendering is available and why not, never failing on an optional browser [tree 5946eb90ec00] (2026-10-23T02:01:50Z)
- (audit edge) `self-review of the probe (built under T-1638, merged): fmshot.chrome() reused, a 5 s --version probe with stdin closed, output cleaned and cut, always PASS; live fm doctor --json shows the available row` → no browser, an unusable FOREMAN_CHROME, a start that fails or times out each get their own reason [tree 5946eb90ec00] (2026-10-23T02:01:50Z)
- (audit self) `self-review of the probe (built under T-1638, merged): fmshot.chrome() reused, a 5 s --version probe with stdin closed, output cleaned and cut, always PASS; live fm doctor --json shows the available row` → no findings [tree 5946eb90ec00] (2026-10-23T02:01:50Z)
## Log
- 2026-10-23T02:01:21Z created
- 2026-10-23T02:01:21Z redo of T-1638: takes over its start point and edited files
- 2026-10-23T02:01:28Z focused
- 2026-10-23T02:01:34Z set scope=['plugin/lib/fmdoctor.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md']
- 2026-10-23T02:01:49Z scope: plugin/tests/test_shot.py was touched in the lane's history (the Doctor class added, then moved to test_doctor.py per review); its content is back to build's
- 2026-10-23T02:01:58Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1638 [FEATURE S, dropped, 2 steps] fm doctor: a headless-rendering probe (available, or why not)
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1531 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames,
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Lessons
- Probe an optional tool with its cheapest call (--version) in doctor; leave the full launch to the command that needs it
## Files touched
- plugin/tests/test_shot.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- plugin/tests/test_doctor.py
