---
id: T-3047
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T00:08:40Z
updated: 2026-11-05T05:49:38Z
builder_model: haiku
inferred_deps: [T-3042, T-3046]
inferred_why: T-3042: named in its request; T-3046: part 3 exports the survivors that part 2 counts
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T00:10:15Z
plan0_scope: []
lane_stop: merged 2026-11-05T05:24:12Z
base: 9bb63c17fb770e1f5c44063ed82b088c495eb852
base_tree: 7f73260ca146d4278c7cde3124c98493b5c3f87e
verified: strong
unproven: [ui-unshot]
---
# Every kept moon used: export all survivors, the Moons page lists them, promotion draws from all (T-3042 part 3)
## Raw request
> Every kept moon used: export all survivors, the Moons page lists them, promotion draws from all (T-3042 part 3)
## Interpretation
Reading 1 (taken): every kept moon is used: exported whole (not the top 200 families), browsable on the site's Moons page, and drawn on by genesis's moonshot promotion in turn. Reading 2 (ruled out): each of the 10,000 is built or kill-tested: not feasible; the climb takes the best and every one is queued for a draw.
## Assumptions (confidence)
## Acceptance criteria
- [x] Export writes every kept moon to a catalogue file beside genesis.json, not a top slice — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] The site's Moons page lists every kept moon with search and filters (grid, tier, family), paged — verify with `python3 plugin/tests/run.py test_moons_scale test_genesis`
- [x] Promotion draws from every kept moon, family leads first by tier and wildness, then variants, each draw recorded so none is drawn twice — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1) a catalogue file beside genesis.json plus a paged, searchable page: likely outcome: the tower page stays fast, every moon reachable. 2) all moons inside genesis.json: fails if: a 15 MB genesis.json slows every tower load. 3) a page reading candidates.jsonl directly: fails if: rejected rows leak and families are lost. 4) use what exists: export() and the site's Moons section, extended; promote() with a drawn event: likely outcome: small diff. 5) do less: raise EXPORT_TOP to 10,000 families only: fails if: variants inside families stay hidden and nothing is drawn. Choice 1 (80%): built through 4.
## Risks and rollback
## Execution prompt
The parent's brief holds the live data, the design and the measured numbers: read its Execution prompt first (state/projects/foreman-4a056f/tasks/T-3042-and-with-the-10000-moons-thing-i-want-it-to-lite.md). Stores stay append-only (candidates.jsonl, funnel.jsonl are never rewritten; a fate is a row's last event). Never print LLM_API_KEY (models.secret() reads it). Work test-first in plugin/tests/test_moons_scale.py; run python3 plugin/tests/run.py test_moons_scale before each commit. Part 3 = the parent's item (5): export every survivor to moons/catalogue.json (id, title, today, with_this, what, kill, tier, wild, family, grid, cell), the site's Moons page (find it: grep the site builder for moons_scale) pages and searches it with filters for grid, tier and family and stays fast with 10,000 rows, promote draws from every survivor with a drawn event so none is drawn twice. The grid field may be absent on old rows (treat as 'user').
## Steps
1. [x] export every survivor (tests first)
2. [x] the Moons page lists them (tests first)
3. [x] promotion draws from all, recorded (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T05:39:01Z steps 3/3 done
- git: foreman/build; 2 uncommitted: CHANGELOG.md, scripts/
- touched since last checkpoint: CHANGELOG.md
## Docs impact
site Moons page and CHANGELOG; no user docs name the export's top slice
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -25` → ✗ exit 1 · Ran 55 tests in 35.1s (13 classes, 16 at a time; slowest: StoreLock 35s, Funnel 3s, Grow 2s) / FAILED (1 classes: test_moons_scale.Catalogue) [ran] [tree 2de13099e254] [world 2f1906870a] (2026-11-05T00:14:00Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -25` → ✗ exit 1 · Ran 55 tests in 35.1s (13 classes, 16 at a time; slowest: StoreLock 35s, Funnel 3s, Grow 2s) / FAILED (1 classes: test_moons_scale.Catalogue) [ran] [tree 2de13099e254] [world 2f1906870a] (2026-11-05T00:14:00Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -8` → exit 0 · Ran 55 tests in 9.0s (13 classes, 16 at a time; slowest: StoreLock 8s, Funnel 5s, Grow 4s) / OK [ran] [tree 278625dcf297] [world 2f1906870a] (2026-11-05T00:14:12Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -8` → exit 0 · Ran 55 tests in 9.0s (13 classes, 16 at a time; slowest: StoreLock 8s, Funnel 5s, Grow 4s) / OK [ran] [tree 278625dcf297] [world 2f1906870a] (2026-11-05T00:14:12Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -8` → exit 0 · Ran 55 tests in 9.0s (13 classes, 16 at a time; slowest: StoreLock 8s, Funnel 5s, Grow 4s) / OK [ran] [tree 278625dcf297] [world 2f1906870a] (2026-11-05T00:14:12Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale test_genesis 2>&1 | tail -8` → exit 0 · Ran 273 tests in 58.0s (37 classes, 16 at a time; slowest: GenerationReview 53s, GenesisRead 52s, GenesisCheck 49s) / OK [ran] [tree fbf9418614d4] [world 2f1906870a] (2026-11-05T00:16:47Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_genesis 2>&1 | tail -8` → exit 0 · Ran 273 tests in 58.0s (37 classes, 16 at a time; slowest: GenerationReview 53s, GenesisRead 52s, GenesisCheck 49s) / OK [ran] [tree fbf9418614d4] [world 2f1906870a] (2026-11-05T00:16:47Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 55 tests in 5.2s (13 classes, 16 at a time; slowest: StoreLock 5s, Funnel 3s, Grow 2s) / OK [ran] [tree 66564df5d261] [world 2f1906870a] (2026-11-05T00:22:45Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_genesis` → exit 0 · Ran 273 tests in 39.6s (37 classes, 16 at a time; slowest: GenesisRead 38s, GenerationReview 33s, GenesisCheck 32s) / OK [ran] [tree 66564df5d261] [world 2f1906870a] (2026-11-05T00:23:25Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 55 tests in 7.9s (13 classes, 16 at a time; slowest: Funnel 6s, StoreLock 6s, Route 6s) / OK [ran] [tree 66564df5d261] [world 2f1906870a] (2026-11-05T00:24:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1016 tests in 80.3s (215 classes, 16 at a time; slowest: Ship 80s, GenesisRead 44s, GenerationReview 35s) / FAILED (1 classes: test_design_lint.Site) [ran] [tree 66564df5d261] [world 2f1906870a] (2026-11-05T00:27:32Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [20.34s] [ran] [tree 2152f66a43e1] [world 2f1906870a] (2026-11-05T00:29:50Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [23.69s] [ran] [tree 80c86166bbb4] [world 2f1906870a] (2026-11-05T00:35:32Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 59 tests in 4.6s (13 classes, 16 at a time; slowest: Funnel 4s, Grow 3s, Cli 3s) / FAILED (1 classes: test_moons_scale.Promote) [ran] [tree 337de3ec4cf0] [world 2f1906870a] (2026-11-05T00:47:05Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 59 tests in 4.6s (13 classes, 16 at a time; slowest: Funnel 4s, Grow 3s, Cli 3s) / FAILED (1 classes: test_moons_scale.Promote) [ran] [tree 337de3ec4cf0] [world 2f1906870a] (2026-11-05T00:47:05Z)
- (step 1) `node plugin/tests/genesis_page.js site/genesis catalogue` → exit 0 · {"total":true,"markup":false,"rows":50,"index_first":true,"search":true,"grid":true,"user":true,"tier":true,"tier_shard":true,"scroll":true,"family":true,"page":true,"famclick":true,"page_of":true,"em [ran] [tree 23b472e7b382] [world 2f1906870a] (2026-11-05T00:55:20Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_genesis` → exit 0 · Ran 278 tests in 32.8s (37 classes, 16 at a time; slowest: GenesisRead 29s, GenerationReview 27s, GenesisCheck 26s) / OK [ran] [tree 23b472e7b382] [world 2f1906870a] (2026-11-05T00:55:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [14.86s] [ran] [tree 23b472e7b382] [world 2f1906870a] (2026-11-05T00:58:31Z)
- `python3 plugin/tests/run.py test_moons_scale test_genesis` → exit 0 · Ran 306 tests in 32.7s (40 classes, 16 at a time; slowest: GenesisRead 27s, GenerationReview 27s, GenesisCheck 24s) / OK [ran] [tree 4761a60076dc] [world 2f1906870a] (2026-11-05T05:37:45Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 88 tests in 7.4s (16 classes, 16 at a time; slowest: Yield 7s, KeepGrow 6s, Funnel 6s) / OK [ran] [tree 32f3d5ce9393] [world 2f1906870a] (2026-11-05T05:43:50Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale test_genesis` → exit 0 · Ran 306 tests in 38.0s (40 classes, 16 at a time; slowest: GenesisRead 32s, GenerationReview 31s, GenesisCheck 28s) / OK [ran] [tree 32f3d5ce9393] [world 2f1906870a] (2026-11-05T05:43:50Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 88 tests in 7.4s (16 classes, 16 at a time; slowest: Yield 7s, KeepGrow 6s, Funnel 6s) / OK [ran] [tree 32f3d5ce9393] [world 2f1906870a] (2026-11-05T05:43:50Z)
- (audit intent) `builder lane reviewed before merge; merged d09ccf18 with a moonscale conflict resolved earlier; criteria re-run on main green (306 tests)` → the ask was 10,000 moons kept AND used: export, the page and promotion now all read every survivor, not a top slice [tree 32f3d5ce9393] (2026-11-05T05:43:50Z)
- (audit adversary) `builder lane reviewed before merge; merged d09ccf18 with a moonscale conflict resolved earlier; criteria re-run on main green (306 tests)` → the page fetches its own same-origin catalogue file with a timeout and renders moon text with textContent only (a test asserts the render body has no innerHTML), so a moon's text can't inject markup; a bad status or JSON falls to the page's error state [tree 32f3d5ce9393] (2026-11-05T05:43:50Z)
- (audit edge) `builder lane reviewed before merge; merged d09ccf18 with a moonscale conflict resolved earlier; criteria re-run on main green (306 tests)` → an empty catalogue renders the page's empty state; a second promotion run skips every moon already drawn [tree 32f3d5ce9393] (2026-11-05T05:43:50Z)
- `sampo shot site/genesis/index.html` → exit 0 · frame-00.png … frame-04.png (5 frames 250 ms apart, real time) / no poster: the page held still [ran] [tree 32f3d5ce9393] [world 2f1906870a] (2026-11-05T05:48:05Z)
- `sampo shot http://127.0.0.1:8797/genesis/index.html#moons-all --frames 2 --every 4000` → exit 0 · frame-00.png … frame-01.png (2 frames 4000 ms apart, real time) / poster.png (frame-01.png: the most painted of 2) [ran] [tree 9030f718dbed] [world 2f1906870a] (2026-11-05T05:49:31Z)
## Log
- 2026-11-05T00:08:40Z created
- 2026-11-05T00:09:20Z set approved=True
- 2026-11-05T00:09:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3047.builder.md
- 2026-11-05T00:10:14Z focused
- 2026-11-05T00:10:15Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T01:16:09Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0bbc49830437af1d (branch worktree-agent-a0bbc49830437af1d kept: not merged)
- 2026-11-05T05:19:19Z lane: ~/.claude/foreman.lanes/T-3047 on foreman/T-3047
- 2026-11-05T05:24:12Z merged worktree-agent-a0bbc49830437af1d (8 file(s))
- 2026-11-05T05:24:12Z lane removed: ~/.claude/foreman.lanes/T-3047 (branch foreman/T-3047 kept: not merged)
- 2026-11-05T05:37:08Z focused
- 2026-11-05T05:47:31Z done
- 2026-11-05T05:47:33Z committed 88bb651d (1 file)
- 2026-11-05T05:49:31Z ui proof: the page renders with the fresh export (moons-catalogue.json + 001 shard, 321 kept); the shot shows the hero, the catalogue section's rendering is proved by test_genesis's genesis_page.js run (search, filters, paging, textContent only)
- 2026-11-05T05:49:38Z committed 732c3ca6 (53 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-3042 [FEATURE L, planned, 4 steps] 10,000 moons kept and used, and moons on anything related to Sampo
- T-2869 [FEATURE M, done, 2 steps] Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI embe…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- similar finished tasks took 2–5 steps
## Lessons
- Kept work is only kept once something reads it: a top slice exported 2% of the survivors for weeks
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- .fm-scratch/e.json
- .fm-scratch/e2.json
- plugin/lib/sampo/rune.py
- plugin/tests/genesis_page.js
- site/genesis/index.html
- site/genesis/genesis.css
- site/genesis/genesis.js
- plugin/tests/test_genesis.py
- .fm-scratch/render.js
- .fm-scratch/cat.css
- .fm-scratch/t1.json
- .fm-scratch/m1.json
- .fm-scratch/m2.json
- .fm-scratch/t2.json
- .fm-scratch/t3.json
- .fm-scratch/r1.json
- .fm-scratch/t4.json
- .fm-scratch/j1.json
- .fm-scratch/c1.json
- .fm-scratch/n1.json
- .fm-scratch/n2.json
- .fm-scratch/n3.json
- .fm-scratch/n4.json
- CHANGELOG.md
