---
id: T-2995
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T17:58:50Z
updated: 2026-11-04T22:24:02Z
builder_model: haiku
base: 4b3dca08f159e50eaa99ae68458d8bb961826464
base_tree: 19d412d22da7c66b81bc02d1558e4dca287dc4e8
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T17:59:10Z
plan0_scope: []
lane_stop: merged 2026-11-04T18:18:58Z
predict_noted: 2026-11-04T19:59:34Z
verified: strong
unproven: [data, docs, meaning]
---
# Exam keeps green Smith run journals and sampo exam models --traces exports them: the first piece of the distilled actor (T-2971)
## Raw request
> From T-2971 (distil a Smith actor from verified local runs): the exam keeps only events, so the full conversations of green runs are lost; keep them and export them for SFT
## Interpretation
Reading 1 (chosen): two parts: louhi's smith arm copies the run's Smith journal (the messages the model saw and wrote, from its throwaway Smith home) into answers/smith/<scenario>.journal.jsonl when the scenario's verify went green, capped and stripped like the lake; and sampo exam models --traces DIR turns kept journals into chat JSONL for SFT, refusing any run whose worker, planner or any slot was Claude. Reading 2 (ruled out): keep every run's journal; red runs aren't training data and would only cost disk.
## Assumptions (confidence)
## Acceptance criteria
- [x] an exam Smith run whose verify went green keeps its full conversation journal beside its events file, size-capped, names and paths stripped; a red run keeps none — verify with `python3 plugin/tests/run.py test_traces`
- [x] sampo exam models --traces DIR exports kept journals as chat JSONL (system, user, assistant turns with tool calls and results) with provenance (scenario, language, kind, model, outcome), refuses any run with a Claude slot, and drops duplicates — verify with `python3 plugin/tests/run.py test_traces`
## Non-goals
- SFT itself (keep them and export them for SFT: the training is T-2971's next piece; this task keeps and exports)
## Approach (options → choice → why)
1) Copy the journal at the end of the smith arm (green only) and a pure export over answers/smith. Likely outcome: traces accrue with every exam. Fails if: journals are huge; a size cap and the strip bound them.
2) use what exists: rebuild conversations from .events.jsonl. Likely outcome: lossy (no prompts, truncated results). Fails if: SFT needs the exact turns the model saw.
3) do less: export events only. Likely outcome: no trainable traces. Fails if: T-2971 needs conversations.
Choice 1 (80%): exact turns, green only, refuses Claude.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a fake green Smith run keeps its journal, a red one doesn't, a Claude-slot run is refused, the export's chat shape
2. [x] keep the journal in louhi's smith arm; --traces in exam models; map and MASTER lines
3. [x] a live exam smith run on minted scenarios keeps journals; export them; counts in research
## Resume here
<!-- auto -->
- 2026-11-04T21:44:22Z steps 3/3 done
- git: foreman/build; 9 uncommitted: CHANGELOG.md, plugin/lib/sampo/jeffexport.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/mint.py, plugin/lib/sampo/traces.py, plugin/tests/test_jeff_export.py, plugin/tests/test_mint.py, plugin/tests/test_traces.py, site/pages.py
## Docs impact
CHANGELOG line rewritten; research T-2995-traces and T-2995-review
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_traces` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: Traces 1s) / OK [ran] [tree c9785177cd59] [world 2f1906870a] (2026-11-04T18:01:42Z)
- (step 2) `python3 plugin/tests/run.py test_traces` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: Traces 1s) / OK [ran] [tree 30d66c30beb0] [world 2f1906870a] (2026-11-04T18:01:52Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lake test_left_out test_library test_louhi_models test_mcp test_mint test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_traces test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.84s] [ran] [tree 30d66c30beb0] [world 2f1906870a] (2026-11-04T18:07:06Z)
- (step 2) `python3 plugin/tests/run.py test_traces test_exam` → exit 0 · Ran 116 tests in 382.0s (28 classes, 16 at a time; slowest: LeanKind 382s, ExamAuthors 105s, JudgmentKinds 78s) / OK [ran] [tree 51c11c5a364c] [world 2f1906870a] (2026-11-04T19:57:37Z)
- (step 3) `ls state/projects/foreman-4a056f/exam/s5-019/answers/smith/s5-019-m04.journal.jsonl && sampo exam models --traces /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/traces` → exit 0 · state/projects/foreman-4a056f/exam/s5-019/answers/smith/s5-019-m04.journal.jsonl / traces: 2 conversations (0 dupes, 0 Claude runs refused) in /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7 [ran] [tree 0f66a6548c41] [world 2f1906870a] (2026-11-04T20:12:26Z)
- (step 2) `python3 plugin/tests/run.py test_traces test_mint` → exit 0 · Ran 30 tests in 5.1s (4 classes, 16 at a time; slowest: MintWithUntrackedDeps 5s, MintFromRepo 3s, Traces 1s) / OK [ran] [tree 1de54bd4cc36] [world 2f1906870a] (2026-11-04T21:15:57Z)
- `python3 plugin/tests/run.py test_traces` → ✗ exit 1 · Ran 0 tests in 3.1s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (start tree + this task's tests) [ran] [tree 782514a0f944] [world 2f1906870a] (2026-11-04T21:16:27Z)
- `python3 plugin/tests/run.py test_traces` → exit 0 · Ran 11 tests in 1.8s (2 classes, 16 at a time; slowest: Traces 1s, TracesExport 0s) / OK [ran] [tree 782514a0f944] [world 2f1906870a] (2026-11-04T21:16:27Z)
- (ac 1) `python3 plugin/tests/run.py test_traces` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T21:16:27Z [ran] [tree 782514a0f944] [world 2f1906870a] (2026-11-04T21:16:36Z)
- (ac 2) `python3 plugin/tests/run.py test_traces` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T21:16:27Z [ran] [tree 782514a0f944] [world 2f1906870a] (2026-11-04T21:16:36Z)
- (audit intent) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → the live 27B run on minted bugs kept 1 proven journal; the export gives 2 conversations with provenance and no names [tree 782514a0f944] (2026-11-04T21:16:36Z)
- (audit adversary) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a model can't plant training data (repo-side journals ignored, links refused); corrupt meta fails closed; a Claude slot anywhere refuses the run; sensitive sources are refused at mint and export [tree 782514a0f944] (2026-11-04T21:16:36Z)
- (audit edge) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a timeout the grader proves fixed is kept as fixed; a guard-only pass or a close with no verify is not; an oversized run ends on an assistant turn; a bare container with no user still keeps [tree 782514a0f944] (2026-11-04T21:16:36Z)
- (audit maintainer) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → test_traces pins planting, stripping (names, secrets, home, code paths), arguments whole, the cap, proof-only keeping, fail-closed export and the sensitive refusal [tree 782514a0f944] (2026-11-04T21:16:36Z)
- (audit intent) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → the live 27B run on minted bugs kept 1 proven journal; the export gives 2 conversations with provenance and no names [tree ce69163b3cc8] (2026-11-04T21:42:41Z)
- (audit adversary) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a model can't plant training data (repo-side journals ignored, links refused); corrupt meta fails closed; a Claude slot anywhere refuses the run; sensitive sources are refused at mint and export [tree ce69163b3cc8] (2026-11-04T21:42:41Z)
- (audit edge) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a timeout the grader proves fixed is kept as fixed; a guard-only pass or a close with no verify is not; an oversized run ends on an assistant turn; a bare container with no user still keeps [tree ce69163b3cc8] (2026-11-04T21:42:41Z)
- (audit maintainer) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → test_traces pins planting, stripping (names, secrets, home, code paths), arguments whole, the cap, proof-only keeping, fail-closed export and the sensitive refusal [tree ce69163b3cc8] (2026-11-04T21:42:41Z)
- (audit intent) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → the live 27B run on minted bugs kept 1 proven journal; the export gives 2 conversations with provenance and no names [tree bb617924a0d9] (2026-11-04T22:07:34Z)
- (audit adversary) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a model can't plant training data (repo-side journals ignored, links refused); corrupt meta fails closed; a Claude slot anywhere refuses the run; sensitive sources are refused at mint and export [tree bb617924a0d9] (2026-11-04T22:07:34Z)
- (audit edge) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a timeout the grader proves fixed is kept as fixed; a guard-only pass or a close with no verify is not; an oversized run ends on an assistant turn; a bare container with no user still keeps [tree bb617924a0d9] (2026-11-04T22:07:34Z)
- (audit maintainer) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → test_traces pins planting, stripping (names, secrets, home, code paths), arguments whole, the cap, proof-only keeping, fail-closed export and the sensitive refusal [tree bb617924a0d9] (2026-11-04T22:07:34Z)
- (audit intent) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → the live 27B run on minted bugs kept 1 proven journal; the export gives 2 conversations with provenance and no names [tree 39f0fddb5a32] (2026-11-04T22:15:39Z)
- (audit adversary) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a model can't plant training data (repo-side journals ignored, links refused); corrupt meta fails closed; a Claude slot anywhere refuses the run; sensitive sources are refused at mint and export [tree 39f0fddb5a32] (2026-11-04T22:15:39Z)
- (audit edge) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → a timeout the grader proves fixed is kept as fixed; a guard-only pass or a close with no verify is not; an oversized run ends on an assistant turn; a bare container with no user still keeps [tree 39f0fddb5a32] (2026-11-04T22:15:39Z)
- (audit maintainer) `one fm-reviewer pass scoped to traces.py, the keep and export code in louhi.py and test_traces.py: changes needed; fixed test-first: the planted-journal hole (journals read only from Smith's home, no symlinks), corrupt meta now refused, sensitive repos never minted and sensitive or opted-out projects never exported, the path strip narrowed so code keeps its paths, tool-call arguments never cut, the cap drops back to an assistant turn, green needs a passing verify and a grader fix needs a real check, outcome labelled green or fixed, getuser guarded, --export with --traces refused` → test_traces pins planting, stripping (names, secrets, home, code paths), arguments whole, the cap, proof-only keeping, fail-closed export and the sensitive refusal [tree 39f0fddb5a32] (2026-11-04T22:15:39Z)
## Log
- 2026-11-04T17:58:50Z created
- 2026-11-04T17:58:51Z set approved=True
- 2026-11-04T17:58:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2995.builder.md
- 2026-11-04T17:59:09Z focused
- 2026-11-04T17:59:10Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T18:18:58Z merged worktree-agent-a73532dcd0940bef3 (8 file(s))
- 2026-11-04T18:19:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a73532dcd0940bef3
- 2026-11-04T18:23:13Z focused
- 2026-11-04T18:42:24Z step 3 in progress: the local 4B (gemma 12B planning) fixed 0/4 of s4-018's minted Python bugs, so no green run and no journal (the correct behaviour, but no proof of keeping); rerunning with the 27B on jarvis (bg buluqrc5e) for a green run whose journal must be kept; evidence after it ends
- 2026-11-04T18:42:32Z paused: focus moved to T-2991
- 2026-11-04T19:21:43Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T19:21:43Z focused
- 2026-11-04T19:43:38Z focused
- 2026-11-04T19:43:40Z steer: live 27B run fixed 1 of 4 (grader) but no run closed within 40 turns, so no journal was kept; keep when the run closed green OR the hidden check passes on its final tree (the grader's verdict is the stronger proof)
- 2026-11-04T20:05:39Z paused: focus moved to T-3014
- 2026-11-04T20:57:39Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T20:57:39Z focused
- 2026-11-04T21:02:16Z focused
- 2026-11-04T21:05:23Z paused: focus moved to T-3021
- 2026-11-04T21:11:36Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T21:11:36Z focused
- 2026-11-04T21:15:57Z scope: mint.py (sensitive repos refused) and test_mint.py, louhi.py's export branch
- 2026-11-04T21:36:47Z paused: focus moved to T-3023
- 2026-11-04T21:42:40Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T21:42:40Z focused
- 2026-11-04T21:44:24Z paused: focus moved to T-3027
- 2026-11-04T22:07:30Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T22:07:30Z focused
- 2026-11-04T22:15:10Z paused: focus moved to T-3028
- 2026-11-04T22:15:38Z focused
- 2026-11-04T22:24:00Z done
- 2026-11-04T22:24:02Z committed f9eb99d2 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2971 [RESEARCH L, planned, 6 steps] Distil a Smith actor from verified runs: generate fm code runs on the 27B (and the 12B)…
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- the similar finished task took 4 steps
## Lessons
- Training data is an attack surface: anything the model under test can write must never be read back as its own proof; read journals only from the harness's home and fail closed on missing provenance
## Files touched
- plugin/tests/test_traces.py
- plugin/lib/sampo/traces.py
- plugin/lib/sampo/lake.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- plugin/lib/fmtraces.py
- MASTER.md
- docs/map/files-lib-3.md
- plugin/tests/test_live.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/settingsserve.py
- plugin/lib/sampo/live.py
- plugin/lib/sampo/mint.py
- plugin/tests/test_mint.py
- CHANGELOG.md
- site/pages.py
- plugin/tests/test_prove.py
- research/models/bench.jsonl
