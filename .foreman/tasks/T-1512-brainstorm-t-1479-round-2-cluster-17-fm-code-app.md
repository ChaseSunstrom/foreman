---
id: T-1512
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, mods/foreman-ui/hooks, mods/foreman-ui/tests, mods/foreman-ui/.claude-plugin/plugin.json, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:42Z
updated: 2026-10-22T20:03:49Z
base: e93bffdaf5e6a6c6dddc083e7f7d315a02b33f09
base_tree: 20d66e81202cc420b416a6ef3aa8b73c11cf2aad
plan0_at: 2026-10-22T19:20:33Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, mods/foreman-ui/hooks, mods/foreman-ui/tests, mods/foreman-ui/.claude-plugin/plugin.json, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 17): fm code app motion and visuals: a hush key cycling
## Raw request
> Brainstorm T-1479 round 2 (cluster 17): fm code app motion and visuals: a hush key cycling motion full/reduced/off, spinner tempo by agent state, a terminal glyph-width probe, a half-block 3D station track, a riso theme, a keymap poster
## Interpretation
Motion and visuals for both surfaces: a hush key that cycles motion full/reduced/off in fm code app and the same cycle as a foreman-ui option, spinner tempo by agent state (thinking, running, waiting), a terminal glyph-width probe at start, a half-block 3D station track in the app, a riso theme for both, and a keymap poster. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] the hush key cycles motion and the pane honours the same option; the riso theme loads in both; the spinner tempo follows state — verify with `cd plugin/tests && python3 -m unittest test_code_tui.MotionVisuals`
## Non-goals
## Approach (options → choice → why)
Options: separate implementations per surface; chosen: shared values in the settings schema (T-1496), the app draws with fmcodetui, the pane reads the same option names.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] hush key and tempo
3. [x] riso theme in both surfaces
4. [x] glyph probe, half-block track, keymap poster
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_code_tui.py -k MotionVisuals` → ✗ exit 1 · Ran 9 tests in 0.7s (1 classes, 16 at a time; slowest: MotionVisuals 1s) / FAILED (1 classes) [ran] [tree 3a902047c801] (2026-10-22T19:27:44Z)
- (step 2) `python3 plugin/tests/run.py -p test_code_tui.py -k hush -k spinner -k Golden` → ✗ exit 1 · Ran 6 tests in 0.6s (3 classes, 16 at a time; slowest: Golden 1s, MotionVisuals 0s, Motion 0s) / FAILED (1 classes) [ran] [tree b3deb3cb55d2] (2026-10-22T19:29:14Z)
- (step 2) `python3 plugin/tests/run.py -p test_code_tui.py -k test_the_hush_key_cycles -k test_a_hush -k spinner -k Golden` → exit 0 · Ran 5 tests in 0.6s (3 classes, 16 at a time; slowest: Golden 1s, MotionVisuals 0s, Motion 0s) / OK [ran] [tree b3deb3cb55d2] (2026-10-22T19:29:21Z)
- (step 3) `python3 plugin/tests/run.py -p test_code_tui.py -k riso` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: MotionVisuals 0s) / OK [ran] [tree f7310846b921] (2026-10-22T19:31:20Z)
- (step 3) `python3 plugin/tests/run.py -p test_settings.py` → exit 0 · Ran 19 tests in 2.0s (5 classes, 16 at a time; slowest: Command 2s, Guard 0s, PreviewApp 0s) / OK [ran] [tree f7310846b921] (2026-10-22T19:31:23Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 130 tests across 2 files. [43.67s] [ran] [tree f7310846b921] (2026-10-22T19:32:10Z)
- (step 4) `python3 plugin/tests/run.py -p test_code_tui.py` → exit 0 · Ran 154 tests in 8.2s (21 classes, 16 at a time; slowest: Command 8s, Fuzz 7s, Events 3s) / OK [ran] [tree 43a8f7817996] (2026-10-22T19:35:56Z)
- `python3 plugin/tests/run.py -p test_code_tui.py -k MotionVisuals` → exit 0 · Ran 9 tests in 0.6s (1 classes, 16 at a time; slowest: MotionVisuals 1s) / OK [ran] [tree 43a8f7817996] (2026-10-22T19:35:57Z)
- (step 4) `python3 plugin/tests/run.py -p test_code_tui.py -k hostile -k MotionVisuals` → exit 0 · Ran 10 tests in 1.1s (2 classes, 16 at a time; slowest: MotionVisuals 1s, Config 0s) / OK [ran] [tree 49d3f2acb2fe] (2026-10-22T19:39:17Z)
- (step 4) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 130 tests across 2 files. [15.47s] [ran] [tree 3239697e7c4a] (2026-10-22T19:51:08Z)
- (step 4) `python3 plugin/tests/run.py -p test_code_tui.py -k MotionVisuals` → exit 0 · Ran 9 tests in 0.5s (1 classes, 16 at a time; slowest: MotionVisuals 0s) / OK [ran] [tree 3239697e7c4a] (2026-10-22T19:51:09Z)
- (step 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 131 tests across 2 files. [12.18s] [ran] [tree 175b02ba7747] (2026-10-22T19:51:51Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.MotionVisuals` → exit 0 · Ran 9 tests in 0.359s / OK [ran] [tree d5b5ea49889f] (2026-10-22T20:02:26Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_settings` → exit 0 · Ran 190 tests in 6.9s (31 classes, 16 at a time; slowest: Command 7s, Fuzz 6s, Events 3s) / OK [ran] [tree d5b5ea49889f] (2026-10-22T20:02:33Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_settings` → exit 0 · Ran 190 tests in 7.1s (31 classes, 16 at a time; slowest: Command 7s, Fuzz 6s, Events 3s) / OK [ran] [tree d5b5ea49889f] (2026-10-22T20:02:41Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui test_settings` → exit 0 · Ran 190 tests in 7.1s (31 classes, 16 at a time; slowest: Command 7s, Fuzz 6s, Events 3s) / OK [ran] [tree d5b5ea49889f] (2026-10-22T20:02:48Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui test_settings` → exit 0 · Ran 190 tests in 7.3s (31 classes, 16 at a time; slowest: Command 7s, Fuzz 6s, Events 3s) / OK [ran] [tree d5b5ea49889f] (2026-10-22T20:02:56Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.MotionVisuals` → exit 0 · Ran 9 tests in 0.371s / OK [ran] [tree 3ad67d061b06] (2026-10-22T20:03:18Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 1 MEDIUM (riso accent2) + 4 LOW fixed in 323d96aa; pane tests 131 pass` → hush key, spinner tempo by state, riso on both surfaces, glyph probe with a half-block rail, keys poster [tree 3ad67d061b06] (2026-10-22T20:03:18Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 1 MEDIUM (riso accent2) + 4 LOW fixed in 323d96aa; pane tests 131 pass` → the probe writes only when both ends are a terminal and is bounded to 0.25 s; the hush write goes through set_key (guard + lock); load_config messages escape control characters [tree 3ad67d061b06] (2026-10-22T20:03:18Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 1 MEDIUM (riso accent2) + 4 LOW fixed in 323d96aa; pane tests 131 pass` → z doesn't fire while typing or on the settings list; a hush closes the poster; riso dim meets 4.5:1 on bar and paper [tree 3ad67d061b06] (2026-10-22T20:03:18Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 1 MEDIUM (riso accent2) + 4 LOW fixed in 323d96aa; pane tests 131 pass` → MotionVisuals red first; only the 3.4 s golden frame changed, by its spinner glyph [tree 3ad67d061b06] (2026-10-22T20:03:18Z)
## Log
- 2026-10-22T17:36:42Z created
- 2026-10-22T17:46:48Z steer (T-1520): plugin parity: the hush key, state tempo, riso theme and 3D track also reach the foreman-ui band and pane (a motion cycle option, a palette), not only fm code app
- 2026-10-22T17:55:51Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcodeterm.py', 'mods/foreman-ui/hooks', 'mods/foreman-ui/tests', 'mods/foreman-ui/.claude-plugin/plugin.json', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-22T19:20:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1512.builder.md
- 2026-10-22T19:20:33Z focused
- 2026-10-22T19:29:54Z scope: plugin/lib/fmsettings.py and plugin/tests/test_settings.py: the shared palette value set gains riso (SHARED is the one schema both surfaces read)
- 2026-10-22T19:36:57Z scope: README.md and MASTER.md: the hush key, riso theme and palette, tempo, rail and poster in the docs
- 2026-10-22T19:49:32Z steer: review nits: riso accent2 in the pane, riso dim #655D4E, z closes the keys poster, SPIN spacing, pane type/lane colours follow the palette, foreman-ui 0.18.4 (plugin.json + marketplace.json); README hush/riso text moved to its own bullet so it merges cleanly with foreman/build
- 2026-10-22T19:53:25Z merged worktree-agent-aea3ccbba2b1b0057 (14 file(s))
- 2026-10-22T19:53:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aea3ccbba2b1b0057
- 2026-10-22T20:02:25Z focused
- 2026-10-22T20:03:17Z scope: fmsettings.py (riso palette), test_settings.py (unbound-key example), README.md, MASTER.md, golden frame demo-03.4s, mod version bump; other files from other tasks' merges
- 2026-10-22T20:03:47Z done
- 2026-10-22T20:03:49Z committed cf3af358 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261022-grounding-c: 1. **Answer
- research brainstorm-20261020-tui: Method.** I read all of ideas.md (about 560 distinct titles; near-duplicates are merged with "/"). I grepped fmcodetui.py and fmcode.py…
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, …; re-ground the plan against them before editing
## Why not caught
the riso pane palette changed three of four accents
## Lessons
- Contrast ratio alone can't tell two accents apart (blue and sunflower are 1.44:1 yet look nothing alike): test palette roles by colour distance
## Plan gaps
- failed first: step 1 failing tests
- failed first: step 2 hush key and tempo
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/lib/fmsettings.py
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_settings.py
- plugin/lib/fmcodeterm.py
- README.md
- MASTER.md
- .claude-plugin/marketplace.json
- CHANGELOG.md
