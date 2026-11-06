---
id: T-3311
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: [T-3181]
source: user
created: 2026-11-06T04:10:55Z
updated: 2026-11-06T04:11:18Z
---
# Opus-written art cards that let our weak local models make beautiful SVG art: each card a verified generator (composition, palette, shapes, motion as typed slots) the small model fills, with a render checker
## Raw request
> Opus-written art cards that let our weak local models make beautiful SVG art: each card a verified generator (composition, palette, shapes, motion as typed slots) the small model fills, with a render checker
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] Opus writes art cards (one per style or subject family): a parametrised SVG generator with typed slots, a palette from design tokens, composition rules, and a checker that renders it and runs the works gates (blank, overflow, contrast, overlap) — verify with `python3 plugin/tests/run.py test_art_cards`
- [ ] a local model (the GPU mimo 9B or Gemma 12B) fills a card's slots from a one-line brief, and the result passes the gates; blind-judged against the same model's free-hand SVG on 20 briefs, the card output wins most — verify with `python3 plugin/tests/run.py test_art_cards`
- [ ] the cards are callable by name through the calling-cards path (T-3157) and grow over nights, Opus writing new cards where small-model outputs fail — verify with `python3 plugin/tests/run.py test_art_cards`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Opus drafts 10 art cards across styles (illustrated, geometric, data art, icon, scene)  <- CURRENT
2. [ ] slot-filling harness for local models + render checker
3. [ ] blind A/B on 20 briefs; keep what wins
4. [ ] wire into calling cards and the night grower
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:10:55Z created
- 2026-11-06T04:11:18Z set depends_on=['T-3181']
## Follow-ups captured
