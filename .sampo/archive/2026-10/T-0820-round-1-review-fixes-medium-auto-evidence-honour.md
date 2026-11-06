---
id: T-0820
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:15:56Z
updated: 2026-10-14T18:26:42Z
base: 89f23856f59a1172c4957ca793b4699fb02d1192
base_tree: 8f194d0f3cd670123846a2b227fb68f6f67bf9dc
verified: strong
---
# Round-1 review fixes (medium): auto-evidence honours failure summaries, bench replays aren't one-off, record_pid survives overlap and stops at its own claude
## Raw request
> Round-1 review fixes (medium): auto-evidence honours failure summaries, bench replays aren't one-off, record_pid survives overlap and stops at its own claude
## Interpretation
Three medium defects the round-1 review found where today's changes meet older code: Bash-run verify commands bypass T-0773's exit-0 failure check; bench replays became one-off sessions under T-0775; record_pid (T-0777) can crash on overlapping SessionStarts and lets a child claude -p claim its parent's process.
## Assumptions (confidence)
## Acceptance criteria
- [x] a verify command run from Bash that exits 0 but prints a failure summary records a failing run — verify with `python3 plugin/tests/run.py test_hooks`
- [x] a bench replay's claude -p child is not a one-off session — verify with `python3 plugin/tests/run.py test_hooks`
- [x] record_pid writes this session's entries when another SessionStart removed a dead one first, and never maps a parent session's claude to a child claude -p — verify with `python3 plugin/tests/run.py test_bus`
## Non-goals
## Approach (options → choice → why)
Options: (a) move run_command's exit-0 failure classification into one fmcore helper both call; FOREMAN_BENCH=1 set by fmbench._env and honoured by _oneoff; record_pid tolerates a concurrent remove and records ancestors only up to the first process named claude; (b) re-run verify commands instead of trusting Bash output; (c) have the bench replay pass FOREMAN_DRIVE_TASK. Chose (a); (b) doubles run time; (c) would turn on fm run's dialog-free paths, which the bench shouldn't measure.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for the three
2. [x] Shared failure-summary check used by run_command and _auto_evidence
3. [x] FOREMAN_BENCH honoured by _oneoff; fmbench sets it
4. [x] record_pid: tolerant remove, stop at the first claude ancestor
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.AutoEvidence test_hooks.Stop test_bus` → exit 0 · Ran 52 tests in 35.2s (7 classes, 16 at a time; slowest: Stop 35s, Watch 4s, Approvals 4s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:19:20Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.AutoEvidence test_hooks.Stop test_bus` → exit 0 · Ran 52 tests in 34.2s (7 classes, 16 at a time; slowest: Stop 34s, Watch 4s, Approvals 4s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:19:54Z)
- (step 3) `python3 plugin/tests/run.py test_hooks.AutoEvidence test_hooks.Stop test_bus` → exit 0 · Ran 52 tests in 30.5s (7 classes, 16 at a time; slowest: Stop 30s, Watch 4s, Approvals 4s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:20:25Z)
- (step 4) `python3 plugin/tests/run.py test_hooks.AutoEvidence test_hooks.Stop test_bus` → exit 0 · Ran 52 tests in 34.9s (7 classes, 16 at a time; slowest: Stop 35s, Watch 5s, Approvals 4s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:21:00Z)
- `python3 plugin/tests/run.py test_hooks.AutoEvidence test_hooks.Stop test_bus` → ✗ exit 1 · Ran 52 tests in 30.6s (7 classes, 16 at a time; slowest: Stop 30s, Watch 4s, Approvals 4s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 0c7671e8403f] (2026-10-14T18:22:04Z)
- `python3 plugin/tests/run.py test_hooks.AutoEvidence test_hooks.Stop test_bus` → exit 0 · Ran 52 tests in 33.3s (7 classes, 16 at a time; slowest: Stop 33s, Watch 4s, Approvals 4s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:22:04Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (34 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.6    45.4     150  [0] / SessionEnd                  38.0    42.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 0c7671e8403f] (2026-10-14T18:25:53Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 144 tests in 33.0s (20 classes, 16 at a time; slowest: Stop 33s, PreToolUse 16s, SessionStart 14s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:26:41Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 144 tests in 33.0s (20 classes, 16 at a time; slowest: Stop 33s, PreToolUse 16s, SessionStart 14s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:26:41Z)
- (ac 3) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 11 tests in 4.0s (5 classes, 16 at a time; slowest: Watch 4s, Approvals 4s, Bus 2s) / OK [ran] [tree 0c7671e8403f] (2026-10-14T18:26:41Z)
- (audit intent) `self: three fixes, each red→green; full suite 1,310 OK` → verify commands run in Bash now go through the same fmcore.judged as fm's own runs (exit 0 + failure summary → 1, zero tests → 5); fmbench._env sets FOREMAN_BENCH so replays aren't one-off; record_pid tolerates a racing remove and stops at its own claude [tree 0c7671e8403f] (2026-10-14T18:26:41Z)
- (audit edge) `self: three fixes, each red→green; full suite 1,310 OK` → a criterion whose output legitimately prints 'FAILED (failures=…' while passing (a test about failure output) now records a failure — same rule fm check already applied since T-0773; a user who exports FOREMAN_BENCH in an ad-hoc claude -p gets the old non-one-off behaviour, an opt-out, not a hole (the guard still applies); no procfs and no ps → _comm is '' and record_pid keeps the old 4-ancestor depth [tree 0c7671e8403f] (2026-10-14T18:26:41Z)
## Log
- 2026-10-14T18:15:56Z created
- 2026-10-14T18:16:29Z focused
- 2026-10-14T18:26:41Z done
- 2026-10-14T18:26:42Z committed e08db45 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- research T-0383-review: Verdict: merge after fixes.** I found no CRITICAL or HIGH defects. I could not run anything, so the tests and the timing figures are unverified.
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Why not caught
none: the cross-task review is the check that caught them (each was a seam between two of today's tasks)
## Lessons
- A rule added at one entry point (fm's runner) must be found at every entry point that records the same thing (Bash auto-evidence): grep for the other writers of the record
## Files touched
- plugin/tests/test_bus.py
- plugin/tests/test_hooks.py
- plugin/lib/fmbench.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmbus.py
