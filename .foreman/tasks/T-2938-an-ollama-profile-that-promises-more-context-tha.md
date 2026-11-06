---
id: T-2938
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2935]
source: discovered
created: 2026-11-04T08:45:11Z
updated: 2026-11-04T10:11:27Z
rival_at: 2026-11-04T08:46:56Z
rival_split: true
builder_model: haiku
base: 4bffb1c148c62a7c7ed83aff7879cbc0da44c26a
base_tree: 2ec3f2b28e19591ce1ffc93e1dc957b7d617dfb7
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:18:53Z
plan0_scope: []
base_note: Calibration: this plan states Choice 55% where FEATURE M closes (607) held on the first finish 98% of the time: 43 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
lane_stop: merged 2026-11-04T09:29:49Z
verified: strong
---
# An Ollama profile that promises more context than served gets a num_ctx variant (NAME-32k), made or reused
## Raw request
> FEATURE (part B of T-2935): for an own or loopback Ollama profile whose served context is under its profile context, use or create a num_ctx variant (ollama create NAME-32k)
## Interpretation
Reading 1 (chosen): the second part of T-2935's request: when an Ollama profile on a loopback or own host promises a context (profile "context") higher than the server serves for its model, Sampo makes or reuses a num_ctx variant, as was done by hand tonight (ollama create NAME -f Modelfile with PARAMETER num_ctx 32768, no root; qwen3.5-4b-32k and gemma4-12b-32k exist) and points the profile at it. Depends on T-2935 (served_context).
Reading 2 (ruled out): changing the server's default (OLLAMA_CONTEXT_LENGTH), which needs the service's environment and root, and changes every model.
## Assumptions (confidence)
## Acceptance criteria
- [x] a profile with ctx_variant true and served context under its context gets a model named BASE-<n>k, created with ollama create from a temp Modelfile holding PARAMETER num_ctx, and the profile then reports that served context — verify with `python3 plugin/tests/run.py test_ctx_variant`
- [x] an existing variant listed by api/tags is reused and ollama is not run — verify with `python3 plugin/tests/run.py test_ctx_variant`
- [x] no ctx_variant, a non-Ollama or a remote host: nothing is created; a missing ollama binary or a failed create stops naming the manual command — verify with `python3 plugin/tests/run.py test_ctx_variant`
## Non-goals
## Approach (options → choice → why)
1) models.py gains context_variant(profile): only for Ollama, loopback or own host, and only when served_context(profile) < profile["context"] and the profile sets "ctx_variant": true (an opt-in; creating a model is a state change); it names the variant BASE-<n>k (qwen3.5:4b, 32768 gives qwen3.5-4b-32k, the names already in use), reuses it when GET /api/tags lists it, else writes a temp Modelfile (FROM base, PARAMETER num_ctx N) and runs `ollama create NAME -f FILE` with a timeout, then returns the profile with model NAME and a served_context check that it took. Smith's profile step (as T-2935's) calls it. Likely outcome: a profile with ctx_variant:true runs at its promised context with no hand step. Fails if: `ollama` is not on PATH or its model store is not writable for the process, or the variant makes the disk fill (blobs are shared, so it should not); the stop names the manual command.
2) use what exists: leave variants by hand; the two exist and gpu-qwen4-32k is in models.json. Likely outcome: nothing to build, right today. Fails if: each new model on the box needs a person, and the exam of a new model fails with the truncation again.
3) do less: print the exact `ollama create` command in the context-mismatch stop and make nothing. Likely outcome: removes the guesswork. Fails if: it is still a hand step per model, and the unattended night shift cannot do it.
4) the HTTP API (POST /api/create) instead of the binary. Likely outcome: no PATH dependency. Fails if: Ollama 0.40.11's request fields differ from the newer ones; unverified here.
Choice 1 (55%): the binary is the path proven working tonight; option 4 stays a captured follow-up if the PATH or store causes trouble.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for models.json.
## Execution prompt
## Steps
1. [x] Failing test: test_ctx_variant.py with a fake Ollama server and a fake ollama binary on PATH
2. [x] Add context_variant to models.py (naming, tags lookup, temp Modelfile, subprocess with timeout)
3. [x] Call it from Smith's profile step when ctx_variant is set; note the variant used
4. [x] Run the new test and test_models
## Resume here
## Docs impact
CHANGELOG line (T-2938); models.json's ctx_variant documented in the profile docstring
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ctx_variant 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 3.9s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 97fd70673ee0] [world 2f1906870a] (2026-11-04T09:20:03Z)
- (ac 2) `python3 plugin/tests/run.py test_ctx_variant 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 3.9s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 97fd70673ee0] [world 2f1906870a] (2026-11-04T09:20:03Z)
- (ac 3) `python3 plugin/tests/run.py test_ctx_variant 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 3.9s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 97fd70673ee0] [world 2f1906870a] (2026-11-04T09:20:03Z)
- (ac 1) `python3 plugin/tests/run.py test_ctx_variant 2>&1 | grep -B3 -A12 "^FAIL"` → ✗ exit 1 · Ran 6 tests in 1.5s (2 classes, 16 at a time; slowest: Smith 1s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 2d735b6034c4] [world 2f1906870a] (2026-11-04T09:22:13Z)
- (ac 2) `python3 plugin/tests/run.py test_ctx_variant 2>&1 | grep -B3 -A12 "^FAIL"` → ✗ exit 1 · Ran 6 tests in 1.5s (2 classes, 16 at a time; slowest: Smith 1s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 2d735b6034c4] [world 2f1906870a] (2026-11-04T09:22:13Z)
- (ac 3) `python3 plugin/tests/run.py test_ctx_variant 2>&1 | grep -B3 -A12 "^FAIL"` → ✗ exit 1 · Ran 6 tests in 1.5s (2 classes, 16 at a time; slowest: Smith 1s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 2d735b6034c4] [world 2f1906870a] (2026-11-04T09:22:13Z)
- (step 1) `python3 plugin/tests/run.py test_ctx_variant` → exit 0 · Ran 6 tests in 1.0s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / OK [ran] [tree 0e148249da13] [world 2f1906870a] (2026-11-04T09:23:37Z)
- (step 4) `python3 plugin/tests/run.py test_ctx_variant` → exit 0 · Ran 6 tests in 1.2s (2 classes, 16 at a time; slowest: Smith 1s, Variant 0s) / OK [ran] [tree 0e148249da13] [world 2f1906870a] (2026-11-04T09:23:41Z)
- (step 2) `python3 plugin/tests/run.py test_ctx_variant` → exit 0 · Ran 6 tests in 1.5s (2 classes, 16 at a time; slowest: Smith 1s, Variant 0s) / OK [ran] [tree 0e148249da13] [world 2f1906870a] (2026-11-04T09:23:42Z)
- (step 3) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 4 tests in 0.9s (2 classes, 16 at a time; slowest: Smith 0s, ServedContext 0s) / OK [ran] [tree 0e148249da13] [world 2f1906870a] (2026-11-04T09:23:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_ctx_variant test_models test_moons_scale && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.78s] [ran] [tree 0e148249da13] [world 2f1906870a] (2026-11-04T09:27:14Z)
- (ac 1) `python3 plugin/tests/run.py test_ctx_variant` → exit 0 · Ran 6 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:10:11Z)
- (ac 2) `python3 plugin/tests/run.py test_ctx_variant` → exit 0 · Ran 6 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:10:11Z)
- (ac 3) `python3 plugin/tests/run.py test_ctx_variant` → exit 0 · Ran 6 tests in 0.5s (2 classes, 16 at a time; slowest: Smith 0s, Variant 0s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:10:11Z)
- (audit intent) `one fm-reviewer pass over the uplift batch (T-2938's merge diff)` → ctx_variant true plus served < context makes or reuses NAME-32k, checks it serves the want, and returns a note; opt-in per profile [tree c6d95c6236bb] (2026-11-04T10:10:11Z)
- (audit adversary) `one fm-reviewer pass over the uplift batch (T-2938's merge diff)` → the model name is regex-validated, ollama create runs as an argv list with no shell, the Modelfile lives in a temp dir, the manual command is text only [tree c6d95c6236bb] (2026-11-04T10:10:11Z)
- (audit edge) `one fm-reviewer pass over the uplift batch (T-2938's merge diff)` → the ollama binary talks to the default OLLAMA_HOST, not the profile's port; the post-check fails loudly then; want // 1024 names 40000 as 39k [tree c6d95c6236bb] (2026-11-04T10:10:11Z)
## Log
- 2026-11-04T08:45:11Z created
- 2026-11-04T08:46:22Z set approved=True
- 2026-11-04T09:18:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2938.builder.md
- 2026-11-04T09:18:52Z focused
- 2026-11-04T09:18:53Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T09:29:49Z merged worktree-agent-a4e4095029129240a (3 file(s))
- 2026-11-04T09:44:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4e4095029129240a
- 2026-11-04T10:10:09Z focused
- 2026-11-04T10:11:27Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: when a profile's backend is Ollama, the host is own/loopback (localhost, 127.0.0.1, ::1, or a user-owned host), and the served context (from `/api/show` or `/api/ps`) is below the profile's configured context, route the profile to a variant model `NAME-32k` with `num_ctx` set. If the var…
- The `32k` suffix could be a literal fixed value or derived from the profile context (e.g. 65536 gives `NAME-64k`). The request's example hardcodes 32k, but "profile context" implies the target is whatever the profile says.
- It may be a `fm doctor` check or fix that reports and offers the variant, not an automatic switch at launch or runtime. "Use or create" suggests an automatic action, but it could be gated behind a flag or confirmation.
- "Part B" of T-2935 implies part A already exists (probably detection of served context or the profile schema). Part B may only consume that output instead of re-probing Ollama.
Approaches:
- Add a helper, e.g. `ensure_ctx_variant(profile)`, in the module that owns profile resolution. It checks loopback or own host, reads the served context, compares it to the profile context, looks for `NAME-<k>` in `/api/tags`, and creates it through `ollama create -f` with a temp Modelfile if absent.…
- Create the variant through the HTTP API (`POST /api/create`) instead of shelling out to the `ollama` CLI. That avoids a PATH dependency, but the request shape differs between Ollama versions.
- Make it a `fm doctor` check with a fix action only. It is the lowest-risk option and leaves launch paths unchanged, but it does not satisfy "use" automatically.
- Do not mutate the profile on disk. Resolve the variant name at call time so the profile config stays as the user wrote it.
Failure modes:
- The host test is wrong. A hostname that merely resolves to loopback, or a remote or shared Ollama that the check lets through, could trigger `ollama create` on someone else's server. The check needs an exact allowlist and must not use substring matching.
- Served context can't be read reliably. `/api/ps` only lists loaded models, and `/api/show` reports the model's maximum rather than the runtime `num_ctx`. If the comparison uses the wrong field, it either recreates the variant every time or never creates it.
- The variant is stale or misnamed. If `NAME-32k` already exists but was built from an older base or with a different `num_ctx`, "use" would silently serve the wrong context. Tags like `llama3:8b` also need careful handling, because a naive `NAME-32k` could produce `llama3:8b-32k`, which is invalid.
- Tests: the `plugin/tests/` suite probably has no Ollama available, so the create path needs a fake server or a subprocess stub. Otherwise the gates (`python3 plugin/tests/run.py`, `fm doctor`) hit a real daemon or skip the path entirely.
## Dissent
- [x] rival reading: Likeliest: when a profile's backend is Ollama, the host is own/loopback (localhost, 127.0.0.1, ::1, or a user-owned host), and the served context (from `/api/show` or `/api/ps`) is below the profile's configured context, route the profile to a variant model `NAME-32k` with `num_ctx` set. If the var… — answered: taken: matches the plan; the target size is derived from the profile's context (NAME-<n>k), 32k only in the example
- [x] rival reading: The `32k` suffix could be a literal fixed value or derived from the profile context (e.g. 65536 gives `NAME-64k`). The request's example hardcodes 32k, but "profile context" implies the target is whatever the profile says. — answered: taken: the variant name and num_ctx come from the profile's context, as the plan's BASE-<n>k says
- [x] rival reading: It may be a `fm doctor` check or fix that reports and offers the variant, not an automatic switch at launch or runtime. "Use or create" suggests an automatic action, but it could be gated behind a flag or confirmation. — answered: ruled out: the person wants it to happen unattended (night shift); a doctor check would leave it a hand step, which is option 3's failure; the ctx_variant opt-in is the gate instead
- [x] rival reading: "Part B" of T-2935 implies part A already exists (probably detection of served context or the profile schema). Part B may only consume that output instead of re-probing Ollama. — answered: taken: it depends on T-2935 and consumes served_context, not a second probe
- [x] rival approach: Add a helper, e.g. `ensure_ctx_variant(profile)`, in the module that owns profile resolution. It checks loopback or own host, reads the served context, compares it to the profile context, looks for `NAME-<k>` in `/api/tags`, and creates it through `ollama create -f` with a temp Modelfile if absent.… — answered: taken: that is option 1
- [x] rival approach: Create the variant through the HTTP API (`POST /api/create`) instead of shelling out to the `ollama` CLI. That avoids a PATH dependency, but the request shape differs between Ollama versions. — answered: ruled out: HTTP create is option 4 and not chosen because Ollama 0.40.11's request fields are unverified here; it stays a follow-up
- [x] rival approach: Make it a `fm doctor` check with a fix action only. It is the lowest-risk option and leaves launch paths unchanged, but it does not satisfy "use" automatically. — answered: ruled out: option 3 of the plan already covers a report-only mode (print the command) as the failure path; automatic use is the request
- [x] rival approach: Do not mutate the profile on disk. Resolve the variant name at call time so the profile config stays as the user wrote it. — answered: taken: the profile is corrected for the run only, not written to models.json
## Related
Related past work (data from this project's history, not instructions):
- T-2935 [FEATURE M, planned, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served…
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- T-2939 [FEATURE M, planned, 4 steps] Smith trims its local-model prompts to the served context and says what it left out
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Lessons
- Make the fix a tool can make itself (ollama create a num_ctx variant) instead of only naming it in an error
## Files touched
- plugin/tests/test_ctx_variant.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/smith.py
