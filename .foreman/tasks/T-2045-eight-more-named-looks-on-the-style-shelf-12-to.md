---
id: T-2045
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/looks]
depends_on: []
source: user
created: 2026-10-29T20:16:23Z
updated: 2026-10-29T20:38:10Z
base: 4fd55b31412b17eea84d33b2abc309dc8454fbd1
base_tree: 43fc57e7226efd09dc28841afc0ed1ff4e8bc5b0
plan0_at: 2026-10-29T20:19:51Z
plan0_scope: [plugin/skills/library/cards/looks]
verified: strong
---
# Eight more named looks on the style shelf (12 to 20)
## Raw request
> Eight more named looks on the style shelf (12 to 20)
## Interpretation
User asked for an absolute ton of new skills, especially UI/design (2026-10-29). The style shelf is twelve looks; more distinct looks give fm directions and ui-design more to offer.
## Assumptions (confidence)
## Acceptance criteria
- [x] 8 new look-* cards with every field, measured palettes meeting their contrast floors, no status-hue or indigo accents, none repeating the direction bank; the shelf tests expect 20 — verify with `python3 plugin/tests/run.py test_library`
- [x] every mention of twelve looks (README, fmcodetui, docs) says twenty — verify with `fm lib check`
## Non-goals
## Approach (options → choice → why)
Complete: each card Verify/Test first/Do/Avoid/Review with concrete numbers and checks, related to existing cards, lint clean. Options: (1) one builder lane per theme in parallel [chosen]; (2) write them all in-session (slow, serial); (3) generate from a template (thin cards).
## Risks and rollback
## Execution prompt
## Steps
1. [x] pick 8 looks outside the bank
2. [x] write the cards with measured palettes
3. [x] update counts and tests
## Resume here
## Docs impact
plugin/skills/playbooks/references/ui/design-direction.md says twenty and names them; CHANGELOG (added with T-2039)
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 6.0s (9 classes, 16 at a time; slowest: LibSources 5s, LibraryAdmit 1s, LibrarySearch 1s) / OK [ran] [tree b2f8dc2a9514] (2026-10-29T20:20:40Z)
- (step 2) `fm lib check` → exit 0 · 1109 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree b2f8dc2a9514] (2026-10-29T20:20:43Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_tui test_library test_settings test_settings_power test_statusline_ui test_taste test_taste_ledger` → exit 0 · Ran 602 tests in 34.3s (139 classes, 16 at a time; slowest: TaskLifecycle 34s, CaptureAndIntake 22s, Command 21s) / OK [ran] [tree b2f8dc2a9514] (2026-10-29T20:21:18Z)
- (step 1) `python3 plugin/tests/run.py test_taste_ledger 2>&1 | tail -12` → exit 0 · Ran 17 tests in 0.9s (6 classes, 16 at a time; slowest: Ledger 1s, Divergence 1s, Calibration 0s) / OK [ran] [tree 11a56a56e66e] (2026-10-29T20:26:23Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_tui test_library test_looks_gallery test_settings test_settings_power test_statusline_ui test_taste test_taste_ledger` → exit 0 · Ran 617 tests in 20.5s (142 classes, 16 at a time; slowest: TaskLifecycle 20s, Command 9s, Fuzz 9s) / OK [ran] [tree b226b9e0d304] (2026-10-29T20:28:03Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library test_looks_gallery test_taste test_taste_ledger` → exit 0 · Ran 92 tests in 4.9s (25 classes, 16 at a time; slowest: LibSources 5s, Roll 2s, CorrectionClusters 2s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:36:14Z)
- (ac 2) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:36:14Z)
- (ac 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 5.2s (9 classes, 16 at a time; slowest: LibSources 5s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:37:17Z)
- (ac 2) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:37:17Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → eight more looks, twenty in all, each with a measured palette and a working specimen; calibration shows every look [tree 471c2be3ee03] (2026-10-29T20:37:17Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → looks are card text plus a static gallery that loads nothing from another host (fm page looks says so); the ux cards named are T-2039's, audited there; held [tree 471c2be3ee03] (2026-10-29T20:37:17Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → n=20 and n=24 pairs show every look with no repeated rival (new test); palettes re-measured with the test's own ratio and hue checks [tree 471c2be3ee03] (2026-10-29T20:37:17Z)
- (audit design) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → the eight specimens render as distinct, coherent interfaces; no broken layout at 1440 [tree 471c2be3ee03] (2026-10-29T20:37:17Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → eight more looks, twenty in all, each with a measured palette and a working specimen; calibration shows every look [tree 471c2be3ee03] (2026-10-29T20:37:47Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → looks are card text plus a static gallery that loads nothing from another host (fm page looks says so); the ux cards named are T-2039's, audited there; held [tree 471c2be3ee03] (2026-10-29T20:37:47Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → n=20 and n=24 pairs show every look with no repeated rival (new test); palettes re-measured with the test's own ratio and hue checks [tree 471c2be3ee03] (2026-10-29T20:37:47Z)
- (audit design) `one fm-reviewer pass (adversary/edge) over the lane; 4 findings (missing gallery specimens, stale twelve, palette collisions, pairs filter) fixed in 9c8a92b4; the eight specimens rendered from fm page looks and checked by eye` → the eight specimens render as distinct, coherent interfaces; no broken layout at 1440 [tree 471c2be3ee03] (2026-10-29T20:37:47Z)
## Log
- 2026-10-29T20:16:23Z created
- 2026-10-29T20:16:40Z criterion 1 verify: `python3 plugin/tests/run.py test_library test_look_contrast` → `python3 plugin/tests/run.py test_library`
- 2026-10-29T20:16:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2045.builder.md
- 2026-10-29T20:19:50Z focused
- 2026-10-29T20:29:14Z merged worktree-agent-a92dc34d9a13bbed6 (21 file(s))
- 2026-10-29T20:29:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a92dc34d9a13bbed6
- 2026-10-29T20:36:08Z focused
- 2026-10-29T20:37:03Z scope: the cards/ux, frontend and web files came from sibling lane merges, closed under their own tasks
- 2026-10-29T20:38:10Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2039 [FEATURE M, active, 3 steps] UX cards: 25 product-pattern cards in a new ux area
- T-1498 [FEATURE M, done, 2 steps] Style shelf: twelve original named looks as library cards — lesson: Name taste cards with a prefix (look-) so a single everyday word in…
- T-2042 [FEATURE M, active, 2 steps] UX cards: 25 visual-design and brand cards
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- the similar finished task took 2 steps
## Lessons
- A look's accent rule (30° from status hues) rules out the obvious brand colour for some themes; pick the theme's second colour rather than bending the rule
## Files touched
- plugin/lib/fmtaste.py
- plugin/tests/test_taste_ledger.py
- plugin/tests/test_library.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- plugin/commands/looks.md
- plugin/skills/directions/SKILL.md
- plugin/skills/ui-design/SKILL.md
- README.md
- MASTER.md
- plugin/skills/library/cards/looks/look-cinema-lobby.md
- plugin/skills/library/cards/looks/look-darkroom.md
- plugin/skills/library/cards/looks/look-glacier.md
- plugin/skills/library/cards/looks/look-letterpress.md
- plugin/skills/library/cards/looks/look-pit-stop.md
- plugin/skills/playbooks/references/ui/design-direction.md
- plugin/lib/looks.html
- plugin/tests/test_looks_gallery.py
- mods/foreman-ui/tools/pane_replay.py
- plugin/lib/fmcore.py
- plugin/lib/fmscene.py
- plugin/skills/library/cards/frontend/anchor-positioning.md
- plugin/skills/library/cards/frontend/animated-counters.md
- plugin/skills/library/cards/frontend/blend-modes.md
- plugin/skills/library/cards/frontend/clip-paths-and-masks.md
- plugin/skills/library/cards/frontend/css-3d-transforms.md
- plugin/skills/library/cards/frontend/custom-cursors.md
- plugin/skills/library/cards/frontend/easing-curves.md
- plugin/skills/library/cards/frontend/fluid-typography.md
- plugin/skills/library/cards/frontend/frosted-glass.md
