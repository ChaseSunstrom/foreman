---
id: T-0395
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:41:50Z
updated: 2026-10-09T02:43:22Z
base: 4cd6e1861756cdc6b14f28020f30f7fbd69e02e9
base_tree: ee4467522d4537a5f4b5a53b81faeaf628fa0da5
verified: strong
---
# Guard: the pipe-shell refusal of curl | python3 -c should say how it passes (JARVIS lost a turn: hf download > log on the same line)
## Raw request
> Guard: the pipe-shell refusal of curl | python3 -c should say how it passes (JARVIS lost a turn: hf download > log on the same line)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the refusal of a data-reading python -c beside a file-writing command says to run the rest separately — verify with `python3 plugin/tests/run.py -k test_pipe_shell_refusal_says_how_it_passes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the hint
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 02:37 UTC) [ran] [tree ee4467522d45] (2026-10-09T02:41:55Z)
- `python3 plugin/tests/run.py -k test_pipe_shell_refusal_says_how_it_passes` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PipeShellHint 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2d1a2512d663] (2026-10-09T02:42:08Z)
- `python3 plugin/tests/run.py -k test_pipe_shell_refusal_says_how_it_passes` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PipeShellHint 0s) / OK [ran] [tree 2d1a2512d663] (2026-10-09T02:42:08Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed (slower: 7.0 s vs a usual 3.8 s); python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.4    36.1     150  [0] / SessionEnd                  29.9    32.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/r [ran] [tree 62006891c3e4] (2026-10-09T02:43:21Z)
- (ac 1) `python3 plugin/tests/run.py -k test_pipe_shell_refusal_says_how_it_passes` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PipeShellHint 0s) / OK [ran] [tree 62006891c3e4] (2026-10-09T02:43:21Z)
- (audit intent) `self: message text only; replay shows no verdict change; the split-off command passes (test)` → the refusal says what passes and how to split the line (test) [tree 62006891c3e4] (2026-10-09T02:43:21Z)
- (audit adversary) `self: message text only; replay shows no verdict change; the split-off command passes (test)` → _hint only appends text after the decision; the replay corpus shows 0 newly allowed [tree 62006891c3e4] (2026-10-09T02:43:21Z)
- (audit edge) `self: message text only; replay shows no verdict change; the split-off command passes (test)` → only python* refusals get it; shells (bash, sh) piped a download keep the plain refusal [tree 62006891c3e4] (2026-10-09T02:43:21Z)
- (audit self) `self: message text only; replay shows no verdict change; the split-off command passes (test)` → no findings [tree 62006891c3e4] (2026-10-09T02:43:21Z)
## Log
- 2026-10-09T02:41:50Z created
- 2026-10-09T02:41:50Z focused
- 2026-10-09T02:43:22Z done
- 2026-10-09T02:43:22Z committed e0f4cb7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0344 [FIX M, done, 3 steps] Guard false positives: str.replace isn't a write; curl | python3 -c with proved-pure code isn't pipe-shell — lesson: A text pattern can't p…
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-08: T-0368: entry points re-exec under a saved supported Python
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
