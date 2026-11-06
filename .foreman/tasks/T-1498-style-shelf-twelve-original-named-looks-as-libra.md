---
id: T-1498
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/looks, plugin/tests/test_library.py, plugin/skills/playbooks/references/ui/design-direction.md, README.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:13Z
updated: 2026-10-22T18:16:55Z
base: 16c6cd964fa63bc618721808c0dadcb43fa2a885
base_tree: 05be2257f9f8d14f388a7fcb9deca00a3b66e097
plan0_at: 2026-10-22T18:02:40Z
plan0_scope: [plugin/skills/library/cards/looks, plugin/tests/test_library.py, CHANGELOG.md]
verified: strong
---
# Style shelf: twelve original named looks as library cards
## Raw request
> Style shelf: twelve original named looks as library cards
## Interpretation
Brainstorm T-1479 cluster 7: a named look gives Claude a concrete, non-generic target. Twelve original looks (for example: lab notebook, transit signage, risograph zine, museum placard, instrument panel, botanical plate, brutalist index, night market, cartographer, ceramic studio, broadcast graphics, archive ledger), each a card with palette roles (hex), type pairing by class, layout idea, motion temperament, texture, one do and one don't, and the subjects it suits. Original writing; no brand imitation.
## Assumptions (confidence)
## Acceptance criteria
- [x] twelve look cards exist in a looks group, each with every field, and fm lib finds them — verify with `cd plugin/tests && python3 -m unittest test_library.Looks`
## Non-goals
## Approach (options → choice → why)
Options: one long gallery page; chosen: one card per look in the existing library format so fm lib show NAME and suggestions work.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: the twelve cards and their fields
2. [x] write the cards
## Resume here
## Docs impact
CHANGELOG.md line; README.md area list; plugin/skills/playbooks/references/ui/design-direction.md pointer
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_library.Looks` → ✗ exit 1 · Ran 3 tests in 0.614s / FAILED (failures=2) [ran] [tree 88e47865b3a7] (2026-10-22T18:07:32Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.Looks` → exit 0 · Ran 3 tests in 0.589s / OK [ran] [tree 350e23099b06] (2026-10-22T18:13:15Z)
- `cd plugin/tests && python3 -m unittest test_library.Looks` → ✗ exit 1 · Ran 3 tests in 0.814s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree d7e4600cb8a7] (2026-10-22T18:15:32Z)
- `cd plugin/tests && python3 -m unittest test_library.Looks` → exit 0 · Ran 3 tests in 0.952s / OK [ran] [tree d7e4600cb8a7] (2026-10-22T18:15:32Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.Looks` → exit 0 · Ran 3 tests in 1.041s / OK [ran] [tree d7e4600cb8a7] (2026-10-22T18:15:34Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_library` → exit 0 · Ran 33 tests in 17.091s / OK [ran] [tree d7e4600cb8a7] (2026-10-22T18:15:52Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library` → exit 0 · Ran 33 tests in 17.450s / OK [ran] [tree d7e4600cb8a7] (2026-10-22T18:16:10Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.Looks` → exit 0 · Ran 3 tests in 0.891s / OK [ran] [tree e1b9cc8c368e] (2026-10-22T18:16:20Z)
- (audit intent) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → concrete, original, non-generic targets for UI work, findable with fm lib [tree e1b9cc8c368e] (2026-10-22T18:16:20Z)
- (audit edge) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → fm lib's automatic suggestions can't offer them (no stack to detect); search, list, show and the playbook pointer do [tree e1b9cc8c368e] (2026-10-22T18:16:20Z)
- (audit maintainer) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → one card format; README counts 28 areas [tree e1b9cc8c368e] (2026-10-22T18:16:20Z)
- (audit intent) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → concrete, original, non-generic targets for UI work, findable with fm lib [tree e1b9cc8c368e] (2026-10-22T18:16:40Z)
- (audit adversary) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → the test exec()s the python block of cards in the repo's own looks folder only (our files, reviewed in the diff), never a third-party or fetched card [tree e1b9cc8c368e] (2026-10-22T18:16:40Z)
- (audit edge) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → fm lib's automatic suggestions can't offer them (no stack to detect); search, list, show and the playbook pointer do [tree e1b9cc8c368e] (2026-10-22T18:16:40Z)
- (audit maintainer) `builder test-first (red proved: 2 failures on the start tree); the test re-measures every stated contrast ratio against its floor and runs each card's own contrast code; dark looks meet 7:1 body text; accents kept 30 degrees from the reserved status hues; five suggested looks that duplicated design-direction's bank were replaced; names prefixed look- so everyday prompt words don't trigger them` → one card format; README counts 28 areas [tree e1b9cc8c368e] (2026-10-22T18:16:40Z)
## Log
- 2026-10-22T17:36:13Z created
- 2026-10-22T17:58:58Z set scope=['plugin/skills/library/cards/looks', 'plugin/tests/test_library.py', 'CHANGELOG.md']
- 2026-10-22T18:02:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1498.builder.md
- 2026-10-22T18:02:39Z focused
- 2026-10-22T18:13:00Z scope: README.md area count (27 -> 28, adds looks) and one pointer line in design-direction.md's bank to the looks shelf; both go stale or undiscoverable without it
- 2026-10-22T18:15:27Z merged worktree-agent-a7f95bd08bc36f755 (15 file(s))
- 2026-10-22T18:15:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7f95bd08bc36f755
- 2026-10-22T18:15:28Z focused
- 2026-10-22T18:16:18Z set scope=['plugin/skills/library/cards/looks', 'plugin/tests/test_library.py', 'plugin/skills/playbooks/references/ui/design-direction.md', 'README.md', 'CHANGELOG.md']
- 2026-10-22T18:16:53Z done
- 2026-10-22T18:16:55Z committed 1844b2bd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1489 [FEATURE M, done, 2 steps] UI playbook: type and colour — lesson: Embedded scripts in a playbook should be run by the writer against the playbook's own example; i…
- T-1499 [FEATURE M, planned, 2 steps] Style shelf: shader looks, light and material recipes, an SVG icon system
- playbook Design direction before pixels (skills/playbooks/references/ui/design-direction.md)
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- the similar finished task took 2 steps
## Why not caught
new cards
## Lessons
- Name taste cards with a prefix (look-) so a single everyday word in a prompt doesn't pull them in.
## Plan gaps
- failed first: step 1 failing test: the twelve cards and their fields
## Files touched
- plugin/tests/test_library.py
- plugin/skills/library/cards/looks/look-lab-notebook.md
- plugin/skills/library/cards/looks/look-transit-signage.md
- plugin/skills/library/cards/looks/look-cartographer.md
- plugin/skills/library/cards/looks/look-ceramic-studio.md
- plugin/skills/library/cards/looks/look-broadcast-graphics.md
- plugin/skills/library/cards/looks/look-archive-ledger.md
- plugin/skills/library/cards/looks/look-night-market.md
- plugin/skills/library/cards/looks/look-card-catalogue.md
- plugin/skills/library/cards/looks/look-sewing-pattern.md
- plugin/skills/library/cards/looks/look-shipping-manifest.md
- plugin/skills/library/cards/looks/look-observatory.md
- plugin/skills/library/cards/looks/look-lido.md
- README.md
- plugin/skills/playbooks/references/ui/design-direction.md
- CHANGELOG.md
