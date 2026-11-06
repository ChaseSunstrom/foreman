---
id: T-2043
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/frontend]
depends_on: []
source: user
created: 2026-10-29T20:16:23Z
updated: 2026-10-29T20:34:32Z
base: a9854fad723e709fd17f7a0c52b10d43356c3b53
base_tree: a7e3ddfceca3f3841193ce61ca309e1993a10b26
plan0_at: 2026-10-29T20:17:16Z
plan0_scope: [plugin/skills/library/cards/frontend]
verified: strong
---
# Frontend cards: 28 motion, effects and modern-CSS cards
## Raw request
> Frontend cards: 28 motion, effects and modern-CSS cards
## Interpretation
User asked for an absolute ton of new skills, especially UI/design (2026-10-29). Motion, effects and modern CSS, as code.
## Assumptions (confidence)
## Acceptance criteria
- [x] 28 new cards in plugin/skills/library/cards/frontend (scroll-driven-animations, view-transitions, spring-physics, micro-interactions, easing-curves, stagger-choreography, svg-animation, kinetic-typography, scroll-reveal, parallax-depth, progress-indicators, gesture-input, custom-cursors, css-3d-transforms, frosted-glass, gradient-design, grain-and-noise, shadows-and-elevation, clip-paths-and-masks, blend-modes, fluid-typography, variable-fonts, oklch-color, anchor-positioning, popover-api, scroll-snap-carousels, animated-counters, haptic-feedback) each pass the card lint with no related note — verify with `fm lib check`
- [x] the library tests pass — verify with `python3 plugin/tests/run.py test_library`
## Non-goals
## Approach (options → choice → why)
Complete: each card Verify/Test first/Do/Avoid/Review with concrete numbers and checks, related to existing cards, lint clean. Options: (1) one builder lane per theme in parallel [chosen]; (2) write them all in-session (slow, serial); (3) generate from a template (thin cards).
## Risks and rollback
## Execution prompt
## Steps
1. [x] draft the 28 cards
2. [x] lint and fix
## Resume here
## Docs impact
CHANGELOG (added with T-2039)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 5.3s (9 classes, 16 at a time; slowest: LibSources 5s, LibraryAdmit 1s, LibrarySearch 1s) / OK [ran] [tree 6e5231ef853c] (2026-10-29T20:21:56Z)
- (step 2) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:33:40Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:33:41Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 6.5s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:33:48Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:33:56Z)
- (ac 2) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 7.3s (9 classes, 16 at a time; slowest: LibSources 7s, LibraryAdmit 2s, ShaderLooks 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:33:56Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over the lane; 6 findings fixed by the builder in b375b7a9; merged tree re-linted and tested` → 28 frontend cards for motion, effects and modern CSS with support notes and runnable checks [tree 471c2be3ee03] (2026-10-29T20:33:56Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over the lane; 6 findings fixed by the builder in b375b7a9; merged tree re-linted and tested` → cards are text read into context; no secrets, no fetch-and-run commands; npx lines now name real packages; held [tree 471c2be3ee03] (2026-10-29T20:33:56Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over the lane; 6 findings fixed by the builder in b375b7a9; merged tree re-linted and tested` → stale browser-support claims (Safari 26, Firefox 147) and two nonexistent CLIs (npx fonttools, culori) corrected; support lines now say check caniuse [tree 471c2be3ee03] (2026-10-29T20:33:56Z)
## Log
- 2026-10-29T20:16:23Z created
- 2026-10-29T20:16:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2043.builder.md
- 2026-10-29T20:17:15Z focused
- 2026-10-29T20:28:42Z merged worktree-agent-a9c91001c6644144b (28 file(s))
- 2026-10-29T20:29:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9c91001c6644144b
- 2026-10-29T20:33:39Z focused
- 2026-10-29T20:33:48Z scope: other cards and looks files came from sibling lane merges, closed under their own tasks; T-2043 wrote only cards/frontend
- 2026-10-29T20:34:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2039 [FEATURE M, active, 3 steps] UX cards: 25 product-pattern cards in a new ux area
- T-2044 [FEATURE M, planned, 2 steps] Web cards: 24 UI, motion and creative-coding library cards
- T-2042 [FEATURE M, active, 2 steps] UX cards: 25 visual-design and brand cards
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
## Lessons
- Browser-support lines go stale fastest; every support claim names a version and says check caniuse
## Files touched
- plugin/skills/library/cards/frontend/scroll-driven-animations.md
- plugin/skills/library/cards/frontend/view-transitions.md
- plugin/skills/library/cards/frontend/spring-physics.md
- plugin/skills/library/cards/frontend/micro-interactions.md
- plugin/skills/library/cards/frontend/easing-curves.md
- plugin/skills/library/cards/frontend/stagger-choreography.md
- plugin/skills/library/cards/frontend/svg-animation.md
- plugin/skills/library/cards/frontend/kinetic-typography.md
- plugin/skills/library/cards/frontend/scroll-reveal.md
- plugin/skills/library/cards/frontend/parallax-depth.md
- plugin/skills/library/cards/frontend/progress-indicators.md
- plugin/skills/library/cards/frontend/gesture-input.md
- plugin/skills/library/cards/frontend/custom-cursors.md
- plugin/skills/library/cards/frontend/css-3d-transforms.md
- plugin/skills/library/cards/frontend/frosted-glass.md
- plugin/skills/library/cards/frontend/gradient-design.md
- plugin/skills/library/cards/frontend/grain-and-noise.md
- plugin/skills/library/cards/frontend/shadows-and-elevation.md
- plugin/skills/library/cards/frontend/clip-paths-and-masks.md
- plugin/skills/library/cards/frontend/blend-modes.md
- plugin/skills/library/cards/frontend/fluid-typography.md
- plugin/skills/library/cards/frontend/variable-fonts.md
- plugin/skills/library/cards/frontend/oklch-color.md
- plugin/skills/library/cards/frontend/anchor-positioning.md
- plugin/skills/library/cards/frontend/popover-api.md
- plugin/skills/library/cards/frontend/scroll-snap-carousels.md
- plugin/skills/library/cards/frontend/animated-counters.md
- plugin/skills/library/cards/frontend/haptic-feedback.md
- MASTER.md
- README.md
