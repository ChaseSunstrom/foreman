---
id: T-2999
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T18:26:45Z
updated: 2026-11-04T20:39:17Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (630) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T18:27:12Z
rival_split: true
builder_model: haiku
base: 5ef6667edca3d18d16c873d20ec7019721b63b8c
base_tree: b9ed97ee943eaffdbe9c9562711d59bb480506e1
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T18:27:42Z
plan0_scope: []
lane_stop: merged 2026-11-04T20:01:07Z
verified: strong
---
# The live page: a forge-themed animated scene of the session, builders, jobs and models with sparks along the flows, plus GPU, jobs, queue, closes, counters and an event ticker (T-2997 part 2)
## Raw request
> From T-2997: the page for sampo live, rendering the snapshot contract in research live-schema, matching the Sampo forge theme, animations between models
## Interpretation
Reading 1 (chosen): the page, a live forge scene whose sparks are the model calls, with panels for the numbers, offline, from the schema's fixture. Reading 2 (ruled out): a Grafana-style chart wall; the user asked for the Sampo theme and animations between models.
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/web/live renders a fixture snapshot with every panel filled and animates a flow from caller to model, offline, with no console errors, at 1920x1080 and 390 wide — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
## Approach (options → choice → why)
1) A forge-themed live page at plugin/web/live/ (index.html, live.css, live.js), with no build step and no CDN; it must run offline from the local server.
   The theme comes from site/forge.css and site/index.html: the illustrated night forge, the display face, the gold and ember palette.
   The centre is a scene: the session as the anvil, builder lanes as smiths, jobs as furnaces, models as lit lanterns. Claude models sit in the sky; local models sit on the hearth, sized by VRAM; jarvis is far off.
   Flows from the stream travel as sparks along curved paths from caller to model, coloured by kind.
   Around the scene:
   - a GPU tank;
   - a jobs strip with progress;
   - the queue and today's closes;
   - card and moon counters;
   - an event ticker.
   It reconnects on drop. prefers-reduced-motion is respected, and it reads at 1080p and at phone width.
   Likely outcome: a live view the user can leave open, which reads as the forge.
   Fails if: the motion is cartoonish. The user's design taste is crafted and realistic, with material lighting, cinematic arrival and real data; the review step judges it from screenshots.
