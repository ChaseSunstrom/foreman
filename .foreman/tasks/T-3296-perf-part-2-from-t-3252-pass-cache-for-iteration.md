---
id: T-3296
type: PERFORMANCE
tier: L
status: planned
priority: normal
scope: [plugin/tests/run.py, plugin/tests/perf_bench.py, plugin/lib/sampo/works.py, plugin/lib/sampo/shot.py, plugin/lib/sampo/night.py, plugin/lib/sampo/models.py, plugin/tests/test_pass_cache.py, plugin/tests/test_slots.py, plugin/tests/test_design_works.py, research/perf/, CHANGELOG.md]
depends_on: [T-3297, T-3270]
source: user
created: 2026-11-06T02:55:22Z
updated: 2026-11-06T03:08:11Z
---
# PERF part 2 (from T-3252): pass cache for iteration runs, one browser per run, SCHED_IDLE generators, model thread caps, and the before/after bench
## Raw request
> PERF part 2 (from T-3252): pass cache for iteration runs, one browser per run, SCHED_IDLE generators, model thread caps, and the before/after bench
## Interpretation
Reading 1 (chosen): the rest of T-3252 after part 1 (T-3297: slot pool, fork server, bench, lane ceiling): a pass cache so iteration runs (check --affected, evidence runs) skip a test class whose inputs haven't changed, while ship and post-merge gates always run in full; one browser shared per run for works and page tests instead of a launch per check; generators (moons, cards, night) at SCHED_IDLE by default; local model servers' CPU threads capped when the model sits fully on the GPU (measured 200% CPU); and an ABAB before/after bench. The user lifted the CPU limit on 2026-11-06, so the goal is throughput and correctness under many parallel lanes, not a cap. T-3270 (ambient verdict reuse by tree id, in a lane) overlaps the pass cache: build on it. Reading 2 (ruled out): drop part 2 since CPU no longer matters. Ruled out because the same waste is what made ~20 lanes thrash at load 250 and fail timing tests.
## Assumptions (confidence)
## Acceptance criteria
- [ ] an unchanged test class is not re-run by check --affected or evidence runs across worktrees, while ship and post-merge gates always run in full — verify with `python3 plugin/tests/run.py test_pass_cache`
- [ ] works and page tests share one browser per run; moons, cards and night run SCHED_IDLE by default — verify with `python3 plugin/tests/run.py test_slots test_design_works`
- [ ] llama-server and Ollama models fully on the GPU run with their CPU threads capped (measured: 200% CPU before) — verify with `python3 plugin/tests/run.py test_slots`
- [ ] a before/after bench with the slot pool, run ABAB on a comparable machine state, recorded in research/perf/bench.jsonl, keeping only what won — verify with `python3 plugin/tests/run.py test_perf_bench`
- [ ] a changed helper module, fixture file or run.py makes a cached class run again; a run without --pass-cache (ship, post-merge, full check) never reads the cache, even with an env flag set — verify with `python3 plugin/tests/run.py test_pass_cache`
## Non-goals
## Approach (options → choice → why)
1. Pass cache, opt-in per invocation: run.py consults it only when its caller passes --pass-cache (check --affected and task evidence do; ship, post-merge verify and full sampo check never do, and run.py ignores any env flag). The key is content-addressed: the class's test file, every module it imported (recorded from sys.modules after its run), the fixture/data files under plugin/tests it opened, run.py itself and the Python version; a pass for a key is valid in any worktree. One file per key, written atomically (tmp + rename), so 20 lanes can't corrupt it. Then one shared browser per run with a fresh context per check and a relaunch after a crash; SCHED_IDLE for moons, cards and night; model-server thread caps only when the server reports every layer on the GPU. Bench ABAB last, 3 repetitions per arm, keep a change only above a 10% win. Likely outcome: iteration runs drop to the classes a change reaches, with no stale green in a gate.
2. Reuse T-3270's tree-id verdict only. Likely outcome: helps only when nothing at all changed; fails if: one unrelated edit invalidates everything.
3. Cache at module granularity by mtime. fails if: an edited helper a class imports leaves a stale pass.
4. Do less: only SCHED_IDLE and thread caps. Likely outcome: small, safe; leaves the biggest waste in place.

