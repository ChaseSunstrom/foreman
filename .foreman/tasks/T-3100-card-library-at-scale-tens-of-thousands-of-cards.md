---
id: T-3100
type: FEATURE
tier: L
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:05:17Z
updated: 2026-11-05T05:59:18Z
group: card library at scale
---
# Card library at scale: tens of thousands of cards on every kind of work, browsable on the main site, each UI card with a rendered example
## Raw request
> Card library at scale: tens of thousands of cards on every kind of work, browsable on the main site, each UI card with a rendered example
## Interpretation
The user (2026-11-05): 'how can I view all of the cards?', 'can you add it to the main website? and also have UI examples of each of the UI cards used and such?', 'and we will want 10s of thousands of skills/cards not just related to UI too, but all sorts of things'. Reading 1 (chosen): a Cards page on the main site over the whole store, a rendered example beside every UI card, grids as data with many new domains (more languages, ops and infra, data and ML, security, docs and research writing, design, product and planning, and Sampo's own problem solving, memory and efficiency), and a fill to 30,000 kept cards, local writers first. Reading 2: only a browser for today's 5,031 cards and their UI examples; rejected, the third message asks for tens of thousands on all sorts of things.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the main site has a Cards page over the whole card store, searchable and filterable by grid cell, with a permalink per card — verify with `python3 plugin/tests/run.py test_site_build`
- [ ] every UI card on the Cards page shows a rendered example of its component, a card-specific one where a checked one exists, else its component's kit demo — verify with `python3 plugin/tests/run.py test_site_build test_small_cards`
- [ ] at least 30,000 cards are kept across at least 8 grids, the counts on the Cards page and the live page — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the card store, admit() and grow --grid, the site build and the live progress feed; four M parts: the site page, UI examples, grids as data with new domains, the 30,000 fill; likely outcome: the page ships first on today's cards and grows as the fill runs. 2. Do less: the site page and UI examples only, growth later; fails if: the user's tens of thousands never start. 3. Generate examples as screenshots at build; fails if: thousands of PNGs bloat the site and can't follow the theme. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] part 1: the site Cards page  <- CURRENT
2. [ ] part 2: UI examples
3. [ ] part 3: grids as data, new domains
4. [ ] part 4: the fill to 30,000 kept
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:05:17Z created
- 2026-11-05T03:06:28Z set approved=True
- 2026-11-05T03:08:31Z blocked: umbrella: parts T-3101 to T-3105 wait for builder slots, which free as the merge queue lands
- 2026-11-05T05:59:18Z steer: user 2026-11-05: 'I want opus to design the svg/art walk through cards and such, as it is the best model for UI and stuff, and you can use haiku for moon ideas and cards and whatever if the locals aren't cutting it' -> local writers first, Haiku as the fallback when they fall short
## Follow-ups captured
## Build vs reuse
Reuses smallcards (the store, admit, dedupe, grow --grid, coverage), the site build (site/build.py, pages.py, writeif), the live progress feed (T-3083), the night job, and the local writers moons already uses (moonscale._ask); the card library artifact's page is the starting design for the site page. Nothing new outside the repo.
