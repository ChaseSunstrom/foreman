---
id: T-2480
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T16:16:54Z
updated: 2026-11-01T16:28:39Z
base: 044632b5eafc791c229b8a1af3e94d128d1afb8a
base_tree: c91d3e9a9a80c034df5f046e350b66148f75774b
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T16:16:55Z
plan0_scope: []
verified: strong
---
# Sweep fix tasks are filed unplanned (tier M, no criterion, no regression test), so each needs re-planning and a typed red before it can close
## Raw request
> Sweep fix tasks are filed unplanned (tier M, no criterion, no regression test), so each needs re-planning and a typed red before it can close
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a sweep fix task is tier S with a step, a criterion on its row and a Regression test section — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fill them in _sweep_fixes
## Resume here
## Docs impact
none: MASTER's T-2477 note covers the fix tasks
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_each_red_line_keeps_step_on_sweep_and_a_clean_one_moves_on test_genesis` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: GenesisSweep 0s) / FAILED (1 classes: test_genesis.GenesisSweep) [ran] [tree 11cc9fc369b4] (2026-11-01T16:17:03Z)
- `python3 plugin/tests/run.py -k test_each_red_line_keeps_step_on_sweep_and_a_clean_one_moves_on test_genesis` → ✗ exit 1 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: GenesisSweep 0s) / FAILED (1 classes: test_genesis.GenesisSweep) (start tree + this task's tests) [ran] [tree 76990d33d734] (2026-11-01T16:17:16Z)
- `python3 plugin/tests/run.py -k test_each_red_line_keeps_step_on_sweep_and_a_clean_one_moves_on test_genesis` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisSweep 1s) / OK [ran] [tree 76990d33d734] (2026-11-01T16:17:16Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 12.1s (18 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 9s, GenesisSweep 8s) / OK [ran] [tree 76990d33d734] (2026-11-01T16:17:28Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree 76990d33d734] (2026-11-01T16:17:46Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree 76990d33d734] (2026-11-01T16:23:18Z)
- (audit intent) `main-thread lens pass over the 6-line _sweep_fixes change and its assertions` → a sweep fix task is filed S with a step, a criterion verified by fm genesis sweep N and a Regression test section naming its row, so it closes without re-planning or a typed red [tree 76990d33d734] (2026-11-01T16:23:18Z)
- (audit edge) `main-thread lens pass over the 6-line _sweep_fixes change and its assertions` → an existing open fix task for the row is reused unchanged (the dedupe runs first) [tree 76990d33d734] (2026-11-01T16:23:18Z)
- (audit self) `main-thread lens pass over the 6-line _sweep_fixes change and its assertions` → no findings [tree 76990d33d734] (2026-11-01T16:23:18Z)
## Log
- 2026-11-01T16:16:54Z created
- 2026-11-01T16:16:54Z focused
- 2026-11-01T16:16:55Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T16:17:35Z scope: plugin/lib/fmgenesis.py (_sweep_fixes) and plugin/tests/test_genesis.py only
- 2026-11-01T16:23:43Z done
- 2026-11-01T16:23:46Z committed 21cbd8b7 (2 files)
- 2026-11-01T16:23:55Z guard authorization added: publish
- 2026-11-01T16:28:39Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2479 [FIX S, done, 1 steps] Genesis gen-1 sweep: genesis check is red — gen-1/mission-genesis.md: no cold-read pass for its current text: fm genesi… — lesson: A sweep …
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- T-2433 [FIX M, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: A lane that changes a refusal's reason must grep the suite for the old message…
- decision 2026-11-01: [cites: user steer 2026-11-01: standing rule, the tower advances itself: (2) a red sweep creates its own fix tasks and re-runs when they close; a cl…
## Lessons
- Work a gate files for itself should arrive ready to close, or every loop turn re-plans it
## Plan gaps
- failed first: step 1 red test, then fill them in _sweep_fixes
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
