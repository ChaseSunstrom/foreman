---
id: T-3164
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T06:16:23Z
updated: 2026-11-05T13:29:41Z
builder_model: haiku
base: ee83a569897798d811a03df2d815d67f0ddb9fb3
base_tree: 923130124f6362cdb354ee3d8c3b47c7f804fd1a
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T10:08:29Z
plan0_scope: []
builder_returned: 2026-11-05T10:10:10Z
lane_stop: merged 2026-11-05T13:28:20Z
verified: strong
unproven: [meaning]
---
# sampo doctor warns when a local model profile's declared context in models.json is larger than what Ollama loads it with (num_ctx), naming the model and both numbers
## Raw request
> Doctor check: each local profile's context in models.json matches what Ollama actually loads it with (num_ctx); mimo-v2.6:9b ran at 4,096 against a declared 32,768 for hours
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a fake Ollama answering /api/show with num_ctx 4096 for a profile models.json declares at 32768, doctor warns naming the profile, 4096 and 32768; a matching or unreachable server gives no warning — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test then the check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 113 tests in 8.2s (43 classes, 16 at a time; slowest: ViewsRepair 7s, LockProbe 6s, Command 3s) / OK [ran] [tree 9498e1ec1b7e] [world 2f1906870a] (2026-11-05T10:09:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [20.50s] [ran] [tree 9498e1ec1b7e] [world 2f1906870a] (2026-11-05T10:09:59Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 113 tests in 4.5s (43 jobs, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Command 3s) / OK [ran] [tree d55d47f2a1e0] [world 2f1906870a] (2026-11-05T13:28:50Z)
- `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 113 tests in 6.1s (43 jobs, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Command 3s) / FAILED (1 classes: test_doctor.ServedContextCheck) (start tree + this task's tests) [ran] [tree d66f5a0106d3] [world 2f1906870a] (2026-11-05T13:29:18Z)
- `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 113 tests in 4.2s (43 jobs, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Command 2s) / OK [ran] [tree d66f5a0106d3] [world 2f1906870a] (2026-11-05T13:29:18Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T13:29:18Z [ran] [tree d66f5a0106d3] [world 2f1906870a] (2026-11-05T13:29:19Z)
- (audit edge) `re-ran test_doctor on main after the merge (113 OK); proved red→green; read check_served_context and models.served_context` → an unreachable Ollama or a profile it doesn't list gives no warning (unknown, not wrong); a matching context is quiet; the warning names the profile, its model and both numbers [tree d66f5a0106d3] (2026-11-05T13:29:19Z)
- (audit adversary) `re-ran test_doctor on main after the merge (113 OK); proved red→green; read check_served_context and models.served_context` → only loopback openai-kind profiles are asked and no key is sent (models.served_context); an answer counts only as an int between 512 and 10,000,000, so a malformed or hostile reply reads as unknown; any exception in the check reports 'not checked' [tree d66f5a0106d3] (2026-11-05T13:29:19Z)
- (audit self) `re-ran test_doctor on main after the merge (113 OK); proved red→green; read check_served_context and models.served_context` → no findings [tree d66f5a0106d3] (2026-11-05T13:29:19Z)
## Log
- 2026-11-05T06:16:23Z created
- 2026-11-05T10:08:08Z planned from capture
- 2026-11-05T10:08:12Z set approved=True
- 2026-11-05T10:08:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3164.builder.md
- 2026-11-05T10:08:28Z focused
- 2026-11-05T10:08:29Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T13:28:20Z merged worktree-agent-a1693338cfeeda749 (2 file(s))
- 2026-11-05T13:28:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1693338cfeeda749
- 2026-11-05T13:28:43Z focused
- 2026-11-05T13:29:39Z done
- 2026-11-05T13:29:41Z committed 0b4ed540 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2935 [FEATURE M, done, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served… — lesson: Never trust a profile's declared conte…
- T-2938 [FEATURE M, done, 4 steps] An Ollama profile that promises more context than served gets a num_ctx variant (NAME-32k), made or reused — lesson: Make the fix a too…
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- decision 2026-11-04: T-3006's arm comparison runs on local models (gemma 12B, MiMo 9B) instead of the 27B: the Jarvis profiles need LLM_API_KEY, which is never stored, s…
- similar past tasks were M: consider --tier M
## Files touched
- plugin/lib/sampo/doctor.py
- plugin/tests/test_doctor.py
- CHANGELOG.md
