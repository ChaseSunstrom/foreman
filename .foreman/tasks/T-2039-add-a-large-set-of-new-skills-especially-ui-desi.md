---
id: T-2039
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/ux, README.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-29T20:08:56Z
updated: 2026-10-29T20:31:12Z
base: c2d6f013659ed2e6d8441ed02d1b292712cae44d
base_tree: ba095ce5d1a7076a3457ba2c8b462f1b6c9a21f9
plan0_at: 2026-10-29T20:17:03Z
plan0_scope: [plugin/skills/library/cards/ux]
verified: strong
---
# UX cards: 25 product-pattern cards in a new ux area
## Raw request
> FEATURE: add a large set of new skills, especially UI/design (the user: 'an absolute metric fuck ton of skills, especially UI/design/etc.')
## Interpretation
User asked for an absolute ton of new skills, especially UI/design. Product UX patterns have no home: frontend covers code, design covers architecture. A new ux area holds them.
## Assumptions (confidence)
## Acceptance criteria
- [x] 25 new cards in plugin/skills/library/cards/ux (onboarding-flows, empty-states, navigation-patterns, ux-writing, error-messages, search-ux, filters-and-facets, command-palette, settings-pages, pricing-pages, checkout-flows, sign-up-flows, notification-design, dashboard-design, progressive-disclosure, multi-step-wizards, undo-patterns, destructive-actions, mobile-navigation, tooltips-and-coachmarks, feedback-collection, permission-prompts, information-architecture, usability-testing, dark-patterns) each pass the card lint with no related note — verify with `fm lib check`
- [x] the library tests pass with the new area — verify with `python3 plugin/tests/run.py test_library test_docs`
## Non-goals
## Approach (options → choice → why)
Complete: 25 cards, each Verify/Test first/Do/Avoid/Review, concrete numbers and checks, related to existing cards. Options: (1) new ux area [chosen: fits fm lib list --area]; (2) put them in frontend (mixes code and product design); (3) playbooks instead (heavier, fewer topics). Rest captured as later lanes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] draft the 25 cards from the frontend card format
2. [x] lint and fix
3. [x] README areas line names the ux area
## Resume here
## Docs impact
README areas line; CHANGELOG
## Verification evidence
- (step 1) `fm lib check` → exit 0 · 1109 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 2ead27ab5507] (2026-10-29T20:21:01Z)
- (step 2) `python3 plugin/tests/run.py test_library test_docs` → exit 0 · Ran 117 tests in 9.7s (27 classes, 16 at a time; slowest: Fences 9s, LibSources 8s, LibraryAdmit 4s) / OK [ran] [tree 2ead27ab5507] (2026-10-29T20:21:11Z)
- (step 3) `grep -c 'UX patterns and visual design' README.md` → exit 0 · 1 [ran] [tree ce7660ada4da] (2026-10-29T20:30:05Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree ce7660ada4da] (2026-10-29T20:30:05Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_library test_docs` → exit 0 · Ran 117 tests in 7.9s (27 classes, 16 at a time; slowest: Fences 8s, LibSources 4s, LibraryAdmit 1s) / OK [ran] [tree ce7660ada4da] (2026-10-29T20:30:13Z)
- (ac 1) `fm lib check` → exit 0 · 1219 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 471c2be3ee03] (2026-10-29T20:30:47Z)
- (ac 2) `python3 plugin/tests/run.py test_library test_docs` → exit 0 · Ran 117 tests in 8.4s (27 classes, 16 at a time; slowest: Fences 8s, LibSources 5s, LibraryAdmit 2s) / OK [ran] [tree 471c2be3ee03] (2026-10-29T20:30:47Z)
- (audit intent) `one fm-reviewer pass (adversary/edge) over all four card lanes; 5 findings fixed by the builder in 9295cee1; merged tree re-linted and tested` → 25 product-pattern cards in a new ux area, each with runnable Verify lines; README names the area [tree 471c2be3ee03] (2026-10-29T20:30:47Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge) over all four card lanes; 5 findings fixed by the builder in 9295cee1; merged tree re-linted and tested` → cards are text read into context; checked permission-prompts and design-tokens carry no secrets, no commands that fetch and run remote code, and the denial test now really denies; held [tree 471c2be3ee03] (2026-10-29T20:30:47Z)
- (audit edge) `one fm-reviewer pass (adversary/edge) over all four card lanes; 5 findings fixed by the builder in 9295cee1; merged tree re-linted and tested` → invented CLI names (axe-core-cli) and a fixture test that could never fail were the failure modes; all replaced with real packages or a crawl [tree 471c2be3ee03] (2026-10-29T20:30:47Z)
## Log
- 2026-10-29T20:08:56Z created
- 2026-10-29T20:16:08Z planned from capture
- 2026-10-29T20:16:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2039.builder.md
- 2026-10-29T20:17:02Z focused
- 2026-10-29T20:28:31Z merged worktree-agent-a6ffb0c9390926f8b (26 file(s))
- 2026-10-29T20:29:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6ffb0c9390926f8b
- 2026-10-29T20:29:52Z focused
- 2026-10-29T20:30:20Z set scope=['plugin/skills/library/cards/ux', 'README.md', 'CHANGELOG.md']
- 2026-10-29T20:30:20Z scope: README areas line and the changelog lines for all five card/look lanes
- 2026-10-29T20:31:10Z done
- 2026-10-29T20:31:12Z committed b5910904 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2043 [FEATURE M, planned, 2 steps] Frontend cards: 28 motion, effects and modern-CSS cards
- T-2042 [FEATURE M, planned, 2 steps] UX cards: 25 visual-design and brand cards
- T-2044 [FEATURE M, planned, 2 steps] Web cards: 24 UI, motion and creative-coding library cards
- decision 2026-10-23: T-1538: leave out nudge keys on a live dev server, a gamut-cube picker, a nightly design residency and a weekly design PR
## Lessons
- Builders writing cards invent CLI package names from memory; the lint can't see it, so a reviewer must check every npx line (T-2049 captures a lint)
## Files touched
- plugin/skills/library/cards/ux/onboarding-flows.md
- plugin/skills/library/cards/ux/empty-states.md
- plugin/skills/library/cards/ux/navigation-patterns.md
- plugin/skills/library/cards/ux/ux-writing.md
- plugin/skills/library/cards/ux/error-messages.md
- plugin/skills/library/cards/ux/search-ux.md
- plugin/skills/library/cards/ux/filters-and-facets.md
- plugin/skills/library/cards/ux/command-palette.md
- plugin/skills/library/cards/ux/settings-pages.md
- plugin/skills/library/cards/ux/pricing-pages.md
- plugin/skills/library/cards/ux/checkout-flows.md
- plugin/skills/library/cards/ux/sign-up-flows.md
- plugin/skills/library/cards/ux/notification-design.md
- plugin/skills/library/cards/ux/dashboard-design.md
- plugin/skills/library/cards/ux/progressive-disclosure.md
- plugin/skills/library/cards/ux/multi-step-wizards.md
- plugin/skills/library/cards/ux/undo-patterns.md
- plugin/skills/library/cards/ux/destructive-actions.md
- plugin/skills/library/cards/ux/mobile-navigation.md
- plugin/skills/library/cards/ux/tooltips-and-coachmarks.md
- plugin/skills/library/cards/ux/feedback-collection.md
- plugin/skills/library/cards/ux/permission-prompts.md
- plugin/skills/library/cards/ux/information-architecture.md
- plugin/skills/library/cards/ux/usability-testing.md
- plugin/skills/library/cards/ux/dark-patterns.md
- README.md
- CHANGELOG.md
- MASTER.md
- plugin/commands/looks.md
- plugin/lib/fmcli.py
