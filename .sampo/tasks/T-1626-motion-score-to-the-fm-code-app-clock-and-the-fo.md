---
id: T-1626
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmmotion.py, plugin/lib/fmcli.py, plugin/tests/test_motion_score.py, plugin/tests/test_code_tui.py, plugin/skills/playbooks/references/ui/motion.md, CHANGELOG.md, MASTER.md, plugin/skills/ui-design/SKILL.md]
depends_on: []
source: followup
created: 2026-10-22T20:57:15Z
updated: 2026-10-28T17:25:13Z
base: b4caa04f44b2f7aef642f7b128f518bb5be51fd7
base_tree: 552ba8122bd0ecf0963d4a00b9b39cd5634b62a4
plan0_at: 2026-10-28T17:13:08Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmmotion.py, plugin/tests/test_motion.py, plugin/tests/test_codetui.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/motion.md]
verified: strong
---
# fm code's motion clock reads the project's Motion Score; fm motion compile --to lab: a page to play, scrub and edit each motion
## Raw request
> Motion Score to the fm code app clock and the foreman-ui pane option set, a motion lab page and drag-to-edit player (from T-1526; waits: after fm motion compile; only where the surfaces already have timing knobs)
## Interpretation
Where a surface already has a timing knob, the project's Motion Score sets it: fm code's eased values (bars, counts, columns, deck ring) take their seconds from motions named fm-code-*. A lab page (a fourth compile target) plays each motion, scrubs it by dragging, and edits duration and bezier handles into a score line to paste back. The foreman-ui pane is left out: its timers (FLASH_MS, CLOSING_MS, FRAME_MS) are feed and settle cadences in a TS mod that would need its own TOML read; recorded as a decision.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code eases bars, counts, columns and the deck ring over the durations motion.toml gives fm-code-bars/-counts/-columns/-deck, and keeps its own without one — verify with `python3 plugin/tests/run.py Motion`
- [x] fm motion compile --to lab writes one self-contained page: each motion plays, scrubs by drag, and its duration and bezier handles edit into a score line to paste back; node parses its script — verify with `python3 plugin/tests/run.py Lab`
## Non-goals
## Approach (options → choice → why)
Complete: (1) fm code durations from the score, (2) the pane's timings, (3) a lab page, (4) a drag-to-edit player. Options: A fm code reads motion.toml via fmmotion.check, by key family → named motion; B a Foreman-owned score for its own surfaces; C per-motion tui.toml keys through fm settings; D lab as compile --to lab, reusing check/compile and --out; E a separate fm motion lab verb serving a page. Choice: A + D (one existing reader, one existing writer path; no new verb, no server). Durations only: the clock's knob is dur, the curve stays ease_out. 0 ms clamps to 1 ms (no divide by zero).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: fm code takes durations from motion.toml (red)
2. [x] fm code: score_durations + Motion.eased uses them
3. [x] test: --to lab page (red)
4. [x] fmmotion: lab target
5. [x] docs: motion.md, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-28T17:17:50Z step 1/5: test: fm code takes durations from motion.toml (red)
- git: foreman/build; 7 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmmotion.py, plugin/skills/playbooks/references/ui/motion.md, plugin/tests/test_code_tui.py, plugin/tests/test_motion_score.py
- touched since last checkpoint: plugin/tests/test_code_tui.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_motion_score.py, CHANGELOG.md, plugin/lib/fmmotion.py, plugin/skills/playbooks/references/ui/motion.md
- failures met: playwright
## Docs impact
plugin/skills/playbooks/references/ui/motion.md, plugin/skills/ui-design/SKILL.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Motion` → ✗ exit 1 · Ran 36 tests in 0.8s (3 classes, 16 at a time; slowest: MotionVisuals 1s, Motion 0s, Motion 0s) / FAILED (1 classes) [ran] [tree d40612eb8e40] (2026-10-28T17:14:42Z)
- (step 3) `python3 plugin/tests/run.py Lab` → ✗ exit 1 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Lab 0s) / FAILED (1 classes) [ran] [tree d40612eb8e40] (2026-10-28T17:14:43Z)
- (step 2) `python3 plugin/tests/run.py Motion` → exit 0 · Ran 36 tests in 0.8s (3 classes, 16 at a time; slowest: MotionVisuals 1s, Motion 0s, Motion 0s) / OK [ran] [tree def819c5360c] (2026-10-28T17:15:00Z)
- (step 4) `python3 plugin/tests/run.py Lab Compile` → exit 0 · Ran 19 tests in 1.9s (3 classes, 16 at a time; slowest: SteerCompile 2s, Compile 1s, Lab 0s) / OK [ran] [tree c0f5e5bd8794] (2026-10-28T17:17:16Z)
- (step 5) `grep -c 'compile --to lab' plugin/skills/playbooks/references/ui/motion.md CHANGELOG.md` → exit 0 · plugin/skills/playbooks/references/ui/motion.md:1 / CHANGELOG.md:1 [ran] [tree 4d11f27d1976] (2026-10-28T17:17:25Z)
- (ac 1) `python3 plugin/tests/run.py Motion` → exit 0 · Ran 36 tests in 0.8s (3 classes, 16 at a time; slowest: MotionVisuals 1s, Motion 0s, Motion 0s) / OK [ran] [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (ac 2) `python3 plugin/tests/run.py Lab` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: Lab 0s) / OK [ran] [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (step 3) `python3 plugin/tests/run.py Lab` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: Lab 0s) / OK [ran] [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit intent) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → met; the foreman-ui pane has no duration knob, so it keeps its own timers (CHANGELOG says so) [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit adversary) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → ok; JSON escapes </, title html-escaped, placeholders can't inject into each other [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit edge) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → ok; unreadable score ignored, 0 ms is 1 ms, score read once at start [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit design) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → fixed handle target size, roles, aspect, scrub follow, none feedback [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit maintainer) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → fixed bar/col coverage; browser behaviour checked headless, not in the suite [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit operator) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → fixed stale --to lists [tree daf0a4fc8e67] (2026-10-28T17:24:12Z)
- (audit intent) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → met; the foreman-ui pane has no duration knob, so it keeps its own timers (CHANGELOG says so) [tree daf0a4fc8e67] (2026-10-28T17:24:44Z)
- (audit adversary) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → ok; JSON escapes </, title html-escaped, placeholders can't inject into each other [tree daf0a4fc8e67] (2026-10-28T17:24:44Z)
- (audit edge) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → ok; unreadable score ignored, 0 ms is 1 ms, score read once at start [tree daf0a4fc8e67] (2026-10-28T17:24:44Z)
- (audit design) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → fixed handle target size, roles, aspect, scrub follow, none feedback [tree daf0a4fc8e67] (2026-10-28T17:24:44Z)
- (audit maintainer) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → fixed bar/col coverage; browser behaviour checked headless, not in the suite [tree daf0a4fc8e67] (2026-10-28T17:24:44Z)
- (audit operator) `one fm-reviewer pass (design, maintainer, operator, intent, adversary, edge) over the diff; 6 findings fixed: 28 px handle targets with slider role and value text, unsquashed curve box, scrub follows playback, Play disabled for reduced none, bar/col families tested, lab listed in help, skill and MASTER; page re-checked headless (drag, keys, duration, scrub, no errors)` → fixed stale --to lists [tree daf0a4fc8e67] (2026-10-28T17:24:44Z)
## Log
- 2026-10-22T20:57:15Z created
- 2026-10-28T17:12:46Z planned from capture
- 2026-10-28T17:13:07Z focused
- 2026-10-28T17:14:20Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/motion.md']
- 2026-10-28T17:14:20Z scope: the test files are test_motion_score.py and test_code_tui.py (guessed names were wrong); fmcli.py holds the --to choices
- 2026-10-28T17:17:29Z criterion 1 verify: `python3 plugin/tests/run.py Score` → `python3 plugin/tests/run.py Motion`
- 2026-10-28T17:20:00Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'plugin/tests/test_code_tui.py', 'plugin/skills/playbooks/references/ui/motion.md', 'CHANGELOG.md', 'MASTER.md', 'plugin/skills/ui-design/SKILL.md']
- 2026-10-28T17:20:00Z scope: MASTER.md and ui-design SKILL.md listed --to without lab (review, operator lens)
- 2026-10-28T17:25:11Z done
- 2026-10-28T17:25:13Z committed 13397289 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1526 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Motion Score: one file of named motions that compiles to CSS, WAAPI, thr
- playbook Motion: choreography, timing and reduced motion (fm playbooks show ui/motion)
- T-1515 [FEATURE S, done, 1 steps] Expand the terminal UI playbook: display width and wide glyphs, resize, bracketed paste, the motion budget, terminal lifecycle and CLI …
- decision 2026-10-23: T-1670: left out the recorded-time clock, the fm page timeline and forked-skill QA
- the similar finished task took 1 steps
- start here (files T-1515 touched): plugin/skills/playbooks/references/ui/terminal-ui.md, plugin/skills/playbooks/references/ui/INDEX.md, plugin/skills/playbooks/ratchet.json, CHANGELOG.md
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/lib/fmmotion.py, plugin/skills/playbooks/references/ui/motion.md; re-ground the plan against them before editing
## Lessons
- An SVG handle drawn in viewBox units needs a separate invisible hit circle: the visible dot alone is a 6 px target
## Plan gaps
- failed first: step 1 test: fm code takes durations from motion.toml (red)
- failed first: step 3 test: --to lab page (red)
## Files touched
- plugin/tests/test_code_tui.py
- plugin/tests/test_motion_score.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- plugin/lib/fmmotion.py
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/motion.md
- MASTER.md
- plugin/skills/ui-design/SKILL.md
