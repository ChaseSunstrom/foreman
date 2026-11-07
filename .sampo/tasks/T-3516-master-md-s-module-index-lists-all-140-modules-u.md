---
id: T-3516
type: CLEAN
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:11:45Z
updated: 2026-11-06T19:25:45Z
lane: ~/.claude/foreman.lanes/T-3516
lane_branch: foreman/T-3516
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T19:13:27Z
plan0_scope: []
---
# MASTER.md's module index lists all 140 modules under their old fm* names (fmcli,…
## Raw request
> CLEAN: MASTER.md's module index lists all 140 modules under their old fm* names (fmcli, fmagents, …) though the code is plugin/lib/sampo/*.py and the fm* files are 157-byte shims (T-2742): regenerate it with the new names
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] MASTER.md's module index names plugin/lib/sampo/<name>.py modules, not the fm* shims, and doctor's map check passes — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] regenerate the index with the new names
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor.MapNamesRealModules` → ✗ exit 1 · Ran 2 tests in 0.9s (1 jobs, 16 at a time; slowest: MapNamesRealModules 0s) / FAILED (1 classes: test_doctor.MapNamesRealModules) [ran] [tree 932c6770427b] [world 2f1906870a] (2026-11-06T19:15:15Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_docs.MapShards` → ✗ exit 1 · Ran 124 tests in 90.1s (46 jobs, 16 at a time; slowest: ViewsRepair 9s, Command 5s, LockProbe 5s) / FAILED (2 classes: test_doctor.Checks, test_docs.MapShards) [ran] [tree 749d57afc3cf] [world 2f1906870a] (2026-11-06T19:22:16Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_docs.MapShards` → exit 0 · Ran 124 tests in 48.6s (48 jobs, 16 at a time; slowest: ViewsRepair 6s, LockProbe 3s, Timing 3s) / OK [ran] [tree 749d57afc3cf] [world 2f1906870a] (2026-11-06T19:23:27Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_docs.MapShards` → exit 0 · Ran 123 tests in 86.7s (45 jobs, 16 at a time; slowest: ViewsRepair 9s, Command 8s, Timing 6s) / OK [ran] [tree d53a757e51ca] [world 2f1906870a] (2026-11-06T19:25:40Z)
## Log
- 2026-11-06T19:11:45Z created
- 2026-11-06T19:12:39Z set tier=S
- 2026-11-06T19:12:40Z planned: it has criteria and steps
- 2026-11-06T19:12:43Z lane: ~/.claude/foreman.lanes/T-3516 on foreman/T-3516
- 2026-11-06T19:13:26Z focused
- 2026-11-06T19:13:27Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T19:15:36Z focused
- 2026-11-06T19:15:49Z focused
- 2026-11-06T19:18:03Z focused
- 2026-11-06T19:20:09Z focused
- 2026-11-06T19:20:43Z focused
- 2026-11-06T19:21:32Z focused
- 2026-11-06T19:21:38Z focused
- 2026-11-06T19:21:48Z focused
- 2026-11-06T19:21:56Z focused
- 2026-11-06T19:22:37Z focused
- 2026-11-06T19:23:33Z focused
- 2026-11-06T19:24:04Z focused
- 2026-11-06T19:24:07Z focused
- 2026-11-06T19:24:12Z focused
- 2026-11-06T19:25:45Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-2780 [CLEAN S, done, 1 steps] test_evolve_never_revises_the_guards_own_files tries the guard's files under their sampo names too (plugin/lib/sampo/hooks.py, replay, ev…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
