---
id: T-1822
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:13:24Z
updated: 2026-10-28T09:01:48Z
base: bc0ba1ec865176b1476340b670cca9ae95af7981
base_tree: 30d9e03228222a422c87bb13d9bcfe722246fd9e
plan0_at: 2026-10-28T08:57:23Z
plan0_scope: []
verified: strong
---
# FEATURE: plugin parity test: every user-facing fm verb is reachable through the installed
## Raw request
> FEATURE: plugin parity test: every user-facing fm verb is reachable through the installed plugin (a command, skill or hook), checked in CI so it stays so (T-1798 brainstorm)
## Interpretation
Every command the fm code app offers (COMMAND_LABELS, plus extensions' extra labels) must have a route in the Claude Code plugin: an fm verb (plugin/bin/fm is on the plugin's PATH), a /foreman: skill or command, git, or a Claude Code built-in; or be named app-only with a reason (navigation, the frame's photo booth, Breakout). A unittest checks each route resolves, so CI fails when a new app command lands without one (memory: cc-plugin-parity).
## Assumptions (confidence)
## Acceptance criteria
- [x] each COMMAND_LABELS command has a resolving plugin route or an APP_ONLY reason — verify with `cd plugin/tests && python3 -m unittest -q test_plugin_parity`
- [x] a new app command without a route fails the test (checked by the test itself) — verify with `cd plugin/tests && python3 -m unittest -q test_plugin_parity`
## Non-goals
## Approach (options → choice → why)
Options: (a) a ROUTES map in fmcodetui shown in the help view; (b) the map inside the test; (c) parse fm help/skills for names (fuzzy, no reasons). Choice: (b): nothing at runtime reads it, and the help view's CLI lines are terminal commands, not Claude Code routes; the test's failure message names where to add a new command's route.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: every app command resolves to a plugin route or APP_ONLY
2. [x] Fill CLI routes and APP_ONLY in fmcodetui; help view shows them
3. [x] Gates and review
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_plugin_parity` → ✗ exit 1 · Ran 3 tests in 0.030s / FAILED (failures=26) [ran] [tree 16c62b8719b0] (2026-10-28T08:57:37Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_plugin_parity` → exit 0 · Ran 3 tests in 0.027s / OK [ran] [tree da4c5ac4a56c] (2026-10-28T08:57:44Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_plugin_parity` → exit 0 · Ran 3 tests in 0.026s / OK [ran] [tree 7bc090d358b5] (2026-10-28T08:57:55Z)
- (audit intent) `self-review (test-only diff)` → each of the 25 COMMAND_LABELS commands has exactly one route or app-only reason; routes resolve against fm's real parser and plugin files [tree c8f84b39f0c7] (2026-10-28T08:59:04Z)
- (audit edge) `self-review` → a typo'd fm verb, fm subcommand, skill or unknown key fails (asserted); extensions' labels are user-local, left out [tree c8f84b39f0c7] (2026-10-28T08:59:04Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 08:51 UTC; claude plugin test mods/foreman-ui → [ran] [tree c8f84b39f0c7] (2026-10-28T09:01:32Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_plugin_parity` → exit 0 · Ran 3 tests in 0.026s / OK [ran] [tree c8f84b39f0c7] (2026-10-28T09:01:44Z)
- (ac 2) `cd plugin/tests && python3 -m unittest -q test_plugin_parity` → exit 0 · Ran 3 tests in 0.026s / OK [ran] [tree c8f84b39f0c7] (2026-10-28T09:01:44Z)
- (audit intent) `self-review: test-only diff, lenses intent and edge` → each COMMAND_LABELS command has one resolving Claude Code route or an app-only reason [tree c8f84b39f0c7] (2026-10-28T09:01:44Z)
- (audit edge) `self-review: test-only diff, lenses intent and edge` → typo'd fm verb, subcommand, skill or key fails; extensions left out (user-local) [tree c8f84b39f0c7] (2026-10-28T09:01:44Z)
## Log
- 2026-10-28T08:13:24Z created
- 2026-10-28T08:14:55Z set status=planned
- 2026-10-28T08:57:22Z focused
- 2026-10-28T08:57:28Z steer: step 2 is now: fill PLUGIN_ROUTES and APP_ONLY inside test_plugin_parity (no runtime reader; help view keeps CLI's terminal lines)
- 2026-10-28T09:01:46Z done
- 2026-10-28T09:01:48Z committed aadb1cb7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1546 [FEATURE M, done, 6 steps] Round 3 (T-1520): fm code app visual extras: a photo booth for frames, an isometric layout — lesson: A chaos harness is safe to run any…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- research T-1798-triage: Source: research/brainstorm-20261028-025248 (4 rounds × 14 lenses, 626 distinct ideas; the simplicity lens failed in round 3).
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- similar finished tasks took 3–6 steps
## Lessons
- A parity map nothing reads at runtime belongs in its test, not the module
## Plan gaps
- failed first: step 1 Failing test: every app command resolves to a plugin route or APP_ONLY
## Files touched
- plugin/tests/test_plugin_parity.py
- CHANGELOG.md
- MASTER.md
