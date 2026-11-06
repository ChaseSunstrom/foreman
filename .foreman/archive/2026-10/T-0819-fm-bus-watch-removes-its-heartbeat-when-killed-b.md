---
id: T-0819
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-14T18:10:03Z
updated: 2026-10-14T18:15:26Z
base: e5df8015564e111332438df79d0513fd524301b6
base_tree: 2a5d935940b2e3635175b0932b5f9d8779b791fd
verified: strong
---
# Fm bus watch removes its heartbeat when killed by SIGTERM/SIGHUP (live probe: the session
## Raw request
> fm bus watch removes its heartbeat when killed by SIGTERM/SIGHUP (live probe: the session ended, watch-<sid> stayed); tidy prunes stale watch-* files
## Interpretation
Claude Code ends a monitor with a signal; Python's default SIGTERM/SIGHUP handling skips watch()'s finally, so the heartbeat file outlives the session.
## Assumptions (confidence)
## Acceptance criteria
- [x] a watcher stopped by SIGTERM removes its heartbeat; tidy deletes watch-* heartbeats older than a day — verify with `python3 plugin/tests/run.py test_bus test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: SIGTERM leaves the heartbeat; tidy leaves old ones
2. [x] Signal handler in watch; tidy prune
## Resume here
## Docs impact
none: internal cleanup
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus test_tidy` → exit 0 · Ran 21 tests in 4.2s (10 classes, 16 at a time; slowest: Approvals 4s, Watch 4s, Apply 2s) / OK [ran] [tree 7180d285e9c5] (2026-10-14T18:11:03Z)
- (step 2) `python3 plugin/tests/run.py test_bus test_tidy` → exit 0 · Ran 21 tests in 4.1s (10 classes, 16 at a time; slowest: Approvals 4s, Watch 4s, Apply 2s) / OK [ran] [tree 7180d285e9c5] (2026-10-14T18:11:07Z)
- `python3 plugin/tests/run.py test_bus test_tidy` → ✗ exit 1 · Ran 21 tests in 4.3s (10 classes, 16 at a time; slowest: Approvals 4s, Watch 3s, Apply 2s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 7180d285e9c5] (2026-10-14T18:11:16Z)
- `python3 plugin/tests/run.py test_bus test_tidy` → exit 0 · Ran 21 tests in 4.1s (10 classes, 16 at a time; slowest: Approvals 4s, Watch 3s, Apply 2s) / OK [ran] [tree 7180d285e9c5] (2026-10-14T18:11:16Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                34.7    37.2     150  [0] / SessionEnd                  32.9    38.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 7180d285e9c5] (2026-10-14T18:13:05Z)
- (step 2) `python3 plugin/tests/run.py test_bus test_tidy` → exit 0 · Ran 21 tests in 4.1s (10 classes, 16 at a time; slowest: Approvals 4s, Watch 3s, Apply 2s) / OK [ran] [tree 8f194d0f3cd6] (2026-10-14T18:13:27Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                35.5    44.8     150  [0] / SessionEnd                  33.2    37.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 8f194d0f3cd6] (2026-10-14T18:15:16Z)
- (ac 1) `python3 plugin/tests/run.py test_bus test_tidy` → exit 0 · Ran 21 tests in 4.1s (10 classes, 16 at a time; slowest: Approvals 4s, Watch 3s, Apply 2s) / OK [ran] [tree 8f194d0f3cd6] (2026-10-14T18:15:25Z)
- (audit edge) `self + live probe: a fresh interactive claude in tmux started the foreman-mail monitor (fm bus watch) and it found its own session id via by-pid; killing the session left watch-<sid> behind, which this fixes; round-1 reviewer finding 9 (seen-<sid> never pruned) folded in` → SIGKILL still can't clean up, so tidy sweeps watch-/seen- files older than 7 days; a live session rewrites seen-<sid> on every tool call with mail present and its heartbeat every 2 s, so neither is swept [tree 8f194d0f3cd6] (2026-10-14T18:15:25Z)
- (audit self) `self + live probe: a fresh interactive claude in tmux started the foreman-mail monitor (fm bus watch) and it found its own session id via by-pid; killing the session left watch-<sid> behind, which this fixes; round-1 reviewer finding 9 (seen-<sid> never pruned) folded in` → no findings [tree 8f194d0f3cd6] (2026-10-14T18:15:25Z)
## Log
- 2026-10-14T18:10:03Z created
- 2026-10-14T18:10:10Z focused
- 2026-10-14T18:15:26Z done
- 2026-10-14T18:15:26Z committed 89f2385 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0777 [FEATURE M, done, 3 steps] Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux — les…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-0708 [FEATURE M, done, 5 steps] Frontier 08 — Orchestrator control plane — lesson: Cross-session control fits in the hooks that already run: deliver on the next tool c…
- decision 2026-10-14: Keep the Read hook unscoped (T-0782 dropped)
- similar finished tasks took 2–5 steps
## Lessons
- Cleanup in a finally doesn't run on SIGTERM in Python: a long-running child that the harness ends by signal needs a handler that exits
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/lib/fmtidy.py
- plugin/tests/test_tidy.py
