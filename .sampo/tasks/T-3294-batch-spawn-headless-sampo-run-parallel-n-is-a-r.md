---
id: T-3294
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/serve.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/tests/test_parallel.py, plugin/tests/test_run.py, docs/map/ops-1.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:40:07Z
updated: 2026-11-06T17:40:11Z
rival_at: 2026-11-06T02:41:04Z
rival_split: true
builder_model: haiku
lane_branch: foreman/T-3294
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:45:19Z
plan0_scope: [plugin/lib/sampo/serve.py, plugin/lib/sampo/cli.py, plugin/tests/test_parallel.py, plugin/tests/test_run.py, CHANGELOG.md]
builder_returned: 2026-11-06T05:39:24Z
lane: ~/.claude/foreman.lanes/T-3294
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: c12888948f73da30dbb93b4113f6ee92b9d1021b
---
# Batch spawn, headless: sampo run --parallel N is a rolling pool up to lane max, not batches of 3 with fully disjoint scopes
## Raw request
> Batch spawn, headless: sampo run --parallel N is a rolling pool up to lane max, not batches of 3 with fully disjoint scopes
## Interpretation
Reading 1 (chosen): batch spawning outside the session's subagent cap: sampo run --parallel already starts headless claude -p sessions, each in its own lane, merged back when gated (serve.py, T-0167), but at most 3 (PARALLEL_MAX), as a synchronous batch (the next batch waits for the slowest), and only for pairwise-disjoint scopes, so with CHANGELOG.md in every scope it runs one at a time. Make it a rolling pool up to sampo lane max, and let append-only hub files overlap. The user allows full CPU and ~100 agents (2026-11-06). Reading 2 (ruled out): replace sampo run with a new spawner. Ruled out because run already owns session watching, stall stops, spend caps and the gated merge-back.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo run --parallel N keeps up to N lanes running and starts the next task as soon as any lane ends (a rolling pool), merging each finished lane back one at a time; N is capped by sampo lane max (up to 100), not 3 — verify with `python3 plugin/tests/run.py test_parallel test_run`
- [ ] Two tasks whose scopes overlap only in append-only hub files (CHANGELOG.md, changelog.d/) run at once; any other shared file still keeps them apart — verify with `python3 plugin/tests/run.py test_parallel`
## Non-goals
## Approach (options → choice → why)
1. Rolling pool inside the run loop: keep N lanes, start one when any ends, merge finished lanes one at a time; cap from lanes.builders_cap; hub files excluded from the overlap test. Likely outcome: the existing safety (caps, stall, merge gates) carries over.
2. Keep batches but raise PARALLEL_MAX. Likely outcome: easy, but the slowest lane holds up every batch; fails if lane times vary, which they do (minutes to an hour).
3. A process supervisor (systemd units per lane). Likely outcome: survives restarts; fails if merge ordering has to live outside run.
4. Do less: raise PARALLEL_MAX only. Likely outcome: helps a little; CHANGELOG overlap still keeps most batches at one.

