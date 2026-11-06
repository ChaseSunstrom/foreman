---
id: T-0399
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:57:19Z
updated: 2026-10-09T02:58:37Z
base: 09b86bddc461e22a0a269e2b0cc5efbc6927efd7
base_tree: 58fee916be1861f38055925573fd4ba7d7f2370d
verified: strong
---
# Builder brief: edit files with the Edit/Write tools, never shell heredocs (JARVIS builders: 5 'too complex' isolation refusals in 10 min on python/cat heredoc edits)
## Raw request
> Builder brief: edit files with the Edit/Write tools, never shell heredocs (JARVIS builders: 5 'too complex' isolation refusals in 10 min on python/cat heredoc edits)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the builder brief tells builders to edit with Edit/Write, not cat/python heredocs or sed — verify with `python3 plugin/tests/run.py -k test_the_brief_says_edit_with_the_edit_tool`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the contract line
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_the_brief_says_edit_with_the_edit_tool` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Brief 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fddc9cfae460] (2026-10-09T02:57:37Z)
- `python3 plugin/tests/run.py -k test_the_brief_says_edit_with_the_edit_tool` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree fddc9cfae460] (2026-10-09T02:57:37Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.2    33.2     150  [0] / SessionEnd                  29.8    30.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 936 tests in [ran] [tree 121f1989765f] (2026-10-09T02:58:36Z)
- (ac 1) `python3 plugin/tests/run.py -k test_the_brief_says_edit_with_the_edit_tool` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree 121f1989765f] (2026-10-09T02:58:36Z)
- (audit intent) `self: one contract line; the brief test reads the generated brief` → new builder briefs say Edit/Write only and why (test) [tree 121f1989765f] (2026-10-09T02:58:36Z)
- (audit edge) `self: one contract line; the brief test reads the generated brief` → the existing isolation rule (don't retry, report) stays for commands like make and gradle [tree 121f1989765f] (2026-10-09T02:58:36Z)
- (audit self) `self: one contract line; the brief test reads the generated brief` → no findings [tree 121f1989765f] (2026-10-09T02:58:36Z)
## Log
- 2026-10-09T02:57:19Z created
- 2026-10-09T02:57:19Z focused
- 2026-10-09T02:58:36Z done
- 2026-10-09T02:58:37Z committed b860a14 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- T-0308 [SECURITY M, done, 2 steps] No edits without a task, for Bash writes too: the guard refuses shell writes into the project while no task is active — lesson: A gate…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 1–2 steps
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
