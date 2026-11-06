---
id: T-1401
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmrelease.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/lib/fmcodebench.py, plugin/lib/fmcodetui.py, plugin/tests/test_safety_gate.py, plugin/tests/helpers.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_release.py, plugin/tests/test_release_py.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-22T17:24:56Z
inferred_deps: [T-1382, T-1268]
inferred_why: T-1382: named in its request; T-1268: stale-safety gate reads the corpus replay result
base: 2be76554ecb94caeea9d173e730d6b4ad33e0761
base_tree: 06425ee9efbfb3ba00678c6ed9e1c894f2586851
plan0_at: 2026-10-22T16:38:02Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmrelease.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/test_safety_gate.py, CHANGELOG.md]
verified: strong
---
# Unattended fm code and fm release --push refuse on a stale or red safety replay
## Raw request
> SECURITY: Stale safety stack gate: an unattended fm code run and fm release --push refuse when the last canary or guard-corpus replay is red or older than N days, naming the check (S14, A12)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: with a stubbed failing replay both refuse, naming the check; a fresh green replay lets both run
## Interpretation
The guard corpus replay (fm replay --cases) and the release canary prove the safety stack still holds, but nothing requires them to be recent: an unattended fm code run or a release can go out on a guard that last passed its corpus weeks ago, or failed it.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a red or an 8-day-old corpus replay, an unattended fm code run and fm release --push refuse naming the check, its date and the refresh command; a fresh green replay lets both run — verify with `cd plugin/tests && python3 -m unittest test_safety_gate`
- [x] --stale-ok REASON runs anyway and logs the waiver — verify with `cd plugin/tests && python3 -m unittest test_safety_gate.SafetyGate.test_waiver_is_logged`
## Non-goals
## Approach (options → choice → why)
The safety stack's own checks are fm replay --cases (the guard corpus, T-1162; T-1263 adds evasions) and the release canary (sentinels). Both already log a ledger event with a result. Options: (1) run the replay inline before every fm code run (too slow for each run) → rejected; (2) chosen: read the latest replay and canary results from the ledger; an unattended fm code run (no TTY, or --yes/headless) and fm release --push refuse when the newest guard-corpus replay is red or older than SAFETY_STALE_DAYS (7), naming the check, its date and the command that refreshes it (fm replay --cases); an attended run only warns. fm release already runs its gates, so its refusal adds the corpus replay's freshness to them. A --stale-ok REASON flag logs an explicit waiver on the ledger (never silent).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] latest replay result from the ledger, the freshness rule
3. [x] refusals in fm code (unattended) and fm release --push, the waiver
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_safety_gate` → ✗ exit 1 · Ran 11 tests in 15.443s / FAILED (failures=7, errors=2) [ran] [tree 20f50d62716d] (2026-10-22T16:44:29Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_safety_gate.SafetyGate.test_the_rule test_safety_gate.SafetyGate.test_the_replay_records_its_result` → exit 0 · Ran 2 tests in 0.247s / OK [ran] [tree de3095a4575c] (2026-10-22T16:45:01Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_safety_gate` → exit 0 · Ran 11 tests in 15.491s / OK [ran] [tree caa86d0f96a6] (2026-10-22T16:46:57Z)
- `cd plugin/tests && python3 -m unittest test_safety_gate` → ✗ exit 1 · Ran 11 tests in 18.655s / FAILED (failures=7, errors=2) (start tree + this task's tests) [ran] [tree c1f03e086b26] (2026-10-22T17:12:40Z)
- `cd plugin/tests && python3 -m unittest test_safety_gate` → exit 0 · Ran 11 tests in 17.097s / OK [ran] [tree c1f03e086b26] (2026-10-22T17:12:40Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_safety_gate` → exit 0 · Ran 11 tests in 18.836s / OK [ran] [tree c1f03e086b26] (2026-10-22T17:13:05Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_safety_gate.SafetyGate.test_waiver_is_logged` → exit 0 · Ran 1 test in 3.870s / OK [ran] [tree c1f03e086b26] (2026-10-22T17:13:09Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_safety_gate test_code_tui.Paste` → exit 0 · Ran 17 tests in 17.465s / OK [ran] [tree c1f03e086b26] (2026-10-22T17:13:28Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_safety_gate test_code_tui.Paste` → exit 0 · Ran 17 tests in 15.479s / OK [ran] [tree c1f03e086b26] (2026-10-22T17:13:44Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_safety_gate test_code_tui.Paste` → exit 0 · Ran 17 tests in 16.390s / OK [ran] [tree c1f03e086b26] (2026-10-22T17:14:01Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_safety_gate` → exit 0 · Ran 12 tests in 15.342s / OK [ran] [tree 2738e569449e] (2026-10-22T17:20:16Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_safety_gate.SafetyGate.test_waiver_is_logged` → exit 0 · Ran 1 test in 3.185s / OK [ran] [tree 2738e569449e] (2026-10-22T17:20:21Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_safety_gate test_code_tui.Paste` → exit 0 · Ran 18 tests in 16.521s / OK [ran] [tree 2738e569449e] (2026-10-22T17:20:38Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_safety_gate test_code_tui.Paste` → exit 0 · Ran 18 tests in 16.647s / OK [ran] [tree 2738e569449e] (2026-10-22T17:20:55Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_safety_gate test_code_tui.Paste` → exit 0 · Ran 18 tests in 17.684s / OK [ran] [tree 2738e569449e] (2026-10-22T17:21:14Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_safety_gate` → exit 0 · Ran 12 tests in 16.528s / OK [ran] [tree 2738e569449e] (2026-10-22T17:21:44Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_safety_gate.SafetyGate.test_waiver_is_logged` → exit 0 · Ran 1 test in 3.107s / OK [ran] [tree 2738e569449e] (2026-10-22T17:21:44Z)
- (audit intent) `builder (high) test-first; merged; red proved with fm task prove (11 tests); I added the app's attended env and a logged safety_warned; one fm-reviewer pass: 3 findings fixed test-first (a substitute FOREMAN_GUARD_CASES replay never passes, a future-dated record isn't fresh, --stale-ok without --push refused), 2 accepted; affected 501 tests OK` → unattended fm code and fm release --push refuse on a red, empty, stale or missing corpus replay, naming the check, date and refresh [tree 2738e569449e] (2026-10-22T17:21:44Z)
- (audit adversary) `builder (high) test-first; merged; red proved with fm task prove (11 tests); I added the app's attended env and a logged safety_warned; one fm-reviewer pass: 3 findings fixed test-first (a substitute FOREMAN_GUARD_CASES replay never passes, a future-dated record isn't fresh, --stale-ok without --push refused), 2 accepted; affected 501 tests OK` → a substitute case file is recorded as such and ignored; FOREMAN_CODE_ATTENDED and --stale-ok both leave a ledger event, so no route is silent; a hard barrier was not asked for [tree 2738e569449e] (2026-10-22T17:21:44Z)
- (audit edge) `builder (high) test-first; merged; red proved with fm task prove (11 tests); I added the app's attended env and a logged safety_warned; one fm-reviewer pass: 3 findings fixed test-first (a substitute FOREMAN_GUARD_CASES replay never passes, a future-dated record isn't fresh, --stale-ok without --push refused), 2 accepted; affected 501 tests OK` → a future date counts as stale; a record from the same second takes the one that landed last [tree 2738e569449e] (2026-10-22T17:21:44Z)
- (audit operator) `builder (high) test-first; merged; red proved with fm task prove (11 tests); I added the app's attended env and a logged safety_warned; one fm-reviewer pass: 3 findings fixed test-first (a substitute FOREMAN_GUARD_CASES replay never passes, a future-dated record isn't fresh, --stale-ok without --push refused), 2 accepted; affected 501 tests OK` → the refusal names fm replay --cases; fm night refreshes Foreman's own repo [tree 2738e569449e] (2026-10-22T17:21:44Z)
- (audit maintainer) `builder (high) test-first; merged; red proved with fm task prove (11 tests); I added the app's attended env and a logged safety_warned; one fm-reviewer pass: 3 findings fixed test-first (a substitute FOREMAN_GUARD_CASES replay never passes, a future-dated record isn't fresh, --stale-ok without --push refused), 2 accepted; affected 501 tests OK` → enforce is the one door; the refusal text rewrite in fmcode is string-based (accepted) [tree 2738e569449e] (2026-10-22T17:21:44Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T18:37:14Z grounding (2026-10-21): records that exist — state/guard-replay.json (fmreplay._baseline_path, a baseline from Oct 9, not a pass/fail result) and per-release canary logs state/projects/<p>/logs/canary-<version>.txt (fmrelease._canary_log); fm code has no --unattended flag (every worker turn is unattended). So the gate needs a pass/fail record with a time first: fm bench guard --coverage writing its result and time, and the canary's verdict parsed from its log
- 2026-10-22T16:37:39Z planned from capture
- 2026-10-22T16:37:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1401.builder.md
- 2026-10-22T16:38:01Z focused
- 2026-10-22T17:10:55Z merged worktree-agent-a514db68b0087cc2c (10 file(s))
- 2026-10-22T17:10:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a514db68b0087cc2c
- 2026-10-22T17:10:57Z focused
- 2026-10-22T17:11:22Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmrelease.py', 'plugin/lib/fmreplay.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcodebench.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_safety_gate.py', 'plugin/tests/helpers.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_release.py', 'plugin/tests/test_release_py.py', 'CHANGELOG.md']
- 2026-10-22T17:11:22Z scope: widened for what the builder had to touch (bench seeds pass --stale-ok, test helpers stub a replay, release tests) and the app's spawn line; steer: an attended warning is logged on the ledger too, so FOREMAN_CODE_ATTENDED set by an agent is never silent
- 2026-10-22T17:15:56Z steer: review: a replay over FOREMAN_GUARD_CASES (a substitute case file) is recorded as such and never passes the gate; a future-dated record is not fresh; --stale-ok without --push is refused
- 2026-10-22T17:24:53Z done
- 2026-10-22T17:24:56Z committed d52876df (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py, plugin/tests/test_release.py, plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmrelease.py, plugin/lib/fmreplay.py, plugin/tests/test_safety_gate.py; re-ground the plan against them before editing
## Why not caught
new gate; the review read the override path
## Lessons
- A gate fed by a self-reported ledger record must refuse records made under a test override, or the override becomes the bypass.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_code.py
- plugin/tests/test_release.py
- plugin/tests/test_release_py.py
- plugin/tests/test_safety_gate.py
- plugin/lib/fmreplay.py
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodebench.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
