---
id: T-2886
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: [T-3093]
source: user
created: 2026-11-04T03:52:03Z
updated: 2026-11-06T03:53:23Z
base: 5de167c784f44cc82a9dc40f1f944a571df03532
---
# Model bench: every local backend (Ollama decision models, Jeff, SelfJev, embedders, generators) measured on Sampo's own work with and without it, as a Louhi arm; numbers on the site's Models section; rerun every Rune generation
## Raw request
> Model bench: every local backend (Ollama decision models, Jeff, SelfJev, embedders, generators) measured on Sampo's own work with and without it, as a Louhi arm; numbers on the site's Models section; rerun every Rune generation
## Interpretation
Reading 1 (taken): every local backend measured on Sampo's own labelled work with and without it (built), its numbers on the site's Models section (to build), rerun every Rune generation (to build), and winners promoted to live with decision rows (to build). Reading 2 (ruled out): public benchmarks (MMLU, HumanEval): they say nothing about whether a model helps Sampo decide a tier or dedupe a moon.
## Assumptions (confidence)
## Acceptance criteria
- [ ] decide() answers through a systemone backend (Ollama's /v1/systemone, Jeff, SelfJev), only listed choices and probabilities taken — verify with `python3 plugin/tests/run.py test_models_systemone`
- [ ] sampo louhi models runs the decision arm (intake type and tier from held-out closed tasks) and the embedding arm (title-to-brief recall) and records accuracy, calibration and latency per backend — verify with `python3 plugin/tests/run.py test_louhi_models`
- [ ] the generation arm records ideas yield through the moons funnel and Smith's seed pass rate per model — verify with `python3 plugin/tests/run.py test_louhi_models`
- [ ] The site's Models section (on the Benchmarks page the forge site already has) shows the latest complete run per backend and use: accuracy, Brier, p50/p95 latency, rows and each row's timeout, beside the rules path and the majority baseline; a partial or failed run never replaces it: the section says 'stale since gen N' instead — verify with `python3 plugin/tests/run.py test_site_build test_louhi_models`
- [ ] Every Rune generation reruns the bench as a $0 local job that takes the GPU lock and never runs beside moons grow; a run with a backend down, a timeout or a busy GPU records what it skipped and keeps the last good rows — verify with `python3 plugin/tests/run.py test_louhi_models test_night`
- [ ] Promotion has a rule: a backend goes live for a use only when, on at least 200 held-out rows of a frozen held-out set (task ids pinned at gen 4, plus the rolling set shown beside it), it beats both the rules path and the majority baseline by at least 5 points (paired test, p < 0.05) with a Brier score no worse; a decision row cites the run; it is demoted when a later run falls under; rows closed after a model went live are excluded from judging that model — verify with `python3 plugin/tests/run.py test_louhi_models`
## Non-goals
Public benchmarks; fine-tuning (Jeff's trainer is a later Jevlike task); changing any live decision path before the bench shows a win.
## Approach (options → choice → why)
1) use what exists (most of it): the bench (sampo exam models, research/models/bench.jsonl, its arms) is built; what remains reads it: a Models section on the site from the latest row per backend and use, a Rune stage that reruns the bench each generation (local models only, /usr/bin/bash, in the night's job list), and a promotion step that makes a backend live for a use only when it beats the rules path and the majority baseline on held-out rows, with a decision row citing the run: likely outcome: the numbers visible and acted on. 2) rebuild the bench as one verb: fails if: throws away 2,092 rows and four merged tasks. 3) site only: fails if: the numbers go stale and never change what runs. 4) do less: mark the built criteria done and drop the rest: fails if: the user asked for the site numbers and a rerun every generation. Choice 1 (85%).
## Risks and rollback
GPU contention: the arms run one backend at a time, local-first, with a job cap, never beside grow on the same server. Held-out leakage: the split is by a task-id hash, and no prompt shows a held-out label. Noisy labels: a 50-row hand check bounds the ceiling. Rollback: the arm is additive; the systemone kind is used only by profiles that name it; the live switch keeps needing a decision row.
## Execution prompt
## Steps
1. [x] systemone backend kind and local profiles (lane A)
2. [x] Louhi models arm: decision and embedding arms, held-out split, metrics, results file (lane A)
3. [x] generation arm: ideas yield per model and Smith seeds with timeouts sized to the model (lane B)
4. [ ] site Models section, per-generation $0 rerun (child T-3093, M, in a lane)  <- CURRENT
5. [ ] promotion and demotion rule (child T-3093)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models_systemone test_louhi_models` → exit 0 · Ran 25 tests in 25.4s (3 classes, 16 at a time; slowest: LouhiModels 25s, LouhiLoo 3s, Systemone 0s) / OK [ran] [tree f78e3fa0e0e2] [world 2f1906870a] (2026-11-05T00:51:08Z)
- (step 2) `python3 plugin/tests/run.py test_models_systemone test_louhi_models` → exit 0 · Ran 25 tests in 30.1s (3 classes, 16 at a time; slowest: LouhiModels 30s, LouhiLoo 2s, Systemone 0s) / OK [ran] [tree f78e3fa0e0e2] [world 2f1906870a] (2026-11-05T00:55:44Z)
- (step 3) `python3 plugin/tests/run.py test_models_systemone test_louhi_models` → exit 0 · Ran 25 tests in 66.8s (3 classes, 16 at a time; slowest: LouhiModels 66s, LouhiLoo 5s, Systemone 1s) / OK [ran] [tree f78e3fa0e0e2] [world 2f1906870a] (2026-11-05T00:57:42Z)
## Log
- 2026-11-04T03:52:03Z created
- 2026-11-04T03:52:47Z set approved=True
- 2026-11-05T00:50:31Z grounded 2026-11-04: steps 1-3 were built under T-2894 (generation arm, baselines), T-2975 (retrieval rows), T-2976 (leave-one-project-out) and earlier lanes: test_models_systemone and test_louhi_models pass; research/models/bench.jsonl holds 2,092 rows (loo 2,016, decision 50, verifier 12, embedding 10, retrieval 4). Not built: the site's Models section, the per-generation rerun, promoting winners
- 2026-11-05T00:51:08Z start point recorded late (no focus had kept one): its diff starts at 5de167c
- 2026-11-05T00:58:26Z criterion 4 verify: `python3 plugin/tests/run.py test_site_build test_genesis` → `python3 plugin/tests/run.py test_site_build test_louhi_models`
- 2026-11-05T00:58:26Z criterion 4 text: the site's Models section and every Rune generation show the latest run → The site's Models section (on the Benchmarks page the forge site already has) shows the latest complete run per backend and use: accuracy, Brier, p50/p95 latency, rows and each row's timeout, beside the rules path and the majority baseline; a partial or failed run never replaces it: the section says 'stale since gen N' instead
- 2026-11-05T00:58:27Z step 4 text: site Models section and the tower's per-generation rerun, after the site port merges → site Models section on the Benchmarks page and the per-generation $0 rerun (GPU lock, never beside grow, last good rows kept)
- 2026-11-05T00:58:28Z step 5 text: run the full lineup; promote winners to live with decision rows citing the run → promotion and demotion under the rule (≥200 frozen held-out rows, +5 points, p<0.05, Brier no worse), decision rows citing the run; the noise ceiling from re-tiered tasks shown beside accuracy
- 2026-11-05T02:02:18Z step 4 text: site Models section on the Benchmarks page and the per-generation $0 rerun (GPU lock, never beside grow, last good rows kept) → site Models section, per-generation $0 rerun (child T-3093, M, in a lane)
- 2026-11-05T02:02:19Z step 5 text: promotion and demotion under the rule (≥200 frozen held-out rows, +5 points, p<0.05, Brier no worse), decision rows citing the run; the noise ceiling from re-tiered tasks shown beside accuracy → promotion and demotion rule (child T-3093)
- 2026-11-05T02:02:19Z set depends_on=['T-3093']
- 2026-11-05T02:02:19Z blocked: steps 4-5 are T-3093, building in a lane
- 2026-11-06T03:53:23Z unblocked
## Follow-ups captured
## Build vs reuse
Reuse: louhi (held-out hashing, run ids, scorecard shape), models (decide, registry, complete, embed, shadow uses, live()), moonscale (admit, the funnel's kill and tier stages), smithbench (seeds), core (briefs). Build: the systemone backend kind, the models arm with its decision, embedding and generation sub-arms, the results file, the site section, the per-generation stage. Nothing outside fits: lm-eval-harness and promptfoo would need installs and grade other tasks than Sampo's.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Step 4 is gated on "after the site port merges" with no check that the port exists or when it lands, and the criterion `test_site_build test_genesis` can't pass until it does. Step 5 depends on step 4, so the whole task can stall. — Name the port's task ID and state. Build the Models section …
- HIGH: Promotion rule is underspecified, and step 5 has no acceptance criterion. "Beats the rules path and majority baseline on held-out rows" has no margin, minimum row count, or calibration condition. With about 2,092 rows split by task-id hash, small gains will be noise, so a model could be promo…
- HIGH: Rerunning the bench every Rune generation conflicts with the "never beside grow on the same server" and job-cap risk mitigation. Nothing says what happens when the bench times out, a backend is down, or the GPU is busy. A failed or partial run could blank the site's Models section or write pa…
- MEDIUM: Held-out leakage is addressed only for prompts. Rune generations produce new tasks, and "the latest run" gets compared across generations, so the held-out set shifts and numbers aren't comparable over time. Also, if promoted models later influence which tasks get closed or labelled, labels …
- MEDIUM: The "50-row hand check bounds the ceiling" is mentioned in risks but isn't a step or criterion, so it may never happen. And it isn't clear who does it. — Make it a step with an owner and a stored artifact, and have the site display the ceiling next to the accuracy numbers.
- LOW: The criteria for the generation arm (ideas yield, Smith seed pass rate) are checked only by unit tests, which can't show those metrics are meaningful across models of different speeds, given timeouts "sized to the model". Timeouts that differ per model can bias the pass rate. — Record timeout …
Verdict: revise — the built parts are sound, but the remaining work has a blocking dependency, no concrete promotion criterion, and unspecified failure behavior for a per-generation job that feeds the public site.
## Dissent
- [x] HIGH: Step 4 is gated on "after the site port merges" with no check that the port exists or when it lands, and the criterion `test_site_build test_genesis` can't pass until it does. Step 5 depends on step 4, so the whole task can stall. — Name the port's task ID and state. Build the Models section … — answered: adopted: the site port has landed (the forge site with a Benchmarks page, commits ea432bd0, ce3234ff); the Models section goes there, no gate
- [x] HIGH: Promotion rule is underspecified, and step 5 has no acceptance criterion. "Beats the rules path and majority baseline on held-out rows" has no margin, minimum row count, or calibration condition. With about 2,092 rows split by task-id hash, small gains will be noise, so a model could be promo… — answered: adopted: a promotion criterion: ≥200 frozen held-out rows, +5 points over both the rules path and the majority baseline, paired p<0.05, Brier no worse, demotion when a later run falls under
- [x] HIGH: Rerunning the bench every Rune generation conflicts with the "never beside grow on the same server" and job-cap risk mitigation. Nothing says what happens when the bench times out, a backend is down, or the GPU is busy. A failed or partial run could blank the site's Models section or write pa… — answered: adopted: the per-generation rerun is a $0 local job under the GPU lock, never beside moons grow; a failed or partial run records what it skipped and keeps the last good rows; the site says stale sinc…
- [x] MEDIUM: Held-out leakage is addressed only for prompts. Rune generations produce new tasks, and "the latest run" gets compared across generations, so the held-out set shifts and numbers aren't comparable over time. Also, if promoted models later influence which tasks get closed or labelled, labels … — answered: adopted: a frozen held-out set pinned at gen 4 for comparisons over time, the rolling set beside it; rows closed after a model went live are excluded from judging that model
- [x] MEDIUM: The "50-row hand check bounds the ceiling" is mentioned in risks but isn't a step or criterion, so it may never happen. And it isn't clear who does it. — Make it a step with an owner and a stored artifact, and have the site display the ceiling next to the accuracy numbers. — answered: adopted differently: no Claude-written hand labels (models learn and are judged only on outcomes and the user's words); the noise ceiling is estimated from tasks whose type or tier was changed after …
- [x] LOW: The criteria for the generation arm (ideas yield, Smith seed pass rate) are checked only by unit tests, which can't show those metrics are meaningful across models of different speeds, given timeouts "sized to the model". Timeouts that differ per model can bias the pass rate. — Record timeout … — answered: adopted: each row records its timeout, and the Models section shows it
