---
id: T-3371
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:20:48Z
updated: 2026-11-06T07:05:37Z
base_note: 
lane: ~/.claude/foreman/.claude/worktrees/agent-a8f347513a4f6aa2c
lane_branch: worktree-agent-a8f347513a4f6aa2c
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T06:28:16Z
plan0_scope: []
builder_returned: 2026-11-06T07:05:37Z
---
# Sampo lease drop run in a lane worktree dropped leases it never claimed (claims.py,…
## Raw request
> FIX: sampo lease drop run in a lane worktree dropped leases it never claimed (claims.py, mandate.py, sync.py, cli.py held by other lanes; T-3266 builder report 2026-11-06): drop must only release the caller's own session/lane leases
## Interpretation
Reading 1: identity is session+active task plus lane-<id> pre-claims. Reading 2: identity is the whole session, ruled out because lanes share the main session id (T-1216).
## Assumptions (confidence)
## Acceptance criteria
- [ ] lease drop releases only caller's leases and its lane pre-claims — verify with `python3 -m unittest plugin/tests/test_claims.py`
## Non-goals
## Approach (options → choice → why)
1) mine() keyed session+task, add lane pre-claims and unseen-task guard; likely outcome: exact drops. 2) use what exists: the lease's own session/task fields already identify the holder, which is option 1's base; fails if tasks are unseen. 3) do less: refuse bare drop in lanes; fails because lanes lose cleanup. Choice 1 (90%): smallest change in the shared predicate.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then fix mine() in bus.py
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 -m unittest plugin/tests/test_claims.py 2>&1 | tail -30` → ✗ exit 1 (never ran: the test module test_claims couldn't import) · Ran 1 test in 0.000s / FAILED (errors=1) (ran] (tree 0f4f85918c56] (world 2f1906870a] (2026-11-06T06:28:42Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -t plugin/tests -p test_claims.py` → exit 0 · Ran 20 tests in 11.813s / OK (ran] (tree ccc3ef9fbb1c] (world 2f1906870a] (2026-11-06T06:30:00Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bus test_claims test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 539 tests in 541.9s (135 jobs, 16 at a time; slowest: AffectedPairs 257s, TaskLifecycle 20s, LouhiModels 13s) / FAILED (3 classes: test_bus.Lease, test_cli.AffectedPairs, test_left_out.LeftOut) (ran] (tree ccc3ef9fbb1c] (world 2f1906870a] (2026-11-06T06:39:05Z)
- (step 1) `python3 plugin/tests/run.py test_bus.Lease test_claims` → exit 0 · Ran 29 tests in 58.1s (16 jobs, 16 at a time; slowest: ClaimsReview 3s, Lease 3s, Stop 2s) / OK (ran] (tree 1d3d61d6de50] (world 2f1906870a] (2026-11-06T06:48:21Z)
## Log
- 2026-11-06T06:20:48Z created
- 2026-11-06T06:22:41Z also (T-3352 builder): sampo lease drop with no args reported 'Dropped 0' while the lane held three leases; the lane-vs-session identity of drop is inconsistent both ways
- 2026-11-06T06:27:51Z planned: it has criteria and steps
- 2026-11-06T06:28:14Z focused
- 2026-11-06T06:28:16Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T07:00:26Z focused
- 2026-11-06T07:02:08Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2870 [FIX S, done, 1 steps] Sampo lease drop run from a builder lane drops every lease the session holds (16 at once…
- T-3321 [FEATURE M, active, 3 steps] Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap…
- T-3283 [FIX S, done, 2 steps] A builder's lease take isn't refused by another lane's brief pre-claim (advisory since T-1138 for edits, still refusing in fm lease take) —…
- decision 2026-10-16: T-1032 plan: automatic failure→fix pairing in the hooks, recall across projects, pre-run warning, feedback counts, fm fix CLI, git transport via fm …
- similar finished tasks took 1–2 steps
