---
id: T-1329
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:08Z
updated: 2026-10-21T06:07:08Z
base: 25e56aed6c517b74a658d5daa62d7dd508ef0bc4
base_tree: 75b10ba237a9aab6034fb29b06a8b8693867c841
plan0_at: 2026-10-21T05:30:45Z
plan0_scope: []
verified: strong
---
# Live progress from a CLI runner: what claude (stream-json) or codex (--json) is doing shows in Activity as it happens, with a heartbeat when it's quiet
## Raw request
> Live progress from a CLI runner: what claude (stream-json) or codex (--json) is doing shows in Activity as it happens, with a heartbeat when it's quiet
## Interpretation
A run that hands work to a coding CLI shows nothing for minutes today (the nixie report). Make each tool use the CLI makes show in Activity as it happens, and a ticking 'still working' line while it is quiet, for the worker and the planner alike.
## Assumptions (confidence)
## Acceptance criteria
- [x] a claude worker or planner turn shows each tool use as an Activity line as it happens (Read → read FILE, Edit/Write → edit FILE, Bash → run CMD, Grep/Glob → search PATTERN; cut to 200 characters), replayed in tests from a real recorded stream (plugin/tests/fixtures/claude-worker-stream.jsonl, this machine's paths removed) — verify with `python3 plugin/tests/run.py test_code_worker`
- [x] the planner's text and token counts still come from the stream's final result line; a malformed line is skipped, and a stream that ends without a result line is the same error as today — verify with `python3 plugin/tests/run.py test_code_worker`
- [x] while any CLI turn prints nothing a reader can show, fm code emits a working event every 10 s (FM_HEARTBEAT sets it for tests) from the thread that reads the CLI's output, and the TUI shows it as a ticking line that the next real line replaces — verify with `python3 plugin/tests/run.py test_code_worker test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: (A) a reader thread per CLI turn that splits lines, parses claude's stream-json and ticks on idle via select; (B) a main-thread wait loop that polls and emits heartbeats while a pump thread parses lines; (C) parse only after the turn ends (no live view). Choice: A, one shared fmcore.pump used by run_bounded (workers) and fmmodels._cli (planner): every live emit comes from one thread, so no interleaving; select keeps it stdlib and works on Linux and macOS. Claude's runner templates switch to --output-format stream-json --verbose; the planner reads its reply from the final result line; a stream with no result line is a ModelError. Codex --json parsing is left for later (captured), since only claude's stream was recorded here.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests with a fake streaming CLI
2. [x] Stream parsing per runner; progress events; TUI heartbeat
## Resume here
<!-- auto -->
- 2026-10-21T05:46:56Z step 1/2: Failing tests with a fake streaming CLI
- git: foreman/build; 9 uncommitted: CHANGELOG.md, README.md, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcore.py, plugin/lib/fmmodels.py, plugin/tests/test_code_tui.py, plugin/tests/test_code_worker.py, plugin/tests/fixtures/claude-worker-stream.jsonl
- touched since last checkpoint: plugin/tests/fixtures/claude-worker-stream.jsonl, plugin/tests/test_code_tui.py, plugin/lib/fmcore.py, plugin/lib/fmcode.py, plugin/lib/fmmodels.py, plugin/tests/test_code_worker.py, plugin/lib/fmcodetui.py, CHANGELOG.md, README.md, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1330_task_tests.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker test_code_tui` → ✗ exit 1 · Ran 134 tests in 111.9s (14 classes, 16 at a time; slowest: Worker 112s, Fuzz 20s, Command 8s) / FAILED (2 classes) [ran] [tree f81cffc41e17] (2026-10-21T05:33:09Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error:|assert" | head -20` → ✗ exit 1 · FAILED (errors=1) / FAILED (1 classes) [ran] [tree 573258452ebb] (2026-10-21T05:36:59Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error:|assert" | head -20` → ✗ exit 1 · FAILED (errors=1) / FAILED (1 classes) [ran] [tree 573258452ebb] (2026-10-21T05:36:59Z)
- (ac 3) `python3 plugin/tests/run.py test_code_worker test_code_tui 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error:|assert" | head -20` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 7a148d36dd6a] (2026-10-21T05:39:14Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code_tui test_models` → exit 0 · Ran 187 tests in 105.9s (20 classes, 16 at a time; slowest: Worker 106s, Fuzz 16s, Command 9s) / OK [ran] [tree ab6b8926df1b] (2026-10-21T05:45:21Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED" | head` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes) [ran] [tree ba8b27ba1bcc] (2026-10-21T05:50:40Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED" | head` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes) [ran] [tree ba8b27ba1bcc] (2026-10-21T05:50:40Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code_tui test_models test_code` → exit 0 · Ran 235 tests in 113.0s (32 classes, 16 at a time; slowest: Worker 113s, Bench 32s, Review 22s) / OK [ran] [tree b2eae48126eb] (2026-10-21T05:54:59Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker test_code_tui` → exit 0 · Ran 138 tests in 119.3s (14 classes, 16 at a time; slowest: Worker 119s, Fuzz 24s, Command 13s) / OK [ran] [tree b2eae48126eb] (2026-10-21T06:00:06Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 54 tests in 110.4s (1 classes, 16 at a time; slowest: Worker 110s) / OK [ran] [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 54 tests in 110.4s (1 classes, 16 at a time; slowest: Worker 110s) / OK [ran] [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (ac 3) `python3 plugin/tests/run.py test_code_worker test_code_tui` → exit 0 · Ran 138 tests in 114.7s (14 classes, 16 at a time; slowest: Worker 114s, Fuzz 15s, Command 9s) / OK [ran] [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (audit intent) `one fm-reviewer pass (five lenses); 6 findings fixed test-first (callbacks guarded so the pipe always drains; control characters stripped; a result with no reply text is an error; stream parsing follows the template, so a code.toml override works; late lines ignored; live targets redacted); real claude run closed with 16 live tool events` → each claude tool use shows live for worker and planner; reply and tokens from the final result line; heartbeat every FM_HEARTBEAT s from the reader thread, one ticking TUI line [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (audit adversary) `one fm-reviewer pass (five lenses); 6 findings fixed test-first (callbacks guarded so the pipe always drains; control characters stripped; a result with no reply text is an error; stream parsing follows the template, so a code.toml override works; late lines ignored; live targets redacted); real claude run closed with 16 live tool events` → tool targets and names carry no control characters (OSC 52 test); targets redacted; nothing from the stream runs [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (audit edge) `one fm-reviewer pass (five lenses); 6 findings fixed test-first (callbacks guarded so the pipe always drains; control characters stripped; a result with no reply text is an error; stream parsing follows the template, so a code.toml override works; late lines ignored; live targets redacted); real claude run closed with 16 live tool events` → malformed lines skipped; a stream with no result, or a result with no text (error_max_turns), is a ModelError; a raising callback can't stall the CLI; late lines after a turn show nothing [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (audit operator) `one fm-reviewer pass (five lenses); 6 findings fixed test-first (callbacks guarded so the pipe always drains; control characters stripped; a result with no reply text is an error; stream parsing follows the template, so a code.toml override works; late lines ignored; live targets redacted); real claude run closed with 16 live tool events` → plain fm code prints the tool lines and 'working (N s)'; --json gives tool and working events; the journal keeps claude's reply, not the stream [tree b2eae48126eb] (2026-10-21T06:03:52Z)
- (audit maintainer) `one fm-reviewer pass (five lenses); 6 findings fixed test-first (callbacks guarded so the pipe always drains; control characters stripped; a result with no reply text is an error; stream parsing follows the template, so a code.toml override works; late lines ignored; live targets redacted); real claude run closed with 16 live tool events` → one pump for workers and planners; stream parsing keys on --output-format stream-json in the template; codex/gemini parsing captured as T-1366 [tree b2eae48126eb] (2026-10-21T06:03:52Z)
## Log
- 2026-10-21T03:24:08Z created
- 2026-10-21T03:36:41Z grounding (a real claude -p --output-format stream-json --verbose call): one JSON object per line; type=assistant → message.content blocks: tool_use {name: Read|Edit|Write|Bash|Grep|Glob…, input: {file_path|command|pattern}} and text; type=user → tool_result; type=result → result (final text), usage, total_cost_usd, is_error; plus system lines (hook_started/hook_response, init with model and tools, ui_toast), rate_limit_event. Plan: the claude runner's work and plan templates use stream-json --verbose; run_bounded/_cli read lines as they come and turn tool_use into progress events (action, target), text into say; the final result line replaces --output-format json for the planner's text and usage. Other CLIs: codex exec --json (to check), else a heartbeat every 10 s from the harness ('claude working, 40 s').
- 2026-10-21T03:41:18Z steer (second plan): criteria split per behaviour; claude's format from a real recorded stream (fixture), codex streaming left out until a real codex stream can be recorded (heartbeat covers it); heartbeat ticks from the output reader thread with FM_HEARTBEAT for tests; existing worker and planner tests stay as the regression guard
- 2026-10-21T03:48:20Z steer (catalogue R6): add a 'launched' event naming the runner, pid and what it waits on within 1 s of spawn, before any model output, so no screen is ever blank
- 2026-10-21T05:30:45Z focused
- 2026-10-21T05:45:21Z real run (claude 2.1.305, scratch repo, no model): fm code 'make calc.add add' --json closed T-0001 with 16 live tool events (read/run/edit), a runner note and the tree check intact; first try stopped because the harness wrote its events file inside the repo (the planner tree check refused it, as it should)
- 2026-10-21T05:46:58Z paused: focus moved to T-1331
- 2026-10-21T05:47:46Z focused
- 2026-10-21T05:57:58Z scope: plugin/lib/fmcore.py, plugin/lib/fmmodels.py, plugin/lib/fmcodetui.py, plugin/tests/fixtures/claude-worker-stream.jsonl, README.md, CHANGELOG.md — the shared reader (pump), the planner path, the TUI lines, the recorded stream, docs
- 2026-10-21T06:07:06Z done
- 2026-10-21T06:07:08Z committed 28a773ef (9 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The single acceptance criterion bundles three distinct behaviors (per-tool-use Activity lines, both runners claude and codex, and a ticking heartbeat) behind one test command, and it says nothing about what "passes" means. A fake CLI that only emits claude-style events would pass while codex …
- HIGH: The plan never says how the real event schemas will be learned. The claude stream-json and codex --json formats are versioned and differ (tool_use blocks nested in assistant messages vs. item.started/completed events). Writing the fake CLI from memory bakes in guesses, so tests pass while the…
- HIGH: The heartbeat is timing-dependent, and the plan doesn't say how it will be tested without sleeping. It also doesn't say where the ticker runs: a TUI-side timer or a runner-side event. If the runner blocks reading stdout, there is nowhere to tick. — Decide that the reader runs in a thread or u…
- MEDIUM: Failure and edge handling is missing: malformed or partial JSON lines, a CLI that exits nonzero mid-stream, stderr interleaving, very long tool inputs (the Activity line should be truncated), and the fallback when the CLI lacks the streaming flag. The final result must still be extracted fr…
- MEDIUM: Switching runners to stream-json/--json changes the output format that the existing result parsing depends on, which is a regression risk for current worker and planner flows. There is no rollback or flag. — Keep the existing tests in the suite as the regression guard (run the full test_cod…
- LOW: Step 1 is marked as the current step, but the files and modules involved (plugin/tests, worker/planner/TUI) aren't identified, and the scope of "worker or planner" is unclear: both, or only the paths that use CLI runners. — List the touched modules and confirm that both the worker and planner …
Verdict: revise — the direction is sound, but the acceptance criterion is too coarse, the event schemas are unverified, and the heartbeat design is undefined, so tests could pass while the real feature doesn't work.
## Dissent
- [ ] HIGH: The single acceptance criterion bundles three distinct behaviors (per-tool-use Activity lines, both runners claude and codex, and a ticking heartbeat) behind one test command, and it says nothing about what "passes" means. A fake CLI that only emits claude-style events would pass while codex …
- [ ] HIGH: The plan never says how the real event schemas will be learned. The claude stream-json and codex --json formats are versioned and differ (tool_use blocks nested in assistant messages vs. item.started/completed events). Writing the fake CLI from memory bakes in guesses, so tests pass while the…
- [ ] HIGH: The heartbeat is timing-dependent, and the plan doesn't say how it will be tested without sleeping. It also doesn't say where the ticker runs: a TUI-side timer or a runner-side event. If the runner blocks reading stdout, there is nowhere to tick. — Decide that the reader runs in a thread or u…
- [ ] MEDIUM: Failure and edge handling is missing: malformed or partial JSON lines, a CLI that exits nonzero mid-stream, stderr interleaving, very long tool inputs (the Activity line should be truncated), and the fallback when the CLI lacks the streaming flag. The final result must still be extracted fr…
- [ ] MEDIUM: Switching runners to stream-json/--json changes the output format that the existing result parsing depends on, which is a regression risk for current worker and planner flows. There is no rollback or flag. — Keep the existing tests in the suite as the regression guard (run the full test_cod…
- [ ] LOW: Step 1 is marked as the current step, but the files and modules involved (plugin/tests, worker/planner/TUI) aren't identified, and the scope of "worker or planner" is unclear: both, or only the paths that use CLI runners. — List the touched modules and confirm that both the worker and planner …
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- T-1328 [FEATURE M, done, 5 steps] Runners: fm code finds every model and coding CLI on the machine, works with no setup, and one config line picks the default — lesson: …
- decision 2026-09-26: T-0014 fm run: minimal one-shot worker (fresh claude -p per task, drive scoped to that task via FOREMAN_DRIVE_TASK, per-task timeout, stop on no pro…
## Lessons
- A reader thread that also emits must guard its callbacks: an exception there stops the draining and the child blocks on a full pipe
## Plan gaps
- failed first: step 1 Failing tests with a fake streaming CLI
## Files touched
- plugin/tests/fixtures/claude-worker-stream.jsonl
- plugin/tests/test_code_worker.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcore.py
- plugin/lib/fmcode.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- README.md
