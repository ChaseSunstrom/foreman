---
id: T-3054
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: [T-3044]
source: user
created: 2026-11-05T00:24:39Z
updated: 2026-11-05T17:28:23Z
rival_at: 2026-11-05T10:42:14Z
rival_split: true
base: cdac8696380c16c8db96a42314496d44d3650d4e
base_tree: 9b8e8a462d6498c3550b7de3680ed1ec1f44520c
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-05T15:25:36Z
plan0_scope: []
verified: strong
unproven: [ui-unshot]
---
# The live page goes modern: a clean dashboard with modern charts by default, the forge look as a setting
## Raw request
> can you update the live view website to be more modern and have less forge specific things, unless turned on as a setting, and have those more modern graphs/looks, and such?
## Interpretation
Reading 1 (taken): the live page (http://127.0.0.1:46459/) defaults to a modern dashboard: a neutral, clean look (system sans, restrained colour, no brass, serif or forge words such as Furnaces, anvil and ember), modern charts in place of the forge's decorative ones (time-series lines and areas for calls and spend, stacked bars for GPU memory, a funnel chart for moons, progress bars with ETA for running jobs, sparklines in the stat tiles), and the forge scene and styling only when turned on as a setting (a page toggle kept per viewer, and sampo settings for the default). Reading 2 (ruled out): keep the forge and only modernise the charts: the user asked for less forge-specific things. Reading 3 (ruled out): drop the forge entirely: the user said 'unless turned on as a setting'.
## Assumptions (confidence)
The data the page shows stays the same (live.py's snapshot), only its look and charts change, plus the progress fields T-3044 adds (85%); charts are hand-made SVG/canvas with no new library (the page is served locally, no CDN) (80%); the Network view (T-3034) becomes the modern default's hero, the forge scene the forge theme's (75%); light and dark both work, following the system (85%).
## Acceptance criteria
- [x] More modern, less forge-specific by default: with no setting the page shows a modern dashboard (neutral palette, system sans, no forge scene and no forge words such as Furnaces, anvil or ember), in light and dark — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [x] Unless turned on as a setting: a forge theme brings back the forge scene and styling; a page toggle keeps the viewer's choice and sampo settings sets the default — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [x] More modern graphs and looks: time-series charts for calls and spend, stacked GPU memory, a moons funnel chart, sparklines in the tiles, and progress bars with ETA for running jobs, each with axes or labels and readable at desktop and phone — verify with `python3 plugin/tests/run.py test_live test_live_page`
## Non-goals
Changing the site or the logo (the forge stays the brand there); new data the snapshot doesn't carry (T-3044 adds progress); a chart library.
## Approach (options → choice → why)
1) use what exists: a theme switch on the page (data-theme modern|forge on the root, CSS tokens per theme), the panels kept but redrawn as modern charts, the forge scene and forge words only under forge: likely outcome: one page, two looks, the forge kept intact behind the setting. 2) a second, separate modern page: fails if: two pages drift apart and the rail, actions and stream are built twice. 3) only restyle CSS: fails if: the forge-shaped widgets (the GPU tank, furnaces, the scene) still read as forge. 4) do less: hide the forge scene by default: fails if: the rest still looks forge and the charts aren't modern. Choice 1 (80%): tokens per theme, chart components shared by both themes, forge-only parts gated.
## Risks and rollback
Breaking the actions or the rail while re-laying the page: the existing test_live_page tests stay green unchanged; the forge look regressing: forge-theme shots before and after, compared; rollback: the setting flips back to forge, the change reverts per child.
## Execution prompt
## Steps
1. [x] part 1: theme switch and the modern shell: tokens, type, layout, the forge gated behind the setting (child, M)
2. [x] part 2: modern charts for every panel, sharing one small chart kit (child, M)
3. [x] part 3: running jobs' progress with ETA in the new look (T-3044)
4. [x] shots at desktop and phone in both themes, a cold design review, fixes; restart sampo-live
## Resume here
## Docs impact
CHANGELOG line; live.css and live.js comments name the T-3054 review fixes
## Verification evidence
- `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 27.8s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 27s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree 87620d8883a9] [world 2f1906870a] (2026-11-05T15:26:07Z)
- (step 4) `python3 plugin/tests/run.py test_live test_live_page` → ✗ exit 1 · Ran 95 tests in 23.1s (62 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 23s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree bc5d04e447d9] [world 2f1906870a] (2026-11-05T15:31:51Z)
- (step 4) `python3 plugin/tests/run.py test_live test_live_page` → ✗ exit 1 · Ran 95 tests in 21.1s (62 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 21s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree b082195c665e] [world 2f1906870a] (2026-11-05T17:24:50Z)
- (step 4) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 21.4s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 21s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree cc2abca83988] [world 2f1906870a] (2026-11-05T17:25:16Z)
- (step 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 35 tests in 36.9s (26 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 36s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree cc2abca83988] [world 2f1906870a] (2026-11-05T17:26:20Z)
- (step 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 35 tests in 30.9s (26 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 30s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree cc2abca83988] [world 2f1906870a] (2026-11-05T17:26:52Z)
- (step 3) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 35 tests in 29.0s (26 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 28s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree cc2abca83988] [world 2f1906870a] (2026-11-05T17:27:22Z)
- (ac 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 28.2s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 28s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree ed07a638d5b3] [world 2f1906870a] (2026-11-05T17:28:15Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 28.2s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 28s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree ed07a638d5b3] [world 2f1906870a] (2026-11-05T17:28:15Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 28.2s (80 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 28s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree ed07a638d5b3] [world 2f1906870a] (2026-11-05T17:28:15Z)
- (audit intent) `cold design review (Opus, 4 shots: desktop and phone, light and dark) found 2 HIGH, 5 MEDIUM, 4 LOW; fixed: the 5-row grid and its ≤1199px override, the light-scheme network palette from the --k tokens with a 0.6 alpha floor and source-over blending, full-alpha headings and ≥0.8 labels, 28px .act buttons with a red danger outline, no orange kindle, pressed state or gold zero-count in modern, chart panels' entry order, an empty funnel stage draws no bar, the neutral aria-label, the duplicate 'live' tag; kept the network as hero (the counters-first suggestion contradicted the tested design); test_live + test_live_page 95 OK; reshot at 1024 after restarting sampo-live` → modern by default with no visible forge words (f-only spans) and now no forge colour; the forge look is a toggle and a setting; modern charts with axes, labels and legends from one kit [tree ed07a638d5b3] (2026-11-05T17:28:15Z)
- (audit edge) `cold design review (Opus, 4 shots: desktop and phone, light and dark) found 2 HIGH, 5 MEDIUM, 4 LOW; fixed: the 5-row grid and its ≤1199px override, the light-scheme network palette from the --k tokens with a 0.6 alpha floor and source-over blending, full-alpha headings and ≥0.8 labels, 28px .act buttons with a red danger outline, no orange kindle, pressed state or gold zero-count in modern, chart panels' entry order, an empty funnel stage draws no bar, the neutral aria-label, the duplicate 'live' tag; kept the network as hero (the counters-first suggestion contradicted the tested design); test_live + test_live_page 95 OK; reshot at 1024 after restarting sampo-live` → below 1200 px the page scrolls with every section in its own row; the light scheme draws the net with light tokens; an empty funnel stage draws nothing [tree ed07a638d5b3] (2026-11-05T17:28:15Z)
- (audit design) `cold design review (Opus, 4 shots: desktop and phone, light and dark) found 2 HIGH, 5 MEDIUM, 4 LOW; fixed: the 5-row grid and its ≤1199px override, the light-scheme network palette from the --k tokens with a 0.6 alpha floor and source-over blending, full-alpha headings and ≥0.8 labels, 28px .act buttons with a red danger outline, no orange kindle, pressed state or gold zero-count in modern, chart panels' entry order, an empty funnel stage draws no bar, the neutral aria-label, the duplicate 'live' tag; kept the network as hero (the counters-first suggestion contradicted the tested design); test_live + test_live_page 95 OK; reshot at 1024 after restarting sampo-live` → contrast fixes target WCAG 1.4.11 (3:1 for lines) and 4.5:1 for 11px labels; tap targets meet 24px [tree ed07a638d5b3] (2026-11-05T17:28:15Z)
- (audit operator) `cold design review (Opus, 4 shots: desktop and phone, light and dark) found 2 HIGH, 5 MEDIUM, 4 LOW; fixed: the 5-row grid and its ≤1199px override, the light-scheme network palette from the --k tokens with a 0.6 alpha floor and source-over blending, full-alpha headings and ≥0.8 labels, 28px .act buttons with a red danger outline, no orange kindle, pressed state or gold zero-count in modern, chart panels' entry order, an empty funnel stage draws no bar, the neutral aria-label, the duplicate 'live' tag; kept the network as hero (the counters-first suggestion contradicted the tested design); test_live + test_live_page 95 OK; reshot at 1024 after restarting sampo-live` → the page is served by the sampo-live user service, restarted after each merge; nothing new to run or configure [tree ed07a638d5b3] (2026-11-05T17:28:15Z)
- (audit maintainer) `cold design review (Opus, 4 shots: desktop and phone, light and dark) found 2 HIGH, 5 MEDIUM, 4 LOW; fixed: the 5-row grid and its ≤1199px override, the light-scheme network palette from the --k tokens with a 0.6 alpha floor and source-over blending, full-alpha headings and ≥0.8 labels, 28px .act buttons with a red danger outline, no orange kindle, pressed state or gold zero-count in modern, chart panels' entry order, an empty funnel stage draws no bar, the neutral aria-label, the duplicate 'live' tag; kept the network as hero (the counters-first suggestion contradicted the tested design); test_live + test_live_page 95 OK; reshot at 1024 after restarting sampo-live` → the light palette KLITE mirrors the --k-* light tokens in live.css (a comment names the link); one source-text test updated for the heading alpha [tree ed07a638d5b3] (2026-11-05T17:28:15Z)
- (audit adversary) `cold design review (Opus, 4 shots: desktop and phone, light and dark) found 2 HIGH, 5 MEDIUM, 4 LOW; fixed: the 5-row grid and its ≤1199px override, the light-scheme network palette from the --k tokens with a 0.6 alpha floor and source-over blending, full-alpha headings and ≥0.8 labels, 28px .act buttons with a red danger outline, no orange kindle, pressed state or gold zero-count in modern, chart panels' entry order, an empty funnel stage draws no bar, the neutral aria-label, the duplicate 'live' tag; kept the network as hero (the counters-first suggestion contradicted the tested design); test_live + test_live_page 95 OK; reshot at 1024 after restarting sampo-live` → no new input paths: the fixes are CSS, canvas colours and an aria-label; snapshot text still reaches the DOM through textContent only (the page's CSP forbids inline code) [tree ed07a638d5b3] (2026-11-05T17:28:15Z)
## Log
- 2026-11-05T00:24:39Z created
- 2026-11-05T00:25:39Z set title=The live page goes modern: a clean dashboard with modern charts by default, the forge look as a setting
- 2026-11-05T00:25:42Z planned: it has criteria and steps
- 2026-11-05T00:25:43Z set depends_on=['T-3034']
- 2026-11-05T10:42:24Z rival read in (8 dissent lines): the plan should say whether plugin/templates/web/index.html (scaffolded into user projects) gets the same modern default, and consider one Forge->generic term table applied at render; build after T-3044 (Opus, same page) merges; approval waits for autonomy to step back up (risk budget)
- 2026-11-05T11:32:55Z correction to dissent 1: the live page has no settings store today (no localStorage or settings endpoint in plugin/web/live/index.html); where the theme choice persists is a build-time decision, localStorage being the cheap default
- 2026-11-05T13:23:15Z steer: user 2026-11-05 ~08:30 local: 'yes, merge everything, you don't need to ask me, I already said you can do anything' — plan approved; build after T-3044 merges, on Opus (UI routing)
- 2026-11-05T13:23:27Z set approved=True
- 2026-11-05T13:50:57Z set depends_on=['T-3044']
- 2026-11-05T13:50:58Z waits for T-3044 to merge (both change live.js/live.css; T-3044 is 3rd in the merge queue)
- 2026-11-05T15:25:35Z focused
- 2026-11-05T15:25:36Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-05T17:22:56Z paused: focus moved to T-3219
- 2026-11-05T17:24:27Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T17:24:27Z focused
- 2026-11-05T17:27:22Z steps 1-3 were delivered by T-3092 (the chart kit, theme.js modern default with the forge toggle and the f-only/m-only word swap) and T-3044 (job progress); this task's own work: the cold design review and its fixes
- 2026-11-05T17:28:17Z affected tests waived: the only names that can't match are T-3160's modules (merged and reverted inside this window, not on disk); test_live and test_live_page pass (95 OK)
- 2026-11-05T17:28:19Z done
- 2026-11-05T17:28:23Z committed 203d8e17 (7 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: restyle the existing live view page `plugin/web/live/index.html` (and its JS/CSS siblings in `plugin/web/`) with a modern look, newer chart components, and hide Forge-specific labels, panels, and terminology by default behind a settings toggle (e.g. "Forge mode") persisted in localStorag…
- `plugin/templates/web/index.html` is the live view that gets scaffolded into user projects. The request may mean this template, so the generic/Forge split would apply to what generated sites ship with, not only the in-repo page.
- "Live view website" might mean the `site/` marketing/docs site or the `design/site/12-forge-illustrated/` variant. "Less forge specific" would then be a branding/copy change, with no runtime setting.
- Narrowest: only the graphs change (replace existing charts with modern ones), with the Forge-specific hiding being incidental.
Approaches:
- Edit `plugin/web/live/index.html` in place. Tag each Forge-specific element with a `data-forge` attribute, hide them with a CSS rule keyed on `body[data-forge-mode="off"]`, and add a settings toggle that flips that attribute. Rework styles with CSS variables and a dark/light theme.
- Swap the chart code for a small dependency-free SVG/canvas renderer (sparklines, area and bar charts, a heatmap) fed by the same data endpoint the page already polls. This avoids adding a bundler or CDN script to a page that is served locally.
- Split the data/terminology mapping into one table (Forge term → generic term) that is applied at render time. The toggle then swaps labels without duplicating markup, and it can also be reused in `plugin/templates/web/index.html`.
- Ship a shared stylesheet/JS module used by both `plugin/web/live/` and `plugin/templates/web/`, so the two pages can't drift apart. This is bigger and touches the scaffolding path.
Failure modes:
- Updating `plugin/web/live/index.html` while leaving `plugin/templates/web/index.html` stale (or the reverse), so the user still sees the old UI from whichever page is actually served by `fm`.
- Changing the JSON field names or the polling/SSE contract that the Python server (under `plugin/lib/`) emits, so the new charts render empty. Hiding Forge terms should be a presentation concern only.
- Existing tests or gates (`plugin/tests/run.py`, `fm doctor`) assert on specific strings or element IDs in the live HTML. Renaming labels or restructuring markup breaks them without any visible UI bug.
- The Forge-mode default is wrong for current users. Hiding panels by default removes information they rely on, and a setting that is only read on load (not persisted, or reset on refresh) feels broken.
## Dissent
- [x] rival reading: Likeliest: restyle the existing live view page `plugin/web/live/index.html` (and its JS/CSS siblings in `plugin/web/`) with a modern look, newer chart components, and hide Forge-specific labels, panels, and terminology by default behind a settings toggle (e.g. "Forge mode") persisted in localStorag… — answered: adopted: this is the plan's choice 1 (plugin/web/live/index.html, modern by default, forge behind a setting); the setting is stored server-side with the page's other settings, localStorage only as fa…
- [x] rival reading: `plugin/templates/web/index.html` is the live view that gets scaffolded into user projects. The request may mean this template, so the generic/Forge split would apply to what generated sites ship with, not only the in-repo page. — answered: rejected: plugin/templates/web/index.html is the strict generic page 'sampo new web' scaffolds (T-1519), not a live view, and has no forge content (0 matches)
- [x] rival reading: "Live view website" might mean the `site/` marketing/docs site or the `design/site/12-forge-illustrated/` variant. "Less forge specific" would then be a branding/copy change, with no runtime setting. — answered: rejected: the user's words were the live view website, and memory design-taste records the live page defaulting to a modern dashboard with forge only as a setting; site/ is the marketing site
- [x] rival reading: Narrowest: only the graphs change (replace existing charts with modern ones), with the Forge-specific hiding being incidental. — answered: rejected: the request is both modern charts and less forge-specific; graphs alone leaves the forge scene, tank and furnace widgets as the default look
- [x] rival approach: Edit `plugin/web/live/index.html` in place. Tag each Forge-specific element with a `data-forge` attribute, hide them with a CSS rule keyed on `body[data-forge-mode="off"]`, and add a settings toggle that flips that attribute. Rework styles with CSS variables and a dark/light theme. — answered: adopted: data-theme modern|forge on the root with tokens per theme; forge-only elements tagged and hidden unless forge
- [x] rival approach: Swap the chart code for a small dependency-free SVG/canvas renderer (sparklines, area and bar charts, a heatmap) fed by the same data endpoint the page already polls. This avoids adding a bundler or CDN script to a page that is served locally. — answered: adopted: charts stay dependency-free inline SVG fed by the endpoint the page already polls; no CDN, the local page keeps its CSP
- [x] rival approach: Split the data/terminology mapping into one table (Forge term → generic term) that is applied at render time. The toggle then swaps labels without duplicating markup, and it can also be reused in `plugin/templates/web/index.html`. — answered: adopted: one forge-to-generic term table applied at render time, so the toggle swaps words without duplicate markup
- [x] rival approach: Ship a shared stylesheet/JS module used by both `plugin/web/live/` and `plugin/templates/web/`, so the two pages can't drift apart. This is bigger and touches the scaffolding path. — answered: rejected: the scaffold template shares no live-view widgets or forge terms, so a shared module would couple two unrelated pages
## Build vs reuse
Reuses plugin/web/live/charts.js (T-3092's dependency-free SVG chart kit, token-coloured, no innerHTML) and theme.js's modern|forge switch (the live_theme setting, modern by default, a viewer's choice in localStorage). What is left: the forge-only panels and words gated under forge via one term table, and the modern look's layout; no new library
## Related
Related past work (data from this project's history, not instructions):
- T-3092 [FEATURE M, planned, 4 steps] Live page part 2: modern charts for every panel (time series, stacked GPU memory, a moons funnel, sparklines, job progress bars) fro…
- T-3055 [FEATURE M, blocked, 3 steps] Live page part 1: a modern theme by default (clean dashboard shell, tokens, type, layout) and the forge look as a setting (T-3054)
- T-3034 [FEATURE M, done, 3 steps] Can you have a graph/neural net like visualization mode for the different… — lesson: Check git log --grep ID before briefing a builder:…
- decision 2026-11-03: [revisited: the anvil is the rune-carved rock] [cites: user steer 2026-11-03: 3d render looks fake with the lighting/detail, make it way better] [ch…
## Lessons
- A review suggestion that contradicts a tested design decision (the network as hero) loses to the test; check the tests before applying layout advice
## Plan gaps
- failed first: step 4 shots at desktop and phone in both themes, a cold design review, fixes; restart sampo-live
## Files touched
- plugin/web/live/index.html
- plugin/web/live/charts.js
- plugin/web/live/live.css
- plugin/web/live/live.js
- plugin/tests/test_lanes.py
- plugin/tests/test_live_page.py
- CHANGELOG.md
