---
id: T-3017
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T20:27:34Z
updated: 2026-11-04T23:56:20Z
builder_model: haiku
route_probe: 1
base: a9df127fe2aa1c3bd1943e15d576c3dfd7372487
base_tree: 065be57f1fe4c1387d509743dd1c4e42686880f1
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T23:14:25Z
plan0_scope: []
lane_stop: merged 2026-11-04T23:43:57Z
verified: strong
---
# Live page: a local model that is called but not loaded right now (gemma4-12b-32k between…
## Raw request
> Live page: a local model that is called but not loaded right now (gemma4-12b-32k between calls) is drawn on Jarvis's hill as remote; the call row should carry local/remote from the endpoint and the page hang local ones on the gantry
## Interpretation
A local model called but not loaded at the moment (gemma between calls, unloaded by Ollama) has no /api/ps row, so the live server adds it from the call log with where=remote and the page hangs it on Jarvis's hill. The call row should record where the call went (the endpoint's host: loopback = local), and the server should use that, so local models hang on the gantry whether loaded or not.
## Assumptions (confidence)
## Acceptance criteria
- [x] a call row records where (local for a loopback endpoint, remote otherwise), and a called-but-unloaded local model reaches the snapshot as a gpu model, not remote; a row without where keeps today's behaviour — verify with `python3 plugin/tests/run.py test_live test_models`
## Non-goals
## Approach (options → choice → why)
1) note_call writes where: local|remote from the endpoint host it already parses; live.py's call-log fallback uses it (local -> where gpu, so the page hangs it), old rows without it keep today's guess. Likely outcome: right placement with one field. Fails if: a local endpoint is reached by a LAN address (it would read as remote, as today).
2) Use what exists: look the name up in Ollama's /api/tags (installed models). Likely outcome: right for Ollama models. Fails if: the same tag is installed on Jarvis too, or the local server isn't Ollama.
3) Do less: name heuristics in live.js. Fails if: any new model name.
Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: note_call's where; the snapshot's placement of an unloaded local model
2. [x] the field in note_call and its use in live.py's call-log fallback
## Resume here
<!-- auto -->
- 2026-11-04T23:53:20Z steps 2/2 done
- git: foreman/build; 4 uncommitted: plugin/lib/sampo/jeffexport.py, plugin/lib/sampo/smith.py, plugin/tests/test_code.py, plugin/tests/test_jeff_export.py
- touched since last checkpoint: .claude/worktrees/agent-a53e5de90407a3f55/plugin/tests/test_models.py, .claude/worktrees/agent-a53e5de90407a3f55/plugin/lib/sampo/models.py, .claude/worktrees/agent-a53e5de90407a3f55/plugin/tests/test_live.py, .claude/worktrees/agent-a53e5de90407a3f55/plugin/lib/sampo/live.py
## Docs impact
CHANGELOG line written with T-3026's close
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models test_live` → exit 0 · Ran 147 tests in 33.6s (26 classes, 16 at a time; slowest: Page 32s, Serve 12s, Act 11s) / OK [ran] [tree 6d1ee0345af4] [world 2f1906870a] (2026-11-04T23:15:25Z)
- (step 2) `python3 plugin/tests/run.py test_models test_live` → exit 0 · Ran 148 tests in 34.1s (26 classes, 16 at a time; slowest: Page 34s, Serve 14s, Act 13s) / OK [ran] [tree 15834c7e19e3] [world 2f1906870a] (2026-11-04T23:16:34Z)
- `python3 plugin/tests/run.py test_live.Snapshot.test_a_called_but_unloaded_local_model_hangs_on_the_gantry test_live.Snapshot.test_a_ledger_row_seen_first_does_not_hide_a_local_calls_row` → ✗ exit 1 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: Snapshot 1s) / FAILED (1 classes: test_live.Snapshot) (start tree + this task's tests) [ran] [tree b0bd19a34d2b] [world 2f1906870a] (2026-11-04T23:46:21Z)
- `python3 plugin/tests/run.py test_live.Snapshot.test_a_called_but_unloaded_local_model_hangs_on_the_gantry test_live.Snapshot.test_a_ledger_row_seen_first_does_not_hide_a_local_calls_row` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Snapshot 1s) / OK [ran] [tree b0bd19a34d2b] [world 2f1906870a] (2026-11-04T23:46:21Z)
- (ac 1) `python3 plugin/tests/run.py test_live test_models` → exit 0 · Ran 151 tests in 43.0s (26 classes, 16 at a time; slowest: Page 43s, Serve 11s, Act 10s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:54:03Z)
- `python3 plugin/tests/run.py test_live.Snapshot.test_a_called_but_unloaded_local_model_hangs_on_the_gantry test_live.Snapshot.test_a_ledger_row_seen_first_does_not_hide_a_local_calls_row` → exit 0 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: Snapshot 0s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:54:03Z)
- (audit edge) `self: read note_call and the call-log fallback; a row without where keeps today's guess; a ledger row seen first no longer hides a local call (red on the first commit, green on the fix)` → a LAN address to a local server reads as remote (as before); claude stays cloud [tree 4bb5feb560e4] (2026-11-04T23:54:03Z)
- (audit self) `self: read note_call and the call-log fallback; a row without where keeps today's guess; a ledger row seen first no longer hides a local call (red on the first commit, green on the fix)` → no findings [tree 4bb5feb560e4] (2026-11-04T23:54:03Z)
## Log
- 2026-11-04T20:27:34Z created
- 2026-11-04T22:16:01Z planned: it has criteria and steps
- 2026-11-04T22:16:02Z set approved=True
- 2026-11-04T23:14:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3017.builder.md
- 2026-11-04T23:14:24Z focused
- 2026-11-04T23:14:25Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T23:17:21Z red check: test_a_ledger_row_seen_first_does_not_hide_a_local_calls_row fails on 8b3426e0 (before the fix) and passes on 6a040f9c
- 2026-11-04T23:43:57Z merged worktree-agent-a53e5de90407a3f55 (4 file(s))
- 2026-11-04T23:44:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a53e5de90407a3f55
- 2026-11-04T23:53:17Z focused
- 2026-11-04T23:56:20Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3014 [FIX M, done, 3 steps] Live page on real data: fonts served, the ledger in words, every model call animated (local, Jarvis, Smith) — lesson: A live page must be j…
- research live-schema: Server: `sampo live [--port N]`
- T-2938 [FEATURE M, done, 4 steps] An Ollama profile that promises more context than served gets a num_ctx variant (NAME-32k), made or reused — lesson: Make the fix a too…
- decision 2026-11-04: T-3006's arm comparison runs on local models (gemma 12B, MiMo 9B) instead of the 27B: the Jarvis profiles need LLM_API_KEY, which is never stored, s…
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Lessons
- Decide a node's placement from every row that names it, not the first one seen
## Files touched
- plugin/tests/test_live.py
- plugin/tests/test_models.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/live.py
