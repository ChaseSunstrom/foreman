---
id: T-1829
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T09:53:03Z
updated: 2026-10-28T09:54:25Z
base: b734071b2fa3325e0bd124b827eea5abb87ddf90
base_tree: 9379b93449288fff01dcf2b280c1cc446971bcff
plan0_at: 2026-10-28T09:53:07Z
plan0_scope: []
verified: strong
---
# fm release-check keeps FOREMAN_DOCTOR_BENCH so the suite's release-check run skips the hook timing bench (flaky under parallel load)
## Raw request
> fm release-check keeps FOREMAN_DOCTOR_BENCH so the suite's release-check run skips the hook timing bench (flaky under parallel load)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] release-check's child env keeps FOREMAN_DOCTOR_BENCH and the release-check test sets it to 0 — verify with `python3 plugin/tests/run.py test_board_verbs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test on the child env, then keep the variable
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_board_verbs.BoardVerbs.test_release_check_child_env_keeps_only_the_bench_switch` → red as expected (exit 1) · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BoardVerbs 0s) / FAILED (1 classes) [ran] [tree 85e2bdc191d5] (2026-10-28T09:53:22Z)
- (step 1) `python3 plugin/tests/run.py test_board_verbs` → exit 0 · Ran 8 tests in 8.7s (1 classes, 16 at a time; slowest: BoardVerbs 8s) / OK [ran] [tree c0f29d16eaf3] (2026-10-28T09:53:40Z)
- `python3 plugin/tests/run.py test_board_verbs.BoardVerbs.test_release_check_child_env_keeps_only_the_bench_switch` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: BoardVerbs 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c0f29d16eaf3] (2026-10-28T09:53:56Z)
- `python3 plugin/tests/run.py test_board_verbs.BoardVerbs.test_release_check_child_env_keeps_only_the_bench_switch` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BoardVerbs 0s) / OK [ran] [tree c0f29d16eaf3] (2026-10-28T09:53:56Z)
- (ac 1) `python3 plugin/tests/run.py test_board_verbs` → exit 0 · Ran 8 tests in 8.5s (1 classes, 16 at a time; slowest: BoardVerbs 8s) / OK [ran] [tree c0f29d16eaf3] (2026-10-28T09:54:13Z)
- (audit edge) `self: a two-line env change plus a pure env test; the child still drops FOREMAN_INHIBITED, CLAUDE* and GIT_*` → unset FOREMAN_DOCTOR_BENCH keeps today's behaviour (a newcomer's release-check still measures) [tree c0f29d16eaf3] (2026-10-28T09:54:13Z)
- (audit operator) `self: a two-line env change plus a pure env test; the child still drops FOREMAN_INHIBITED, CLAUDE* and GIT_*` → one env key per release-check, no cost at scale [tree c0f29d16eaf3] (2026-10-28T09:54:13Z)
- (audit self) `self: a two-line env change plus a pure env test; the child still drops FOREMAN_INHIBITED, CLAUDE* and GIT_*` → no findings [tree c0f29d16eaf3] (2026-10-28T09:54:13Z)
## Log
- 2026-10-28T09:53:03Z created
- 2026-10-28T09:53:06Z focused
- 2026-10-28T09:54:24Z done
- 2026-10-28T09:54:25Z committed a32aa679 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1379 [FIX M, done, 3 steps] test_breaker's pause test and test_scout's dry-run test pass at any machine load — lesson: A load flake is often real work inside a fixed t…
- T-1730 [FIX M, done, 3 steps] Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil… — lesson: Judge an…
- T-1719 [FIX S, done, 0 steps] Test_hooks.NoTaskGate hook calls time out at their 10 s limit under the 16-way parallel ru
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar finished tasks took 0–3 steps
- start here (files T-1379 touched): plugin/tests/test_doctor.py, plugin/tests/helpers.py, plugin/lib/fmdoctor.py
## Why not caught
release-check strips every FOREMAN_ variable, so the T-1379 bench switch from helpers never reached its doctor; the timing only crosses 150 ms when the 16-way suite loads the machine, under the busy() thresholds
## Lessons
- A sandboxing env filter needs an explicit pass-through for the test switches its children read
## Files touched
- plugin/tests/test_board_verbs.py
- plugin/lib/fmdemo.py
