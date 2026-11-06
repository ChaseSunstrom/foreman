---
id: T-1825
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:14:33Z
updated: 2026-10-28T09:25:39Z
base: 23f12f0e83669e351320674f8c9ed494e4d1020e
base_tree: d35af88f1907c5465fe318ca65fdde169bf621fa
plan0_at: 2026-10-28T09:17:14Z
plan0_scope: []
verified: strong
---
# FEATURE: fm run (headless) skips a model call when the tree and the failing check's output
## Raw request
> FEATURE: fm run (headless) skips a model call when the tree and the failing check's output are the same as the last attempt's: block with that diagnosis instead (T-1798 usage-efficiency lens)
## Interpretation
In fm run's serial loop, a session can move the brief (a new failing evidence line) while leaving the files and the failing check exactly as it found them. Today that counts as progress and buys another session (up to SESSIONS_PER_TASK = 3), which repeats the same failure. Compare the state when a session starts with the state when it ends: the worktree id plus the newest evidence line, if it is a failed run (its timestamp aside). If they match and no step or criterion advanced, block the task with that diagnosis (the failing check) and move on to the next task instead of paying for a repeat.
## Assumptions (confidence)
## Acceptance criteria
- [x] a session that leaves the tree and its failing check unchanged is not repeated: the task is blocked with the check named; a session that changes files keeps its sessions — verify with `cd plugin/tests && python3 -m unittest -q test_unattended.RunRepeatSkip`
## Non-goals
## Approach (options → choice → why)
(a) Compare each session's start and end key (worktree_id + newest failed evidence line without its timestamp), block and skip on a match. Chosen: two worktree_id calls per session, no new state, and fm run's existing block() helper. (b) Store the key on the run_session ledger event and compare across runs: rejected because a user's fm task unblock would be re-blocked right away; the in-run block already covers the next run. (c) Hash the whole check output: rejected because the evidence line already holds the exit code, the output tail and the tree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test RunRepeatSkip in test_unattended.py
2. [x] _repeat_key in fmserve and the check in cmd_run's serial loop; MASTER and CHANGELOG
3. [x] gates and review
## Resume here
<!-- auto -->
- 2026-10-28T09:23:03Z step 3/3: gates and review
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmserve.py, plugin/tests/test_unattended.py
- touched since last checkpoint: plugin/tests/test_unattended.py, plugin/lib/fmserve.py, CHANGELOG.md, MASTER.md
- failures met: fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hide…
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_unattended.RunRepeatSkip` → red as expected (exit 1) · Ran 2 tests in 0.720s / FAILED (failures=2) [ran] [tree b4c67dbc70c5] (2026-10-28T09:17:19Z)
- (step 2) `cd ~/.claude/foreman/plugin/tests && python3 -m unittest -q test_unattended 2>&1 | tail -4` → exit 0 · Ran 12 tests in 8.083s / OK [ran] [tree 4033877ae147] (2026-10-28T09:18:09Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_unattended.RunRepeatSkip` → exit 0 · Ran 2 tests in 1.272s / OK [ran] [tree 4033877ae147] (2026-10-28T09:18:16Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_unattended test_serve test_orchestration test_parallel test_runtime test_code_worker test_panic test_outbound` → exit 0 · Ran 160 tests in 156.255s / OK [ran] [tree 1f48e1e83423] (2026-10-28T09:20:53Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmserve.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.4    46.1     150  [0] / SessionEnd                  34.8    55.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 1f48e1e83423] (2026-10-28T09:24:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_unattended.RunRepeatSkip` → exit 0 · Ran 2 tests in 1.283s / OK [ran] [tree 1f48e1e83423] (2026-10-28T09:25:14Z)
- (audit intent) `self-review of a ~25-line diff in fmserve.cmd_run plus two tests; gates green on this tree` → a session that leaves the files and its failing check unchanged blocks the task with that diagnosis, never a third paid session [tree 1f48e1e83423] (2026-10-28T09:25:14Z)
- (audit edge) `self-review of a ~25-line diff in fmserve.cmd_run plus two tests; gates green on this tree` → no key without git or when the newest run passed; a step or criterion that advanced isn't blocked; the first evidence now counts as progress (fixed _fingerprint) [tree 1f48e1e83423] (2026-10-28T09:25:14Z)
- (audit adversary) `self-review of a ~25-line diff in fmserve.cmd_run plus two tests; gates green on this tree` → compared only against the session's own start, so a user's unblock isn't re-blocked by a stale key; at most one wasted session [tree 1f48e1e83423] (2026-10-28T09:25:14Z)
- (audit operator) `self-review of a ~25-line diff in fmserve.cmd_run plus two tests; gates green on this tree` → cost at scale is two worktree_id calls per session (git add on a copied index re-hashes changed files only) against a saved session of hundreds of k tokens [tree 1f48e1e83423] (2026-10-28T09:25:14Z)
## Log
- 2026-10-28T08:14:33Z created
- 2026-10-28T08:14:56Z set status=planned
- 2026-10-28T09:17:14Z focused
- 2026-10-28T09:25:37Z done
- 2026-10-28T09:25:39Z committed 3c601892 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one [stale: plugin/tests/ru…
- playbook Agent Introspection Debugging (fm playbooks show reflect/agent-introspection)
- T-0686 [FEATURE M, done, 5 steps] Milestone: Intelligence — Debugging and diagnosis — lesson: Escalation belongs in fm next, keyed on recorded evidence (failed runs per …
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- the similar finished task took 5 steps
## Lessons
- count list items by line start, not by '\n- ': the first item has no newline before it
## Files touched
- plugin/tests/test_unattended.py
- plugin/lib/fmserve.py
- CHANGELOG.md
- MASTER.md
