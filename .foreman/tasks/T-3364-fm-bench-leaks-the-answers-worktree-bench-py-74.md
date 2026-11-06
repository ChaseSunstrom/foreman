---
id: T-3364
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/bench.py, plugin/tests/test_bench.py]
depends_on: []
source: discovered
created: 2026-11-06T05:55:15Z
updated: 2026-11-06T07:10:33Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a930cb76c3efc3c84
lane_branch: worktree-agent-a930cb76c3efc3c84
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:58:04Z
plan0_scope: [plugin/lib/sampo/bench.py, plugin/tests/test_bench.py]
builder_returned: 2026-11-06T07:10:33Z
---
# fm bench leaks the answers: _worktree (bench.py:74) is a linked git worktree, so an agent can git show the case commit's hidden tests and reference fix; arms must run in a fresh git init of git archive base (long.py's _archive), and a transcript audit voids any run that touches spec-suite/, the source repo or cases.json
## Raw request
> fm bench leaks the answers: _worktree (bench.py:74) is a linked git worktree, so an agent can git show the case commit's hidden tests and reference fix; arms must run in a fresh git init of git archive base (long.py's _archive), and a transcript audit voids any run that touches spec-suite/, the source repo or cases.json
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the case commit is unreachable from the arm's tree, and a fake transcript that reads cases.json is flagged as a leak — verify with `python3 plugin/tests/run.py test_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] run_case(fresh=True) and the leak audit
## Resume here
<!-- auto -->
- 2026-11-06T07:00:31Z steps 2/2 done
- git: worktree-agent-a930cb76c3efc3c84; 0 uncommitted
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_bench` → exit 0 · (no output) (ran] (tree 3f038110fba5] (world 2f1906870a] (2026-11-06T06:21:31Z)
- (step 1) `python3 plugin/tests/run.py test_bench` → exit 0 · (no output) (ran] (tree 3f038110fba5] (world 2f1906870a] (2026-11-06T06:21:31Z)
- (step 2) `python3 plugin/tests/run.py test_bench` → exit 0 · Ran 66 tests in 348.0s (62 jobs, 16 at a time; slowest: SoakStorm 7s, Ablation.test_a_feature_whose_off_arm_ties_full_foreman_files_one_subtraction_candidate 6s, Ablation.test_ablate_runs_full_foreman (ran] (tree 3f038110fba5] (world 2f1906870a] (2026-11-06T06:32:44Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_bench_family test_core test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 424 tests in 760.4s (150 jobs, 16 at a time; slowest: Ablation.test_a_feature_whose_off_arm_ties_full_foreman_files_one_subtraction_candidate 7s, SoakStorm 6s, ConfidenceRoutes 6s) / FAILED (1 cla (ran] (tree 3f038110fba5] (world 2f1906870a] (2026-11-06T06:39:47Z)
- (step 1) `python3 plugin/tests/run.py test_bench` → exit 0 · Ran 69 tests in 42.8s (63 jobs, 16 at a time; slowest: Modules 5s, SoakStorm 5s, Ablation.test_ablate_runs_full_foreman_and_one_arm_per_feature_off 5s) / OK (ran] (tree 9d7f43ff0b89] (world 2f1906870a] (2026-11-06T07:10:18Z)
## Log
- 2026-11-06T05:55:15Z created
- 2026-11-06T05:57:55Z focused
- 2026-11-06T05:58:04Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-3340 [FEATURE M, planned, 2 steps] Benchmark queue fixture: bench/spec-suite/queue.py (make.py --suite queue) builds 12 candidate tasks on hard's invoicing package (ke…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-31: End-of-run exam: one fresh child-authored draw (seed 70, 18 per kind, all six languages, 6 held out per kind), the zero-token arms on all, then the …
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bench.py, plugin/tests/test_core.py, plugin/tests/test_rename_scan.py