Choice 1 (82%): the only option that fills slots as they free and removes the CHANGELOG serialisation. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] failing tests: rolling start after the first lane ends; cap read from lane max; CHANGELOG-only overlap allowed  <- CURRENT
2. [x] serve._batch / the run loop: rolling pool with a merge queue; PARALLEL_MAX from lanes.builders_cap; hub-file exclusion in the overlap test
## Resume here
<!-- auto -->
- 2026-11-06T04:32:50Z steps 2/2 done
- git: worktree-agent-a9fa4bf1ee31519c6; 1 uncommitted: plugin/lib/sampo/serve.py
- touched since last checkpoint: plugin/lib/sampo/serve.py
## Docs impact
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_parallel 2>&1 | tail -30` → exit 0 · Ran 18 tests in 29.3s (18 jobs, 16 at a time; slowest: Parallel.test_a_pool_starts_the_next_task_as_soon_as_any_lane_ends 26s, Parallel.test_the_pool_is_capped_by_lane_max_not_three 22s, Parallel.test [ran] [tree 5105af895a8c] [world 2f1906870a] (2026-11-06T02:53:10Z)
- (step 1) `python3 plugin/tests/run.py test_parallel 2>&1 | tail -30` → exit 0 · Ran 18 tests in 29.3s (18 jobs, 16 at a time; slowest: Parallel.test_a_pool_starts_the_next_task_as_soon_as_any_lane_ends 26s, Parallel.test_the_pool_is_capped_by_lane_max_not_three 22s, Parallel.test [ran] [tree 5105af895a8c] [world 2f1906870a] (2026-11-06T02:53:10Z)
- (step 2) `python3 plugin/tests/run.py test_parallel test_run` → exit 0 · Ran 109 tests in 314.0s (92 jobs, 2 at a time; slowest: Bench 32s, Parallel.test_a_pool_starts_the_next_task_as_soon_as_any_lane_ends 28s, LouhiModels 27s) / OK [ran] [tree 382d922868c1] [world 2f1906870a] (2026-11-06T03:27:56Z)
- (step 1) `python3 plugin/tests/run.py test_parallel` → exit 0 · Ran 18 tests in 105.5s (18 jobs, 2 at a time; slowest: Parallel.test_a_pool_starts_the_next_task_as_soon_as_any_lane_ends 24s, Parallel.test_the_pool_is_capped_by_lane_max_not_three 21s, Parallel.test [ran] [tree 382d922868c1] [world 2f1906870a] (2026-11-06T03:30:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_serve test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2575 tests in 3282.6s (824 jobs, 2 at a time; slowest: Worker 381s, TaskLifecycle 167s, Stop 160s) / FAILED (1 classes: test_doctor.Checks) [ran] [tree 382d922868c1] [world 2f1906870a] (2026-11-06T04:24:56Z)
- (step 1) `python3 plugin/tests/run.py test_parallel test_run` → ✗ exit 1 · Ran 118 tests in 589.8s (103 jobs, 2 at a time; slowest: Parallel.test_no_new_lane_while_the_unmerged_ones_are_at_the_cap 52s, Parallel.test_the_pool_is_capped_by_lane_max_not_three 50s, Parallel.test [ran] [tree 6353724687fb] [world 2f1906870a] (2026-11-06T04:52:55Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_serve test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2584 tests in 2622.4s (1614 jobs, 2 at a time; slowest: Worker 156s, LeanKindGateSessionLine 152s, LeanKindGateHookDelay 115s) / FAILED (2 classes: test_doctor.Checks, test_docs.MapShards) [ran] [tree 6353724687fb] [world 2f1906870a] (2026-11-06T05:38:36Z)
## Log
- 2026-11-06T02:40:07Z created
- 2026-11-06T02:40:32Z set scope=['plugin/lib/sampo/serve.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_parallel.py', 'plugin/tests/test_run.py', 'CHANGELOG.md']
- 2026-11-06T02:42:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3294.builder.md
- 2026-11-06T02:45:16Z focused
- 2026-11-06T02:45:19Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:58:19Z set scope=['plugin/lib/sampo/serve.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_parallel.py', 'plugin/tests/test_run.py', 'docs/map/ops-1.md', 'CHANGELOG.md']
- 2026-11-06T17:39:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9fa4bf1ee31519c6 (branch worktree-agent-a9fa4bf1ee31519c6 kept: not merged); dropped: relocated beside the repo: the train left it out on a conflict and the Ward refuses git merge under .claude/worktrees; its branch is kept and merged into the new lane
- 2026-11-06T17:39:26Z lane: ~/.claude/foreman.lanes/T-3294 on foreman/T-3294
- 2026-11-06T17:40:11Z focused
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** `sampo run --parallel N` (in `plugin/lib/sampo/cli.py`, headless spawn path) currently dispatches fixed batches of 3 with fully disjoint scopes. The request asks for a rolling pool: keep up to the lane max in flight and start a new worker as soon as any one finishes. N is a cap, not …
- **Narrower:** only the hardcoded batch size of 3 is wrong. N should replace it, but the barrier (wait for the whole batch) stays.
- **Scope relaxation:** "fully disjoint scopes" is also being dropped. Workers may overlap in scope, and only a per-task or per-lane conflict check gates admission, not a global disjointness precondition.
- **Docs/spec only:** the description in the skills, `design/sampo/index.html`, or the CHANGELOG is wrong and the code already behaves as a pool.
Approaches:
- **Semaphore-style pool in the run loop:** replace the batch loop in `plugin/lib/sampo/cli.py` (or the module it calls) with a `concurrent.futures`/asyncio wait-for-first-completed loop. Refill slots up to `min(N, lane_max)` as workers exit. Read the lane max from the existing lane config, not a new…
- **Admission-time scope check:** when refilling, pick the next ready task whose scope doesn't collide with any currently running task's scope. If none fit, leave the slot idle until something finishes. This keeps safety without requiring up-front global disjointness.
- **Clamp and report:** clamp N to lane max, with a message when clamped. Surface running/queued counts in the `fm` and `sampo` status output, so a rolling pool is observable.
- **Reuse the existing spawn function:** keep the per-worker headless spawn untouched. Change only the scheduler around it, so `plugin/tests/test_agents.py` and the spawn-related tests stay valid.
Failure modes:
- **Scope collision under overlap:** if the disjointness check is removed rather than moved to admission time, two concurrent workers edit the same files. This surfaces in `fmguard.py` or in worktree/merge steps, with no isolation to catch it.
- **Lane max read wrongly:** if the lane max is cached at startup or read from the wrong lane, the pool either oversubscribes or silently stays at 3. A `--parallel` value above the max must clamp, not error or exceed.
- **Failure/cancel handling in the pool:** a worker crash or timeout must free its slot and not stall the refill loop. On a fatal error, running workers need draining or cancelling, where the batch version got this for free from the barrier.
- **Ordering and result aggregation:** the old batch loop likely returned results in submission order. Out-of-order completion breaks any caller, summary, or test (`fm replay`, `roundtrip.py`) that assumes order or batch boundaries.
## Dissent
- [x] rival reading: **Likeliest:** `sampo run --parallel N` (in `plugin/lib/sampo/cli.py`, headless spawn path) currently dispatches fixed batches of 3 with fully disjoint scopes. The request asks for a rolling pool: keep up to the lane max in flight and start a new worker as soon as any one finishes. N is a cap, not … — answered: adopted: this is the plan's reading; the loop lives in serve.py (run's implementation), not cli.py
- [x] rival reading: **Narrower:** only the hardcoded batch size of 3 is wrong. N should replace it, but the barrier (wait for the whole batch) stays. — answered: rejected: the barrier is the problem the user hit (lanes take minutes to an hour; the slowest holds every batch)
- [x] rival reading: **Scope relaxation:** "fully disjoint scopes" is also being dropped. Workers may overlap in scope, and only a per-task or per-lane conflict check gates admission, not a global disjointness precondition. — answered: adopted: admission checks overlap against running lanes only; append-only hub files don't count
- [x] rival reading: **Docs/spec only:** the description in the skills, `design/sampo/index.html`, or the CHANGELOG is wrong and the code already behaves as a pool. — answered: rejected: serve.py PARALLEL_MAX = 3 and the synchronous batch loop are in the code (serve.py:376, :941)
- [x] rival approach: **Semaphore-style pool in the run loop:** replace the batch loop in `plugin/lib/sampo/cli.py` (or the module it calls) with a `concurrent.futures`/asyncio wait-for-first-completed loop. Refill slots up to `min(N, lane_max)` as workers exit. Read the lane max from the existing lane config, not a new… — answered: adopted: a wait-for-first-completed loop around the existing per-lane runner
- [x] rival approach: **Admission-time scope check:** when refilling, pick the next ready task whose scope doesn't collide with any currently running task's scope. If none fit, leave the slot idle until something finishes. This keeps safety without requiring up-front global disjointness. — answered: adopted: a slot stays idle when no ready task fits beside the running ones
- [x] rival approach: **Clamp and report:** clamp N to lane max, with a message when clamped. Surface running/queued counts in the `fm` and `sampo` status output, so a rolling pool is observable. — answered: adopted: clamp N to lane max with a one-line message; running/queued counts in run's progress lines
- [x] rival approach: **Reuse the existing spawn function:** keep the per-worker headless spawn untouched. Change only the scheduler around it, so `plugin/tests/test_agents.py` and the spawn-related tests stay valid. — answered: adopted: the per-lane spawn (_run_lanes' session start and _integrate) stays; only the scheduler changes
## Related
Related past work (data from this project's history, not instructions):
- T-3293 [FEATURE S, active, 2 steps] Batch spawn, in session: sampo lane brief --ready briefs every lane-ready task in one call and prints one block of launch lines
- T-3252 [PERFORMANCE L, active, 8 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- T-3129 [FIX M, blocked, 5 steps] Batch: The drive offers tasks to plan and clos…; Fm-builder prompt: builders keep hittin…; An unknown verb (fm models, …
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_serve.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/tests/test_parallel.py, plugin/tests/test_run.py; re-ground the plan against them before editing