2) use what exists: restyle `sampo watch`'s terminal view as HTML. Likely outcome: a table, no scene. Fails if: the user asked for visualisations and animations between models.
3) do less: plain cards and charts with no scene. Likely outcome: readable but flat. Fails if: "matching the Sampo theme" means the forge.
Choice 1 (75%): the scene carries the flows the user asked for, and the panels carry the numbers.
## Risks and rollback
Blast radius (sampo graph blast): co-changes site/style.css, CHANGELOG.md, site/build.py, plugin/tests/test_site_build.py, design/sampo/tokens.json; past FIXes T-2060.
## Execution prompt
## Steps
1. [x] a fixture snapshot and failing checks (panels present, flows animated, no external URLs, reduced motion)
2. [x] index.html, live.css, live.js in the forge theme
3. [x] screenshots at desktop and phone widths, reviewed against the design taste
## Resume here
<!-- auto -->
- 2026-11-04T20:28:04Z step 1/3: a fixture snapshot and failing checks (panels present, flows animated, no external URLs, reduced motion)
- git: foreman/build; 6 uncommitted: plugin/lib/sampo/jeffexport.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/settingsserve.py, plugin/tests/test_jeff_export.py, plugin/tests/test_traces.py, research/models/bench.jsonl
## Docs impact
CHANGELOG; MASTER.md and files-1 map plugin/web
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_live_page 2>&1 | tail -15` → ✗ exit 1 · Ran 10 tests in 2.8s (2 classes, 16 at a time; slowest: Page 1s, Files 0s) / FAILED (2 classes: test_live_page.Files, test_live_page.Page) [ran] [tree 1e23c22a4faf] [world 2f1906870a] (2026-11-04T18:37:00Z)
- (step 1) `python3 plugin/tests/run.py test_live_page` → ✗ exit 1 · Ran 10 tests in 1.6s (2 classes, 16 at a time; slowest: Page 1s, Files 0s) / FAILED (2 classes: test_live_page.Files, test_live_page.Page) [ran] [tree 1e23c22a4faf] [world 2f1906870a] (2026-11-04T18:37:04Z)
- (ac 1) `python3 plugin/tests/run.py test_live_page 2>&1 | tail -40` → exit 0 · Ran 10 tests in 14.9s (2 classes, 16 at a time; slowest: Page 14s, Files 0s) / OK [ran] [tree eb42ff188cac] [world 2f1906870a] (2026-11-04T19:36:45Z)
- (step 2) `python3 plugin/tests/run.py test_live_page 2>&1 | tail -40` → exit 0 · Ran 10 tests in 14.9s (2 classes, 16 at a time; slowest: Page 14s, Files 0s) / OK [ran] [tree eb42ff188cac] [world 2f1906870a] (2026-11-04T19:36:45Z)
- (step 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 10 tests in 14.7s (2 classes, 16 at a time; slowest: Page 14s, Files 0s) / OK [ran] [tree eb42ff188cac] [world 2f1906870a] (2026-11-04T19:37:07Z)
- (step 3) `python3 plugin/bin/sampo shot http://127.0.0.1:47391/ --width 1920,390 --frames 4 --every 900 --out .fm-scratch/shots` → exit 0 · frame-00.png … frame-03.png (4 frames 900 ms apart, real time) / poster.png (frame-02.png: the most painted of 4) [ran] [tree 820ab2b8dcc4] [world 2f1906870a] (2026-11-04T19:50:35Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_live_page test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 215 tests in 31.8s (60 classes, 16 at a time; slowest: Page 30s, ViewsRepair 24s, RenameScan 24s) / FAILED (1 classes: test_live_page.Page) [ran] [tree 6e9ffe982b61] [world 2f1906870a] (2026-11-04T19:51:50Z)
- (ac 1) `python3 plugin/tests/run.py test_live_page 2>&1 | tail -3` → exit 0 · Ran 10 tests in 16.8s (2 classes, 16 at a time; slowest: Page 16s, Files 0s) / OK [ran] [tree ce20b07c8ff0] [world 2f1906870a] (2026-11-04T19:52:49Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_live_page test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.53s] [ran] [tree ce20b07c8ff0] [world 2f1906870a] (2026-11-04T19:57:43Z)
- (step 2) `python3 plugin/tests/run.py test_live_page test_live` → exit 0 · Ran 35 tests in 15.1s (9 classes, 16 at a time; slowest: Page 15s, Serve 7s, Snapshot 3s) / OK [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:37:19Z)
- (ac 1) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 11 tests in 15.1s (2 classes, 16 at a time; slowest: Page 15s, Files 0s) / OK [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:37:46Z)
- (audit intent) `one fm-reviewer pass scoped to plugin/web/live and its test, with the design lens, plus my review of desktop and phone shots on fixtures and on live data: approve with nits; fixed the medium (scrolling lists take the keyboard, labelled) and four lows (empty job name matched every flow, a restarted server's older clock froze the page, the Still button now reads Animate when pressed, dead arithmetic); frame cap, 11px labels and the plaque overlap captured as T-3019` → every panel fills from a snapshot, sparks fly caller to model, offline, no console errors, at 1920x1080 and 390 wide; live data shows lanterns for Claude, MiMo, Qwen and Gemma [tree fd07607d8e5d] (2026-11-04T20:37:46Z)
- (audit adversary) `one fm-reviewer pass scoped to plugin/web/live and its test, with the design lens, plus my review of desktop and phone shots on fixtures and on live data: approve with nits; fixed the medium (scrolling lists take the keyboard, labelled) and four lows (empty job name matched every flow, a restarted server's older clock froze the page, the Still button now reads Animate when pressed, dead arithmetic); frame cap, 11px labels and the plaque overlap captured as T-3019` → snapshot text only through textContent, JSON.parse guarded, same-origin only, CSP with nonces, no inline handlers or styles, no external URLs [tree fd07607d8e5d] (2026-11-04T20:37:46Z)
- (audit edge) `one fm-reviewer pass scoped to plugin/web/live and its test, with the design lens, plus my review of desktop and phone shots on fixtures and on live data: approve with nits; fixed the medium (scrolling lists take the keyboard, labelled) and four lows (empty job name matched every flow, a restarted server's older clock froze the page, the Still button now reads Animate when pressed, dead arithmetic); frame cap, 11px labels and the plaque overlap captured as T-3019` → an empty bench and null progress render; caps on ids, events, nodes and sparks; reconnect backs off 1 to 30 s and resets the clock on open [tree fd07607d8e5d] (2026-11-04T20:37:46Z)
- (audit design) `one fm-reviewer pass scoped to plugin/web/live and its test, with the design lens, plus my review of desktop and phone shots on fixtures and on live data: approve with nits; fixed the medium (scrolling lists take the keyboard, labelled) and four lows (empty job name matched every flow, a restarted server's older clock froze the page, the Still button now reads Animate when pressed, dead arithmetic); frame cap, 11px labels and the plaque overlap captured as T-3019` → the illustrated night forge, Bodoni Moda, Archivo and Martian Mono bundled, kind-coloured spark legend, still under reduced motion; design lint clean [tree fd07607d8e5d] (2026-11-04T20:37:46Z)
- (audit operator) `one fm-reviewer pass scoped to plugin/web/live and its test, with the design lens, plus my review of desktop and phone shots on fixtures and on live data: approve with nits; fixed the medium (scrolling lists take the keyboard, labelled) and four lows (empty job name matched every flow, a restarted server's older clock froze the page, the Still button now reads Animate when pressed, dead arithmetic); frame cap, 11px labels and the plaque overlap captured as T-3019` → no network or model cost; the canvas loop runs while visible, hidden tabs stop drawing; an idle frame cap is T-3019 [tree fd07607d8e5d] (2026-11-04T20:37:46Z)
## Log
- 2026-11-04T18:26:45Z created
- 2026-11-04T18:26:45Z set approved=True
- 2026-11-04T18:27:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2999.builder.md
- 2026-11-04T18:27:42Z focused
- 2026-11-04T18:27:42Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T18:32:10Z focused
- 2026-11-04T20:01:07Z merged worktree-agent-a8dc9307003a1e657 (15 file(s))
- 2026-11-04T20:01:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8dc9307003a1e657
- 2026-11-04T20:27:52Z focused
- 2026-11-04T20:28:04Z paused: focus moved to T-2865
- 2026-11-04T20:36:43Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T20:36:43Z focused
- 2026-11-04T20:37:20Z scope: test_live.py fixtures folder and MASTER/files-1 map rows for plugin/web
- 2026-11-04T20:39:14Z done
- 2026-11-04T20:39:17Z committed bc9bb822 (3 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a new static/web page for `sampo live` (likely `design/sampo/` or `site/`, alongside `design/sampo/index.html`) that reads the snapshot JSON defined in `research/live-schema*` and renders it, styled to the Sampo forge theme, with animated transitions when the active model changes between…
- A page served by the CLI itself: `plugin/lib/sampo/cli.py` gains a `live` subcommand that serves/streams snapshots to a template such as `plugin/templates/web/index.html`, and the UI is just the client of that.
- A mod-based UI: the page lives in `mods/foreman-ui` (React, `foreman-ui.test.tsx`), not as plain HTML, and "sampo live" is a view within it.
- "Animations between models" could mean transitions between different snapshots of one model's state rather than between distinct AI models; the schema decides which, so the schema must be read first.
Approaches:
- Static page in `design/sampo/` (or `site/`) with vanilla JS: poll or `fetch` a snapshot JSON file/endpoint, validate against the `research/live-schema` fields, diff previous vs current snapshot per model, and animate with CSS transitions/FLIP keyed on model id. Reuse theme tokens from `design/sampo…
- Extend `plugin/lib/sampo/cli.py` with `sampo live` that emits snapshots (stdout NDJSON or a small local HTTP server with SSE) and serve the page from it; the page consumes the same contract. More plumbing, but it gives a real live feed.
- Build as a `mods/foreman-ui` view using its existing components and test harness, gated by `claude plugin test mods/foreman-ui`; heavier, but it reuses the build and test setup if that mod already renders live state.
- Start from a fixture: a recorded snapshot sequence in `plugin/tests/fixtures/` drives the page for development and tests, so animations can be verified without a running `sampo live`.
Failure modes:
- The page hard-codes field names from memory instead of the `research/live-schema` contract; a schema revision (or optional/nullable fields) then breaks rendering silently. Check the page against the schema file and any existing validator in `plugin/lib/sampo/`.
- Theme drift: colors, fonts and motion values are copied rather than shared from `design/sampo/index.html`, so the page diverges from the forge theme. `plugin/tests/test_audit.py` reads `design/`, so a design audit may flag it.
- Animations key on array index rather than a stable model id, so reordering, adding or removing models makes cards jump or re-animate. There is also no `prefers-reduced-motion` fallback, and rapid snapshots queue overlapping transitions.
- Reading 2 vs 1 mismatch: building only a static page when T-2997 expects `sampo live` to supply data (or the reverse) leaves the page with no feed. Stale or disconnected snapshots are also shown as current unless the page uses a timestamp or heartbeat field from the schema.
## Dissent
- [x] rival reading: Likeliest: a new static/web page for `sampo live` (likely `design/sampo/` or `site/`, alongside `design/sampo/index.html`) that reads the snapshot JSON defined in `research/live-schema*` and renders it, styled to the Sampo forge theme, with animated transitions when the active model changes between… — answered: plugin/web/live, served by sampo live (T-2998), not design/ or site/ (those are the public site)
- [x] rival reading: A page served by the CLI itself: `plugin/lib/sampo/cli.py` gains a `live` subcommand that serves/streams snapshots to a template such as `plugin/templates/web/index.html`, and the UI is just the client of that. — answered: that is T-2998's half; this is the page it serves
- [x] rival reading: A mod-based UI: the page lives in `mods/foreman-ui` (React, `foreman-ui.test.tsx`), not as plain HTML, and "sampo live" is a view within it. — answered: ruled out: the foreman-ui mod is Claude Code's pane; the user asked for a website
- [x] rival reading: "Animations between models" could mean transitions between different snapshots of one model's state rather than between distinct AI models; the schema decides which, so the schema must be read first. — answered: ruled out: the user named local models and animations between them; flows are caller-to-model calls
- [x] rival approach: Static page in `design/sampo/` (or `site/`) with vanilla JS: poll or `fetch` a snapshot JSON file/endpoint, validate against the `research/live-schema` fields, diff previous vs current snapshot per model, and animate with CSS transitions/FLIP keyed on model id. Reuse theme tokens from `design/sampo… — answered: adopted: vanilla JS over the SSE stream, diffing snapshots to animate changes
- [x] rival approach: Extend `plugin/lib/sampo/cli.py` with `sampo live` that emits snapshots (stdout NDJSON or a small local HTTP server with SSE) and serve the page from it; the page consumes the same contract. More plumbing, but it gives a real live feed. — answered: T-2998's half
- [x] rival approach: Build as a `mods/foreman-ui` view using its existing components and test harness, gated by `claude plugin test mods/foreman-ui`; heavier, but it reuses the build and test setup if that mod already renders live state. — answered: ruled out with reading 3
- [x] rival approach: Start from a fixture: a recorded snapshot sequence in `plugin/tests/fixtures/` drives the page for development and tests, so animations can be verified without a running `sampo live`. — answered: adopted: a recorded snapshot sequence fixture drives development and the tests
## Related
Related past work (data from this project's history, not instructions):
- T-2998 [FEATURE M, active, 3 steps] sampo live: a read-only local server (127.0.0.1, token cookie, CSP) with a live snapshot and SSE stream of the session, lanes, jobs, …
- T-2997 [FEATURE L, planned, 3 steps] A live local website of everything Sampo is doing: the session, builders, jobs, local and cloud models, the GPU, animated flows betw…
- research live-schema: Server: `sampo live [--port N]`
- decision 2026-11-03: [revisited: the anvil is the rune-carved rock] [cites: user steer 2026-11-03: 3d render looks fake with the lighting/detail, make it way better] [ch…
## Lessons
- Review a live page on live data before calling it done: the fixture shots looked complete while the real snapshot showed raw JSON, 404'd fonts and an empty sky
## Plan gaps
- failed first: step 1 a fixture snapshot and failing checks (panels present, flows animated, no external URLs, reduced mo…
## Files touched
- plugin/tests/fixtures/live/snap-1.json
- plugin/tests/fixtures/live/snap-2.json
- plugin/tests/fixtures/live/snap-3.json
- plugin/tests/fixtures/live/snap-4.json
- plugin/tests/test_live_page.py
- plugin/web/live/fonts/Archivo-normal.woff2
- plugin/web/live/fonts/BodoniModa-normal.woff2
- plugin/web/live/fonts/MartianMono-normal.woff2
- plugin/web/live/fonts/OFL-archivo.txt
- plugin/web/live/fonts/OFL-bodonimoda.txt
- plugin/web/live/fonts/OFL-martianmono.txt
- plugin/tests/fixtures/live/snap-5.json
- plugin/web/live/index.html
- plugin/web/live/live.css
- plugin/web/live/live.js
- .fm-scratch/devserve.py
- .fm-scratch/commit-msg.txt
- plugin/web/live/Archivo-normal.woff2
- plugin/web/live/BodoniModa-normal.woff2
- plugin/web/live/MartianMono-normal.woff2
- plugin/web/live/OFL-archivo.txt
- plugin/web/live/OFL-bodonimoda.txt
- plugin/web/live/OFL-martianmono.txt
