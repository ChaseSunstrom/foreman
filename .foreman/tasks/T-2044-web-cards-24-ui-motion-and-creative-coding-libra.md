---
id: T-2044
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/web]
depends_on: []
source: user
created: 2026-10-29T20:16:23Z
updated: 2026-10-29T20:35:51Z
base: 887073112ad80be42cbab8eec2734759b7ff16a0
base_tree: 4f24226e6e7930aa77586bac0287bec7e44eaf60
plan0_at: 2026-10-29T20:17:27Z
plan0_scope: [plugin/skills/library/cards/web]
verified: strong
---
# Web cards: 24 UI, motion and creative-coding library cards
## Raw request
> Web cards: 24 UI, motion and creative-coding library cards
## Interpretation
User asked for an absolute ton of new skills, especially UI/design (2026-10-29). Libraries the UI and motion work reaches for, detected from package.json.
## Assumptions (confidence)
## Acceptance criteria
- [x] 24 new cards in plugin/skills/library/cards/web (gsap, lenis, rive, lottie, react-spring, anime-js, pixijs, p5js, babylonjs, spline, theatre-js, headless-ui, ark-ui, panda-css, unocss, open-props, daisyui, mantine, floating-ui, embla-carousel, swiper, auto-animate, tweakpane, matter-js) each with dep: detect signals, passing the card lint with no related note — verify with `fm lib check`
- [x] the library tests pass — verify with `python3 plugin/tests/run.py test_library`
## Non-goals
## Approach (options → choice → why)
Complete: each card Verify/Test first/Do/Avoid/Review with concrete numbers and checks, related to existing cards, lint clean. Options: (1) one builder lane per theme in parallel [chosen]; (2) write them all in-session (slow, serial); (3) generate from a template (thin cards).
## Risks and rollback
## Execution prompt
## Steps
1. [x] draft the 24 cards
2. [x] lint and fix
## Resume here
## Docs impact
CHANGELOG (added with T-2039)
## Verification evidence
- (step 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:35:37Z)
- (step 2) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:35:37Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:35:38Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 4.6s (9 classes, 16 at a time; slowest: LibSources 4s, LibraryAdmit 1s, LibrarySearch 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:35:42Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:35:48Z)
- (ac 2) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 5.3s (9 classes, 16 at a time; slowest: LibSources 5s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:35:48Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over the lane; 7 findings fixed by the builder in d2d1b6fb; merged tree re-linted and tested` → 24 web library cards (GSAP to Matter.js), each detected from package.json, with runnable checks [tree 471c2be3ee03] (2026-10-29T20:35:48Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over the lane; 7 findings fixed by the builder in d2d1b6fb; merged tree re-linted and tested` → cards are text read into context; no secrets, no fetch-and-run commands; npx lines name real packages (postcss-cli); held [tree 471c2be3ee03] (2026-10-29T20:35:48Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over the lane; 7 findings fixed by the builder in d2d1b6fb; merged tree re-linted and tested` → wrong API facts (floating-ui arrow order, daisyUI majors, a nonexistent vite flag) and jsdom tests that need layout or WebGL fixed or marked browser-mode [tree 471c2be3ee03] (2026-10-29T20:35:48Z)
## Log
- 2026-10-29T20:16:23Z created
- 2026-10-29T20:16:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2044.builder.md
- 2026-10-29T20:17:26Z focused
- 2026-10-29T20:29:26Z merged worktree-agent-a63d912dabf9085e9 (24 file(s))
- 2026-10-29T20:29:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a63d912dabf9085e9
- 2026-10-29T20:35:36Z focused
- 2026-10-29T20:35:43Z scope: other cards and looks files came from sibling lane merges, closed under their own tasks; T-2044 wrote only cards/web
- 2026-10-29T20:35:51Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2039 [FEATURE M, active, 3 steps] UX cards: 25 product-pattern cards in a new ux area
- T-2043 [FEATURE M, active, 2 steps] Frontend cards: 28 motion, effects and modern-CSS cards
- T-2042 [FEATURE M, active, 2 steps] UX cards: 25 visual-design and brand cards
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
## Lessons
- A library card's test must run where the library works: layout and WebGL need a browser, not jsdom
## Files touched
- plugin/skills/library/cards/web/gsap.md
- plugin/skills/library/cards/web/lenis.md
- plugin/skills/library/cards/web/rive.md
- plugin/skills/library/cards/web/lottie-web.md
- plugin/skills/library/cards/web/react-spring.md
- plugin/skills/library/cards/web/anime-js.md
- plugin/skills/library/cards/web/pixijs.md
- plugin/skills/library/cards/web/p5js.md
- plugin/skills/library/cards/web/babylonjs.md
- plugin/skills/library/cards/web/spline.md
- plugin/skills/library/cards/web/theatre-js.md
- plugin/skills/library/cards/web/headless-ui.md
- plugin/skills/library/cards/web/ark-ui.md
- plugin/skills/library/cards/web/panda-css.md
- plugin/skills/library/cards/web/unocss.md
- plugin/skills/library/cards/web/open-props.md
- plugin/skills/library/cards/web/daisyui.md
- plugin/skills/library/cards/web/mantine.md
- plugin/skills/library/cards/web/floating-ui.md
- plugin/skills/library/cards/web/embla-carousel.md
- plugin/skills/library/cards/web/swiper.md
- plugin/skills/library/cards/web/auto-animate.md
- plugin/skills/library/cards/web/tweakpane.md
- plugin/skills/library/cards/web/matter-js.md
