---
id: T-2824
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T17:43:53Z
updated: 2026-11-03T21:08:46Z
steer_method_rate: 0.218
done_in: T-2742
---
# Treat the user's visual preference as standing for all Sampo-facing design work: a…
## Raw request
> I like the kind of rock with runes on it look and such, not the round thing
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the user's visual preference as standing for all Sampo-facing design work: a carved-stone look with rune-style engraving (angular, chiseled glyphs, weathered rock texture, inscribed edges), not a round or circular motif.
- Apply it to every visual surface the work touches: logo, mascot, icons, favicon, badges, buttons, avatars, loaders and progress indicators, empty states, illustrations, splash and README art, and docs diagrams.
- Replace round elements with stone-slab or monolith forms (rectangular, faceted, or irregular rock silhouettes) and runic glyphs. Don't use circles, discs, orbs, or pill-shaped containers as the main shape unless the user asks for one.
- Build the style into shared design tokens, themes, and components (colors, border radius, texture, glyph set, icon set) so new work inherits it. Don't restyle individual screens by hand.
- Keep rune glyphs decorative or symbolic only, and make sure they never replace readable text, labels, or accessible names. Keep contrast, legibility at small sizes, and alt text and ARIA labels intact.
- Reduce border radii to near-square or chamfered corners. Remove existing circular avatars, round buttons, and spinner rings in the touched area, or flag any that can't be changed, such as third-party widgets or OS-mandated icons.
- Check the result by search and by looking. Grep styles and assets for `border-radius: 50%`, `rounded-full`, circle SVG elements, and similar. Render or screenshot the affected views and confirm the stone-and-rune look, with no round primary shapes remaining.
- Update visual snapshot tests, design docs, style guide or CLAUDE.md notes, and asset sources so they match. Record the preference in memory as a user or feedback item.
- Make the changes directly and show before/after evidence. Don't just suggest options.
- Treat "the round thing" as the circular or orb motif currently in use. If you can't tell which element is meant, find the likeliest candidate in the project and say which one you changed.
- Keep outward or irreversible steps behind the user's grant: publishing assets, replacing a live brand logo or favicon, deleting original art files, and pushing or deploying. Keep the originals until the user approves.
- Don't add new fonts, textures, or asset packs from outside sources without checking their license, and don't pull them from untrusted downloads without the user's approval.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-03T17:43:53Z created
- 2026-11-03T21:08:46Z done in T-2742: already a decision citing this steer (decisions.md, check pending T-2788): the anvil is the rune-carved stone
## Follow-ups captured
