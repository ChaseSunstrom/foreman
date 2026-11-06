---
id: T-2042
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/ux]
depends_on: []
source: user
created: 2026-10-29T20:16:22Z
updated: 2026-10-29T20:32:50Z
base: 6002ef58cbced061d1c8503cd897f461ca467428
base_tree: 33e3ff95bf6726582b8cac793bb5c115806d36f7
plan0_at: 2026-10-29T20:17:08Z
plan0_scope: [plugin/skills/library/cards/ux]
verified: strong
---
# UX cards: 25 visual-design and brand cards
## Raw request
> UX cards: 25 visual-design and brand cards
## Interpretation
User asked for an absolute ton of new skills, especially UI/design (2026-10-29). Visual design fundamentals and brand.
## Assumptions (confidence)
## Acceptance criteria
- [x] 25 new cards in plugin/skills/library/cards/ux (visual-hierarchy, grid-systems, spacing-scales, type-pairing, type-scales, color-palettes, design-tokens, icon-design, logo-design, brand-identity, illustration-systems, image-direction, chart-design, landing-pages, hero-sections, calls-to-action, social-proof, bento-grids, gestalt-principles, ui-polish, design-handoff, art-direction, app-icons-and-favicons, social-share-images, email-design) each pass the card lint with no related note — verify with `fm lib check`
- [x] the library tests pass — verify with `python3 plugin/tests/run.py test_library`
## Non-goals
## Approach (options → choice → why)
Complete: each card Verify/Test first/Do/Avoid/Review with concrete numbers and checks, related to existing cards, lint clean. Options: (1) one builder lane per theme in parallel [chosen]; (2) write them all in-session (slow, serial); (3) generate from a template (thin cards).
## Risks and rollback
## Execution prompt
## Steps
1. [x] draft the 25 cards
2. [x] lint and fix
## Resume here
## Docs impact
CHANGELOG (added with T-2039)
## Verification evidence
- (step 1) `fm lib check` → exit 0 · 1109 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree ba7d63137fb1] (2026-10-29T20:21:21Z)
- (step 2) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 5.2s (9 classes, 16 at a time; slowest: LibSources 5s, LibraryAdmit 1s, LibrarySearch 1s) / OK [ran] [tree ba7d63137fb1] (2026-10-29T20:21:27Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:32:19Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 6.4s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibrarySuggest 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:32:25Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:32:34Z)
- (ac 2) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 7.7s (9 classes, 16 at a time; slowest: LibSources 7s, LibraryAdmit 3s, LibrarySearch 1s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:32:34Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over the lane; 8 findings fixed by the builder in 0a0d053c; merged tree re-linted and tested` → 25 visual-design cards (hierarchy, grids, type, palettes, tokens, brand, charts, landing pages) with runnable checks [tree 471c2be3ee03] (2026-10-29T20:32:34Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over the lane; 8 findings fixed by the builder in 0a0d053c; merged tree re-linted and tested` → cards are text read into context; no secrets, no fetch-and-run commands; Verify lines now name only real tools (axe, stylelint --config, jq); held [tree 471c2be3ee03] (2026-10-29T20:32:34Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over the lane; 8 findings fixed by the builder in 0a0d053c; merged tree re-linted and tested` → scripts no repo ships and a palette test that checked constants were replaced by token-file reads and AxeBuilder; type-scale numbers corrected [tree 471c2be3ee03] (2026-10-29T20:32:34Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over the lane; 8 findings fixed by the builder in 0a0d053c; merged tree re-linted and tested` → 25 visual-design cards (hierarchy, grids, type, palettes, tokens, brand, charts, landing pages) with runnable checks [tree 471c2be3ee03] (2026-10-29T20:32:46Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over the lane; 8 findings fixed by the builder in 0a0d053c; merged tree re-linted and tested` → cards are text read into context; no secrets, no fetch-and-run commands; Verify lines now name only real tools (axe, stylelint --config, jq); held [tree 471c2be3ee03] (2026-10-29T20:32:46Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over the lane; 8 findings fixed by the builder in 0a0d053c; merged tree re-linted and tested` → scripts no repo ships and a palette test that checked constants were replaced by token-file reads and AxeBuilder; type-scale numbers corrected [tree 471c2be3ee03] (2026-10-29T20:32:46Z)
## Log
- 2026-10-29T20:16:22Z created
- 2026-10-29T20:16:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2042.builder.md
- 2026-10-29T20:17:08Z focused
- 2026-10-29T20:29:20Z merged worktree-agent-a0d5d596ead849745 (25 file(s))
- 2026-10-29T20:29:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0d5d596ead849745
- 2026-10-29T20:32:10Z focused
- 2026-10-29T20:32:46Z scope: the web/frontend cards and looks files came from the T-2043/T-2044/T-2045 lane merges, closed under their own tasks; T-2042 wrote only cards/ux
- 2026-10-29T20:32:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2039 [FEATURE M, active, 3 steps] UX cards: 25 product-pattern cards in a new ux area
- T-2044 [FEATURE M, planned, 2 steps] Web cards: 24 UI, motion and creative-coding library cards
- T-2043 [FEATURE M, planned, 2 steps] Frontend cards: 28 motion, effects and modern-CSS cards
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
## Lessons
- A card's test should read the repo's own tokens; a test over hard-coded constants checks arithmetic, not the project
## Files touched
- plugin/skills/library/cards/ux/visual-hierarchy.md
- plugin/skills/library/cards/ux/grid-systems.md
- plugin/skills/library/cards/ux/spacing-scales.md
- plugin/skills/library/cards/ux/type-pairing.md
- plugin/skills/library/cards/ux/type-scales.md
- plugin/skills/library/cards/ux/color-palettes.md
- plugin/skills/library/cards/ux/design-tokens.md
- plugin/skills/library/cards/ux/icon-design.md
- plugin/skills/library/cards/ux/logo-design.md
- plugin/skills/library/cards/ux/brand-identity.md
- plugin/skills/library/cards/ux/illustration-systems.md
- plugin/skills/library/cards/ux/image-direction.md
- plugin/skills/library/cards/ux/chart-design.md
- plugin/skills/library/cards/ux/landing-pages.md
- plugin/skills/library/cards/ux/hero-sections.md
- plugin/skills/library/cards/ux/calls-to-action.md
- plugin/skills/library/cards/ux/social-proof.md
- plugin/skills/library/cards/ux/bento-grids.md
- plugin/skills/library/cards/ux/gestalt-principles.md
- plugin/skills/library/cards/ux/ui-polish.md
- plugin/skills/library/cards/ux/design-handoff.md
- plugin/skills/library/cards/ux/art-direction.md
- plugin/skills/library/cards/ux/app-icons-and-favicons.md
- plugin/skills/library/cards/ux/social-share-images.md
- plugin/skills/library/cards/ux/email-design.md
- plugin/skills/library/cards/web/anime-js.md
- plugin/skills/library/cards/web/ark-ui.md
- plugin/skills/library/cards/web/auto-animate.md
- plugin/skills/library/cards/web/babylonjs.md
- plugin/skills/library/cards/web/daisyui.md
