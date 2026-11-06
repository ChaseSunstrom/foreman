---
id: T-1515
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/terminal-ui.md, plugin/skills/playbooks/references/ui/INDEX.md, plugin/skills/playbooks/ratchet.json, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:43Z
updated: 2026-10-23T08:38:16Z
base: 935e6b494b97266d07bb240a01e79ada76b9c062
base_tree: 797cbef827b1ce88b633c89d34d29d1a0d2d2b90
plan0_at: 2026-10-23T08:36:28Z
plan0_scope: [plugin/skills/playbooks/references/ui/terminal-ui.md, plugin/skills/playbooks/references/ui/INDEX.md, plugin/skills/playbooks/references/INDEX.md, CHANGELOG.md]
verified: strong
---
# Expand the terminal UI playbook: display width and wide glyphs, resize, bracketed paste, the motion budget, terminal lifecycle and CLI product design
## Raw request
> Brainstorm T-1479 round 2 (cluster 20): expand ui/terminal-ui.md: display width and wide glyphs, resize, bracketed paste, motion budget, CLI product design
## Interpretation
Expand ui/terminal-ui.md: display width and wide glyphs (measure columns, never len), resize handling, bracketed paste, a motion budget and frame clock, colour roles across dark and light terminals, and CLI product design (help text, errors that say how to fix, progressive disclosure), for both fm code app and Claude Code mods. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/terminal-ui.md has sections on display width and wide glyphs, resize, bracketed paste, a motion budget, the terminal's lifecycle and CLI product design, each rule a reviewer can mark pass or fail, and the playbook tests pass — verify with `python3 plugin/tests/run.py test_docs test_playbook_evals`
## Non-goals
## Approach (options → choice → why)
Options: a new file; chosen: extend the existing playbook, keeping its numbered rules.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the sections (Foreman's own fmcodeterm and fmcodetui as the worked examples)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs test_playbook_evals test_playbook_check test_playbook_machinery` → exit 0 · Ran 136 tests in 8.6s (32 classes, 16 at a time; slowest: Fences 8s, Load 4s, Snippets 2s) / OK [ran] [tree 65cd17caac89] (2026-10-23T08:38:03Z)
- (audit intent) `self` → pass: every topic named in the request has its own section of pass/fail rules; facts checked against fmcodeterm (ENTER/LEAVE sequences, SIGWINCH wake pipe, colour_depth, title push/pop) [tree 65cd17caac89] (2026-10-23T08:38:04Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_playbook_evals` → exit 0 · Ran 81 tests in 8.6s (19 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 65cd17caac89] (2026-10-23T08:38:13Z)
- (audit intent) `self: intent` → all six topics covered; examples point at code that exists [tree 65cd17caac89] (2026-10-23T08:38:13Z)
- (audit self) `self: intent` → no findings [tree 65cd17caac89] (2026-10-23T08:38:13Z)
## Log
- 2026-10-22T17:36:43Z created
- 2026-10-22T17:56:02Z set scope=['plugin/skills/playbooks/references/ui/terminal-ui.md', 'CHANGELOG.md']
- 2026-10-23T08:36:26Z planned from capture
- 2026-10-23T08:36:26Z set scope=['plugin/skills/playbooks/references/ui/terminal-ui.md', 'plugin/skills/playbooks/references/ui/INDEX.md', 'plugin/skills/playbooks/references/INDEX.md', 'CHANGELOG.md']
- 2026-10-23T08:36:27Z focused
- 2026-10-23T08:37:54Z scope: plugin/skills/playbooks/ratchet.json — the size ratchet records terminal-ui's growth (and scene-3d's and verification-loop's small earlier growth within slack)
- 2026-10-23T08:37:54Z set scope=['plugin/skills/playbooks/references/ui/terminal-ui.md', 'plugin/skills/playbooks/references/ui/INDEX.md', 'plugin/skills/playbooks/ratchet.json', 'CHANGELOG.md']
- 2026-10-23T08:38:14Z done
- 2026-10-23T08:38:16Z committed 6116bdb2 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook UI playbooks (fm playbooks show ui/INDEX)
- T-1512 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 17): fm code app motion and visuals: a hush key cycling — lesson: Contrast ratio alone can't tell tw…
- T-1507 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 12): design tokens: a design-extract skill that derives — lesson: A parser that re-scans the parent …
- decision 2026-10-22: Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or…
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–4 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/skills/playbooks/references/ui/INDEX.md; re-ground the plan against them before editing
## Lessons
- A playbook rule earns its place when a reviewer can mark it pass or fail
## Files touched
- plugin/skills/playbooks/references/ui/terminal-ui.md
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/skills/playbooks/ratchet.json
- CHANGELOG.md
