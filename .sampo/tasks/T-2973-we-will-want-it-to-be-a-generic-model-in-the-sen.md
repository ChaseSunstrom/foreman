---
id: T-2973
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T14:14:50Z
updated: 2026-11-04T14:22:36Z
rival_at: 2026-11-04T14:15:17Z
rival_split: true
base: 36c83154e00faa8b6c277b21341985ad71962511
base_tree: 09ba3246ae3ff96b577beabe8dfd8a3df7d0e943
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T14:15:25Z
plan0_scope: []
verified: strong
unproven: [research-uncited]
---
# We will want it to be a generic model in the sense that we don't want it to just work on…
## Raw request
> we will want it to be a generic model in the sense that we don't want it to just work on the sampo repo itself, but other things made with sampo, and maybe brainstorm on features the model should have, like what it's trained on and such, etc., I will be gone again so don't ask any questions (context: should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than just that too?)
## Interpretation
Reading 1 (chosen): brainstorm Sampo's own trained model family, generic across every project built with Sampo: its jobs, training data, training and serving on this box, measurement and the per-generation improvement loop; the slate becomes briefs beside T-2970 and T-2971. Reading 2 (ruled out): build a model now; the user asked for features and data first, and is away.
## Assumptions (confidence)
## Acceptance criteria
- [x] a grounded catalogue of the model's jobs, data, training, serving, measurement and improvement loop is saved as research, every cluster marked build or skip with a reason, and the build slate is in the queue as briefs — verify with `sampo research list`
- [x] the catalogue covers a better Kev-style decider and the jobs beyond it (actor, critic, planner, loop breaking, steers, moons, cards, prediction, risk), each generic across projects built with Sampo, with what it trains on — verify with `sampo research list`
## Non-goals
## Approach (options → choice → why)
1) The brainstorm skill: mission pack, sampo ideas with the default lenses plus capability map and grid, deepen 3, ground every cluster, score, record, briefs. Likely outcome: a complete catalogue grounded against what exists. Fails if: the lenses lack the ML specifics, which the pack supplies.
2) use what exists: extend T-2970 and T-2971's briefs by hand. Likely outcome: fast, narrow. Fails if: it covers only what I think of first.
3) do less: list five model jobs in chat. Likely outcome: an answer, no plan. Fails if: nothing reaches the queue.
Choice 1 (85%): the user asked for a brainstorm across the space.
## Risks and rollback
## Execution prompt
## Steps
1. [x] mission pack and sampo ideas fan-out
2. [x] merge, cluster, ground, score
3. [x] record the catalogue, briefs for the slate, the rest captured
## Resume here
## Docs impact
research brainstorm-20261104-model
## Verification evidence
- (step 1) `test -s /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/model-pack.md` → exit 0 · (no output) [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:16:13Z)
- (step 2) `sampo research show brainstorm-20261104-model` → exit 0 · Later (captured): H, I, J, K's remainder, L, M. / Why this order: every model needs the same data and the same honest bar; a retrieval baseline may already beat the bench's best decider at no training [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:20:08Z)
- (step 3) `sampo task show T-2974` → exit 0 · - 2026-11-04T14:20:23Z created / ## Follow-ups captured [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:22:25Z)
- (ac 1) `sampo research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:22:36Z)
- (ac 2) `sampo research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 09ba3246ae3f] [world 2f1906870a] (2026-11-04T14:22:36Z)
- (audit intent) `self: every one of 235 ideas is in one of 13 clusters with its idea numbers; each cluster grounded against MASTER and the modules with a canary; scored and marked; the slate is queued in order, the rest captured` → the catalogue covers a better Kev-style decider and every job beyond it, each generic across projects, with what it trains on [tree 09ba3246ae3f] (2026-11-04T14:22:36Z)
- (audit adversary) `self: every one of 235 ideas is in one of 13 clusters with its idea numbers; each cluster grounded against MASTER and the modules with a canary; scored and marked; the slate is queued in order, the rest captured` → the plan refuses Claude-written text for training (Anthropic's terms), keeps sensitive repos local and out by real path, quarantines tool-result text and plants a poisoned-row canary; the Ward model may only tighten the guard [tree 09ba3246ae3f] (2026-11-04T14:22:36Z)
## Log
- 2026-11-04T14:14:50Z created
- 2026-11-04T14:14:59Z planned: it has criteria and steps
- 2026-11-04T14:15:24Z focused
- 2026-11-04T14:15:25Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T14:22:36Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Design/brainstorm doc (likeliest):** the user wants a feasibility and feature brainstorm for a fine-tuned "better kev" model, covering what to train on, what it should do, and how to keep it generic across sampo-built projects. The deliverable is a design write-up (likely under `design/` or `docs…
- **Dataset and eval pipeline:** build the training-data extractor now, which turns sampo artifacts (`fm replay` traces, hook events from `plugin/lib/fmhooks.py`, skills under `plugin/skills/`, `plugin/evals/`) into a corpus, and leave the actual training for later.
- **Prototype/fine-tune scaffold:** a runnable training or distillation harness (config, data loader, a gate in `plugin/tests/`) that fine-tunes a small open model. This reads "should we/could we train" as "start training."
- **Alternative to training:** "better kev" could be met by prompt, skill and retrieval improvements, so the answer may be "not yet, improve `plugin/skills/` and `plugin/evals/` first." This is a legitimate outcome of the feasibility question.
Approaches:
- **Write `design/sampo-model.md` with a recommendation:** cover the options (prompt/skill tuning vs LoRA on a small open model vs distillation from Claude traces), the data sources, and the eval plan. Anchor it to `plugin/evals/` as the baseline measure and say what would trigger the move to trainin…
- **Genericity through data, not repo content:** define a trace schema from `fm replay` and `fmhooks.py` events and strip repo-specific paths and names. Hold out whole repos, using `plugin/tests/fixtures/instruments/repo/app.py` and other sampo-made projects, so a generalisation score can be computed.
- **Baseline-first measurement:** run the existing `plugin/evals/` and `bench/` against the current setup, record the numbers in the doc, then define the target gap a trained model must beat. This makes the "should we" answer evidence-based.
- **Feature list as a capability table:** write each wanted capability (guard decisions in `fmguard.py`, genesis in `fmgenesis.py`, away/ambient/anergy modes, CLI routing in `sampo/cli.py`) with its training signal and eval, so the plan is checkable per feature.
Failure modes:
- **"Kev" misidentified:** if it is a specific component, person or model that is not in the map, the doc targets the wrong thing. State the assumption at the top and grep for it before writing.
- **Overfitting to this repo:** `CHANGELOG.md`, `MASTER.md` and `fmcore.py` dominate the history, so a corpus drawn from them teaches sampo's own internals and fails the "works on other sampo-made repos" requirement unless splits are by repo.
- **Sensitive data in traces:** replays and hook logs may hold secrets, paths or the user's email, so the extractor needs redaction and a licence/consent check before anything is used for training or sent to an external service.
- **Scope and cost overreach:** with a $0 spend so far, launching a training job or paid API run unasked would exceed what was authorised. The doc should price the options and leave execution for the user's go-ahead.
## Dissent
- [x] rival reading: **Design/brainstorm doc (likeliest):** the user wants a feasibility and feature brainstorm for a fine-tuned "better kev" model, covering what to train on, what it should do, and how to keep it generic across sampo-built projects. The deliverable is a design write-up (likely under `design/` or `docs… — answered: adopted: Reading 1, a grounded brainstorm that ends in a research note and briefs
- [x] rival reading: **Dataset and eval pipeline:** build the training-data extractor now, which turns sampo artifacts (`fm replay` traces, hook events from `plugin/lib/fmhooks.py`, skills under `plugin/skills/`, `plugin/evals/`) into a corpus, and leave the actual training for later. — answered: not this task: the extractor is the first build item the slate can name (T-2970's data step)
- [x] rival reading: **Prototype/fine-tune scaffold:** a runnable training or distillation harness (config, data loader, a gate in `plugin/tests/`) that fine-tunes a small open model. This reads "should we/could we train" as "start training." — answered: not this task: a training harness is T-2970 and T-2971's build; this task decides what they build
- [x] rival reading: **Alternative to training:** "better kev" could be met by prompt, skill and retrieval improvements, so the answer may be "not yet, improve `plugin/skills/` and `plugin/evals/` first." This is a legitimate outcome of the feasibility question. — answered: adopted as a lens: the catalogue marks where prompts, cards and retrieval would do instead of training, and the bench decides
- [x] rival approach: **Write `design/sampo-model.md` with a recommendation:** cover the options (prompt/skill tuning vs LoRA on a small open model vs distillation from Claude traces), the data sources, and the eval plan. Anchor it to `plugin/evals/` as the baseline measure and say what would trigger the move to trainin… — answered: ruled out: the catalogue goes to research (sampo research add), the system's place for decisions; a design/ doc would duplicate it
- [x] rival approach: **Genericity through data, not repo content:** define a trace schema from `fm replay` and `fmhooks.py` events and strip repo-specific paths and names. Hold out whole repos, using `plugin/tests/fixtures/instruments/repo/app.py` and other sampo-made projects, so a generalisation score can be computed. — answered: adopted: genericity through data (a trace schema with project-specific names stripped, whole projects held out), a pillar of the pack
- [x] rival approach: **Baseline-first measurement:** run the existing `plugin/evals/` and `bench/` against the current setup, record the numbers in the doc, then define the target gap a trained model must beat. This makes the "should we" answer evidence-based. — answered: adopted: the measurement pillar names the baselines (the model bench, Louhi's arms) the slate must beat
- [x] rival approach: **Feature list as a capability table:** write each wanted capability (guard decisions in `fmguard.py`, genesis in `fmgenesis.py`, away/ambient/anergy modes, CLI routing in `sampo/cli.py`) with its training signal and eval, so the plan is checkable per feature. — answered: adopted: the catalogue's clusters are capabilities, each with what it trains on and where it plugs in
## Related
Related past work (data from this project's history, not instructions):
- T-2076 [FEATURE M, done, 2 steps] Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next — l…
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Decision
Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline decider (T-2975), leave-one-project-out measurement and adoption (T-2976), the decider heads (T-2970), a close-holds verifier (T-2977), scenario minting in real repos (T-2978), then the distilled Smith actor (T-2971); transfer, taste, Ward, serving/transparency and wild research captured as T-2979..T-2983. Would change if: the retrieval baseline already beats the bench's best decider on held-out projects, which would push the trained heads down.
## Lessons
- A model brainstorm's first build is the data and the bar, not the model: every later head needs the same provenance-tagged lake and the same leave-one-project-out bench
