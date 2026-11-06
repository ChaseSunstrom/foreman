---
id: T-3350
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T05:12:25Z
updated: 2026-11-06T07:02:07Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ab11b694bbbebc758
lane_branch: worktree-agent-ab11b694bbbebc758
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:27:48Z
plan0_scope: []
---
# State writes give up after 5 s with 'lock busy' (core.py:1181 timeout, cli.py:8782-8786…
## Raw request
> State writes give up after 5 s with 'lock busy' (core.py:1181 timeout, cli.py:8782-8786 exit 3) and every caller retries by hand: tonight captures, audits, task evidence and sampo check --evidence each failed several times while a finish, ship or merge held the lock (builders report the same). Interactive mutate should wait with backoff up to ~60 s and say what holds the lock (pid, verb) while waiting; hooks keep their quick timeout but must not drop their state (hooks.py:3704-3725 sets save=False, so the drive's dedupe never persists); capture_promises/capture_friction (cli.py:4634, 4654) drop captures on a 1 s timeout
## Interpretation
Interactive CLI state writes wait up to 60 s (SAMPO_LOCK_WAIT) with jittered backoff and one 'waiting' line at 5 s naming holder; hooks keep 5 s/explicit budgets. Lock file records holder; holds >=500 ms logged to lock-holds.log.
## Assumptions (confidence)
## Acceptance criteria
- [ ] second process waits out an 8 s hold instead of exit 3; a hook-sized budget still gives up in time — verify with `python3 -m unittest plugin.tests.test_lock_wait`
## Non-goals
## Approach (options → choice → why)
core.lock timeout=None uses module LOCK_WAIT (5 s); cli.main sets it to 60 around the verb. Holder pid/verb in .lock; holds >=500 ms logged to lock-holds.log. Not done: hooks.py save=False drop and capture_promises 1 s drops (separate).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test_lock_wait.py then core.lock/cli.main change
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 -m unittest plugin.tests.test_lock_wait 2>&1 | tail -8` → ✗ exit 1 · Ran 4 tests in 11.100s / FAILED (failures=1, errors=3) (ran] (tree f17b43cff051] (world 2f1906870a] (2026-11-06T06:28:19Z)
- (step 1) `python3 -m unittest plugin.tests.test_lock_wait plugin.tests.test_exit_next 2>&1 | tail -8` → exit 0 · Ran 12 tests in 11.305s / OK (ran] (tree 5ac5d1ae3d0b] (world 2f1906870a] (2026-11-06T06:28:49Z)
- (step 1) `python3 -m unittest plugin.tests.test_lock_wait` → exit 0 · Ran 4 tests in 11.173s / OK (ran] (tree 5ac5d1ae3d0b] (world 2f1906870a] (2026-11-06T06:29:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_doctor test_kalevala test_left_out test_lock_wait test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 640 tests in 742.0s (153 jobs, 16 at a time; slowest: AffectedPairs 173s, TaskLifecycle 21s, LouhiModels 12s) / FAILED (2 classes: test_cli.AffectedPairs, test_left_out.LeftOut) (ran] (tree 5ac5d1ae3d0b] (world 2f1906870a] (2026-11-06T06:41:33Z)
- (step 1) `python3 -m unittest plugin.tests.test_lock_wait` → exit 0 · Ran 9 tests in 13.436s / OK (ran] (tree a5a1b92dcee0] (world 2f1906870a] (2026-11-06T06:54:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_doctor test_hooks test_kalevala test_left_out test_lock_wait test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 902 tests in 223.5s (403 jobs, 16 at a time; slowest: AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 70s, AffectedPairs.test_an_affected_run_with_evidence_records_it 48s, Affec (ran] (tree a5a1b92dcee0] (world 2f1906870a] (2026-11-06T06:58:37Z)
## Log
- 2026-11-06T05:12:25Z created
- 2026-11-06T06:27:45Z planned: it has criteria and steps
- 2026-11-06T06:27:47Z focused
- 2026-11-06T06:27:48Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
