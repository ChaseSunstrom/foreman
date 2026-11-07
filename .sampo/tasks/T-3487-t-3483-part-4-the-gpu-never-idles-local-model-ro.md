---
id: T-3487
type: FEATURE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/night.py, plugin/tests/test_louhi_models.py]
depends_on: []
source: user
created: 2026-11-06T18:37:55Z
updated: 2026-11-07T00:42:55Z
builder_model: haiku
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T18:39:54Z
plan0_scope: []
builder_returned: 2026-11-06T18:45:28Z
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
---
# T-3483 part 4: the GPU never idles: local-model rounds run beside sampo moons grow --keep (their own lock and a deadline instead of the moons store lock), and a gpu-idle sensor (nvidia-smi under 10% for 10 min while a bench is due) queues loop rounds
## Raw request
> T-3483 part 4: the GPU never idles: local-model rounds run beside sampo moons grow --keep (their own lock and a deadline instead of the moons store lock), and a gpu-idle sensor (nvidia-smi under 10% for 10 min while a bench is due) queues loop rounds
## Interpretation
Reading 1 (chosen): local-model rounds stop sharing the moons store lock (louhi.bench_night takes it at louhi.py ~1705 and skips while sampo moons grow --keep holds it, moonscale.py ~257/~692), so a 10,000-moon run no longer blocks every bench; plus a gpu-idle sensor that queues a round when nvidia-smi shows <10% for 10 min while a bench is due. Reading 2 (ruled out): make the moons generator itself use the GPU more (more workers): it already waits on the CPU-side dedupe at load ~30, and it isn't the local-model exam the user asked to keep running.
## Assumptions (confidence)
## Acceptance criteria
- [x] a held moons store lock no longer stops a loop round — verify with `python3 plugin/tests/run.py test_louhi`
## Non-goals
## Approach (options → choice → why)
1) A separate exam lock with a deadline for local-model rounds; likely outcome: benches run beside moons grow, GPU busy; fails if: two writers share the exam log (it is append-only jsonl, so no). 2) Shorter lock holds inside moons grow; fails if: the generator's write path breaks (riskier, touches it). 3) A priority lock; fails if: one contended lock gets machinery it doesn't need. 4) Use what exists: louhi.bench_night already has a deadline and a busy row (louhi.py ~1705-1714); keep both, swap only which lock it takes; likely outcome: a few-line change with the existing busy-row test adapted. 5) Do less: move the nightly bench to a time moons isn't running; fails if: moons grow --keep runs for days. Choice 1 (80%) built as 4: the smallest change at the cause; the gpu-idle sensor reads nvidia-smi --query-gpu=utilization.gpu once per tick, no tool means no sensor (ponytail: one GPU).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the change
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 29 tests in 15.1s (5 jobs, 16 at a time; slowest: LouhiModels 13s, ModelBenchVisible 3s, LouhiLoo 1s) / OK [ran] [tree 2c7cbc236669] [world 2f1906870a] (2026-11-06T18:41:26Z)
- (step 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 29 tests in 15.1s (5 jobs, 16 at a time; slowest: LouhiModels 13s, ModelBenchVisible 3s, LouhiLoo 1s) / OK [ran] [tree 2c7cbc236669] [world 2f1906870a] (2026-11-06T18:41:26Z)
- (step 1) `python3 plugin/tests/run.py test_louhi` → ✗ exit 1 · Ran 30 tests in 5.3s (12 jobs, 16 at a time; slowest: ModelBenchVisible 4s, LouhiModels.test_the_generation_arm_writes_yield_and_pass_rate_one_endpoint_at_a_time 4s, LouhiModels.test_cap_leaves_rows_o [ran] [tree f5996b4abb6f] [world 2f1906870a] (2026-11-06T18:41:44Z)
- (step 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 30 tests in 5.2s (12 jobs, 16 at a time; slowest: ModelBenchVisible 4s, LouhiModels.test_cap_leaves_rows_out_and_show_says_how_many 4s, LouhiModels.test_run_writes_one_row_per_backend_and_use_from [ran] [tree 4ec23bf9d458] [world 2f1906870a] (2026-11-06T18:42:14Z)
- (step 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 31 tests in 3.2s (12 jobs, 16 at a time; slowest: ModelBenchVisible 3s, LouhiModels.test_a_busy_529_is_retried_then_counted 2s, LouhiModels.test_backends_run_grouped_by_endpoint_the_served_model_f [ran] [tree f05c91940fab] [world 2f1906870a] (2026-11-06T18:42:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_exam test_left_out test_louhi_models test_mint test_models test_night test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [18.03s] [ran] [tree f05c91940fab] [world 2f1906870a] (2026-11-06T18:45:02Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree cfdefe208291] (2026-11-06T22:17:13Z)
- (ac 1) `python3 plugin/tests/run.py test_louhi` → exit 0 · Ran 32 tests in 4.3s (13 jobs, 16 at a time; slowest: ModelBenchVisible 4s, LouhiModels.test_retrieval_rows_vote_from_the_nearest_train_requests_and_abstain_when_split 3s, LouhiModels.test_a_failing_b [ran] [tree cfdefe208291] [world 2f1906870a] (2026-11-06T22:17:21Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree cfdefe208291] (2026-11-06T22:17:21Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree cfdefe208291] (2026-11-06T22:17:21Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree cfdefe208291] (2026-11-06T22:17:21Z)
## Log
- 2026-11-06T18:37:55Z created
- 2026-11-06T18:38:03Z set approved=True
- 2026-11-06T18:38:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3487.builder.md
- 2026-11-06T18:39:49Z focused
- 2026-11-06T18:39:54Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T19:15:34Z andon answered: the GPU-idle sensor is T-3494 (its own task); T-3487 delivers only the exam-lock criterion, as its lane assumed
- 2026-11-06T19:16:09Z focused
- 2026-11-06T21:46:50Z merged worktree-agent-ab67d3d29dd165711 in merge train
- 2026-11-06T22:17:12Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/louhi.py', 'plugin/lib/sampo/night.py', 'plugin/tests/test_louhi_models.py']
- 2026-11-06T22:17:13Z scope: widened at merge to the reviewed lane's own diff (f2ef6913b), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:20:57Z done
- 2026-11-06T22:21:05Z committed 26c228bf6 (1 file)
- 2026-11-07T00:42:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab67d3d29dd165711; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- T-3484 [FEATURE M, planned, 1 steps] T-3483 part 1: sampo exam loop: each round runs the smith arm on N unseen scenarios per local profile, then the failure taxonomy, an…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- similar past tasks were L: consider --tier L
## Lessons
- none: a builder lane; its findings are in the brief
## Files touched
- plugin/tests/test_louhi_models.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/night.py
- plugin/lib/sampo/cli.py
- ANDON.md
- CHANGELOG.md
