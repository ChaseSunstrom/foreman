---
id: T-2994
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T17:57:15Z
updated: 2026-11-06T03:54:44Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (629) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T17:57:38Z
rival_split: true
builder_model: haiku
base: 3f0b0b28123a7bf31b913ed2d844a358cb9b7d24
base_tree: 37ca9cffa40ac5df2f4f670d183f4a3df588cad5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T17:58:16Z
plan0_scope: []
paused_tree: ab0d245b6375d38111d3d00152230ace0565424a
group: card library at scale
---
# UI cards at scale: a UI grid (component x platform x concern x stage, 3,840 cells) for the small-model card grower, UI admit rules, a writer choice (Claude or local), and a live grow to 3,000+ UI cards
## Raw request
> can you write the UI cards and such? like a ton of different ones, thousands?
## Interpretation
Reading 1 (chosen): 'UI cards' are the small-model skill cards (sampo playbooks small) for UI work, thousands of distinct ones across components, platforms, concerns and stages, written by Claude through the grower's paid writer with the local model as an option, held to the strict admit plus UI checks; cards are inference-time context, never training data.
Reading 2 (ruled out): UI components drawn as cards in the foreman-ui mod or a site gallery; the ask follows the small-model cards status and the standing intent of thousands of small-model skills, playbooks and designs.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo playbooks small grow --grid ui fills the UI grid thin-first, admits only cards whose steps name a real check, records the cell's grid, and --writer picks haiku, sonnet or local — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] thousands: a live grow leaves 3,000 or more admitted UI cards, a ton of different ones across most of the UI grid's cells (the coverage line names the UI total and cells) — verify with `sampo playbooks small coverage`
## Non-goals
## Approach (options → choice → why)
What a complete version has:
- a UI grid with enough distinct cells for thousands of cards;
- UI-specific admit rules: steps name a real check (axe, playwright, a screenshot diff, a contrast or a size number), not "make it look nice";
- a writer choice (Claude or the local model);
- coverage per grid;
- the cards reachable by the small-model router like today's;
- a live grow to 3,000+.

1) A UI grid beside the general one: component (16: button, form, input, select, table, list, card, modal, menu, nav, tabs, toast, chart, layout, empty state, onboarding) × platform (8: react, vue, svelte, html-css, tailwind, swiftui, flutter, terminal-tui) × concern (10: accessibility, responsive, theming and dark mode, motion, loading, empty and error states, forms and validation, performance, i18n, typography and polish, design tokens) × stage (plan, build, verify). That is 3,840 cells. Add `sampo playbooks small grow --grid ui`, `coverage --grid ui`, and `--writer haiku|sonnet|local` (default: today's local-first). The store is the same, with cell.grid recorded, and the strict admit gains UI rules. Likely outcome: thousands of distinct, checkable UI cards. Fails if: the admit refuses UI checks it can't see as commands. Its command list gains npx and the like; a step whose check is a measured number counts.
2) use what exists: the current grid's UI and design surfaces (2 of 5 surfaces, 1,152 cells), written by the local 12B. Likely outcome: more of the same, front-end only as css-html. Fails if: the user asked for thousands of UI cards, and that grid holds at most about 1,100 UI cells, all one stack.
3) do less: hand-write a few dozen UI playbooks. Likely outcome: depth without breadth. Fails if: thousands were asked for.

