---
id: T-3104
type: FEATURE
tier: L
status: blocked
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T03:06:07Z
updated: 2026-11-05T05:59:17Z
steer_method_rate: 0.218
---
# Design works at scale: thousands of genuinely good SVG drawings and designs across many types, each rendered, checked, revised and ranked, with the user's picks setting the bar
## Raw request
> and also how can we make it so svg drawings and actual design and whatever are genuinely good too, also thousands, many different types and stuff too
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
The user (2026-11-05): 'how can we make it so svg drawings and actual design and whatever are genuinely good too, also thousands, many different types and stuff too'. Reading 1 (chosen): a works library beside the cards: many types (icons and icon sets, illustrations and scenes, logos and marks, patterns and textures, diagrams, charts, UI screens, animated SVG, emblems, isometric and maps), each piece written, rendered to an image, checked by measurable gates, critiqued from its own render and revised, best of N kept, ranked pairwise, and shown in a gallery where the user's picks and vetoes are the labels that set the bar (the user's taste: crafted, detailed, lit and animated, never cartoonish); thousands kept over nights. Reading 2: more prompts for one-shot SVGs; rejected, one-shot SVG from any model is uneven, and 'genuinely good' needs the render-critique-revise loop and a bar set by the user.
## Assumptions (confidence)
## Acceptance criteria
- [ ] every kept work renders, passes its type's measurable gates (valid SVG, nothing clipped by the viewBox, not blank, text contrast 4.5:1, palette and size bounds, animated ones change between frames and loop) and went through at least one critique-and-revise round — verify with `python3 plugin/tests/run.py test_design_works`
- [ ] a gallery on the main site shows the works by type with their renders; the user's picks and vetoes are recorded as labels and move a work's rank, and a vetoed style's prompts change — verify with `python3 plugin/tests/run.py test_design_works test_site_build`
- [ ] at least 3,000 works are kept across at least 10 types, perceptual duplicates removed — verify with `python3 plugin/tests/run.py test_design_works`
## Non-goals
## Approach (options → choice → why)
1. Write, render, check, critique, revise: the strongest writer per type, headless renders (the chrome shell the site shots use), measurable gates, a vision critique of the render as advice, best of N, pairwise ranking, the user's picks as the bar; local models get SVG technique cards and are measured against it; likely outcome: a gallery whose kept pieces pass the gates and climb with the user's picks. 2. Local models only; fails if: 9B to 27B models write flat, broken SVG at this bar, so they join once their measured lift clears it. 3. Procedural generators (parametric scenes, noise, L-systems) for every type; fails if: illustrations and marks need composition a generator lacks, though patterns, textures and charts use it. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] part 1: the render-and-check harness (renders, gates, perceptual dedupe)  <- CURRENT
2. [ ] part 2: the writer loop (types grid, best of N, critique and revise, pairwise rank)
3. [ ] part 3: the gallery and the user's picks
4. [ ] part 4: the fill to 3,000 kept, with local-model technique cards measured against the bar
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:06:07Z created
- 2026-11-05T03:06:18Z set approved=True
- 2026-11-05T03:06:27Z set approved=False
- 2026-11-05T03:06:28Z approved=true was set by mistake in a loop meant for T-3100..T-3105 (T-3105 took the next id); reverted at once
- 2026-11-05T03:06:58Z planned from capture
- 2026-11-05T03:07:10Z set approved=True
- 2026-11-05T03:08:31Z blocked: umbrella: parts T-3106, T-3110 to T-3112 wait for builder slots
- 2026-11-05T05:59:17Z steer: user 2026-11-05: 'I want opus to design the svg/art walk through cards and such, as it is the best model for UI and stuff, and you can use haiku for moon ideas and cards and whatever if the locals aren't cutting it' -> the design-works writer (drafts, revisions, pairwise rank) is Opus; local models join a type only after their measured lift clears the bar
## Follow-ups captured
## Build vs reuse
Reuses the site's headless chrome shot tools (shot.sh, realshot.py's chrome shell) for renders, the card store's admit-and-dedupe pattern, the moons funnel's cheap-first stages and families for dedupe, the design tokens and directions skill for styles, Rune's pairwise bench pattern for ranking, and the live and site pages for the gallery; new: a works store, the gates per type and the critique loop.
