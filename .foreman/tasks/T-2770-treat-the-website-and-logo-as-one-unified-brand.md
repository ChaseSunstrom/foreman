---
id: T-2770
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T04:43:48Z
updated: 2026-11-03T04:46:45Z
steer_method_rate: 0.218
---
# Treat the website and logo as one unified brand system: redesign them together from…
## Raw request
> I don't think I am a fan of the website and logo, I want it to look nicer, way better animations, more details on the site, better logo, cooler website matching the vibe of the logo completely, completely redesigned/reimagined, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the website and logo as one unified brand system: redesign them together from scratch, not as incremental tweaks, so the site's look, colors, typography, imagery and motion all derive from and fully match the new logo's vibe.
- Create a new, better logo (clean, scalable vector such as SVG) and deliver it in every form the project uses: header mark, favicon and app icons, social/OG share image, and light/dark variants. Replace every place the old logo appears.
- Reimagine the visual design completely: new layout, color palette, typography scale, spacing, components and a consistent design-token set, rather than restyling the existing pages.
- Add far better animations: polished page-load, scroll-triggered reveals, hover/focus micro-interactions and smooth transitions. Keep them performant (transform/opacity, no layout jank) and honor `prefers-reduced-motion`.
- Add more detail and content depth to the site: richer sections, fuller descriptions, features, visuals and supporting information. Use real content from the project where it exists and clearly marked placeholders where it does not, never invented facts.
- Keep the site's existing purpose, pages, links, and working functionality intact while redesigning; check that nothing is lost or broken.
- Make the result responsive across mobile, tablet and desktop, accessible (contrast, keyboard navigation, focus states, alt text, semantic HTML) and fast (optimized assets, sensible loading).
- Act rather than advise: inspect the current site and logo first, then implement the redesign directly, and verify by building and running it, checking it in a browser at multiple viewport sizes, and reviewing screenshots against the logo's look.
- Update all related surfaces together: metadata and titles, README/docs, and any tests or snapshots that the redesign affects, and run the project's existing tests, lint and build to confirm they pass.
- Keep outward or irreversible steps behind the user's grant: do not deploy, publish, push, or overwrite/delete existing assets without confirmation. Preserve the originals (for example in version control or a backup folder) so the change can be reverted.
- Where taste is subjective, pick a strong, coherent direction and commit to it, then summarize the choices and offer alternatives rather than stopping to ask up front.
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
- 2026-11-03T04:43:48Z created
- 2026-11-03T04:46:45Z dropped: same request as T-2772, which redesigns the logo and site together as one system (the directions each pair a logo with its site, and the build-out carries the pick through every surface)
## Follow-ups captured
