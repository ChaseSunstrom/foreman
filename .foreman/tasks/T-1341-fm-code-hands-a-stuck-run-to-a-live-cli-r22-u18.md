---
id: T-1341
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, plugin/tests/test_code_tui.py, plugin/tests/test_code.py, CHANGELOG.md, README.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:28Z
updated: 2026-10-23T14:10:58Z
base: 62e1804074043dbc853b0496dcfd8759b8241820
base_tree: 48c693ce4cc14c5653de7a0f16b6a322b2048dd1
plan0_at: 2026-10-23T13:59:37Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, plugin/tests/test_code_tui.py, plugin/tests/test_code.py, CHANGELOG.md, README.md]
verified: strong
---
# Fm code hands a stuck run to a live CLI (R22+U18): x on a stuck or blocked run suspends th
## Raw request
> fm code hands a stuck run to a live CLI (R22+U18): x on a stuck or blocked run suspends the app and opens the chosen CLI interactively in the project with the task brief as its opening prompt; on exit the app returns and re-runs the task's checks
## Interpretation
When an fm code run stalls or ends blocked, the person can only stop, wait, resume or switch runner. x on that card hands the task to a live CLI: the app stops the run, gives the terminal to the chosen CLI (the run's runner when it has an interactive form, else claude) in the project, with the task's brief as its opening prompt (task, plan title, criteria with their commands, why the run stopped); when the person exits it, the app takes the terminal back and re-runs the task's checks through fm code's own guarded path (fm code --recheck ID: each criterion's command through Foreman's guard, recorded as evidence), so the screen shows what holds now.
## Assumptions (confidence)
## Acceptance criteria
- [x] x on a stall or failure card stops the run and asks the screen loop to hand the terminal to the CLI with the brief; after it, the app starts fm code --recheck ID — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] fm code --recheck ID re-runs an ended run's criteria through the guard, records each as evidence, and streams plan, task and verify events — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
Complete version: the key on both cards, the CLI chosen honestly (installed, interactive), the brief as the first prompt, the terminal handed over and taken back cleanly, the checks re-run guarded and recorded, the result on screen with the next command. Options for the hand-over: the terminal session's own leave/enter around a blocking child (chosen: the Ctrl-Z path already restores and re-enters), a new terminal window (desktop-specific), tmux split (only in tmux). For the re-check: fm code --recheck ID reusing Run.verify (chosen: the guard and evidence as in a run), the TUI running commands itself (no guard), --resume (a blocked run's journal is ended, and a resume would re-do the human's step with the model).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the hand-over and the recheck
2. [x] fm code --recheck, the LIVE templates, App.hand_off and the loop's outside(), CHANGELOG and README
## Resume here
## Docs impact
README.md (fm code tui paragraph: x hands a stuck run to a live CLI, then the recheck), CHANGELOG.md, fm code --help (--recheck)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui test_code` → ✗ exit 1 · Ran 429 tests in 81.9s (90 classes, 16 at a time; slowest: Worker 82s, Fakes 47s, Bench 25s) / FAILED (2 classes) [ran] [tree cc68f8b0d8f8] (2026-10-23T14:02:33Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_code` → exit 0 · Ran 429 tests in 76.2s (90 classes, 16 at a time; slowest: Worker 76s, Fakes 44s, Bench 20s) / OK [ran] [tree 4e31c78d89d5] (2026-10-23T14:05:15Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code test_cli test_docs` → exit 0 · Ran 618 tests in 78.4s (141 classes, 16 at a time; slowest: Worker 78s, Fakes 45s, TaskLifecycle 29s) / OK [ran] [tree 4e31c78d89d5] (2026-10-23T14:06:35Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 222 tests in 8.2s (42 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 4e31c78d89d5] (2026-10-23T14:06:44Z)
- (ac 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 429 tests in 76.1s (90 classes, 16 at a time; slowest: Worker 76s, Fakes 44s, Bench 21s) / OK [ran] [tree 4e31c78d89d5] (2026-10-23T14:08:00Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 222 tests in 8.2s (42 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 4e31c78d89d5] (2026-10-23T14:09:36Z)
- (ac 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 429 tests in 76.1s (90 classes, 16 at a time; slowest: Worker 76s, Fakes 44s, Bench 21s) / OK [ran] [tree 4e31c78d89d5] (2026-10-23T14:09:36Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the hand-over stops the run first (a stall's live child is killed, waited up to 5 s), runs the CLI with the app's terminal restored and Ctrl-C left to the CLI (the app ignores SIGINT meanwhile, the child gets it back), then re-enters and redraws; the brief is printable text only; the recheck is fm code's own Run.verify on the saved plan (guard first, evidence recorded, a refusal says so and runs nothing), exit 1 while any fails; tested on a real blocked run fixed by hand: 1/1 pass, then a break: exit 1` → a run the model can't finish goes to a person in a real CLI with the task's context, and coming back proves what holds through the same guarded checks [tree 4e31c78d89d5] (2026-10-23T14:09:36Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the hand-over stops the run first (a stall's live child is killed, waited up to 5 s), runs the CLI with the app's terminal restored and Ctrl-C left to the CLI (the app ignores SIGINT meanwhile, the child gets it back), then re-enters and redraws; the brief is printable text only; the recheck is fm code's own Run.verify on the saved plan (guard first, evidence recorded, a refusal says so and runs nothing), exit 1 while any fails; tested on a real blocked run fixed by hand: 1/1 pass, then a break: exit 1` → no task yet (said), no interactive CLI (said; the run goes on), the run's runner not interactive or not installed (claude), a live stall (stopped first), an unknown id for --recheck (exit 1, no journal), a check the guard refuses (said, nothing run), a CLI that won't start (said) [tree 4e31c78d89d5] (2026-10-23T14:09:36Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the hand-over stops the run first (a stall's live child is killed, waited up to 5 s), runs the CLI with the app's terminal restored and Ctrl-C left to the CLI (the app ignores SIGINT meanwhile, the child gets it back), then re-enters and redraws; the brief is printable text only; the recheck is fm code's own Run.verify on the saved plan (guard first, evidence recorded, a refusal says so and runs nothing), exit 1 while any fails; tested on a real blocked run fixed by hand: 1/1 pass, then a break: exit 1` → the CLI and its argv come from a fixed table, the brief is one argv element (no shell), plan-written check commands run only through the guard and recorded as evidence, exactly as in a run; nothing here grants or skips a check [tree 4e31c78d89d5] (2026-10-23T14:09:36Z)
## Log
- 2026-10-21T03:47:28Z created
- 2026-10-23T13:56:04Z set tier=M, scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcodeterm.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_code.py', 'CHANGELOG.md', 'README.md']
- 2026-10-23T13:59:36Z focused
- 2026-10-23T14:10:56Z done
- 2026-10-23T14:10:58Z committed 71c0ed31 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research T-1330-review: Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands. [stale: plugin/lib/fm…
- decision 2026-10-23: A broken code.toml: fm code config falls back to defaults and names the line; runs keep refusing it
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodeterm.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Handing a terminal to a child means the parent must ignore SIGINT while the child gets it back (preexec), or Ctrl-C in the child kills the app
## Plan gaps
- failed first: step 1 red tests: the hand-over and the recheck
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- README.md
