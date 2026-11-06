---
id: T-2460
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T08:21:31Z
updated: 2026-11-01T08:33:13Z
base: 541ceedaa40883dc1b2d19aac476afed5369cf7a
base_tree: 21f264e11cfeecb23720e6f7c1715e9869bd93dd
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T08:21:32Z
plan0_scope: []
verified: strong
---
# Round first holds the self-improvement (friction) pass too: with --round-first on, fm next offered fm friction during round 1, which the user's steer bars
## Raw request
> Round first holds the self-improvement (friction) pass too: with --round-first on, fm next offered fm friction during round 1, which the user's steer bars
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with fm drive --round-first on and the round open, fm next doesn't offer the friction pass (it says it waits for the round); with the switch off, or the round done, it is offered as before — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the round check before the friction pass in fmcore._next_for
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k test_the_friction_pass_waits` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: RoundFirst 0s) / FAILED (1 classes: test_core.RoundFirst) [ran] [tree fb3e72aca3c7] (2026-11-01T08:21:50Z)
- (step 2) `python3 plugin/tests/run.py test_core test_hooks test_friction` → exit 0 · Ran 391 tests in 41.6s (61 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree 89312189884e] (2026-11-01T08:22:51Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 133 tests in 6.0s (27 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 89312189884e] (2026-11-01T08:22:57Z)
- `python3 plugin/tests/run.py test_core -k test_the_friction_pass_waits` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: RoundFirst 0s) / FAILED (1 classes: test_core.RoundFirst) (start tree + this task's tests) [ran] [tree 89312189884e] (2026-11-01T08:23:00Z)
- `python3 plugin/tests/run.py test_core -k test_the_friction_pass_waits` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: RoundFirst 0s) / OK [ran] [tree 89312189884e] (2026-11-01T08:23:00Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 133 tests in 6.0s (27 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 89312189884e] (2026-11-01T08:28:22Z)
- (audit self) `self: fm check exit 0; red→green test (the friction pass is offered with the switch off and waits, named, with --round-first on during the open round); fm task prove proved; fm next on this project no longer offers it` → no findings [tree 89312189884e] (2026-11-01T08:28:22Z)
## Log
- 2026-11-01T08:21:31Z created
- 2026-11-01T08:21:32Z focused
- 2026-11-01T08:21:32Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T08:23:00Z scope: plugin/lib/fmcore.py (_round_first, the friction branch) and plugin/tests/test_core.py (the test)
- 2026-11-01T08:28:42Z done
- 2026-11-01T08:28:44Z committed 8048b07b (2 files)
- 2026-11-01T08:28:56Z guard authorization added: publish
- 2026-11-01T08:33:13Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2327 [FEATURE M, done, 3 steps] Enforce the user's 2026-10-31 steers as automatic checks: session arms of fm exam long run wait for the end-of-run exam, fm next offers…
- decision 2026-11-01: [revisited: T-2450 (the secrets finder reads a date as a credential)] [cites: user steer 2026-10-31: finish round 1 completely, in order; no new mai…
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- T-0435 [FEATURE M, done, 2 steps] fm friction reads every project's friction, labelled by project — lesson: Aggregated signals need their source kept: a line without its…
- similar past tasks were L: consider --tier L
## Lessons
- Turning one brake off (pace) exposed a path another rule should have held: check every brake's paths when a steer changes one
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
