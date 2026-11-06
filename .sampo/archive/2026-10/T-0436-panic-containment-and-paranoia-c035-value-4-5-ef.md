---
id: T-0436
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T15:17:03Z
base: 1a35601b4f9437a499710a6b6fa7fb8eec2388c9
base_tree: 37f2c08271f094656f88156bdeebfbf735d40fe4
verified: strong
---
# fm pause: one flag stops everything Foreman runs unattended
## Raw request
> SECURITY: Panic, containment and paranoia (C035, value 4/5, effort S, risk low)
>   first version: fm pause: one flag file that makes the Stop drive, fm run/serve/night and lane launches stop, and sets autonomy to standard; fm resume clears it. Only tightens; the user can toggle it.
>   what it is: A visible kill switch, freeze-everything button, paranoid-hour dial and compromise containment.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
fm drive off is per project and the PAUSE override pauses one task; nothing stops every session and launcher at once. One file, state_dir()/PANIC, set by fm pause and cleared by fm resume, makes the drive return nothing and fm run, fm serve start, fm night and fm lane new refuse; a running fm run loop re-checks it each iteration. It only ever stops things, so it can only tighten.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm pause makes the drive return nothing and run, serve start, night and lane new refuse — verify with `python3 plugin/tests/run.py -k panic_blocks_unattended`
- [x] fm pause off clears it — verify with `python3 plugin/tests/run.py -k panic_resume`
## Non-goals
## Approach (options → choice → why)
(A, chosen) one flag file + c.panicked() checked at each entry point. (B, rejected) drive=false in every project's meta: not atomic, and resume must remember prior state. (C, rejected) a guard block on every tool call: too broad for a first version. A claude child already running keeps going (new launches stop).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: panic_blocks_unattended, panic_resume
2. [x] c.panicked/set_panic + fm pause/resume commands + status banner
3. [x] checks in _drive, cmd_run (each loop), cmd_serve start, cmd_night, lane new; MASTER + help tiers
## Resume here
## Docs impact
CHANGELOG line; help tier lists pause
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_panic` → ✗ exit 1 · Ran 3 tests in 2.1s (1 classes, 16 at a time; slowest: Panic 2s) / FAILED (1 classes) [ran] [tree 73ff75e32179] (2026-10-09T14:44:19Z)
- (step 2) `python3 plugin/tests/run.py -k panic_resume` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Panic 1s) / OK [ran] [tree 744ebb4bb912] (2026-10-09T14:46:16Z)
- (step 3) `python3 plugin/tests/run.py -k panic_blocks_unattended` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Panic 1s) / OK [ran] [tree 744ebb4bb912] (2026-10-09T14:46:17Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.9    34.6     150  [0] / SessionEnd                  29.9    32.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 984 tests in [ran] [tree 744ebb4bb912] (2026-10-09T14:47:33Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 14:47 UTC) [ran] [tree 744ebb4bb912] (2026-10-09T14:47:37Z)
- (step 1) `python3 plugin/tests/run.py -p test_panic.py` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: Panic 2s) / OK [ran] [tree 8ece48961a4f] (2026-10-09T15:16:54Z)
- (ac 1) `python3 plugin/tests/run.py -k panic_blocks_unattended` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Panic 1s) / OK [ran] [tree 8ece48961a4f] (2026-10-09T15:16:56Z)
- (ac 2) `python3 plugin/tests/run.py -k panic_resume` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Panic 1s) / OK [ran] [tree 8ece48961a4f] (2026-10-09T15:16:56Z)
- (audit intent) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → one command stops the unattended paths the user cares about (drive, run, serve, night, lanes) [tree 8ece48961a4f] (2026-10-09T15:16:56Z)
- (audit edge) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → a running claude child finishes its turn; autonomy reads standard while paused so nothing self-approves [tree 8ece48961a4f] (2026-10-09T15:16:56Z)
- (audit operator) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → other launchers (session start, ideas, research ask, bench, fmrelate) still start children while paused, captured as T-0591 [tree 8ece48961a4f] (2026-10-09T15:16:56Z)
- (audit intent) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → one command stops the unattended paths the user cares about (drive, run, serve, night, lanes) [tree 8ece48961a4f] (2026-10-09T15:17:02Z)
- (audit edge) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → a running claude child finishes its turn; autonomy reads standard while paused so nothing self-approves [tree 8ece48961a4f] (2026-10-09T15:17:02Z)
- (audit operator) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → other launchers (session start, ideas, research ask, bench, fmrelate) still start children while paused, captured as T-0591 [tree 8ece48961a4f] (2026-10-09T15:17:02Z)
- (audit adversary) `self: builder diff reviewed (one PANIC file under the state dir; checked in drive, next/state autonomy, run/serve/night/lane new); merged --no-ff; criteria re-run on the merged tree; panic+hooks+serve+cli suites green` → the flag only removes behaviour (grants nothing, can't be used to widen); the guard files in this task's span are T-0581/T-0585/T-0589/T-0590 commits landed around the lane, each with its own adversary audit [tree 8ece48961a4f] (2026-10-09T15:17:02Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:33:00Z planned from capture
- 2026-10-09T14:40:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0436.builder.md
- 2026-10-09T14:41:09Z focused
- 2026-10-09T15:15:51Z merged worktree-agent-a9f85a7ddb26ef8a2 (8 file(s))
- 2026-10-09T15:15:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9f85a7ddb26ef8a2
- 2026-10-09T15:15:51Z focused
- 2026-10-09T15:16:11Z criterion 2 text: fm resume clears it → fm pause off clears it
- 2026-10-09T15:17:03Z done
- 2026-10-09T15:17:03Z committed 0afd44a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0506 [SECURITY M, dropped, 0 steps] Panic, containment and paranoia (C035, value 4/5, effort S, risk low)
- research brainstorm-foreman-20261009: 835 ideas, 103 capabilities; every idea is listed under exactly one capability.
- T-0434 [FEATURE M, done, 3 steps] Heartbeat and breaker for unattended runs — lesson: A breaker must count failures, not outcomes: a task that says why it's blocked is t…
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
- the similar finished task took 3 steps
## Lessons
- a kill switch is one flag every launcher checks at its own entry, not a per-project setting; list every launcher before calling it done
## Files touched
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/tests/test_panic.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/lib/fmcore.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/lib/fmcli.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/lib/fmhooks.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/lib/fmserve.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/lib/fmnight.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/plugin/lib/fmlanes.py
- .claude/worktrees/agent-a9f85a7ddb26ef8a2/MASTER.md
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmagents.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmnight.py
- plugin/lib/fmserve.py
- plugin/tests/fixtures/guard_fuzz_escapes.txt
- plugin/tests/test_agents.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_panic.py
- plugin/tests/test_parallel.py
