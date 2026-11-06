---
id: T-2893
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T04:07:09Z
updated: 2026-11-04T04:20:59Z
rival_at: 2026-11-04T04:07:37Z
rival_split: true
builder: 2026-11-04T04:08:00Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|14305|50467
lane: ~/.claude/foreman/.claude/worktrees/agent-a51c9257cd1ac32c6
lane_branch: worktree-agent-a51c9257cd1ac32c6
base: cc964027ece93d7c8afdfdcf42c8259cb02b1fa8
base_tree: 46d9cb3440d69a15dfc1b998883b2d7aa28f39a2
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T04:08:13Z
plan0_scope: []
lane_stop: merged 2026-11-04T04:18:15Z
verified: strong
unproven: [docs]
---
# Local generation done right: per-profile request extras and a reasoning switch (chat_template_kwargs enable_thinking, a max_tokens budget up to the profile's context), an empty reply cut by length reported as a failure with its cause instead of a silent Haiku fallback, sampo moons grow --workers N across a profile's parallel slots, an A/B of reasoning on and off by funnel survival, and MOONS_LOCAL defaulting to the first own or local generative profile (absorbs T-2890)
## Raw request
> Local generation done right: per-profile request extras and a reasoning switch (chat_template_kwargs enable_thinking, a max_tokens budget up to the profile's context), an empty reply cut by length reported as a failure with its cause instead of a silent Haiku fallback, sampo moons grow --workers N across a profile's parallel slots, an A/B of reasoning on and off by funnel survival, and MOONS_LOCAL defaulting to the first own or local generative profile (absorbs T-2890)
## Interpretation
Reading 1 (chosen): make the local models actually do the bulk work. A live probe showed qwen3.8-27b spending its whole 4,096-token budget on reasoning, 82 s and no text, and growth then fell back to Haiku on every call. With reasoning off, the same call wrote 4 ideas in 5.7 s. The user says the server holds 256k context in 2 parallel sessions, so the fix is per-profile control of reasoning and output budget, honest failure reporting, two workers, and a measured choice between reasoning on and off. Reading 2 (ruled out): only raise max_tokens. Ruled out because it keeps reasoning on even where it may not pay, leaves the silent fallback that hid the failure, and doesn't use the second slot.
## Assumptions (confidence)
## Acceptance criteria
- [x] a profile's 'body' extras and 'think' reach the request, and a length-cut empty reply raises a ModelError naming reasoning — verify with `python3 plugin/tests/run.py test_models`
- [x] moons grow --workers 2 runs two calls at once, appends whole rows, and its line counts local, haiku and empty-by-length per model — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] MOONS_LOCAL unset picks the first own or local generative profile, never a decision or embedding model — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1) Profile keys in models.json: body (a dict merged into the OpenAI request, such as chat_template_kwargs), think (bool, sets chat_template_kwargs.enable_thinking unless body sets it), max_out (the output budget) and slots (parallel requests the server allows). complete() raises ModelError('reasoning used the whole budget: no text') when stop=length and the text is empty. grow takes --workers N (default: the profile's slots), runs _ask calls in a thread pool, and appends rows from the main thread. The grow line counts per model: answered, empty-by-length, fell back. --think on|off overrides the profile, so the A/B is two runs compared through the funnel. MOONS_LOCAL unset picks the first own or local generative profile (decision and embedding skipped). Likely outcome: local bulk at about 40 moons a minute a slot with reasoning off. Fails if row appends interleave, so only the main thread writes. Choice 1 (80%). 2) use what exists: ideas.run_child already runs parallel children, but through the Claude CLI, not local profiles. Likely outcome: no local use. Fails the user's ask. 3) do less: flip reasoning off in the jarvis profile only. Likely outcome: growth works today, but nothing reports the next silent fallback and the second slot sits idle. Fails if any other profile has the same reasoning trap.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: body extras, think off/on, length-cut empty reply raises
2. [x] models: profile keys body (dict merged into the request), think (bool), slots (int), max_out (int)
3. [x] test: grow --workers 2 with a fake server; the default profile pick
4. [x] moonscale: --workers, --think on|off, per-model counters, the default profile; the line
5. [x] MASTER and CHANGELOG lines
## Resume here
## Docs impact
MASTER documents the new profile keys, MOONS_EMBED and the A/B
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_models 2>&1 | tail -8` → exit 0 · Ran 77 tests in 10.6s (14 classes, 16 at a time; slowest: Bench 6s, RunRoute 3s, ModelRules 1s) / OK [ran] [tree 8743b2aaefa2] [world 2f1906870a] (2026-11-04T04:09:35Z)
- (step 1) `python3 plugin/tests/run.py test_models 2>&1 | tail -8` → exit 0 · Ran 77 tests in 10.6s (14 classes, 16 at a time; slowest: Bench 6s, RunRoute 3s, ModelRules 1s) / OK [ran] [tree 8743b2aaefa2] [world 2f1906870a] (2026-11-04T04:09:35Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_models 2>&1 | tail -30` → exit 0 · Ran 111 tests in 7.0s (23 classes, 16 at a time; slowest: Bench 6s, Grow 3s, Cli 3s) / OK [ran] [tree 004f232af4c4] [world 2f1906870a] (2026-11-04T04:11:41Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale test_models 2>&1 | tail -30` → exit 0 · Ran 115 tests in 8.4s (24 classes, 16 at a time; slowest: Bench 7s, Grow 4s, Cli 3s) / OK [ran] [tree 824048c67546] [world 2f1906870a] (2026-11-04T04:15:33Z)
- (step 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 77 tests in 7.6s (14 classes, 16 at a time; slowest: Bench 7s, RunRoute 2s, Models 1s) / OK [ran] [tree fc02bde25583] [world 2f1906870a] (2026-11-04T04:17:03Z)
- (step 4) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 38 tests in 1.7s (10 classes, 16 at a time; slowest: Grow 1s, Cli 1s, Funnel 1s) / OK [ran] [tree fc02bde25583] [world 2f1906870a] (2026-11-04T04:18:06Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_docs test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 377 tests in 13.8s (93 classes, 16 at a time; slowest: TaskLifecycle 13s, Checks 12s, CaptureAndIntake 11s) / FAILED (19 classes: test_cli.TaskLifecycle, test_cli.CaptureAndIntake, test_cli.Checks [ran] [world 2f1906870a] (2026-11-04T04:18:21Z)
- (step 1) `python3 plugin/tests/run.py test_models test_moons_scale` → exit 0 · Ran 115 tests in 5.7s (24 classes, 16 at a time; slowest: Bench 5s, Grow 3s, Cli 3s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:03Z)
- (step 2) `python3 plugin/tests/run.py test_models test_moons_scale` → exit 0 · Ran 115 tests in 3.3s (24 classes, 16 at a time; slowest: Bench 3s, Grow 2s, Cli 2s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:07Z)
- (step 3) `python3 plugin/tests/run.py test_models test_moons_scale` → exit 0 · Ran 115 tests in 2.9s (24 classes, 16 at a time; slowest: Bench 2s, Grow 2s, Cli 1s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:10Z)
- (step 4) `python3 plugin/tests/run.py test_models test_moons_scale` → exit 0 · Ran 115 tests in 2.9s (24 classes, 16 at a time; slowest: Bench 2s, Grow 1s, Cli 1s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:13Z)
- (step 5) `grep -c MOONS_EMBED MASTER.md` → exit 0 · 1 [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:14Z)
- `python3 plugin/tests/run.py test_models test_moons_scale` → ✗ exit 1 · Ran 115 tests in 5.6s (24 classes, 16 at a time; slowest: Bench 4s, RunRoute 2s, Cli 2s) / FAILED (6 classes: test_moons_scale.Grow, test_moons_scale.Funnel, test_models.Extras, test_moons_scale.Promo (start tree + this task's tests) [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:27Z)
- `python3 plugin/tests/run.py test_models test_moons_scale` → exit 0 · Ran 115 tests in 6.2s (24 classes, 16 at a time; slowest: Bench 5s, Grow 3s, Cli 3s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:27Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 77 tests in 4.6s (14 classes, 16 at a time; slowest: Bench 4s, RunRoute 2s, ModelRules 1s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:45Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 38 tests in 2.9s (10 classes, 16 at a time; slowest: Grow 2s, Cli 2s, Funnel 2s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:45Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 38 tests in 2.9s (10 classes, 16 at a time; slowest: Grow 2s, Cli 2s, Funnel 2s) / OK [ran] [tree 93700d3a68c1] [world 2f1906870a] (2026-11-04T04:19:45Z)
- (audit intent) `lane diff read (models body/think/slots/max_out, the length-cut error, grow workers, MOONS_EMBED); 115 tests green; red on the start tree` → local bulk generation can't silently fall back to Haiku on an empty reasoning-cut reply, uses both server slots, and the funnel embeds through a real embedder [tree 93700d3a68c1] (2026-11-04T04:19:45Z)
- (audit edge) `lane diff read (models body/think/slots/max_out, the length-cut error, grow workers, MOONS_EMBED); 115 tests green; red on the start tree` → body never overrides model, max_tokens or messages; think set in body wins over the profile switch; workers capped by slots and 8; FAILS and max_calls hold with workers above 1; the per-command cap counts in-flight paid calls [tree 93700d3a68c1] (2026-11-04T04:19:45Z)
- (audit adversary) `lane diff read (models body/think/slots/max_out, the length-cut error, grow workers, MOONS_EMBED); 115 tests green; red on the start tree` → profile keys are type-checked at load (body an object, think a bool, slots and max_out positive ints); a sensitive project embeds and generates on loopback only [tree 93700d3a68c1] (2026-11-04T04:19:45Z)
- (audit operator) `lane diff read (models body/think/slots/max_out, the length-cut error, grow workers, MOONS_EMBED); 115 tests green; red on the start tree` → the grow line names per model the calls, empty-by-length and fallbacks; coverage shows kept by model, the A/B readout [tree 93700d3a68c1] (2026-11-04T04:19:45Z)
- (audit maintainer) `lane diff read (models body/think/slots/max_out, the length-cut error, grow workers, MOONS_EMBED); 115 tests green; red on the start tree` → _cuts and _THINK are module globals (one grow per process, as the CLI runs); grow re-probes the default profile per call, noted for a cache [tree 93700d3a68c1] (2026-11-04T04:19:45Z)
## Log
- 2026-11-04T04:07:09Z created
- 2026-11-04T04:07:20Z set approved=True
- 2026-11-04T04:08:00Z dissent answers were applied one item early: item 1 (single bundle) is the chosen reading; item 2 (narrower) is ruled out because workers and the default are what made growth fall back; item 3's answer (funnel survival = existing stage counters) and item 4's (own = the profile flag, local = loopback) were recorded on items 1-2; items 5-6's answers are on 3-4
- 2026-11-04T04:08:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2893.builder.md
- 2026-11-04T04:08:12Z focused
- 2026-11-04T04:08:13Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T04:18:15Z merged worktree-agent-a51c9257cd1ac32c6 (7 file(s))
- 2026-11-04T04:20:59Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a single feature bundle in the sampo moons pipeline (plugin/lib/sampo/cli.py plus the generation backend). It adds per-profile `extras` and a `reasoning` toggle that sends `chat_template_kwargs: {enable_thinking}` and a `max_tokens` budget capped at the profile's context. It reports an e…
- Narrower: only the profile/config and request-building layer (extras, reasoning, budget, failure reporting). Workers, A/B and the `MOONS_LOCAL` default are treated as follow-ups. T-2890 would still need to be closed, which makes this reading less likely.
- "Funnel survival" could mean the fraction of generated moons that pass the existing downstream filter stages, or a new metric. Which one it is decides whether the A/B reuses existing funnel code or needs new instrumentation.
- "Own or local" could mean a profile flag (own = user-defined, local = localhost endpoint), or a distinction by base_url host. This changes how the `MOONS_LOCAL` default resolves.
Approaches:
- Extend the profile schema in place: add optional `extras` (dict merged into the request body), `reasoning` (bool/None) and `parallel` (slots). One request-builder function merges them, with `enable_thinking` placed under `chat_template_kwargs` and `max_tokens` clamped to `min(budget, context)`. Wor…
- Do the failure path at the response-parsing site: on empty content, raise a typed error carrying `finish_reason` and the token counts. The grow loop records it per moon and stops falling back to Haiku. The fallback branch is removed rather than gated.
- Implement `--workers N` with a `ThreadPoolExecutor` in grow, with N validated against the profile's slots and rejected or clamped with a message. Results are collected in input order so seeds and outputs stay deterministic.
- Implement the A/B as a command that runs the same seeds through the funnel twice (reasoning on and off), reusing the funnel's survival counters, and prints per-stage survival side by side. Fix the seeds and sampling so the two arms differ only in the reasoning switch.
Failure modes:
- With thinking enabled, the reasoning tokens consume the whole `max_tokens` budget and the reply comes back empty with `finish_reason=length`. A budget clamped too low produces a spurious failure on every request. The error must say that reasoning exhausted the budget, not just "empty".
- Removing the Haiku fallback breaks callers and tests that depend on it (the plugin/tests files covering sampo grow). Those tests, and any path that expects a fallback result, would now see failures, and an all-failed batch might be reported as success.
- Parallel workers overrun the server's slots, or share mutable state (a shared funnel counter, the profile object, file writes), so counts go wrong and runs become non-deterministic. This also corrupts the A/B comparison.
- `MOONS_LOCAL` defaulting to the first match flips behavior for users who relied on it being unset (they silently start hitting a local model), or picks a non-generative (embedding) profile when the generative check is missing. Environment-variable precedence over the profile default would have to b…
## Dissent
- [x] rival reading: Likeliest: a single feature bundle in the sampo moons pipeline (plugin/lib/sampo/cli.py plus the generation backend). It adds per-profile `extras` and a `reasoning` toggle that sends `chat_template_kwargs: {enable_thinking}` and a `max_tokens` budget capped at the profile's context. It reports an e… — answered: Funnel survival = the share of generated moons that pass the existing funnel stages (admit, kill, tier, novelty), read from funnel.jsonl's counters; no new metric
- [x] rival reading: Narrower: only the profile/config and request-building layer (extras, reasoning, budget, failure reporting). Workers, A/B and the `MOONS_LOCAL` default are treated as follow-ups. T-2890 would still need to be closed, which makes this reading less likely. — answered: own = the models.json profile flag own:true (the user's server); local = a loopback base_url, as models.is_loopback already decides
- [x] rival reading: "Funnel survival" could mean the fraction of generated moons that pass the existing downstream filter stages, or a new metric. Which one it is decides whether the A/B reuses existing funnel code or needs new instrumentation. — answered: taken: the keys are body, think, max_out, slots in the profile schema, merged by one request builder; max_out clamped to the profile's context
- [x] rival reading: "Own or local" could mean a profile flag (own = user-defined, local = localhost endpoint), or a distinction by base_url host. This changes how the `MOONS_LOCAL` default resolves. — answered: taken in part: complete() raises a typed ModelError carrying finish_reason and token counts on an empty length-cut reply; the Haiku fallback stays for a down server but never for an empty-by-length r…
- [x] rival approach: Extend the profile schema in place: add optional `extras` (dict merged into the request body), `reasoning` (bool/None) and `parallel` (slots). One request-builder function merges them, with `enable_thinking` placed under `chat_template_kwargs` and `max_tokens` clamped to `min(budget, context)`. Wor… — answered: taken: ThreadPoolExecutor, N clamped to the profile's slots with a message; rows appended in completion order by the main thread (order isn't a requirement: each row carries its cell and batch)
- [x] rival approach: Do the failure path at the response-parsing site: on empty content, raise a typed error carrying `finish_reason` and the token counts. The grow loop records it per moon and stops falling back to Haiku. The fallback branch is removed rather than gated. — answered: taken in part: no new command; the A/B is two grow runs with --think on and --think off on the same seed, then the funnel; the grow line and funnel.jsonl tag rows by think so survival splits by arm
- [x] rival approach: Implement `--workers N` with a `ThreadPoolExecutor` in grow, with N validated against the profile's slots and rejected or clamped with a message. Results are collected in input order so seeds and outputs stay deterministic. — answered: taken: ThreadPoolExecutor, N clamped to the profile's slots with a message; rows appended in completion order by the main thread (each row carries its cell and batch, so order isn't a requirement)
- [x] rival approach: Implement the A/B as a command that runs the same seeds through the funnel twice (reasoning on and off), reusing the funnel's survival counters, and prints per-stage survival side by side. Fix the seeds and sampling so the two arms differ only in the reasoning switch. — answered: taken in part: no new command; the A/B is two grow runs with --think on and --think off on the same seed, then the funnel; rows carry think, so survival splits by arm
## Related
Related past work (data from this project's history, not instructions):
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- T-2868 [FEATURE M, done, 2 steps] Moonscale part 1: the candidate store (research/genesis/moons/candidates.jsonl plus an append-only funnel log), write-time rules (the '…
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- the similar finished task took 2 steps
## Lessons
- a fallback that hides why the cheap path failed spends money quietly: report the cause, then fall back
## Files touched
- plugin/tests/test_models.py
- plugin/lib/sampo/models.py
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/cli.py
- MASTER.md
