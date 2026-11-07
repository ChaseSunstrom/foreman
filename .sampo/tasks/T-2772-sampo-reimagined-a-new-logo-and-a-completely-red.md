---
id: T-2772
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T04:44:31Z
updated: 2026-11-03T20:24:36Z
done_in: T-2742
---
# Sampo reimagined: a new logo and a completely redesigned site (user steer 2026-11-03): four rendered directions (logo, animated hero, sections) to choose from, then the chosen one carried through every page, the logo's variants, the README header and the design tokens, with far richer animation and detail, the site matching the logo's world completely
## Raw request
> Sampo reimagined: a new logo and a completely redesigned site (user steer 2026-11-03): four rendered directions (logo, animated hero, sections) to choose from, then the chosen one carried through every page, the logo's variants, the README header and the design tokens, with far richer animation and detail, the site matching the logo's world completely
## Interpretation
Reading 1 (chosen): the user rejected the Runestone logo and the site built on it (T-2747, T-2751, T-2753, T-2759). They want it nicer, with much better animation, more detail and a better logo, and a site that matches the logo's world completely: a full reimagining. SAMPO.md's frame still holds ('ancient forge meets living machine', the logo deliverables, the site page list, the quality bar), but this time the user's eye picks, not only a cold review. So: four distinct directions, each a new logo plus a live animated landing concept (scratchpad/directions-v2/1-kirjokansi, 2-forge, 3-copper-mountain, 4-living-machine). Each is published as a private artifact so the user can open it live from any device, and the user picks one (or a blend). The pick then becomes design/sampo (tokens.json, the logo and every variant SAMPO.md lists: 16 px icon, mono, wordmark, animated with a still, favicon, app and Desktop icons, README headers, share card, pane glyph) and every site page: the landing, the feature pages, Rune live, Louhi, Moons, Underworld, Ward, install and docs. Each page meets the quality bar and passes a cold design review on a stronger model. T-2767's data layer (the stats.py collectors) carries over; its visuals are redone. Reading 2 (ruled out): restyle the current site's tokens and keep the Runestone. The user asked for a complete redesign, logo included.
## Assumptions (confidence)
## Acceptance criteria
- [ ] four distinct directions exist as live pages, each with its own animated logo, hero and sections, shown to the user for a pick — verify with `ls /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2`
- [ ] the user's pick is recorded with fm decide --cites, and the build-out is its own planned task with criteria for the logo variants, tokens, every page, the quality bar and a cold review — verify with `fm decide --review`
## Non-goals
## Approach (options → choice → why)
1. Directions first, then build (chosen): four opus designers in parallel, each with a self-contained concept (logo, animated hero, four or more sections, a canvas or WebGL scene, reduced-motion stills, a phone layout). Publish them as artifacts and ask the user to pick. Then builder lanes carry the pick into design/sampo/logo/build.py (generated SVG variants, byte-for-byte tested as now), tokens.json (which drives style.css through site/build.py --tokens), and the pages split across lanes: the landing; the feature-page template; Rune, Louhi, Moons and Underworld; Ward, install and docs. Likely outcome: a site the user chose, built on the existing build and test machinery. Fails if: the concept's raw HTML doesn't fit build.py's page model; then the landing becomes a hand-authored template that build.py fills with data.
2. Pick for the user by a cold design review, as last time. Fails if: that is how Runestone shipped and the user rejected it.
3. One designer, one direction, then iterate with the user. Fails if: there is one sample to react to, and each round trip is slow.
4. Use what exists: the directions skill and fm looks for the six style directions. Fails if: they make palettes and type specimens, not animated logo and hero concepts, which is the level the user judges at.
Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] four direction concepts in parallel, each a logo plus a live landing concept, screenshots  <- CURRENT
2. [ ] show them; the user picks
3. [ ] record the user's pick (fm decide citing their steer) and plan the build-out as its own L task with its own criteria: logo and variants, tokens, every page, quality bar, cold review
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-03T04:44:31Z created
- 2026-11-03T04:46:36Z step 3 text: the chosen direction becomes design/sampo (tokens, logo and variants) and every site page → record the user's pick (fm decide citing their steer) and plan the build-out as its own L task with its own criteria: logo and variants, tokens, every page, quality bar, cold review
- 2026-11-03T04:46:37Z second plan: split the build-out (old step 3) into its own task after the pick (HIGH 1, adopted); the steer's date is UTC 2026-11-03, the user's message this session (HIGH 2, dismissed); each designer has its own world, palette and motion language in its prompt (MEDIUM 3, done; phone and WebGL weight is the build-out's quality bar); artifacts are private by default (MEDIUM 4, noted); the Runestone stays in git history as the rollback (LOW)
- 2026-11-03T20:24:36Z done in T-2742: the directions were rendered (directions-v2, picker artifact) and the user picked 12-forge-illustrated on 2026-11-03; T-2788 carries the pick through every surface under T-2742 step 7
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The only acceptance criterion is `ls` on a directory, which proves files exist, not that four distinct, working, animated directions exist or that the user saw them. Steps 1–2 also hinge on "publish as private artifacts" and "user picks", and nothing checks either — Replace it with checkable …
- HIGH: The task bundles two very different deliverables: a choose-one exploration (step 1–2) and a huge build-out (step 3: tokens, ~10 logo variants, README, every page, cold review per page). Step 3 has no criteria at all, and the Interpretation's quality bar and "cold design review on a stronger m…
- HIGH: The date in the steer (2026-11-03) is a day after today (2026-11-02), and the request hasn't been confirmed by the user in this session. The plan also commits to reading 1 (full redesign including logo) at 80% on a paraphrase of a steer — Confirm the steer's date and wording against the origi…
- MEDIUM: Directions are diverse by name only. Four designers running independently with the same brief tend to converge, and they are told to produce a "canvas or WebGL scene", which is heavy and fragile on a phone and under reduced motion — Give each designer a distinct, written constraint (palette…
- MEDIUM: Publishing as private artifacts is an outward-facing step with no stated confirmation or visibility check. The content is the project's brand and may carry unreleased material; "private" is assumed, not verified — Confirm the artifact's access scope (owner-only link) before sharing, and say…
- LOW: No rollback or isolation is stated for step 3. It replaces the logo, tokens, README header and every page of a live site, while the old Runestone assets are the only fallback, and the directory isn't a git repo here — Tag or branch the current design/sampo and site before the carry-through, an…
Verdict: revise — step 1 is sound, but the criteria don't prove the request, step 3 is unspecified, and the date and steer should be confirmed before spending the budget.
## Dissent
- [ ] HIGH: The only acceptance criterion is `ls` on a directory, which proves files exist, not that four distinct, working, animated directions exist or that the user saw them. Steps 1–2 also hinge on "publish as private artifacts" and "user picks", and nothing checks either — Replace it with checkable …
- [ ] HIGH: The task bundles two very different deliverables: a choose-one exploration (step 1–2) and a huge build-out (step 3: tokens, ~10 logo variants, README, every page, cold review per page). Step 3 has no criteria at all, and the Interpretation's quality bar and "cold design review on a stronger m…
- [ ] HIGH: The date in the steer (2026-11-03) is a day after today (2026-11-02), and the request hasn't been confirmed by the user in this session. The plan also commits to reading 1 (full redesign including logo) at 80% on a paraphrase of a steer — Confirm the steer's date and wording against the origi…
- [ ] MEDIUM: Directions are diverse by name only. Four designers running independently with the same brief tend to converge, and they are told to produce a "canvas or WebGL scene", which is heavy and fragile on a phone and under reduced motion — Give each designer a distinct, written constraint (palette…
- [ ] MEDIUM: Publishing as private artifacts is an outward-facing step with no stated confirmation or visibility check. The content is the project's brand and may carry unreleased material; "private" is assumed, not verified — Confirm the artifact's access scope (owner-only link) before sharing, and say…
- [ ] LOW: No rollback or isolation is stated for step 3. It replaces the logo, tokens, README header and every page of a live site, while the old Runestone assets are the only fallback, and the directory isn't a git repo here — Tag or branch the current design/sampo and site before the carry-through, an…
## Build vs reuse
Reuses: design/sampo/logo/build.py, which regenerates every logo SVG byte for byte and is tested by test_sampo_design. It also reuses design/sampo/tokens.json → site/build.py --tokens → style.css with its staleness check, site/stats.py for the real numbers, and T-2759's quality-bar tests (test_site_landing: hosts, reduced motion, no-JS, 320 px, contrast, design lint). The new parts are the directions themselves, which no existing generator makes at this level: fm looks and the directions skill make palettes and type, not animated marks and heroes.
