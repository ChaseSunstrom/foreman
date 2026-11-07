---
id: T-3245
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: [T-3247, T-3248, T-3163]
source: user
created: 2026-11-05T21:05:47Z
updated: 2026-11-06T00:00:13Z
rival_at: 2026-11-05T21:10:04Z
rival_split: true
---
# Completely update the README to the Sampo look with the charts and such; turn every…
## Raw request
> Completely update the README to the Sampo look with the charts and such; turn every table (and table-like block) into a picture too; re-record the Claude example video with the CC mod's look (user ask 2026-11-05: can you completely update the readme to match the Sampo look with the charts and such? and for all tables and such, turn them into pictures too, and re-record the claude example video with the mod look and stuff)
## Interpretation
Reading 1 (chosen): the README becomes a Sampo page: the crest header, every pipe table drawn as a themed picture (light and dark), real-data charts in the live page's modern style, the three diagrams redrawn in the same look and saying Sampo (they still say Foreman), and the Claude example (demo/live.*) re-recorded with today's CC mod (the crest, T-3163's row kinds). Text stays readable: each picture has alt text naming its content and the table's text sits in a collapsed details block for search and screen readers. Reading 2 (ruled out): one big landing image instead of text; rejected, the README must stay searchable, accessible and diffable.
## Assumptions (confidence)
## Acceptance criteria
- [ ] README.md has no pipe tables left: each is a <picture> with a dark and a light SVG drawn by demo/readme_figures.py from its data, with alt text naming its content and the table's text in a collapsed details block; every figure passes sampo works check — verify with `python3 plugin/tests/run.py test_readme`
- [ ] at least four charts from real data (tests in the suite, tasks closed per day, merge time after T-3141, models bench or moons kept and cards written), dated, in the live page's modern chart style — verify with `python3 plugin/tests/run.py test_readme`
- [ ] the Sampo look: the live page's and mod's colour tokens, the crest header, and the loop, guard and architecture diagrams redrawn so none says Foreman — verify with `python3 plugin/tests/run.py test_readme`
- [ ] python3 demo/readme_figures.py --check exits 0 when every figure is current and 1 naming the stale ones — verify with `python3 demo/readme_figures.py --check`
- [ ] demo/live.cast, .svg and .mp4 re-recorded with today's CC mod (after T-3163 merges) and the README's video and caption updated — verify with `python3 plugin/tests/run.py test_readme`
## Non-goals
No animation inside README images (GitHub doesn't run it in <img> beyond SMIL, and motion distracts in a README); the site's pages are out of scope.
## Approach (options → choice → why)
1) use what exists: a generator beside demo/record.py (demo/readme_figures.py) draws each README table and chart as an SVG in the live page's and mod's tokens, light and dark (a GitHub <picture> pair), from the table's own data kept in the script and from real data for the charts (sampo stats, the ledger, research/models/bench.jsonl, moons and cards counts); sampo works check gates every figure (contrast, safe, size); likely outcome: a README that looks like Sampo and stays current, since one command redraws it.
2) hand-draw each figure once (Opus, static SVGs): fails if: the numbers go stale and every edit means redrawing by hand.
3) screenshot HTML tables to PNG through headless Chrome: fails if: PNGs are heavy, blur on high-DPI screens and can't follow the reader's theme.
4) do less: restyle the Markdown and keep the tables: fails if: the user asked for the tables as pictures and for charts.
Choice 1 (80%): generated, themed, gated SVGs; the hand-made diagrams (loop, guard, architecture) are redrawn in the same tokens and say Sampo.
Build vs reuse: reuse the live page's colour tokens (live.css, its modern theme), the crest header (design/sampo/logo), charts.js's chart shapes, sampo works check for the gates, demo/record_live.py and mods/foreman-ui/tools/shot.py for the video; no new dependency.
## Risks and rollback
GitHub renders SVG inside <img> only (no scripts, no external fonts): figures use system fonts and inline styles, checked by sampo works check. A figure's numbers go stale: --check fails when a regenerated figure differs. The video costs a real model turn (sonnet, a few minutes) and must wait for T-3163 to merge. Rollback: git revert of the README commit; the figures are new files.
## Execution prompt
## Steps
1. [ ] failing tests: no pipe tables, every figure exists in both themes and passes works check, no diagram says Foreman, --check  <- CURRENT
2. [ ] the generator and the table figures
3. [ ] the charts from real data
4. [ ] the diagrams and the header in the Sampo look
5. [ ] the README rewritten around the figures; shots of it in light and dark reviewed
6. [ ] re-record the Claude example with the current mod (after T-3163 merges)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T21:05:47Z created
- 2026-11-05T21:09:38Z planned: it has criteria and steps
- 2026-11-05T21:10:16Z set approved=True
- 2026-11-05T21:10:16Z approved: L plans are user-approved ('I approve all changes btw', 2026-10-30)
- 2026-11-06T00:00:12Z set depends_on=['T-3247', 'T-3248', 'T-3163']
- 2026-11-06T00:00:13Z split: steps 1-3 are T-3247 (generator, tables, charts; in review), step 4 is T-3248 (diagrams, builder), step 6 waits for T-3163 (builder); steps 5-6 stay here once those merge
## Follow-ups captured
## Build vs reuse
Reuses the live page's colour tokens (site/live.css modern theme), the crest header (design/sampo/logo), charts.js's chart shapes, sampo works check for every figure, demo/record_live.py and mods/foreman-ui/tools/shot.py for the video; a new demo/readme_figures.py beside demo/record.py; no new dependency.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: restyle README.md to match the Sampo design system.** "Sampo look" is the visual language in `design/sampo/index.html` and `plugin/lib/sampo/`. The README gets a hero banner, section headers and chart images (rendered SVG/PNG, committed under something like `docs/img/`). Every markdown…
- **Narrower: visual refresh only.** Same README content and structure, with new images swapped in for tables. Video is a separate follow-up.
- **"Sampo look" means the site, not the design system.** The target would be `design/site/12-forge-illustrated/index.html` or `site/`, with the README mirroring the landing page rather than `design/sampo`.
- **"Charts" means real data.** The charts would be generated from `bench/` and `plugin/tests/bench_hooks.py` output, not decorative. That makes the README a rendered view of measured numbers.
Approaches:
- **Generate images from a script.** A new script (e.g. `design/sampo/render_readme.py`) parses README tables and bench output, emits Sampo-styled SVGs, and rasterizes them. README then references the images and keeps an `<details>` or alt-text fallback. Pro: re-runnable when numbers change. Check fi…
- **Screenshot Sampo HTML.** Build table and chart components in `design/sampo/index.html` and headless-screenshot them (Playwright or Chromium) to PNG. Pro: guaranteed to match the look. Con: fonts, theme and size depend on the environment.
- **Re-record the video from a scripted session.** Use `demo/` (check what recorder it uses, e.g. vhs or asciinema) with the `mods/foreman-ui` mod installed, driven by a fixed tape script. Export as GIF/MP4 and link it from the README. Verify `claude plugin test mods/foreman-ui` passes first.
- **Hand-author the README in one pass, then image-ify.** Rewrite prose and structure first, then extract each table to an image. This keeps the narrative review separate from asset generation, but leaves assets that go stale.
Failure modes:
- **Tables as images lose text.** Search, copy, screen readers and diffs all break. A table image whose source data isn't kept next to it (alt text, a collapsed text version, or a source `.md`/`.json`) will drift from the code. `CHANGELOG.md` and `MASTER.md` are heavily edited, so any tables copied f…
- **Charts show invented or stale numbers.** If they're not produced from `plugin/tests/bench_hooks.py --runs 20` or `bench/` output, they misstate performance. Charts that look good but are not reproducible would be a correctness problem for a README.
- **Video can't be recorded in this sandbox.** There is no git repo here and the working directory is a runtime path (`/run/user/1000/fm-children-1000`). The recorder, a real Claude session or the `foreman-ui` mod may not be available or may need auth. Fabricating a mockup and calling it a "recording…
- **Images render differently on GitHub.** GitHub's dark and light themes, relative paths and SVG sanitizing (external fonts are stripped) can break the look. Transparent PNGs also vanish on dark mode. The rendered README must be checked in both themes, and the images need to be committed alongside i…
## Dissent
- [x] rival reading: **Likeliest: restyle README.md to match the Sampo design system.** "Sampo look" is the visual language in `design/sampo/index.html` and `plugin/lib/sampo/`. The README gets a hero banner, section headers and chart images (rendered SVG/PNG, committed under something like `docs/img/`). Every markdown… — answered: adopted: the figures take design/sampo's tokens (the design system) with the live page's modern chart style; the README gets the crest hero and section headers
- [x] rival reading: **Narrower: visual refresh only.** Same README content and structure, with new images swapped in for tables. Video is a separate follow-up. — answered: rejected: the user asked to completely update it and re-record the video
- [x] rival reading: **"Sampo look" means the site, not the design system.** The target would be `design/site/12-forge-illustrated/index.html` or `site/`, with the README mirroring the landing page rather than `design/sampo`. — answered: rejected for the figures: the user's design-taste note says the live page defaults to the modern dashboard and the forge is a setting; the header keeps the crest from design/sampo/logo
- [x] rival reading: **"Charts" means real data.** The charts would be generated from `bench/` and `plugin/tests/bench_hooks.py` output, not decorative. That makes the README a rendered view of measured numbers. — answered: adopted: charts are measured numbers; bench_hooks output joins the sources
- [x] rival approach: **Generate images from a script.** A new script (e.g. `design/sampo/render_readme.py`) parses README tables and bench output, emits Sampo-styled SVGs, and rasterizes them. README then references the images and keeps an `<details>` or alt-text fallback. Pro: re-runnable when numbers change. Check fi… — answered: adopted, as option 1, but kept SVG (not rasterized) so each figure follows the reader's theme
- [x] rival approach: **Screenshot Sampo HTML.** Build table and chart components in `design/sampo/index.html` and headless-screenshot them (Playwright or Chromium) to PNG. Pro: guaranteed to match the look. Con: fonts, theme and size depend on the environment. — answered: rejected: screenshots depend on the machine's fonts and size and can't follow the theme (option 3)
- [x] rival approach: **Re-record the video from a scripted session.** Use `demo/` (check what recorder it uses, e.g. vhs or asciinema) with the `mods/foreman-ui` mod installed, driven by a fixed tape script. Export as GIF/MP4 and link it from the README. Verify `claude plugin test mods/foreman-ui` passes first. — answered: adopted: demo/record_live.py already drives a scripted request through Claude Code with the mod in shot.py's tmux harness and writes cast, svg and mp4
- [x] rival approach: **Hand-author the README in one pass, then image-ify.** Rewrite prose and structure first, then extract each table to an image. This keeps the narrative review separate from asset generation, but leaves assets that go stale. — answered: rejected: hand-drawn assets go stale; the prose rewrite is step 5, after the generator
