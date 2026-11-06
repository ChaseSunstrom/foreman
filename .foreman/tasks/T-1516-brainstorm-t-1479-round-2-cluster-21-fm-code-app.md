---
id: T-1516
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/test_code_tui.py, plugin/tests/fixtures, mods/foreman-ui/tests, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:43Z
updated: 2026-10-22T21:55:38Z
base: 83fe4550cd961493a97127523a198007a555f21e
base_tree: 8f8e570cf973dece1f27f4242a74ed2c1d593fdd
plan0_at: 2026-10-22T21:30:56Z
plan0_scope: [plugin/tests/test_code_tui.py, plugin/tests/fixtures, mods/foreman-ui/tests, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 21): fm code app test net: a width-oracle sweep over ho
## Raw request
> Brainstorm T-1479 round 2 (cluster 21): fm code app test net: a width-oracle sweep over hostile strings for every panel, and a crash during a test saved as a replayable fixture
## Interpretation
A width-oracle sweep over hostile strings (CJK, emoji, combining marks, RTL, zero-width, control characters) for every fm code app panel and every foreman-ui row, and a crash in a TUI test saved as a replayable fixture. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] every panel's rows fill exactly their width for each hostile string; a crash writes a fixture that replays it — verify with `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth`
## Non-goals
## Approach (options → choice → why)
Options: random fuzz only; chosen: a fixed hostile corpus plus the existing fuzz, asserting each rendered row fills exactly its width.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] the sweep
3. [x] crash fixtures
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth` → exit 0 · Ran 3 tests in 0.701s / OK [ran] [tree 93cd607d2139] (2026-10-22T21:33:14Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth` → exit 0 · Ran 3 tests in 0.703s / OK [ran] [tree 93cd607d2139] (2026-10-22T21:33:40Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth.test_a_crash_writes_a_fixture` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree 93cd607d2139] (2026-10-22T21:33:40Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth test_code_tui.Columns` → ✗ exit 1 · Ran 8 tests in 0.957s / FAILED (failures=1) [ran] [tree 31f0dd04c561] (2026-10-22T21:41:13Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth test_code_tui.Columns` → exit 0 · Ran 8 tests in 0.980s / OK [ran] [tree 374cf4b3324b] (2026-10-22T21:42:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth` → exit 0 · Ran 3 tests in 1.690s / OK [ran] [tree b50c18332c01] (2026-10-22T21:54:09Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 174 tests in 17.3s (24 classes, 16 at a time; slowest: Command 17s, Fuzz 17s, Events 7s) / OK [ran] [tree b50c18332c01] (2026-10-22T21:54:27Z)
- (audit self) `sweep of 9 hostile strings over every panel and view (asserted equal to VIEWS) and prompt mode at four sizes; probe text asserted on 100+ screens` → 174 tests green after the merge [tree b50c18332c01] (2026-10-22T21:54:28Z)
- (audit adversary) `crash fixtures named by (label, size, mode, exception type), at most 50, under fixtures/crashes only; replay fails on a stale label` → tested [tree b50c18332c01] (2026-10-22T21:54:28Z)
- (audit design) `VS16 pictographs 2 columns, skin tones zero-width, half-cut wide cells blanked; real-terminal width table asserted` → fixed two renderer bugs and two more from review [tree b50c18332c01] (2026-10-22T21:54:29Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.HostileWidth` → exit 0 · Ran 3 tests in 1.652s / OK [ran] [tree b50c18332c01] (2026-10-22T21:54:38Z)
- (audit adversary) `one fm-reviewer pass (self, adversary, design); findings fixed test-first; criterion green after the merge` → bounded crash fixtures [tree b50c18332c01] (2026-10-22T21:54:38Z)
- (audit design) `one fm-reviewer pass (self, adversary, design); findings fixed test-first; criterion green after the merge` → real terminal widths for emoji and wide cells [tree b50c18332c01] (2026-10-22T21:54:38Z)
- (audit self) `one fm-reviewer pass (self, adversary, design); findings fixed test-first; criterion green after the merge` → no findings [tree b50c18332c01] (2026-10-22T21:54:38Z)
## Log
- 2026-10-22T17:36:43Z created
- 2026-10-22T17:46:49Z steer (T-1520): the width-oracle sweep also covers the foreman-ui mod's rows (mods/foreman-ui/tests)
- 2026-10-22T17:56:05Z set scope=['plugin/tests/test_code_tui.py', 'plugin/tests/fixtures', 'mods/foreman-ui/tests', 'CHANGELOG.md']
- 2026-10-22T21:28:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1516.builder.md
- 2026-10-22T21:30:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1516.builder.md
- 2026-10-22T21:30:55Z focused
- 2026-10-22T21:53:52Z merged worktree-agent-a12fce62f55b30ae2 (4 file(s))
- 2026-10-22T21:53:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a12fce62f55b30ae2
- 2026-10-22T21:53:56Z focused
- 2026-10-22T21:54:30Z scope: plugin/lib/fmcodetui.py (the sweep found real width bugs: VS16, skin tones, half-cut wide cells) and MASTER.md (one line)
- 2026-10-22T21:55:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1509 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 14): fm smoke hostile profiles: torture content (long w — lesson: A new check added to an existing g…
- T-1512 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 17): fm code app motion and visuals: a hush key cycling — lesson: Contrast ratio alone can't tell tw…
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, mods/foreman-ui/tests/fixtures/pane-busy.ts, mods/foreman-ui/tests/fixtures/replay.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tests/replay.test.tsx, plugin/tests/fix…; re-ground the plan against them before editing
## Why not caught
the panels had only been tested with ASCII and plain CJK
## Lessons
- A width test that shares the implementation's width rule can only find structural bugs; anchor it with a table of widths real terminals draw
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/fixtures/crashes/17210c76a9.json
- plugin/tests/fixtures/crashes/25de27587e.json
- plugin/tests/fixtures/crashes/43a32cf120.json
- plugin/tests/fixtures/crashes/882a3bdab2.json
- plugin/tests/fixtures/crashes/8d3ce6241f.json
- plugin/tests/fixtures/crashes/962d83cd11.json
- plugin/tests/fixtures/crashes/9c7fe29a6b.json
- plugin/tests/fixtures/crashes/9e9322b8aa.json
- plugin/tests/fixtures/crashes/ab73f8c41d.json
- plugin/tests/fixtures/crashes/e38a193214.json
- plugin/tests/fixtures/crashes/f19f6e5f49.json
- plugin/tests/fixtures/crashes/f60df7fc3d.json
