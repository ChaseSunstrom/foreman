---
id: T-1678
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T21:28:46Z
updated: 2026-10-23T09:16:57Z
base: a5afa311f732637cd3bf5dd3a29afa507e4c476f
base_tree: d6e2c11df0ff8bee2021fb2abb314853fb292ad2
plan0_at: 2026-10-23T09:14:53Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# A slow gate's one failure in a load spike opens an urgent baseline task: rerun just its failing tests first
## Raw request
> T-1597 (Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load) wasn't caught before it shipped: the baseline capture ran once, during a load spike
## Interpretation
fm check reruns a failing gate once only when it took 120 s or less, so the full suite (about 230 s) never gets the flake check, and T-1597 opened an urgent baseline task for two tests that failed once under load. For a slow gate whose output names every failure (unittest dotted names with matching FAILED totals, or pytest node ids matching its summary with no errors), rerun the gate with just those names; all passing makes it a flake (noted, ledgered), anything else stands.
## Assumptions (confidence)
## Acceptance criteria
- [x] a slow gate failing only tests that pass when rerun alone passes as flaky with no baseline task; an output whose names don't cover every failure, or a runner fm can't name tests for, keeps the failure — verify with `python3 plugin/tests/run.py test_cli.Checks`
## Non-goals
## Approach (options → choice → why)
Options: rerun the whole slow gate (another 4 minutes per red); skip baseline capture when the load average is high (hides real failures on busy machines); rerun only the named failing tests when the output vouches the names are complete. Choice: the last; FOREMAN_SLOW_GATE sets the threshold (tests use 0).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then _narrow_rerun and _slow_gate in cmd_check
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_cli.Checks` → ✗ exit 1 · Ran 9 tests in 6.5s (1 classes, 16 at a time; slowest: Checks 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bceb3e4a9c62] (2026-10-23T09:15:10Z)
- `python3 plugin/tests/run.py test_cli.Checks` → ✗ exit 1 · Ran 9 tests in 6.0s (1 classes, 16 at a time; slowest: Checks 6s) / FAILED (1 classes) [ran] [tree bceb3e4a9c62] (2026-10-23T09:15:10Z)
- `python3 plugin/tests/run.py test_cli.Checks` → ✗ exit 1 · Ran 9 tests in 7.0s (1 classes, 16 at a time; slowest: Checks 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8778c97af848] (2026-10-23T09:15:28Z)
- `python3 plugin/tests/run.py test_cli.Checks` → exit 0 · Ran 10 tests in 6.2s (1 classes, 16 at a time; slowest: Checks 6s) / OK [ran] [tree 8778c97af848] (2026-10-23T09:15:28Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_verify_strength test_check_gates` → ✗ exit 1 · run.py: no test matches test_check_gates [ran] [tree 8778c97af848] (2026-10-23T09:15:36Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_verify_strength` → exit 0 · Ran 135 tests in 23.8s (37 classes, 16 at a time; slowest: TaskLifecycle 24s, VerifyStrength 14s, Repeat 10s) / OK [ran] [tree 8778c97af848] (2026-10-23T09:16:04Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.Checks` → exit 0 · Ran 10 tests in 5.9s (1 classes, 16 at a time; slowest: Checks 6s) / OK [ran] [tree 8778c97af848] (2026-10-23T09:16:30Z)
- (audit edge) `self review; check-related suites green` → only exit 1 (not a timeout or crash) with no environment failure class; unittest names must add up to the FAILED totals and pytest's summary must say N failed with no errors, else the whole failure stands; go/cargo names never narrow (test) [tree 8778c97af848] (2026-10-23T09:16:30Z)
- (audit adversary) `self review; check-related suites green` → a gate output that names one failing test but hides another can't pass: the totals must match the names, and the narrowed rerun must itself pass under judged() (zero tests run counts as a failure) [tree 8778c97af848] (2026-10-23T09:16:30Z)
- (audit self) `self review; check-related suites green` → no findings [tree 8778c97af848] (2026-10-23T09:16:30Z)
## Log
- 2026-10-22T21:28:46Z created
- 2026-10-23T09:14:42Z set type=FIX, tier=S, scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-10-23T09:14:42Z set title=A slow gate's one failure in a load spike opens an urgent baseline task: rerun just its failing tests first
- 2026-10-23T09:14:52Z focused
- 2026-10-23T09:16:55Z done
- 2026-10-23T09:16:57Z committed e612083b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1597 [FIX S, done, 1 steps] Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load — lesson: Under heavy machine load the …
- research T-0274-review-1: Verdict: approve with nits.** `note_flakes` can't change the exit code or hide a failure. The findings are a regex false-name problem, one miss…
- research T-1518-review: Verdict:** approve with nits. I found nothing in `--repeat` that forges or weakens evidence. The canary has two real weaknesses. I had no shell, …
- decision 2026-10-22: Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE th…
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Why not caught
the rerun rule skipped every gate over 120 s, which is the full suite: the one gate most likely to meet a load spike
## Plan gaps
- failed first: step 1 failing test, then _narrow_rerun and _slow_gate in cmd_check
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
- plugin/lib/fmcli.py
