---
id: T-3379
type: PERFORMANCE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:22:19Z
updated: 2026-11-06T08:57:03Z
base_note: 
lane: ~/.claude/foreman/.claude/worktrees/agent-a62fa1ce1fdf8b5ac
lane_branch: worktree-agent-a62fa1ce1fdf8b5ac
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T06:29:30Z
plan0_scope: []
lane_stop: refused 2026-11-06T08:51:40Z
builder_returned: 2026-11-06T08:56:15Z
inferred_deps: [T-3274, T-3287]
inferred_why: T-3274: named in its request; T-3287: named in its request
---
# test_exam's GateGrowth classes (LeanKindGate*, one per louhi.GATE_MUTATIONS entry,…
## Raw request
> PERF: test_exam's GateGrowth classes (LeanKindGate*, one per louhi.GATE_MUTATIONS entry, T-3171) each run louhi.gate_mutations(runs=2) real hook benches: ~480 s per class under load, killed by run.py, and they keep every lane's affected check red on 2026-11-06 (T-3274, T-3287). Make the planted-growth proof cheap (bench a stub hook or a recorded baseline, runs=1 with a scaled band) or gate them to changes in louhi/bench/hooks, so the self-change gate keeps its proof without 8 min per class
## Interpretation
Reading 1: bench fewer fixtures in the gate runner so each class is cheap (chosen; keeps real gate). Reading 2: gate classes on changed files (rejected: the proof should keep running).
## Assumptions (confidence)
## Acceptance criteria
- [ ] each LeanKindGate class still passes (refused by own metric, dropped check flips, controls pass) — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) stub hook with cost model: fails if the stub drifts from real hooks, losing the proof. 2) use what exists: selfgate's memoized base bench shared across classes via disk cache; fails if classes stay separate processes with stale caches. 3) do less: bench 4 of 16 fixtures in-process in the gate runner; likely outcome: ~4x cheaper, same refusals. Choice 3 (90%): real hooks and gate stay; measure one class before (72 s at load 21) and after.
## Risks and rollback
## Execution prompt
## Steps
1. [x] runner benches a fixture subset; test + timing
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest plugin/tests/test_exam.py -k GateBenchFixtures` → ✗ exit 1 (never ran: the test module test_exam couldn't import) · Ran 1 test in 0.000s / FAILED (errors=1) (ran] (tree daff622e7bc1] (world 2f1906870a] (2026-11-06T06:39:35Z)
- (step 1) `python3 plugin/tests/run.py test_exam.GateBenchFixtures test_exam.LeanKindGateHookDelay` → exit 0 · Ran 2 tests in 76.8s (2 jobs, 16 at a time; slowest: LeanKindGateHookDelay 35s, GateBenchFixtures 0s) / OK (ran] (tree daff622e7bc1] (world 2f1906870a] (2026-11-06T06:40:58Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 121 tests in 568.3s (75 jobs, 16 at a time; slowest: JudgmentKinds 71s, LanesKind 38s, LeanKindGateGuardAllow 37s) / OK (ran] (tree daff622e7bc1] (world 2f1906870a] (2026-11-06T06:46:45Z)
## Log
- 2026-11-06T06:22:19Z created
- 2026-11-06T06:29:05Z planned: it has criteria and steps
- 2026-11-06T06:29:28Z focused
- 2026-11-06T06:29:30Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T06:54:41Z focused
- 2026-11-06T08:57:03Z criterion 1 verify: `python3 -m unittest test_exam.LeanKindGateHookDelay` → `python3 plugin/tests/run.py test_exam`
- 2026-11-06T08:57:03Z merge refusal cause: criterion 1's verify ran 'python3 -m unittest test_exam.LeanKindGateHookDelay' from the repo root, where test_exam isn't importable (ERROR: _FailedTest); verify now 'python3 plugin/tests/run.py test_exam' (122 OK in the lane after merging 3d1fb1b45)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2961 [FIX M, done, 1 steps] Baseline red:… — lesson: A lane's affected tests don't include the repo-wide scans (test_left_out); a merge of new library lines should run…
- T-3171 [PERFORMANCE S, done, 1 steps] The self-change gate test that plants growths takes 238-390 s alone and sets the full suite's floor: keep every check it makes, cut…
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
