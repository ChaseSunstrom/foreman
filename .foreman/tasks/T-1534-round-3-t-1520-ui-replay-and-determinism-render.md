---
id: T-1534
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/tests, mods/foreman-ui/tools, mods/foreman-ui/README.md, plugin/lib/fmpage.py, plugin/tests/test_ui_replay.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:46Z
updated: 2026-10-22T21:10:35Z
base: 25ed7207948ea04c6a7389f5848390523ac50994
base_tree: 7b4848d2ef23787498b9b80f2c1adb3700bea894
plan0_at: 2026-10-22T20:38:06Z
plan0_scope: [mods/foreman-ui/tests, mods/foreman-ui/tools, plugin/lib/fmpage.py, plugin/tests/test_ui_replay.py, CHANGELOG.md]
verified: strong
---
# Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with
## Raw request
> Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with no live session, replay a recorded UI session beside the task timeline, a twin-run determinism diff, a locale and environment matrix for golden frames, and visual QA in a forked skill context (c032 c062 c090 c092 c067). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with no live session, replay a recorded UI session beside the task timeline, a twin-run determinism diff, a locale and environment matrix for golden frames, and visual QA in a forked skill context (c032 c062 c090 c092 c067). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [x] the pane renders from a recorded fixture with no live session; two runs of the same fixture are identical — verify with `cd plugin/tests && python3 -m unittest test_ui_replay`
## Non-goals
## Approach (options → choice → why)
Options: live sessions only; chosen: foreman-ui rendered from recorded fixtures (the mod's test harness), a session replay beside the task timeline in fm page, a twin-run determinism diff for golden frames, a locale and environment matrix, and visual QA run as a forked skill.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] fixture rendering
3. [x] replay and determinism
4. [x] locale matrix and forked QA
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ui_replay` → ✗ exit 1 · Ran 6 tests in 0.2s (2 classes, 16 at a time; slowest: Layout 0s, Replay 0s) / FAILED (2 classes) [ran] [tree 79121ffbbac9] (2026-10-22T20:43:34Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 133 tests across 3 files. [31.86s] [ran] [tree 7799cc749138] (2026-10-22T20:51:53Z)
- (step 3) `python3 mods/foreman-ui/tools/replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts` → exit 0 · identical: run 1, run 2 (80x40) [ran] [tree 7799cc749138] (2026-10-22T20:51:57Z)
- (step 4) `python3 mods/foreman-ui/tools/replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts --matrix` → exit 0 · identical: run 1, run 2, TZ=Pacific/Kiritimati LANG=de_DE.UTF-8 (80x40) [ran] [tree 7799cc749138] (2026-10-22T20:52:03Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 133 tests across 3 files. [44.47s] [ran] [tree 737efd5f7dcd] (2026-10-22T20:54:24Z)
- (step 3) `python3 mods/foreman-ui/tools/replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts` → exit 0 · identical: run 1, run 2 (80x40) [ran] [tree 737efd5f7dcd] (2026-10-22T20:54:28Z)
- (step 4) `python3 mods/foreman-ui/tools/replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts --matrix` → exit 0 · identical: run 1, run 2, TZ=Pacific/Kiritimati LANG=de_DE.UTF-8 (80x40) [ran] [tree 737efd5f7dcd] (2026-10-22T20:54:35Z)
- (step 1) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 9 tests in 0.6s (3 classes, 16 at a time; slowest: Layout 0s, Tool 0s, Fixture 0s) / OK [ran] [tree 737efd5f7dcd] (2026-10-22T20:54:37Z)
- (step 1) `python3 plugin/tests/run.py test_ui_replay` → exit 0 · Ran 13 tests in 1.4s (4 classes, 16 at a time; slowest: Run 1s, Tool 0s, Fixture 0s) / OK [ran] [tree 961ec6a29709] (2026-10-22T21:04:00Z)
- (step 3) `python3 mods/foreman-ui/tools/pane_replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts` → exit 0 · identical: run 1, run 2 (80x40) [ran] [tree 961ec6a29709] (2026-10-22T21:04:04Z)
- (step 4) `python3 mods/foreman-ui/tools/pane_replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts --matrix` → exit 0 · identical: run 1, run 2, TZ=Pacific/Kiritimati LANG=de_DE.UTF-8 (80x40) [ran] [tree 961ec6a29709] (2026-10-22T21:04:10Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 133 tests across 3 files. [37.62s] [ran] [tree 961ec6a29709] (2026-10-22T21:04:53Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_ui_replay` → exit 0 · Ran 13 tests in 1.050s / OK [ran] [tree f7518f8bde5b] (2026-10-22T21:09:21Z)
- (step 3) `python3 mods/foreman-ui/tools/pane_replay.py twin mods/foreman-ui/tests/fixtures/pane-busy.ts` → exit 0 · identical: run 1, run 2 (80x40) [ran] [tree f7518f8bde5b] (2026-10-22T21:09:24Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1534-review.md)` → fixture stays data (JSON.parse of a string; .ts read from its export default line, extra code refused); escape/C1/bidi from a view stripped before the terminal (clean() ported from kit.ts); claude runs in its own process group, killed whole on timeout [tree f7518f8bde5b] (2026-10-22T21:09:35Z)
- (audit edge) `review edge lens` → UTF-8 decode with replacement (tested with \377); twin identical at 80x40 and 40x12; --matrix with UTC+14 and de_DE [tree f7518f8bde5b] (2026-10-22T21:09:36Z)
- (audit operator) `pane_replay.py twin run by hand after the merge` → identical: run 1, run 2 (80x40) [tree f7518f8bde5b] (2026-10-22T21:09:36Z)
- (audit maintainer) `review maintainer lens` → renamed to pane_replay.py (no clash with fm replay); wiring test named as such; README for the mod [tree f7518f8bde5b] (2026-10-22T21:09:37Z)
- (audit intent) `criterion: the pane renders from a recorded fixture with no live session; two runs identical` → met as a pair: test_ui_replay (13) proves the tool and wiring, claude plugin test mods/foreman-ui and twin prove the engine draws the same bytes [tree f7518f8bde5b] (2026-10-22T21:09:37Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_ui_replay` → exit 0 · Ran 13 tests in 1.025s / OK [ran] [tree f7518f8bde5b] (2026-10-22T21:09:45Z)
- (audit adversary) `one fm-reviewer five-lens pass; 6 findings fixed test-first by the builder; twin identical after the merge` → fixture as data only; terminal escapes stripped; process group killed on timeout [tree f7518f8bde5b] (2026-10-22T21:09:45Z)
- (audit edge) `one fm-reviewer five-lens pass; 6 findings fixed test-first by the builder; twin identical after the merge` → UTF-8 replacement decode, two sizes, time zone and locale matrix [tree f7518f8bde5b] (2026-10-22T21:09:45Z)
## Log
- 2026-10-22T17:43:46Z created
- 2026-10-22T17:58:22Z set scope=['mods/foreman-ui/tests', 'mods/foreman-ui/tools', 'plugin/lib/fmpage.py', 'plugin/tests/test_ui_replay.py', 'CHANGELOG.md']
- 2026-10-22T20:37:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1534.builder.md
- 2026-10-22T20:38:06Z focused
- 2026-10-22T21:03:15Z set scope=['mods/foreman-ui/tests', 'mods/foreman-ui/tools', 'mods/foreman-ui/README.md', 'plugin/lib/fmpage.py', 'plugin/tests/test_ui_replay.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T21:03:15Z scope: + mods/foreman-ui/README.md and MASTER.md for the review's docs/parity pointer (item 5)
- 2026-10-22T21:09:04Z merged worktree-agent-ae1352ab98d48c0bd (8 file(s))
- 2026-10-22T21:09:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae1352ab98d48c0bd
- 2026-10-22T21:09:09Z focused
- 2026-10-22T21:10:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1543 [FEATURE M, active, 4 steps] Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren
- T-1537 [FEATURE M, active, 4 steps] Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_page.py, plugin/tests/test_shot.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, mods/foreman-ui/README.md, mods/foreman-ui/tests/fixtures/pane-busy.ts, mods/foreman-ui/tests/fixtures/replay.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/t…; re-ground the plan against them before editing
## Why not caught
the first twin run was the first time two mounts were compared
## Lessons
- Determinism checks need the renderer's own counters left out: callback ids rising per mount made identical frames differ
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_ui_replay.py
- mods/foreman-ui/tests/fixtures/pane-busy.json
- mods/foreman-ui/tools/replay.py
- mods/foreman-ui/tests/fixtures/pane-busy.ts
- mods/foreman-ui/tests/fixtures/replay.ts
- mods/foreman-ui/tests/replay.test.tsx
- mods/foreman-ui/tools/pane_replay.py
- mods/foreman-ui/README.md
- MASTER.md
- CHANGELOG.md
