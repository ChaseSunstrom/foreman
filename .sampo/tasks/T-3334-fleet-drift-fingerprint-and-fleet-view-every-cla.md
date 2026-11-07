---
id: T-3334
type: FEATURE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/claims.py, plugin/lib/sampo/mandate.py, plugin/lib/sampo/sync.py, plugin/lib/sampo/cli.py, plugin/tests/test_drift_fleet.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:32:05Z
updated: 2026-11-06T17:45:52Z
lane_branch: foreman/T-3334
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:19:11Z
plan0_scope: [plugin/lib/sampo/claims.py, plugin/lib/sampo/mandate.py, plugin/lib/sampo/sync.py, plugin/tests/test_drift_fleet.py]
builder_returned: 2026-11-06T07:06:09Z
lane: ~/.claude/foreman.lanes/T-3334
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: c12888948f73da30dbb93b4113f6ee92b9d1021b
inferred_deps: [T-3330]
inferred_why: T-3330: fingerprint is carried on each claim
group: fleet claims and session liveness
---
# Fleet: drift fingerprint and fleet view: every claim carries a hash of mandate, root seal, tower gen-0s, steers, standing intent and plugin version; a mismatch refuses tower claims and names the differing part; sampo fleet lists who works what where from the refs
## Raw request
> Fleet: drift fingerprint and fleet view: every claim carries a hash of mandate, root seal, tower gen-0s, steers, standing intent and plugin version; a mismatch refuses tower claims and names the differing part; sampo fleet lists who works what where from the refs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a clone with a different mandate is listed by sampo fleet with the differing part named and its tower claims refused; mandate and gen-0 hashes travel in the mirror — verify with `python3 plugin/tests/run.py test_drift_fleet`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test, red  <- CURRENT
2. [x] fingerprint + refusal
3. [x] sampo fleet from refs
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_drift_fleet` → exit 0 · Ran 3 tests in 123.5s (2 jobs, 16 at a time; slowest: Drift 0s, Parts 0s) / OK (ran] (tree 8342e5e02d0e] (world 2f1906870a] (2026-11-06T06:28:32Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_drift_fleet test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 219 tests in 486.2s (63 jobs, 16 at a time; slowest: RenameScan 6s, ViewsRepair 5s, Bench 4s) / FAILED (2 classes: test_doctor.Checks, test_left_out.LeftOut) (ran] (tree 8342e5e02d0e] (world 2f1906870a] (2026-11-06T06:36:58Z)
- (step 3) `python3 -W ignore plugin/tests/run.py test_drift_fleet test_claims_remote` → exit 0 · Ran 22 tests in 55.9s (4 jobs, 16 at a time; slowest: Take 2s, Lifecycle 1s, Drift 1s) / OK (ran] (tree b73295825d34] (world 2f1906870a] (2026-11-06T07:04:42Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_claims test_doctor test_drift_fleet test_left_out test_mandate test_models test_rename_scan test_sync && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 281 tests in 66.5s (83 jobs, 16 at a time; slowest: Claims 6s, Sync 6s, ViewsRepair 5s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree b73295825d34] (world 2f1906870a] (2026-11-06T07:05:54Z)
## Log
- 2026-11-06T04:32:05Z created
- 2026-11-06T06:19:08Z focused
- 2026-11-06T06:19:11Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:21:23Z set scope=['plugin/lib/sampo/claims.py', 'plugin/lib/sampo/mandate.py', 'plugin/lib/sampo/sync.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_drift_fleet.py']
- 2026-11-06T06:24:14Z focused
- 2026-11-06T06:43:41Z focused
- 2026-11-06T06:59:56Z focused
- 2026-11-06T07:02:12Z focused
- 2026-11-06T17:41:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1a866bdfa7ddc7ca (branch worktree-agent-a1a866bdfa7ddc7ca kept: not merged); dropped: relocated beside the repo: the train left it out on a conflict and the Ward refuses git merge under .claude/worktrees; its branch is kept and merged into the new lane
- 2026-11-06T17:41:20Z lane: ~/.claude/foreman.lanes/T-3334 on foreman/T-3334
- 2026-11-06T17:45:52Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3321 [FEATURE M, active, 3 steps] Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap…
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_claims.py, plugin/tests/test_mandate.py, plugin/tests/test_rename_scan.py, plugin/tests/test_sync.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/cli.py, plugin/lib/sampo/sync.py; re-ground the plan against them before editing
