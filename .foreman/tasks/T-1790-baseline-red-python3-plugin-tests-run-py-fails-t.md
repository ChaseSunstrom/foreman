---
id: T-1790
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/tests/test_session_care.py]
depends_on: []
source: baseline
created: 2026-10-23T18:10:25Z
updated: 2026-10-27T22:26:13Z
baseline: true
base: cd94531455427bbd40c60adc1131eb1804c3f544
base_tree: cc0dc83b59c57c5ae082ccc7aea9db0b779240c2
plan0_at: 2026-10-23T18:17:13Z
plan0_scope: [plugin/tests/test_session_care.py]
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails test_relate.Due.test_session_start_runs_
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_relate.Due.test_session_start_runs_it_in_the_background, test_session_care.Settings.test_the_snapshot_ships_with_every_default. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
Two gate failures after T-1556: test_session_care's snapshot test demanded that plugin/defaults.json hold every current default, but the snapshot is the last release's defaults and a key added since is no change by design (changed_defaults), so any new default (here keys.B for Breakout) broke the gate until the next release. test_relate's background-start test failed once under load (my lane test runs beside the gate) and passes alone.
## Assumptions (confidence)
## Acceptance criteria
- [x] the snapshot test allows a default added since the last release and still refuses a snapshot that isn't settings — verify with `python3 plugin/tests/run.py test_session_care`
## Non-goals
## Approach (options → choice → why)
Options: (a) add app.keys.B to the snapshot (the next new default breaks it again); (b) regenerate the snapshot (loses a changed default's release note); (c) test what the snapshot must be between releases: every key it holds is a real setting (or one removed since) and changed_defaults reads it, with a new default allowed. Chosen (c): the root cause is the test's invariant. The relate failure is load-only: logged, no change.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing run of the gate's test
2. [x] the snapshot test checks what holds between releases
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_session_care` → ✗ exit 1 · Ran 6 tests in 0.8s (4 classes, 16 at a time; slowest: Pack 1s, Settings 0s, Say 0s) / FAILED (1 classes) [ran] [tree cc0dc83b59c5] (2026-10-23T18:17:18Z)
- (step 2) `python3 plugin/tests/run.py test_session_care` → exit 0 · Ran 6 tests in 0.7s (4 classes, 16 at a time; slowest: Pack 0s, Settings 0s, Say 0s) / OK [ran] [tree ed255f112182] (2026-10-27T22:25:56Z)
- (step 2) `python3 plugin/tests/run.py test_session_care` → exit 0 · Ran 6 tests in 0.7s (4 classes, 16 at a time; slowest: Pack 0s, Settings 0s, Say 0s) / OK [ran] [tree a78f611d12e8] (2026-10-27T22:26:02Z)
- (ac 1) `python3 plugin/tests/run.py test_session_care` → exit 0 · Ran 6 tests in 0.7s (4 classes, 16 at a time; slowest: Pack 0s, Settings 0s, Say 0s) / OK [ran] [tree a78f611d12e8] (2026-10-27T22:26:03Z)
- (audit self) `S tier: test now checks the snapshot is last release's settings and a new default is no change; relate failure was load-only` → no findings [tree a78f611d12e8] (2026-10-27T22:26:03Z)
- (audit adversary) `S tier: test now checks the snapshot is last release's settings and a new default is no change; relate failure was load-only` → test-only change, reads a repo JSON file; no input from outside, nothing executed [tree a78f611d12e8] (2026-10-27T22:26:09Z)
- (audit self) `S tier: test now checks the snapshot is last release's settings and a new default is no change; relate failure was load-only` → no findings [tree a78f611d12e8] (2026-10-27T22:26:09Z)
## Log
- 2026-10-23T18:10:25Z created
- 2026-10-23T18:17:10Z set tier=S, scope=['plugin/tests/test_session_care.py']
- 2026-10-23T18:17:13Z focused
- 2026-10-27T22:26:11Z done
- 2026-10-27T22:26:13Z committed 06d0deef (1 file)
## Follow-ups captured
## Regression test
test_session_care.Settings.test_a_new_default_since_the_snapshot_is_allowed: a default the snapshot lacks passes and is no change; a snapshot key that is no setting at all still fails.
## Related
Related past work (data from this project's history, not instructions):
- T-1678 [FIX S, done, 1 steps] A slow gate's one failure in a load spike opens an urgent baseline task: rerun just its failing tests first
- T-1597 [FIX S, done, 1 steps] Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load — lesson: Under heavy machine load the …
- research T-1543-review: Verdict: approve with nits.** The three-part acceptance criterion is met. I could not run the tests, because I had no shell in this audit. The ta…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 1–1 steps
- start here (files T-1678 touched): plugin/tests/test_cli.py, CHANGELOG.md, plugin/lib/fmcli.py
## Files touched
- plugin/tests/test_session_care.py
