---
id: T-3330
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/fleet.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/hooks.py, plugin/tests/test_fleet_focus.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:31:57Z
updated: 2026-11-07T00:57:34Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a6974a31f571ee3eb
lane_branch: worktree-agent-a6974a31f571ee3eb
base: f411f679994b62594fe9e6ee6d701ac0a56c080d
base_tree: e9852af9e333832b952bca409fda465999846644
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:28:59Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/tests/test_claims_remote.py]
builder_returned: 2026-11-06T07:07:04Z
group: fleet claims and session liveness
---
# Fleet: starting a task takes its claim; hooks refuse edits once the claim is lost, naming the holder's machine
## Raw request
> Fleet: starting a task takes its claim; hooks refuse edits once the claim is lost, naming the holder's machine
## Interpretation
Reading 1: focus takes the claim, hooks read a cache. Reading 2: hooks poll the remote (ruled out: slow, network in PreToolUse).
## Assumptions (confidence)
## Acceptance criteria
- [ ] with fleet on, clone A focuses T-x and holds its claim; clone B's focus of T-x is refused naming A's machine and until; after A's lease lapses B can take it; with fleet off nothing changes — verify with `python3 plugin/tests/run.py test_claims_remote test_hooks`
## Non-goals
## Approach (options → choice → why)
1) hook queries the remote each edit; fails if: slow or offline blocks edits. 2) use what exists: claims.py take/renew, plus a small local cache file focus and refresh write and the hook reads; fails if: cache stale (bounded by background refresh every 10 min). 3) do less: only refuse at focus; fails if: a lapsed claim never stops the old holder. Choice 2 (80%): cheap, no network in the hook.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/test_hooks.py, plugin/lib/sampo/cli.py, CHANGELOG.md, plugin/tests/test_cli.py, plugin/tests/test_lanes.py; past FIXes T-2839, T-2848, T-2866, T-2872, T-2873.
## Execution prompt
## Steps
1. [ ] test, red  <- CURRENT
2. [x] focus takes the claim; edits check it at most once per 10 minutes
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fleet_focus` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 79.7s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (ran] (tree b08bea1a3532] (world 2f1906870a] (2026-11-06T06:30:44Z)
- (step 2) `python3 plugin/tests/run.py test_fleet_focus` → exit 0 · Ran 4 tests in 29.2s (1 jobs, 16 at a time; slowest: FleetFocus 2s) / OK (ran] (tree c01e7eebb3ab] (world 2f1906870a] (2026-11-06T06:31:44Z)
- (ac 1) `python3 plugin/tests/run.py test_claims_remote test_hooks` → exit 0 · (no output) (ran] (tree c01e7eebb3ab] (world 2f1906870a] (2026-11-06T06:34:38Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_doctor test_fleet_focus test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 831.903s) · timed out after 831.903s (ran] (tree c01e7eebb3ab] (world 2f1906870a] (2026-11-06T06:45:49Z)
- (step 2) `python3 plugin/tests/run.py test_fleet_focus` → exit 0 · Ran 4 tests in 27.7s (1 jobs, 16 at a time; slowest: FleetFocus 2s) / OK (ran] (tree c01e7eebb3ab] (world 2f1906870a] (2026-11-06T06:49:50Z)
- (step 2) `python3 plugin/tests/run.py test_fleet_focus` → exit 0 · Ran 8 tests in 8.4s (1 jobs, 16 at a time; slowest: FleetFocus 6s) / OK (ran] (tree 403c3381f731] (world 2f1906870a] (2026-11-06T07:01:48Z)
## Log
- 2026-11-06T04:31:57Z created
- 2026-11-06T06:28:56Z focused
- 2026-11-06T06:28:59Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:29:09Z set scope=['plugin/lib/sampo/fleet.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_fleet_focus.py']
- 2026-11-06T07:00:30Z focused
- 2026-11-06T07:01:11Z focused
- 2026-11-07T00:57:34Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3321 [FEATURE M, active, 3 steps] Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-3333 [FEATURE M, active, 3 steps] Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts mer…
- decision 2026-11-03: [costly] [cites: user steer: read SAMPO.md (protected core queued for the user; nothing a user has may break)] The rename's guard step comes first: …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/cli.py, plugin/lib/sampo/fleet.py, plugin/lib/sampo/hooks.py, plugin/tests/test_fleet_focus.py; re-ground the plan against them before editing