Choice 1 (82%): a content-addressed, opt-in cache can't feed a gate, and the key covers imports, data files and the runner. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] pass cache for iteration runs only  <- CURRENT
2. [ ] one browser per run; SCHED_IDLE generators; model thread caps
3. [ ] bench after, ABAB: record before and after, keep only what won
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T02:55:22Z created
- 2026-11-06T03:07:05Z set depends_on=['T-3297', 'T-3270'], scope=['plugin/tests/run.py', 'plugin/tests/perf_bench.py', 'plugin/lib/sampo/works.py', 'plugin/lib/sampo/shot.py', 'plugin/lib/sampo/night.py', 'plugin/lib/sampo/models.py', 'plugin/tests/test_pass_cache.py', 'plugin/tests/test_slots.py', 'plugin/tests/test_design_works.py', 'research/perf/', 'CHANGELOG.md']
- 2026-11-06T03:08:11Z plan review (sampo second plan) folded in: opt-in per invocation, content-addressed key incl. data files and run.py, atomic per-key files, browser fresh context + relaunch, GPU-layer rule for thread caps, bench 3x per arm with a 10% bar
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The pass-cache key (import closure + test file hashes) omits non-import inputs: fixtures, data files, config, env vars, plugin/tests/run.py itself, Python version, installed deps, and dynamically loaded modules (importlib, subprocess-spawned scripts, files read at runtime). A stale pass could…
- HIGH: Criterion 1 says "across worktrees" but nothing in the plan says where the cache lives or how it's shared safely. Concurrent lanes (~20) writing one store risks corrupt or racy entries, and a pass cached from a lane with uncommitted or different state could be served to another. — Specify a c…
- HIGH: "Ship and post-merge gates always run in full" is enforced only by an env flag that check --affected and evidence set. If the flag leaks (inherited env, a wrapper), or a gate forgets to clear it, the cache bypasses gates silently. The safe default is inverted. — Make caching opt-in per invoca…
- MEDIUM: Several criteria can't prove the request. "Unchanged class not re-run" has no stated negative case (changed helper → rerun), and the thread-cap criterion verifies via test_slots, but the claim is about measured CPU on real GPU-resident models, which a unit test can't show. SCHED_IDLE and sh…
- MEDIUM: Shared browser per run introduces test isolation risks (cookies, storage, crashed page poisoning later tests, parallel pages in one process) and no fallback is described. Also the thread cap has no rule for deciding "fully on GPU" and could slow models that partially offload. — Use a fresh …
- LOW: Bench risk: with the CPU limit lifted, ABAB "comparable machine state" is hard at load up to 250, and "keep only what won" with no threshold or sample count invites noise-driven decisions. Steps also give no rollback beyond that. — Define N repetitions, a win threshold, and report variance; la…
Verdict: revise — the cache-safety gaps (key completeness, concurrent shared store, opt-out gate enforcement) could produce false greens, so fix those before implementation.
## Dissent
- [ ] HIGH: The pass-cache key (import closure + test file hashes) omits non-import inputs: fixtures, data files, config, env vars, plugin/tests/run.py itself, Python version, installed deps, and dynamically loaded modules (importlib, subprocess-spawned scripts, files read at runtime). A stale pass could…
- [ ] HIGH: Criterion 1 says "across worktrees" but nothing in the plan says where the cache lives or how it's shared safely. Concurrent lanes (~20) writing one store risks corrupt or racy entries, and a pass cached from a lane with uncommitted or different state could be served to another. — Specify a c…
- [ ] HIGH: "Ship and post-merge gates always run in full" is enforced only by an env flag that check --affected and evidence set. If the flag leaks (inherited env, a wrapper), or a gate forgets to clear it, the cache bypasses gates silently. The safe default is inverted. — Make caching opt-in per invoca…
- [ ] MEDIUM: Several criteria can't prove the request. "Unchanged class not re-run" has no stated negative case (changed helper → rerun), and the thread-cap criterion verifies via test_slots, but the claim is about measured CPU on real GPU-resident models, which a unit test can't show. SCHED_IDLE and sh…
- [ ] MEDIUM: Shared browser per run introduces test isolation risks (cookies, storage, crashed page poisoning later tests, parallel pages in one process) and no fallback is described. Also the thread cap has no rule for deciding "fully on GPU" and could slow models that partially offload. — Use a fresh …
- [ ] LOW: Bench risk: with the CPU limit lifted, ABAB "comparable machine state" is hard at load up to 250, and "keep only what won" with no threshold or sample count invites noise-driven decisions. Steps also give no rollback beyond that. — Define N repetitions, a win threshold, and report variance; la…
