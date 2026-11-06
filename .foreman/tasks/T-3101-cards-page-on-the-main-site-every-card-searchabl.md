---
id: T-3101
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:05:32Z
updated: 2026-11-05T11:55:26Z
builder_model: haiku
base: 649c130fd5512e2b371e1ec37198dca24c3ba6e4
base_tree: 946756ed98ad467484520834dd9e75a8aeb7b3c0
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-05T06:43:23Z
plan0_scope: []
builder_returned: 2026-11-05T08:01:18Z
lane_stop: merged 2026-11-05T11:45:50Z
verified: strong
unproven: [docs]
---
# Cards page on the main site: every card, searchable and filterable by grid cell, with a permalink per card (T-3100 part 1)
## Raw request
> Cards page on the main site: every card, searchable and filterable by grid cell, with a permalink per card (T-3100 part 1)
## Interpretation
Reading 1 (chosen): the site build exports the card store as a small search index (id, grid, cell, title, when) plus per-grid body shards, written only when changed, and site/cards.html loads them: search, grid tabs, facet filters with counts, cards that open in place to steps, commands, example, check and traps, #K-000123 permalinks, both themes, phone width; the nav links it. Reading 2: embed every card in one page as the private artifact does; rejected, at 30,000 cards one page is tens of megabytes.
## Assumptions (confidence)
## Acceptance criteria
- [x] site/build.py writes site/cards/index.json (id, grid, cell, title, when per card) and one body shard per grid, only when their content changes, from the card store; a build with an empty store writes an empty index and the page says so — verify with `python3 plugin/tests/run.py test_site_build`
- [x] site/cards.html searches titles, when lines and commands, filters by grid and each cell field with counts, opens a card in place, keeps a #K-id permalink, and is linked from the site nav; it reads in light and dark and at 390 px with no page scroll sideways — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: port the artifact's page (scratchpad cards/template.html) into site/pages.py's page frame and the site tokens, data from smallcards.rows() at build; likely outcome: the page ships on today's 5,031 cards and scales by shard. 2. Do less: a static list of titles; fails if: nobody can read a card's steps. 3. A server-side search on the live page only; fails if: the main site is static and must stand alone. Choice 1 (80%)
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, plugin/tests/test_site.py, MASTER.md, README.md, site/build.py; past FIXes T-2061, T-2064, T-2960.
## Execution prompt
## Steps
1. [x] failing tests: export shape and write-if-changed, empty store, nav link, permalink, the page's filters
2. [x] the export in build.py and the page in pages.py (ported from the artifact)
3. [x] shots in both themes, desktop and phone
## Resume here
<!-- auto -->
- 2026-11-05T07:39:44Z step 1/3: failing tests: export shape and write-if-changed, empty store, nav link, permalink, the page's filters
- git: worktree-agent-ad1db1057a05b4694; 3 uncommitted: plugin/tests/test_site_build.py, site/build.py, site/cards.js
- touched since last checkpoint: site/build.py, plugin/tests/test_site_build.py, site/cards.js
## Docs impact
site nav gains Cards; docs/map/files-lib-2.md names the export; CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -15` → ✗ exit 1 · Ran 18 tests in 6.0s (12 classes, 16 at a time; slowest: Landing 4s, Reproducible 2s, TitleCard 2s) / FAILED (2 classes: test_site_build.CardsPage, test_site_build.CardsExport) [ran] [tree 4ffef946dc93] [world 2f1906870a] (2026-11-05T06:50:56Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -15` → ✗ exit 1 · Ran 18 tests in 6.0s (12 classes, 16 at a time; slowest: Landing 4s, Reproducible 2s, TitleCard 2s) / FAILED (2 classes: test_site_build.CardsPage, test_site_build.CardsExport) [ran] [tree 4ffef946dc93] [world 2f1906870a] (2026-11-05T06:50:56Z)
- (step 1) `python3 plugin/tests/run.py test_site_build` → ✗ exit 1 · Ran 18 tests in 3.2s (12 classes, 16 at a time; slowest: Landing 3s, Reproducible 1s, TitleCard 1s) / FAILED (2 classes: test_site_build.CardsPage, test_site_build.CardsExport) [ran] [tree 4ffef946dc93] [world 2f1906870a] (2026-11-05T06:54:33Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -40` → ✗ exit 1 · Ran 23 tests in 11.3s (12 classes, 16 at a time; slowest: CardsPage 10s, Landing 5s, Reproducible 3s) / FAILED (1 classes: test_site_build.CardsExport) [ran] [tree 73d58935e372] [world 2f1906870a] (2026-11-05T07:04:05Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -40` → ✗ exit 1 · Ran 23 tests in 11.3s (12 classes, 16 at a time; slowest: CardsPage 10s, Landing 5s, Reproducible 3s) / FAILED (1 classes: test_site_build.CardsExport) [ran] [tree 73d58935e372] [world 2f1906870a] (2026-11-05T07:04:05Z)
- (step 2) `python3 plugin/tests/run.py test_site_build test_small_cards 2>&1 | tail -15` → exit 0 · Ran 43 tests in 9.8s (16 classes, 16 at a time; slowest: CardsPage 9s, Landing 3s, Reproducible 1s) / OK [ran] [tree 99e6971467cd] [world 2f1906870a] (2026-11-05T07:05:23Z)
- (step 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 23 tests in 10.3s (12 classes, 16 at a time; slowest: CardsPage 10s, Landing 2s, Reproducible 1s) / OK [ran] [tree 99e6971467cd] [world 2f1906870a] (2026-11-05T07:06:26Z)
- (step 3) `python3 plugin/tests/run.py test_site_build test_small_cards 2>&1 | tail -3` → exit 0 · Ran 43 tests in 11.0s (16 classes, 16 at a time; slowest: CardsPage 10s, Landing 4s, Reproducible 3s) / OK [ran] [tree ebc9009d9d8b] [world 2f1906870a] (2026-11-05T07:12:09Z)
- (step 3) `sampo shot --width 1280,390 --scheme both --frames 1 --out .fm-scratch/shots3 http://127.0.0.1:8731/cards.html` → exit 0 · viewport.png / frame-00.png (1 frames 250 ms apart, real time) [ran] [tree ebc9009d9d8b] [world 2f1906870a] (2026-11-05T07:13:55Z)
- (step 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 23 tests in 9.8s (12 classes, 16 at a time; slowest: CardsPage 9s, Landing 4s, Reproducible 3s) / OK [ran] [tree beb19a071583] [world 2f1906870a] (2026-11-05T07:16:00Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1060 tests in 69.1s (222 classes, 16 at a time; slowest: Ship 69s, GenesisRead 35s, GenerationReview 33s) / FAILED (3 classes: test_genesis.GenesisExport, test_site_sections.Built, test_design_lin [ran] [tree beb19a071583] [world 2f1906870a] (2026-11-05T07:17:11Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [16.57s] [ran] [tree 9db20831f88e] [world 2f1906870a] (2026-11-05T07:19:31Z)
- (step 3) `sampo shot --width 1280,390 --scheme both --frames 1 --out .fm-scratch/shots4 http://127.0.0.1:8731/cards.html#K-000002` → exit 0 · frame-00.png (1 frames 250 ms apart, real time) / note: still loading after 30 s; taken as it stood [ran] [tree 9db20831f88e] [world 2f1906870a] (2026-11-05T07:21:09Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -30` → ✗ exit 1 · Ran 24 tests in 12.3s (12 classes, 16 at a time; slowest: CardsPage 11s, Landing 6s, Reproducible 4s) / FAILED (1 classes: test_site_build.CardsExport) [ran] [tree 88d0f6bac91d] [world 2f1906870a] (2026-11-05T07:30:46Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -30` → ✗ exit 1 · Ran 24 tests in 12.3s (12 classes, 16 at a time; slowest: CardsPage 11s, Landing 6s, Reproducible 4s) / FAILED (1 classes: test_site_build.CardsExport) [ran] [tree 88d0f6bac91d] [world 2f1906870a] (2026-11-05T07:30:46Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -6` → exit 0 · Ran 25 tests in 12.9s (12 classes, 16 at a time; slowest: CardsPage 13s, Landing 2s, Reproducible 1s) / OK [ran] [tree 2137e59719b2] [world 2f1906870a] (2026-11-05T07:43:54Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -6` → exit 0 · Ran 25 tests in 12.9s (12 classes, 16 at a time; slowest: CardsPage 13s, Landing 2s, Reproducible 1s) / OK [ran] [tree 2137e59719b2] [world 2f1906870a] (2026-11-05T07:43:54Z)
- (step 2) `python3 plugin/tests/run.py test_site_build test_genesis test_small_cards test_site_sections test_design_lint` → exit 0 · Ran 318 tests in 44.1s (50 classes, 16 at a time; slowest: GenesisRead 39s, GenerationReview 38s, GenesisCheck 35s) / OK [ran] [tree 7b060415ec3e] [world 2f1906870a] (2026-11-05T07:44:58Z)
- (step 3) `sampo shot --width 1280,390 --scheme both --frames 1 --out .fm-scratch/shots5 http://127.0.0.1:8731/cards.html` → exit 0 · viewport.png / frame-00.png (1 frames 250 ms apart, real time) [ran] [tree 7b060415ec3e] [world 2f1906870a] (2026-11-05T07:45:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_gates test_design_lint test_design_sprint test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_fmpy test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_map test_mcp test_models test_moons_scale test_moonshot test_motion_verify test_parallel test_proof test_rename_scan test_replay test_sampo_design test_scaffold test_session_fixes test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_snapshots test_steer test_suite_hygiene test_taste_ledger test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [32.18s] [ran] [tree 7b060415ec3e] [world 2f1906870a] (2026-11-05T08:00:56Z)
- (step 1) `python3 plugin/tests/run.py test_site_build test_genesis` → exit 0 · Ran 244 tests in 19.2s (36 jobs, 16 at a time; slowest: GenerationReview 19s, GenesisRead 16s, GenesisCheck 14s) / OK [ran] [tree db0898411c4f] [world 2f1906870a] (2026-11-05T11:46:19Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 25 tests in 12.7s (12 jobs, 16 at a time; slowest: CardsPage 12s, Landing 4s, Reproducible 2s) / OK [ran] [tree d396b2f87759] [world 2f1906870a] (2026-11-05T11:47:29Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 25 tests in 12.7s (12 jobs, 16 at a time; slowest: CardsPage 12s, Landing 4s, Reproducible 2s) / OK [ran] [tree d396b2f87759] [world 2f1906870a] (2026-11-05T11:47:29Z)
- (audit intent) `re-ran test_site_build + test_genesis on main after the merge (244 OK); read export_cards: manifest + id-ordered pages + per-grid body blocks, write-if-changed, stale files removed only from the names the last export listed` → AC1 met with paging (index.json is now a 2 KB manifest over index.<n>.json pages, a deliberate change for tens of thousands of cards); AC2's light, dark and 390 px shots taken in the lane (step 3) [tree d396b2f87759] (2026-11-05T11:47:29Z)
- (audit adversary) `re-ran test_site_build + test_genesis on main after the merge (244 OK); read export_cards: manifest + id-ordered pages + per-grid body blocks, write-if-changed, stale files removed only from the names the last export listed` → card text is model-written, so untrusted: every card field reaches the DOM through textContent (cards.js has no innerHTML/insertAdjacentHTML/outerHTML); fetch URLs are base + a manifest name + .json on the same origin, the ?v= pinned to 1-16 hex; the #K-id hash is used undecoded, so a malformed escape can't throw; links are '#'+id only [tree d396b2f87759] (2026-11-05T11:47:29Z)
- (audit edge) `re-ran test_site_build + test_genesis on main after the merge (244 OK); read export_cards: manifest + id-ordered pages + per-grid body blocks, write-if-changed, stale files removed only from the names the last export listed` → an empty store writes an empty manifest and the page says so (tested); duplicate ids keep the first; a grid outside CARD_GRIDS gets its fields from its own cells; a stalled fetch aborts with a message [tree d396b2f87759] (2026-11-05T11:47:29Z)
- (audit operator) `re-ran test_site_build + test_genesis on main after the merge (244 OK); read export_cards: manifest + id-ordered pages + per-grid body blocks, write-if-changed, stale files removed only from the names the last export listed` → the export is committed with the site: 6.8 MB for 5,031 cards (25 files); ids only grow, so a day's new cards rewrite the manifest, the last page and the last block per grid, not the rest; at tens of thousands of cards it is tens of MB in git [tree d396b2f87759] (2026-11-05T11:47:29Z)
## Log
- 2026-11-05T03:05:32Z created
- 2026-11-05T03:06:17Z set approved=True
- 2026-11-05T03:08:32Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-05T05:46:52Z unblocked
- 2026-11-05T05:46:58Z blocked: approved; host load 30.9 on 16 CPUs refuses new lanes; brief it when load eases
- 2026-11-05T06:43:04Z unblocked
- 2026-11-05T06:43:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3101.builder.md
- 2026-11-05T06:43:22Z focused
- 2026-11-05T06:43:23Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-05T11:45:50Z merged worktree-agent-ad1db1057a05b4694 (36 file(s))
- 2026-11-05T11:45:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad1db1057a05b4694
- 2026-11-05T11:45:58Z focused
- 2026-11-05T11:46:53Z scope: rune.py (publish re-exports the card store daily) and smallcards.home (the store path the export reads) are part of keeping the page current
- 2026-11-05T11:55:22Z done
- 2026-11-05T11:55:26Z committed bef0b797 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-2909 [FEATURE M, done, 5 steps] Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage …
- T-2903 [FIX M, blocked, 2 steps] One shared nav for the landing, the tower and the section pages, with Install and GitHub back on the tower
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar finished tasks took 5–5 steps
## Lessons
- A generated export committed to git must change only the files its new rows touch: order by an id that only grows and block by it
## Plan gaps
- failed first: step 1 failing tests: export shape and write-if-changed, empty store, nav link, permalink, the page's filt…
## Files touched
- plugin/tests/test_site_build.py
- site/build.py
- site/pages.py
- site/cards.js
- .fm-scratch/js-bare.json
- site/sections.css
- site/index.html
- site/cards/general-1.json
- site/cards/general-2.json
- site/cards/general-3.json
- site/cards/general-4.json
- site/cards/general-5.json
- site/cards/general-6.json
- site/cards/general-7.json
- site/cards/general-8.json
- site/cards/index.json
- site/cards/ui-1.json
- site/cards/ui-10.json
- site/cards/ui-11.json
- site/cards/ui-12.json
- site/cards/ui-13.json
- site/cards/ui-2.json
- site/cards/ui-3.json
- site/cards/ui-4.json
- site/cards/ui-5.json
- site/cards/ui-6.json
- site/cards/ui-7.json
- site/cards/ui-8.json
- site/cards/ui-9.json
- .fm-scratch/probe_store.py