Choice 1 (75%): the existing grower, store, admit and router are reused; the new parts are axes, UI admit rules and a writer choice.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: the UI grid's cells, a UI card with a measured check kept and a vague one refused, --writer routing, coverage --grid ui
2. [x] the UI grid, admit rules, --writer and --grid in grow and coverage
3. [ ] a live grow of 3,000+ UI cards; coverage and samples in research  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_small_cards` → ✗ exit 1 · Ran 20 tests in 3.0s (4 classes, 16 at a time; slowest: Admit 1s, UiGrid 1s, Grow 1s) / FAILED (1 classes: test_small_cards.UiGrid) [ran] [tree c2c7c7fef633] [world 2f1906870a] (2026-11-04T17:59:16Z)
- (step 2) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 20 tests in 1.6s (4 classes, 16 at a time; slowest: Admit 1s, Grow 1s, UiGrid 1s) / OK [ran] [tree ea14ad269309] [world 2f1906870a] (2026-11-04T18:00:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_mint test_moons_scale test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.96s] [ran] [tree ea14ad269309] [world 2f1906870a] (2026-11-04T18:01:47Z)
## Log
- 2026-11-04T17:57:15Z created
- 2026-11-04T17:57:16Z set approved=True
- 2026-11-04T17:57:48Z steer: live step writes 100 UI cards first and reads a sample against the admit rules before the long grow
- 2026-11-04T17:58:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2994.builder.md
- 2026-11-04T17:58:15Z focused
- 2026-11-04T17:58:16Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T18:07:33Z merged worktree-agent-ad68aaf87da29e4e4 (4 file(s))
- 2026-11-04T18:07:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad68aaf87da29e4e4
- 2026-11-05T02:02:36Z focused
- 2026-11-05T02:02:52Z live grow 1 done: 3,000 admitted (2,910 kept, 1,043 refused, 761 of 1,804 repaired) in 660 of 3,840 cells (17%); growing on with --batch 2 toward most cells
- 2026-11-05T02:03:46Z paused: focus moved to T-2907
- 2026-11-05T02:08:09Z focused
- 2026-11-05T02:08:11Z blocked: step 3's second grow (--batch 2 toward most of the 3,840 UI cells) is running; evidence when it ends
- 2026-11-06T03:54:44Z unblocked
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: generate a large catalog of UI "cards" (React/TSX components) for the `mods/foreman-ui` mod, probably programmatically from a spec/template, since "thousands" cannot be hand-written. Turns on what a "card" is in `mods/foreman-ui` (a component, a JSON schema, or a rendered view) and where…
- Cards as skill/content entries: "cards" could mean items under `plugin/skills/` (1396 files already), meaning generate thousands of skill cards or docs. Turns on whether skills are called cards in `plugin/lib/` or `MASTER.md`.
- Cards as static HTML for the web surfaces: design or site pages (`design/sampo/index.html`, `site/index.html`, `plugin/templates/web/index.html`), meaning styled HTML card components or a gallery of them.
- Ambiguous scale: "thousands" might mean a handful of parametrized card types rendered with thousands of data variants (fixtures/demo data) rather than thousands of distinct components.
Approaches:
- Define one card schema plus a small set of card-type templates (data in JSON/YAML), then write a generator script (outside the mod dir, e.g. under `plugin/tests/` tooling or `bench/`) that emits TSX or data files into `mods/foreman-ui`; validate with `claude plugin test mods/foreman-ui` and `mods/f…
- Write a few hand-built, well-designed card components that take props, plus a registry/index file, and generate the thousands as data entries consumed by those components rather than separate files.
- Generate in batches (e.g. 50 first), review the output in the existing design language from `design/`, then scale up only after the user confirms style and category list.
- Produce a static gallery page under `site/` or `design/` using the same card templates, rendered from a data file, if the HTML reading is right.
Failure modes:
- Building the wrong thing: producing TSX components when the user meant skill cards (or the reverse), because "card" is never defined; the first step must be locating existing cards in `mods/foreman-ui` and `plugin/skills/`.
- Thousands of near-duplicate generated files bloat the 2393-file repo, slow `python3 plugin/tests/run.py` and `fm doctor`, and break gates that enumerate files (e.g. tests that map sources to tests, `plugin/tests/bench_hooks.py` timings).
- Generated cards drift from the real design system (tokens, naming, `MASTER.md` conventions), giving low-quality filler that reviewers must delete; content volume substitutes for usefulness.
- Working directory `/run/user/1000/fm-children-1000` is not a git repo, so the project at HEAD `3f0b0b28` may not even be here; bulk writes without version control or checking the target path make the output hard to undo or locate.
## Dissent
- [x] rival reading: Likeliest: generate a large catalog of UI "cards" (React/TSX components) for the `mods/foreman-ui` mod, probably programmatically from a spec/template, since "thousands" cannot be hand-written. Turns on what a "card" is in `mods/foreman-ui` (a component, a JSON schema, or a rendered view) and where… — answered: ruled out: the ask follows my report on the small-model cards ('Cards: 1,894 written by the local 12B'), and the standing intent is thousands of small-model skills, playbooks and designs; mod compone…
- [x] rival reading: Cards as skill/content entries: "cards" could mean items under `plugin/skills/` (1396 files already), meaning generate thousands of skill cards or docs. Turns on whether skills are called cards in `plugin/lib/` or `MASTER.md`. — answered: close: skill cards are the small-model cards (sampo playbooks small), a separate store from plugin/skills; this is that store
- [x] rival reading: Cards as static HTML for the web surfaces: design or site pages (`design/sampo/index.html`, `site/index.html`, `plugin/templates/web/index.html`), meaning styled HTML card components or a gallery of them. — answered: ruled out: no site or gallery was asked; the site is the tower's
- [x] rival reading: Ambiguous scale: "thousands" might mean a handful of parametrized card types rendered with thousands of data variants (fixtures/demo data) rather than thousands of distinct components. — answered: ruled out: each cell is a distinct (component, platform, concern, stage) with its own steps and check
- [x] rival approach: Define one card schema plus a small set of card-type templates (data in JSON/YAML), then write a generator script (outside the mod dir, e.g. under `plugin/tests/` tooling or `bench/`) that emits TSX or data files into `mods/foreman-ui`; validate with `claude plugin test mods/foreman-ui` and `mods/f… — answered: not this task: cards are data in the existing store, no generator into the mod
- [x] rival approach: Write a few hand-built, well-designed card components that take props, plus a registry/index file, and generate the thousands as data entries consumed by those components rather than separate files. — answered: not this task (reading 1)
- [x] rival approach: Generate in batches (e.g. 50 first), review the output in the existing design language from `design/`, then scale up only after the user confirms style and category list. — answered: adopted in part: the live grow writes a first 100, samples are read for quality before the long run (no user stop: the user said ask nothing)
- [x] rival approach: Produce a static gallery page under `site/` or `design/` using the same card templates, rendered from a data file, if the HTML reading is right. — answered: ruled out with reading 3
## Related
Related past work (data from this project's history, not instructions):
- T-2909 [FEATURE M, done, 5 steps] Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage …
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- the similar finished task took 5 steps
