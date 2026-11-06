---
id: T-1650
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_looks_gallery.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:58:29Z
updated: 2026-10-23T12:32:16Z
base: 554c555218264ef959eec381e1b03579731aade4
base_tree: 0776ac83a1e63b8b1b9bdb2950b8ae5ebc00c65c
plan0_at: 2026-10-23T12:30:00Z
plan0_scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_looks_gallery.py, CHANGELOG.md]
verified: strong
---
# Looks gallery extras: shader sketchbook live thumbnails, trading cards, dice, a site galle
## Raw request
> Looks gallery extras: shader sketchbook live thumbnails, trading cards, dice, a site gallery (from T-1539; waits: after the gallery)
## Interpretation
This pass: fm page looks --cards writes the look cards as trading cards on a print sheet (63 x 88 mm, nine to an A4 page), each in its own palette roles and type pair, one file with nothing from another host. Dice shipped as fm design roll (T-1648); the shader sketchbook and the site gallery are captured as their own items.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm page looks --cards writes one card per look on an A4 print sheet, text escaped, no outside host, its own --out mark — verify with `python3 plugin/tests/run.py test_looks_gallery`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] cards_html and --cards, test first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_looks_gallery.Cards` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Cards 0s) / FAILED (1 classes) [ran] [tree 800f87ee4459] (2026-10-23T12:30:03Z)
- (step 1) `python3 plugin/tests/run.py test_looks_gallery test_page test_cli` → exit 0 · Ran 147 tests in 39.6s (44 classes, 16 at a time; slowest: TaskLifecycle 39s, StateViews 21s, AuditPrep 20s) / OK [ran] [tree ee90a1e5d33a] (2026-10-23T12:31:37Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery` → exit 0 · Ran 14 tests in 3.6s (3 classes, 16 at a time; slowest: Roll 3s, Gallery 1s, Cards 0s) / OK [ran] [tree ee90a1e5d33a] (2026-10-23T12:31:42Z)
- (ac 1) `python3 plugin/tests/run.py test_looks_gallery` → exit 0 · Ran 14 tests in 3.6s (3 classes, 16 at a time; slowest: Roll 3s, Gallery 1s, Cards 0s) / OK [ran] [tree ee90a1e5d33a] (2026-10-23T12:31:46Z)
- (audit edge) `self: the sheet reuses look_cards and FACES; every card text is escaped, colours come only from the cards' hex roles, ids from sanitized names; looked at it (fm shot): 12 cards in their own palettes, the strip outlined so a swatch the colour of its card still shows` → a card without --surface, --text or --accent falls back to white, near-black and its text colour; --out refuses a file fm didn't write and the gallery and the sheet never overwrite each other (each its own mark); print keeps the colours (print-color-adjust) [tree ee90a1e5d33a] (2026-10-23T12:31:46Z)
- (audit adversary) `self: the sheet reuses look_cards and FACES; every card text is escaped, colours come only from the cards' hex roles, ids from sanitized names; looked at it (fm shot): 12 cards in their own palettes, the strip outlined so a swatch the colour of its card still shows` → a hostile title or line in a card is escaped (tested with </style><script> and an img onerror); nothing loads from another host [tree ee90a1e5d33a] (2026-10-23T12:31:46Z)
- (audit self) `self: the sheet reuses look_cards and FACES; every card text is escaped, colours come only from the cards' hex roles, ids from sanitized names; looked at it (fm shot): 12 cards in their own palettes, the strip outlined so a swatch the colour of its card still shows` → no findings [tree ee90a1e5d33a] (2026-10-23T12:31:46Z)
## Log
- 2026-10-22T20:58:29Z created
- 2026-10-23T12:25:02Z set tier=S, scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_looks_gallery.py', 'CHANGELOG.md']
- 2026-10-23T12:30:00Z focused
- 2026-10-23T12:32:14Z done
- 2026-10-23T12:32:16Z committed e3714c7e (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- T-1539 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second po
- T-1649 [FEATURE M, done, 3 steps] Looks gallery: fm page builds one living specimen per look card, single file, no network — lesson: Never gate visible content on a scro…
- T-1648 [FEATURE M, done, 3 steps] fm design roll: a seeded, coherent pick from the look cards, applied as one reversible patch — lesson: An undo record must be written a…
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_page.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/tests/test_looks_gallery.py; re-ground the plan against them before editing
## Lessons
- Look at a generated page before closing: the first render hid a swatch the colour of its own card
## Plan gaps
- failed first: step 1 cards_html and --cards, test first
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmpage.py
- plugin/tests/test_looks_gallery.py
