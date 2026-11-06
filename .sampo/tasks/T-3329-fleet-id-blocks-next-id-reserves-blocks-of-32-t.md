---
id: T-3329
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/claims.py, plugin/lib/sampo/cli.py, plugin/tests/test_id_blocks.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:31:56Z
updated: 2026-11-06T06:47:27Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aeb5a77060abc43f5
lane_branch: worktree-agent-aeb5a77060abc43f5
base: e6d249cd52497dc477ea4c54b0159c21cef34c7f
base_tree: be236efca055096c48da09056d95772cb57f90d4
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:18:30Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/tests/test_id_blocks.py]
builder_returned: 2026-11-06T06:47:27Z
---
# Fleet: id blocks: next_id reserves blocks of 32 T-numbers through a claims ref so two machines never mint the same id
## Raw request
> Fleet: id blocks: next_id reserves blocks of 32 T-numbers through a claims ref so two machines never mint the same id
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] two clones each mint 40 ids against one bare remote with no overlap; offline, a machine keeps minting inside its current block and says when the block runs out; ids stay T-\d{4,} — verify with `python3 plugin/tests/run.py test_id_blocks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] two-clone test, red
2. [x] block reservation in next_id (core.py:2360)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_id_blocks` → ✗ exit 1 · Ran 3 tests in 20.3s (1 jobs, 16 at a time; slowest: IdBlocks 0s) / FAILED (1 classes: test_id_blocks.IdBlocks) (ran] (tree 21ec40f7f204] (world 2f1906870a] (2026-11-06T06:19:43Z)
- (step 2) `python3 plugin/tests/run.py test_id_blocks` → exit 0 · Ran 3 tests in 16.7s (1 jobs, 16 at a time; slowest: IdBlocks 1s) / OK (ran] (tree 09835981426e] (world 2f1906870a] (2026-11-06T06:21:41Z)
- (step 1) `python3 plugin/tests/run.py test_id_blocks` → exit 0 · Ran 3 tests in 313.3s (1 jobs, 16 at a time; slowest: IdBlocks 0s) / OK (ran] (tree edadc7f9bc5b] (world 2f1906870a] (2026-11-06T06:25:15Z)
- (step 2) `python3 plugin/tests/run.py test_id_blocks` → exit 0 · Ran 3 tests in 6.3s (1 jobs, 16 at a time; slowest: IdBlocks 0s) / OK (ran] (tree edadc7f9bc5b] (world 2f1906870a] (2026-11-06T06:26:07Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_claims test_core test_doctor test_id_blocks test_left_out test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 394 tests in 429.3s (99 jobs, 16 at a time; slowest: Claims 10s, RenameScan 8s, ConfidenceRoutes 6s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree edadc7f9bc5b] (world 2f1906870a] (2026-11-06T06:28:55Z)
- (step 2) `python3 plugin/tests/run.py test_id_blocks` → exit 0 · Ran 8 tests in 3.6s (1 jobs, 16 at a time; slowest: IdBlocks 1s) / OK (ran] (tree 4d1bf384276b] (world 2f1906870a] (2026-11-06T06:47:11Z)
## Log
- 2026-11-06T04:31:56Z created
- 2026-11-06T06:18:26Z focused
- 2026-11-06T06:18:30Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:20:00Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/claims.py', 'plugin/tests/test_id_blocks.py']
- 2026-11-06T06:39:50Z focused
- 2026-11-06T06:40:05Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/claims.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_id_blocks.py']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3321 [FEATURE M, active, 3 steps] Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-3333 [FEATURE M, planned, 3 steps] Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts me…
- decision 2026-11-01: [cites: user steer 2026-11-01: standing rule (3): never block on the user for a question about rules, gates or process; decide by gen-0 and the stan…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/claims.py, plugin/lib/sampo/core.py, plugin/tests/test_id_blocks.py; re-ground the plan against them before editing
