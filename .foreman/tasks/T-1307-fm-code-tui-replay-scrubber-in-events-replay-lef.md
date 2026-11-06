---
id: T-1307
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T00:22:55Z
updated: 2026-10-23T13:37:10Z
base: 458143b66aa2ffca27168f75208ba2dd9bf33c3c
base_tree: f34c278cd36aefe8e478686c2ebe2333d2762805
plan0_at: 2026-10-23T13:32:37Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Fm code tui replay scrubber: in --events replay, left/right step through the run's events
## Raw request
> fm code tui replay scrubber: in --events replay, left/right step through the run's events and the panels fade between views (log, diff, history) instead of jumping (C11)
## Interpretation
A replayed run (fm code tui --events FILE, or Enter on a past run) shows only its end. Left and right step one event back or forward (Home and End jump to the start and the end), rebuilding the screen at that event, so a run can be read the way it happened. A switch between the run, its diff and past runs fades in for a quarter second instead of jumping; with motion off it jumps as before (a fade is a colour change, so reduced motion keeps it).
## Assumptions (confidence)
## Acceptance criteria
- [x] on a replay, left/right/Home/End step through its events and say which; a live run ignores them; view switches fade in unless motion is off — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Complete version: the events kept by replay, the four keys only on a replay with no live run, where you are said in the message, the fade over every view switch, honest under motion settings. Options for stepping: rebuild State from events[:n] (chosen: State.apply is the one reducer, a run is hundreds of events, so a rebuild is instant), keep snapshots per event (memory for nothing), an inverse per event (a second reducer to keep right). Fade: faded() over the frame's cells for 0.25 s after the view changes (chosen; FX.since keys it, mono has no colours to mix so it stays still), or a per-panel reveal (the diff already has one, T-1312).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the scrubber and the fade
2. [x] replay keeps its events, the scrub keys, the fade in render; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md; the replay's own message names the keys (◂▸ and its event count), the help poster lists configurable keys only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 214 tests in 8.0s (40 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / FAILED (2 classes) [ran] [tree 3725ffe05af6] (2026-10-23T13:33:09Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 214 tests in 8.0s (40 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree b74c9e6dfeed] (2026-10-23T13:34:43Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code` → exit 0 · Ran 420 tests in 91.5s (88 classes, 16 at a time; slowest: Worker 91s, Fakes 45s, Bench 21s) / OK [ran] [tree b74c9e6dfeed] (2026-10-23T13:36:15Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 214 tests in 14.9s (40 classes, 16 at a time; slowest: Fuzz 14s, Command 14s, Events 6s) / OK [ran] [tree b74c9e6dfeed] (2026-10-23T13:36:31Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 214 tests in 14.9s (40 classes, 16 at a time; slowest: Fuzz 14s, Command 14s, Events 6s) / OK [ran] [tree b74c9e6dfeed] (2026-10-23T13:36:48Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): stepping rebuilds State from the file's events through the one reducer, so a step shows exactly what the live run showed then; keys act only on a replay in the main view with no live run, and a new run clears the scrub; the event name shown is printable characters only, 30 at most; the fade restyles the frame's cells for 0.25 s through faded(), stays still with motion off and in mono (no colours to mix); rendered a replay four events back at 110 columns: step 2 running, status bar shows ◂▸ 10/14` → a past run can be read the way it happened, step by step, and moving between views no longer jumps [tree b74c9e6dfeed] (2026-10-23T13:36:48Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): stepping rebuilds State from the file's events through the one reducer, so a step shows exactly what the live run showed then; keys act only on a replay in the main view with no live run, and a new run clears the scrub; the event name shown is printable characters only, 30 at most; the fade restyles the frame's cells for 0.25 s through faded(), stays still with motion off and in mono (no colours to mix); rendered a replay four events back at 110 columns: step 2 running, status bar shows ◂▸ 10/14` → an empty or one-event file (no step hint), past either end (stays), a live run (keys ignored), a prompt over the run (no fade: it counts as the run), motion off and reduced (off jumps; reduced fades, a colour change) [tree b74c9e6dfeed] (2026-10-23T13:36:48Z)
## Log
- 2026-10-21T00:22:55Z created
- 2026-10-23T13:31:58Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'docs/fm-code.md']
- 2026-10-23T13:32:35Z set scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T13:32:37Z focused
- 2026-10-23T13:37:07Z done
- 2026-10-23T13:37:10Z committed 8192efb0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Motion: choreography, timing and reduced motion (fm playbooks show ui/motion)
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research brainstorm-20261020-tui: Method.** I read all of ideas.md (about 560 distinct titles; near-duplicates are merged with "/"). I grepped fmcodetui.py and fmcode.py…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- A reducer that rebuilds from events makes a scrubber free: keep the events, not snapshots
## Plan gaps
- failed first: step 1 red tests: the scrubber and the fade
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
