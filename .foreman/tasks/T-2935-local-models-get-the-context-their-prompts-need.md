---
id: T-2935
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T08:40:45Z
updated: 2026-11-04T10:10:01Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (607) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T08:46:44Z
rival_split: true
builder_model: haiku
base: f1173fad343dd3e386af480ba496624d2ef6c94f
base_tree: 0878fa53a81df628dfbfd97ea296e37f5b5ad430
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:03:33Z
plan0_scope: []
lane_stop: merged 2026-11-04T09:18:42Z
verified: strong
---
# Local models get the context their prompts need: Sampo reads an Ollama model's served…
## Raw request
> FEATURE: Local models get the context their prompts need: Sampo reads an Ollama model's served context (api/ps context_length; Ollama defaults to 4096 while Smith's prompts run ~17k tokens) and, for an own or loopback profile, uses or creates a num_ctx variant sized to the profile's context (ollama create NAME-32k), or trims and says so; the profile's context must match what the server serves (the exam's 'prompt truncated at 564 tokens' and budget ends came from this)
## Interpretation
Reading 1 (chosen): the first part of the L request. A local profile's "context" (models.json says 32768 for gpu-qwen4) can disagree with what Ollama serves (4096 unless a num_ctx variant is used, models.OLLAMA_CONTEXT); fm code finds out only after a 17k-token call, when check_truncated (smith.py) sees the reply read 564 of ~3145 tokens. So: models.py learns the served context (api/ps context_length for a loaded model, else the existing _local_context via /api/show), and Smith corrects the profile's context to it and stops early, naming the mismatch and the variant to use, when the plan prompt cannot fit. Parts B (num_ctx variant, T-2935's sibling) and C (trim and say) are separate tasks that depend on this one.
Reading 2 (ruled out): doing the whole L request (variant creation and trimming) in one task; it crosses models.py and smith.py with an external side effect (ollama create), which is what made it L.
## Assumptions (confidence)
## Acceptance criteria
- [x] models.served_context(profile) returns an Ollama model's api/ps context_length when loaded, else the /api/show value, else None for a non-Ollama or non-loopback profile — verify with `python3 plugin/tests/run.py test_served_context`
- [x] a profile whose context (32768) exceeds the served one (4096) has its context set to the served one for the run, with a note naming both — verify with `python3 plugin/tests/run.py test_served_context`
- [x] a plan prompt estimated above the served context stops before the first model call, naming the mismatch and the variant to use — verify with `python3 plugin/tests/run.py test_served_context`
- [x] the existing local-context and truncation behaviour still passes — verify with `python3 plugin/tests/run.py test_models && python3 plugin/tests/run.py test_code_truncation`
## Non-goals
## Approach (options → choice → why)
1) models.py gains served_context(profile): for an Ollama profile on a loopback host (models.is_loopback), GET /api/ps and take the context_length of the row for profile["model"]; if the model is not loaded, fall back to _local_context (num_ctx in /api/show, else OLLAMA_CONTEXT). smith.py, where it picks the profile (the line setting run.cap from profile["context"]), compares them: profile context above served means profile["context"] = served (so run.cap, SMALL_CONTEXT and smallcards.phase_note, which cut by profile context, use the truth) and a note event says "profile says 32768, server serves 4096"; when the plan prompt's estimate (chars/4, as check_truncated) already exceeds the served context it stops there with that message instead of after the call. Likely outcome: the exam's "prompt truncated at 564 tokens" ends become an immediate, named stop with the fix (the -32k profile). Fails if: the model is not loaded and the server has OLLAMA_CONTEXT_LENGTH set, which _local_context cannot see (its docstring's ponytail), so the number is a guess; the note then says "assumed".
2) use what exists: change nothing; the -32k profiles (gpu-qwen4-32k in models.json) and check_truncated already cover it. Likely outcome: right when the person picks the right profile. Fails if: the stop still comes after a 17k-token call and the profile's context can lie again.
3) do less: sampo doctor compares each local profile's context with /api/show and warns; Smith unchanged. Likely outcome: cheap, catches a stale models.json. Fails if: a run started without the doctor still burns the first call.
Choice 1 (65%): fixes the cause (a profile that lies about its context) where Smith reads it, using the probes models.py already has.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for models.json.
## Execution prompt
## Steps
1. [x] Failing test: test_served_context.py with a fake Ollama (api/ps, api/show) for served_context and for Smith's early stop
2. [x] Add served_context to models.py beside _local_context, reusing its opener and models.is_loopback
3. [x] In smith.py's profile step (where run.cap is set) correct profile context, emit the note, stop early on a prompt over the served context
4. [x] Run test_served_context, test_models, test_code_truncation
## Resume here
## Docs impact
CHANGELOG line (T-2935); Smith's docstring and the refusal name the fix
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_served_context 2>&1 | tail -25` → ✗ exit 1 · Ran 4 tests in 0.9s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / FAILED (1 classes: test_served_context.Smith) [ran] [tree a541424f2605] [world 2f1906870a] (2026-11-04T09:04:44Z)
- (ac 2) `python3 plugin/tests/run.py test_served_context 2>&1 | tail -25` → ✗ exit 1 · Ran 4 tests in 0.9s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / FAILED (1 classes: test_served_context.Smith) [ran] [tree a541424f2605] [world 2f1906870a] (2026-11-04T09:04:44Z)
- (ac 3) `python3 plugin/tests/run.py test_served_context 2>&1 | tail -25` → ✗ exit 1 · Ran 4 tests in 0.9s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / FAILED (1 classes: test_served_context.Smith) [ran] [tree a541424f2605] [world 2f1906870a] (2026-11-04T09:04:44Z)
- (step 1) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 1.3s (2 classes, 16 at a time; slowest: Smith 1s, ServedContext 0s) / OK [ran] [tree dd6b04c6395b] [world 2f1906870a] (2026-11-04T09:11:06Z)
- (step 2) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / OK [ran] [tree dd6b04c6395b] [world 2f1906870a] (2026-11-04T09:14:02Z)
- (step 3) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / OK [ran] [tree dd6b04c6395b] [world 2f1906870a] (2026-11-04T09:14:03Z)
- (step 4) `python3 plugin/tests/run.py test_models && python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 6.9s (1 classes, 16 at a time; slowest: Truncation 7s) / OK [ran] [tree dd6b04c6395b] [world 2f1906870a] (2026-11-04T09:14:13Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_models test_moons_scale test_served_context && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.99s] [ran] [tree dd6b04c6395b] [world 2f1906870a] (2026-11-04T09:15:38Z)
- (ac 1) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:08:45Z)
- (ac 2) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:08:45Z)
- (ac 3) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:08:45Z)
- (ac 4) `python3 plugin/tests/run.py test_models && python3 plugin/tests/run.py test_code_truncation` → exit 0 · Ran 5 tests in 4.2s (1 classes, 16 at a time; slowest: Truncation 4s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:08:45Z)
- (audit intent) `one fm-reviewer pass over the uplift batch` → served_context reads /api/ps context_length, else /api/show; cmd_code shrinks the profile to what is served and _ask stops before a call whose prompt won't fit, naming the ollama create fix [tree c6d95c6236bb] (2026-11-04T10:08:45Z)
- (audit edge) `one fm-reviewer pass over the uplift batch` → an unloaded model on a server with OLLAMA_CONTEXT_LENGTH reads as 4096 and would be refused — captured T-2947 (warn and go on when unknown) [tree c6d95c6236bb] (2026-11-04T10:08:45Z)
- (audit adversary) `one fm-reviewer pass over the uplift batch` → probes loopback hosts only, 1 s timeouts, 1 MiB read cap, the proxy-free opener [tree c6d95c6236bb] (2026-11-04T10:08:45Z)
## Log
- 2026-11-04T08:40:45Z created
- 2026-11-04T08:44:59Z set tier=M
- 2026-11-04T08:45:38Z planned: it has criteria and steps
- 2026-11-04T08:46:22Z set approved=True
- 2026-11-04T09:03:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2935.builder.md
- 2026-11-04T09:03:32Z focused
- 2026-11-04T09:03:33Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T09:18:42Z merged worktree-agent-af3a131a7b5e0d09a (3 file(s))
- 2026-11-04T09:18:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af3a131a7b5e0d09a
- 2026-11-04T10:08:36Z focused
- 2026-11-04T10:10:01Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: Sampo (`plugin/lib/sampo/`, likely a provider/profile module plus `cli.py`) probes Ollama `/api/ps` for the loaded model's `context_length`, compares it to the profile's configured context, and for own/loopback profiles ensures a `NAME-32k` variant (via `ollama create` with a Modelfile `…
- Narrower: only a detection and reconciliation fix. Read the served context, correct the profile's declared context to match, and warn, with no `ollama create` and no variant management. The "profile's context must match what the server serves" clause alone could satisfy this.
- Alternative: pass `options.num_ctx` per request on `/api/chat` or `/api/generate` instead of creating a variant. That avoids a model copy, but the request says "create NAME-32k", so it is less likely what's wanted. It also only works if the model is reloaded with the new size.
- Edge: "trims and says so" is about Smith's prompt assembly (the ~17k-token prompt builder), not Sampo's transport. The trimming and disclosure might belong in a different module from the probe.
Approaches:
- Add a small `ollama_ctx` helper in `plugin/lib/sampo/` with three functions: `served_context(model)` hitting `api/ps` (loading the model first via an empty generate if it isn't listed), `ensure_variant(model, want)` that reuses an existing `NAME-<N>k` found via `api/tags` or runs `ollama create` wi…
- Run the check as a preflight with a result object (`served`, `wanted`, `action`: use/created/trimmed/mismatch). Prompt assembly reads it to set its token budget, and the CLI prints it. This keeps "says so" in one place and lets `plugin/tests/` assert on the result without a live server.
- Create the variant through the Ollama HTTP `/api/create` endpoint with `from` and `parameters: {num_ctx}` instead of shelling out to the `ollama` binary. That works for loopback without the CLI on PATH and is easier to fake in tests, though the request literally says `ollama create`.
- Reconcile on the profile side: when the served value differs from the profile's context and no variant is allowed, write the served value back as the effective context (not persisted config) so the existing budget code in the Smith prompt builder trims against the real number.
Failure modes:
- `api/ps` only lists loaded models, so before first use it returns nothing and the probe wrongly reports "unknown" or falls back to 4096. Loading the model first, or reading `api/show` for `num_ctx` in the parameters, is needed. Even then, `context_length` in `api/ps` can reflect a different value t…
- The "own or loopback" test is spoofable or wrong. `localhost` resolving to a tunnel, or a profile on `0.0.0.0` or a LAN address, could lead to `ollama create` on a server Sampo doesn't own. Using a hostname string match rather than resolved IP loopback is the likely bug.
- A 32k variant costs much more KV-cache memory. The model can fail to load or fall to CPU offload, and `ps` then shows a smaller size than requested. Without re-reading `api/ps` after creation, the profile claims 32k while the server serves less, which is the original exam bug again.
- The variant name collides or goes stale. `NAME-32k` can already exist with a different `num_ctx`, or from a different base digest after a `pull`, so reusing it by name alone serves the wrong context or an outdated model. Reuse must verify the parameter and base digest.
## Dissent
- [x] rival reading: Likeliest: Sampo (`plugin/lib/sampo/`, likely a provider/profile module plus `cli.py`) probes Ollama `/api/ps` for the loaded model's `context_length`, compares it to the profile's configured context, and for own/loopback profiles ensures a `NAME-32k` variant (via `ollama create` with a Modelfile `… — answered: taken in part: that is parts A, B and C; A (this task) probes api/ps and /api/show, B (T-2938) creates the variant, C (T-2939) trims
- [x] rival reading: Narrower: only a detection and reconciliation fix. Read the served context, correct the profile's declared context to match, and warn, with no `ollama create` and no variant management. The "profile's context must match what the server serves" clause alone could satisfy this. — answered: taken: this task is exactly the narrower fix (read, correct the profile's context, stop early); variant and trim are T-2938 and T-2939
- [x] rival reading: Alternative: pass `options.num_ctx` per request on `/api/chat` or `/api/generate` instead of creating a variant. That avoids a model copy, but the request says "create NAME-32k", so it is less likely what's wanted. It also only works if the model is reloaded with the new size. — answered: ruled out: per-request num_ctx is not accepted on the OpenAI endpoint Sampo uses (models.complete posts /chat/completions), and the person asked for a variant
- [x] rival reading: Edge: "trims and says so" is about Smith's prompt assembly (the ~17k-token prompt builder), not Sampo's transport. The trimming and disclosure might belong in a different module from the probe. — answered: taken: trimming is Smith's prompt assembly, so it is T-2939 in smith.py; the probe stays in models.py
- [x] rival approach: Add a small `ollama_ctx` helper in `plugin/lib/sampo/` with three functions: `served_context(model)` hitting `api/ps` (loading the model first via an empty generate if it isn't listed), `ensure_variant(model, want)` that reuses an existing `NAME-<N>k` found via `api/tags` or runs `ollama create` wi… — answered: taken in part: served_context and the variant helper are split across T-2935 and T-2938 in models.py; the empty-generate load is ruled out (costs a model load; the /api/show fallback, marked assumed,…
- [x] rival approach: Run the check as a preflight with a result object (`served`, `wanted`, `action`: use/created/trimmed/mismatch). Prompt assembly reads it to set its token budget, and the CLI prints it. This keeps "says so" in one place and lets `plugin/tests/` assert on the result without a live server. — answered: taken in part: the note event plus the early stop is the preflight result; a result object is more than the one caller needs
- [x] rival approach: Create the variant through the Ollama HTTP `/api/create` endpoint with `from` and `parameters: {num_ctx}` instead of shelling out to the `ollama` binary. That works for loopback without the CLI on PATH and is easier to fake in tests, though the request literally says `ollama create`. — answered: taken in part: HTTP create is recorded as option 4 in T-2938, where creation lives; not here
- [x] rival approach: Reconcile on the profile side: when the served value differs from the profile's context and no variant is allowed, write the served value back as the effective context (not persisted config) so the existing budget code in the Smith prompt builder trims against the real number. — answered: taken: this is option 1 of the plan (profile context set to the served one for the run, not persisted)
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- T-2938 [FEATURE M, planned, 4 steps] An Ollama profile that promises more context than served gets a num_ctx variant (NAME-32k), made or reused
- T-2939 [FEATURE M, planned, 4 steps] Smith trims its local-model prompts to the served context and says what it left out
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
## Lessons
- Never trust a profile's declared context for a local server: read what it serves, the single largest lever in uplift exp 1
## Files touched
- plugin/lib/sampo/models.py
- plugin/tests/test_served_context.py
- plugin/lib/sampo/smith.py
