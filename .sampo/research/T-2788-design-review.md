# Ship review: Sampo site (landing, Rune tower, features/code, features/proof)

Verdict: SHIP WITH FIXES. The landing is faithful to the converged forge and the hard bar holds. One High on the tower page (rules grid broken at desktop widths), plus 4 Medium and 5 Low. Built with `python3 site/build.py <dir>` (positional target, no --out flag), served on 127.0.0.1:8765, Chromium headless, 6.5 s settle.

Counts: High 1, Medium 4, Low 5.

Hard-bar results (32 page/width/theme combinations, 320/390/768/1440, light+dark):
- Horizontal overflow: none anywhere (scrollWidth == innerWidth in all 32).
- Console: 0 errors/pageerrors. One WebGL "GPU stall due to ReadPixels" perf warning, landing 1440 light only (headless GL driver, ignore).
- Outside hosts: none. 4xx responses: none (tower's ../style.css resolves).
- No JS: every section is present and readable when scrolled (figure fallbacks work). A full_page screenshot looks empty below the fold only because of `content-visibility:auto` (forge.css:30), not missing content.
- Reduced motion: hero and tower hold clean stills (t6-landing-0.png, t6-tower-0.png); no ghost trails.
- Contrast (computed on text with solid backgrounds): all pass except the two items under L1.
Screenshots are in /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/shipreview/ (sc-* scroll series, t2..t6-*, landing-*-top.png). Filenames below are relative to that folder.

## High

H1. Tower, rules grid collapses at width >= 820 (checked 1024 and 1440; fine at 390). Page: genesis/index.html, dark (light same DOM).
- Files: t2-rules-1440.png, sc-tower-1440-dark-13.png.
- What: the intent and run rules ("Spikes, not vetoes", "Louhi holds out", "Subtract as you add", "Everything finished", ...) show a title only. Body text is pushed out of view, the title touches the card's left edge (computed padding is `22px 0`), long titles clip ("Two new tries, then move c"), card heights are uneven, and the grid uses only 744 px of the 1296 px column, leaving the right half empty.
- Cause: the tower still loads `../style.css`, whose `.rules > div { display:grid; padding:22px 0 }` and `@media (min-width:820px){ .rules > div { grid-template-columns:280px 1fr } }` (site/style.css:328-332) override genesis.css `.rule` (genesis.css:241). The 280 px title column swallows the 241 px card.
- Fix: in site/genesis/genesis.css add `.rules>.rule{display:block;grid-template-columns:none;padding:14px 16px 15px;border-bottom:0}` and `.rules{border-top:0;max-width:none}` (or rename the tower container so the site rule cannot match). Spec R-v ("uneven holes") is a milder symptom of the same clash.

## Medium

M1. Landing hero, 1440x900, both themes: hero sits about 90 px lower than the spec.
- Files: landing-1440-dark-top.png vs spec hero-1440.png; landing-1440-light-top.png vs hero-1440-light.png.
- What: eyebrow at y=199 (spec 108) and it wraps to two lines ("...CODING / AGENTS"); the headline, body and install box shift down, so the "Into the forge / Strike the anvil" CTAs fall below the fold (spec shows them at y=823). The shipped nav has two extra items (Features, Benchmarks), which is fine.
- Fix: forge.css hero block: cut top padding by about 90 px and give the eyebrow `white-space:nowrap` or a wider text column.

M2. Landing hero: hammer motion trail is clipped by a hard horizontal edge (dark 1440, dark 768, light 1440).
- Files: sc-landing-768-dark-00.png (ghost polygon with a flat top at y=403), landing-1440-dark-top.png (flat-top ghost at ~y=277), landing-1440-light-top.png (pale ghost slab at x=1090-1220, y=277-370).
- What: the swing's blur plate is cut by the art layer's top bound, so a translucent slab with a straight top edge floats near the hammer; in light it reads as a pale box. Absent in reduced motion.
- Fix: extend the hero canvas/svg `.lay` upper bound (negative top inset) or fade the trail to 0 before it reaches the clip (site/forge.js trail draw, forge.css `.lay`).

M3. Landing at 768, Smith section: content is not centred.
- File: sc-landing-768-dark-04.png.
- What: the session box and the "Many hands, one Smith" card end at x=658 while the header and hero use the 38-730 gutters, leaving a 110 px dead right margin against 38 px on the left.
- Fix: forge.css single-column `.sec` rules between 640-900 px: let `.term` and the card use `width:100%`/`max-width:none`.

M4. Feature pages (code, proof) do not carry the forge: flat, different type system, no art.
- Files: t4-code-1440-light-0.png, t4-proof-1440-dark-0.png.
- What: Noto Serif display and a sidebar layout with no sky, ember or illustration, against the landing's high-contrast display face and night sky. They read as a different site; the tower also uses Noto Serif, so the display face differs between the landing and everything else.
- Fix (smallest): load the landing's display face and sky background in site/style.css (`--display`, `body`, `.top`); one hero figure per section page is the larger option.

## Low

L1. Two AA contrast misses, features/code.html, light theme, all widths.
- `.chip.pass` ("PASS", 12.75 px): `#e2e6f1` on `#1f7a45` = 4.28:1 (need 4.5). Darken bg to `#1a6e3d` or use white text.
- `.plus` ("+25", "+4", 17 px, 9 instances): `#1f7a45` on the light card = 4.28:1. Darken to `#1a6e3d` in site/style.css `.plus`.

L2. Tower moons table (1440, dark): "5 of 5" wraps to two lines in the WILD column and the TIER header wraps to three lines. File sc-tower-1440-dark-05.png. Fix: `white-space:nowrap` on the wild cell, shorter header.

L3. Tower header is narrower than its content: brand at x=160 and theme button ends x=1280 while content spans 72-1368 (landing header spans 72-1368). Files sc-tower-1440-dark-00.png vs sc-landing-1440-dark-01.png. Fix: match the `.top` inner max-width in genesis.css to the page column.

L4. features/code.html: the command box clips its text at the right edge with no wrap or scroll ("...an item with qty" cut, t5-a.png). Fix: `white-space:pre-wrap` or `overflow-x:auto` on that block. Also in the pipeline diagram "type, size, checks, steps" touches the Plan slot box edge (t4-code-1440-light-0.png).

L5. Landing 390 dark: the "How the pieces fit" diagram renders at about 5 px text, unreadable on a phone (sc-landing-390-dark-14.png). Fix: let it scroll horizontally at natural size on phones. features/code case cards also leave a 470 px empty left column below the terminal image on desktop (t4-code-1440-light-2.png): make the image sticky or place the text beside it.

## Spec Lows still present (already in _review/final.md)
L-z plain hill and flagstones (the quench's hill is a black mass, sc-landing-1440-dark-05.png), L-bb green blobs in the quench reflection, L-cc smooth knoll on the Moons chart, L-dd soft vertical figure sides by day. R-v is subsumed by H1 and is worse than the spec describes.

Not covered: every combination was not viewed (tower light at 768/390/320 and code/proof at 768 were measured for overflow, errors and contrast only, not looked at).

## Fixed (T-2964)

H1, M1, M2, M3 and L1-L5 fixed in the files the review traced (site/genesis/genesis.css .rules>.rule; forge.css hero padding and eyebrow; the smear canvas bound; single-column .sec widths; the two greens; the moons table header; the tower header width; the command box wrap; the diagram scroll at 390). Shots in the scratchpad's shipreview/fixed/. M4 (the feature pages carrying the forge) is T-2965.

## The design rounds before it

Critique 7 on the design itself converged: nothing above Low on the landing (6 Low) or the tower (1 Low); directions-v2/12-forge-illustrated/_review/final.md.
