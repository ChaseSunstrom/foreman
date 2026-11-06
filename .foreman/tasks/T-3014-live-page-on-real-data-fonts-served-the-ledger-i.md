---
id: T-3014
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T20:02:29Z
updated: 2026-11-04T20:27:44Z
base_note: Calibration: this plan states Choice 75% where FIX M closes (130) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T20:04:56Z
rival_split: true
base: 802fd5b8ec6af852a3e310766afb83ea19b33a23
base_tree: 0af09401ddb307c91a29504e9dae2f1487817daf
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-04T20:05:42Z
plan0_scope: []
verified: strong
unproven: [docs]
---
# Live page on real data: fonts served, the ledger in words, every model call animated (local, Jarvis, Smith)
## Raw request
> Live page on real data: fonts served, the ledger in words, every model call animated (local, Jarvis, Smith)
## Interpretation
Reading 1 (chosen): the page as built is right; what the live data shows is thin and rough: fonts fall back, the ledger prints JSON, local and remote model calls never reach the scene. Reading 2 (ruled out): redesign the scene for sparse data; the fixture shot shows the design holds when calls are visible.
## Assumptions (confidence)
## Acceptance criteria
- [x] the live server serves the page's woff2 fonts as font/woff2 bytes and still 404s names outside the page folder — verify with `python3 plugin/tests/run.py test_live`
- [x] models.complete appends one capped row per call (time, model or remote profile, caller) and the live snapshot's models and flows include those calls, so a Smith exam run on Jarvis and a local card writer show as lanterns with sparks — verify with `python3 plugin/tests/run.py test_live test_models`
- [x] the ledger ticker reads in words (T-2995 edited test_traces.py; T-2999 step 3 evidence) instead of raw JSON — verify with `python3 plugin/tests/run.py test_live test_live_page`
## Non-goals
## Approach (options → choice → why)
1) A call log in models.complete (state/calls.jsonl: ts, to, caller; to is the model for a local endpoint, the profile name for a remote one; rotated to one .1 file past 4 MB), read by live._calls with a caller-to-kind map; _static serves bytes; events rendered as words server-side (task + verb + the payload's file basename, step, cmd head). Likely outcome: every local and remote call animates, fonts load, the ticker reads cleanly; about 10k rows a day at ~150 B, 1.5 MB, so one rotation file bounds it. Fails if: the append slows the hot path; it is one open-append-close per call, small next to a model call's 100 ms+.
2) use what exists: read Smith journals (state/code/*.jsonl) and the ledger's cards/moons events for calls. Likely outcome: Smith calls appear only for the main project's runs; exam runs use a temp FOREMAN_HOME so they never show, and the local card writer has no per-call row. Fails if: most local traffic is exam and grow, which it is today.
3) do less: fix fonts and the ticker only. Likely outcome: a cleaner page that still shows a quiet sky while Jarvis and the GPU work. Fails if: the user asked to see the models and the animations between them.
Choice 1 (75%): the only way every caller shows, at a bounded cost.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fonts: _static serves binary types
2. [x] a call log in models.complete, read by live._calls and models
3. [x] events in words; restart the live server and screenshot it
## Resume here
## Docs impact
CHANGELOG and docs/map/files-lib-2.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 31 tests in 16.6s (9 classes, 16 at a time; slowest: Page 15s, Serve 9s, Snapshot 5s) / OK [ran] [tree 0af09401ddb3] [world 2f1906870a] (2026-11-04T20:11:18Z)
- (step 2) `python3 plugin/tests/run.py test_live test_models` → exit 0 · Ran 111 tests in 15.4s (23 classes, 16 at a time; slowest: Page 15s, Serve 7s, Bench 5s) / OK [ran] [tree 0f66a6548c41] [world 2f1906870a] (2026-11-04T20:12:39Z)
- (step 3) `sampo shot http://127.0.0.1:46459/?t=yjSjYJlQOgTtECJLdBruYzdfS5m147pHV1_jIeLgQmQ --frames 2 --every 1500 --out /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/live-shots6` → exit 0 · frame-00.png … frame-01.png (2 frames 1500 ms apart, real time) / poster.png (frame-00.png: the most painted of 2) [ran] [tree 144dc967c1bb] [world 2f1906870a] (2026-11-04T20:19:29Z)
- `python3 plugin/tests/run.py test_live` → ✗ exit 1 · Ran 34 tests in 16.5s (9 classes, 16 at a time; slowest: Page 15s, Serve 7s, Snapshot 3s) / FAILED (2 classes: test_live.Snapshot, test_live.Serve) (start tree + this task's tests) [ran] [tree 144dc967c1bb] [world 2f1906870a] (2026-11-04T20:20:06Z)
- `python3 plugin/tests/run.py test_live` → exit 0 · Ran 34 tests in 14.9s (9 classes, 16 at a time; slowest: Page 15s, Serve 6s, Snapshot 3s) / OK [ran] [tree 144dc967c1bb] [world 2f1906870a] (2026-11-04T20:20:06Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T20:20:06Z [ran] [tree 144dc967c1bb] [world 2f1906870a] (2026-11-04T20:20:57Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_models` → exit 0 · Ran 114 tests in 15.5s (23 classes, 16 at a time; slowest: Page 15s, Serve 7s, Snapshot 3s) / OK [ran] [tree 144dc967c1bb] [world 2f1906870a] (2026-11-04T20:20:57Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 34 tests in 15.9s (9 classes, 16 at a time; slowest: Page 15s, Serve 8s, Snapshot 6s) / OK [ran] [tree 144dc967c1bb] [world 2f1906870a] (2026-11-04T20:20:57Z)
- (audit intent) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first (complete and embed log their calls, the CLI hands the path to children, changelog)` → fonts, words and the call log meet the three criteria; complete() and embed() now tested end to end [tree 144dc967c1bb] (2026-11-04T20:20:57Z)
- (audit adversary) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first (complete and embed log their calls, the CLI hands the path to children, changelog)` → _static still takes only flat names with known extensions; the log holds fixed-shape rows (time, model, lowercase verb) [tree 144dc967c1bb] (2026-11-04T20:20:57Z)
- (audit edge) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first (complete and embed log their calls, the CLI hands the path to children, changelog)` → a failed call still logs (row before the request); a child under a temp home logs to the inherited file; rotation past 4 MB keeps one .1 [tree 144dc967c1bb] (2026-11-04T20:20:57Z)
- (audit operator) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first (complete and embed log their calls, the CLI hands the path to children, changelog)` → one ~150 B append per call, ~1.5 MB a busy day, read by a 400-row tail [tree 144dc967c1bb] (2026-11-04T20:20:57Z)
## Log
- 2026-11-04T20:02:29Z created
- 2026-11-04T20:02:41Z set approved=True
- 2026-11-04T20:05:39Z focused
- 2026-11-04T20:05:42Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-04T20:20:11Z scope: cli.py (sets SAMPO_CALLS so exam children log to the real file), helpers.py (tests never log into it), settingsserve.py (_send takes bytes), CHANGELOG and the map entry
- 2026-11-04T20:27:43Z done
- 2026-11-04T20:27:44Z committed 0aab7282 (7 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: upgrade `plugin/web/live/index.html` (the live page) so it renders real runtime data, not fixtures. That means (a) fonts actually served locally by the page's server rather than from a CDN or system fallback, (b) the "ledger" (the cost/event record, probably written by `plugin/lib/fmcore…
- Same request aimed at `site/genesis/index.html` (backed by `plugin/lib/fmgenesis.py`) or `design/sampo/index.html`, the marketing or design surface. The "live page" would be a public demo fed by recorded real data, not a running instance.
- Same request aimed at `plugin/templates/web/index.html`, the scaffold template that generated projects get. The live page would be a template with the font, ledger and animation behaviour baked in for downstream use.
- "Local, Jarvis, Smith" may name three routing tiers or backends, not three animation styles. The animation would then need a per-backend visual identity, and the model-call source must already tag calls with the backend. If it doesn't, that tagging is the real work.
Approaches:
- Add a small stream endpoint (SSE or tail-poll of the ledger file) in whichever server serves `plugin/web/live/`. The page consumes it, maps each ledger record to a sentence via a pure formatter (kept in `plugin/lib/`, so Python tests can cover it), and appends an animated row whose class depends on…
- Render server-side: `fm` writes a snapshot of the ledger as words into the HTML, and the client only animates the delta between polls. This is simpler and works offline, but the page feels less live and the "in words" logic lives in Python only.
- Build the page as a `mods/foreman-ui` React component, reusing its test harness (`claude plugin test mods/foreman-ui`), and embed it in the live page. This gets typed tests, but adds a build step to an otherwise static page.
- Replay-driven: develop against `fm replay` output to produce deterministic animation, then switch the source to the live ledger. That gives a verifiable path before real data is wired in.
Failure modes:
- The ledger schema doesn't record which backend served a call (local vs Jarvis vs Smith), or names them differently across `fmcore.py`, `fmhooks.py` and `fmguard.py`. Animations then default to one style, or the sentences mislabel the backend, and the bug appears only on real data, not fixtures.
- Fonts appear to work because they're installed on the developer's machine. The `@font-face` path is wrong relative to how `plugin/bin/fm` serves the directory, so a clean browser falls back silently. It needs checking with the cache cleared and the system font absent, plus a MIME/CORS check on the …
- The live tail leaks or distorts data: partially written ledger lines get parsed as JSON, rotation or truncation resets the offset, and prompts or secrets from real calls are shown verbatim in the "words" view. The formatter needs to redact, and the reader needs to handle half-written lines.
- Animation cost hits the hook budget or the page: if the ledger writer in `fmhooks.py` is touched, `plugin/tests/bench_hooks.py` regresses. On the page side, unbounded DOM rows from a long ledger will stall the browser unless old entries are capped.
## Dissent
- [x] rival reading: Likeliest: upgrade `plugin/web/live/index.html` (the live page) so it renders real runtime data, not fixtures. That means (a) fonts actually served locally by the page's server rather than from a CDN or system fallback, (b) the "ledger" (the cost/event record, probably written by `plugin/lib/fmcore… — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival reading: Same request aimed at `site/genesis/index.html` (backed by `plugin/lib/fmgenesis.py`) or `design/sampo/index.html`, the marketing or design surface. The "live page" would be a public demo fed by recorded real data, not a running instance. — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival reading: Same request aimed at `plugin/templates/web/index.html`, the scaffold template that generated projects get. The live page would be a template with the font, ledger and animation behaviour baked in for downstream use. — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival reading: "Local, Jarvis, Smith" may name three routing tiers or backends, not three animation styles. The animation would then need a per-backend visual identity, and the model-call source must already tag calls with the backend. If it doesn't, that tagging is the real work. — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival approach: Add a small stream endpoint (SSE or tail-poll of the ledger file) in whichever server serves `plugin/web/live/`. The page consumes it, maps each ledger record to a sentence via a pure formatter (kept in `plugin/lib/`, so Python tests can cover it), and appends an animated row whose class depends on… — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival approach: Render server-side: `fm` writes a snapshot of the ledger as words into the HTML, and the client only animates the delta between polls. This is simpler and works offline, but the page feels less live and the "in words" logic lives in Python only. — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival approach: Build the page as a `mods/foreman-ui` React component, reusing its test harness (`claude plugin test mods/foreman-ui`), and embed it in the live page. This gets typed tests, but adds a build step to an otherwise static page. — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
- [x] rival approach: Replay-driven: develop against `fm replay` output to produce deterministic animation, then switch the source to the live ledger. That gives a verifiable path before real data is wired in. — answered: the live page is plugin/web/live served by sampo watch --web, which already streams SSE; the live shots showed three data gaps on that server, fixed there
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2957 [FEATURE M, done, 3 steps] Re-sync site/ to the converged illustrated forge (critique 7 converged: landing round 7, tower round 4): the redrawn eight stations as …
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar finished tasks took 3–9 steps
## Why not caught
the page test served fixtures from its own static handler and no test fetched a binary; now test_live fetches a woff2 and drives complete/embed into the snapshot
## Lessons
- A live page must be judged on live data: the fixture shots looked complete while fonts 404'd, the ticker printed JSON and no local call reached the scene
## Files touched
- CHANGELOG.md
- docs/map/files-lib-2.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/models.py
- plugin/tests/helpers.py
- plugin/tests/test_live.py
- plugin/lib/sampo/live.py
