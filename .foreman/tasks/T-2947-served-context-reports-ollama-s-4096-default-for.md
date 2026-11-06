---
id: T-2947
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T09:44:05Z
updated: 2026-11-04T12:44:20Z
builder_model: sonnet
base: 0c4056bb7a6e49d2754ef9472edeee08b32e9e30
base_tree: 4563dfdc5760e91e0072b3f5bf05496223439d97
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T11:51:35Z
plan0_scope: []
lane_stop: merged 2026-11-04T12:41:49Z
verified: strong
---
# served_context reports Ollama's 4096 default for an unloaded model whose server sets…
## Raw request
> served_context reports Ollama's 4096 default for an unloaded model whose server sets OLLAMA_CONTEXT_LENGTH (or newer Ollama's VRAM default), so Smith refuses a plan prompt the server would serve: when /api/ps is empty and /api/show has no num_ctx, warn and go on instead of shrinking the profile (models.py:377, test_served_context.py:585 pins the old fallback); probe served context once per run, not twice (context_variant and cmd_code)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with /api/ps empty and /api/show carrying no num_ctx, served_context returns None (unknown) instead of 4096, so Smith neither shrinks the profile nor refuses; a model that is loaded or has num_ctx is read as before — verify with `python3 plugin/tests/run.py test_served_context test_ctx_variant`
- [x] one fm code run probes the served context once — verify with `python3 plugin/tests/run.py test_served_context`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: an Ollama fake with an empty /api/ps and a num_ctx-less /api/show gives no served note and no refusal
2. [x] models.served_context returns None for the unknown case; cmd_code reuses context_variant's probe
## Resume here
## Docs impact
CHANGELOG line (T-2947)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant 2>&1 | tail -8` → ✗ exit 1 · Ran 11 tests in 1.2s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / FAILED (2 classes: test_ctx_variant.Variant, test_ctx_variant.Smith) [ran] [tree 25ad3ec1820c] [world 2f1906870a] (2026-11-04T11:52:20Z)
- (ac 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant 2>&1 | tail -12` → ✗ exit 1 · Ran 11 tests in 1.0s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree 0f1b1426b2b1] [world 2f1906870a] (2026-11-04T11:52:36Z)
- (ac 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant 2>&1 | tail -3` → exit 0 · Ran 11 tests in 1.1s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 5ca42c66df6c] [world 2f1906870a] (2026-11-04T11:52:44Z)
- (step 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant 2>&1 | tail -3` → exit 0 · Ran 11 tests in 1.1s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 5ca42c66df6c] [world 2f1906870a] (2026-11-04T11:52:44Z)
- (step 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 11 tests in 1.1s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 5ca42c66df6c] [world 2f1906870a] (2026-11-04T11:52:46Z)
- (step 2) `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 11 tests in 1.2s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 5ca42c66df6c] [world 2f1906870a] (2026-11-04T11:52:48Z)
- (ac 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant 2>&1 | tail -12` → ✗ exit 1 · Ran 11 tests in 1.6s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / FAILED (1 classes: test_ctx_variant.Variant) [ran] [tree f65ad2f04115] [world 2f1906870a] (2026-11-04T11:56:16Z)
- (ac 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant 2>&1 | tail -4` → exit 0 · Ran 11 tests in 1.4s (4 classes, 16 at a time; slowest: Smith 1s, Variant 0s, Smith 0s) / OK [ran] [tree 3018075135b3] [world 2f1906870a] (2026-11-04T11:56:22Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_ctx_variant test_models test_moons_scale test_served_context && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.72s] [ran] [tree 3018075135b3] [world 2f1906870a] (2026-11-04T11:56:37Z)
- (step 2) `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 11 tests in 1.4s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 3018075135b3] [world 2f1906870a] (2026-11-04T11:57:37Z)
- `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 10 tests in 2.6s (4 classes, 16 at a time; slowest: Smith 0s, Smith 0s, Variant 0s) / OK (start tree + this task's tests) [ran] [tree b4fa2d896f4d] [world 2f1906870a] (2026-11-04T12:09:54Z)
- `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 10 tests in 0.8s (4 classes, 16 at a time; slowest: Smith 0s, Smith 0s, Variant 0s) / OK [ran] [tree b4fa2d896f4d] [world 2f1906870a] (2026-11-04T12:09:54Z)
- `python3 plugin/tests/run.py test_served_context test_ctx_variant` → ✗ exit 1 · Ran 11 tests in 2.9s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / FAILED (3 classes: test_ctx_variant.Variant, test_served_context.ServedContext, test_served_context.Smith) (start tree + this task's tests) [ran] [tree 5f117801238d] [world 2f1906870a] (2026-11-04T12:42:02Z)
- `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 11 tests in 1.0s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 5f117801238d] [world 2f1906870a] (2026-11-04T12:42:02Z)
- (ac 1) `python3 plugin/tests/run.py test_served_context test_ctx_variant` → exit 0 · Ran 11 tests in 1.0s (4 classes, 16 at a time; slowest: Smith 1s, Smith 0s, Variant 0s) / OK [ran] [tree 8f2d6fe0cba9] [world 2f1906870a] (2026-11-04T12:42:15Z)
- (ac 2) `python3 plugin/tests/run.py test_served_context` → exit 0 · Ran 5 tests in 1.0s (2 classes, 16 at a time; slowest: Smith 1s, ServedContext 0s) / OK [ran] [tree 8f2d6fe0cba9] [world 2f1906870a] (2026-11-04T12:42:15Z)
- (audit intent) `self-review of the lane diff after one round back (the first version made no variant for an unknown context; sent back so ctx_variant profiles still get one)` → an unknown served context (no /api/ps row, no num_ctx in /api/show) neither shrinks nor refuses; a ctx_variant profile on a live Ollama still gets its num_ctx variant; one probe a run [tree 8f2d6fe0cba9] (2026-11-04T12:42:15Z)
- (audit edge) `self-review of the lane diff after one round back (the first version made no variant for an unknown context; sent back so ctx_variant profiles still get one)` → a profile at or below 4096 gets no variant (Ollama's default covers it); with ctx_variant on and an unknown context, one extra /api/ps request tells unknown from not-Ollama [tree 8f2d6fe0cba9] (2026-11-04T12:42:15Z)
- (audit adversary) `self-review of the lane diff after one round back (the first version made no variant for an unknown context; sent back so ctx_variant profiles still get one)` → the probes stay loopback, 1 s timeouts, 1 MB cap; bad JSON reads as unknown [tree 8f2d6fe0cba9] (2026-11-04T12:42:15Z)
- (audit self) `self-review of the lane diff after one round back (the first version made no variant for an unknown context; sent back so ctx_variant profiles still get one)` → no findings [tree 8f2d6fe0cba9] (2026-11-04T12:42:15Z)
## Log
- 2026-11-04T09:44:05Z created
- 2026-11-04T09:47:13Z planned: it has criteria and steps
- 2026-11-04T11:07:17Z set approved=True
- 2026-11-04T11:51:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2947.builder.md
- 2026-11-04T11:51:34Z focused
- 2026-11-04T11:51:35Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T12:41:49Z merged worktree-agent-a097f9b130493294c (4 file(s))
- 2026-11-04T12:41:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a097f9b130493294c
- 2026-11-04T12:41:56Z focused
- 2026-11-04T12:42:11Z scope: models.py (served_context, context_variant, _ollama_ps), smith.py cmd_code's probe lines, test_served_context, test_ctx_variant, CHANGELOG
- 2026-11-04T12:44:17Z done
- 2026-11-04T12:44:20Z committed b991eafa (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2935 [FEATURE M, done, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served… — lesson: Never trust a profile's declared conte…
- T-2938 [FEATURE M, done, 4 steps] An Ollama profile that promises more context than served gets a num_ctx variant (NAME-32k), made or reused — lesson: Make the fix a too…
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
- similar past tasks were M: consider --tier M
## Why not caught
test_served_context pinned the 4096 fallback as intended behaviour; the audit's edge lens found the server-wide case
## Lessons
- Unknown is not the default: a probe that can't see a server-wide setting should say unknown and let the run's own truncation check catch a real cut
## Files touched
- plugin/tests/test_served_context.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/smith.py
- plugin/tests/test_ctx_variant.py
- CHANGELOG.md
