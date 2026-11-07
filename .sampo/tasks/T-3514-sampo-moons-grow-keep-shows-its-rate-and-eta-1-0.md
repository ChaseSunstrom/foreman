---
id: T-3514
type: FEATURE
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:11:44Z
updated: 2026-11-06T19:20:43Z
lane: ~/.claude/foreman.lanes/T-3514
lane_branch: foreman/T-3514
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T19:13:43Z
plan0_scope: []
group: moons grow throughput
---
# Sampo moons grow --keep shows its rate and ETA: 1,041 to 1,369 kept in 9.5 h (about 34…
## Raw request
> FEATURE: sampo moons grow --keep shows its rate and ETA: 1,041 to 1,369 kept in 9.5 h (about 34 an hour of 33,439 generated), so 10,000 kept is about 250 h away; name the filter that drops most and tune workers or filters
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo moons grow --keep prints its kept-per-hour rate, the ETA to the target and the filter that drops the most candidates — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] rate, ETA and top filter in grow's progress, test-first  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 119 tests in 120.3s (20 jobs, 16 at a time; slowest: Cli 3s, KeepGrow 3s, Wilder 3s) / FAILED (1 classes: test_moons_scale.KeepGrow) [ran] [tree 182153054ebf] [world 2f1906870a] (2026-11-06T19:16:19Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 119 tests in 65.9s (20 jobs, 16 at a time; slowest: Yield 3s, KeepGrow 3s, Wilder 3s) / FAILED (1 classes: test_moons_scale.Pace) [ran] [tree bd7a7400ba08] [world 2f1906870a] (2026-11-06T19:20:43Z)
## Log
- 2026-11-06T19:11:44Z created
- 2026-11-06T19:12:40Z set tier=S
- 2026-11-06T19:12:40Z planned: it has criteria and steps
- 2026-11-06T19:12:43Z lane: ~/.claude/foreman.lanes/T-3514 on foreman/T-3514
- 2026-11-06T19:13:42Z focused
- 2026-11-06T19:13:43Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- T-3044 [FEATURE M, done, 4 steps] The live page shows each running job's progress (training models, growing cards and moons, exams): done of total, rate and ETA — lesson…
- T-3042 [FEATURE L, planned, 4 steps] 10,000 moons kept and used, and moons on anything related to Sampo
- similar past tasks were L: consider --tier L
- similar finished tasks took 4–5 steps
