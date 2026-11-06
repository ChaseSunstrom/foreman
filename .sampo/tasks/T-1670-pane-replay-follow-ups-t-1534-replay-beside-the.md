---
id: T-1670
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/tools/pane_replay.py, mods/foreman-ui/tests/replay.test.tsx, mods/foreman-ui/tests/fixtures/golden.ts, plugin/tests/test_ui_replay.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T20:59:53Z
updated: 2026-10-29T20:24:31Z
base: 76a4e4aafe42946a0f9f56cba19524944e52709e
base_tree: 535f6bdc1f3eb95e278a57327eeeab6e3f26b17c
plan0_at: 2026-10-23T17:55:53Z
plan0_scope: [mods/foreman-ui/tools/pane_replay.py, mods/foreman-ui/tests/replay.test.tsx, mods/foreman-ui/tests/fixtures/golden.ts, plugin/tests/test_ui_replay.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Pane replay follow-ups (T-1534): replay beside the task timeline in fm page, SVG/PNG outpu
## Raw request
> Pane replay follow-ups (T-1534): replay beside the task timeline in fm page, SVG/PNG output, committed golden frames, the kit clock set to the recorded view's time, forked-skill visual QA
## Interpretation
Follow-ups of the pane replay (T-1534): a replayed frame as SVG (and PNG with rsvg-convert) for docs and reviews, and a committed golden frame: the mod's own replay test (run by the claude plugin test gate) compares the pane drawn from the synthetic fixture with tests/fixtures/golden.ts, which pane_replay.py golden --update rewrites. Left out: the kit clock from the recorded view's time (fm ui --json carries no capture time; the frozen clock already makes runs reproducible), replay beside the task timeline in fm page (an Artifact page only Claude publishes) and forked-skill visual QA (a skill for a check the gate now makes).
## Assumptions (confidence)
## Acceptance criteria
- [x] pane_replay.py svg writes a valid SVG of a replayed frame (PNG with rsvg-convert) and golden compares or rewrites the committed golden; the mod's replay test fails when the pane drifts from it — verify with `python3 plugin/tests/run.py test_ui_replay`
## Non-goals
## Approach (options → choice → why)
Golden: (a) the text layout in a Python test (tests never reach the real claude, T-0283); (b) the drawn tree compared inside replay.test.tsx, which the gate already runs; (c) a pixel PNG (rsvg and fonts vary by machine). Chosen (b): exact, no new runner, and the failure names the update command. SVG: the text frame laid out as monospace lines, escaped, PNG via the rsvg-convert the photo booth already uses.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] svg and png output
3. [x] golden frame and its kit check
4. [x] docs
## Resume here
## Docs impact
CHANGELOG and MASTER lines from the lane cover the verbs; no new flags
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ui_replay` → ✗ exit 1 · Ran 17 tests in 2.1s (5 classes, 16 at a time; slowest: Run 1s, Frames 0s, Tool 0s) / FAILED (1 classes) [ran] [tree a3f85c3a2b0a] (2026-10-23T17:55:55Z)
- (step 1) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 17 tests in 1.3s (5 classes, 16 at a time; slowest: Run 1s, Frames 0s, Tool 0s) / OK [ran] [tree c70e1ebe3045] (2026-10-23T17:57:38Z)
- (step 2) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 17 tests in 1.3s (5 classes, 16 at a time; slowest: Run 1s, Frames 0s, Tool 0s) / OK [ran] [tree c70e1ebe3045] (2026-10-23T17:57:40Z)
- (step 3) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 17 tests in 1.3s (5 classes, 16 at a time; slowest: Run 1s, Frames 0s, Tool 0s) / OK [ran] [tree c70e1ebe3045] (2026-10-23T17:57:42Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 150 tests across 4 files. [11.88s] [ran] [tree c70e1ebe3045] (2026-10-23T17:57:55Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_suite_hygiene` → exit 0 · Ran 78 tests in 9.3s (21 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 1s, UndefinedNames 1s) / OK [ran] [tree c70e1ebe3045] (2026-10-23T17:58:05Z)
- (ac 1) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 17 tests in 1.3s (5 classes, 16 at a time; slowest: Run 1s, Frames 0s, Fixture 0s) / OK [ran] [tree c70e1ebe3045] (2026-10-23T17:58:07Z)
- (ac 1) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 20 tests in 1.3s (5 classes, 16 at a time; slowest: Run 1s, Frames 0s, Layout 0s) / OK [ran] [tree ba095ce5d1a7] (2026-10-29T20:24:12Z)
- (audit intent) `one fm-reviewer pass over the merged diff (intent, edge, maintainer); 7 findings fixed test-first` → golden --update recovers from a missing or conflicted golden (stub in the staged copy; update never reads it); a compare no longer blesses a missing golden [tree ba095ce5d1a7] (2026-10-29T20:24:12Z)
- (audit edge) `one fm-reviewer pass over the merged diff (intent, edge, maintainer); 7 findings fixed test-first` → .PNG/.png both convert, other extensions refused; rsvg-convert failure is one line, not a traceback; U+2028 in a title no longer splits the tree line [tree ba095ce5d1a7] (2026-10-29T20:24:12Z)
- (audit maintainer) `one fm-reviewer pass over the merged diff (intent, edge, maintainer); 7 findings fixed test-first` → golden drift diffs the text rows, not 30 KB raster JSON; the string-check test names the mod gate that runs the comparison [tree ba095ce5d1a7] (2026-10-29T20:24:12Z)
- (audit adversary) `one fm-reviewer pass over the merged diff (intent, edge, maintainer); 7 findings fixed test-first` → no new input surface; the view still goes in as JSON.parse data [tree ba095ce5d1a7] (2026-10-29T20:24:12Z)
- (audit operator) `one fm-reviewer pass over the merged diff (intent, edge, maintainer); 7 findings fixed test-first` → golden prints 'none committed' with the --update hint [tree ba095ce5d1a7] (2026-10-29T20:24:12Z)
## Log
- 2026-10-22T20:59:53Z created
- 2026-10-23T17:55:12Z set type=FEATURE, tier=M, scope=['mods/foreman-ui/tools/pane_replay.py', 'mods/foreman-ui/tests/replay.test.tsx', 'mods/foreman-ui/tests/fixtures/golden.ts', 'plugin/tests/test_ui_replay.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:55:15Z lane: ~/.claude/foreman.lanes/T-1670 on foreman/T-1670
- 2026-10-23T17:55:52Z focused
- 2026-10-29T20:13:56Z merged foreman/T-1670 (6 file(s))
- 2026-10-29T20:13:59Z lane removed: ~/.claude/foreman.lanes/T-1670
- 2026-10-29T20:22:52Z focused
- 2026-10-29T20:24:29Z done
- 2026-10-29T20:24:31Z committed c2d6f013 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-23: T-1670: left out the recorded-time clock, the fm page timeline and forked-skill QA
- research T-1534-review: Verdict:** changes needed (one MEDIUM, easy to fix). The data-not-code question comes out clean.
- T-1534 [FEATURE M, done, 4 steps] Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with — lesson: Determinism checks need the render…
- T-1546 [FEATURE M, done, 6 steps] Round 3 (T-1520): fm code app visual extras: a photo booth for frames, an isometric layout — lesson: A chaos harness is safe to run any…
- similar finished tasks took 4–6 steps
- likely tests for the scope: plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, mods/foreman-ui/tests/fixtures/golden.ts, mods/foreman-ui/tests/replay.test.tsx, mods/foreman-ui/tools/pane_replay.py, plugin/tests/test_ui_replay.py; re-ground the plan against them before editing
## Lessons
- a golden tool must bootstrap itself: never make the update path read or import the file it is about to rewrite
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_ui_replay.py
- mods/foreman-ui/tools/pane_replay.py
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/tests/fixtures/golden.ts
- mods/foreman-ui/tests/replay.test.tsx
