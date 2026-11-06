---
id: T-3093
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/pages.py, site/build.py, site/stats.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/night.py, plugin/lib/sampo/rune.py, plugin/tests/test_site_build.py, plugin/tests/test_louhi_models.py, plugin/tests/test_night.py]
depends_on: []
source: user
created: 2026-11-05T02:02:06Z
updated: 2026-11-05T07:43:48Z
builder_model: haiku
base: 732c3ca6888b7d09e02135a5c8bd5b95eae2f38d
base_tree: f204b4fe9164cad84f821105674dec1fe14cd7d9
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T02:02:22Z
plan0_scope: [site/pages.py, site/build.py, site/stats.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/night.py, plugin/lib/sampo/rune.py, plugin/tests/test_site_build.py, plugin/tests/test_louhi_models.py, plugin/tests/test_night.py]
lane_stop: merged 2026-11-05T05:54:37Z
verified: strong
---
# Model bench, the visible half: a Models section on the site's Benchmarks page, a $0 rerun every Rune generation, and the promotion rule with decision rows (T-2886 steps 4-5)
## Raw request
> Model bench, the visible half: a Models section on the site's Benchmarks page, a $0 rerun every Rune generation, and the promotion rule with decision rows (T-2886 steps 4-5)
## Interpretation
Reading 1 (taken): T-2886's unbuilt half: the numbers visible on the site, refreshed every generation for free, and acted on by a strict promotion rule. Reading 2 (ruled out): rebuild the bench: steps 1-3 are built (2,092 rows, test_models_systemone and test_louhi_models pass).
## Assumptions (confidence)
## Acceptance criteria
- [x] The site's Benchmarks page has a Models section from research/models/bench.jsonl: per backend and use the latest complete run's accuracy, Brier, p50 and p95 latency, rows and timeout, beside the rules path and the majority baseline; a partial or failed run never replaces it (the section says stale since gen N) — verify with `python3 plugin/tests/run.py test_site_build test_louhi_models test_night`
- [x] Every Rune generation reruns the bench as a $0 local night job under the GPU lock, never beside moons grow; a backend down, a timeout or a busy GPU is recorded as skipped and the last good rows stay — verify with `python3 plugin/tests/run.py test_site_build test_louhi_models test_night`
- [x] The promotion rule: a backend goes live for a use only on at least 200 rows of a frozen held-out set (task ids pinned at gen 4, the rolling set shown beside it), beating the rules path and the majority baseline by at least 5 points (paired p < 0.05) with Brier no worse; a decision row cites the run; demoted when a later run falls under; rows closed after it went live never judge it; the noise ceiling from re-tiered tasks shown beside accuracy — verify with `python3 plugin/tests/run.py test_site_build test_louhi_models test_night`
## Non-goals
## Approach (options → choice → why)
1) use what exists: bench.jsonl as the source, the site's Benchmarks page builder (site/pages.py, build.py), night.py's job list and its GPU lock, decide()'s live switch with decision rows: likely outcome: small additions to proven parts. 2) a separate dashboard: fails if: a second place for the same numbers. 3) promote by hand: fails if: the user asked for it to run itself. 4) do less: the section only: fails if: no rerun and no promotion. Choice 1 (85%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/lib/sampo/cli.py, plugin/tests/test_site.py, site/style.css; past FIXes T-1371, T-2060, T-2061, T-2064, T-2087.
## Execution prompt
Read T-2886's brief (state/projects/foreman-4a056f/tasks/T-2886-model-bench-every-local-backend-ollama-decision.md) first: its Approach, the dissent answers and the log say what is built. The site is the forge site (site/index.html with a Benchmarks page; find where its pages are built). Rows: research/models/bench.jsonl (arm, use, backend, accuracy, Brier, latency fields; read a few). Frozen held-out set: pin the task ids the bench's held-out split holds today into a file under research/models/, and keep the rolling set beside it. Promotion acts through the existing live switch for decide() backends; read models.py and louhi.py for how a backend is made live. The noise ceiling: tasks whose type or tier changed after creation (the ledger's task_set events) give the label-disagreement rate. Never use Claude-written labels.
## Steps
1. [x] the Models section (tests first)
2. [x] the per-generation $0 rerun with the GPU lock and last-good rows (tests first)
3. [x] the promotion and demotion rule with decision rows and the frozen set (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T02:10:34Z step 2/3: the per-generation $0 rerun with the GPU lock and last-good rows (tests first)
- git: worktree-agent-a1c3b4d31b1174236; 5 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/night.py, plugin/tests/test_louhi_models.py, plugin/tests/test_night.py
- touched since last checkpoint: plugin/tests/test_louhi_models.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/night.py, plugin/tests/test_night.py
## Docs impact
the site's Benchmarks page carries the Models section; CHANGELOG had its line at merge
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_louhi_models 2>&1 | tail -40` → exit 0 · Ran 27 tests in 17.0s (3 classes, 16 at a time; slowest: LouhiModels 15s, ModelBenchVisible 3s, LouhiLoo 1s) / OK [ran] [tree 26687a7bf3f6] [world 2f1906870a] (2026-11-05T02:09:49Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night 2>&1 | tail -30` → exit 0 · Ran 92 tests in 16.5s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 13s, NightTick 4s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:12:12Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night 2>&1 | tail -30` → exit 0 · Ran 92 tests in 16.5s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 13s, NightTick 4s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:12:12Z)
- (ac 3) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night 2>&1 | tail -30` → exit 0 · Ran 92 tests in 16.5s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 13s, NightTick 4s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:12:12Z)
- (step 2) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night 2>&1 | tail -30` → exit 0 · Ran 92 tests in 16.5s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 13s, NightTick 4s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:12:12Z)
- (step 1) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · Ran 92 tests in 16.7s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 13s, NightGuards 5s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:12:33Z)
- (step 2) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · Ran 92 tests in 16.6s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 13s, NightTick 5s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:12:50Z)
- (step 3) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · Ran 92 tests in 16.8s (28 classes, 16 at a time; slowest: LouhiModels 16s, Night 14s, NightTick 4s) / OK [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:13:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_exam test_fmpy test_genesis test_goal test_left_out test_louhi_models test_map test_mint test_models test_moons_scale test_moonshot test_motion_verify test_night test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [33.44s] [ran] [tree 87ccc1b9d855] [world 2f1906870a] (2026-11-05T02:18:16Z)
- `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · Ran 93 tests in 18.6s (29 classes, 16 at a time; slowest: LouhiModels 18s, Night 15s, NightTick 6s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:37:28Z)
- `python3 plugin/tests/run.py test_louhi_models` → ✗ exit 1 · Ran 27 tests in 15.9s (3 classes, 16 at a time; slowest: LouhiModels 14s, ModelBenchVisible 3s, LouhiLoo 1s) / FAILED (1 classes: test_louhi_models.ModelBenchVisible) (start tree + this task's tests) [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:38:25Z)
- `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 27 tests in 13.9s (3 classes, 16 at a time; slowest: LouhiModels 13s, ModelBenchVisible 3s, LouhiLoo 1s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:38:25Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:37:28Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:38:32Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:37:28Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:38:32Z)
- (ac 3) `python3 plugin/tests/run.py test_site_build test_louhi_models test_night` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:37:28Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:38:32Z)
- (audit intent) `builder lane reviewed and merged (40743659); criteria re-run on main green (93 tests); red→green proved on test_louhi_models` → the model bench's visible half: a Models section on the site's Benchmarks page, a $0 rerun every Rune generation, and the promotion rule with decision rows [tree 9ff1569cf979] (2026-11-05T07:38:32Z)
- (audit edge) `builder lane reviewed and merged (40743659); criteria re-run on main green (93 tests); red→green proved on test_louhi_models` → no bench rows yet renders the section's empty state; a model below the bar is listed but never promoted [tree 9ff1569cf979] (2026-11-05T07:38:32Z)
## Log
- 2026-11-05T02:02:06Z created
- 2026-11-05T02:02:07Z set approved=True
- 2026-11-05T02:02:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3093.builder.md
- 2026-11-05T02:02:21Z focused
- 2026-11-05T02:02:22Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T02:06:31Z focused
- 2026-11-05T02:10:06Z scope: plugin/lib/sampo/cli.py gets one --night flag for exam models run
- 2026-11-05T03:35:29Z gate hold 2026-11-05 03:5x: SubagentStop +22%, TaskCompleted +72%, PreCompact +16%, SubagentStart +67%; the diff (louhi +251, night NAMES +1, cli +2, site) adds nothing on those hooks' paths; the noise pattern of T-3091's 8 holds; retried at the end of the queue at lower load
- 2026-11-05T05:54:37Z merged worktree-agent-a1c3b4d31b1174236 (8 file(s))
- 2026-11-05T05:54:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1c3b4d31b1174236
- 2026-11-05T07:36:55Z focused
- 2026-11-05T07:37:29Z scope: files outside its globs came from other tasks' merges and closes landing between its merge (40743659) and this close
- 2026-11-05T07:43:48Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2886 [FEATURE L, blocked, 5 steps] Model bench: every local backend (Ollama decision models, Jeff, SelfJev, embedders, generators) measured on Sampo's own work with an…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-11-03: [outward] [revisited: Kirjokansi fused with Ilmarinen's forge] [cites: user steer 2026-11-03: I kind of just like number 1, but way better, more ani…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.p…
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/louhi.py, plugin/lib/sampo/night.py, plugin/tests/test_louhi_models.py, plugin/tests/test_night.py, plugin/tests/test_site_build.py, site/build.py, site/pages.py; re-ground the plan against them before editing
## Lessons
- A model is promoted only by a held-out bar it clears; Jeff's 26% vs the constant guess's 37% shows why the bar is needed
## Files touched
- plugin/tests/test_louhi_models.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/night.py
- plugin/tests/test_night.py
- site/pages.py
- site/build.py
- plugin/tests/test_site_build.py
