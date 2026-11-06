---
id: T-0825
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:37:31Z
updated: 2026-10-14T18:43:42Z
base: ec6e1de0a42a83041f0931401b3dfb547ffb24d2
base_tree: 383b93960dab03aed30bd030a2c9d734044e39e3
verified: strong
---
# Read-only fm verbs survive a closed stdout pipe and no stdin (fm … | head, a reader that quits)
## Raw request
> Read-only fm verbs survive a closed stdout pipe and no stdin (fm … | head, a reader that quits)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] status, queue, next, digest, ui --json, state and research list exit without a traceback when stdout closes early and stdin is /dev/null — verify with `python3 plugin/tests/run.py test_verbs_nopipe`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing sweep test, then the fix where the traceback comes from
## Resume here
## Docs impact
none: behaviour fix
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verbs_nopipe` → exit 0 · Ran 1 tests in 3.6s (1 classes, 16 at a time; slowest: ClosedPipe 4s) / OK [ran] [tree 970cf624d692] (2026-10-14T18:41:28Z)
- `python3 plugin/tests/run.py test_verbs_nopipe` → ✗ exit 1 · Ran 1 tests in 3.9s (1 classes, 16 at a time; slowest: ClosedPipe 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 970cf624d692] (2026-10-14T18:41:36Z)
- `python3 plugin/tests/run.py test_verbs_nopipe` → exit 0 · Ran 1 tests in 3.5s (1 classes, 16 at a time; slowest: ClosedPipe 3s) / OK [ran] [tree 970cf624d692] (2026-10-14T18:41:36Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                38.9    43.8     150  [0] / SessionEnd                  34.5    37.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 970cf624d692] (2026-10-14T18:43:32Z)
- (ac 1) `python3 plugin/tests/run.py test_verbs_nopipe` → exit 0 · Ran 1 tests in 3.6s (1 classes, 16 at a time; slowest: ClosedPipe 4s) / OK [ran] [tree 970cf624d692] (2026-10-14T18:43:41Z)
- (audit edge) `self: the fix sits in the one entry point every verb goes through (plugin/bin/fm), so all 108 verbs get it, not only the 8 the sweep runs` → a reader that quits gives exit 0 (it chose to stop reading; Python's default was 120, which pipefail scripts would read as fm failing); output already written before the close is unaffected [tree 970cf624d692] (2026-10-14T18:43:41Z)
- (audit self) `self: the fix sits in the one entry point every verb goes through (plugin/bin/fm), so all 108 verbs get it, not only the 8 the sweep runs` → no findings [tree 970cf624d692] (2026-10-14T18:43:41Z)
## Log
- 2026-10-14T18:37:31Z created
- 2026-10-14T18:40:48Z focused
- 2026-10-14T18:43:41Z done
- 2026-10-14T18:43:42Z committed 2f5cd14 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0716 [SECURITY S, done, 3 steps] Pipe-into-shell gaps (T-0715 review): option args read as script (bash -o posix, python3 -
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- similar finished tasks took 2–3 steps
## Lessons
- Python CLIs that are piped into head need BrokenPipeError handled once at the entry point, with stdout pointed at devnull so the shutdown flush stays quiet
## Files touched
- plugin/tests/test_verbs_nopipe.py
- plugin/bin/fm
